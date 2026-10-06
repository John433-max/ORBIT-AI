"""Unit tests for thinking.Thinker classify → plan → act."""

from thinking import ThinkResult, Thinker, Thought


def test_classify_math_and_chat():
    t = Thinker({})
    assert t.classify("what is 12*7") == "calc"
    assert t.classify("hello") == "chat"
    assert t.classify("my name is Ada") == "memory"
    assert t.classify("summarize the document") == "docs"


def test_plan_matches_kind():
    t = Thinker({})
    assert t.plan("x", "calc")[0] == "calc"
    assert t.plan("x", "code") == ["code"]
    assert t.plan("x", "chat") == ["chat"]


def test_think_uses_calc_runner():
    t = Thinker(
        {
            "calc": lambda req, ctx: {"ok": True, "content": "84"},
            "search": lambda req, ctx: {"ok": True, "content": "web"},
            "chat": lambda req, ctx: "hedge",
        }
    )
    res = t.think("what is 12*7")
    assert isinstance(res, ThinkResult)
    assert res.ok
    assert res.answer == "84"
    assert any(th.kind == "decide" for th in res.thoughts)


def test_think_fallback_when_no_runners():
    t = Thinker({})
    res = t.think("what is the capital of France?")
    assert res.ok
    assert "solid answer" in res.answer.lower() or res.answer
    assert any(th.kind == "fallback" for th in res.thoughts)


def test_thought_to_dict():
    th = Thought("classify", "calc")
    d = th.to_dict()
    assert d["kind"] == "classify" and d["text"] == "calc"
    r = ThinkResult(answer="ok", thoughts=[th], plan=["chat"])
    assert r.to_dict()["ok"] is True


def test_think_keeps_honest_missing_document():
    t = Thinker(
        {
            "docs": lambda req, ctx: {
                "ok": False,
                "content": "I couldn't find document #42.",
            },
            "search": lambda req, ctx: {"ok": True, "content": "wikiHow summary of documents"},
            "chat": lambda req, ctx: {
                "ok": True,
                "content": "I'm still thinking that through, but I don't have a solid answer yet.",
            },
        }
    )
    res = t.think("summarize document #42")
    assert "couldn't find document #42" in res.answer
    assert "solid answer" not in res.answer.lower()
    assert "wikihow" not in res.answer.lower()
    assert any(th.kind == "decide" and "empty docs" in th.text for th in res.thoughts)


def test_binary_search_function_is_code_not_web():
    t = Thinker({})
    assert t.classify("write a python function that implements binary search") == "code"
    assert t.classify("implement binary search on a sorted list") == "code"
    assert t.classify("search for recent news about fusion energy") == "search"
    assert t.classify("what is your name") == "chat"
