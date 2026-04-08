"""Load curated SWE-bench Verified task metadata for dry-run mode.

Provides task IDs, difficulty labels, problem snippets, and per-repo
file paths from the embedded JSON. Falls back to legacy 8-task list
if the JSON is missing or corrupt.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

_DATA_DIR = Path(__file__).parent
_EMBEDDED_PATH = _DATA_DIR / "swe_bench_tasks.json"

# Legacy fallback (original 8 hardcoded task IDs)
LEGACY_TASK_IDS = [
    "django__django-16379",
    "django__django-15388",
    "flask__flask-4992",
    "requests__requests-6028",
    "sympy__sympy-20442",
    "scikit-learn__scikit-learn-25638",
    "matplotlib__matplotlib-25311",
    "pytest__pytest-11143",
]


@dataclass(frozen=True)
class TaskMetadata:
    """Metadata for a single SWE-bench Verified task."""

    instance_id: str
    repo: str
    short_repo: str
    problem_snippet: str
    difficulty: str  # "easy", "medium", "hard", "expert"
    fail_to_pass_count: int
    pass_to_pass_count: int


# In-memory cache
_CACHE: dict | None = None


def load_task_metadata() -> dict:
    """Load the embedded SWE-bench JSON, caching in memory.

    Returns the full dict with keys: version, source, task_count, tasks, repo_file_paths.
    """
    global _CACHE
    if _CACHE is None:
        try:
            _CACHE = json.loads(_EMBEDDED_PATH.read_text(encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError):
            _CACHE = {"tasks": [], "repo_file_paths": {}}
    return _CACHE


def get_task_ids(count: int | None = None) -> list[str]:
    """Return list of task instance_ids from embedded data.

    Falls back to LEGACY_TASK_IDS if embedded data is empty.
    """
    data = load_task_metadata()
    ids = [t["instance_id"] for t in data.get("tasks", [])]
    if not ids:
        ids = list(LEGACY_TASK_IDS)
    return ids[:count] if count else ids


def get_task(instance_id: str) -> TaskMetadata | None:
    """Look up metadata for a single task by instance_id."""
    data = load_task_metadata()
    for t in data.get("tasks", []):
        if t["instance_id"] == instance_id:
            return TaskMetadata(
                instance_id=t["instance_id"],
                repo=t["repo"],
                short_repo=t.get("short_repo", t["repo"].split("/")[-1]),
                problem_snippet=t.get("problem_snippet", ""),
                difficulty=t.get("difficulty", "medium"),
                fail_to_pass_count=t.get("fail_to_pass_count", 1),
                pass_to_pass_count=t.get("pass_to_pass_count", 10),
            )
    return None


def get_repo_file_paths(repo: str) -> list[str]:
    """Return plausible source file paths for a given repo.

    Args:
        repo: Full repo path (e.g., "django/django") or short name (e.g., "django").
    """
    data = load_task_metadata()
    paths_map = data.get("repo_file_paths", {})

    # Try full repo name first, then short name
    if repo in paths_map:
        return paths_map[repo]

    # Try matching by short name
    for key, paths in paths_map.items():
        if key.endswith(f"/{repo}") or key == repo:
            return paths

    return []


def get_difficulty_distribution() -> dict[str, int]:
    """Return count of tasks per difficulty level."""
    data = load_task_metadata()
    dist: dict[str, int] = {}
    for t in data.get("tasks", []):
        d = t.get("difficulty", "medium")
        dist[d] = dist.get(d, 0) + 1
    return dist
