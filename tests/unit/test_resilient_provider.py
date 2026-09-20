"""ResilientProvider failover + cache unit tests."""
from orbit.models.base import GenerateRequest, GenerateResult, ModelInfo, ModelProvider
from orbit.models.echo import EchoProvider
from orbit.models.resilient import ProviderSlot, ResilientProvider, build_failover_chain


class _FailThenOk(ModelProvider):
    name = "flaky"

    def __init__(self):
        self.n = 0

    def health_check(self):
        return {"ok": True, "provider": "flaky"}

    def info(self):
        return ModelInfo(name="flaky", provider="flaky")

    def generate(self, request):
        self.n += 1
        if self.n == 1:
            return GenerateResult(text="", ok=False, error="503 overloaded", provider="flaky")
        return GenerateResult(text=f"ok:{request.prompt}", ok=True, provider="flaky")


class _AlwaysFail(ModelProvider):
    name = "dead"

    def health_check(self):
        return {"ok": False, "provider": "dead"}

    def info(self):
        return ModelInfo(name="dead", provider="dead")

    def generate(self, request):
        return GenerateResult(text="", ok=False, error="timeout", provider="dead")


def test_failover_to_echo():
    p = ResilientProvider(
        [
            ProviderSlot(_AlwaysFail(), label="dead"),
            ProviderSlot(EchoProvider(), label="echo"),
        ]
    )
    r = p.generate(GenerateRequest(prompt="hello"))
    assert r.ok
    assert "hello" in r.text
    assert p.failover_count >= 1


def test_retry_same_flaky_backend():
    flaky = _FailThenOk()
    p = ResilientProvider([ProviderSlot(flaky, label="flaky")], max_attempts=3)
    r = p.generate(GenerateRequest(prompt="x"))
    assert r.ok and r.text == "ok:x"
    assert flaky.n == 2


def test_cache_hit():
    echo = EchoProvider()
    p = ResilientProvider([ProviderSlot(echo, label="echo")])
    a = p.generate(GenerateRequest(prompt="cached"))
    b = p.generate(GenerateRequest(prompt="cached"))
    assert a.text == b.text
    stats = p.cache.stats()
    assert stats["hits"] >= 1


def test_build_failover_chain_includes_echo():
    p = build_failover_chain()
    assert p.name == "resilient"
    hc = p.health_check()
    assert "backends" in hc
    labels = [s.label for s in p.slots]
    assert "echo" in labels
