# Improvement Cycle 232

## Problem
GitHub `code_synth.py` still ~32 templates (~18KB) vs local 132 templates / 130KB.
GitHub `evals/datasets/smoke.jsonl` stops around code_75; local eval is 136/136
(coding 117/117). Probes already pass locally.

## Research
Highest remaining queue item after local coding/search/identity: GitHub parity.
Do not replace GH `agents.py` slim CI surface with the 75KB local orchestrator
in the same commit (prior CI breakage).

## Implementation
- Documented gap.
- Push local `evals/datasets/smoke.jsonl` + `code_synth.py` +
  `tests/unit/test_code_synth.py` when the GitHub connector accepts the payload.
- Local behavior unchanged this cycle.

## Tests
- doctor READY
- eval 136/136
- pytest test_code_synth + test_agents: 66 passed
- probes: coding sandbox fn, search honest no-live-web, identity ORBIT

## Next
Push full `code_synth.py` if this cycle only landed smoke; then slim-parity
agents.py or fastapi serve extras.
