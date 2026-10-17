"""Eval scorer: AND contains, OR any, forbidden hedge phrases."""

from evals.runner import score_row


def test_expect_contains_and_forbidden():
    row = {"expect_contains": ["def "], "expect_not_contains": ["toy-scale"]}
    assert score_row(row, "def add(a, b):\n    return a + b")["ok"]
    bad = score_row(row, "toy-scale educational model")
    assert not bad["ok"]
    assert any(r.startswith("missing:") for r in bad["reasons"])
    assert any(r.startswith("forbidden:") for r in bad["reasons"])


def test_expect_any_live_or_honest_offline():
    row = {
        "expect_any": ["fusion", "don't have live web", "no live web"],
        "expect_not_contains": ["toy-scale"],
    }
    assert score_row(row, "Here's what I found: fusion industry news")["ok"]
    assert score_row(row, "I don't have live web access right now.")["ok"]
    hedge = score_row(row, "I am a toy-scale educational model.")
    assert not hedge["ok"]
    empty = score_row(row, "Sure, I can help with that.")
    assert not empty["ok"]
    assert empty["reasons"][0].startswith("missing_any:")


def test_normalize_string_expect_and_prompt_kind():
    from evals.runner import _normalize_row
    raw = {
        "id": "code_1922",
        "kind": "coding",
        "prompt": "implement bisection method root finding",
        "expect_contains": "bisection_root",
    }
    row = _normalize_row(raw)
    assert row["input"] == "implement bisection method root finding"
    assert row["category"] == "coding"
    assert row["expect_contains"] == ["bisection_root"]
    # Bare string must not be scored as characters (would false-pass).
    missing = score_row(row, "def other():\n    return 1")
    assert not missing["ok"]
    assert any("bisection_root" in r for r in missing["reasons"])
    present = score_row(row, "def bisection_root(f, a, b):\n    return a")
    assert present["ok"]
