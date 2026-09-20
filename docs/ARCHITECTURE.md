# ORBIT Architecture

```
User → Web UI / CLI / OrbitAI
         → Orchestrator (agents.py) + Thinker (thinking.py)
              → ToolRegistry (tools/base.py) + Agents
              → documents.py (RAG) · memory_store.py · science_math/calculator
              → chat.generate / TinyLM / ModelProvider (orbit/models/)
         → api.py (FastAPI OpenAI-compatible)
```

## Model providers

Agents depend on `ModelProvider`, not a hard-wired TinyLM import.
See `docs/MODEL_PROVIDERS.md`.

## Tool permissions

SAFE < READ_ONLY < WRITE < NETWORK < EXECUTION < PRIVILEGED

## Agent run limits

`orbit/core/state.py` — max_steps, max_tool_calls, timeout_s.

## Rules of the road

1. Preserve working code; incremental changes only.
2. Permission levels enforced in ToolRegistry, not model text.
3. Sandbox is host best-effort, not multi-tenant isolation.
4. Do not invent performance numbers or test results.
