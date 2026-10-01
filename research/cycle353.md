# Improvement Cycle 353

## Problem
Coding synthesis still fell back on several Easy LeetCode asks. Probes showed no template for same-color chessboards (3274), maximum difference of increasing elements (2016), collect-elements operations (2869), categorize-box (2525), equal digit count/value (2283), and k-distant indices (2200). GitHub main also stopped at `code_synth_p81` while local already had p82.

## Research
Official problem statements define the functions. Matching stays first-hit plus Cycle 283 token-superset upgrade, so matchers use phrases that previously returned the `write_a_python_function_*` fallback. LeetCode 2869 removes from the end of the array, not the front.

## Implementation
`code_synth_p83.py` with six verified templates. Loader lists `code_synth_p83`. Unit test `test_p83_chessboards_diff_collect_box_digits_kdistant`. Smoke rows `code_740`–`code_745`.

## Tests
Direct execution of the new unit test and the p82 test: both passed. Collision probes (array-increasing ops, ancestor diff, count digits, find indices, chessboard square color) still hit the older templates. Subset eval of the six new rows: 6/6. Full smoke: 785/785 (was 779/779).

## Benchmark

| Metric | Before | After | Difference |
|---|---:|---:|---:|
| templates | 746 | 752 | +6 |
| p83 prompts verified | 0/6 (fallback) | 6/6 | +6 |
| smoke accuracy | 779/779 | 785/785 | +6 rows, still 100% |
| p82 regression | pass | pass | unchanged |

## Result
Kept. New asks return the named functions and pass the built-in examples.

## Next
Push p82+p83 packs, loader, smoke, and unit test to GitHub main. Do not overwrite slim `agents.py`.
