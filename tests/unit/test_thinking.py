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
