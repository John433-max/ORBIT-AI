"""Phase D/E: permissions + agent state machine."""

from tools.base import ToolRegistry, ToolCall, BaseTool, ToolResult
from orbit.core.state import AgentStateMachine, RunState, ToolCallRecord


class _SafeTool(BaseTool):
    name = "safe.ping"
    description = "ping"
    permission_level = "SAFE"
    parameters = {"type": "object", "properties": {}}

    def execute(self, **_):
        return ToolResult(ok=True, content="pong")


class _NetTool(BaseTool):
    name = "net.ping"
    description = "net"
    permission_level = "NETWORK"
    parameters = {"type": "object", "properties": {}}

    def execute(self, **_):
        return ToolResult(ok=True, content="net")


def test_permission_ordering():
    reg = ToolRegistry("SAFE")
    reg.register(_SafeTool())
    reg.register(_NetTool())
    assert reg.execute(ToolCall(tool="safe.ping")).ok
    denied = reg.execute(ToolCall(tool="net.ping"))
    assert not denied.ok and "permission" in (denied.error or "").lower()

    reg2 = ToolRegistry("NETWORK")
    reg2.register(_NetTool())
    assert reg2.execute(ToolCall(tool="net.ping")).ok


def test_legacy_full_allows_network():
    reg = ToolRegistry("FULL")
    reg.register(_NetTool())
    assert reg.execute(ToolCall(tool="net.ping")).ok


def test_state_machine_lifecycle():
    sm = AgentStateMachine(max_steps=5, max_tool_calls=3, timeout_s=10)
    run = sm.start("test task")
    assert run.run_id
    assert run.current_state == RunState.UNDERSTAND.value
    run.transition(RunState.PLAN)
    run.add_tool_call(ToolCallRecord(tool="calculator", ok=True, content="42"))
    assert len(run.tool_calls) == 1
    run.complete("42")
    assert run.status == "completed"
    assert sm.get(run.run_id) is run


def test_orchestrator_handle_includes_run_id():
    import importlib.util
    if importlib.util.find_spec("agents") is None:
        import pytest
        pytest.skip("agents.py not in checkout")
    from agents import Orchestrator

    orch = Orchestrator(sandbox_root=".")
    out = orch.handle("12*3")
    assert out.get("ok")
    if getattr(orch, "state_machine", None):
        assert out.get("run_id")
