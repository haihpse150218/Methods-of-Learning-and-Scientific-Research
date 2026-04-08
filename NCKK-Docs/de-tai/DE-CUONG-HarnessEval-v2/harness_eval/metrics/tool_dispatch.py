"""D1. Tool Dispatch metrics (M1.1, M1.2, M1.3).

M1.1 Correct Selection Rate: % calls selecting an acceptable tool
M1.2 Redundant Call Rate: % calls whose output is unused within 3 subsequent turns
M1.3 Utilization Breadth: Unique tool types used / total tools available
"""

from dataclasses import dataclass


@dataclass
class ToolCall:
    """A single tool call from an agent trace."""

    turn_index: int
    tool_name: str
    output: str
    acceptable_tools: list[str] | None = None  # ground truth for M1.1


@dataclass
class ToolDispatchResult:
    """Results for all D1 metrics on a single task."""

    m1_1_correct_selection: float
    m1_2_redundant_call_rate: float
    m1_3_utilization_breadth: float


def correct_selection_rate(tool_calls: list[ToolCall]) -> float:
    """M1.1: % calls selecting an acceptable tool.

    Each tool call has a set of acceptable tools (annotated by 2 human raters).
    A call is "correct" if the tool used is in the acceptable set.

    Returns:
        Float in [0, 1]. Returns 0.0 if no calls have annotations.
    """
    annotated = [tc for tc in tool_calls if tc.acceptable_tools is not None]
    if not annotated:
        return 0.0
    correct = sum(1 for tc in annotated if tc.tool_name in tc.acceptable_tools)
    return correct / len(annotated)


def redundant_call_rate(tool_calls: list[ToolCall]) -> float:
    """M1.2: % calls whose output is unused within 3 subsequent turns.

    A tool call is "redundant" if its output string does not appear (even partially)
    in any of the next 3 tool call outputs or contexts.

    Returns:
        Float in [0, 1]. Returns 0.0 if fewer than 2 calls.
    """
    if len(tool_calls) < 2:
        return 0.0

    redundant_count = 0
    for i, tc in enumerate(tool_calls):
        if not tc.output:
            continue
        # Check if output is referenced in next 3 turns
        future_window = tool_calls[i + 1 : i + 4]
        output_used = any(
            tc.output[:50] in future_tc.output for future_tc in future_window if future_tc.output
        )
        if not output_used and future_window:
            redundant_count += 1

    # Last call can't be redundant (no future context)
    evaluable = len(tool_calls) - 1
    return redundant_count / evaluable if evaluable > 0 else 0.0


def utilization_breadth(tool_calls: list[ToolCall], available_tools: list[str]) -> float:
    """M1.3: Unique tool types used / total tools available.

    Returns:
        Float in [0, 1]. Returns 0.0 if no tools available.
    """
    if not available_tools:
        return 0.0
    used_tools = {tc.tool_name for tc in tool_calls}
    return len(used_tools & set(available_tools)) / len(available_tools)
