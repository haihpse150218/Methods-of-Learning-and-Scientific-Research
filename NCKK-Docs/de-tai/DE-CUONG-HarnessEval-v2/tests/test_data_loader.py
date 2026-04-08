"""Tests for st_utils/data_loader.py — trajectory scanning and metrics."""

import json
from pathlib import Path

import pandas as pd
import pytest

from st_utils.data_loader import (
    build_anova_dataframe,
    compute_metrics_for_log,
    load_trajectory,
    scan_trajectories,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_trajectory(
    tmp_path: Path,
    condition_id: str,
    task_id: str,
    resolved: bool = True,
    model: str = "claude-sonnet-4",
    total_cost: float = 0.30,
    context_tokens_used: int = 10000,
    tool_level: str = "full",
    context_strategy: str = "full",
    backend: str = "claude",
    turns: list[dict] | None = None,
) -> Path:
    """Write a minimal trajectory JSON to tmp_path/<condition_id>/<task_id>.json."""
    if turns is None:
        turns = [
            {
                "turn": 1,
                "action": "read",
                "output": "some file content here",
                "acceptable_tools": ["read", "grep"],
            },
            {
                "turn": 2,
                "action": "grep",
                "output": "some file content here matched",
                "acceptable_tools": ["grep", "read"],
            },
        ]

    cond_dir = tmp_path / condition_id
    cond_dir.mkdir(parents=True, exist_ok=True)
    log = {
        "task_id": task_id,
        "model": model,
        "resolved": resolved,
        "config": {
            "tool_level": tool_level,
            "context_strategy": context_strategy,
            "backend": backend,
        },
        "condition_id": condition_id,
        "total_cost": total_cost,
        "context_tokens_used": context_tokens_used,
        "trajectory": turns,
    }
    path = cond_dir / f"{task_id}.json"
    path.write_text(json.dumps(log), encoding="utf-8")
    return path


# ===========================================================================
# TestScanTrajectories
# ===========================================================================


class TestScanTrajectories:
    def test_returns_metadata_keys(self, tmp_path):
        """Each item in the result list must have the required metadata keys."""
        _make_trajectory(tmp_path, "full_full_claude", "django__django-001")
        result = scan_trajectories(tmp_path)

        assert len(result) == 1
        item = result[0]
        required_keys = {"condition_id", "task_id", "resolved", "model", "total_cost", "num_turns", "path"}
        assert required_keys.issubset(item.keys())

    def test_scans_multiple_conditions(self, tmp_path):
        """Should scan all condition subdirectories and aggregate results."""
        _make_trajectory(tmp_path, "full_full_claude", "task-A")
        _make_trajectory(tmp_path, "minimal_full_claude", "task-A")
        _make_trajectory(tmp_path, "minimal_full_claude", "task-B")

        result = scan_trajectories(tmp_path)
        assert len(result) == 3

        condition_ids = {r["condition_id"] for r in result}
        assert condition_ids == {"full_full_claude", "minimal_full_claude"}

    def test_metadata_values_are_correct(self, tmp_path):
        """Spot-check that metadata values are extracted accurately."""
        _make_trajectory(
            tmp_path,
            condition_id="medium_summary_gpt",
            task_id="flask__flask-001",
            resolved=False,
            model="gpt-4o",
            total_cost=0.45,
            turns=[{"turn": 1, "action": "read", "output": "x", "acceptable_tools": ["read"]}],
        )
        result = scan_trajectories(tmp_path)
        assert len(result) == 1
        item = result[0]
        assert item["condition_id"] == "medium_summary_gpt"
        assert item["task_id"] == "flask__flask-001"
        assert item["resolved"] is False
        assert item["model"] == "gpt-4o"
        assert item["total_cost"] == pytest.approx(0.45)
        assert item["num_turns"] == 1
        assert isinstance(item["path"], Path)


# ===========================================================================
# TestLoadTrajectory
# ===========================================================================


class TestLoadTrajectory:
    def test_load_returns_dict_with_expected_fields(self, tmp_path):
        """load_trajectory should return the parsed JSON as a dict."""
        path = _make_trajectory(tmp_path, "full_full_claude", "sympy__sympy-001")
        log = load_trajectory(path)

        assert isinstance(log, dict)
        assert log["task_id"] == "sympy__sympy-001"
        assert log["condition_id"] == "full_full_claude"
        assert "trajectory" in log
        assert isinstance(log["trajectory"], list)


# ===========================================================================
# TestComputeMetrics
# ===========================================================================


class TestComputeMetrics:
    def _make_log_with_turns(self, turns: list[dict], tool_level: str = "full") -> dict:
        return {
            "task_id": "test-task",
            "model": "claude",
            "resolved": True,
            "config": {
                "tool_level": tool_level,
                "context_strategy": "full",
                "backend": "claude",
            },
            "condition_id": f"{tool_level}_full_claude",
            "total_cost": 0.1,
            "context_tokens_used": 5000,
            "trajectory": turns,
        }

    def test_metric_result_structure(self):
        """Each metric result must have value, label, dim, detail keys."""
        turns = [
            {"turn": 1, "action": "read", "output": "data", "acceptable_tools": ["read"]},
            {"turn": 2, "action": "grep", "output": "data found", "acceptable_tools": ["grep"]},
        ]
        log = self._make_log_with_turns(turns)
        metrics = compute_metrics_for_log(log)

        expected_metric_ids = {"m11", "m12", "m13", "m22"}
        assert set(metrics.keys()) == expected_metric_ids

        for key, val in metrics.items():
            assert "value" in val, f"{key} missing 'value'"
            assert "label" in val, f"{key} missing 'label'"
            assert "dim" in val, f"{key} missing 'dim'"
            assert "detail" in val, f"{key} missing 'detail'"
            assert isinstance(val["value"], float), f"{key} value must be float"
            assert 0.0 <= val["value"] <= 1.0, f"{key} value out of [0,1]: {val['value']}"

    def test_metrics_with_known_inputs(self):
        """M1.1 should be 1.0 when all tool choices match acceptable_tools."""
        turns = [
            {"turn": 1, "action": "read", "output": "content A", "acceptable_tools": ["read"]},
            {"turn": 2, "action": "edit", "output": "content A modified", "acceptable_tools": ["edit"]},
        ]
        log = self._make_log_with_turns(turns, tool_level="full")
        metrics = compute_metrics_for_log(log)

        assert metrics["m11"]["value"] == pytest.approx(1.0)
        # m13: 2 unique tools used / 12 full tools = 2/12
        assert metrics["m13"]["value"] == pytest.approx(2 / 12)


# ===========================================================================
# TestBuildAnovaDataframe
# ===========================================================================


class TestBuildAnovaDataframe:
    def test_dataframe_columns_and_rows(self, tmp_path):
        """build_anova_dataframe should return a DataFrame with required columns."""
        _make_trajectory(tmp_path, "full_full_claude", "task-1", resolved=True, total_cost=0.30)
        _make_trajectory(tmp_path, "full_full_claude", "task-2", resolved=False, total_cost=0.20)
        _make_trajectory(tmp_path, "minimal_full_claude", "task-1", resolved=True, total_cost=0.10)

        df = build_anova_dataframe(tmp_path)

        assert isinstance(df, pd.DataFrame)
        required_cols = {"task_id", "condition_id", "tool_config", "context_strategy", "backend", "resolve_rate", "total_cost"}
        assert required_cols.issubset(df.columns)

        # One row per trajectory file scanned
        assert len(df) == 3

        # resolve_rate should be 0.0 or 1.0 (per-trajectory binary)
        assert set(df["resolve_rate"].unique()).issubset({0.0, 1.0})

        # Spot-check parsed config columns
        full_claude_rows = df[df["condition_id"] == "full_full_claude"]
        assert (full_claude_rows["tool_config"] == "full").all()
        assert (full_claude_rows["backend"] == "claude").all()
