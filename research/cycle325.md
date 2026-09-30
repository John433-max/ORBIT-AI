# Improvement Cycle 325

## Problem
GitHub `code_synth` loader stopped at p60; local p62 templates and newer Easy coverage were not on main. Coding/search/identity probes already pass locally.

## Research
Keep packs split. Push small p62 + new p63 without replacing slim GitHub `agents.py`. Avoid name collisions with existing altitude / digit-sum / delayed-arrival / pivot-integer templates.

## Implementation
- `code_synth_p63.py`: find_max_k, delete_greatest_value, count_changing_keys, check_x_matrix, count_negatives, find_subarrays.
- Loader lists `code_synth_p63`.
- Smoke `code_620`–`code_625`.

## Tests
- synthesize_and_verify True on 6 new prompts
- Orchestrator coding_agent + Verified on all 6
- doctor READY
- prior latest.json 648/648 (dataset now 665)

## Next
Push remaining missing GH packs (p2/p3, p28–p32, p44, p47/p49, p53–p57, p59) in later commits; keep slim agents.py.
