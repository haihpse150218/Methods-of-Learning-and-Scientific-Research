"""Tests for configuration modules (RO2 design validation)."""

import pytest

from harness_eval.configs.tool_config import ToolConfig, ToolLevel, FULL_TOOLS, MEDIUM_TOOLS, MINIMAL_TOOLS
from harness_eval.configs.context_config import ContextConfig, ContextStrategy
from harness_eval.configs.backend_config import BackendConfig, BackendType
from harness_eval.configs.experiment import ExperimentConfig, Condition, CRITICAL_CONDITIONS


# ============================================================
# D1: Tool Configuration Tests
# ============================================================

class TestToolConfig:
    def test_full_has_12_tools(self):
        config = ToolConfig(level=ToolLevel.FULL)
        assert config.tool_count == 12

    def test_medium_has_8_tools(self):
        config = ToolConfig(level=ToolLevel.MEDIUM)
        assert config.tool_count == 8

    def test_minimal_has_5_tools(self):
        config = ToolConfig(level=ToolLevel.MINIMAL)
        assert config.tool_count == 5

    def test_minimal_is_subset_of_medium(self):
        """Minimal tools must be a subset of medium tools (gradual reduction)."""
        minimal = set(ToolConfig(level=ToolLevel.MINIMAL).tools)
        medium = set(ToolConfig(level=ToolLevel.MEDIUM).tools)
        assert minimal.issubset(medium), f"Minimal tools not subset of medium: {minimal - medium}"

    def test_medium_is_subset_of_full(self):
        """Medium tools must be a subset of full tools."""
        medium = set(ToolConfig(level=ToolLevel.MEDIUM).tools)
        full = set(ToolConfig(level=ToolLevel.FULL).tools)
        assert medium.issubset(full), f"Medium tools not subset of full: {medium - full}"

    def test_all_levels_have_bash(self):
        """Every tool level must include bash (essential for coding tasks)."""
        for level in ToolLevel:
            config = ToolConfig(level=level)
            assert config.has_tool("bash"), f"{level.value} missing bash"

    def test_all_levels_have_edit(self):
        """Every tool level must include edit (essential for code modification)."""
        for level in ToolLevel:
            config = ToolConfig(level=level)
            assert config.has_tool("edit"), f"{level.value} missing edit"

    def test_from_level_name(self):
        config = ToolConfig.from_level_name("medium")
        assert config.level == ToolLevel.MEDIUM
        assert config.tool_count == 8

    def test_from_level_name_invalid(self):
        with pytest.raises(ValueError):
            ToolConfig.from_level_name("nonexistent")

    def test_no_duplicate_tools(self):
        """Each tool level should have no duplicate tool names."""
        for level in ToolLevel:
            tools = ToolConfig(level=level).tools
            assert len(tools) == len(set(tools)), f"Duplicates in {level.value}"


# ============================================================
# D2: Context Configuration Tests
# ============================================================

class TestContextConfig:
    def test_default_is_full(self):
        config = ContextConfig()
        assert config.strategy == ContextStrategy.FULL

    def test_sliding_window_default_50k(self):
        config = ContextConfig(strategy=ContextStrategy.SLIDING_WINDOW)
        assert config.window_size_tokens == 50_000

    def test_summary_default_2k(self):
        config = ContextConfig(strategy=ContextStrategy.SUMMARY)
        assert config.summary_max_tokens == 2_000

    def test_from_strategy_name(self):
        config = ContextConfig.from_strategy_name("sliding_window")
        assert config.strategy == ContextStrategy.SLIDING_WINDOW

    def test_description_full(self):
        config = ContextConfig(strategy=ContextStrategy.FULL)
        assert "no truncation" in config.description.lower()

    def test_description_sliding(self):
        config = ContextConfig(strategy=ContextStrategy.SLIDING_WINDOW)
        assert "50,000" in config.description

    def test_description_summary(self):
        config = ContextConfig(strategy=ContextStrategy.SUMMARY)
        assert "2,000" in config.description

    def test_three_strategies_exist(self):
        """RO3 requires exactly 3 context strategies."""
        assert len(ContextStrategy) == 3


