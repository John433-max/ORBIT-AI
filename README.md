# ORBIT-AI

Unified educational LLM + agents platform.

## Quick start

```bash
pip install -r requirements.txt
python run_orbit.py
# open http://127.0.0.1:8000/
```

```bash
from orbit_ai import OrbitAI
ai = OrbitAI()
print(ai.ask("what is your name"))
```

See SETUP.md and UNIFIED.md for full docs.

## Features
- TinyLM (NumPy/Torch educational decoder-only Transformer)
- Agents: chat, research, memory, documents, calculator, code, lab
- Thinking loop, science/math (calculus, geometry, physics)
- Web UI + OpenAI-compatible API
- INT4 quantization, KV cache, RoPE, GQA, SwiGLU, SWA

## Note
Large `.npz` checkpoints are gitignored; train or download separately.
