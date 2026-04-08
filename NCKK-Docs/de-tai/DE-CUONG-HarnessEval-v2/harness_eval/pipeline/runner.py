"""Pipeline runner for HarnessEval experiments.

Orchestrates running one or more conditions:
1. Generate/load task list from SWE-Bench
2. For each condition: configure harness, run agent on each task, collect trajectory
3. Save trajectory JSON to output directory
4. Aggregate results for analysis
"""

from __future__ import annotations

import csv
import hashlib
import json
import logging
import random
import subprocess
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from harness_eval.configs.experiment import (
    CRITICAL_CONDITIONS,
    Condition,
    ExperimentConfig,
)

logger = logging.getLogger("harness_eval.runner")

# Default SWE-bench task IDs used when no tasks_file is provided
DEFAULT_TASK_IDS = [
    "django__django-16379",
    "django__django-15388",
    "flask__flask-4992",
    "requests__requests-6028",
    "sympy__sympy-20442",
    "scikit-learn__scikit-learn-25638",
    "matplotlib__matplotlib-25311",
    "pytest__pytest-11143",
]

# Synthetic trajectory templates for dry-run mode
_ACTIONS = [
    ("read", {"path": "src/module.py"}),
    ("grep", {"pattern": "def handle_request", "path": "src/"}),
    ("read", {"path": "src/module.py", "offset": 120, "limit": 40}),
    ("edit", {
        "path": "src/module.py",
        "old_string": "    return result",
        "new_string": "    if result is None:\n        return default\n    return result",
    }),
    ("bash", {"command": "cd /repo && python -m pytest tests/ -x -q 2>&1 | tail -5"}),
]


@dataclass
class TaskResult:
    """Result from running one task under one condition."""

    task_id: str
    condition_id: str
    resolved: bool
    trajectory: list[dict]
    total_cost: float
    duration_seconds: float
    model: str
    context_tokens_used: int = 0


@dataclass
class ConditionResult:
    """Aggregated results for one condition."""

    condition_id: str
    task_results: list[TaskResult] = field(default_factory=list)

    @property
    def resolve_rate(self) -> float:
        if not self.task_results:
            return 0.0
        return sum(1 for r in self.task_results if r.resolved) / len(self.task_results)

    @property
    def total_cost(self) -> float:
        return sum(r.total_cost for r in self.task_results)

    @property
    def avg_duration(self) -> float:
        if not self.task_results:
            return 0.0
        return sum(r.duration_seconds for r in self.task_results) / len(self.task_results)


@dataclass
class RunConfig:
    """Configuration for a pipeline run."""

    output_dir: Path
    tasks_file: Path | None = None
    dry_run: bool = False
    max_tasks: int | None = None
    conditions: list[str] | None = None
    verbose: bool = False
    sweagent_dir: Path | None = None  # Path to SWE-Agent installation
    dataset: str = "princeton-nlp/SWE-bench_Verified"  # SWE-bench dataset
    timeout: int = 600  # Per-task timeout in seconds


