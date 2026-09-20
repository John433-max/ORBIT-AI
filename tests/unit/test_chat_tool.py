"""Unit tests for tools.chat_tool (no TinyLM / torch required)."""

from tools.chat_tool import ChatRetrieveTool, query_persona


class _HitStore:
    def query(self, q, k=3):
        return [
            {
                "score": 0.91,
                "text": "Q: who are you",
                "metadata": {"answer": "I am ORBIT."},
            }
        ]


def test_query_persona_empty_store():
    out = query_persona(None, "hello")
    assert out["ok"] is True
    assert out["matched"] is False
    assert out["hits"] == []


def test_query_persona_match():
    out = query_persona(_HitStore(), "who are you", threshold=0.42)
    assert out["matched"] is True
    assert out["answer"] == "I am ORBIT."


def test_retrieve_tool_requires_query():
    tool = ChatRetrieveTool(store=_HitStore())
    bad = tool.execute(query="")
    assert bad.ok is False
    good = tool.execute(query="who are you")
    assert good.ok is True
    assert "ORBIT" in good.content
