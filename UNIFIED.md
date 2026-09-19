# ORBIT as one AI

Everything lives under `artifacts/orbit/` and is reachable through one surface.

## One process

```bash
cd artifacts/orbit
pip install -r requirements.txt
python run_orbit.py
# → http://127.0.0.1:8000/   Web chat UI
# → /docs                     OpenAPI
# → /health                   unified status
```

## One Python facade

```bash
python orbit_ai.py                         # status JSON
python orbit_ai.py "what is your name"     # chat / agents
python orbit_ai.py "calculate 12*8"
python orbit_ai.py "benchmark the model gqa"
```

## What is connected

| Layer | Module | Role |
|-------|--------|------|
| Chat + agents | `agents.Orchestrator` | Routes to code, research, document, finance, **lab**, chat, … |
| Neural LM | `model.TinyLM` + BPE + `checkpoint_*.npz` | Generation / persona fallback |
| Educational lab | `tinylm/` | RoPE/GQA/SwiGLU/INT4 experiments (LabAgent) |
| Documents | `documents.DocumentStore` | TXT/MD/CSV/JSON (+ PDF/DOCX if installed) |
| API | `api.py` | OpenAI-compatible `/v1/chat/completions` |
| Web UI | `webui/index.html` | Browser chat |
| Memory | `memory_store` / SQLite | Long-term notes |

## Honest limits

- The trained checkpoint is **toy-scale** — retrieval + tools carry most useful answers.
- PDF/DOCX need optional `pypdf` / `python-docx`.
- TinyLM lab does **not** share the BPE vocab with the product LM (research submodule).
