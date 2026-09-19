"""Agent run state machine (Phase E)."""

from __future__ import annotations

import time
import uuid
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class RunState(str, Enum):
    RECEIVE = "RECEIVE"
    UNDERSTAND = "UNDERSTAND"
    PLAN = "PLAN"
    SELECT_TOOL = "SELECT_TOOL"
    EXECUTE = "EXECUTE"
    OBSERVE = "OBSERVE"
    VERIFY = "VERIFY"
    CONTINUE = "CONTINUE"
    ANSWER = "ANSWER"
    FAILED = "FAILED"
    DONE = "DONE"


@dataclass
class ToolCallRecord:
    tool: str
    arguments: Dict[str, Any] = field(default_factory=dict)
    ok: bool = False
    content: str = ""
    error: Optional[str] = None
    latency_ms: float = 0.0


@dataclass
class AgentRun:
    task: str
    run_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    current_state: str = RunState.RECEIVE.value
    step_number: int = 0
    plan: List[str] = field(default_factory=list)
    tool_calls: List[ToolCallRecord] = field(default_factory=list)
    observations: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    final_answer: str = ""
    status: str = "running"
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    max_steps: int = 20
    max_tool_calls: int = 30
    timeout_s: float = 120.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def touch(self) -> None:
        self.updated_at = time.time()

    def transition(self, state: RunState | str) -> None:
        self.current_state = state.value if isinstance(state, RunState) else str(state)
        self.step_number += 1
        self.touch()

    def add_tool_call(self, record: ToolCallRecord) -> None:
        self.tool_calls.append(record)
        if record.content:
            self.observations.append(record.content[:2000])
        if record.error:
            self.errors.append(record.error)
        self.touch()

    def elapsed_s(self) -> float:
        return time.time() - self.created_at

    def should_stop(self) -> Optional[str]:
        if self.step_number >= self.max_steps:
            return "max_steps"
        if len(self.tool_calls) >= self.max_tool_calls:
            return "max_tool_calls"
        if self.elapsed_s() >= self.timeout_s:
            return "timed_out"
        return None

    def complete(self, answer: str, status: str = "completed") -> None:
        self.final_answer = answer
        self.status = status
        self.current_state = RunState.DONE.value if status == "completed" else RunState.FAILED.value
        self.touch()

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class AgentStateMachine:
    def __init__(self, max_steps: int = 20, max_tool_calls: int = 30, timeout_s: float = 120.0):
        self.max_steps = max_steps
        self.max_tool_calls = max_tool_calls
        self.timeout_s = timeout_s
        self.runs: Dict[str, AgentRun] = {}

    def start(self, task: str) -> AgentRun:
        run = AgentRun(
            task=task,
            max_steps=self.max_steps,
            max_tool_calls=self.max_tool_calls,
            timeout_s=self.timeout_s,
        )
        run.transition(RunState.UNDERSTAND)
        self.runs[run.run_id] = run
        return run

    def get(self, run_id: str) -> Optional[AgentRun]:
        return self.runs.get(run_id)
