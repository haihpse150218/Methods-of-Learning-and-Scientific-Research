"""Factory for creating harness configurations and SWE-Agent commands.

Composes ToolProvider + ContextStrategyProvider + LLMBackendProvider
into a single HarnessConfig that can generate SWE-Agent CLI commands.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from pathlib import Path

from harness_eval.configs.tool_config import ToolLevel
from harness_eval.configs.context_config import ContextStrategy
from harness_eval.configs.backend_config import BackendType
from harness_eval.configs.experiment import CRITICAL_CONDITIONS
from harness_eval.harness.interfaces import (
    ToolProvider,
    ContextStrategyProvider,
    LLMBackendProvider,
    get_tool_provider,
    get_context_provider,
    get_backend_provider,
)


@dataclass
class HarnessConfig:
    """A complete harness configuration for one experimental condition."""

    tool: ToolProvider
    context: ContextStrategyProvider
    backend: LLMBackendProvider

    @property
    def condition_id(self) -> str:
        return (
            f"{self.tool.get_tool_level().value}"
            f"_{self.context.get_strategy().value}"
            f"_{self.backend.get_backend_type().value}"
        )

    @property
    def is_critical(self) -> bool:
        key = (
            self.tool.get_tool_level().value,
            self.context.get_strategy().value,
            self.backend.get_backend_type().value,
        )
        return key in CRITICAL_CONDITIONS

    @property
    def sweagent_config_paths(self) -> list[str]:
        """Return ordered list of SWE-Agent YAML config paths to compose."""
        return [
            "config/harness_eval/base.yaml",
            self.tool.get_sweagent_config_path(),
            self.context.get_sweagent_config_path(),
            self.backend.get_sweagent_config_path(),
        ]

    def describe(self) -> str:
        return (
            f"Condition: {self.condition_id}\n"
            f"  Tool:    {self.tool.get_tool_level().value} ({len(self.tool.get_tools())} tools)\n"
            f"  Context: {self.context.get_strategy().value} (max_tokens={self.context.get_max_tokens()})\n"
            f"  Backend: {self.backend.get_model_id()}\n"
            f"  Critical: {self.is_critical}"
        )


def create_harness_config(
    tool: ToolLevel | str,
    context: ContextStrategy | str,
    backend: BackendType | str,
) -> HarnessConfig:
    """Create a HarnessConfig from enum values or string names.

    Examples:
        create_harness_config("full", "sliding_window", "claude")
        create_harness_config(ToolLevel.MINIMAL, ContextStrategy.SUMMARY, BackendType.DEEPSEEK)
    """
    if isinstance(tool, str):
        tool = ToolLevel(tool)
    if isinstance(context, str):
        context = ContextStrategy(context)
    if isinstance(backend, str):
        backend = BackendType(backend)

    return HarnessConfig(
        tool=get_tool_provider(tool),
        context=get_context_provider(context),
        backend=get_backend_provider(backend),
    )


def generate_all_configs() -> list[HarnessConfig]:
    """Generate all 27 HarnessConfigs (3x3x3 factorial design)."""
    configs = []
    for tool, ctx, be in product(ToolLevel, ContextStrategy, BackendType):
        configs.append(create_harness_config(tool, ctx, be))
    return configs


def generate_sweagent_command(
    config: HarnessConfig,
    output_dir: str = "trajectories/harness_eval",
    sweagent_dir: str | Path = ".",
    extra_args: list[str] | None = None,
) -> str:
    """Generate a SWE-Agent CLI command for a given condition.

    Args:
        config: HarnessConfig for the condition.
        output_dir: Base output directory for trajectories.
        sweagent_dir: Path to SWE-Agent installation.
        extra_args: Additional CLI arguments.

    Returns:
        Full CLI command string.
    """
    sweagent_dir = Path(sweagent_dir)
    cond_output = f"{output_dir}/{config.condition_id}"

    parts = ["python -m sweagent run-batch"]
    for cfg_path in config.sweagent_config_paths:
        parts.append(f"  --config {cfg_path}")
    parts.append(f"  --output_dir {cond_output}")

    if extra_args:
        for arg in extra_args:
            parts.append(f"  {arg}")

    return " \\\n".join(parts)


def generate_run_script(
    configs: list[HarnessConfig] | None = None,
    output_dir: str = "trajectories/harness_eval",
    runs_per_critical: int = 3,
    runs_per_other: int = 1,
) -> str:
    """Generate a bash script that runs all conditions sequentially.

    Args:
        configs: List of configs (default: all 27).
        output_dir: Base output directory.
        runs_per_critical: Number of runs for critical conditions.
        runs_per_other: Number of runs for other conditions.

    Returns:
        Bash script content.
    """
    if configs is None:
        configs = generate_all_configs()

    lines = [
        "#!/bin/bash",
        "# HarnessEval — Run all conditions",
        f"# Generated for {len(configs)} conditions",
        "set -euo pipefail",
        "",
    ]

    for i, cfg in enumerate(configs, 1):
        runs = runs_per_critical if cfg.is_critical else runs_per_other
        lines.append(f"# [{i}/{len(configs)}] {cfg.condition_id} ({runs} run(s))")
        for run_idx in range(runs):
            cmd = generate_sweagent_command(cfg, output_dir=f"{output_dir}/run_{run_idx}")
            lines.append(cmd)
            lines.append("")

    return "\n".join(lines)
