"""
Structured tool-calling agent (ORBIT v2 Phase 18/19 foundation).

Instead of pure keyword routing, this agent:
1. Receives a user message
2. Optionally decides a tool is needed (heuristic for now; later: LLM)
3. Emits a structured ToolCall
4. Validates + executes via ToolRegistry
5. Returns observation + optional final answer

The original keyword Orchestrator in agents.py is preserved.
"""

from __future__ import annotations

import json
import re
from typing import Any, Dict, List, Optional

from tools import ToolRegistry, ToolCall, ToolResult, default_registry
from agent.planner import Planner


class ToolCallingAgent:
    """
    Minimal structured tool-calling loop.

    Configurable:
      - max_iterations
      - permission_level
      - allowed_tools (None = all registered that pass permission)
    """

    def __init__(
        self,
        registry: Optional[ToolRegistry] = None,
        permission_level: str = "SAFE",
        max_iterations: int = 5,
        allowed_tools: Optional[List[str]] = None,
    ):
        self.registry = registry or default_registry(permission_level)
        self.registry.permission_level = permission_level.upper()
        self.max_iterations = max_iterations
        self.allowed_tools = set(allowed_tools) if allowed_tools else None
        self.planner = Planner()

    def _parse_tool_call(self, text: str) -> Optional[ToolCall]:
        text = text.strip()
        if text.startswith("{") and "tool" in text:
            try:
                d = json.loads(text)
                if "tool" in d:
                    return ToolCall.from_dict(d)
            except json.JSONDecodeError:
                pass
        m = re.search(r"\{[^{}]*\"tool\"[^{}]*\}", text, re.DOTALL)
        if m:
            try:
                d = json.loads(m.group(0))
                if "tool" in d:
                    return ToolCall.from_dict(d)
            except json.JSONDecodeError:
                pass
        return None

    def _heuristic_tool(self, message: str) -> Optional[ToolCall]:
        msg = message.strip().lower()
        if re.search(r"[\d\s\+\-\*/\(\)\.]+", message) and any(
            op in message for op in "+-*/"
        ):
            expr = re.sub(r"[^0-9\+\-\*/\(\)\.\s]", "", message).strip()
            if expr and any(c.isdigit() for c in expr):
                return ToolCall(tool="calculator", arguments={"expression": expr})
        if msg.startswith("search:") or msg.startswith("web:"):
            q = message.split(":", 1)[1].strip()
            return ToolCall(tool="web.search", arguments={"query": q})
        return None

    def execute_parallel(self, calls: List[ToolCall]) -> List[Dict[str, Any]]:
        out = []
        for i, call in enumerate(calls):
            if self.allowed_tools is not None and call.tool not in self.allowed_tools:
                out.append({"iteration": i, "call": call.to_dict(),
                            "result": {"ok": False, "error": f"Tool not allowed: {call.tool}"}})
                continue
            result = self.registry.execute(call)
            out.append({"iteration": i, "call": call.to_dict(), "result": result.to_dict()})
        return out

    def run(self, message: str, history: Optional[List[Dict]] = None) -> Dict[str, Any]:
        history = history or []
        observations: List[Dict[str, Any]] = []
        call = self._parse_tool_call(message)
        planned_calls: List[ToolCall] = []
        if call is not None:
            planned_calls = [call]
        else:
            plan = self.planner.plan(message)
            for step in plan.steps:
                if step.action == "tool" and step.tool:
                    planned_calls.append(ToolCall(tool=step.tool, arguments=step.arguments))
            if not planned_calls:
                h = self._heuristic_tool(message)
                if h is not None:
                    planned_calls = [h]

        for i, call in enumerate(planned_calls[: self.max_iterations]):
            if self.allowed_tools is not None and call.tool not in self.allowed_tools:
                observations.append({
                    "iteration": i,
                    "call": call.to_dict(),
                    "result": {"ok": False, "error": f"Tool not allowed: {call.tool}"},
                })
                break
            result: ToolResult = self.registry.execute(call)
            observations.append({
                "iteration": i,
                "call": call.to_dict(),
                "result": result.to_dict(),
            })
            if not result.ok:
                break

        if observations:
            parts = []
            all_ok = True
            for obs in observations:
                res = obs["result"]
                ok = res.get("ok", False)
                all_ok = all_ok and ok
                c = res.get("content") or res.get("error") or ""
                if not isinstance(c, str):
                    c = str(c)
                tool_name = obs["call"].get("tool", "tool")
                parts.append(f"[{tool_name}] {c}" if len(observations) > 1 else c)
            return {
                "ok": all_ok,
                "content": "\n".join(parts),
                "observations": observations,
                "source": "tool_calling_agent",
                "openai_tools": self.registry.openai_tools(),
            }

        return {
            "ok": True,
            "content": (
                "No tool was selected. Provide a structured tool call, e.g.\n"
                '{"tool": "calculator", "arguments": {"expression": "2+2"}}'
            ),
            "observations": [],
            "source": "tool_calling_agent",
            "openai_tools": self.registry.openai_tools(),
        }
