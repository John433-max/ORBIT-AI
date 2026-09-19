"""CI-safe unit tests (no agents.py required)."""
from orbit.models.echo import EchoProvider
from orbit.models.base import GenerateRequest


def test_echo_health():
    p = EchoProvider()
    assert p.health_check()["ok"] is True


def test_echo_generate():
    p = EchoProvider()
    r = p.generate(GenerateRequest(prompt="hello"))
    assert r.ok and "hello" in r.text


def test_echo_messages():
    p = EchoProvider()
    r = p.generate(GenerateRequest(messages=[{"role": "user", "content": "ping"}]))
    assert "ping" in r.text
