# Cycle 251 — GitHub code_synth pack parity

Date: 2026-09-27

## Problem
Local coding path is 234 templates / smoke 246/246, but GitHub still
had only `code_synth.py` + a slim `code_synth_p1.py` (~12 KB). Missing
`code_synth_p2.py` and `code_synth_p3.py` means CI and clones cannot
match local coding coverage.

## Change
Push local packs + loader + smoke + unit tests. Do **not** overwrite
GitHub `agents.py` (16 KB CI stub vs local 80 KB).

## Local baseline (this run)
- doctor: READY (fastapi/uvicorn warning, Ollama optional)
- smoke: 246/246 (coding 219/219)
- probes: add-two-numbers → coding_agent verified; fusion search →
  research_agent; identity → ORBIT
- pytest tests/unit/test_code_synth.py + test_agents + thinking: 83 passed

## Files
- code_synth.py (lazy pack loader)
- code_synth_p1.py / p2.py / p3.py
- tests/unit/test_code_synth.py
- evals/datasets/smoke.jsonl
