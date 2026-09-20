# ORBIT AI — Modular Local AI Agent Runtime

**Open Research Build for Instruction-Tuned Transformers**

A modular local AI **agent runtime**: model providers, tool-using agents, document RAG, memory, science/math solvers, sandboxed execution, API, and browser chat UI — designed to be readable, testable, and honest about scale.

> **ORBIT is not a fixed model size.** TinyLM is an educational/experimental backend. Production answers come from tools, retrieval, solvers, and whatever **ModelProvider** you configure (Ollama, OpenAI-compatible, GGUF, TinyLM, or resilient failover).

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-pytest-brightgreen.svg)](#testing)
[![GitHub](https://img.shields.io/badge/GitHub-John433--max%2FORBIT--AI-181717?logo=github)](https://github.com/John433-max/ORBIT-AI)

---

## Highlights

| Capability | What you get |
|------------|----------------|
| **Unified facade** | One object (`OrbitAI`) and one process (`run_orbit.py`) for chat, tools, and lab |
| **Agents** | Code sandbox, research, memory, documents, calculator, finance, lab |
| **Thinking loop** | Classify → plan → tools → natural answer (not keyword-only routing) |
| **Science & math** | Arithmetic, calculus (sympy), geometry, physics, unit conversion |
| **TinyLM lab** | From-scratch NumPy/Torch transformer: RoPE, GQA, SwiGLU, KV cache, INT4 |
| **Web UI + API** | Chat at `/`, OpenAI-compatible `POST /v1/chat/completions` |
| **Documents** | TXT / MD / CSV / JSON (+ PDF / DOCX when optional deps are installed) |

> **Honest scope:** The neural weights are **toy-scale**. Useful answers come mainly from tools, retrieval, and structured solvers — not from pretending to be a frontier model.

---

## Quick start

```bash
# 1. Environment
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Launch (API + Web UI)
python run_orbit.py
# → http://127.0.0.1:8000/
```

### Python API

```python
from orbit_ai import OrbitAI

ai = OrbitAI()                          # thinking on by default
print(ai.ask("what is your name"))
print(ai.ask("12 * 5"))
print(ai.ask("derivative of x^2"))
print(ai.ask("100 km to m"))
print(ai.status())
```

### CLI

```bash
python orbit_ai.py                        # status JSON
python orbit_ai.py "what is your name"
python orbit_ai.py "area of a circle radius 5"
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│  Web UI  (/)     OpenAPI (/docs)     Health (/health)   │
├─────────────────────────────────────────────────────────┤
│  OrbitAI  ·  Orchestrator  ·  Thinker                   │
│  Agents: chat · research · memory · document · calc · … │
├─────────────────────────────────────────────────────────┤
│  Tools registry  ·  DocumentStore  ·  Memory (SQLite)   │
├──────────────────────┬──────────────────────────────────┤
│  ModelProvider       │  tinylm/ lab (NumPy + Torch)     │
│  ollama / openai /   │  RoPE · GQA · INT4 · KV cache    │
│  gguf / tinylm /     │                                  │
│  resilient           │                                  │
└──────────────────────┴──────────────────────────────────┘
```

| Layer | Location | Role |
|-------|----------|------|
| Facade | `orbit_ai.py` | Single entry for chat, docs, metrics, lab |
| Orchestrator | `agents.py` | Routing, multi-intent, natural output |
| Thinking | `thinking.py` | Plan → act → answer |
| Science/math | `science_math.py`, `calculator.py` | Closed-form + sympy |
| Documents | `documents.py` | Chunk, embed, extract, summarize |
| Model router | `orbit/models/` | Provider abstraction |
| Educational lab | `tinylm/` | Architecture experiments |
| API | `api.py` | FastAPI, streaming chat completions |
| UI | `webui/index.html` | Browser chat |

---

## Examples

```text
you:  what is your name
ORBIT: I'm ORBIT …

you:  15 * 7
ORBIT: 15 * 7 = 105

you:  derivative of sin(x)
ORBIT: d/dx(sin(x)) = cos(x)

you:  area of a circle radius 5
ORBIT: Area of circle (r=5.0) = 78.5398 (πr²)

you:  100 km to m
ORBIT: 100 km = 100000 m
```

---

## Configuration & platforms

- **Python:** 3.10+ (developed on 3.12)
- **OS:** Linux, macOS, Windows (WSL2 supported)
- **GPU:** Not required (NumPy CPU path)
- **Env:** see `.env.example` (`ORBIT_MODEL_PROVIDER`, `ORBIT_MODEL_NAME`, …)

Full platform notes: **[SETUP.md](SETUP.md)**

---

## Testing

```bash
PYTHONPATH=. pytest tests/unit -q
```

---

## Documentation

| Doc | Contents |
|------|----------|
| [SETUP.md](SETUP.md) | Install on Windows / macOS / Linux |
| [DESIGN.md](DESIGN.md) | Historical design notes (labeled) |
| [AUDIT/PHASE0_REPOSITORY_AUDIT.md](AUDIT/PHASE0_REPOSITORY_AUDIT.md) | Phase 0 audit |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | System architecture |
| [SOURCE.md](SOURCE.md) | Full source archive notes |

---

## License & credit

Educational prototype. See repository files for licensing details.

**ORBIT is a modular local AI agent runtime — not a 100B model.**
