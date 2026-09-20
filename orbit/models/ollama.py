"""Ollama HTTP adapter (optional — requires local Ollama)."""

from __future__ import annotations

from typing import Any, Dict

from orbit.models.base import GenerateRequest, GenerateResult, ModelInfo, ModelProvider


class OllamaProvider(ModelProvider):
    name = "ollama"

    def __init__(self, model: str = "llama3.2", base_url: str = "http://127.0.0.1:11434"):
        self.model = model
        self.base_url = base_url.rstrip("/")

    def health_check(self) -> Dict[str, Any]:
        try:
            import httpx

            r = httpx.get(f"{self.base_url}/api/tags", timeout=3.0)
            if r.status_code != 200:
                return {"ok": False, "provider": "ollama", "error": f"HTTP {r.status_code}"}
            tags = r.json().get("models") or []
            names = [m.get("name") for m in tags]
            return {"ok": True, "provider": "ollama", "models": names, "selected": self.model}
        except Exception as e:
            return {"ok": False, "provider": "ollama", "error": str(e)}

    def info(self) -> ModelInfo:
        return ModelInfo(
            name=self.model,
            provider="ollama",
            supports_stream=True,
            supports_tools=False,
            context_length=8192,
            metadata={"base_url": self.base_url},
        )

    def generate(self, request: GenerateRequest) -> GenerateResult:
        try:
            import httpx

            if request.messages:
                payload = {
                    "model": self.model,
                    "messages": request.messages,
                    "stream": False,
                    "options": {
                        "temperature": request.temperature,
                        "num_predict": request.max_tokens,
                    },
                }
                url = f"{self.base_url}/api/chat"
            else:
                payload = {
                    "model": self.model,
                    "prompt": request.prompt,
                    "stream": False,
                    "options": {
                        "temperature": request.temperature,
                        "num_predict": request.max_tokens,
                    },
                }
                url = f"{self.base_url}/api/generate"
            r = httpx.post(url, json=payload, timeout=120.0)
            if r.status_code != 200:
                return GenerateResult(
                    text="",
                    ok=False,
                    error=f"Ollama HTTP {r.status_code}: {r.text[:200]}",
                    provider="ollama",
                    model=self.model,
                )
            data = r.json()
            text = data.get("message", {}).get("content") or data.get("response") or ""
            return GenerateResult(text=text, ok=True, provider="ollama", model=self.model, raw=data)
        except Exception as e:
            return GenerateResult(text="", ok=False, error=str(e), provider="ollama", model=self.model)
