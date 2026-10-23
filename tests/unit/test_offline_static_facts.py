"""Offline static geography facts must answer, news must stay honest."""

from agents import Orchestrator, _offline_static_fact


def test_offline_static_fact_capitals():
    assert "Paris" in _offline_static_fact("what is the capital of France")
    assert "Tokyo" in _offline_static_fact("capital of Japan")
    assert "Berlin" in _offline_static_fact("capital of Germany")
    assert "London" in _offline_static_fact("capital of the UK")
    assert "Ottawa" in _offline_static_fact("what is the capital of Canada")


def test_offline_static_fact_skips_news_and_prices():
    assert _offline_static_fact("search for recent news about fusion energy") is None
    assert _offline_static_fact("latest news capital of France") is None
    assert _offline_static_fact("what is the price of the capital of Japan") is None
    assert _offline_static_fact("who is the president of France") is None


def test_handle_returns_labeled_offline_fact():
    orch = Orchestrator()
    for prompt, city in (
        ("what is the capital of France", "Paris"),
        ("capital of Japan", "Tokyo"),
        ("what is the capital of Germany", "Berlin"),
    ):
        out = orch.handle(prompt)
        body = out.get("content") or ""
        assert city in body, body
        assert "offline known fact" in body.lower(), body
        assert "toy-scale" not in body.lower()


def test_news_still_honest_no_live_web():
    orch = Orchestrator()
    out = orch.handle("search for recent news about fusion energy")
    assert out.get("agent") == "research_agent"
    body = (out.get("content") or "").lower()
    assert "no live web" in body
    assert "paris" not in body
