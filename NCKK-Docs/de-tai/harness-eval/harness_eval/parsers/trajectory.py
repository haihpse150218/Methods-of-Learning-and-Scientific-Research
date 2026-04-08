"""Parse SWE-Agent trajectory files into structured data for the metrics system.

Supports two formats:
1. HarnessEval JSON — our internal format (app/trajectories/)
2. SWE-Agent .traj — native SWE-Agent output format
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

from harness_eval.metrics.tool_dispatch import ToolCall

# Required top-level fields in the trajectory JSON.
_REQUIRED_TOP_FIELDS = {"task_id", "model", "resolved", "config", "trajectory"}
_REQUIRED_CONFIG_FIELDS = {"tool_level", "context_strategy", "backend"}
_REQUIRED_TURN_FIELDS = {"turn", "action", "output"}


@dataclass
class TrajectoryMetadata:
    """Parsed metadata from a trajectory file."""

    task_id: str
    model: str
    resolved: bool
    condition_id: str
    tool_level: str  # "full", "medium", "minimal"
    context_strategy: str  # "full", "sliding_window", "summary"
    backend: str  # "claude", "gpt", "deepseek"
    total_cost: float
    context_tokens_used: int
    num_turns: int


@dataclass
class ParsedTrajectory:
    """Full parsed trajectory: metadata + tool calls."""

    metadata: TrajectoryMetadata
    tool_calls: list[ToolCall]
    raw: dict  # original JSON dict


def validate_trajectory(data: dict) -> list[str]:
    """Validate trajectory JSON schema.

    Returns:
        List of error messages. Empty list means valid.
    """
    errors: list[str] = []

    # Top-level fields
    missing_top = _REQUIRED_TOP_FIELDS - set(data.keys())
    if missing_top:
        errors.append(f"Missing top-level fields: {sorted(missing_top)}")

    # Config sub-fields
    config = data.get("config")
    if config is not None and isinstance(config, dict):
        missing_cfg = _REQUIRED_CONFIG_FIELDS - set(config.keys())
        if missing_cfg:
            errors.append(f"Missing config fields: {sorted(missing_cfg)}")
    elif "config" in data:
        errors.append("'config' must be a dict")

    # Trajectory turns
    trajectory = data.get("trajectory")
    if trajectory is not None:
        if not isinstance(trajectory, list):
            errors.append("'trajectory' must be a list")
        else:
            for i, turn in enumerate(trajectory):
                if not isinstance(turn, dict):
                    errors.append(f"Turn {i} is not a dict")
                    continue
                missing_turn = _REQUIRED_TURN_FIELDS - set(turn.keys())
                if missing_turn:
                    errors.append(
                        f"Turn {i} missing fields: {sorted(missing_turn)}"
                    )

    return errors


def _parse_tool_calls(trajectory: list[dict]) -> list[ToolCall]:
    """Convert raw trajectory turns into ToolCall objects."""
    tool_calls: list[ToolCall] = []
    for turn in trajectory:
        tool_calls.append(
            ToolCall(
                turn_index=turn["turn"],
                tool_name=turn["action"],
                output=turn.get("output", ""),
                acceptable_tools=turn.get("acceptable_tools"),
            )
        )
    return tool_calls


def parse_trajectory_file(path: Path | str) -> ParsedTrajectory:
    """Parse a single trajectory JSON file.

    Args:
        path: Path to the JSON file.

    Returns:
        ParsedTrajectory with metadata and tool calls.

    Raises:
        FileNotFoundError: If file doesn't exist.
        ValueError: If JSON is invalid or missing required fields.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Trajectory file not found: {path}")

    text = path.read_text(encoding="utf-8")
    if not text.strip():
        raise ValueError(f"Trajectory file is empty: {path}")

    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path}: {exc}") from exc

    errors = validate_trajectory(data)
    if errors:
        raise ValueError(
            f"Invalid trajectory in {path}: {'; '.join(errors)}"
        )

    config = data["config"]
    trajectory = data["trajectory"]

    metadata = TrajectoryMetadata(
        task_id=data["task_id"],
        model=data["model"],
        resolved=bool(data["resolved"]),
        condition_id=data.get("condition_id", ""),
        tool_level=config["tool_level"],
        context_strategy=config["context_strategy"],
        backend=config["backend"],
        total_cost=float(data.get("total_cost", 0.0)),
        context_tokens_used=int(data.get("context_tokens_used", 0)),
        num_turns=len(trajectory),
    )

    tool_calls = _parse_tool_calls(trajectory)

    return ParsedTrajectory(metadata=metadata, tool_calls=tool_calls, raw=data)


