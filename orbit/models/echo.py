"""Deterministic echo provider for tests and offline demos."""

from __future__ import annotations

from typing import Any, Dict

from orbit.models.base import GenerateRequest, GenerateResult, ModelInfo, ModelProvider


class EchoProvider(ModelProvider):
    name = "echo"

    def health_check(self) -> Dict[str, Any]:
        return {"ok": True, "provider": "echo"}

    def info(self) -> ModelInfo:
        return ModelInfo(name="echo", provider="echo", supports_stream=True, context_length=8192)

    def generate(self, request: GenerateRequest) -> GenerateResult:
        if request.messages:
            last = request.messages[-1].get("content", "")
        else:
            last = request.prompt or ""
        text = f"[echo] {last}".strip()
        return GenerateResult(text=text, ok=True, provider="echo", model="echo")
