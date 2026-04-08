"""LLM backend configuration for modular harness.

Supports 3 backends per RO3.
Default profile: Qwen (DashScope API)
Alternative profiles: Claude/GPT/DeepSeek, Ollama (local)
"""

from dataclasses import dataclass
from enum import Enum


class BackendType(str, Enum):
    CLAUDE = "claude"
    GPT = "gpt"
    DEEPSEEK = "deepseek"


# Active backend profile — switch between model families here
# Each profile maps the 3 abstract roles (CLAUDE=strong, GPT=mid, DEEPSEEK=budget)
# to concrete model IDs.
BACKEND_PROFILES = {
    "qwen": {
        BackendType.CLAUDE: {
            "model_id": "qwen3.5-122b-a10b",
            "provider": "dashscope",
            "cost_per_eval_usd": 0.30,
            "temperature": 0.0,
        },
        BackendType.GPT: {
            "model_id": "qwen3-max",
            "provider": "dashscope",
            "cost_per_eval_usd": 0.25,
            "temperature": 0.0,
        },
        BackendType.DEEPSEEK: {
            "model_id": "qwen2.5-7b-instruct-1m",
            "provider": "dashscope",
            "cost_per_eval_usd": 0.05,
            "temperature": 0.0,
        },
    },
    "original": {
        BackendType.CLAUDE: {
            "model_id": "claude-sonnet-4-20250514",
            "provider": "anthropic",
            "cost_per_eval_usd": 0.35,
            "temperature": 0.0,
        },
        BackendType.GPT: {
            "model_id": "gpt-4o-2025-03-01",
            "provider": "openai",
            "cost_per_eval_usd": 0.30,
            "temperature": 0.0,
        },
        BackendType.DEEPSEEK: {
            "model_id": "deepseek-chat",
            "provider": "deepseek",
            "cost_per_eval_usd": 0.15,
            "temperature": 0.0,
        },
    },
}

# Active profile — change this to switch model family
ACTIVE_PROFILE = "qwen"

BACKEND_REGISTRY = BACKEND_PROFILES[ACTIVE_PROFILE]


@dataclass
class BackendConfig:
    """Configuration for the LLM backend component."""

    backend: BackendType = BackendType.CLAUDE

    @property
    def model_id(self) -> str:
        return BACKEND_REGISTRY[self.backend]["model_id"]

    @property
    def provider(self) -> str:
        return BACKEND_REGISTRY[self.backend]["provider"]

    @property
    def cost_per_eval(self) -> float:
        return BACKEND_REGISTRY[self.backend]["cost_per_eval_usd"]

    @property
    def temperature(self) -> float:
        return BACKEND_REGISTRY[self.backend]["temperature"]

    @classmethod
    def from_name(cls, name: str) -> "BackendConfig":
        return cls(backend=BackendType(name.lower()))
