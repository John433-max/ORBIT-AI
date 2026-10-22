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


def test_generic_coding_asks_return_real_code_not_miss():
    """Hello / scraper asks route to CodeAgent and return real source."""
    orch = Orchestrator()
    hello = orch.handle("make a script that prints hello")
    assert hello["agent"] == "coding_agent"
    assert "def hello" in hello["content"]
    assert "couldn't synthesize" not in hello["content"].lower()
    assert "I'm ORBIT" not in hello["content"]

    scrape = orch.handle("write a web scraper")
    assert scrape["agent"] == "coding_agent"
    assert "def scrape_text" in scrape["content"]
    assert "couldn't synthesize" not in scrape["content"].lower()

    # Prose stays off the code path; weak chat falls through to research.
    about = orch.handle("write about fusion energy")
    assert about["agent"] == "research_agent"


def test_build_scraper_and_class_return_real_code():
    """Priority-1: build-scraper and class asks route to CodeAgent with real source."""
    from agents import _wants_code_written, Orchestrator

    assert _wants_code_written("build a simple web scraper")
    assert _wants_code_written("create a class for a bank account")
    assert not _wants_code_written("write about fusion energy")

    orch = Orchestrator()
    scrape = orch.handle("build a simple web scraper")
    assert scrape["agent"] == "coding_agent"
    assert "def scrape_text" in scrape["content"]
    assert "couldn't synthesize" not in scrape["content"].lower()
    assert "I'm ORBIT" not in scrape["content"]

    klass = orch.handle("create a class for a bank account")
    assert klass["agent"] == "coding_agent"
    assert "class BankAccount" in klass["content"]
    assert "couldn't synthesize" not in klass["content"].lower()
    assert "I'm ORBIT" not in klass["content"]


def test_tell_me_about_routes_to_research_not_hedge():
    """Priority-2: 'tell me about X' is a knowledge ask, not the chat hedge."""
    orch = Orchestrator()
    assert orch.route("tell me about SPARC tokamak") == "research"
    out = orch.handle("tell me about SPARC tokamak")
    assert out["agent"] == "research_agent"
    low = (out.get("content") or "").lower()
    assert "how can i help" not in low
    assert "no live web" in low or "sparc" in low

    # Identity stays on chat, not research.
    assert orch.route("tell me about yourself") == "chat"
    ident = orch.handle("tell me about yourself")
    assert "ORBIT" in (ident.get("content") or "")
    assert "no live web" not in (ident.get("content") or "").lower()

    # Prose still routes to chat, but the hedge falls through to research
    # (honest offline note); agent label reflects research_agent.
    assert orch.route("write about fusion energy") == "chat"
    about = orch.handle("write about fusion energy")
    assert about["agent"] == "research_agent"
    about_low = (about.get("content") or "").lower()
    assert "how can i help" not in about_low
    assert "no live web" in about_low or "fusion" in about_low


def test_file_inventory_phrases_stay_sandbox_not_research():
    """Sandbox file listing must not weak-fall through to ResearchAgent."""
    from agents import Orchestrator, _looks_like_file_inventory, _looks_like_knowledge

    for q in (
        "list files",
        "what files are in the sandbox",
        "which files are available",
        "show me the files",
        "what's in the sandbox",
        "files in the workspace",
    ):
        assert _looks_like_file_inventory(q), q
        assert not _looks_like_knowledge(q), q

    orch = Orchestrator()
    for q in (
        "list files",
        "what files are in the sandbox",
        "which files are available",
        "show me the files",
        "what's in the sandbox",
    ):
        assert orch.route(q) == "chat", q
        out = orch.handle(q)
        assert out["agent"] == "main_chat_agent", q
        low = (out.get("content") or "").lower()
        assert "sandbox" in low or "files" in low, out.get("content")
        assert "no live web" not in low, out.get("content")
        assert "how can i help" not in low, out.get("content")


def test_offline_algorithm_explainer_returns_local_template():
    """Offline research: conceptual algorithm asks get a code_synth reference.

    News/lookup phrases must stay on the pure offline message (no template).
    """
    orch = Orchestrator()
    how = orch.handle("how does binary search work")
    assert how["agent"] == "research_agent"
    body = how.get("content") or ""
    assert "No live web" in body or "live web" in body.lower()
    assert "def binary_search" in body
    assert "Verified" in body
    assert how.get("raw", {}).get("edu_template") is True or "def binary_search" in body

    news = orch.handle("search for recent news about fusion energy")
    assert news["agent"] == "research_agent"
    nbody = news.get("content") or ""
    assert "def " not in nbody
    assert "live web" in nbody.lower() or "No live web" in nbody


def test_self_identity_orbit_name_not_research():
    """'what is ORBIT' / 'who is orbit' stay on chat identity, not web research."""
    orch = Orchestrator()
    assert orch.route("what is ORBIT") == "chat"
    assert orch.route("who is orbit") == "chat"
    assert orch.route("what is orbit AI") == "chat"
    assert orch.route("what is your name") == "chat"
    for q in ("what is ORBIT", "who is orbit", "what is orbit AI"):
        out = orch.handle(q)
        assert out["agent"] == "main_chat_agent"
        assert "ORBIT" in out["content"]
        assert "no live web" not in out["content"].lower()
        assert (out.get("raw") or {}).get("identity") is True
    # Astronomy must not be claimed as self-identity.
    astro = orch.handle("what is the orbit of the earth")
    assert (astro.get("raw") or {}).get("identity") is not True
