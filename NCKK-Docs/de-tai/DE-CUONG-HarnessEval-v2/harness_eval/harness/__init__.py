"""Modular harness: interfaces + factory for SWE-Agent integration.

Bridges harness_eval config system with SWE-Agent YAML configs.
"""

from harness_eval.harness.interfaces import (
    ContextStrategyProvider,
    LLMBackendProvider,
    ToolProvider,
)
from harness_eval.harness.factory import (
    HarnessConfig,
    create_harness_config,
    generate_all_configs,
    generate_sweagent_command,
)

__all__ = [
    "ContextStrategyProvider",
    "LLMBackendProvider",
    "ToolProvider",
    "HarnessConfig",
    "create_harness_config",
    "generate_all_configs",
    "generate_sweagent_command",
]
