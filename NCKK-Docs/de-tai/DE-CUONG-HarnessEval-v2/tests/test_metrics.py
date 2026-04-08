"""Tests for all 7 HarnessEval metrics (3 dimensions)."""

import pytest
import numpy as np

from harness_eval.metrics.tool_dispatch import (
    ToolCall,
    correct_selection_rate,
    redundant_call_rate,
    utilization_breadth,
)
from harness_eval.metrics.context_utilization import (
    TokenSegment,
    info_retention_score,
    effective_token_ratio,
)
from harness_eval.metrics.backend_portability import (
    cross_backend_stddev,
    min_max_ratio,
)


# ============================================================
# M1.1: Correct Selection Rate
# ============================================================

class TestCorrectSelectionRate:
    def test_all_correct(self):
        calls = [
            ToolCall(turn_index=0, tool_name="read", output="content", acceptable_tools=["read", "grep"]),
            ToolCall(turn_index=1, tool_name="edit", output="done", acceptable_tools=["edit", "write"]),
        ]
        assert correct_selection_rate(calls) == 1.0

    def test_all_incorrect(self):
        calls = [
            ToolCall(turn_index=0, tool_name="bash", output="err", acceptable_tools=["read"]),
            ToolCall(turn_index=1, tool_name="glob", output="files", acceptable_tools=["grep"]),
        ]
        assert correct_selection_rate(calls) == 0.0

    def test_mixed(self):
        calls = [
            ToolCall(turn_index=0, tool_name="read", output="ok", acceptable_tools=["read"]),
            ToolCall(turn_index=1, tool_name="bash", output="err", acceptable_tools=["grep"]),
            ToolCall(turn_index=2, tool_name="edit", output="ok", acceptable_tools=["edit"]),
        ]
        assert abs(correct_selection_rate(calls) - 2 / 3) < 1e-9

    def test_no_annotations(self):
        """Calls without acceptable_tools should be skipped."""
        calls = [
            ToolCall(turn_index=0, tool_name="read", output="ok"),
        ]
        assert correct_selection_rate(calls) == 0.0

    def test_empty(self):
        assert correct_selection_rate([]) == 0.0

    def test_multiple_acceptable_tools(self):
        """M1.1 uses a SET of acceptable tools, not single ground-truth."""
        calls = [
            ToolCall(turn_index=0, tool_name="grep", output="found",
                     acceptable_tools=["grep", "glob", "find"]),
        ]
        assert correct_selection_rate(calls) == 1.0


# ============================================================
# M1.2: Redundant Call Rate
# ============================================================

class TestRedundantCallRate:
    def test_no_redundancy(self):
        """All outputs are referenced in subsequent turns."""
        calls = [
            ToolCall(turn_index=0, tool_name="read", output="file content here"),
            ToolCall(turn_index=1, tool_name="edit", output="file content here modified and file content here used"),
            ToolCall(turn_index=2, tool_name="test_runner", output="file content here modified and file content here used verified"),
        ]
        # turn 0 output[:50] appears in turn 1, turn 1 output[:50] appears in turn 2
        rate = redundant_call_rate(calls)
        assert rate == 0.0

    def test_all_redundant(self):
        """No output is referenced in subsequent turns."""
        calls = [
            ToolCall(turn_index=0, tool_name="read", output="alpha"),
            ToolCall(turn_index=1, tool_name="glob", output="beta"),
            ToolCall(turn_index=2, tool_name="grep", output="gamma"),
        ]
        rate = redundant_call_rate(calls)
        assert rate == 1.0

    def test_single_call(self):
        calls = [ToolCall(turn_index=0, tool_name="read", output="data")]
        assert redundant_call_rate(calls) == 0.0

    def test_empty(self):
        assert redundant_call_rate([]) == 0.0


# ============================================================
# M1.3: Utilization Breadth
# ============================================================

class TestUtilizationBreadth:
    def test_all_tools_used(self):
        available = ["read", "write", "bash"]
        calls = [
            ToolCall(turn_index=0, tool_name="read", output=""),
            ToolCall(turn_index=1, tool_name="write", output=""),
            ToolCall(turn_index=2, tool_name="bash", output=""),
        ]
        assert utilization_breadth(calls, available) == 1.0

    def test_partial_usage(self):
        available = ["read", "write", "bash", "grep"]
        calls = [
            ToolCall(turn_index=0, tool_name="read", output=""),
            ToolCall(turn_index=1, tool_name="bash", output=""),
        ]
        assert utilization_breadth(calls, available) == 0.5

    def test_no_tools_used(self):
        available = ["read", "write"]
        assert utilization_breadth([], available) == 0.0

    def test_no_tools_available(self):
        calls = [ToolCall(turn_index=0, tool_name="read", output="")]
        assert utilization_breadth(calls, []) == 0.0

    def test_unknown_tool_not_counted(self):
        """Tools not in available list shouldn't count toward breadth."""
        available = ["read", "write"]
        calls = [
            ToolCall(turn_index=0, tool_name="read", output=""),
            ToolCall(turn_index=1, tool_name="unknown_tool", output=""),
        ]
        assert utilization_breadth(calls, available) == 0.5

    def test_duplicate_tool_calls_counted_once(self):
        """Using the same tool multiple times counts as 1 unique tool."""
        available = ["read", "write", "bash"]
        calls = [
            ToolCall(turn_index=0, tool_name="read", output=""),
            ToolCall(turn_index=1, tool_name="read", output=""),
            ToolCall(turn_index=2, tool_name="read", output=""),
        ]
        assert abs(utilization_breadth(calls, available) - 1 / 3) < 1e-9


