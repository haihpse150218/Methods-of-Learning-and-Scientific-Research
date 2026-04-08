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

# Legacy fallback task IDs (used when embedded SWE-bench data unavailable)
_LEGACY_TASK_IDS = [
    "django__django-16379",
    "django__django-15388",
    "flask__flask-4992",
    "requests__requests-6028",
    "sympy__sympy-20442",
    "scikit-learn__scikit-learn-25638",
    "matplotlib__matplotlib-25311",
    "pytest__pytest-11143",
]


def _get_default_task_ids() -> list[str]:
    """Load task IDs from embedded SWE-bench data, falling back to legacy list."""
    try:
        from harness_eval.data.loader import get_task_ids
        ids = get_task_ids()
        return ids if ids else list(_LEGACY_TASK_IDS)
    except Exception:
        return list(_LEGACY_TASK_IDS)


def _get_task_metadata(task_id: str):
    """Look up SWE-bench metadata for a task. Returns TaskMetadata or None."""
    try:
        from harness_eval.data.loader import get_task
        return get_task(task_id)
    except Exception:
        return None


def _get_repo_files(task_id: str) -> list[str]:
    """Get real file paths for a task's repo."""
    try:
        from harness_eval.data.loader import get_repo_file_paths
        repo = task_id.split("__")[0].replace("_", "-") if "__" in task_id else ""
        # Try various formats
        for name in [repo, repo.replace("-", "/")]:
            paths = get_repo_file_paths(name)
            if paths:
                return paths
        # Try from metadata
        meta = _get_task_metadata(task_id)
        if meta:
            return get_repo_file_paths(meta.repo)
    except Exception:
        pass
    return []


# Difficulty-based resolve rates (calibrated to SWE-bench literature)
_DIFFICULTY_BASE_RATES = {
    "easy": 0.75,
    "medium": 0.55,
    "hard": 0.30,
    "expert": 0.15,
}

# Difficulty-based turn count ranges
_TURN_RANGES = {
    "easy": (3, 5),
    "medium": (5, 8),
    "hard": (8, 12),
    "expert": (10, 15),
}

