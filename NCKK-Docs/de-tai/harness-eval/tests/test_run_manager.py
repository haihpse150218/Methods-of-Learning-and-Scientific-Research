"""Tests for st_utils.run_manager module."""

import time
import pytest
from pathlib import Path

from st_utils.run_manager import RunManager


class TestRunManager:
    def test_initial_state(self):
        rm = RunManager()
        status = rm.get_status()
        assert status["status"] == "idle"
        assert status["progress"] == (0, 0)
        assert status["logs"] == []
        assert status["current_condition"] == ""

    def test_dry_run_pilot(self, tmp_path):
        rm = RunManager()
        rm.start(
            conditions=["full_full_claude"],
            mode="dry-run",
            max_tasks=2,
            output_dir=tmp_path / "output",
        )
        # Wait for completion (up to 6 seconds)
        for _ in range(30):
            if rm.get_status()["status"] in ("done", "failed"):
                break
            time.sleep(0.2)
        status = rm.get_status()
        assert status["status"] == "done"
        assert len(status["logs"]) > 0

    def test_stop(self, tmp_path):
        rm = RunManager()
        rm.start(
            conditions=["full_full_claude"],
            mode="dry-run",
            max_tasks=100,
            output_dir=tmp_path / "output",
        )
        time.sleep(0.3)
        rm.stop()
        assert rm.get_status()["status"] in ("stopped", "done")

    def test_clear(self):
        rm = RunManager()
        rm.clear()
        status = rm.get_status()
        assert status["status"] == "idle"
        assert status["progress"] == (0, 0)
        assert status["logs"] == []

    def test_cannot_start_while_running(self, tmp_path):
        rm = RunManager()
        # Use many conditions so the run doesn't finish instantly
        all_conds = [
            f"{t}_{c}_{b}"
            for t in ["full", "medium", "minimal"]
            for c in ["full", "sliding_window", "summary"]
            for b in ["claude", "gpt", "deepseek"]
        ]
        rm.start(
            conditions=all_conds,
            mode="dry-run",
            max_tasks=8,
            output_dir=tmp_path / "output",
        )
        time.sleep(0.05)
        with pytest.raises(RuntimeError, match="already running"):
            rm.start(
                conditions=["full_full_claude"],
                mode="dry-run",
                max_tasks=2,
                output_dir=tmp_path / "output2",
            )
        rm.stop()

    def test_progress_advances(self, tmp_path):
        rm = RunManager()
        rm.start(
            conditions=["full_full_claude"],
            mode="dry-run",
            max_tasks=3,
            output_dir=tmp_path / "output",
        )
        # Wait for completion
        for _ in range(30):
            if rm.get_status()["status"] in ("done", "failed"):
                break
            time.sleep(0.2)
        status = rm.get_status()
        current, total = status["progress"]
        assert total > 0
        assert current == total

    def test_logs_contain_condition_and_tasks(self, tmp_path):
        rm = RunManager()
        rm.start(
            conditions=["full_full_claude"],
            mode="dry-run",
            max_tasks=2,
            output_dir=tmp_path / "output",
        )
        for _ in range(30):
            if rm.get_status()["status"] in ("done", "failed"):
                break
            time.sleep(0.2)
        logs = rm.get_status()["logs"]
        # Should have at least condition log line
        log_text = "\n".join(logs)
        assert "full_full_claude" in log_text

    def test_clear_after_run(self, tmp_path):
        rm = RunManager()
        rm.start(
            conditions=["full_full_claude"],
            mode="dry-run",
            max_tasks=1,
            output_dir=tmp_path / "output",
        )
        for _ in range(30):
            if rm.get_status()["status"] in ("done", "failed"):
                break
            time.sleep(0.2)
        rm.clear()
        status = rm.get_status()
        assert status["status"] == "idle"
        assert status["logs"] == []
        assert status["progress"] == (0, 0)

    def test_get_status_returns_copy(self):
        rm = RunManager()
        s1 = rm.get_status()
        s2 = rm.get_status()
        # Mutating one should not affect the other
        s1["logs"].append("extra")
        assert "extra" not in rm.get_status()["logs"]
