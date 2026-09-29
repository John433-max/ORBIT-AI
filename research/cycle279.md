# Cycle 279 — code_synth pack 21 + smoke expansion

Date: 2026-09-28

## Baseline
- doctor: READY (fastapi/uvicorn warning; Ollama optional down)
- smoke: 402/402 (coding 362/362)
- probes: coding → verified add(); search → research path; identity → ORBIT

## Problem
Highest remaining queue item after passing probes is coding-eval expansion + GitHub pack parity.

## Change
- Added `code_synth_p21.py`: goat_latin, reordered_power_of_2, prime_number_of_set_bits, valid_square, complex_number_multiply, convert_to_base7.
- Tightened `is_prime` / `is_power_of_two` matchers so they do not steal set-bits / reordered-power prompts.
- Wired pack into `code_synth.py` loader.
- Smoke +6 coding rows (code_363–code_368).
- All 6 templates `verify_source` ok; matchers unique vs existing packs.

## Result
- templates 393 → 399
- smoke 402 → 408; eval 408/408 coding 368/368
- unit: tests/unit/test_code_synth.py + test_thinking.py 70 passed
