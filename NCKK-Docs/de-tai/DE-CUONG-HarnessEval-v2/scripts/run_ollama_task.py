"""Mini SWE-Agent: Run a coding task using Ollama local LLM.

Simulates the SWE-Agent workflow without Docker:
1. Clone/read a test repo
2. Send problem statement to Ollama
3. LLM responds with actions (read, edit, bash)
4. Record trajectory
5. Save as HarnessEval JSON

Usage:
    python scripts/run_ollama_task.py
    python scripts/run_ollama_task.py --model qwen2.5:1.5b --max-turns 5
"""

from __future__ import annotations

import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

OLLAMA_BASE = "http://localhost:11434"
DEFAULT_MODEL = "qwen2.5:7b"
TRAJECTORIES_DIR = Path(__file__).parent.parent / "trajectories"

# Sample coding tasks (mini SWE-bench style)
TASKS = [
    {
        "task_id": "mini__fix-add-function",
        "problem": (
            "The function `add(a, b)` in `math_utils.py` has a bug — it returns `a - b` "
            "instead of `a + b`. Fix the bug.\n\n"
            "```python\n# math_utils.py\ndef add(a, b):\n    return a - b\n```"
        ),
        "expected_fix": "return a + b",
        "repo": "test-repo",
    },
    {
        "task_id": "mini__fix-greeting",
        "problem": (
            "The function `greet(name)` should return 'Hello, {name}!' but it returns "
            "'Goodbye, {name}!'. Fix it.\n\n"
            "```python\n# greetings.py\ndef greet(name):\n    return f'Goodbye, {name}!'\n```"
        ),
        "expected_fix": "Hello, {name}!",
        "repo": "test-repo",
    },
    {
        "task_id": "mini__fix-divide-by-zero",
        "problem": (
            "The function `safe_divide(a, b)` crashes with ZeroDivisionError when b=0. "
            "Add proper handling to return 0 when b is 0.\n\n"
            "```python\n# calc.py\ndef safe_divide(a, b):\n    return a / b\n```"
        ),
        "expected_fix": "if b == 0",
        "repo": "test-repo",
    },
    {
        "task_id": "mini__fix-list-average",
        "problem": (
            "The function `average(numbers)` crashes on empty lists. Fix it to return 0 "
            "for empty input.\n\n"
            "```python\n# stats.py\ndef average(numbers):\n    return sum(numbers) / len(numbers)\n```"
        ),
        "expected_fix": "if not numbers",
        "repo": "test-repo",
    },
    {
        "task_id": "mini__fix-string-reverse",
        "problem": (
            "The function `reverse_string(s)` should reverse a string but currently "
            "returns it unchanged. Fix it.\n\n"
            "```python\n# strings.py\ndef reverse_string(s):\n    return s\n```"
        ),
        "expected_fix": "s[::-1]",
        "repo": "test-repo",
    },
]

# System prompt for the mini agent
SYSTEM_PROMPT = """You are a coding assistant. You will be given a buggy code snippet and asked to fix it.

Respond with EXACTLY this format for each step:

THOUGHT: <your reasoning>
ACTION: <one of: read, edit, test>
ARGS: <action arguments as JSON>

After fixing, respond with:
THOUGHT: The bug is fixed.
ACTION: submit
ARGS: {"status": "done"}

Be concise. Fix the bug in as few steps as possible."""


def call_ollama(model: str, messages: list[dict], max_tokens: int = 500) -> dict:
    """Call Ollama chat API."""
    resp = requests.post(
        f"{OLLAMA_BASE}/api/chat",
        json={
            "model": model,
            "messages": messages,
            "stream": False,
            "options": {"temperature": 0, "num_predict": max_tokens},
        },
        timeout=120,
    )
    resp.raise_for_status()
    return resp.json()


def parse_action(text: str) -> tuple[str, str, dict]:
    """Parse LLM response into (thought, action, args)."""
    thought = ""
    action = "unknown"
    args = {}

    for line in text.split("\n"):
        line = line.strip()
        if line.upper().startswith("THOUGHT:"):
            thought = line[8:].strip()
        elif line.upper().startswith("ACTION:"):
            action = line[7:].strip().lower()
        elif line.upper().startswith("ARGS:"):
            args_str = line[5:].strip()
            try:
                args = json.loads(args_str)
            except json.JSONDecodeError:
                args = {"raw": args_str}

    return thought, action, args


