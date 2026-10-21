"""Cycle 460: algorithm 'search' must not steal code-write routes."""

from agents import Orchestrator


def test_binary_search_routes_to_code_not_research():
    orch = Orchestrator()
    assert orch.route("write a python function that implements binary search") == "code"
    assert orch.route("implement binary search on a sorted list") == "code"
    assert orch.route("search for recent news about fusion energy") == "research"
    assert orch.route("what is your name") == "chat"
    code = orch.handle("implement binary search on a sorted list")
    assert code["agent"] == "coding_agent"
    assert "def binary_search" in code["content"]
    assert "Verified" in code["content"]
    web = orch.handle("search for recent news about fusion energy")
    assert web["agent"] == "research_agent"
    assert "Here's what I found" in web["content"] or "live web" in web["content"].lower() or "fusion" in web["content"].lower()



def test_recover_bst_title_routes_to_code():
    """Cycle 547: bare 'recover binary search tree' is a template, not web search."""
    orch = Orchestrator()
    assert orch.route("recover binary search tree") == "code"
    result = orch.handle("recover binary search tree")
    assert result["agent"] == "coding_agent"
    assert "def recover_bst" in result["content"]
    assert "Verified" in result["content"]
    assert "NotImplementedError" not in result["content"]


def test_look_this_up_and_google_route_to_research():
    """Priority-2: phrasing variants must hit ResearchAgent, not chat hedge."""
    orch = Orchestrator()
    for prompt in (
        "look this up: quantum computing breakthrough",
        "look that up",
        "look it up please",
        "google fusion energy",
        "web search fusion energy",
        "search the web for fusion",
    ):
        assert orch.route(prompt) == "research", prompt
        result = orch.handle(prompt)
        assert result["agent"] == "research_agent", prompt
        low = (result["content"] or "").lower()
        assert "toy-scale" not in low
        assert any(
            phrase in low
            for phrase in ("no live web", "can't complete this search", "here's what i found", "sources:")
        ), result["content"]
    # Must not steal code or identity.
    assert orch.route("write a python function that adds two numbers") == "code"
    assert orch.route("what is your name") == "chat"


def test_document_inventory_phrases_route_to_document():
    """Possessive / show / which inventory asks hit DocumentAgent, not chat."""
    orch = Orchestrator()
    for q in (
        "list my documents",
        "list the documents",
        "list uploaded documents",
        "show me my documents",
        "show my documents",
        "which documents are loaded",
        "which documents do you have",
        "what documents do you have",
    ):
        assert orch._route(q) == "document", q
        out = orch.handle(q)
        assert out.get("agent") == "document", q
        assert "no documents loaded" in (out.get("content") or "").lower(), q


def test_implement_article_phrase_routes_to_code_not_hedge():
    """Priority-1: 'implement a ...' must hit CodeAgent, not the chat hedge."""
    from agents import _wants_code_written, Orchestrator

    assert _wants_code_written("implement a simple calculator")
    assert _wants_code_written("write a simple calculator")
    assert _wants_code_written("write a web scraper")
    assert not _wants_code_written("write about fusion energy")
    assert not _wants_code_written("write a blog post about AI")
    assert not _wants_code_written("write a story")

    orch = Orchestrator()
    assert orch.route("implement a simple calculator") == "code"
    assert orch.route("write about fusion energy") == "chat"
    out = orch.handle("implement a simple calculator")
    assert out["agent"] == "coding_agent"
    assert "def calculate" in out["content"]
    assert "toy-scale" not in out["content"].lower()
    assert "I'm ORBIT" not in out["content"]
