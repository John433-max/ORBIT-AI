# Improvement Cycle 297

Date: 2026-09-29

## Problem
Local runtime is healthy (doctor READY, smoke 498/498, coding/search/identity probes pass).
GitHub `main` still lacks code_synth packs p28–p35 (loader already lists them; missing modules are skipped).
That is the highest remaining priority: GitHub coding-path parity without replacing the slim CI `agents.py`.

## Research
Pack loader already skips missing modules, so adding packs is additive and CI-safe.

## Implementation
- Keep local agents.py / thinking.py unchanged (85KB / 14KB vs GH 16KB / 11KB).
- Publish local `code_synth_p28.py` … `code_synth_p35.py` to GitHub main.
- Do not touch secrets or slim agents.py.

## Tests (local, pre-push)
- doctor: READY (fastapi/uvicorn warning; Ollama optional)
- eval: 498/498
- probes: coding → coding_agent verified add(); research → honest no-live-web; identity → ORBIT

## Next
p2/p3 (large) still local-only; slim-vs-full agents.py still diverged by design for CI.