def run_task(task: dict, model: str, max_turns: int = 8) -> dict:
    """Run a single task and return trajectory dict."""
    print(f"\n{'='*60}")
    print(f"Task: {task['task_id']}")
    print(f"Model: {model}")
    print(f"{'='*60}")

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Fix this bug:\n\n{task['problem']}"},
    ]

    trajectory = []
    resolved = False
    total_tokens = 0
    start_time = time.time()

    for turn in range(1, max_turns + 1):
        print(f"\n--- Turn {turn} ---")

        try:
            result = call_ollama(model, messages, max_tokens=500)
        except Exception as e:
            print(f"  Ollama error: {e}")
            trajectory.append({
                "turn": turn,
                "action": "error",
                "args": {"error": str(e)},
                "output": "",
                "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
            })
            break

        response_text = result.get("message", {}).get("content", "")
        tokens = result.get("eval_count", 0) + result.get("prompt_eval_count", 0)
        total_tokens += tokens

        thought, action, args = parse_action(response_text)

        print(f"  Thought: {thought[:100]}")
        print(f"  Action:  {action}")
        print(f"  Args:    {json.dumps(args)[:100]}")

        # Generate output based on action
        if action == "submit" or action == "done":
            output = "Submitted."
            resolved = task["expected_fix"].lower() in response_text.lower()
            print(f"  Result:  {'RESOLVED' if resolved else 'FAILED'}")
        elif action == "read":
            output = task["problem"]  # Return the buggy code
        elif action == "edit":
            output = "File edited successfully."
            # Check if the fix is in the response
            if task["expected_fix"].lower() in response_text.lower():
                resolved = True
        elif action == "test":
            output = "All tests passed." if resolved else "1 test failed."
        else:
            output = response_text[:200]
            # Check if response contains the fix even without proper format
            if task["expected_fix"].lower() in response_text.lower():
                resolved = True

        acceptable = ["read", "edit", "bash", "test", "submit"]
        trajectory.append({
            "turn": turn,
            "action": action if action in acceptable else "bash",
            "args": args if args else {"command": response_text[:100]},
            "output": output,
            "acceptable_tools": acceptable[:3] if turn <= 2 else acceptable,
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
        })

        # Add assistant response to context
        messages.append({"role": "assistant", "content": response_text})

        if action in ("submit", "done"):
            break

        # Add observation for next turn
        messages.append({"role": "user", "content": f"OBSERVATION:\n{output}"})

    duration = time.time() - start_time
    cost_estimate = total_tokens * 0.0  # Ollama is free

    print(f"\n  Duration: {duration:.1f}s | Tokens: {total_tokens} | Resolved: {resolved}")

    return {
        "task_id": task["task_id"],
        "model": f"ollama/{model}",
        "resolved": resolved,
        "config": {
            "tool_level": "minimal",
            "context_strategy": "full",
            "backend": "ollama",
        },
        "condition_id": "minimal_full_ollama",
        "total_cost": cost_estimate,
        "context_tokens_used": total_tokens,
        "duration_seconds": round(duration, 1),
        "trajectory": trajectory,
    }


def save_trajectory(traj: dict, condition_id: str) -> Path:
    """Save trajectory to trajectories/<condition_id>/<task_id>.json."""
    out_dir = TRAJECTORIES_DIR / condition_id
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{traj['task_id']}.json"
    out_path.write_text(json.dumps(traj, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  Saved: {out_path}")
    return out_path


def main():
    parser = argparse.ArgumentParser(description="Run mini coding tasks with Ollama")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Ollama model name")
    parser.add_argument("--max-turns", type=int, default=8, help="Max turns per task")
    parser.add_argument("--tasks", type=int, default=None, help="Number of tasks to run (default: all)")
    parser.add_argument("--condition", default="minimal_full_ollama", help="Condition ID for output")
    args = parser.parse_args()

    tasks = TASKS[:args.tasks] if args.tasks else TASKS
    print(f"Running {len(tasks)} tasks with {args.model}")
    print(f"Output: trajectories/{args.condition}")

    results = []
    for task in tasks:
        traj = run_task(task, args.model, args.max_turns)
        traj["condition_id"] = args.condition
        traj["config"]["backend"] = "ollama"
        save_trajectory(traj, args.condition)
        results.append(traj)

    # Summary
    resolved = sum(1 for r in results if r["resolved"])
    print(f"\n{'='*60}")
    print(f"SUMMARY: {resolved}/{len(results)} resolved ({resolved/len(results):.0%})")
    print(f"Condition: {args.condition}")
    print(f"Model: {args.model}")
    for r in results:
        status = "PASS" if r["resolved"] else "FAIL"
        print(f"  {r['task_id']}: {status} ({len(r['trajectory'])} turns, {r['duration_seconds']:.1f}s)")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
