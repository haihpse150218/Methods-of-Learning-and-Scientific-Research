"""Generate sample trajectory data for testing the Flask UI."""

import json
import os
import random
from pathlib import Path

random.seed(42)

BASE = Path(__file__).resolve().parent.parent
TRAJ_DIR = BASE / "app" / "trajectories"

TASKS = [
    {"task_id": "django__django-16379", "repo": "django"},
    {"task_id": "django__django-15388", "repo": "django"},
    {"task_id": "flask__flask-4992", "repo": "flask"},
    {"task_id": "requests__requests-6028", "repo": "requests"},
    {"task_id": "sympy__sympy-20442", "repo": "sympy"},
    {"task_id": "scikit-learn__scikit-learn-25638", "repo": "sklearn"},
    {"task_id": "matplotlib__matplotlib-25332", "repo": "matplotlib"},
    {"task_id": "pytest__pytest-11143", "repo": "pytest"},
]

TOOL_SETS = {
    "full": ["bash", "python", "read", "write", "edit", "glob", "grep",
             "find", "git_diff", "git_log", "git_show", "test_runner"],
    "medium": ["bash", "python", "read", "write", "edit", "grep",
               "git_diff", "test_runner"],
    "minimal": ["bash", "read", "write", "edit", "grep"],
}

MODELS = {
    "claude": "claude-sonnet-4-20250514",
    "gpt": "gpt-4o-2025-03-01",
    "deepseek": "deepseek-chat",
}

COSTS = {"claude": 0.35, "gpt": 0.30, "deepseek": 0.15}

CTX_TOKENS = {
    "full": (35000, 60000),
    "sliding_window": (20000, 50000),
    "summary": (8000, 20000),
}


def make_turn(idx, action, args, output, acceptable, ts_min):
    return {
        "turn": idx,
        "action": action,
        "args": args,
        "output": output,
        "acceptable_tools": acceptable,
        "timestamp": f"2026-05-01T10:{ts_min:02d}:{idx * 7:02d}",
    }


def generate_trajectory(task, tool_level, ctx, backend, resolved):
    tools = TOOL_SETS[tool_level]
    turns = []
    idx = 1
    repo = task["repo"]

    # Turn 1: read
    turns.append(make_turn(idx, "read",
        {"path": f"{repo}/core/module.py"},
        (f"class Module:\n    def process(self):\n"
         f"        # main logic\n        return self._handle_request()\n    ...\n"),
        ["read", "grep", "bash"], 0))
    idx += 1

    # Turn 2: grep
    turns.append(make_turn(idx, "grep",
        {"pattern": "def _handle_request", "path": f"{repo}/core/"},
        ("line 142: def _handle_request(self, data):\n"
         "line 143:     validated = self.validate(data)\n"
         "line 144:     return self.execute(validated)"),
        ["grep", "read", "bash"], 1))
    idx += 1

    # Turn 3: read deeper
    turns.append(make_turn(idx, "read",
        {"path": f"{repo}/core/handlers.py", "offset": 140, "limit": 30},
        ("class Handler:\n    def validate(self, data):\n"
         '        if not data:\n            raise ValueError("Empty")\n'
         "        return data"),
        ["read"], 2))
    idx += 1

    # Turn 4: glob/find (medium/full only)
    if tool_level != "minimal":
        if tool_level == "full":
            action, args_t = "glob", {"pattern": "tests/**/test_*.py"}
        else:
            action, args_t = "bash", {"command": 'find tests/ -name "test_*.py"'}
        acceptable = ["glob", "find", "bash"] if tool_level == "full" else ["bash", "grep"]
        turns.append(make_turn(idx, action, args_t,
            "tests/test_module.py\ntests/test_handlers.py\ntests/integration/test_e2e.py",
            acceptable, 3))
        idx += 1

    # Turn N-2: read test
    turns.append(make_turn(idx, "read",
        {"path": "tests/test_module.py"},
        ("from unittest import TestCase\n"
         "class TestModule(TestCase):\n"
         "    def test_process(self):\n"
         "        m = Module()\n"
         "        result = m.process()\n"
         "        self.assertIsNotNone(result)"),
        ["read", "grep"], 4))
    idx += 1

    # Turn N-1: edit
    turns.append(make_turn(idx, "edit",
        {"path": f"{repo}/core/module.py",
         "old_string": "    def _handle_request(self, data):",
         "new_string": "    def _handle_request(self, data=None):"},
        "File edited successfully",
        ["edit", "write"], 5))
    idx += 1

    # Turn N: test
    if resolved:
        test_out = "....\n4 passed in 0.82s"
    else:
        test_out = "...F\n3 passed, 1 FAILED in 1.23s"
    turns.append(make_turn(idx, "bash",
        {"command": "python -m pytest tests/test_module.py -x -q 2>&1 | tail -5"},
        test_out,
        ["bash", "test_runner"], 6))

    lo, hi = CTX_TOKENS[ctx]
    return {
        "task_id": task["task_id"],
        "model": MODELS[backend],
        "resolved": resolved,
        "config": {
            "tool_level": tool_level,
            "context_strategy": ctx,
            "backend": backend,
        },
        "condition_id": f"{tool_level}_{ctx}_{backend}",
        "total_cost": round(COSTS[backend] * random.uniform(0.7, 1.3), 2),
        "context_tokens_used": random.randint(lo, hi),
        "trajectory": turns,
    }


# ── Conditions to generate ──────────────────────────
CONDITIONS = [
    ("minimal", "full", "claude"),
    ("full", "summary", "claude"),
    ("medium", "sliding_window", "gpt"),
    ("full", "full", "gpt"),
    ("minimal", "summary", "deepseek"),
    ("full", "full", "deepseek"),
]

RESOLVE_PROBS = {
    "full_full_claude": 0.75,
    "minimal_full_claude": 0.55,
    "full_summary_claude": 0.63,
    "medium_sliding_window_gpt": 0.60,
    "full_full_gpt": 0.70,
    "minimal_summary_deepseek": 0.40,
    "full_full_deepseek": 0.65,
}


def main():
    count = 0

    for tool, ctx, be in CONDITIONS:
        cond_id = f"{tool}_{ctx}_{be}"
        cond_dir = TRAJ_DIR / cond_id
        cond_dir.mkdir(parents=True, exist_ok=True)
        prob = RESOLVE_PROBS.get(cond_id, 0.5)

        for task in TASKS[:5]:
            resolved = random.random() < prob
            traj = generate_trajectory(task, tool, ctx, be, resolved)
            path = cond_dir / f"{task['task_id']}.json"
            path.write_text(json.dumps(traj, indent=2, ensure_ascii=False), encoding="utf-8")
            count += 1

    # Add more tasks to existing full_full_claude
    cond_dir = TRAJ_DIR / "full_full_claude"
    cond_dir.mkdir(parents=True, exist_ok=True)
    for task in TASKS[1:5]:
        resolved = random.random() < 0.75
        traj = generate_trajectory(task, "full", "full", "claude", resolved)
        path = cond_dir / f"{task['task_id']}.json"
        path.write_text(json.dumps(traj, indent=2, ensure_ascii=False), encoding="utf-8")
        count += 1

    print(f"Generated {count} trajectory files")
    for d in sorted(TRAJ_DIR.iterdir()):
        if d.is_dir():
            n = len(list(d.glob("*.json")))
            print(f"  {d.name}: {n} files")


if __name__ == "__main__":
    main()
