# Improvement Cycle 298

## Problem
Coding/search/identity probes already pass locally (498/498). Highest remaining value: expand deterministic coding coverage and close GitHub pack parity without overwriting the slim remote `agents.py`.

## Research
LeetCode Easy templates that were still missing from packs: 1323 maximum 69 number, 1662 equivalent string arrays, 1523 odds in interval, 1720 decode XOR array, 1748 sum of unique, 1710 maximum units on a truck.

## Finding
`is_odd` in `code_synth_p1` matched any "odd number(s)" phrase and stole the interval prompt. Tightened matcher to exclude interval / "count odd" / plural "odd numbers".

## Implementation
- Added `code_synth_p37.py` (6 templates, all `verify_source` ok).
- Loader hook in `code_synth.py`.
- Smoke rows `code_459`–`code_464`.
- Unit test `test_p37_69_equiv_odds_xor_unique_truck`.

## Tests
pytest test_code_synth + thinking + agents; full smoke eval.

## Result
Templates 489→495. Smoke 498→504 coding +6.