def parse_condition_dir(condition_dir: Path | str) -> list[ParsedTrajectory]:
    """Parse all trajectory files in a condition directory.

    Args:
        condition_dir: Path to directory containing .json files.

    Returns:
        List of ParsedTrajectory, sorted by task_id.

    Raises:
        FileNotFoundError: If directory doesn't exist.
    """
    condition_dir = Path(condition_dir)
    if not condition_dir.is_dir():
        raise FileNotFoundError(
            f"Condition directory not found: {condition_dir}"
        )

    json_files = sorted(condition_dir.glob("*.json"))
    trajectories = [parse_trajectory_file(f) for f in json_files]
    trajectories.sort(key=lambda t: t.metadata.task_id)
    return trajectories


def parse_sweagent_traj(path: Path | str) -> ParsedTrajectory:
    """Parse a native SWE-Agent .traj file into ParsedTrajectory.

    SWE-Agent .traj format has:
    - trajectory[]: steps with action, observation, response, thought, execution_time
    - history[]: full conversation messages
    - info: exit_status, model_stats, submission, swe_agent_version
    - replay_config: original run configuration

    Args:
        path: Path to the .traj file.

    Returns:
        ParsedTrajectory with metadata and tool calls.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Trajectory file not found: {path}")

    data = json.loads(path.read_text(encoding="utf-8"))
    trajectory = data.get("trajectory", [])
    info = data.get("info", {})
    model_stats = info.get("model_stats", {})
    replay_config = data.get("replay_config", {})
    # replay_config can be a JSON string or a dict
    if isinstance(replay_config, str):
        try:
            replay_config = json.loads(replay_config)
        except json.JSONDecodeError:
            replay_config = {}

    # Extract model name from replay_config or info
    model_name = ""
    agent_cfg = replay_config.get("agent", {})
    if isinstance(agent_cfg, dict):
        model_cfg = agent_cfg.get("model", {})
        if isinstance(model_cfg, dict):
            model_name = model_cfg.get("name", "")

    # Determine resolved: SWE-Agent exit_status "submitted" doesn't mean resolved
    # For now, mark as not resolved (actual resolution requires SWE-bench evaluation)
    exit_status = info.get("exit_status", "")
    resolved = "submitted" in exit_status and "exit_cost" not in exit_status

    # Extract condition from config (tool bundles, history processors, model)
    tool_level = _infer_tool_level(replay_config)
    context_strategy = _infer_context_strategy(replay_config)
    backend = _infer_backend(model_name)

    # Build tool calls from trajectory steps
    tool_calls: list[ToolCall] = []
    for i, step in enumerate(trajectory):
        action = step.get("action", "")
        if not action:
            continue
        # Infer tool name from action
        tool_name = _infer_tool_from_action(action)
        tool_calls.append(ToolCall(
            turn_index=i + 1,
            tool_name=tool_name,
            output=step.get("observation", ""),
            acceptable_tools=None,  # not available in .traj format
        ))

    # Build condition_id
    condition_id = f"{tool_level}_{context_strategy}_{backend}"

    metadata = TrajectoryMetadata(
        task_id=path.stem,
        model=model_name,
        resolved=resolved,
        condition_id=condition_id,
        tool_level=tool_level,
        context_strategy=context_strategy,
        backend=backend,
        total_cost=float(model_stats.get("instance_cost", 0.0)),
        context_tokens_used=int(model_stats.get("tokens_sent", 0)),
        num_turns=len(tool_calls),
    )

    # Convert to our internal format for raw
    raw = _traj_to_internal_format(data, metadata)

    return ParsedTrajectory(metadata=metadata, tool_calls=tool_calls, raw=raw)


def convert_traj_to_json(
    traj_path: Path | str,
    output_path: Path | str | None = None,
) -> dict:
    """Convert a SWE-Agent .traj file to our internal JSON format.

    Args:
        traj_path: Path to the .traj file.
        output_path: Optional path to write the JSON file. If None, just returns dict.

    Returns:
        Dict in our internal trajectory format.
    """
    parsed = parse_sweagent_traj(traj_path)
    result = parsed.raw

    if output_path is not None:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8"
        )

    return result


def _infer_tool_from_action(action: str) -> str:
    """Infer tool name from a SWE-Agent action string."""
    action_lower = action.strip().lower()

    # Common patterns
    if action_lower.startswith("find_file") or action_lower.startswith("find "):
        return "find"
    if action_lower.startswith("search_dir") or action_lower.startswith("grep "):
        return "grep"
    if action_lower.startswith("open ") or action_lower.startswith("cat "):
        return "read"
    if action_lower.startswith("edit") or action_lower.startswith("str_replace"):
        return "edit"
    if action_lower.startswith("create") or action_lower.startswith("echo ") and ">" in action:
        return "write"
    if action_lower.startswith("python "):
        return "python"
    if action_lower.startswith("git diff"):
        return "git_diff"
    if action_lower.startswith("git log"):
        return "git_log"
    if action_lower.startswith("git show"):
        return "git_show"
    if action_lower.startswith("pytest") or action_lower.startswith("python -m pytest"):
        return "test_runner"
    if action_lower.startswith("ls ") or action_lower.startswith("find "):
        return "glob"
    if action_lower.startswith("submit"):
        return "bash"

    # Default: it's a bash command
    return "bash"


def _infer_tool_level(replay_config: dict) -> str:
    """Infer tool level from replay config."""
    agent = replay_config.get("agent", {})
    if not isinstance(agent, dict):
        return "unknown"
    tools = agent.get("tools", {})
    if not isinstance(tools, dict):
        return "unknown"
    bundles = tools.get("bundles", [])
    bundle_paths = [b.get("path", "") if isinstance(b, dict) else str(b) for b in bundles]

    has_filemap = any("filemap" in p for p in bundle_paths)
    has_registry = any("registry" in p for p in bundle_paths)
    has_edit = any("edit" in p for p in bundle_paths)

    if has_filemap and has_registry:
        return "full"
    if has_registry and has_edit:
        return "medium"
    return "minimal"


def _infer_context_strategy(replay_config: dict) -> str:
    """Infer context strategy from replay config."""
    agent = replay_config.get("agent", {})
    if not isinstance(agent, dict):
        return "unknown"
    processors = agent.get("history_processors", [])

    has_last_n = any(
        isinstance(p, dict) and p.get("type") == "last_n_observations"
        for p in processors
    )
    has_remove_regex = any(
        isinstance(p, dict) and p.get("type") == "remove_regex"
        for p in processors
    )

    if has_last_n and has_remove_regex:
        return "summary"
    if has_last_n:
        return "sliding_window"
    return "full"


def _infer_backend(model_name: str) -> str:
    """Infer backend from model name."""
    model_lower = model_name.lower()
    if "claude" in model_lower:
        return "claude"
    if "gpt" in model_lower or "openai" in model_lower:
        return "gpt"
    if "deepseek" in model_lower:
        return "deepseek"
    if "ollama" in model_lower or "qwen" in model_lower or "llama" in model_lower:
        return "ollama"
    return "unknown"


def _traj_to_internal_format(traj_data: dict, metadata: TrajectoryMetadata) -> dict:
    """Convert SWE-Agent .traj data to our internal JSON format."""
    trajectory = []
    for i, step in enumerate(traj_data.get("trajectory", [])):
        action = step.get("action", "")
        if not action:
            continue
        trajectory.append({
            "turn": i + 1,
            "action": _infer_tool_from_action(action),
            "args": {"command": action},
            "output": step.get("observation", ""),
            "timestamp": None,
        })

    return {
        "task_id": metadata.task_id,
        "model": metadata.model,
        "resolved": metadata.resolved,
        "config": {
            "tool_level": metadata.tool_level,
            "context_strategy": metadata.context_strategy,
            "backend": metadata.backend,
        },
        "condition_id": metadata.condition_id,
        "total_cost": metadata.total_cost,
        "context_tokens_used": metadata.context_tokens_used,
        "trajectory": trajectory,
    }


def compute_condition_summary(trajectories: list[ParsedTrajectory]) -> dict:
    """Compute summary stats for a condition's trajectories.

    Returns:
        Dict with condition_id, total_tasks, resolved_count, resolve_rate,
        avg_turns, avg_cost, tool_level, context_strategy, backend.
        Returns an empty dict if *trajectories* is empty.
    """
    if not trajectories:
        return {}

    first = trajectories[0].metadata
    resolved_count = sum(1 for t in trajectories if t.metadata.resolved)
    total = len(trajectories)

    return {
        "condition_id": first.condition_id,
        "total_tasks": total,
        "resolved_count": resolved_count,
        "resolve_rate": resolved_count / total,
        "avg_turns": sum(t.metadata.num_turns for t in trajectories) / total,
        "avg_cost": sum(t.metadata.total_cost for t in trajectories) / total,
        "tool_level": first.tool_level,
        "context_strategy": first.context_strategy,
        "backend": first.backend,
    }
