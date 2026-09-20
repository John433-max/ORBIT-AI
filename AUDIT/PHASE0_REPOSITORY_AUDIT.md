# PHASE 0 — Repository audit notes

## Product identity

ORBIT AI is a **modular local AI agent runtime** (agents, tools, RAG, memory, ModelProvider backends).

It is **not** a shipped 100-billion-parameter model. Any discussion of large-scale training in `DESIGN.md` is **historical / research** only.

## Historical “100B” terminology

| Location | Treatment |
|----------|-----------|
| `DESIGN.md` | HISTORICAL — labeled at top; not product claims |
| Honesty tests (`test_agents.py`, `test_tools.py`) | **Kept** — they assert ORBIT is not a 100B model |
| README / SETUP | State runtime identity only |

## Implemented surfaces (summary)

- `agents.Orchestrator` + specialized agents
- `tools.ToolRegistry` + permission levels
- `documents.DocumentStore` (hash embeddings)
- `memory_store` vector/SQLite stores
- `orbit/models/*` providers (tinylm, ollama, openai, echo, resilient, optional gguf)
- FastAPI `api.py` + `api_routes/`
- `run_orbit.py` CLI
- Educational `tinylm/` lab

## Known limitations

- Python sandbox is best-effort, not security-grade isolation
- RAG uses hash embeddings, not neural embedders
- MCP is an adapter surface, not a full server product
- GGUF requires optional `llama-cpp-python`

See current [README.md](../README.md) for the documentation of record.