# Phase definitions for trajectory generation
_PHASES = {
    "exploration": ["read", "grep", "glob", "find", "git_log"],
    "analysis": ["read", "grep", "bash", "git_show", "git_diff"],
    "modification": ["edit", "write", "bash"],
    "verification": ["bash", "test_runner", "git_diff"],
}

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
        task_ids = _get_default_task_ids()
        source = "SWE-bench Verified" if len(task_ids) > 8 else "legacy defaults"
        self.logger.info("Using %d task IDs from %s", len(task_ids), source)
        return list(task_ids)

    # ------------------------------------------------------------------
    # Synthetic data generation (dry-run only)
    # ------------------------------------------------------------------

    def _generate_synthetic_result(
        self, condition: Condition, task_id: str
    ) -> TaskResult:
        """Generate a realistic synthetic TaskResult using SWE-bench metadata.

        Uses real task difficulty from embedded SWE-bench Verified data,
        phased trajectory generation, and real repo file paths.
        """
        seed = int(
            hashlib.md5(f"{condition.condition_id}:{task_id}".encode()).hexdigest()[:8], 16,
        )
        rng = random.Random(seed)

        # Look up real task metadata
        metadata = _get_task_metadata(task_id)
        difficulty = metadata.difficulty if metadata else "medium"

        # Difficulty-aware base rate
        base_rate = _DIFFICULTY_BASE_RATES.get(difficulty, 0.55)

        # Main effects (calibrated for realistic eta-squared)
        tool_mod = {"full": 0.12, "medium": 0.02, "minimal": -0.14}
        ctx_mod = {"full": 0.06, "sliding_window": 0.01, "summary": -0.07}
        backend_mod = {"claude": 0.04, "gpt": 0.01, "deepseek": -0.03}

        tool_val = condition.tool.level.value
        ctx_val = condition.context.strategy.value
        be_val = condition.backend.backend.value

        # Interaction effects
        interaction = 0.0
        if tool_val == "minimal" and ctx_val == "summary":
            interaction = -0.06
        if tool_val == "full" and ctx_val == "full":
            interaction = 0.03
        if tool_val == "minimal" and be_val == "deepseek":
            interaction = -0.04

        noise = rng.gauss(0, 0.03)  # Smaller noise (difficulty provides structured variation)

        resolve_prob = max(0.05, min(0.95,
            base_rate + tool_mod.get(tool_val, 0.0) + ctx_mod.get(ctx_val, 0.0)
            + backend_mod.get(be_val, 0.0) + interaction + noise
        ))
        resolved = rng.random() < resolve_prob

        # Difficulty-aware cost (expert tasks cost more)
        cost_base = condition.backend.cost_per_eval
        difficulty_cost_mult = {"easy": 0.7, "medium": 1.0, "hard": 1.4, "expert": 1.8}
        cost_multiplier = difficulty_cost_mult.get(difficulty, 1.0) * rng.uniform(0.8, 1.2)
        if not resolved:
            cost_multiplier *= 1.2
        total_cost = cost_base * cost_multiplier

        # Difficulty-aware duration
        difficulty_duration = {"easy": 45.0, "medium": 80.0, "hard": 150.0, "expert": 240.0}
        base_duration = difficulty_duration.get(difficulty, 80.0)
        duration = base_duration * rng.uniform(0.6, 1.5)

        # Context tokens by strategy
        ctx_tokens_base = {"full": 60_000, "sliding_window": 40_000, "summary": 15_000}
        context_tokens = int(ctx_tokens_base.get(ctx_val, 40_000) * rng.uniform(0.7, 1.3))

        # Difficulty-aware turn count
        lo, hi = _TURN_RANGES.get(difficulty, (5, 8))
        num_turns = rng.randint(lo, hi)

        trajectory = self._generate_synthetic_trajectory(
            rng, condition, task_id, num_turns, resolved, metadata
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
        metadata=None,
    ) -> list[dict]:
        """Build a realistic phased trajectory using real repo file paths."""
        available_tools = condition.tool.tools
        file_paths = _get_repo_files(task_id)
        repo_short = task_id.split("__")[0] if "__" in task_id else "repo"
        base_time = datetime(2026, 5, 1, 10, 0, 0, tzinfo=timezone.utc)
        trajectory = []

        for turn_idx in range(1, num_turns + 1):
            # Determine phase based on position in trajectory
            progress = turn_idx / num_turns
            if progress <= 0.3:
                phase = "exploration"
            elif progress <= 0.5:
                phase = "analysis"
            elif progress <= 0.8:
                phase = "modification"
            else:
                phase = "verification"

            # Pick action from phase, filtered by available tools
            action = self._pick_phased_action(rng, phase, available_tools)

            timestamp = base_time.timestamp() + turn_idx * rng.randint(5, 20)
            ts_str = datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime(
                "%Y-%m-%dT%H:%M:%S"
            )

            turn: dict = {
                "turn": turn_idx,
                "action": action,
                "args": self._realistic_args(rng, action, repo_short, file_paths, metadata),
                "output": self._realistic_output(
                    rng, action, resolved and turn_idx == num_turns,
                    metadata, turn_idx, phase
                ),
                "acceptable_tools": _pick_acceptable_tools(rng, action, available_tools),
                "timestamp": ts_str,
            }
            trajectory.append(turn)

        return trajectory

    @staticmethod
    def _pick_phased_action(
        rng: random.Random, phase: str, available_tools: list[str]
    ) -> str:
        """Pick an action appropriate for the current phase, filtered by available tools."""
        phase_tools = _PHASES.get(phase, ["bash"])
        candidates = [t for t in phase_tools if t in available_tools]
        if not candidates:
            # Fallback: bash is always available-ish, or pick any available
            candidates = [t for t in available_tools if t in ("bash", "read", "edit")]
            if not candidates:
                candidates = available_tools
        return rng.choice(candidates)

    @staticmethod
    def _realistic_args(
        rng: random.Random, action: str, repo_short: str,
        file_paths: list[str], metadata=None,
    ) -> dict:
        """Generate plausible args using real repo file paths."""
        src_files = [f for f in file_paths if "test" not in f.lower()] or [f"{repo_short}/core.py"]
        test_files = [f for f in file_paths if "test" in f.lower()] or ["tests/test_core.py"]

        match action:
            case "read":
                return {"path": rng.choice(src_files)}
            case "write":
                return {"path": rng.choice(src_files), "content": "# patched\n"}
            case "edit":
                path = rng.choice(src_files)
                return {
                    "path": path,
                    "old_string": "    return result",
                    "new_string": "    if result is None:\n        raise ValueError('unexpected None')\n    return result",
                }
            case "grep":
                keywords = ["def ", "class ", "raise ", "return ", "import ", "self."]
                return {"pattern": rng.choice(keywords), "path": rng.choice(src_files).rsplit("/", 1)[0] + "/"}
            case "glob":
                return {"pattern": f"**/{repo_short}/**/*.py"}
            case "find":
                return {"path": repo_short + "/", "name": "*.py"}
            case "bash":
                test_path = rng.choice(test_files)
                cmds = [
                    f"cd /repo && python -m pytest {test_path} -x -q 2>&1 | tail -10",
                    f"cd /repo && python -c \"from {repo_short} import *; print('OK')\"",
                    f"cd /repo && grep -rn 'TODO\\|FIXME\\|BUG' {rng.choice(src_files)}",
                ]
                return {"command": rng.choice(cmds)}
            case "python":
                return {"code": f"import {repo_short}; print({repo_short}.__version__)"}
            case "git_diff":
                return {}
            case "git_log":
                return {"n": rng.randint(3, 10)}
            case "git_show":
                return {"ref": "HEAD"}
            case "test_runner":
                return {"test_path": rng.choice(test_files)}
            case _:
                return {}

    @staticmethod
    def _realistic_output(
        rng: random.Random, action: str, is_final_pass: bool,
        metadata=None, turn_idx: int = 1, phase: str = "",
    ) -> str:
        """Generate plausible output including real problem context."""
        # First turn: include problem snippet
        if turn_idx == 1 and metadata and metadata.problem_snippet:
            return f"Issue: {metadata.problem_snippet}\n\nSearching for relevant code..."

        if action in ("bash", "test_runner") and is_final_pass:
            n = rng.randint(10, 200)
            return f"{'.' * min(n, 30)}\n{n} passed in {rng.uniform(0.5, 30.0):.2f}s"
        if action in ("bash", "test_runner") and phase == "verification":
            failed = rng.randint(1, 5)
            passed = rng.randint(10, 100)
            return f"{passed} passed, {failed} failed in {rng.uniform(1.0, 20.0):.2f}s"
        if action == "read":
            snippets = [
                "class BaseHandler:\n    def __init__(self):\n        self._initialized = False\n    def process(self, request):\n        ...",
                "def get_queryset(self):\n    qs = super().get_queryset()\n    return qs.filter(active=True)",
                "class Config:\n    DEBUG = False\n    TESTING = False\n    DATABASE_URI = 'sqlite:///app.db'",
            ]
            return rng.choice(snippets)
        if action == "grep":
            lines = rng.randint(1, 8)
            fns = ["handle", "process", "validate", "clean", "save", "update", "create", "delete"]
            return "\n".join(f"line {rng.randint(1, 500)}: def {rng.choice(fns)}_{i}(self, *args):" for i in range(lines))
        if action == "edit":
            return "File edited successfully."
        if action == "git_diff":
            return "+    if result is None:\n+        raise ValueError('unexpected None')\n     return result"
        if action == "git_log":
            return "abc1234 Fix issue with cache invalidation\ndef5678 Add test for edge case\n789abcd Refactor query builder"
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
