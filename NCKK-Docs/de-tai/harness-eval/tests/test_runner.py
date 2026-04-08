"""Tests for harness_eval.pipeline.runner module."""

import csv
import json
import pytest
from pathlib import Path

from harness_eval.pipeline.runner import (
    ConditionResult,
    PipelineRunner,
    RunConfig,
    TaskResult,
    run_pilot,
    run_full,
)
from harness_eval.configs.experiment import ExperimentConfig, Condition
from harness_eval.configs.tool_config import ToolConfig, ToolLevel
from harness_eval.configs.context_config import ContextConfig, ContextStrategy
from harness_eval.configs.backend_config import BackendConfig, BackendType


# ── TaskResult / ConditionResult ─────────────────────

class TestTaskResult:
    def test_fields(self):
        tr = TaskResult(
            task_id="t1", condition_id="c1", resolved=True,
            trajectory=[], total_cost=0.35, duration_seconds=60.0,
            model="test-model",
        )
        assert tr.task_id == "t1"
        assert tr.resolved is True
        assert tr.total_cost == 0.35


class TestConditionResult:
    def test_empty(self):
        cr = ConditionResult(condition_id="c1")
        assert cr.resolve_rate == 0.0
        assert cr.total_cost == 0.0
        assert cr.avg_duration == 0.0

    def test_with_results(self):
        cr = ConditionResult(
            condition_id="c1",
            task_results=[
                TaskResult("t1", "c1", True, [], 0.3, 60.0, "m"),
                TaskResult("t2", "c1", False, [], 0.4, 80.0, "m"),
                TaskResult("t3", "c1", True, [], 0.2, 40.0, "m"),
            ],
        )
        assert abs(cr.resolve_rate - 2 / 3) < 1e-10
        assert abs(cr.total_cost - 0.9) < 1e-10
        assert abs(cr.avg_duration - 60.0) < 1e-10

    def test_all_resolved(self):
        cr = ConditionResult(
            condition_id="c1",
            task_results=[TaskResult("t1", "c1", True, [], 0.1, 10.0, "m")],
        )
        assert cr.resolve_rate == 1.0


# ── PipelineRunner ───────────────────────────────────

