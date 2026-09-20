"""
Configurable chat templates.

Special tokens (aligned with tokenizer V2 plan):
  <pad> <unk> <bos> <eos> <system> <user> <assistant> <tool> <tool_result>
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


DEFAULT_SPECIAL = {
    "pad": "<pad>",
    "unk": "<unk>",
    "bos": "<bos>",
    "eos": "<eos>",
    "system": "<system>",
    "user": "<user>",
    "assistant": "<assistant>",
    "tool": "<tool>",
    "tool_result": "<tool_result>",
}


@dataclass
class ChatTemplate:
    """Simple role-tag chat template."""

    special: Dict[str, str] = field(default_factory=lambda: dict(DEFAULT_SPECIAL))
    add_generation_prompt: bool = True

    def format_message(self, role: str, content: str) -> str:
        tag = self.special.get(role, f"<{role}>")
        return f"{tag}\n{content}\n"

    def format(
        self,
        messages: List[Dict[str, str]],
        add_generation_prompt: Optional[bool] = None,
    ) -> str:
        parts = [self.special.get("bos", "<bos>")]
        for m in messages:
            role = m.get("role", "user")
            content = m.get("content", "")
            parts.append(self.format_message(role, content))
        do_gen = self.add_generation_prompt if add_generation_prompt is None else add_generation_prompt
        if do_gen:
            parts.append(self.special.get("assistant", "<assistant>") + "\n")
        return "".join(parts)


def apply_chat_template(
    messages: List[Dict[str, str]],
    template: Optional[ChatTemplate] = None,
    add_generation_prompt: bool = True,
) -> str:
    tpl = template or ChatTemplate()
    return tpl.format(messages, add_generation_prompt=add_generation_prompt)