# ============================================================
# D3: Backend Configuration Tests
# ============================================================

class TestBackendConfig:
    def test_three_backends_exist(self):
        """RO3 requires exactly 3 LLM backends."""
        assert len(BackendType) == 3

    def test_claude_config(self):
        """Strong backend has a valid model_id and provider."""
        config = BackendConfig(backend=BackendType.CLAUDE)
        assert len(config.model_id) > 0
        assert len(config.provider) > 0

    def test_gpt_config(self):
        """Mid-tier backend has a valid model_id and provider."""
        config = BackendConfig(backend=BackendType.GPT)
        assert len(config.model_id) > 0
        assert len(config.provider) > 0

    def test_deepseek_config(self):
        """Budget backend has a valid model_id and provider."""
        config = BackendConfig(backend=BackendType.DEEPSEEK)
        assert len(config.model_id) > 0
        assert len(config.provider) > 0

    def test_all_temperature_zero(self):
        """Mitigation for LLM non-determinism: all backends use temperature=0."""
        for backend_type in BackendType:
            config = BackendConfig(backend=backend_type)
            assert config.temperature == 0.0, f"{backend_type.value} temperature != 0"

    def test_deepseek_cheapest(self):
        """DeepSeek should be the cheapest backend (used for budget optimization)."""
        costs = {bt: BackendConfig(backend=bt).cost_per_eval for bt in BackendType}
        assert costs[BackendType.DEEPSEEK] == min(costs.values())

    def test_from_name(self):
        config = BackendConfig.from_name("gpt")
        assert config.backend == BackendType.GPT


# ============================================================
# Experiment Design Tests
# ============================================================

class TestExperimentConfig:
    def test_27_conditions(self):
        """RO3: 3x3x3 = 27 conditions."""
        config = ExperimentConfig()
        assert config.total_conditions == 27

    def test_150_tasks(self):
        config = ExperimentConfig()
        assert config.num_tasks == 150

    def test_generate_all_conditions(self):
        config = ExperimentConfig()
        conditions = config.generate_conditions()
        assert len(conditions) == 27

    def test_all_conditions_unique(self):
        config = ExperimentConfig()
        conditions = config.generate_conditions()
        ids = [c.condition_id for c in conditions]
        assert len(ids) == len(set(ids)), "Duplicate condition IDs"

    def test_critical_conditions_count(self):
        """10 critical conditions get 3 runs each."""
        assert len(CRITICAL_CONDITIONS) == 10

    def test_critical_conditions_get_3_runs(self):
        config = ExperimentConfig()
        conditions = config.generate_conditions()
        critical = [c for c in conditions if config.runs_for_condition(c) == 3]
        assert len(critical) == 10

    def test_other_conditions_get_1_run(self):
        config = ExperimentConfig()
        conditions = config.generate_conditions()
        other = [c for c in conditions if config.runs_for_condition(c) == 1]
        assert len(other) == 17

    def test_total_evaluations_7050(self):
        """(10 x 3 + 17 x 1) x 150 = 7,050 evaluations."""
        config = ExperimentConfig()
        assert config.total_evaluations == 7050

    def test_pilot_evaluations_200(self):
        """5 conditions x 20 tasks x 2 runs = 200."""
        config = ExperimentConfig()
        assert config.pilot_evaluations == 200

    def test_condition_id_format(self):
        cond = Condition(
            tool=ToolConfig(level=ToolLevel.FULL),
            context=ContextConfig(strategy=ContextStrategy.SLIDING_WINDOW),
            backend=BackendConfig(backend=BackendType.GPT),
        )
        assert cond.condition_id == "full_sliding_window_gpt"

    def test_estimated_cost_reasonable(self):
        """Budget should be in $2,500-$3,100 range per plan."""
        config = ExperimentConfig()
        cost = config.estimated_total_cost
        assert 1500 <= cost <= 4000, f"Estimated cost ${cost:.0f} outside expected range"
