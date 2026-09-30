# Improvement Cycle 307

## Problem
Smoke coding coverage lagged the template library; GitHub still missing later packs (p43+).

## Implementation
Added `code_synth_p45.py` (6 Easy templates):
- numbers_with_even_digits (tight matcher vs existing `find_numbers`)
- restore_string
- halves_are_alike
- num_water_bottles
- thousand_separator
- average_salary_excluding

Wired pack in `code_synth.py`. Smoke +6 coding rows (code_507–512). Unit test `test_p45_*`.

## Tests
- test_p45 + related: pass
- smoke 552/552 (coding 512/512)
- probes: coding Verified; search honest no-live-web; identity ORBIT

## Benchmark
| Metric | Before | After |
| smoke | 546 dataset / last recorded 540 eval | 552/552 |
| templates | 536 | 542 |

## Next
GitHub parity for remaining packs (p2/p3/p28–p32) or more Easy templates.
