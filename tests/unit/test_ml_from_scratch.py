"""Regression tests for educational ML-from-scratch demos."""

from __future__ import annotations

from examples.ml_from_scratch import DEMOS, run_all, summary


def test_all_demos_ok():
    rows = run_all()
    assert len(rows) == len(DEMOS)
    for r in rows:
        assert r.get("ok") is True, r


def test_summary():
    s = summary()
    assert s["ok"] is True
    assert s["n"] >= 6


def test_one_neuron_separates():
    from examples.ml_from_scratch.one_neuron import run

    out = run()
    assert out["ok"]
    assert out["preds"] == [0, 0, 0, 0, 1, 1, 1, 1]


def test_xor_three_neurons():
    from examples.ml_from_scratch.three_neurons import run

    out = run()
    assert out["ok"]
    assert out["metric"].startswith("4/4")


def test_gradient_descent_converges():
    from examples.ml_from_scratch.gradient_descent import run

    out = run()
    assert out["ok"]
    assert out["loss"] < 0.1


def test_next_token_learns():
    from examples.ml_from_scratch.next_token import run

    out = run()
    assert out["ok"]
    assert out["top_after_the"]
