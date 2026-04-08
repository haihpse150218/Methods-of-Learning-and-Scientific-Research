"""Context strategy configuration for modular harness.

Supports 3 levels per RO2/RO3:
- Full context: Send entire conversation history
- Sliding window: Keep last N tokens (default 50K)
- Summary-based: Compress older context into summaries
"""

from dataclasses import dataclass
from enum import Enum


class ContextStrategy(str, Enum):
    FULL = "full"
    SLIDING_WINDOW = "sliding_window"
    SUMMARY = "summary"


@dataclass
class ContextConfig:
    """Configuration for the context management component of the harness."""

    strategy: ContextStrategy = ContextStrategy.FULL
    window_size_tokens: int = 50_000
    summary_max_tokens: int = 2_000

    @classmethod
    def from_strategy_name(cls, name: str, **kwargs) -> "ContextConfig":
        return cls(strategy=ContextStrategy(name.lower()), **kwargs)

    @property
    def description(self) -> str:
        if self.strategy == ContextStrategy.FULL:
            return "Full context (no truncation)"
        elif self.strategy == ContextStrategy.SLIDING_WINDOW:
            return f"Sliding window ({self.window_size_tokens:,} tokens)"
        else:
            return f"Summary-based (max {self.summary_max_tokens:,} tokens)"
