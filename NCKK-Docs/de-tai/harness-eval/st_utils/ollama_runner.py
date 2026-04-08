"""Ollama local runner — runs mini coding tasks via Ollama API.

Used by RunManager when mode="ollama". Calls Ollama chat API directly
(no Docker, no SWE-Agent subprocess needed).
"""

from __future__ import annotations

import hashlib
import json
import random
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

OLLAMA_BASE = "http://localhost:11434"

# Mini SWE-bench style tasks
TASKS = [
    {
        "task_id": "mini__fix-add-function",
        "problem": 'The function `add(a, b)` returns `a - b` instead of `a + b`. Fix it.\n\n```python\ndef add(a, b):\n    return a - b\n```',
        "expected_fix": "return a + b",
    },
    {
        "task_id": "mini__fix-greeting",
        "problem": 'The function `greet(name)` returns "Goodbye" instead of "Hello". Fix it.\n\n```python\ndef greet(name):\n    return f\'Goodbye, {name}!\'\n```',
        "expected_fix": "Hello",
    },
    {
        "task_id": "mini__fix-divide-by-zero",
        "problem": 'The function `safe_divide(a, b)` crashes when b=0. Return 0 when b is 0.\n\n```python\ndef safe_divide(a, b):\n    return a / b\n```',
        "expected_fix": "if b == 0",
    },
    {
        "task_id": "mini__fix-list-average",
        "problem": 'The function `average(numbers)` crashes on empty lists. Return 0 for empty input.\n\n```python\ndef average(numbers):\n    return sum(numbers) / len(numbers)\n```',
        "expected_fix": "if not numbers",
    },
    {
        "task_id": "mini__fix-string-reverse",
        "problem": 'The function `reverse_string(s)` returns the string unchanged. Fix it.\n\n```python\ndef reverse_string(s):\n    return s\n```',
        "expected_fix": "s[::-1]",
    },
    {
        "task_id": "mini__fix-max-value",
        "problem": 'The function `find_max(lst)` always returns the first element. Fix it.\n\n```python\ndef find_max(lst):\n    return lst[0]\n```',
        "expected_fix": "max(",
    },
    {
        "task_id": "mini__fix-is-even",
        "problem": 'The function `is_even(n)` checks if n is odd instead of even. Fix it.\n\n```python\ndef is_even(n):\n    return n % 2 == 1\n```',
        "expected_fix": "== 0",
    },
    {
        "task_id": "mini__fix-concat-lists",
        "problem": 'The function `concat(a, b)` returns only list a. Fix it to return a + b.\n\n```python\ndef concat(a, b):\n    return a\n```',
        "expected_fix": "a + b",
    },
]

SYSTEM_PROMPT = """You are a coding assistant. Fix the bug in the given code.

Respond with:
THOUGHT: <your reasoning>
ACTION: <read|edit|test|submit>
ARGS: <JSON>

After fixing, respond with:
THOUGHT: Fixed.
ACTION: submit
ARGS: {"status": "done"}"""


def list_models() -> list[dict]:
    """List available Ollama models."""
    try:
        resp = requests.get(f"{OLLAMA_BASE}/api/tags", timeout=5)
        resp.raise_for_status()
        return resp.json().get("models", [])
    except Exception:
        return []


def check_ollama() -> bool:
    """Check if Ollama is running."""
    try:
        resp = requests.get(f"{OLLAMA_BASE}/api/tags", timeout=3)
        return resp.status_code == 200
    except Exception:
        return False


def run_single_task(
    task: dict,
    model: str,
    tool_level: str = "minimal",
    context_strategy: str = "full",
    max_turns: int = 5,
) -> dict:
    """Run a single task via Ollama and return trajectory dict."""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Fix this bug:\n\n{task['problem']}"},
    ]

    trajectory = []
    resolved = False
    total_tokens = 0
    start_time = time.time()

    for turn in range(1, max_turns + 1):
        try:
            resp = requests.post(
                f"{OLLAMA_BASE}/api/chat",
                json={
                    "model": model,
                    "messages": messages,
                    "stream": False,
                    "options": {"temperature": 0, "num_predict": 500},
                },
                timeout=120,
            )
            resp.raise_for_status()
            result = resp.json()
        except Exception as e:
            trajectory.append({
                "turn": turn,
                "action": "error",
                "args": {"error": str(e)},
                "output": "",
                "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
            })
            break

        response_text = result.get("message", {}).get("content", "")
        total_tokens += result.get("eval_count", 0) + result.get("prompt_eval_count", 0)

        # Parse action
        thought, action, args = "", "unknown", {}
        for line in response_text.split("\n"):
            line = line.strip()
            if line.upper().startswith("THOUGHT:"):
                thought = line[8:].strip()
            elif line.upper().startswith("ACTION:"):
                action = line[7:].strip().lower()
            elif line.upper().startswith("ARGS:"):
                try:
                    args = json.loads(line[5:].strip())
                except json.JSONDecodeError:
                    args = {"raw": line[5:].strip()}

        # Check if fix is in response
        if task["expected_fix"].lower() in response_text.lower():
            resolved = True

        # Generate output
        if action in ("submit", "done"):
            output = "Submitted."
        elif action == "read":
            output = task["problem"]
        elif action == "edit":
            output = "File edited successfully."
        elif action == "test":
            output = "All tests passed." if resolved else "1 test failed."
        else:
            output = response_text[:200]

        acceptable = ["read", "edit", "bash", "test", "submit"]
        trajectory.append({
            "turn": turn,
            "action": action if action in acceptable else "bash",
            "args": args if args else {"command": response_text[:100]},
            "output": output,
            "acceptable_tools": acceptable[:3] if turn <= 2 else acceptable,
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
        })

        messages.append({"role": "assistant", "content": response_text})

        if action in ("submit", "done"):
            break
        messages.append({"role": "user", "content": f"OBSERVATION:\n{output}"})

    duration = time.time() - start_time
    condition_id = f"{tool_level}_{context_strategy}_ollama"

    return {
        "task_id": task["task_id"],
        "model": f"ollama/{model}",
        "resolved": resolved,
        "config": {
            "tool_level": tool_level,
            "context_strategy": context_strategy,
            "backend": "ollama",
        },
        "condition_id": condition_id,
        "total_cost": 0.0,
        "context_tokens_used": total_tokens,
        "duration_seconds": round(duration, 1),
        "trajectory": trajectory,
    }


def get_tasks(max_tasks: int | None = None) -> list[dict]:
    """Return list of available tasks."""
    if max_tasks:
        return TASKS[:max_tasks]
    return list(TASKS)
