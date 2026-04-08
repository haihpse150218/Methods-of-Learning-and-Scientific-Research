"""Tests for harness_eval CLI commands."""

import json
import pytest
from pathlib import Path
from click.testing import CliRunner

from harness_eval.cli import main


class TestInfoCommand:
    def test_info_runs(self):
        runner = CliRunner()
        result = runner.invoke(main, ["info"])
        assert result.exit_code == 0
        assert "HarnessEval" in result.output
        assert "27" in result.output  # 27 conditions
        assert "7,050" in result.output  # total evaluations

    def test_info_shows_conditions(self):
        runner = CliRunner()
        result = runner.invoke(main, ["info"])
        assert "full_full_claude" in result.output
        assert "minimal_summary_deepseek" in result.output


class TestPilotCommand:
    def test_pilot_dry_run(self, tmp_path):
        runner = CliRunner()
        output = str(tmp_path / "pilot_out")
        result = runner.invoke(main, ["pilot", "--dry-run", "--output", output, "--max-tasks", "2"])
        assert result.exit_code == 0
        assert "Pilot complete" in result.output
        assert "DRY-RUN" in result.output

    def test_pilot_real_mode_no_sweagent_dir(self):
        runner = CliRunner()
        result = runner.invoke(main, ["pilot", "--output", "/tmp/test"])
        assert result.exit_code != 0
        assert "sweagent-dir" in result.output or "sweagent_dir" in result.output

    def test_pilot_shows_results(self, tmp_path):
        runner = CliRunner()
        output = str(tmp_path / "pilot_out")
        result = runner.invoke(main, ["pilot", "--dry-run", "-o", output, "--max-tasks", "2"])
        assert result.exit_code == 0
        assert "resolve=" in result.output
        assert "cost=$" in result.output


class TestRunCommand:
    def test_run_dry_run_single_condition(self, tmp_path):
        runner = CliRunner()
        output = str(tmp_path / "run_out")
        result = runner.invoke(main, [
            "run", "--dry-run",
            "-o", output,
            "--max-tasks", "2",
            "-c", "full_full_claude",
        ])
        assert result.exit_code == 0
        assert "Experiment complete" in result.output
        assert "full_full_claude" in result.output

    def test_run_real_mode_no_sweagent_dir(self):
        runner = CliRunner()
        result = runner.invoke(main, ["run", "-o", "/tmp/test"])
        assert result.exit_code != 0

    def test_run_dry_run_multiple_conditions(self, tmp_path):
        runner = CliRunner()
        output = str(tmp_path / "run_out")
        result = runner.invoke(main, [
            "run", "--dry-run",
            "-o", output,
            "--max-tasks", "2",
            "-c", "full_full_claude",
            "-c", "minimal_summary_deepseek",
        ])
        assert result.exit_code == 0
        assert "full_full_claude" in result.output
        assert "minimal_summary_deepseek" in result.output


class TestConvertCommand:
    def test_convert_traj_file(self, tmp_path):
        # Create a mock .traj file
        traj_data = {
            "trajectory": [
                {"action": "open src/module.py", "observation": "class Handler:..."},
            ],
            "history": [],
            "info": {
                "exit_status": "submitted",
                "model_stats": {"instance_cost": 0.28, "tokens_sent": 45000},
            },
            "replay_config": {
                "agent": {
                    "model": {"name": "gpt-4o"},
                    "tools": {"bundles": [{"path": "registry"}, {"path": "edit"}]},
                    "history_processors": [],
                }
            },
        }
        traj_path = tmp_path / "test.traj"
        traj_path.write_text(json.dumps(traj_data), encoding="utf-8")

        runner = CliRunner()
        result = runner.invoke(main, ["convert", str(traj_path)])
        assert result.exit_code == 0
        output = json.loads(result.output)
        assert "task_id" in output
        assert "trajectory" in output

    def test_convert_to_file(self, tmp_path):
        traj_data = {
            "trajectory": [{"action": "bash ls", "observation": "file.py"}],
            "history": [],
            "info": {"exit_status": "submitted", "model_stats": {}},
            "replay_config": {"agent": {"model": {"name": "claude"}, "tools": {}, "history_processors": []}},
        }
        traj_path = tmp_path / "input.traj"
        traj_path.write_text(json.dumps(traj_data), encoding="utf-8")
        output_path = tmp_path / "output.json"

        runner = CliRunner()
        result = runner.invoke(main, ["convert", str(traj_path), "-o", str(output_path)])
        assert result.exit_code == 0
        assert output_path.exists()


class TestAnalyzeCommand:
    def test_analyze_trajectory_dir(self, tmp_path):
        # Need full 3x3x3 factorial data for three-way ANOVA
        tools = ["full", "medium", "minimal"]
        contexts = ["full", "sliding_window", "summary"]
        backends = ["claude", "gpt", "deepseek"]
        import itertools
        for tool, ctx, backend in itertools.product(tools, contexts, backends):
            cond_name = f"{tool}_{ctx}_{backend}"
            cd = tmp_path / cond_name
            cd.mkdir()
            for i in range(3):
                traj = {
                    "task_id": f"task-{i}",
                    "model": "test-model",
                    "resolved": (hash(f"{tool}{ctx}{backend}{i}") % 3) != 0,
                    "config": {"tool_level": tool, "context_strategy": ctx, "backend": backend},
                    "condition_id": cond_name,
                    "total_cost": 0.30,
                    "context_tokens_used": 40000,
                    "trajectory": [{"turn": 1, "action": "bash", "output": "ok"}],
                }
                (cd / f"task-{i}.json").write_text(json.dumps(traj), encoding="utf-8")

        runner = CliRunner()
        result = runner.invoke(main, ["analyze", str(tmp_path)])
        assert result.exit_code == 0
        assert "Tool" in result.output

    def test_analyze_empty_dir(self, tmp_path):
        runner = CliRunner()
        result = runner.invoke(main, ["analyze", str(tmp_path)])
        assert result.exit_code != 0
