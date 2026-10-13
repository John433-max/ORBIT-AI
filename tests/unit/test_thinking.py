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


def test_classify_add_and():
    thinker = Thinker({})
    assert thinker.classify("add 12 and 7") == "calc"
    assert thinker.classify("add 3 to 10") == "calc"
    assert thinker.classify("write a function that adds two numbers") == "code"


def test_binary_search_function_is_code_not_web():
    t = Thinker({})
    assert t.classify("write a python function that implements binary search") == "code"
    assert t.classify("implement binary search on a sorted list") == "code"
    assert t.classify("search for recent news about fusion energy") == "search"
    assert t.classify("find recent papers on fusion energy") == "search"
    assert t.classify("find latest news on tokamak reactors") == "search"
    assert t.classify("papers about stellarator design") == "search"
    assert t.classify("what is your name") == "chat"


def test_gradient_descent_question_is_lab_title_is_code():
    """Conceptual ML asks stay on the scratch lab; implementation titles synthesize."""
    t = Thinker({})
    assert t.classify("what is gradient descent") == "lab"
    assert t.classify("explain backpropagation") == "lab"
    assert t.classify("what is overfitting") == "lab"
    assert t.classify("1d gradient descent minimize function") == "code"
    assert t.classify("momentum gradient descent") == "code"
    assert t.classify("gradient descent minimize quadratic") == "code"
    assert t.classify("write a python function for gradient descent") == "code"
    assert t.classify("linear regression least squares slope intercept") == "code"


def test_activation_functions_route_to_lab_not_relu_template():
    t = Thinker({})
    assert t.classify("activation functions relu sigmoid") == "lab"
    assert t.classify("explain activation function relu") == "lab"
    assert t.classify("write a function that implements relu") == "code"
    assert t.classify("implement leetcode 1290") == "code"


def test_code_verb_factorial_is_code_not_search():
    """Cycle 565: 'code a factorial function' must synthesize, not search."""
    from thinking import Thinker, _is_code
    from agents import _wants_code_written

    assert _is_code("code a factorial function")
    assert _is_code("code factorial")
    assert _wants_code_written("code a factorial function")
    assert _wants_code_written("code factorial")
    assert not _wants_code_written("factorial of 5")

    calls = []

    def code_runner(request, context):
        calls.append(request)
        return {"ok": True, "content": "def factorial(n):\n    return 1\n\nVerified"}

    def search_runner(request, context):
        calls.append("search:" + request)
        return {"ok": True, "content": "Here's what I found: factorial wikipedia"}

    t = Thinker({"code": code_runner, "search": search_runner, "calc": search_runner})
    result = t.think("code a factorial function")
    assert "def factorial" in result.answer
    assert "Here's what I found" not in result.answer
    assert any(c == "code a factorial function" for c in calls)
    assert not any(str(c).startswith("search:") for c in calls)


def test_classify_runtime_status_is_chat():
    """Bare status/doctor asks stay on chat, not research."""
    t = Thinker({})
    assert t.classify("status") == "chat"
    assert t.classify("system status") == "chat"
    assert t.classify("runtime status") == "chat"
    assert t.classify("doctor") == "chat"
    assert t.classify("orbit status") == "chat"