# ============================================================
# M2.1: Info Retention Score
# ============================================================

class TestInfoRetentionScore:
    def test_identical_responses(self):
        score = info_retention_score("hello world", "hello world")
        assert score == 1.0

    def test_completely_different(self):
        score = info_retention_score("alpha beta gamma", "delta epsilon zeta")
        assert score == 0.0

    def test_partial_overlap(self):
        score = info_retention_score("the quick brown fox", "the slow brown cat")
        assert 0.0 < score < 1.0

    def test_empty_full(self):
        assert info_retention_score("", "something") == 0.0

    def test_empty_compacted(self):
        assert info_retention_score("something", "") == 0.0

    def test_both_empty(self):
        assert info_retention_score("", "") == 0.0


# ============================================================
# M2.2: Effective Token Ratio
# ============================================================

class TestEffectiveTokenRatio:
    def test_all_relevant(self):
        segments = [
            TokenSegment(text="import os", is_relevant=True, token_count=2),
            TokenSegment(text="def fix():", is_relevant=True, token_count=3),
        ]
        assert effective_token_ratio(segments) == 1.0

    def test_all_irrelevant(self):
        segments = [
            TokenSegment(text="random chat", is_relevant=False, token_count=2),
            TokenSegment(text="old history", is_relevant=False, token_count=3),
        ]
        assert effective_token_ratio(segments) == 0.0

    def test_mixed_weighted(self):
        segments = [
            TokenSegment(text="relevant code", is_relevant=True, token_count=100),
            TokenSegment(text="irrelevant noise", is_relevant=False, token_count=100),
        ]
        assert effective_token_ratio(segments) == 0.5

    def test_weighted_by_token_count(self):
        segments = [
            TokenSegment(text="important", is_relevant=True, token_count=300),
            TokenSegment(text="noise", is_relevant=False, token_count=100),
        ]
        assert effective_token_ratio(segments) == 0.75

    def test_no_segments(self):
        assert effective_token_ratio([]) == 0.0

    def test_unclassified_skipped(self):
        segments = [
            TokenSegment(text="unknown", is_relevant=None, token_count=100),
            TokenSegment(text="relevant", is_relevant=True, token_count=100),
        ]
        assert effective_token_ratio(segments) == 1.0


# ============================================================
# M3.1: Cross-Backend StdDev
# ============================================================

class TestCrossBackendStdDev:
    def test_identical_rates(self):
        rates = {"claude": 0.70, "gpt": 0.70, "deepseek": 0.70}
        assert cross_backend_stddev(rates) < 1e-10

    def test_varied_rates(self):
        rates = {"claude": 0.70, "gpt": 0.65, "deepseek": 0.55}
        stddev = cross_backend_stddev(rates)
        expected = float(np.std([0.70, 0.65, 0.55], ddof=0))
        assert abs(stddev - expected) < 1e-9

    def test_single_backend(self):
        assert cross_backend_stddev({"claude": 0.70}) == 0.0

    def test_empty(self):
        assert cross_backend_stddev({}) == 0.0

    def test_large_variation(self):
        """Large stddev means poor portability."""
        rates = {"claude": 0.90, "gpt": 0.30, "deepseek": 0.10}
        stddev = cross_backend_stddev(rates)
        assert stddev > 0.3  # high variation


# ============================================================
# M3.2: Min/Max Ratio
# ============================================================

class TestMinMaxRatio:
    def test_perfect_portability(self):
        rates = {"claude": 0.70, "gpt": 0.70, "deepseek": 0.70}
        assert min_max_ratio(rates) == 1.0

    def test_half_portability(self):
        rates = {"claude": 0.80, "gpt": 0.40, "deepseek": 0.60}
        assert min_max_ratio(rates) == 0.5

    def test_zero_max(self):
        rates = {"claude": 0.0, "gpt": 0.0}
        assert min_max_ratio(rates) == 0.0

    def test_empty(self):
        assert min_max_ratio({}) == 0.0

    def test_value_range(self):
        """Min/Max ratio must always be in [0, 1]."""
        test_cases = [
            {"a": 0.9, "b": 0.1, "c": 0.5},
            {"a": 1.0, "b": 1.0},
            {"a": 0.0, "b": 0.5},
        ]
        for rates in test_cases:
            ratio = min_max_ratio(rates)
            assert 0.0 <= ratio <= 1.0, f"Ratio {ratio} out of range for {rates}"
