"""Tests for harness_eval.parsers.trajectory module."""

import json
import pytest
from pathlib import Path

from harness_eval.parsers.trajectory import (
    ParsedTrajectory,
    TrajectoryMetadata,
    compute_condition_summary,
    parse_condition_dir,
    parse_trajectory_file,
    validate_trajectory,
)
from harness_eval.metrics.tool_dispatch import ToolCall


# ── Fixtures ─────────────────────────────────────────

SAMPLE_TRAJECTORY = {
    "task_id": "django__django-16379",
    "model": "claude-sonnet-4-20250514",
    "resolved": True,
    "config": {
        "tool_level": "full",
        "context_strategy": "full",
        "backend": "claude",
    },
    "condition_id": "full_full_claude",
    "total_cost": 0.27,
    "context_tokens_used": 42150,
    "trajectory": [
        {
            "turn": 1,
            "action": "read",
            "args": {"path": "src/module.py"},
            "output": "class Module: ...",
            "acceptable_tools": ["read", "grep"],
        },
        {
            "turn": 2,
            "action": "edit",
            "args": {"path": "src/module.py"},
            "output": "File edited",
            "acceptable_tools": ["edit", "write"],
        },
        {
            "turn": 3,
            "action": "bash",
            "args": {"command": "pytest"},
            "output": "3 passed",
        },
    ],
}


@pytest.fixture
def sample_file(tmp_path):
    """Write a sample trajectory JSON file and return its path."""
    p = tmp_path / "full_full_claude" / "django__django-16379.json"
    p.parent.mkdir(parents=True)
    p.write_text(json.dumps(SAMPLE_TRAJECTORY), encoding="utf-8")
    return p


@pytest.fixture
def sample_dir(tmp_path):
    """Create a condition dir with multiple trajectory files."""
    cond_dir = tmp_path / "full_full_claude"
    cond_dir.mkdir()

    for i, resolved in enumerate([True, True, False]):
        data = {**SAMPLE_TRAJECTORY, "task_id": f"task_{i:03d}", "resolved": resolved}
        (cond_dir / f"task_{i:03d}.json").write_text(
            json.dumps(data), encoding="utf-8"
        )
    return cond_dir


# ── validate_trajectory ─────────────────────────────

class TestValidateTrajectory:
    def test_valid(self):
        assert validate_trajectory(SAMPLE_TRAJECTORY) == []

    def test_missing_top_fields(self):
        errors = validate_trajectory({"task_id": "x"})
        assert len(errors) >= 1
        assert "Missing top-level fields" in errors[0]

    def test_missing_config_fields(self):
        data = {**SAMPLE_TRAJECTORY, "config": {"tool_level": "full"}}
        errors = validate_trajectory(data)
        assert any("config fields" in e for e in errors)

    def test_config_not_dict(self):
        data = {**SAMPLE_TRAJECTORY, "config": "bad"}
        errors = validate_trajectory(data)
        assert any("must be a dict" in e for e in errors)

    def test_trajectory_not_list(self):
        data = {**SAMPLE_TRAJECTORY, "trajectory": "bad"}
        errors = validate_trajectory(data)
        assert any("must be a list" in e for e in errors)

    def test_turn_missing_fields(self):
        data = {**SAMPLE_TRAJECTORY, "trajectory": [{"turn": 1}]}
        errors = validate_trajectory(data)
        assert any("Turn 0 missing" in e for e in errors)

    def test_turn_not_dict(self):
        data = {**SAMPLE_TRAJECTORY, "trajectory": ["bad"]}
        errors = validate_trajectory(data)
        assert any("Turn 0 is not a dict" in e for e in errors)


# ── parse_trajectory_file ────────────────────────────

