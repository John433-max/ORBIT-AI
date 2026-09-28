# Improvement Cycle 268

## Problem
GitHub main still missing most `code_synth` packs (`p2`, `p3`, `p5`–`p11`, `p13`).
Local eval is already 360/360; coding/search/identity probes pass.
Highest remaining queue item: GitHub parity without replacing CI-slim `agents.py`.

## Research
Lazy pack loader in `code_synth.py` skips missing modules, so CI stays green if only some packs land.
Pushing verified packs incrementally is safer than overwriting `agents.py` (85KB local vs ~16KB CI surface).

## Implementation
- Document this cycle.
- Push packs p5–p10 (36 templates, Easy/bit/string) to `John433-max/ORBIT-AI` main.
- Leave local full `agents.py` / `thinking.py` un-overwritten on GitHub.

## Tests
Local: doctor READY; smoke 360/360; probes coding/search/identity pass.

## Next
Push p2/p3/p11/p13 + smoke.jsonl in later commits; fastapi extras optional.