class TestPipelineRunner:
    @pytest.fixture
    def runner(self, tmp_path):
        exp = ExperimentConfig()
        config = RunConfig(
            output_dir=tmp_path / "output",
            dry_run=True,
            max_tasks=3,
            conditions=["full_full_claude"],
        )
        return PipelineRunner(exp, config)

    def test_load_default_tasks(self, runner):
        tasks = runner.load_tasks()
        assert len(tasks) >= 8  # 150 from SWE-bench data, or 8 legacy fallback
        assert "django__django-16379" in tasks

    def test_load_tasks_from_file(self, tmp_path):
        tasks_file = tmp_path / "tasks.json"
        tasks_file.write_text(json.dumps(["t1", "t2", "t3"]), encoding="utf-8")
        exp = ExperimentConfig()
        config = RunConfig(output_dir=tmp_path, dry_run=True, tasks_file=tasks_file)
        runner = PipelineRunner(exp, config)
        assert runner.load_tasks() == ["t1", "t2", "t3"]

    def test_load_tasks_dict_format(self, tmp_path):
        tasks_file = tmp_path / "tasks.json"
        tasks_file.write_text(json.dumps({"task_ids": ["a", "b"]}), encoding="utf-8")
        exp = ExperimentConfig()
        config = RunConfig(output_dir=tmp_path, dry_run=True, tasks_file=tasks_file)
        runner = PipelineRunner(exp, config)
        assert runner.load_tasks() == ["a", "b"]

    def test_run_single_task_dry_run(self, runner):
        condition = Condition(
            tool=ToolConfig(ToolLevel.FULL),
            context=ContextConfig(ContextStrategy.FULL),
            backend=BackendConfig(BackendType.CLAUDE),
        )
        result = runner.run_single_task(condition, "django__django-16379")
        assert isinstance(result, TaskResult)
        assert result.task_id == "django__django-16379"
        assert result.condition_id == "full_full_claude"
        assert isinstance(result.resolved, bool)
        assert len(result.trajectory) >= 4
        assert result.total_cost > 0
        assert result.duration_seconds > 0

    def test_run_single_task_deterministic(self, runner):
        condition = Condition(
            tool=ToolConfig(ToolLevel.FULL),
            context=ContextConfig(ContextStrategy.FULL),
            backend=BackendConfig(BackendType.CLAUDE),
        )
        r1 = runner.run_single_task(condition, "test-task")
        r2 = runner.run_single_task(condition, "test-task")
        assert r1.resolved == r2.resolved
        assert r1.total_cost == r2.total_cost

    def test_run_single_task_real_mode_no_sweagent_dir(self, tmp_path):
        """Real mode without sweagent_dir raises ValueError."""
        exp = ExperimentConfig()
        config = RunConfig(output_dir=tmp_path, dry_run=False)
        runner = PipelineRunner(exp, config)
        condition = Condition(
            tool=ToolConfig(ToolLevel.FULL),
            context=ContextConfig(ContextStrategy.FULL),
            backend=BackendConfig(BackendType.CLAUDE),
        )
        with pytest.raises(ValueError, match="sweagent_dir"):
            runner.run_single_task(condition, "t1")

    def test_run_condition(self, runner):
        condition = Condition(
            tool=ToolConfig(ToolLevel.FULL),
            context=ContextConfig(ContextStrategy.FULL),
            backend=BackendConfig(BackendType.CLAUDE),
        )
        result = runner.run_condition(condition, ["t1", "t2"])
        assert isinstance(result, ConditionResult)
        assert len(result.task_results) == 2
        assert 0.0 <= result.resolve_rate <= 1.0

    def test_run_all(self, runner):
        results = runner.run_all()
        # full_full_claude is critical → 3 runs
        assert len(results) == 3
        for cr in results:
            assert cr.condition_id == "full_full_claude"
            assert len(cr.task_results) == 3  # max_tasks=3

    def test_save_trajectory(self, runner, tmp_path):
        condition = Condition(
            tool=ToolConfig(ToolLevel.FULL),
            context=ContextConfig(ContextStrategy.FULL),
            backend=BackendConfig(BackendType.CLAUDE),
        )
        result = TaskResult(
            task_id="test-task", condition_id="full_full_claude",
            resolved=True, trajectory=[{"turn": 1, "action": "read", "output": "ok"}],
            total_cost=0.35, duration_seconds=60.0, model="test",
            context_tokens_used=40000,
        )
        path = runner.save_trajectory(result, condition)
        assert path.exists()

        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["task_id"] == "test-task"
        assert data["resolved"] is True
        assert data["config"]["tool_level"] == "full"
        assert data["config"]["context_strategy"] == "full"
        assert data["config"]["backend"] == "claude"

    def test_save_summary(self, runner):
        results = [
            ConditionResult("c1", [
                TaskResult("t1", "c1", True, [], 0.3, 60.0, "m"),
                TaskResult("t2", "c1", False, [], 0.4, 80.0, "m"),
            ]),
        ]
        path = runner.save_summary(results)
        assert path.exists()

        with open(path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        assert len(rows) == 1
        assert rows[0]["condition_id"] == "c1"
        assert float(rows[0]["resolve_rate"]) == pytest.approx(0.5, abs=0.01)

    def test_trajectory_has_acceptable_tools(self, runner):
        condition = Condition(
            tool=ToolConfig(ToolLevel.FULL),
            context=ContextConfig(ContextStrategy.FULL),
            backend=BackendConfig(BackendType.CLAUDE),
        )
        result = runner.run_single_task(condition, "test-task")
        for turn in result.trajectory:
            assert "acceptable_tools" in turn
            assert turn["action"] in turn["acceptable_tools"]


# ── Convenience functions ────────────────────────────

class TestSWEAgentIntegration:
    """Tests for real mode SWE-Agent integration (mocked subprocess)."""

    def test_find_traj_file_direct(self, tmp_path):
        traj = tmp_path / "django__django-16379.traj"
        traj.write_text("{}", encoding="utf-8")
        found = PipelineRunner._find_traj_file(tmp_path, "django__django-16379")
        assert found == traj

    def test_find_traj_file_nested(self, tmp_path):
        nested = tmp_path / "subdir"
        nested.mkdir()
        traj = nested / "django__django-16379.traj"
        traj.write_text("{}", encoding="utf-8")
        found = PipelineRunner._find_traj_file(tmp_path, "django__django-16379")
        assert found == traj

    def test_find_traj_file_missing(self, tmp_path):
        found = PipelineRunner._find_traj_file(tmp_path, "nonexistent")
        assert found is None

    def test_run_sweagent_subprocess_failure(self, tmp_path, monkeypatch):
        """When SWE-Agent subprocess fails, returns failed TaskResult."""
        import subprocess as sp

        def mock_run(*args, **kwargs):
            return sp.CompletedProcess(args=args[0], returncode=1, stdout="", stderr="Error occurred")

        monkeypatch.setattr("harness_eval.pipeline.runner.subprocess.run", mock_run)

        exp = ExperimentConfig()
        config = RunConfig(
            output_dir=tmp_path / "output",
            dry_run=False,
            sweagent_dir=tmp_path,
            max_tasks=1,
        )
        runner = PipelineRunner(exp, config)
        condition = Condition(
            tool=ToolConfig(ToolLevel.FULL),
            context=ContextConfig(ContextStrategy.FULL),
            backend=BackendConfig(BackendType.CLAUDE),
        )
        result = runner.run_single_task(condition, "test-task")
        assert result.resolved is False
        assert result.trajectory == []
        assert result.total_cost == 0.0

    def test_run_sweagent_timeout(self, tmp_path, monkeypatch):
        """When SWE-Agent times out, returns failed TaskResult."""
        import subprocess as sp

        def mock_run(*args, **kwargs):
            raise sp.TimeoutExpired(cmd=args[0], timeout=600)

        monkeypatch.setattr("harness_eval.pipeline.runner.subprocess.run", mock_run)

        exp = ExperimentConfig()
        config = RunConfig(
            output_dir=tmp_path / "output",
            dry_run=False,
            sweagent_dir=tmp_path,
        )
        runner = PipelineRunner(exp, config)
        condition = Condition(
            tool=ToolConfig(ToolLevel.FULL),
            context=ContextConfig(ContextStrategy.FULL),
            backend=BackendConfig(BackendType.CLAUDE),
        )
        result = runner.run_single_task(condition, "test-task")
        assert result.resolved is False
        assert result.trajectory == []

    def test_run_sweagent_success_with_traj(self, tmp_path, monkeypatch):
        """When SWE-Agent succeeds and produces .traj, parses it correctly."""
        import subprocess as sp

        # Create a mock .traj file that will be found after subprocess runs
        traj_data = {
            "trajectory": [
                {"action": "open src/module.py", "observation": "class Handler:..."},
                {"action": "edit src/module.py", "observation": "File edited successfully."},
            ],
            "history": [],
            "info": {
                "exit_status": "submitted",
                "model_stats": {"instance_cost": 0.28, "tokens_sent": 45000},
            },
            "replay_config": {
                "agent": {
                    "model": {"name": "claude-sonnet-4-20250514"},
                    "tools": {"bundles": [{"path": "registry"}, {"path": "edit"}, {"path": "filemap"}]},
                    "history_processors": [],
                }
            },
        }

        def mock_run(*args, **kwargs):
            # Write .traj file to output dir (simulating SWE-Agent behavior)
            output_dir = tmp_path / "output" / "full_full_claude"
            output_dir.mkdir(parents=True, exist_ok=True)
            traj_path = output_dir / "test-task.traj"
            traj_path.write_text(json.dumps(traj_data), encoding="utf-8")
            return sp.CompletedProcess(args=args[0], returncode=0, stdout="Done", stderr="")

        monkeypatch.setattr("harness_eval.pipeline.runner.subprocess.run", mock_run)

        exp = ExperimentConfig()
        config = RunConfig(
            output_dir=tmp_path / "output",
            dry_run=False,
            sweagent_dir=tmp_path,
        )
        runner = PipelineRunner(exp, config)
        condition = Condition(
            tool=ToolConfig(ToolLevel.FULL),
            context=ContextConfig(ContextStrategy.FULL),
            backend=BackendConfig(BackendType.CLAUDE),
        )
        result = runner.run_single_task(condition, "test-task")
        assert result.resolved is True
        assert len(result.trajectory) == 2
        assert result.total_cost == pytest.approx(0.28)
        assert result.context_tokens_used == 45000

    def test_run_config_sweagent_fields(self):
        """RunConfig has sweagent_dir, dataset, timeout fields."""
        config = RunConfig(
            output_dir=Path("/tmp"),
            sweagent_dir=Path("/opt/swe-agent"),
            dataset="test-dataset",
            timeout=300,
        )
        assert config.sweagent_dir == Path("/opt/swe-agent")
        assert config.dataset == "test-dataset"
        assert config.timeout == 300


class TestConvenienceFunctions:
    def test_run_pilot(self, tmp_path):
        results = run_pilot(tmp_path / "pilot")
        # 5 critical conditions, some with 3 runs
        assert len(results) >= 5
        summary = tmp_path / "pilot" / "summary.csv"
        assert summary.exists()

    def test_run_pilot_with_max_tasks(self, tmp_path):
        results = run_pilot(tmp_path / "pilot", max_tasks=2)
        for cr in results:
            assert len(cr.task_results) <= 2

    def test_run_full(self, tmp_path):
        results = run_full(tmp_path / "full")
        # 27 conditions, some with 3 runs, max_tasks=8 (default)
        assert len(results) >= 27
        summary = tmp_path / "full" / "summary.csv"
        assert summary.exists()

    def test_run_full_with_max_tasks(self, tmp_path):
        results = run_full(tmp_path / "full", max_tasks=2)
        for cr in results:
            assert len(cr.task_results) <= 2
