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
