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


def test_percent_of_word():
    r = parse_and_calculate("what is 15 percent of 80")
    assert r["ok"] and r["result"] == 12.0
    r = parse_and_calculate("15 percent of 80")
    assert r["ok"] and r["result"] == 12.0
    r = parse_and_calculate("20 percentage of 50")
    assert r["ok"] and r["result"] == 10.0


def test_percent_of_symbol():
    r = parse_and_calculate("what is 15% of 80")
    assert r["ok"] and r["result"] == 12.0
    r = parse_and_calculate("15% of 80")
    assert r["ok"] and r["result"] == 12.0


def test_add_and_sum():
    r = parse_and_calculate("add 12 and 7")
    assert r["ok"] and r["result"] == 19
    r = parse_and_calculate("sum 3 and 4")
    assert r["ok"] and r["result"] == 7


def test_half_of():
    r = parse_and_calculate("half of 10")
    assert r["ok"] and r["result"] == 5.0


def test_looks_like_math():
    assert looks_like_math("what is 3+4")
    assert looks_like_math("15 percent of 80")
    assert looks_like_math("add 12 and 7")
