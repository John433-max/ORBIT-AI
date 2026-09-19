"""GGUF / llama.cpp adapter (optional dependency: llama-cpp-python).

Install: pip install llama-cpp-python
Env:
  ORBIT_MODEL_PROVIDER=gguf
  ORBIT_MODEL_NAME=/path/to/model.gguf
  ORBIT_GGUF_N_CTX=2048
  ORBIT_GGUF_N_GPU_LAYERS=0   # CPU-first default
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, Optional

from orbit.models.base import GenerateRequest, GenerateResult, ModelInfo, ModelProvider


class GGUFProvider(ModelProvider):
    name = "gguf"

    def __init__(
        self,
        model_path: str = "",
        n_ctx: int = 2048,
        n_gpu_layers: int = 0,
        chat_format: Optional[str] = None,
    ):
        self.model_path = (model_path or os.environ.get("ORBIT_MODEL_NAME") or "").strip()
        self.n_ctx = int(os.environ.get("ORBIT_GGUF_N_CTX") or n_ctx)
        self.n_gpu_layers = int(os.environ.get("ORBIT_GGUF_N_GPU_LAYERS") or n_gpu_layers)
        self.chat_format = chat_format or os.environ.get("ORBIT_GGUF_CHAT_FORMAT") or None
        self._llm = None
        self._error: Optional[str] = None

    def _ensure(self):
        if self._llm is not None:
            return self._llm
        if not self.model_path or not Path(self.model_path).is_file():
            self._error = f"GGUF file not found: {self.model_path!r}"
            raise FileNotFoundError(self._error)
        try:
            from llama_cpp import Llama
        except ImportError as e:
            self._error = "llama-cpp-python not installed (pip install llama-cpp-python)"
            raise ImportError(self._error) from e
        kwargs: Dict[str, Any] = {
            "model_path": self.model_path,
            "n_ctx": self.n_ctx,
            "n_gpu_layers": self.n_gpu_layers,
            "verbose": False,
        }
        if self.chat_format:
            kwargs["chat_format"] = self.chat_format
        self._llm = Llama(**kwargs)
        return self._llm

    def health_check(self) -> Dict[str, Any]:
        try:
            self._ensure()
            return {
                "ok": True,
                "provider": "gguf",
                "model_path": self.model_path,
                "n_ctx": self.n_ctx,
                "n_gpu_layers": self.n_gpu_layers,
            }
        except Exception as e:
            return {"ok": False, "provider": "gguf", "error": str(e)}

    def info(self) -> ModelInfo:
        return ModelInfo(
            name=Path(self.model_path).name if self.model_path else "gguf",
            provider="gguf",
            supports_stream=False,
            supports_tools=False,
            context_length=self.n_ctx,
            metadata={
                "model_path": self.model_path,
                "n_gpu_layers": self.n_gpu_layers,
            },
        )

    def generate(self, request: GenerateRequest) -> GenerateResult:
        try:
            llm = self._ensure()
        except Exception as e:
            return GenerateResult(
                text="", ok=False, error=str(e), provider="gguf", model=self.model_path,
            )
        try:
            if request.messages:
                out = llm.create_chat_completion(
                    messages=request.messages,
                    max_tokens=request.max_tokens,
                    temperature=request.temperature,
                    stop=request.stop,
                )
                text = out["choices"][0]["message"]["content"] or ""
            else:
                out = llm(
                    request.prompt or "",
                    max_tokens=request.max_tokens,
                    temperature=request.temperature,
                    stop=request.stop or [],
                )
                text = out["choices"][0]["text"] if out.get("choices") else ""
            return GenerateResult(
                text=text, ok=True, provider="gguf",
                model=Path(self.model_path).name, raw=out,
            )
        except Exception as e:
            return GenerateResult(
                text="", ok=False, error=str(e), provider="gguf", model=self.model_path,
            )
