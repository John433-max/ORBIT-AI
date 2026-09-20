# ORBIT Architecture

**Product identity:** ORBIT AI is a modular **local AI agent runtime** (API, agents, tools, memory, RAG, ModelProvider backends). It is **not** a fixed-size foundation model and does not ship 100B parameters.

```
User → CLI / API / UI → Orchestrator / OrbitAI → Agents → Tools → Memory / RAG → ModelProvider
```

Primary code: `api.py`, `agents.py`, `orbit_ai.py`, `tools/`, `documents.py`, `memory_store.py`, `orbit/models/`, `run_orbit.py`.

---

## Educational model lab (TinyLM)

Separately, the repo includes an educational decoder-only transformer lab under `tinylm/` and related modules for studying architecture choices (RoPE, GQA, SwiGLU, KV cache, quant experiments).

### Two lab implementations

### A. Educational implementation (NumPy + custom autograd)

- **Location:** `model_numpy_legacy.py` / `model/` helpers, `autograd.py`
- **Purpose:** Transparent numerics and learning

### B. Practical implementation (PyTorch)

- **Location:** `model_torch.py`, `tinylm/torch_model.py`
- **Purpose:** Training / throughput experiments when Torch is installed

Shared conceptual stack for the lab models:

```
Token Embeddings (often tied with LM head)
        │
        ▼
   Transformer Blocks × N
   (RMSNorm → causal attention + RoPE → residual → RMSNorm → MLP → residual)
        │
        ▼
   Final norm → LM head
```

These lab models are **toy-scale** relative to production chat models. Attach stronger generation via Ollama, OpenAI-compatible APIs, or optional GGUF providers.

## Configuration

Runtime and provider settings: `.env.example`, `orbit/core/config.py`, YAML under `configs/`.

See the root [README.md](../README.md) for the documentation of record.
