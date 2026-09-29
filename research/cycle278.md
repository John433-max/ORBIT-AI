# Cycle 278 — code_synth pack 20 + smoke expansion

Date: 2026-09-28

## Baseline
- doctor: READY (fastapi/uvicorn warning; Ollama optional down)
- smoke: 396/396 (coding 356/356)
- probes: coding → verified add(); search → research path; identity → ORBIT

## Problem
Highest remaining queue item after passing probes is coding-eval expansion + GitHub pack parity.

## Change
- Added `code_synth_p20.py`: most_common_word, construct_rectangle, binary_gap, valid_boomerang, has_groups_size_x, largest_triangle_area.
- Wired pack into `code_synth.py` loader.
- Smoke +6 coding rows (code_357–code_362).
- All 6 templates `verify_source` ok; matchers unique vs existing packs.

## Result
- templates 387 → 393
- smoke 396 → 402; eval 402/402 coding 362/362
- unit: tests/unit/test_code_synth.py + test_thinking.py 69 passed
