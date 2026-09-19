"""ModelProvider unit tests."""
from orbit.models.base import GenerateRequest
from orbit.models.echo import EchoProvider
from orbit.models.router import build_provider
from orbit.core.config import OrbitConfig


def test_echo_generate():
    p = EchoProvider()
    r = p.generate(GenerateRequest(prompt="hello"))
    assert r.ok and "hello" in r.text


def test_build_echo():
    cfg = OrbitConfig(model_provider="echo")
    p = build_provider(cfg)
    assert p.name == "echo"


def test_tinylm_provider_optional():
    from orbit.models.tinylm_provider import TinyLMProvider

    p = TinyLMProvider(preset="rope")
    hc = p.health_check()
    if not hc.get("ok"):
        return
    r = p.generate(GenerateRequest(prompt="hi", max_tokens=8, temperature=0.0))
    assert r.provider == "tinylm"
