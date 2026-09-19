# ORBIT-AI

Unified educational LLM + agents platform.

**Repo:** https://github.com/John433-max/ORBIT-AI

## Quick start

```bash
pip install -r requirements.txt
python run_orbit.py
# open http://127.0.0.1:8000/
```

```python
from orbit_ai import OrbitAI
ai = OrbitAI()
print(ai.ask("what is your name"))
print(ai.ask("100 km to m"))
print(ai.ask("derivative of x^2"))
```

## Features
- TinyLM (NumPy/Torch educational decoder-only Transformer)
- Agents: chat, research, memory, documents, calculator, code, lab
- Thinking loop, science/math (calculus, geometry, physics, **units**)
- Web UI + OpenAI-compatible API
- INT4 quantization, KV cache, RoPE, GQA, SwiGLU, SWA

## Note
Large `.npz` checkpoints are gitignored. Full source zip: project `artifacts/ORBIT-AI-source.zip`.

See UNIFIED.md, SETUP.md, CYCLES_70_79.md.