class PipelineRunner:
    """Runs HarnessEval experiment pipeline."""

    def __init__(self, experiment: ExperimentConfig, run_config: RunConfig):
        self.experiment = experiment
        self.config = run_config
        self.logger = logger

        if self.config.verbose:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run_all(self) -> list[ConditionResult]:
        """Run all (or filtered) conditions and save results."""
        tasks = self.load_tasks()
        if self.config.max_tasks is not None:
            tasks = tasks[: self.config.max_tasks]

        all_conditions = self.experiment.generate_conditions()

        # Filter conditions if requested
        if self.config.conditions is not None:
            filter_set = set(self.config.conditions)
            all_conditions = [c for c in all_conditions if c.condition_id in filter_set]

        self.logger.info(
            "Starting pipeline: %d conditions x %d tasks (dry_run=%s)",
            len(all_conditions),
            len(tasks),
            self.config.dry_run,
        )

        results: list[ConditionResult] = []
        for i, condition in enumerate(all_conditions, 1):
            runs = self.experiment.runs_for_condition(condition)
            self.logger.info(
                "[%d/%d] Condition %s (%d run(s))",
                i,
                len(all_conditions),
                condition.condition_id,
                runs,
            )
            for run_idx in range(runs):
                if runs > 1:
                    self.logger.info("  Run %d/%d", run_idx + 1, runs)
                cond_result = self.run_condition(condition, tasks)
                results.append(cond_result)

                # Save individual trajectories
                for tr in cond_result.task_results:
                    self.save_trajectory(tr, condition)

        summary_path = self.save_summary(results)
        self.logger.info("Summary saved to %s", summary_path)
        return results

    def run_condition(self, condition: Condition, tasks: list[str]) -> ConditionResult:
        """Run one condition on a list of task IDs."""
        cond_result = ConditionResult(condition_id=condition.condition_id)
        for task_id in tasks:
            result = self.run_single_task(condition, task_id)
            cond_result.task_results.append(result)
            self.logger.debug(
                "  %s -> %s (cost=$%.3f, %.1fs)",
                task_id,
                "PASS" if result.resolved else "FAIL",
                result.total_cost,
                result.duration_seconds,
            )
        self.logger.info(
            "  Condition %s: resolve_rate=%.1f%% cost=$%.2f",
            condition.condition_id,
            cond_result.resolve_rate * 100,
            cond_result.total_cost,
        )
        return cond_result

    def run_single_task(self, condition: Condition, task_id: str) -> TaskResult:
        """Run a single task.

        In dry_run mode: generates synthetic results with deterministic randomness.
        In real mode: calls SWE-Agent via subprocess, parses .traj output.
        """
        if self.config.dry_run:
            return self._generate_synthetic_result(condition, task_id)

        return self._run_sweagent_task(condition, task_id)

    # ------------------------------------------------------------------
    # SWE-Agent integration (real mode)
    # ------------------------------------------------------------------

    def _run_sweagent_task(self, condition: Condition, task_id: str) -> TaskResult:
        """Run a single task via SWE-Agent subprocess.

        Composes config YAMLs, calls `sweagent run`, parses .traj output.
        """
        from harness_eval.harness.factory import create_harness_config
        from harness_eval.parsers.trajectory import parse_sweagent_traj

        sweagent_dir = self.config.sweagent_dir
        if sweagent_dir is None:
            raise ValueError(
                "sweagent_dir must be set in RunConfig for real mode. "
                "Point it to your SWE-Agent installation directory."
            )

        # Build HarnessConfig to get YAML paths
        harness_cfg = create_harness_config(
            condition.tool.level, condition.context.strategy, condition.backend.backend
        )

        # Output dir for this condition's trajectories
        cond_output = self.config.output_dir / condition.condition_id
        cond_output.mkdir(parents=True, exist_ok=True)

        # Compose SWE-Agent command
        cmd = [
            "python", "-m", "sweagent", "run",
            "--data_path", task_id,
            "--dataset_name", self.config.dataset,
            "--output_dir", str(cond_output),
        ]
        for cfg_path in harness_cfg.sweagent_config_paths:
            cmd.extend(["--config", str(sweagent_dir / cfg_path)])

        self.logger.info("  Running SWE-Agent: %s", " ".join(cmd))

        start_time = time.time()
        try:
            proc = subprocess.run(
                cmd,
                cwd=str(sweagent_dir),
                capture_output=True,
                text=True,
                timeout=self.config.timeout,
            )
            duration = time.time() - start_time

            if proc.returncode != 0:
                self.logger.warning(
                    "  SWE-Agent failed for %s (exit=%d): %s",
                    task_id, proc.returncode, proc.stderr[-500:] if proc.stderr else "no stderr"
                )
                return TaskResult(
                    task_id=task_id,
                    condition_id=condition.condition_id,
                    resolved=False,
                    trajectory=[],
                    total_cost=0.0,
                    duration_seconds=round(duration, 1),
                    model=condition.backend.model_id,
                )
        except subprocess.TimeoutExpired:
            duration = time.time() - start_time
            self.logger.warning("  SWE-Agent timed out for %s after %ds", task_id, self.config.timeout)
            return TaskResult(
                task_id=task_id,
                condition_id=condition.condition_id,
                resolved=False,
                trajectory=[],
                total_cost=0.0,
                duration_seconds=round(duration, 1),
                model=condition.backend.model_id,
            )

        # Find and parse .traj output file
        traj_file = self._find_traj_file(cond_output, task_id)
        if traj_file is None:
            self.logger.warning("  No .traj file found for %s in %s", task_id, cond_output)
            return TaskResult(
                task_id=task_id,
                condition_id=condition.condition_id,
                resolved=False,
                trajectory=[],
                total_cost=0.0,
                duration_seconds=round(duration, 1),
                model=condition.backend.model_id,
            )

        # Parse .traj and convert to TaskResult
        parsed = parse_sweagent_traj(traj_file)

        # Convert to our JSON format and save
        trajectory_data = parsed.raw.get("trajectory", [])

        result = TaskResult(
            task_id=task_id,
            condition_id=condition.condition_id,
            resolved=parsed.metadata.resolved,
            trajectory=trajectory_data,
            total_cost=parsed.metadata.total_cost,
            duration_seconds=round(duration, 1),
            model=parsed.metadata.model or condition.backend.model_id,
            context_tokens_used=parsed.metadata.context_tokens_used,
        )

        return result

    @staticmethod
    def _find_traj_file(output_dir: Path, task_id: str) -> Path | None:
        """Find the .traj file for a given task in the output directory.

        SWE-Agent typically writes to: output_dir/<task_id>.traj
        or nested: output_dir/<subdir>/<task_id>.traj
        """
        # Direct match
        direct = output_dir / f"{task_id}.traj"
        if direct.exists():
            return direct

        # Search recursively
        matches = list(output_dir.rglob(f"*{task_id}*.traj"))
        if matches:
            return matches[0]

        return None

    def save_trajectory(self, result: TaskResult, condition: Condition) -> Path:
        """Save a TaskResult as trajectory JSON matching app/trajectories/ format."""
        out_dir = self.config.output_dir / condition.condition_id
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"{result.task_id}.json"

        payload = {
            "task_id": result.task_id,
            "model": result.model,
            "resolved": result.resolved,
            "config": {
                "tool_level": condition.tool.level.value,
                "context_strategy": condition.context.strategy.value,
                "backend": condition.backend.backend.value,
            },
            "condition_id": result.condition_id,
            "total_cost": round(result.total_cost, 4),
            "context_tokens_used": result.context_tokens_used,
            "trajectory": result.trajectory,
        }

        out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        self.logger.debug("Saved trajectory -> %s", out_path)
        return out_path

    def save_summary(self, results: list[ConditionResult]) -> Path:
        """Save aggregated summary CSV to output_dir/summary.csv."""
        self.config.output_dir.mkdir(parents=True, exist_ok=True)
        out_path = self.config.output_dir / "summary.csv"

        fieldnames = [
            "condition_id",
            "resolve_rate",
            "total_cost",
            "avg_duration",
            "num_tasks",
        ]

        with open(out_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for cr in results:
                writer.writerow({
                    "condition_id": cr.condition_id,
                    "resolve_rate": f"{cr.resolve_rate:.4f}",
                    "total_cost": f"{cr.total_cost:.2f}",
                    "avg_duration": f"{cr.avg_duration:.1f}",
                    "num_tasks": len(cr.task_results),
                })

        return out_path

    def load_tasks(self) -> list[str]:
        """Load task IDs from tasks_file or return default SWE-bench sample IDs."""
        if self.config.tasks_file is not None:
            self.logger.info("Loading tasks from %s", self.config.tasks_file)
            data = json.loads(self.config.tasks_file.read_text(encoding="utf-8"))
            if isinstance(data, list):
                return data
            # Support {"task_ids": [...]} format
            if isinstance(data, dict) and "task_ids" in data:
                return data["task_ids"]
            raise ValueError(
                f"Unexpected tasks file format: expected list or dict with 'task_ids' key"
            )
        self.logger.info("Using default sample task IDs (%d tasks)", len(DEFAULT_TASK_IDS))
        return list(DEFAULT_TASK_IDS)

    # ------------------------------------------------------------------
    # Synthetic data generation (dry-run only)
    # ------------------------------------------------------------------

    def _generate_synthetic_result(
        self, condition: Condition, task_id: str
    ) -> TaskResult:
        """Generate a realistic synthetic TaskResult for dry-run mode.

        Uses a deterministic seed derived from condition_id + task_id so repeated
        runs with the same inputs produce the same outputs.

        Simulates realistic patterns from SWE-bench literature:
        - Task difficulty varies by repo (django=easier, sympy=harder)
        - Tool level has largest effect (~8% eta-squared)
        - Context strategy has medium effect (~3%)
        - Backend has small effect (~1%)
        - Interaction effects: minimal tools + summary context = extra penalty
        - Noise: per-task random variation
        """
        seed = int(
            hashlib.md5(
                f"{condition.condition_id}:{task_id}".encode()
            ).hexdigest()[:8],
            16,
        )
        rng = random.Random(seed)

        # Task difficulty based on task_id (simulates repo difficulty)
        task_seed = int(hashlib.md5(task_id.encode()).hexdigest()[:8], 16)
        task_rng = random.Random(task_seed)
        task_difficulty = task_rng.gauss(0, 0.08)  # Per-task random intercept

        # Main effects (calibrated for realistic eta-squared)
        # Tool: largest effect (H1) — ~8% variance
        tool_mod = {"full": 0.12, "medium": 0.02, "minimal": -0.14}
        # Context: medium effect (H2) — ~3% variance
        ctx_mod = {"full": 0.06, "sliding_window": 0.01, "summary": -0.07}
        # Backend: small effect — ~1% variance
        backend_mod = {"claude": 0.04, "gpt": 0.01, "deepseek": -0.03}

        tool_val = condition.tool.level.value
        ctx_val = condition.context.strategy.value
        be_val = condition.backend.backend.value

        # Interaction effects (H4)
        interaction = 0.0
        # Minimal tools + summary context = extra penalty (tools can't compensate)
        if tool_val == "minimal" and ctx_val == "summary":
            interaction = -0.06
        # Full tools + full context = slight synergy
        if tool_val == "full" and ctx_val == "full":
            interaction = 0.03
        # DeepSeek struggles more with minimal tools
        if tool_val == "minimal" and be_val == "deepseek":
            interaction = -0.04

        # Base rate ~55% (SWE-bench Verified baseline)
        base_rate = 0.55
        noise = rng.gauss(0, 0.05)  # Per-run noise

        resolve_prob = max(0.05, min(0.95,
            base_rate
            + task_difficulty
            + tool_mod.get(tool_val, 0.0)
            + ctx_mod.get(ctx_val, 0.0)
            + backend_mod.get(be_val, 0.0)
            + interaction
            + noise
        ))
        resolved = rng.random() < resolve_prob

        # Cost varies by backend + task complexity
        cost_base = condition.backend.cost_per_eval
        cost_multiplier = rng.uniform(0.6, 1.5)
        if not resolved:
            cost_multiplier *= 1.2  # Failed tasks often cost more (more retries)
        total_cost = cost_base * cost_multiplier

        # Duration: harder tasks take longer
        base_duration = 60.0 if resolved else 120.0
        duration = base_duration * rng.uniform(0.5, 2.0)

        # Context tokens: more with full context, less with summary
        ctx_tokens_base = {"full": 60_000, "sliding_window": 40_000, "summary": 15_000}
        context_tokens = int(ctx_tokens_base.get(ctx_val, 40_000) * rng.uniform(0.7, 1.3))

        # Build synthetic trajectory
        num_turns = rng.randint(4, 10)
        trajectory = self._generate_synthetic_trajectory(
            rng, condition, task_id, num_turns, resolved
        )

        return TaskResult(
            task_id=task_id,
            condition_id=condition.condition_id,
            resolved=resolved,
            trajectory=trajectory,
            total_cost=round(total_cost, 4),
            duration_seconds=round(duration, 1),
            model=condition.backend.model_id,
            context_tokens_used=context_tokens,
        )

    def _generate_synthetic_trajectory(
        self,
        rng: random.Random,
        condition: Condition,
        task_id: str,
        num_turns: int,
        resolved: bool,
    ) -> list[dict]:
        """Build a synthetic trajectory matching the app/trajectories/ format."""
        available_tools = condition.tool.tools
        base_time = datetime(2026, 5, 1, 10, 0, 0, tzinfo=timezone.utc)
        trajectory = []

        for turn_idx in range(1, num_turns + 1):
            # Pick a plausible action from the condition's available tools
            action = rng.choice(available_tools)
            timestamp = base_time.timestamp() + turn_idx * rng.randint(3, 15)
            ts_str = datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime(
                "%Y-%m-%dT%H:%M:%S"
            )

            turn: dict = {
                "turn": turn_idx,
                "action": action,
                "args": self._synthetic_args(rng, action, task_id),
                "output": self._synthetic_output(rng, action, resolved and turn_idx == num_turns),
                "acceptable_tools": _pick_acceptable_tools(rng, action, available_tools),
                "timestamp": ts_str,
            }
            trajectory.append(turn)

        return trajectory

    @staticmethod
    def _synthetic_args(rng: random.Random, action: str, task_id: str) -> dict:
        """Return plausible args dict for a given action."""
        repo = task_id.split("__")[0] if "__" in task_id else "repo"
        match action:
            case "read":
                return {"path": f"{repo}/core/module.py"}
            case "write":
                return {"path": f"{repo}/core/module.py", "content": "# patched"}
            case "edit":
                return {
                    "path": f"{repo}/core/module.py",
                    "old_string": "    return result",
                    "new_string": "    if result is None:\n        return default\n    return result",
                }
            case "grep":
                return {"pattern": "def process", "path": f"{repo}/"}
            case "glob":
                return {"pattern": f"{repo}/**/test*.py"}
            case "find":
                return {"path": f"{repo}/", "name": "*.py"}
            case "bash":
                return {"command": "cd /repo && python -m pytest tests/ -x -q 2>&1 | tail -5"}
            case "python":
                return {"code": "print('test')"}
            case "git_diff":
                return {}
            case "git_log":
                return {"n": 5}
            case "git_show":
                return {"ref": "HEAD"}
            case "test_runner":
                return {"test_path": "tests/"}
            case _:
                return {}

    @staticmethod
    def _synthetic_output(rng: random.Random, action: str, is_final_pass: bool) -> str:
        """Return plausible output string."""
        if action in ("bash", "test_runner") and is_final_pass:
            n = rng.randint(10, 200)
            return f"{'.' * min(n, 30)}\n{n} passed in {rng.uniform(0.5, 30.0):.2f}s"
        if action == "read":
            return "class Handler:\n    def process(self, request):\n        ..."
        if action == "grep":
            lines = rng.randint(1, 5)
            return "\n".join(f"line {rng.randint(1, 500)}: def process_{i}()" for i in range(lines))
        if action == "edit":
            return "File edited successfully."
        if action == "git_diff":
            return "+    if result is None:\n+        return default"
        return "ok"


def _pick_acceptable_tools(
    rng: random.Random, action: str, available: list[str]
) -> list[str]:
    """Return a short list of acceptable tools for a turn (includes the chosen action)."""
    others = [t for t in available if t != action]
    extras = rng.sample(others, min(rng.randint(1, 2), len(others)))
    return [action] + extras


# ------------------------------------------------------------------
# Convenience functions
# ------------------------------------------------------------------


def run_pilot(
    output_dir: Path,
    dry_run: bool = True,
    sweagent_dir: Path | None = None,
    max_tasks: int | None = None,
) -> list[ConditionResult]:
    """Run pilot study: first 5 critical conditions x pilot_tasks tasks.

    Args:
        output_dir: Where to save trajectory JSON files.
        dry_run: If True, generate synthetic data. If False, call SWE-Agent.
        sweagent_dir: Path to SWE-Agent installation (required if dry_run=False).
        max_tasks: Override number of tasks per condition (default: pilot_tasks from config).
    """
    exp = ExperimentConfig()
    # Pick first 5 critical condition IDs
    all_conditions = exp.generate_conditions()
    critical = [
        c for c in all_conditions
        if (c.tool.level.value, c.context.strategy.value, c.backend.backend.value)
        in CRITICAL_CONDITIONS
    ][:5]
    condition_ids = [c.condition_id for c in critical]

    config = RunConfig(
        output_dir=output_dir,
        dry_run=dry_run,
        max_tasks=max_tasks if max_tasks is not None else exp.pilot_tasks,
        conditions=condition_ids,
        sweagent_dir=sweagent_dir,
    )
    runner = PipelineRunner(exp, config)
    return runner.run_all()


def run_full(
    output_dir: Path,
    dry_run: bool = True,
    sweagent_dir: Path | None = None,
    max_tasks: int | None = None,
) -> list[ConditionResult]:
    """Run full experiment: all 27 conditions.

    Args:
        output_dir: Where to save trajectory JSON files.
        dry_run: If True, generate synthetic data. If False, call SWE-Agent.
        sweagent_dir: Path to SWE-Agent installation (required if dry_run=False).
        max_tasks: Override number of tasks per condition.
    """
    exp = ExperimentConfig()
    config = RunConfig(
        output_dir=output_dir,
        dry_run=dry_run,
        max_tasks=max_tasks,
        sweagent_dir=sweagent_dir,
    )
    runner = PipelineRunner(exp, config)
    return runner.run_all()
