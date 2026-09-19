"""TinyLM adapter — wraps educational generate path without coupling agents to tinylm internals."""

from __future__ import annotations

from typing import Any, Dict, Optional

from orbit.models.base import GenerateRequest, GenerateResult, ModelInfo, ModelProvider


class TinyLMProvider(ModelProvider):
    name = "tinylm"

    def __init__(self, preset: str = "rope", ckpt_path: Optional[str] = None):
        self.preset = preset
        self.ckpt_path = ckpt_path
        self._model = None

    def _ensure(self):
        if self._model is not None:
            return self._model
        try:
            from tools.chat_tool import build_chat_tinylm
            self._model = build_chat_tinylm(self.preset, ckpt_path=self.ckpt_path)
        except Exception as e:
            raise RuntimeError(f"TinyLM unavailable: {e}") from e
        return self._model

    def health_check(self) -> Dict[str, Any]:
        try:
            m = self._ensure()
            src = getattr(m, "_weights_source", "unknown")
            return {"ok": True, "provider": "tinylm", "weights": src, "preset": self.preset}
        except Exception as e:
            return {"ok": False, "provider": "tinylm", "error": str(e)}

    def info(self) -> ModelInfo:
        meta: Dict[str, Any] = {"preset": self.preset}
        try:
            m = self._ensure()
            cfg = getattr(m, "config", None) or getattr(m, "cfg", None)
            if cfg is not None:
                meta["vocab_size"] = getattr(cfg, "vocab_size", None)
                meta["n_layer"] = getattr(cfg, "n_layer", None)
                meta["n_embd"] = getattr(cfg, "n_embd", None)
                meta["weights"] = getattr(m, "_weights_source", None)
        except Exception as e:
            meta["error"] = str(e)
        return ModelInfo(
            name=f"tinylm:{self.preset}",
            provider="tinylm",
            supports_stream=False,
            context_length=64,
            metadata=meta,
        )

    def generate(self, request: GenerateRequest) -> GenerateResult:
        try:
            from tools.chat_tool import generate_chat_tinylm
            prompt = request.prompt
            history = None
            if request.messages:
                history = [{"role": m.get("role", "user"), "content": m.get("content", "")} for m in request.messages[:-1]]
                prompt = request.messages[-1].get("content", "") or prompt
            model = self._ensure()
            out = generate_chat_tinylm(
                request=prompt, history=history, max_tokens=request.max_tokens,
                temperature=request.temperature, preset=self.preset, model=model,
                ckpt_path=self.ckpt_path,
            )
            if not out.get("ok", True) and out.get("error"):
                return GenerateResult(
                    text="", ok=False, error=str(out.get("error")),
                    provider="tinylm", model=f"tinylm:{self.preset}", raw=out,
                )
            return GenerateResult(
                text=str(out.get("text") or ""), ok=True, provider="tinylm",
                model=f"tinylm:{self.preset}",
                usage={"n_new": int(out.get("n_new") or 0)}, raw=out,
            )
        except Exception as e:
            return GenerateResult(text="", ok=False, error=str(e), provider="tinylm", model=f"tinylm:{self.preset}")
