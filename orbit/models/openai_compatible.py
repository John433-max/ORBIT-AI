"""OpenAI-compatible HTTP adapter (local or remote /v1)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from orbit.models.base import GenerateRequest, GenerateResult, ModelInfo, ModelProvider


class OpenAICompatibleProvider(ModelProvider):
    name = "openai"

    def __init__(
        self,
        model: str = "gpt-4o-mini",
        base_url: str = "http://127.0.0.1:8000/v1",
        api_key: str = "",
    ):
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    def _headers(self) -> Dict[str, str]:
        h = {"Content-Type": "application/json"}
        if self.api_key:
            h["Authorization"] = f"Bearer {self.api_key}"
        return h

    def health_check(self) -> Dict[str, Any]:
        try:
            import httpx

            r = httpx.get(f"{self.base_url}/models", headers=self._headers(), timeout=5.0)
            return {"ok": r.status_code < 500, "provider": "openai", "status": r.status_code}
        except Exception as e:
            return {"ok": False, "provider": "openai", "error": str(e)}

    def info(self) -> ModelInfo:
        return ModelInfo(
            name=self.model,
            provider="openai",
            supports_stream=True,
            supports_tools=True,
            context_length=128000,
            metadata={"base_url": self.base_url},
        )

    def generate(self, request: GenerateRequest) -> GenerateResult:
        try:
            import httpx

            messages: List[Dict[str, str]] = list(request.messages or [])
            if not messages and request.prompt:
                messages = [{"role": "user", "content": request.prompt}]
            payload = {
                "model": self.model,
                "messages": messages,
                "max_tokens": request.max_tokens,
                "temperature": request.temperature,
                "stream": False,
            }
            r = httpx.post(
                f"{self.base_url}/chat/completions",
                headers=self._headers(),
                json=payload,
                timeout=120.0,
            )
            if r.status_code != 200:
                return GenerateResult(
                    text="",
                    ok=False,
                    error=f"OpenAI-compatible HTTP {r.status_code}: {r.text[:300]}",
                    provider="openai",
                    model=self.model,
                )
            data = r.json()
            text = data["choices"][0]["message"]["content"]
            usage = data.get("usage") or {}
            return GenerateResult(
                text=text or "",
                ok=True,
                provider="openai",
                model=self.model,
                usage={k: int(v) for k, v in usage.items() if isinstance(v, (int, float))},
                raw=data,
            )
        except Exception as e:
            return GenerateResult(text="", ok=False, error=str(e), provider="openai", model=self.model)
