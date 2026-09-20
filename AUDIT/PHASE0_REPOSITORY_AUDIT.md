# Phase 0 — Repository Audit (2026-09-20)

## Source of truth
- **Local full tree:** project workspace `orbit/` (complete implementation)
- **GitHub:** `John433-max/ORBIT-AI` (partial publish; growing toward parity)
- README is **not** assumed correct until verified against code

## Architecture (actual)

| Layer | Location | Status |
|-------|----------|--------|
| CLI / launcher | `run_orbit.py` | WORKING — doctor, serve, chat, status |
| Facade | `orbit_ai.py` | WORKING |
| Orchestrator | `agents.py` | WORKING — rule-based routing + agents |
| Model providers | `orbit/models/*` | WORKING — base, echo, ollama, openai, tinylm, gguf, resilient, router |
| Config | `orbit/core/config.py` | WORKING — env-driven |
| State machine | `orbit/core/state.py` | WORKING — RunState enum + AgentRun |
| Tools | `tools/*` + `tools/base.py` | WORKING — ToolRegistry + permissions |
| API | `api.py` + `api_routes/*` | WORKING — FastAPI, SSE, OpenAI-compat |
| Web UI | `webui/index.html` | WORKING |
| Memory | `memory_store.py` | WORKING — hash-embed + SQLite |
| RAG/docs | `documents.py` | WORKING — extractive, not generative |
| TinyLM lab | `tinylm/*`, `model.py` | WORKING — educational toy-scale |

## 100B terminology
Product-facing strings cleaned. DESIGN.md labeled HISTORICAL. Tests that assert ORBIT is not a 100B model kept.

## Entry points
```bash
pip install -r requirements.txt
python run_orbit.py doctor
python run_orbit.py serve
```

## Principle
ORBIT is a modular local AI agent runtime — not defined by parameter count.
