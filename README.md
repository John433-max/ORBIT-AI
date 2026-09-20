# ORBIT AI

**ORBIT AI** is a modular **local AI agent runtime**: it connects language models (or educational toy models) to tools, memory, document retrieval, research helpers, math/science solvers, and an HTTP API with a browser chat UI.

It is **model-agnostic**. ORBIT is not itself a large language model and does **not** contain 100-billion-parameter weights. Useful answers usually come from tools, retrieval, and structured solvers, plus whatever **ModelProvider** you configure (TinyLM, Ollama, OpenAI-compatible HTTP, optional GGUF via `llama-cpp-python`, or a resilient failover chain).

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![GitHub](https://img.shields.io/badge/GitHub-John433--max%2FORBIT--AI-181717?logo=github)](https://github.com/John433-max/ORBIT-AI)

---

## Status

ORBIT is under **active development**. The repository is a working prototype with tests, not a finished production product.

- Core routing, tools, API, and educational TinyLM paths are implemented and exercised by unit tests.
- Some surfaces (full MCP server, security-grade sandbox, learned embeddings) are incomplete or best-effort.
- Do not treat experimental paths as production-ready.

---

## Architecture

What exists in this repository:

```
User
  ↓
CLI (run_orbit.py)  /  FastAPI (api.py)  /  Web UI (webui/)
  ↓
ORBIT Runtime (orbit_ai.OrbitAI · agents.Orchestrator · thinking.Thinker)
  ↓
Agents (code, research, calc, document, memory, lab, …)
  ↓
ToolRegistry (tools/)  ·  permissions  ·  metrics
  ↓
Memory (VectorStore / SQLite)  ·  RAG (DocumentStore, hash embeddings)
  ↓
ModelProvider (orbit/models/) — tinylm | ollama | openai | gguf* | echo | resilient
```

\* GGUF works only if `llama-cpp-python` is installed and a `.gguf` path is configured.

| Layer | Location | Role |
|-------|----------|------|
| Facade | `orbit_ai.py` | `ask`, documents, lab helpers, status |
| Orchestrator | `agents.py` | Route → agent → verify → naturalize |
| Thinking | `thinking.py` | Multi-step plan / tool use helper |
| Tools | `tools/` | Calculator, web, memory, documents, python, … |
| Legacy helpers | `tools_legacy.py` | `python_sandbox`, file read, mock search |
| Documents | `documents.py` | Load, chunk, hash-embed search, extract |
| Memory | `memory_store.py` | In-memory or SQLite vector store |
| Providers | `orbit/models/` | ModelProvider interface + adapters |
| TinyLM lab | `tinylm/` | Educational NumPy/Torch decoder experiments |
| API | `api.py`, `api_routes/` | OpenAI-style + `/v2/*` routes |
| UI | `webui/index.html` | Browser chat against the API |
| CLI | `run_orbit.py` | `serve`, `doctor`, `status`, `chat` |

---

## Features

### Implemented (verified in source)

- **Orchestrator + agents** — confidence routing; verifier; naturalized tool output
- **ToolRegistry** — permission levels (`SAFE` … `PRIVILEGED`), call metrics
- **Calculator / science_math** — AST arithmetic; sympy calculus when installed; units / geometry / physics helpers
- **Document RAG** — TXT/MD/CSV/JSON; optional PDF/DOCX/PPTX; chunking; **hash embeddings**; extractive helpers
- **Memory** — `VectorStore` / `SQLiteVectorStore` (hash embed)
- **Web search tools** — DuckDuckGo + stub/mock fallbacks
- **Python execution** — best-effort restricted `exec` (**not** a security-grade sandbox)
- **Model providers** — `tinylm`, `ollama`, `openai`, `echo`, `resilient`, optional `gguf`
- **TinyLM** — educational decoder lab (not frontier chat quality)
- **HTTP API** + **Web UI** + **CLI** (`run_orbit.py`)

### Experimental

- Thinking-loop multi-step paths
- INT4 / quant experiments in `tinylm/`
- GGUF provider (optional dependency)
- MCP **adapter** only (not a full MCP server)
- Resilient provider failover/cache
- Persona retrieval + TinyLM generate fallbacks

### Planned / future

- Security-grade sandbox / containers
- Neural embeddings for RAG
- Richer autonomous coding (edit → test → patch)
- Full MCP client/server productization
- Larger models via providers (ORBIT does not ship 100B weights)

---

## Model support

| Provider | Status | Notes |
|----------|--------|--------|
| `tinylm` | Implemented | Educational local weights |
| `ollama` | Implemented | Local Ollama HTTP |
| `openai` | Implemented | OpenAI-compatible base URL + key |
| `echo` | Implemented | Test stub |
| `resilient` | Implemented | Failover + optional cache |
| `gguf` | Optional | Needs `llama-cpp-python` + file path |

Set `ORBIT_MODEL_PROVIDER` (see `.env.example`).

---

## Installation

**Python 3.10+** (developed on 3.12). CPU-only is fine.

```bash
git clone https://github.com/John433-max/ORBIT-AI.git
cd ORBIT-AI
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
# Optional: pip install -r requirements-torch.txt
```

Copy `.env.example` → `.env` as needed.

---

## Quick start

```bash
python run_orbit.py doctor
python run_orbit.py          # http://127.0.0.1:8000/
```

```python
from orbit_ai import OrbitAI
ai = OrbitAI()
print(ai.ask("12 * 5"))
print(ai.status())
```

```bash
python run_orbit.py chat "derivative of x^2"
```

---

## Configuration

| Variable | Purpose | Required |
|----------|---------|----------|
| `ORBIT_MODEL_PROVIDER` | `auto` / `tinylm` / `ollama` / `openai` / `gguf` / `resilient` / `echo` | Optional |
| `ORBIT_MODEL_NAME` | Model id or GGUF path | Optional |
| `ORBIT_MAX_TOKENS` | Generation cap | Optional |
| `ORBIT_TEMPERATURE` | Sampling temperature | Optional |
| `ORBIT_MAX_STEPS` / `ORBIT_MAX_TOOL_CALLS` | Agent budgets | Optional |
| `ORBIT_OPENAI_BASE_URL` / `ORBIT_OPENAI_API_KEY` | OpenAI-compatible backend | If using openai |
| `ORBIT_OLLAMA_BASE_URL` | Ollama host | Optional |
| `ORBIT_FAILOVER_PROVIDERS` | Resilient chain | Optional |
| `ORBIT_API_KEY` | Optional HTTP Bearer / X-API-Key gate | Optional |
| `ORBIT_RAG_ENABLED` / `ORBIT_MEMORY_ENABLED` / `ORBIT_WEB_ENABLED` | Feature flags | Optional |
| `ORBIT_TINYLM_*` | Lab presets / checkpoints | Optional |

---

## Running ORBIT

| Entry | Role |
|-------|------|
| `python run_orbit.py serve` | Uvicorn `api:app` |
| `python run_orbit.py doctor` | Dependency + provider checks |
| `python run_orbit.py status` | Status JSON |
| `python run_orbit.py chat "..."` | One-shot chat |
| `uvicorn api:app --port 8000` | Direct API |
| `orbit_ai.OrbitAI` | In-process facade |

---

## API

From `api.py` / `api_routes/` (also see `/docs` when running):

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/`, `/health`, `/healthz` | Probe / health |
| GET | `/ui` | Web UI |
| GET | `/v1/models` | Model list |
| POST | `/v1/chat/completions` | Chat |
| GET/POST/DELETE/PUT | `/v1/memory`… | Memory |
| POST/GET/DELETE | `/v1/documents`… | Documents |
| GET/DELETE | `/v1/conversations`… | Conversations |
| POST | `/v1/completions`, `/v1/embeddings` | Completions / embeddings |
| GET | `/v2/health` | v2 health |
| POST | `/v2/generate`, `/v2/embed` | Generate / embed |
| POST | `/v2/memory/search`, `/v2/rag/query` | Memory / RAG |
| POST | `/v2/agent/run`, `/v2/search` | Agent / search |
| GET | `/v2/tools` | List tools |

---

## Agent architecture

`Orchestrator.handle`: receive → score/route → run agent → verify → naturalize → metrics. Optional multi-intent secondary agent and research fallback. Full autonomous software-engineering loops are **not** implemented; coding is primarily sandbox execution.

---

## Tools

`ToolRegistry` with levels `SAFE` < `READ_ONLY` < `WRITE` < `NETWORK` < `EXECUTION` < `PRIVILEGED`. Tools under `tools/` (calculator, web, memory, documents, python, chat, lab, …). Selection is orchestrator/agent-driven, not a trained tool-calling LLM by default.

---

## Memory

Hash-embed `VectorStore` / `SQLiteVectorStore`; `ConversationStore` for API conversations; light session state in the orchestrator.

---

## RAG

Load → chunk → **hash-embed** search → extractive answer/summarize. Neural embedding models are **not** implemented.

---

## Research / coding / MCP

- **Research:** web search snippets (DDG or stubs), not multi-hop verified research.
- **Coding:** sandbox run of provided code, not autonomous edit–test–patch.
- **MCP:** adapter to wrap callables as tools; **not** a full MCP server.

---

## Security

Permission levels, path-bounded file reads, AST-limited python exec with timeouts.

**ORBIT does not currently provide a security-grade sandbox.** Do not expose the API to untrusted users without hardening. Keep secrets in `.env` (gitignored).

---

## Storage / generated files

Do not commit weights or DBs. See `.gitignore` for `*.npz`, `*.gguf`, `*.safetensors`, `*.pt`, `*.db`, `venv/`, etc.

---

## Testing

```bash
PYTHONPATH=. pytest tests/unit -q
```

---

## Documentation map

| File | Role |
|------|------|
| [SETUP.md](SETUP.md) | Platform install |
| [DESIGN.md](DESIGN.md) | **Historical** research notes — not product size claims |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Architecture notes |
| [SOURCE.md](SOURCE.md) | Source layout |

---

## License & honesty

Educational / research prototype. **ORBIT AI is a modular local agent runtime — not a 100B model.** Larger models can be integrated later through providers; they are not ORBIT’s default weights.
