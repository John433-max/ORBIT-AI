"""GGUF provider (optional) + MCP adapter unit tests."""

from orbit.models.gguf import GGUFProvider
from orbit.models.base import GenerateRequest
from orbit.mcp.adapter import MCPToolAdapter, mcp_tools_to_registry
from tools.base import ToolCall, ToolRegistry


def test_gguf_missing_file_health():
    p = GGUFProvider(model_path="/nonexistent/model.gguf")
    hc = p.health_check()
    assert hc["ok"] is False
    assert "error" in hc


def test_gguf_generate_missing_file():
    p = GGUFProvider(model_path="/nonexistent/model.gguf")
    r = p.generate(GenerateRequest(prompt="hi"))
    assert r.ok is False


def test_mcp_adapter_handler():
    def add(a: int = 0, b: int = 0):
        return {"ok": True, "content": str(int(a) + int(b))}

    tool = MCPToolAdapter(
        name="mcp.add",
        description="add two numbers",
        parameters={
            "type": "object",
            "properties": {"a": {"type": "integer"}, "b": {"type": "integer"}},
            "required": ["a", "b"],
        },
        handler=add,
        permission_level="SAFE",
    )
    reg = ToolRegistry("SAFE")
    reg.register(tool)
    res = reg.execute(ToolCall(tool="mcp.add", arguments={"a": 2, "b": 3}))
    assert res.ok
    assert "5" in res.content


def test_mcp_tools_to_registry():
    reg = mcp_tools_to_registry(
        [
            {
                "name": "mcp.echo",
                "description": "echo",
                "handler": lambda text="": {"ok": True, "content": text},
                "permission_level": "SAFE",
            }
        ]
    )
    res = reg.execute(ToolCall(tool="mcp.echo", arguments={"text": "hi"}))
    assert res.ok and "hi" in res.content


def test_mcp_denied_under_safe_when_network():
    reg = ToolRegistry("SAFE")
    reg.register(
        MCPToolAdapter(
            name="mcp.web",
            description="net",
            handler=lambda: {"ok": True, "content": "x"},
            permission_level="NETWORK",
        )
    )
    res = reg.execute(ToolCall(tool="mcp.web", arguments={}))
    assert not res.ok
    assert "permission" in (res.error or "").lower()
