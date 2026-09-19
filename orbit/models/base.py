"""Common ModelProvider interface (Phase C)."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Iterator, List, Optional


@dataclass
class ModelInfo:
    name: str
    provider: str
    supports_tools: bool = False
    supports_stream: bool = False
    context_length: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "provider": self.provider,
            "supports_tools": self.supports_tools,
            "supports_stream": self.supports_stream,
            "context_length": self.context_length,
            "metadata": self.metadata,
        }


@dataclass
class GenerateRequest:
    prompt: str = ""
    messages: List[Dict[str, str]] = field(default_factory=list)
    max_tokens: int = 128
    temperature: float = 0.7
    stop: Optional[List[str]] = None
    stream: bool = False


@dataclass
class GenerateResult:
    text: str
    ok: bool = True
    error: Optional[str] = None
    provider: str = ""
    model: str = ""
    usage: Dict[str, int] = field(default_factory=dict)
    raw: Any = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "ok": self.ok,
            "error": self.error,
            "provider": self.provider,
            "model": self.model,
            "usage": self.usage,
        }


class ModelProvider(ABC):
    """Backend-agnostic text generation."""

    name: str = "base"

    @abstractmethod
    def health_check(self) -> Dict[str, Any]:
        ...

    @abstractmethod
    def info(self) -> ModelInfo:
        ...

    @abstractmethod
    def generate(self, request: GenerateRequest) -> GenerateResult:
        ...

    def stream(self, request: GenerateRequest) -> Iterator[str]:
        """Default: yield full generate() text once."""
        result = self.generate(request)
        if result.text:
            yield result.text

    def count_tokens(self, text: str) -> int:
        return max(1, len(text or "") // 4)

    def supports_tools(self) -> bool:
        return False
