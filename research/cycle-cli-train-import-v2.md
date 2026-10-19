# Cycle: graceful train import in OrbitAI (v2)

## Problem
`run_orbit.py chat` and `OrbitAI()` crashed with `ModuleNotFoundError: No module named 'train'`.
`orbit_ai.OrbitAI._try_load_checkpoint` did a hard `from train import build_model_from_checkpoint`.
`train.py` is absent from the slim tree (only tinylm + agents). CLI chat and probes were unusable.

## Research
Slim checkouts and GitHub-published trees omit the large training script.
Agents already route through Orchestrator + TinyLM / ModelProvider when no full checkpoint is loaded.
Optional import is the standard pattern used elsewhere (doctor API deps, tinylm optional torch).

## Implementation
`orbit_ai.py`: wrap the train/bpe imports in try/except ImportError; return early if missing.
Checkpoint load still runs when train.py is present. No behavior change when train exists.

## Files
- orbit_ai.py

## Tests / probes
- doctor: READY
- `run_orbit.py chat "write a python function that adds two numbers"` → real `def add` + Verified
- `run_orbit.py chat "search for recent news about fusion energy"` → ResearchAgent honest "No live web available..."
- `run_orbit.py chat "what is your name"` → ORBIT identity (not web movie)
- OrbitAI(persist=False): model_loaded=False, agents=7, coding route returns function

## Benchmark
Prior eval (unchanged by this CLI-only fix): accuracy 1.0 (2083/2083).
Coding/search/RAG/permission categories 1.0.

## Result
CLI chat no longer hard-fails on missing train.py. Coding / search / identity probes pass.

## Next
- Optional: restore train.py from pyc if large-checkpoint load is required.
- Continue coding template expansion if new eval gaps appear.
