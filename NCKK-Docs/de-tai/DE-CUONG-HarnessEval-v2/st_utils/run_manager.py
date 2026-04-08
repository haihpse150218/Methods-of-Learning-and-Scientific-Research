"""RunManager: background experiment execution with threading and status tracking.

Wraps harness_eval.pipeline.runner to run experiments in a background thread,
providing thread-safe status polling for Streamlit UIs.
"""

from __future__ import annotations

import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any


class RunManager:
    """Manages background experiment runs using a daemon thread.

    Usage::

        rm = RunManager()
        rm.start(conditions=["full_full_claude"], mode="dry-run",
                 max_tasks=5, output_dir=Path("output"))
        # poll from Streamlit:
        status = rm.get_status()  # {"status", "progress", "logs", "current_condition"}
        rm.stop()   # request cancellation
        rm.clear()  # reset to idle
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._state: dict[str, Any] = self._idle_state()
        self._thread: threading.Thread | None = None
        self._stop_event = threading.Event()
        self._completed_counter: int = 0
        self._total_tasks: int = 0

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def start(
        self,
        conditions: list[str],
        mode: str,
        max_tasks: int,
        output_dir: Path,
        sweagent_dir: Path | None = None,
        parallel: bool = False,
        max_workers: int = 4,
    ) -> None:
        """Start the experiment in a background thread.

        Args:
            conditions: List of condition_id strings (e.g. ["full_full_claude"]).
            mode: "dry-run" for synthetic data, "real" for actual SWE-Agent calls.
            max_tasks: Maximum tasks to run per condition.
            output_dir: Directory where trajectories and summary are saved.
            sweagent_dir: Path to SWE-Agent installation (required for real mode).
            parallel: If True, run conditions concurrently using ThreadPoolExecutor.
            max_workers: Number of parallel workers (default 4, max useful = len(conditions)).

        Raises:
            RuntimeError: If a run is already in progress.
        """
        with self._lock:
            current_status = self._state["status"]
            if current_status == "running":
                raise RuntimeError("A run is already running. Stop it first.")

        # Reset stop event and state
        self._stop_event.clear()
        with self._lock:
            self._state = {
                "status": "running",
                "progress": (0, 0),
                "logs": [],
                "current_condition": "",
            }

        target = self._run_thread_parallel if parallel else self._run_thread
        self._thread = threading.Thread(
            target=target,
            args=(conditions, mode, max_tasks, output_dir, sweagent_dir)
            if not parallel
            else (conditions, mode, max_tasks, output_dir, sweagent_dir, max_workers),
            daemon=True,
            name="RunManager-thread",
        )
        self._thread.start()

    def stop(self) -> None:
        """Signal the background thread to stop after the current task finishes."""
        self._stop_event.set()
        with self._lock:
            if self._state["status"] == "running":
                self._state["status"] = "stopped"

    def get_status(self) -> dict[str, Any]:
        """Return a thread-safe snapshot of the current run status.

        Returns:
            dict with keys:
                - status (str): "idle" | "running" | "done" | "failed" | "stopped"
                - progress (tuple[int, int]): (completed_tasks, total_tasks)
                - logs (list[str]): Log lines accumulated during the run
                - current_condition (str): Currently executing condition_id
        """
        with self._lock:
            return {
                "status": self._state["status"],
                "progress": self._state["progress"],
                "logs": list(self._state["logs"]),  # return a copy
                "current_condition": self._state["current_condition"],
            }

    def clear(self) -> None:
        """Reset to idle state. Signals any running thread to stop first."""
        self._stop_event.set()
        with self._lock:
            self._state = self._idle_state()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _idle_state() -> dict[str, Any]:
        return {
            "status": "idle",
            "progress": (0, 0),
            "logs": [],
            "current_condition": "",
        }

    def _log(self, message: str) -> None:
        """Append a log line thread-safely."""
        with self._lock:
            self._state["logs"].append(message)

    def _set_progress(self, current: int, total: int) -> None:
        with self._lock:
            self._state["progress"] = (current, total)

    def _set_condition(self, cond_id: str) -> None:
        with self._lock:
            self._state["current_condition"] = cond_id

    def _set_status(self, status: str) -> None:
        with self._lock:
            self._state["status"] = status

    # ------------------------------------------------------------------
    # Background thread
    # ------------------------------------------------------------------

    def _run_thread(
        self,
        conditions: list[str],
        mode: str,
        max_tasks: int,
        output_dir: Path,
        sweagent_dir: Path | None,
    ) -> None:
        """Main body of the background thread.

        Builds ExperimentConfig + RunConfig, loads tasks, iterates over
        conditions/tasks, calls PipelineRunner.run_single_task() and
        PipelineRunner.save_trajectory().
        """
        try:
            from harness_eval.configs.experiment import ExperimentConfig
            from harness_eval.pipeline.runner import PipelineRunner, RunConfig

            dry_run = (mode == "dry-run")

            exp = ExperimentConfig()
            run_config = RunConfig(
                output_dir=output_dir,
                dry_run=dry_run,
                max_tasks=max_tasks,
                conditions=conditions,
                sweagent_dir=sweagent_dir,
            )

            runner = PipelineRunner(exp, run_config)

            # Load and cap tasks
            tasks = runner.load_tasks()
            if max_tasks is not None:
                tasks = tasks[:max_tasks]

            # Filter conditions from the full factorial design
            all_conditions = exp.generate_conditions()
            filter_set = set(conditions)
            selected_conditions = [
                c for c in all_conditions if c.condition_id in filter_set
            ]

            total_tasks = len(selected_conditions) * len(tasks)
            completed = 0
            self._set_progress(completed, total_tasks)

            for condition in selected_conditions:
                # Check stop before starting a new condition
                if self._stop_event.is_set():
                    self._set_status("stopped")
                    return

                cond_id = condition.condition_id
                self._set_condition(cond_id)
                self._log(f"Condition: {cond_id}")

                for task_id in tasks:
                    # Check stop before each task
                    if self._stop_event.is_set():
                        self._set_status("stopped")
                        return

                    result = runner.run_single_task(condition, task_id)

                    # Log the result
                    pass_fail = "PASS" if result.resolved else "FAIL"
                    self._log(f"{task_id}: {pass_fail} (${result.total_cost:.4f})")

                    # Save trajectory
                    runner.save_trajectory(result, condition)

                    # Update progress
                    completed += 1
                    self._set_progress(completed, total_tasks)

            # Mark done
            self._set_status("done")

        except Exception as exc:  # noqa: BLE001
            self._log(f"ERROR: {exc}")
            self._set_status("failed")

    # ------------------------------------------------------------------
    # Parallel background thread
    # ------------------------------------------------------------------

    def _run_thread_parallel(
        self,
        conditions: list[str],
        mode: str,
        max_tasks: int,
        output_dir: Path,
        sweagent_dir: Path | None,
        max_workers: int,
    ) -> None:
        """Run conditions in parallel using ThreadPoolExecutor.

        Each condition gets its own PipelineRunner instance to avoid
        shared state issues. Progress is tracked across all workers.
        """
        try:
            from harness_eval.configs.experiment import ExperimentConfig
            from harness_eval.pipeline.runner import PipelineRunner, RunConfig

            dry_run = (mode == "dry-run")
            exp = ExperimentConfig()

            # Filter conditions
            all_conditions = exp.generate_conditions()
            filter_set = set(conditions)
            selected_conditions = [
                c for c in all_conditions if c.condition_id in filter_set
            ]

            # Load tasks once (shared, read-only)
            sample_config = RunConfig(
                output_dir=output_dir, dry_run=dry_run, max_tasks=max_tasks,
            )
            sample_runner = PipelineRunner(exp, sample_config)
            tasks = sample_runner.load_tasks()[:max_tasks]

            total_tasks = len(selected_conditions) * len(tasks)
            self._completed_counter = 0
            self._total_tasks = total_tasks
            self._set_progress(0, total_tasks)
            self._log(f"Starting PARALLEL run: {len(selected_conditions)} conditions x {len(tasks)} tasks ({max_workers} workers)")

            def run_one_condition(condition):
                """Worker function: run all tasks for one condition."""
                cond_id = condition.condition_id
                # Each worker gets its own runner to avoid shared state
                worker_config = RunConfig(
                    output_dir=output_dir,
                    dry_run=dry_run,
                    max_tasks=max_tasks,
                    sweagent_dir=sweagent_dir,
                )
                worker_runner = PipelineRunner(exp, worker_config)

                self._log(f"[{cond_id}] Starting...")

                for task_id in tasks:
                    if self._stop_event.is_set():
                        return cond_id, "stopped"

                    result = worker_runner.run_single_task(condition, task_id)
                    pass_fail = "PASS" if result.resolved else "FAIL"
                    self._log(f"[{cond_id}] {task_id}: {pass_fail} (${result.total_cost:.4f})")
                    worker_runner.save_trajectory(result, condition)

                    # Atomic counter update
                    with self._lock:
                        self._completed_counter += 1
                        self._state["progress"] = (self._completed_counter, self._total_tasks)

                return cond_id, "done"

            # Execute with ThreadPoolExecutor
            effective_workers = min(max_workers, len(selected_conditions))
            with ThreadPoolExecutor(max_workers=effective_workers) as executor:
                futures = {
                    executor.submit(run_one_condition, cond): cond.condition_id
                    for cond in selected_conditions
                }

                for future in as_completed(futures):
                    cond_id = futures[future]
                    if self._stop_event.is_set():
                        break
                    try:
                        result_cid, result_status = future.result()
                        self._log(f"[{result_cid}] Condition complete ({result_status})")
                        self._set_condition(result_cid)
                    except Exception as exc:
                        self._log(f"[{cond_id}] ERROR: {exc}")

            if not self._stop_event.is_set():
                self._set_status("done")
                self._log(f"All {len(selected_conditions)} conditions complete ({self._completed_counter}/{total_tasks} tasks)")
            else:
                self._set_status("stopped")

        except Exception as exc:  # noqa: BLE001
            self._log(f"ERROR: {exc}")
            self._set_status("failed")
