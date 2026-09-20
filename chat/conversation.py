"""Conversation history — separate from model weights."""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional

from chat.template import ChatTemplate, apply_chat_template


@dataclass
class Message:
    role: str
    content: str
    ts: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class Conversation:
    def __init__(
        self,
        system_prompt: Optional[str] = None,
        template: Optional[ChatTemplate] = None,
        max_messages: int = 100,
    ):
        self.messages: List[Message] = []
        self.template = template or ChatTemplate()
        self.max_messages = max_messages
        if system_prompt:
            self.add("system", system_prompt)

    def add(self, role: str, content: str, **metadata) -> None:
        self.messages.append(Message(role=role, content=content, metadata=metadata))
        if len(self.messages) > self.max_messages:
            sys = [m for m in self.messages if m.role == "system"]
            rest = [m for m in self.messages if m.role != "system"]
            self.messages = sys + rest[-(self.max_messages - len(sys)) :]

    def add_user(self, content: str) -> None:
        self.add("user", content)

    def add_assistant(self, content: str) -> None:
        self.add("assistant", content)

    def add_tool(self, content: str, tool_name: str = "") -> None:
        self.add("tool", content, tool_name=tool_name)

    def add_tool_result(self, content: str, tool_name: str = "") -> None:
        self.add("tool_result", content, tool_name=tool_name)

    def as_dicts(self) -> List[Dict[str, str]]:
        return [{"role": m.role, "content": m.content} for m in self.messages]

    def render(self, add_generation_prompt: bool = True) -> str:
        return apply_chat_template(
            self.as_dicts(),
            template=self.template,
            add_generation_prompt=add_generation_prompt,
        )

    def clear(self, keep_system: bool = True) -> None:
        if keep_system:
            self.messages = [m for m in self.messages if m.role == "system"]
        else:
            self.messages.clear()

    def save(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump([m.to_dict() for m in self.messages], f, indent=2)

    def load(self, path: str) -> None:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.messages = [
            Message(
                role=d["role"],
                content=d["content"],
                ts=d.get("ts", time.time()),
                metadata=d.get("metadata", {}),
            )
            for d in data
        ]
