"""Experiment configuration: defines a full factorial design.

27 conditions = 3 (Tool) x 3 (Context) x 3 (Backend)
"""

from dataclasses import dataclass, field
from itertools import product

from harness_eval.configs.tool_config import ToolConfig, ToolLevel
from harness_eval.configs.context_config import ContextConfig, ContextStrategy
from harness_eval.configs.backend_config import BackendConfig, BackendType


@dataclass
class Condition:
    """A single experimental condition (one cell in the 3x3x3 design)."""

    tool: ToolConfig
    context: ContextConfig
    backend: BackendConfig

    @property
    def condition_id(self) -> str:
        return f"{self.tool.level.value}_{self.context.strategy.value}_{self.backend.backend.value}"

    @property
    def estimated_cost_per_task(self) -> float:
        return self.backend.cost_per_eval

    def __repr__(self) -> str:
        return (
            f"Condition(tool={self.tool.level.value}, "
            f"context={self.context.strategy.value}, "
            f"backend={self.backend.backend.value})"
        )


# 10 most important conditions that get 3 runs each
CRITICAL_CONDITIONS = {
    # All full (baseline)
    ("full", "full", "claude"),
    ("full", "full", "gpt"),
    ("full", "full", "deepseek"),
    # Minimal tool (max ablation)
    ("minimal", "full", "claude"),
    ("minimal", "full", "gpt"),
    # Summary context (max context ablation)
    ("full", "summary", "claude"),
    ("full", "summary", "gpt"),
    # Cross extremes
    ("minimal", "summary", "claude"),
    ("minimal", "summary", "gpt"),
    ("minimal", "summary", "deepseek"),
}


@dataclass
class ExperimentConfig:
    """Full factorial experiment design (3x3x3 = 27 conditions)."""

    num_tasks: int = 150
    pilot_tasks: int = 20
    critical_runs: int = 3
    other_runs: int = 1

    def generate_conditions(self) -> list[Condition]:
        conditions = []
        for tool_level, ctx_strategy, backend_type in product(
            ToolLevel, ContextStrategy, BackendType
        ):
            conditions.append(
                Condition(
                    tool=ToolConfig(level=tool_level),
                    context=ContextConfig(strategy=ctx_strategy),
                    backend=BackendConfig(backend=backend_type),
                )
            )
        return conditions

    @property
    def total_conditions(self) -> int:
        return len(list(product(ToolLevel, ContextStrategy, BackendType)))

    def runs_for_condition(self, condition: Condition) -> int:
        key = (
            condition.tool.level.value,
            condition.context.strategy.value,
            condition.backend.backend.value,
        )
        return self.critical_runs if key in CRITICAL_CONDITIONS else self.other_runs

    @property
    def total_evaluations(self) -> int:
        total = 0
        for cond in self.generate_conditions():
            total += self.runs_for_condition(cond) * self.num_tasks
        return total

    @property
    def pilot_evaluations(self) -> int:
        return 5 * self.pilot_tasks * 2  # 5 conditions x 20 tasks x 2 runs

    @property
    def estimated_total_cost(self) -> float:
        total = 0.0
        for cond in self.generate_conditions():
            runs = self.runs_for_condition(cond)
            total += runs * self.num_tasks * cond.estimated_cost_per_task
        return total
