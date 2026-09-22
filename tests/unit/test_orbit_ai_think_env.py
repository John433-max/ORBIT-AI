"""Cycle 94: ORBIT_THINK env controls OrbitAI.use_thinking."""
import os
from orbit_ai import OrbitAI, _env_bool


def test_env_bool():
    os.environ["ORBIT_THINK_TEST"] = "1"
    assert _env_bool("ORBIT_THINK_TEST", False) is True
    os.environ["ORBIT_THINK_TEST"] = "0"
    assert _env_bool("ORBIT_THINK_TEST", True) is False
    os.environ.pop("ORBIT_THINK_TEST", None)
    assert _env_bool("ORBIT_THINK_TEST", True) is True


def test_use_thinking_from_env(monkeypatch):
    monkeypatch.setenv("ORBIT_THINK", "0")
    ai = OrbitAI(load_model=False, persist=False, use_thinking=None)
    assert ai.use_thinking is False
    monkeypatch.setenv("ORBIT_THINK", "1")
    ai2 = OrbitAI(load_model=False, persist=False, use_thinking=None)
    assert ai2.use_thinking is True
    # explicit kwarg wins
    ai3 = OrbitAI(load_model=False, persist=False, use_thinking=False)
    assert ai3.use_thinking is False


def test_status_includes_provider_and_1m():
    ai = OrbitAI(load_model=False, persist=False)
    st = ai.status()
    assert "use_thinking" in st
    assert "tinylm_1m_params" in st
    if st["tinylm_1m_params"] is not None:
        assert 1_000_000 <= st["tinylm_1m_params"] <= 1_300_000
