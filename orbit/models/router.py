"""Select a ModelProvider from config / environment."""

from __future__ import annotations

from typing import Optional

from orbit.core.config import OrbitConfig, load_config
from orbit.models.base import ModelProvider
from orbit.models.echo import EchoProvider
from orbit.models.ollama import OllamaProvider
from orbit.models.openai_compatible import OpenAICompatibleProvider
from orbit.models.tinylm_provider import TinyLMProvider
from orbit.models.gguf import GGUFProvider


def build_provider(cfg: Optional[OrbitConfig] = None) -> ModelProvider:
    cfg = cfg or load_config()
    kind = (cfg.model_provider or "auto").lower()

    if kind in ("resilient", "failover"):
        from orbit.models.resilient import build_failover_chain
        return build_failover_chain(cfg)

    if kind in ("echo", "test"):
        return EchoProvider()

    if kind == "ollama":
        name = cfg.model_name or "llama3.2"
        return OllamaProvider(model=name, base_url=cfg.ollama_base_url)

    if kind in ("openai", "openai_compatible", "remote"):
        name = cfg.model_name or "gpt-4o-mini"
        return OpenAICompatibleProvider(
            model=name,
            base_url=cfg.openai_base_url,
            api_key=cfg.openai_api_key,
        )

    if kind == "tinylm":
        return TinyLMProvider(preset=cfg.tinylm_preset, ckpt_path=cfg.tinylm_ckpt or None)

    if kind in ("gguf", "llama_cpp", "llamacpp"):
        return GGUFProvider(model_path=cfg.model_name)

    if kind == "auto":
        ollama = OllamaProvider(model=cfg.model_name or "llama3.2", base_url=cfg.ollama_base_url)
        if ollama.health_check().get("ok"):
            return ollama
        try:
            tinylm = TinyLMProvider(preset=cfg.tinylm_preset, ckpt_path=cfg.tinylm_ckpt or None)
            if tinylm.health_check().get("ok"):
                return tinylm
        except Exception:
            pass
        return EchoProvider()

    return EchoProvider()


class ModelRouter:
    def __init__(self, provider: Optional[ModelProvider] = None, cfg: Optional[OrbitConfig] = None):
        self.cfg = cfg or load_config()
        self.provider = provider or build_provider(self.cfg)

    def generate(self, **kwargs):
        from orbit.models.base import GenerateRequest
        if "request" in kwargs and hasattr(kwargs["request"], "prompt"):
            return self.provider.generate(kwargs["request"])
        request = GenerateRequest(
            prompt=kwargs.get("prompt", ""),
            messages=kwargs.get("messages") or [],
            max_tokens=int(kwargs.get("max_tokens") or self.cfg.max_tokens),
            temperature=float(kwargs.get("temperature") or self.cfg.temperature),
        )
        return self.provider.generate(request)

    def health(self):
        return self.provider.health_check()

    def info(self):
        return self.provider.info()


def get_default_provider(cfg: Optional[OrbitConfig] = None) -> ModelProvider:
    return build_provider(cfg)
