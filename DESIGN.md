# Historical design notes — large-model research vision (NOT current product identity)

> **Status:** HISTORICAL / RESEARCH. This document captures early design thinking
> about large-scale training. **ORBIT AI today is a modular local AI agent runtime**
> (agents, tools, RAG, memory, ModelProvider backends). It is **not** a 100B model
> and does not claim those capabilities.

## 0. What this document is and isn't

This is a design document plus a real, tested, small prototype (`autograd.py`,
`model.py`, `tokenizer.py`, `train.py`, `generate.py`). Every gradient in the
autograd engine is checked numerically; the training loop reduces loss and
checkpoints correctly.

It is **not** a completed 100B model or a claim that experimental ideas are
proven at scale.

## 1. Architecture research summary

| Technique | Decision |
|---|---|
| Decoder-only Transformer | **Adopt** |
| GQA | **Adopt** (KV-cache memory) |
| RoPE | **Adopt** |
| SwiGLU | **Adopt** |
| RMSNorm | **Adopt** |
| QK-Norm | Optional (implemented in TinyLM) |
| MoE | Research candidate only |

## 2. Current product identity

ORBIT is a **CPU-first local agent runtime**:

- ModelProvider backends (TinyLM, Ollama, OpenAI-compatible, GGUF stub)
- ToolRegistry with permission levels
- Agents + Orchestrator routing
- RAG / DocumentStore / MemoryStore
- FastAPI + optional Web UI

See `README.md`, `docs/ARCHITECTURE.md`, and `UNIFIED.md`.

## 3. Full design notes

The complete historical DESIGN.md (~36 KB, parameter budgets, MoE math, training
notes) is in `ORBIT-AI-github-ready.zip` → `ORBIT-AI-pack/DESIGN.md`.