class TestParseTrajectoryFile:
    def test_basic_parse(self, sample_file):
        result = parse_trajectory_file(sample_file)
        assert isinstance(result, ParsedTrajectory)
        assert result.metadata.task_id == "django__django-16379"
        assert result.metadata.resolved is True
        assert result.metadata.num_turns == 3
        assert result.metadata.tool_level == "full"
        assert result.metadata.backend == "claude"
        assert result.metadata.total_cost == 0.27
        assert result.metadata.context_tokens_used == 42150

    def test_tool_calls(self, sample_file):
        result = parse_trajectory_file(sample_file)
        assert len(result.tool_calls) == 3
        assert all(isinstance(tc, ToolCall) for tc in result.tool_calls)
        assert result.tool_calls[0].tool_name == "read"
        assert result.tool_calls[0].acceptable_tools == ["read", "grep"]
        assert result.tool_calls[2].acceptable_tools is None

    def test_raw_preserved(self, sample_file):
        result = parse_trajectory_file(sample_file)
        assert result.raw["task_id"] == "django__django-16379"

    def test_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            parse_trajectory_file("/nonexistent/path.json")

    def test_empty_file(self, tmp_path):
        p = tmp_path / "empty.json"
        p.write_text("", encoding="utf-8")
        with pytest.raises(ValueError, match="empty"):
            parse_trajectory_file(p)

    def test_invalid_json(self, tmp_path):
        p = tmp_path / "bad.json"
        p.write_text("{invalid", encoding="utf-8")
        with pytest.raises(ValueError, match="Invalid JSON"):
            parse_trajectory_file(p)

    def test_missing_required_fields(self, tmp_path):
        p = tmp_path / "incomplete.json"
        p.write_text(json.dumps({"task_id": "x"}), encoding="utf-8")
        with pytest.raises(ValueError, match="Invalid trajectory"):
            parse_trajectory_file(p)


# ── parse_condition_dir ──────────────────────────────

class TestParseConditionDir:
    def test_basic(self, sample_dir):
        results = parse_condition_dir(sample_dir)
        assert len(results) == 3
        assert all(isinstance(r, ParsedTrajectory) for r in results)

    def test_sorted_by_task_id(self, sample_dir):
        results = parse_condition_dir(sample_dir)
        ids = [r.metadata.task_id for r in results]
        assert ids == sorted(ids)

    def test_dir_not_found(self):
        with pytest.raises(FileNotFoundError):
            parse_condition_dir("/nonexistent/dir")

    def test_empty_dir(self, tmp_path):
        d = tmp_path / "empty_cond"
        d.mkdir()
        results = parse_condition_dir(d)
        assert results == []


# ── compute_condition_summary ────────────────────────

class TestComputeConditionSummary:
    def test_basic(self, sample_dir):
        trajs = parse_condition_dir(sample_dir)
        summary = compute_condition_summary(trajs)
        assert summary["total_tasks"] == 3
        assert summary["resolved_count"] == 2
        assert abs(summary["resolve_rate"] - 2 / 3) < 1e-10
        assert summary["tool_level"] == "full"
        assert summary["backend"] == "claude"

    def test_empty(self):
        assert compute_condition_summary([]) == {}

    def test_all_resolved(self, tmp_path):
        d = tmp_path / "cond"
        d.mkdir()
        for i in range(3):
            data = {**SAMPLE_TRAJECTORY, "task_id": f"t{i}", "resolved": True}
            (d / f"t{i}.json").write_text(json.dumps(data), encoding="utf-8")
        trajs = parse_condition_dir(d)
        summary = compute_condition_summary(trajs)
        assert summary["resolve_rate"] == 1.0

    def test_none_resolved(self, tmp_path):
        d = tmp_path / "cond"
        d.mkdir()
        for i in range(2):
            data = {**SAMPLE_TRAJECTORY, "task_id": f"t{i}", "resolved": False}
            (d / f"t{i}.json").write_text(json.dumps(data), encoding="utf-8")
        trajs = parse_condition_dir(d)
        summary = compute_condition_summary(trajs)
        assert summary["resolve_rate"] == 0.0
