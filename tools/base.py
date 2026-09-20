"""
Standard tool interface for ORBIT v2.

Every tool must define:
  - name
  - description
  - parameters (JSON-schema style)
  - execute(**kwargs) -> ToolResult
"""

from __future__ import annotations

import time
import collections
from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional

MAX_TOOL_CONTENT_CHARS = 4000  # agent context efficiency


@dataclass
class ToolResult:
    ok: bool
    content: str
    data: Any = None
    error: Optional[str] = None
    latency_ms: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ToolCall:
    """Structured tool call produced by the model / agent."""
    tool: str
    arguments: Dict[str, Any] = field(default_factory=dict)
    id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        d = {"tool": self.tool, "arguments": self.arguments}
        if self.id is not None:
            d["id"] = self.id
        return d

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ToolCall":
        return cls(
            tool=d["tool"],
            arguments=d.get("arguments", d.get("args", {})),
            id=d.get("id"),
        )


class BaseTool(ABC):
    """Abstract base class for all ORBIT tools."""

    name: str = "base"
    description: str = ""
    parameters: Dict[str, Any] = {}
    timeout_s: float = 30.0
    permission_level: str = "SAFE"

    def schema(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
            "permission_level": self.permission_level,
        }

    def openai_tool(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters if self.parameters else {"type": "object", "properties": {}},
            },
        }

    def validate_args(self, arguments: Dict[str, Any]) -> Optional[str]:
        required = self.parameters.get("required", [])
        props = self.parameters.get("properties", {})
        for key in required:
            if key not in arguments:
                return f"Missing required argument: {key}"
        for key, val in arguments.items():
            if key not in props:
                continue
            expected = props[key].get("type")
            if expected == "string" and not isinstance(val, str):
                return f"Argument {key} must be string"
            if expected == "number" and not isinstance(val, (int, float)):
                return f"Argument {key} must be number"
            if expected == "integer" and not isinstance(val, int):
                return f"Argument {key} must be integer"
            if expected == "boolean" and not isinstance(val, bool):
                return f"Argument {key} must be boolean"
        return None

    @abstractmethod
    def execute(self, **kwargs) -> ToolResult:
        ...

    def __call__(self, **kwargs) -> ToolResult:
        err = self.validate_args(kwargs)
        if err:
            return ToolResult(ok=False, content="", error=err)
        t0 = time.perf_counter()
        try:
            result = self.execute(**kwargs)
            result.latency_ms = (time.perf_counter() - t0) * 1000.0
            if result.content and len(result.content) > MAX_TOOL_CONTENT_CHARS:
                result.content = (
                    result.content[:MAX_TOOL_CONTENT_CHARS] + "\n…[truncated for context]"
                )
            return result
        except Exception as e:
            return ToolResult(
                ok=False,
                content="",
                error=f"{type(e).__name__}: {e}",
                latency_ms=(time.perf_counter() - t0) * 1000.0,
            )


class ToolRegistry:
    """Register and look up tools by name; enforce permission levels."""

    LEVELS = {
        "SAFE": 0,
        "READ_ONLY": 1,
        "WRITE": 2,
        "NETWORK": 3,
        "EXECUTION": 4,
        "PRIVILEGED": 5,
        "LIMITED": 2,
        "FULL": 5,
    }

    def __init__(self, permission_level: str = "SAFE"):
        self._tools: Dict[str, BaseTool] = {}
        self.permission_level = permission_level.upper()
        self.call_log = collections.deque(maxlen=1000)

    def register(self, tool: BaseTool) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> Optional[BaseTool]:
        return self._tools.get(name)

    def list_tools(self) -> List[Dict[str, Any]]:
        return [t.schema() for t in self._tools.values()]

    def openai_tools(self) -> List[Dict[str, Any]]:
        return [t.openai_tool() for t in self._tools.values() if self.allowed(t)]

    def allowed(self, tool: BaseTool) -> bool:
        need = self.LEVELS.get(tool.permission_level.upper(), 99)
        have = self.LEVELS.get(self.permission_level, 0)
        return have >= need

    def execute(self, call: ToolCall) -> ToolResult:
        tool = self.get(call.tool)
        if tool is None:
            result = ToolResult(ok=False, content="", error=f"Unknown tool: {call.tool}")
            self._record(call.tool, result, denied=False, unknown=True)
            return result
        if not self.allowed(tool):
            result = ToolResult(
                ok=False,
                content="",
                error=f"Tool {call.tool} requires permission {tool.permission_level}, "
                      f"current level is {self.permission_level}",
            )
            self._record(call.tool, result, denied=True, unknown=False)
            return result
        result = tool(**call.arguments)
        self._record(call.tool, result, denied=False, unknown=False)
        return result

    def _record(self, name: str, result: ToolResult, *, denied: bool, unknown: bool) -> None:
        self.call_log.append(
            {
                "tool": name,
                "ok": bool(result.ok),
                "denied": denied,
                "unknown": unknown,
                "error": result.error,
                "latency_ms": float(result.latency_ms or 0.0),
            }
        )

    def metrics(self) -> Dict[str, Any]:
        log = list(self.call_log)
        by: Dict[str, Dict[str, Any]] = {}
        for e in log:
            name = e.get("tool") or "unknown"
            slot = by.setdefault(
                name,
                {"calls": 0, "ok": 0, "errors": 0, "denied": 0, "unknown": 0, "total_ms": 0.0},
            )
            slot["calls"] += 1
            if e.get("ok"):
                slot["ok"] += 1
            if e.get("error"):
                slot["errors"] += 1
            if e.get("denied"):
                slot["denied"] += 1
            if e.get("unknown"):
                slot["unknown"] += 1
            slot["total_ms"] += float(e.get("latency_ms") or 0.0)
        for s in by.values():
            s["ok_rate"] = (s["ok"] / s["calls"]) if s["calls"] else 0.0
            s["avg_ms"] = (s["total_ms"] / s["calls"]) if s["calls"] else 0.0
        return {
            "total_calls": len(log),
            "by_tool": by,
            "recent": log[-10:],
        }
