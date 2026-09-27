# Improvement Cycle 243

## Problem
GitHub `code_synth.py` still ~32 templates (~18KB) while local has 198 verified templates (224KB). CI/eval on main cannot cover the local coding path.

## Research
Highest remaining priority with local doctor READY + smoke 210/210 + probes passing is GitHub parity of the coding path (queue item 4).

## Implementation
Push local `code_synth.py`, `evals/datasets/smoke.jsonl`, `tests/unit/test_code_synth.py`. Do not replace GitHub `agents.py` or `thinking.py` (CI-slim vs local-full; prior placeholder incidents).

## Result
Local: doctor READY; smoke 210/210 coding 183/183; pytest synth+agents+thinking 82 passed.
Probes: add-two-numbers → coding_agent verified; fusion search → research_agent; name → ORBIT.

## Next
Full local agents.py slim-parity or fastapi serve extras.
