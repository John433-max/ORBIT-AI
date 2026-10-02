"""Ollama HTTP adapter (optional — requires a local Ollama daemon).

httpx is preferred when installed. The stdlib urllib path keeps auto-routing
able to prefer a healthy Ollama even in checkouts that did not pip-install
the API extras.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any, Dict, Optional, Tuple

from orbit.models.base import GenerateRequest, GenerateResult, ModelInfo, ModelProvider


def _http_json(
    method: str,
    url: str,
    payload: Optional[dict] = None,
    timeout: float = 3.0,
) -> Tuple[int, str, Any]:
    """GET/POST JSON. Prefer httpx; fall back to urllib so missing extras are not fatal."""
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    try:
        import httpx

        if method == "GET":
            r = httpx.get(url, timeout=timeout)
        else:
            r = httpx.post(url, json=payload, timeout=timeout)
        text = r.text or ""
        try:
            data = r.json() if text else {}
        except Exception:
            data = {}
        return int(r.status_code), text, data
    except ImportError:
        pass

    req = urllib.request.Request(
        url,
        data=body,
        method=method,
        headers={"Content-Type": "application/json", "Accept": "application/json"} if body else {"Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            try:
                data = json.loads(raw) if raw else {}
            except json.JSONDecodeError:
                data = {}
            return int(resp.status), raw, data
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        return int(e.code), raw, {}


class OllamaProvider(ModelProvider):
    name = "ollama"

    def __init__(self, model: str = "llama3.2", base_url: str = "http://127.0.0.1:11434"):
        self.model = model
        self.base_url = base_url.rstrip("/")

    def health_check(self) -> Dict[str, Any]:
        try:
            status, _text, data = _http_json("GET", f"{self.base_url}/api/tags", timeout=3.0)
            if status != 200:
                return {"ok": False, "provider": "ollama", "error": f"HTTP {status}"}
            tags = (data or {}).get("models") or []
            names = [m.get("name") for m in tags if isinstance(m, dict)]
            return {
                "ok": True,
                "provider": "ollama",
                "models": names,
                "selected": self.model,
                "transport": "httpx" if _httpx_available() else "urllib",
            }
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
            status, text, data = _http_json("POST", url, payload, timeout=120.0)
            if status != 200:
                return GenerateResult(
                    text="",
                    ok=False,
                    error=f"Ollama HTTP {status}: {text[:200]}",
                    provider="ollama",
                    model=self.model,
                )
            out = ""
            if isinstance(data, dict):
                out = (data.get("message") or {}).get("content") or data.get("response") or ""
            return GenerateResult(text=out, ok=True, provider="ollama", model=self.model, raw=data)
        except Exception as e:
            return GenerateResult(text="", ok=False, error=str(e), provider="ollama", model=self.model)


def _httpx_available() -> bool:
    try:
        import httpx  # noqa: F401

        return True
    except ImportError:
        return False
