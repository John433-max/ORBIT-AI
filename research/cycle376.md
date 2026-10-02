# Improvement Cycle 376

## Problem
GitHub main loader stopped at code_synth_p96. Local Cycles 373-375 (p97-p99) already route furthest-origin, two-out-of-three, knight-tour, and related Easy asks, but those modules were absent on main.

## Research
Pack-split loader (Cycle 244) skips missing modules so CI still collects. Parity requires publishing the pack files and appending their names to the loader list.

## Finding
Local probes already pass: add-two-numbers returns verified code; fusion search returns the honest no-live-web sentence; identity stays ORBIT. Highest remaining gap was GitHub parity, not routing.

## Implementation
No local behavior change. Published tested files to main:
- code_synth_p97.py, code_synth_p98.py, code_synth_p99.py
- code_synth.py loader entries p97-p99
- evals/datasets/smoke.jsonl
- tests/unit/test_code_synth.py

## Tests
- test_p97 / test_p98 / test_p99 executed: pass
- all 842 templates verify_source ok
- probes: coding, search, identity pass

## Result
Remote main now loads p97-p99. Commits 1f979509, b07a36d7, c7b484c4, 91142c9a, 27ba187f, 38b091f6.

## Next
Ollama still optional (no httpx). API deps (fastapi/uvicorn) still a doctor warning. Prefer Ollama only when a healthy endpoint exists.
