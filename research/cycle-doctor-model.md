# Cycle: doctor model package import

## Problem
`python run_orbit.py doctor` reported NOT READY because
`from model import TinyLM` failed: `No module named 'model.model'`.
`model/__init__.py` imported `from model.model import TinyLM` but the
module was never committed. GitHub main has the same gap.

## Baseline
- doctor: NOT READY (1 blocking)
- smoke: 2095/2095 (100%)
- probes: coding_agent ok, research_agent live results, identity ORBIT

## Change
Added `model/model.py` that re-exports `tinylm.numpy_model.TinyLMNumPy`
as `TinyLM`. Stub raises if the educational backend cannot be imported.

## After
- doctor: READY (4 non-blocking: PyYAML, API deps, TinyLM ckpt keys, Ollama)
- probes unchanged: coding / search / identity all pass

## Next
TinyLM warning: default checkpoint missing layer-2 keys
(`layers.2.ln1_w`, …). Non-blocking. Prefer Ollama when healthy;
document fastapi/uvicorn install for serve.
