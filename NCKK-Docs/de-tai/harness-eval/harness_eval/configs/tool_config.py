"""Tool configuration for modular harness.

Supports 3 levels per RO2/RO3:
- Full (12 tools): All SWE-Agent tools
- Medium (8 tools): Core development tools
- Minimal (5 tools): Essential-only tools
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import ClassVar


class ToolLevel(str, Enum):
    FULL = "full"
    MEDIUM = "medium"
    MINIMAL = "minimal"


# Tool registry: all 12 tools available in SWE-Agent
FULL_TOOLS = [
    "bash",
    "python",
    "read",
    "write",
    "edit",
    "glob",
    "grep",
    "find",
    "git_diff",
    "git_log",
    "git_show",
    "test_runner",
]

MEDIUM_TOOLS = [
    "bash",
    "python",
    "read",
    "write",
    "edit",
    "grep",
    "git_diff",
    "test_runner",
]

MINIMAL_TOOLS = [
    "bash",
    "read",
    "write",
    "edit",
    "grep",
]


@dataclass
class ToolConfig:
    """Configuration for the tool system component of the harness."""

    level: ToolLevel = ToolLevel.FULL

    LEVEL_MAP: ClassVar[dict[ToolLevel, list[str]]] = {
        ToolLevel.FULL: FULL_TOOLS,
        ToolLevel.MEDIUM: MEDIUM_TOOLS,
        ToolLevel.MINIMAL: MINIMAL_TOOLS,
    }

    @property
    def tools(self) -> list[str]:
        return self.LEVEL_MAP[self.level]

    @property
    def tool_count(self) -> int:
        return len(self.tools)

    def has_tool(self, tool_name: str) -> bool:
        return tool_name in self.tools

    @classmethod
    def from_level_name(cls, name: str) -> "ToolConfig":
        return cls(level=ToolLevel(name.lower()))
