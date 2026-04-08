"""Abstract interfaces for the 3 swappable harness layers.

Layer 1: ToolProvider — controls which tools the agent can use
Layer 2: ContextStrategyProvider — controls history/context management
Layer 3: LLMBackendProvider — controls which LLM backend is used

Each provider maps to a SWE-Agent YAML config file.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from harness_eval.configs.tool_config import ToolConfig, ToolLevel
from harness_eval.configs.context_config import ContextConfig, ContextStrategy
from harness_eval.configs.backend_config import BackendConfig, BackendType


class ToolProvider(ABC):
    """Layer 1: Provides tool configuration for the agent."""

    @abstractmethod
    def get_tool_level(self) -> ToolLevel: ...

    @abstractmethod
    def get_sweagent_config_path(self) -> str: ...

    @abstractmethod
    def get_tools(self) -> list[str]: ...


class ContextStrategyProvider(ABC):
    """Layer 2: Provides context/history management strategy."""

    @abstractmethod
    def get_strategy(self) -> ContextStrategy: ...

    @abstractmethod
    def get_sweagent_config_path(self) -> str: ...

    @abstractmethod
    def get_max_tokens(self) -> int | None: ...


class LLMBackendProvider(ABC):
    """Layer 3: Provides LLM backend configuration."""

    @abstractmethod
    def get_backend_type(self) -> BackendType: ...

    @abstractmethod
    def get_sweagent_config_path(self) -> str: ...

    @abstractmethod
    def get_model_id(self) -> str: ...


# ── Concrete implementations ────────────────────────


class FullToolProvider(ToolProvider):
    def get_tool_level(self) -> ToolLevel:
        return ToolLevel.FULL

    def get_sweagent_config_path(self) -> str:
        return "config/harness_eval/tool_full.yaml"

    def get_tools(self) -> list[str]:
        return ToolConfig(ToolLevel.FULL).tools


class MediumToolProvider(ToolProvider):
    def get_tool_level(self) -> ToolLevel:
        return ToolLevel.MEDIUM

    def get_sweagent_config_path(self) -> str:
        return "config/harness_eval/tool_medium.yaml"

    def get_tools(self) -> list[str]:
        return ToolConfig(ToolLevel.MEDIUM).tools


class MinimalToolProvider(ToolProvider):
    def get_tool_level(self) -> ToolLevel:
        return ToolLevel.MINIMAL

    def get_sweagent_config_path(self) -> str:
        return "config/harness_eval/tool_minimal.yaml"

    def get_tools(self) -> list[str]:
        return ToolConfig(ToolLevel.MINIMAL).tools


class FullContextProvider(ContextStrategyProvider):
    def get_strategy(self) -> ContextStrategy:
        return ContextStrategy.FULL

    def get_sweagent_config_path(self) -> str:
        return "config/harness_eval/ctx_full.yaml"

    def get_max_tokens(self) -> int | None:
        return None  # no limit


class SlidingWindowContextProvider(ContextStrategyProvider):
    def get_strategy(self) -> ContextStrategy:
        return ContextStrategy.SLIDING_WINDOW

    def get_sweagent_config_path(self) -> str:
        return "config/harness_eval/ctx_sliding_window.yaml"

    def get_max_tokens(self) -> int | None:
        return 50_000


class SummaryContextProvider(ContextStrategyProvider):
    def get_strategy(self) -> ContextStrategy:
        return ContextStrategy.SUMMARY

    def get_sweagent_config_path(self) -> str:
        return "config/harness_eval/ctx_summary.yaml"

    def get_max_tokens(self) -> int | None:
        return 2_000


class ClaudeBackendProvider(LLMBackendProvider):
    """Strong backend: qwen3.5-122b-a10b (replaces Claude Sonnet 4)."""

    def get_backend_type(self) -> BackendType:
        return BackendType.CLAUDE

    def get_sweagent_config_path(self) -> str:
        return "config/harness_eval/be_qwen_large.yaml"

    def get_model_id(self) -> str:
        return BackendConfig(BackendType.CLAUDE).model_id


class GPTBackendProvider(LLMBackendProvider):
    """Mid-tier backend: qwen3-max (replaces GPT-4o)."""

    def get_backend_type(self) -> BackendType:
        return BackendType.GPT

    def get_sweagent_config_path(self) -> str:
        return "config/harness_eval/be_qwen_mid.yaml"

    def get_model_id(self) -> str:
        return BackendConfig(BackendType.GPT).model_id


class DeepSeekBackendProvider(LLMBackendProvider):
    """Budget backend: qwen2.5-7b-instruct-1m (replaces DeepSeek-V3)."""

    def get_backend_type(self) -> BackendType:
        return BackendType.DEEPSEEK

    def get_sweagent_config_path(self) -> str:
        return "config/harness_eval/be_qwen_small.yaml"

    def get_model_id(self) -> str:
        return BackendConfig(BackendType.DEEPSEEK).model_id


# ── Factories ────────────────────────────────────────

TOOL_PROVIDERS: dict[ToolLevel, type[ToolProvider]] = {
    ToolLevel.FULL: FullToolProvider,
    ToolLevel.MEDIUM: MediumToolProvider,
    ToolLevel.MINIMAL: MinimalToolProvider,
}

CONTEXT_PROVIDERS: dict[ContextStrategy, type[ContextStrategyProvider]] = {
    ContextStrategy.FULL: FullContextProvider,
    ContextStrategy.SLIDING_WINDOW: SlidingWindowContextProvider,
    ContextStrategy.SUMMARY: SummaryContextProvider,
}

BACKEND_PROVIDERS: dict[BackendType, type[LLMBackendProvider]] = {
    BackendType.CLAUDE: ClaudeBackendProvider,
    BackendType.GPT: GPTBackendProvider,
    BackendType.DEEPSEEK: DeepSeekBackendProvider,
}


def get_tool_provider(level: ToolLevel) -> ToolProvider:
    return TOOL_PROVIDERS[level]()


def get_context_provider(strategy: ContextStrategy) -> ContextStrategyProvider:
    return CONTEXT_PROVIDERS[strategy]()


def get_backend_provider(backend: BackendType) -> LLMBackendProvider:
    return BACKEND_PROVIDERS[backend]()
