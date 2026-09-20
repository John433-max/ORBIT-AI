"""Required edge-case tests (audit Phase 5)."""

from __future__ import annotations

import time

import pytest


def test_calculator_large_integer_exact():
    from calculator import parse_and_calculate

    r = parse_and_calculate("999999999*999999999")
    assert r["ok"] is True
    assert r["result"] == 999999998000000001


def test_calculator_division_by_zero():
    from calculator import parse_and_calculate

    r = parse_and_calculate("1/0")
    assert r["ok"] is False
    assert "zero" in (r.get("error") or "").lower()


def test_agent_missing_tool_safe():
    from tools.base import ToolRegistry, ToolCall

    reg = ToolRegistry("SAFE")
    res = reg.execute(ToolCall(tool="does.not.exist", arguments={}))
    assert res.ok is False
    assert "Unknown tool" in (res.error or "")


def test_agent_tool_exception_structured():
    from tools.base import BaseTool, ToolRegistry, ToolCall, ToolResult

    class Boom(BaseTool):
        name = "test.boom"
        description = "raises"
        permission_level = "SAFE"
        parameters = {"type": "object", "properties": {}}

        def execute(self, **_):
            raise RuntimeError("intentional boom")

    reg = ToolRegistry("SAFE")
    reg.register(Boom())
    res = reg.execute(ToolCall(tool="test.boom", arguments={}))
    assert res.ok is False
    assert res.error


def test_thinking_state_machine_max_steps():
    from orbit.core.state import AgentStateMachine

    sm = AgentStateMachine(max_steps=3, max_tool_calls=10, timeout_s=60)
    run = sm.start("task")
    for _ in range(5):
        run.transition("EXECUTE")
    assert run.should_stop() == "max_steps"


def test_memory_two_independent_sessions():
    agents = pytest.importorskip("agents")
    Orchestrator = agents.Orchestrator

    a = Orchestrator(sandbox_root=".")
    b = Orchestrator(sandbox_root=".")
    a.handle("my name is SessionAlpha")
    b.handle("my name is SessionBeta")
    ca = a.handle("what is my name").get("content") or ""
    cb = b.handle("what is my name").get("content") or ""
    assert "Alpha" in ca
    assert "Beta" in cb
    assert "Alpha" not in cb
    assert "Beta" not in ca


def test_rag_no_relevant_documents_honest():
    agents = pytest.importorskip("agents")
    Orchestrator = agents.Orchestrator

    o = Orchestrator(sandbox_root=".")
    out = o.handle("according to the document what is the secret UNIQ_CODE_ZZZ")
    text = (out.get("content") or "").lower()
    honest = (
        "don't have a document" in text
        or "don't have any" in text
        or "no document" in text
        or "indexed document" in text
        or "upload" in text
    )
    assert honest, text
    assert "UNIQ_CODE_ZZZ" not in (out.get("content") or "") or "don't" in text


def test_sandbox_timeout_stops():
    from tools.base import ToolRegistry, ToolCall
    from tools.python import PythonTool

    reg = ToolRegistry("EXECUTION")
    reg.register(PythonTool())
    t0 = time.time()
    res = reg.execute(
        ToolCall(tool="python.execute", arguments={"code": "while True:\n    pass", "timeout": 2})
    )
    dt = time.time() - t0
    assert res.ok is False
    assert dt < 8
    err = (res.error or "") + str(res.data or "")
    assert "time" in err.lower() or "timeout" in err.lower()


def test_sandbox_blocks_os_import():
    from tools.base import ToolRegistry, ToolCall
    from tools.python import PythonTool

    reg = ToolRegistry("EXECUTION")
    reg.register(PythonTool())
    res = reg.execute(
        ToolCall(tool="python.execute", arguments={"code": "import os\nprint(os.getcwd())"})
    )
    assert res.ok is False


def test_permission_cannot_escalate():
    from tools.base import ToolRegistry, ToolCall
    from tools.python import PythonTool

    reg = ToolRegistry("SAFE")
    reg.register(PythonTool())
    res = reg.execute(ToolCall(tool="python.execute", arguments={"code": "print(1)"}))
    assert res.ok is False
    assert "permission" in (res.error or "").lower()
