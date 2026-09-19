"""MCP → ORBIT ToolRegistry adapter."""

from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional

from tools.base import BaseTool, ToolRegistry, ToolResult


class MCPToolAdapter(BaseTool):
    def __init__(
        self,
        name: str,
        description: str,
        parameters: Optional[Dict[str, Any]] = None,
        handler: Optional[Callable[..., Any]] = None,
        permission_level: str = "SAFE",
        timeout_s: float = 30.0,
        source: str = "mcp",
    ):
        self.name = name
        self.description = description or f"MCP tool {name}"
        self.parameters = parameters or {"type": "object", "properties": {}}
        self.permission_level = permission_level
        self.timeout_s = timeout_s
        self._handler = handler
        self.source = source

    def execute(self, **kwargs) -> ToolResult:
        if self._handler is None:
            return ToolResult(ok=False, content="", error=f"MCP tool {self.name} has no handler bound")
        try:
            out = self._handler(**kwargs)
            if isinstance(out, ToolResult):
                return out
            if isinstance(out, dict):
                return ToolResult(
                    ok=bool(out.get("ok", True)),
                    content=str(out.get("content") or out.get("text") or out),
                    data=out.get("data"),
                    error=out.get("error"),
                )
            return ToolResult(ok=True, content=str(out))
        except Exception as e:
            return ToolResult(ok=False, content="", error=str(e))


def mcp_tools_to_registry(
    descriptors: List[Dict[str, Any]],
    registry: Optional[ToolRegistry] = None,
    permission_level: str = "SAFE",
) -> ToolRegistry:
    reg = registry or ToolRegistry(permission_level=permission_level)
    for d in descriptors or []:
        name = d.get("name")
        if not name:
            continue
        tool = MCPToolAdapter(
            name=name,
            description=d.get("description") or "",
            parameters=d.get("parameters"),
            handler=d.get("handler"),
            permission_level=d.get("permission_level") or "SAFE",
            timeout_s=float(d.get("timeout_s") or 30),
            source=d.get("source") or "mcp",
        )
        reg.register(tool)
    return reg
