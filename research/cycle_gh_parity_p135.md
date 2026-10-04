# Cycle GH-parity p135

Date: 2026-10-04

## Problem
Local smoke 1088/1088 already covers code_synth_p135 (closed islands, all paths, eventual safe, inform time, detonate bombs, reorder routes). GitHub main stopped at code_1041 / p134, so CI could not see those verified templates. Local thinking/agents also route `add N and/to M` to calculator without stealing "write a function that adds…".

## Implementation
Push focused files only:
- code_synth.py (loader lists code_synth_p135)
- code_synth_p135.py
- evals/datasets/smoke.jsonl
- agents.py / thinking.py (add-number calculator route)

## Tests
- doctor READY
- eval 1088/1088 (100%) before push
- probes: add-function → verified Python; fusion search → no live web; name → ORBIT
- pytest test_classify_add_and + test_p135_closed_islands_routes
