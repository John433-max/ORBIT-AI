"""Calculator unit tests."""
from calculator import calculate, parse_and_calculate, looks_like_math


def test_basic_ops():
    assert calculate("2+3")["result"] == 5
    assert calculate("10*5")["result"] == 50
    assert calculate("100/4")["result"] == 25


def test_div_zero():
    r = calculate("1/0")
    assert r["ok"] is False


def test_word_ops():
    r = parse_and_calculate("12 times 5")
    assert r["ok"] and r["result"] == 60


def test_looks_like_math():
    assert looks_like_math("what is 3+4")
