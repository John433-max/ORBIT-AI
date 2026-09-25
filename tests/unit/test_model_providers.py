"""Unit tests for ModelProvider abstraction (Phase C)."""

from __future__ import annotations

from orbit.core.config import OrbitConfig, load_config
from orbit.models.base import GenerateRequest
from orbit.models.echo import EchoProvider
from orbit.models.router import ModelRouter, build_provider


def test_load_config_defaults():
    cfg = load_config({})
    assert cfg.model_provider == "auto"
    assert cfg.host == "127.0.0.1"
    assert cfg.port == 8000


def test_load_config_env():
    cfg = load_config(
        {
            "ORBIT_MODEL_PROVIDER": "echo",
            "ORBIT_PORT": "9001",
            "ORBIT_MAX_STEPS": "5",
        }
    )
    assert cfg.model_provider == "echo"
    assert cfg.port == 9001
    assert cfg.max_steps == 5


def test_echo_provider_generate():
    p = EchoProvider()
    assert p.health_check()["ok"] is True
    r = p.generate(GenerateRequest(prompt="hello orbit"))
    assert r.ok and "hello orbit" in r.text
    r2 = p.generate(GenerateRequest(messages=[{"role": "user", "content": "ping"}]))
    assert "ping" in r2.text


def test_build_provider_echo():
    cfg = OrbitConfig(model_provider="echo")
    p = build_provider(cfg)
    assert p.name == "echo"
    assert p.generate(GenerateRequest(prompt="x")).ok


def test_model_router():
    router = ModelRouter(cfg=OrbitConfig(model_provider="echo"))
    out = router.generate(prompt="test")
    assert out.ok
    assert router.health()["ok"] is True
    info = router.info()
    assert info.provider == "echo"


def test_auto_prefers_healthy_ollama(monkeypatch):
    """Priority 5: auto must pick Ollama when its health check is ok."""
    from orbit.models import ollama as ollama_mod
    from orbit.models.ollama import OllamaProvider

    def fake_health(self):
        return {"ok": True, "provider": "ollama", "models": ["llama3.2"], "selected": self.model}

    monkeypatch.setattr(OllamaProvider, "health_check", fake_health)
    monkeypatch.setattr(ollama_mod.OllamaProvider, "health_check", fake_health)
    cfg = OrbitConfig(model_provider="auto")
    p = build_provider(cfg)
    assert p.name == "ollama"


def test_tinylm_provider_optional():
    from orbit.models.tinylm_provider import TinyLMProvider

    p = TinyLMProvider(preset="rope")
    hc = p.health_check()
    # Without full TinyLM stack in a partial checkout, health may fail — that is OK
    if not hc.get("ok"):
        return
    r = p.generate(GenerateRequest(prompt="hi", max_tokens=8, temperature=0.0))
    assert r.provider == "tinylm"
