"""Data loader for HarnessEval trajectory files.

Provides functions to scan trajectory JSON files, load individual trajectories,
compute metrics per log, and build DataFrames for ANOVA analysis.

No @st.cache_data decorators here — caching is applied at the call site
(e.g. inside Streamlit tab modules) so these functions are plain and testable.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from harness_eval.configs.tool_config import ToolConfig, ToolLevel
from harness_eval.metrics.tool_dispatch import (
    ToolCall,
    correct_selection_rate,
    redundant_call_rate,
    utilization_breadth,
)
from harness_eval.metrics.context_utilization import TokenSegment, effective_token_ratio


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def scan_trajectories(base_dir: Path) -> list[dict]:
    """Scan condition directories under *base_dir* and return metadata list.

    Expected layout::

        base_dir/
          <condition_id>/
            <task_id>.json
            ...
          ...

    Returns:
        List of dicts, each with keys:
            condition_id, task_id, resolved, model, total_cost, num_turns, path
    """
    results: list[dict] = []

    for cond_dir in sorted(base_dir.iterdir()):
        if not cond_dir.is_dir():
            continue

        for json_file in sorted(cond_dir.glob("*.json")):
            try:
                log = load_trajectory(json_file)
            except (json.JSONDecodeError, OSError):
                continue

            trajectory = log.get("trajectory", [])
            results.append(
                {
                    "condition_id": log.get("condition_id", cond_dir.name),
                    "task_id": log.get("task_id", json_file.stem),
                    "resolved": bool(log.get("resolved", False)),
                    "model": log.get("model", ""),
                    "total_cost": float(log.get("total_cost", 0.0)),
                    "num_turns": len(trajectory),
                    "path": json_file,
                }
            )

    return results


def load_trajectory(path: Path) -> dict:
    """Load and parse a single trajectory JSON file.

    Args:
        path: Absolute path to the ``.json`` trajectory file.

    Returns:
        Parsed JSON as a Python dict.
    """
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def compute_metrics_for_log(log: dict) -> dict[str, dict]:
    """Compute per-trajectory metrics M1.1, M1.2, M1.3, and M2.2.

    Note: M2.1 (Info Retention Score) and M3.1/M3.2 (cross-backend metrics)
    require paired runs or aggregated data, so they are skipped here.

    For M2.2 (Effective Token Ratio), we lack segment-level annotations in
    the trajectory format, so we estimate relevance from non-empty outputs:
    each trajectory turn is treated as one segment; turns with a non-empty
    ``output`` field are classified as relevant; token_count defaults to 1.

    Args:
        log: Parsed trajectory dict (as returned by :func:`load_trajectory`).

    Returns:
        Dict mapping metric ID → result dict with keys:
            value (float), label (str), dim (str), detail (str)
    """
    config = log.get("config", {})
    tool_level_name = config.get("tool_level", "full")

    try:
        tool_config = ToolConfig.from_level_name(tool_level_name)
    except ValueError:
        tool_config = ToolConfig(ToolLevel.FULL)

    available_tools = tool_config.tools
    trajectory = log.get("trajectory", [])

    # Build ToolCall objects from trajectory turns
    tool_calls: list[ToolCall] = []
    for turn in trajectory:
        tool_calls.append(
            ToolCall(
                turn_index=turn.get("turn", 0),
                tool_name=turn.get("action", ""),
                output=turn.get("output", "") or "",
                acceptable_tools=turn.get("acceptable_tools", None),
            )
        )

    # ------------------------------------------------------------------
    # M1.1 Correct Selection Rate
    # ------------------------------------------------------------------
    m11_value = correct_selection_rate(tool_calls)

    # ------------------------------------------------------------------
    # M1.2 Redundant Call Rate
    # ------------------------------------------------------------------
    m12_value = redundant_call_rate(tool_calls)

    # ------------------------------------------------------------------
    # M1.3 Utilization Breadth
    # ------------------------------------------------------------------
    m13_value = utilization_breadth(tool_calls, available_tools)

    # ------------------------------------------------------------------
    # M2.2 Effective Token Ratio (estimated from non-empty outputs)
    # ------------------------------------------------------------------
    segments: list[TokenSegment] = []
    for turn in trajectory:
        raw_output = turn.get("output", "") or ""
        is_relevant = bool(raw_output.strip())
        segments.append(
            TokenSegment(
                text=raw_output,
                is_relevant=is_relevant,
                token_count=1,
            )
        )

    m22_value = effective_token_ratio(segments) if segments else 0.0

    return {
        "m11": {
            "value": float(m11_value),
            "label": "Correct Selection Rate",
            "dim": "D1 Tool Dispatch",
            "detail": (
                f"% tool calls selecting an acceptable tool. "
                f"Tool level: {tool_level_name} ({len(available_tools)} tools available)."
            ),
        },
        "m12": {
            "value": float(m12_value),
            "label": "Redundant Call Rate",
            "dim": "D1 Tool Dispatch",
            "detail": (
                "% calls whose output is not referenced in the next 3 turns. "
                "Lower is better."
            ),
        },
        "m13": {
            "value": float(m13_value),
            "label": "Utilization Breadth",
            "dim": "D1 Tool Dispatch",
            "detail": (
                f"Unique tools used / total tools available "
                f"({len(available_tools)} tools in '{tool_level_name}' level)."
            ),
        },
        "m22": {
            "value": float(m22_value),
            "label": "Effective Token Ratio",
            "dim": "D2 Context Utilization",
            "detail": (
                "Estimated % turns with non-empty output (proxy for task-relevant tokens). "
                "Full segment annotation requires LLM classifier."
            ),
        },
    }


def build_anova_dataframe(base_dir: Path) -> pd.DataFrame:
    """Build a flat DataFrame of all trajectories suitable for ANOVA.

    Columns:
        task_id, condition_id, tool_config, context_strategy, backend,
        resolve_rate, total_cost

    Args:
        base_dir: Root directory containing condition subdirectories.

    Returns:
        pd.DataFrame with one row per trajectory file.
    """
    metadata = scan_trajectories(base_dir)

    rows: list[dict] = []
    for item in metadata:
        path: Path = item["path"]
        try:
            log = load_trajectory(path)
        except (json.JSONDecodeError, OSError):
            continue

        config = log.get("config", {})
        rows.append(
            {
                "task_id": item["task_id"],
                "condition_id": item["condition_id"],
                "tool_config": config.get("tool_level", ""),
                "context_strategy": config.get("context_strategy", ""),
                "backend": config.get("backend", ""),
                "resolve_rate": 1.0 if item["resolved"] else 0.0,
                "total_cost": item["total_cost"],
            }
        )

    if not rows:
        return pd.DataFrame(
            columns=[
                "task_id",
                "condition_id",
                "tool_config",
                "context_strategy",
                "backend",
                "resolve_rate",
                "total_cost",
            ]
        )

    return pd.DataFrame(rows)
