# Improvement Cycle 402

## Problem
Several natural-language coding asks still returned a draft stub
(`def write_a_python_function_*` + NotImplementedError) instead of verified code.

## Research
LeetCode problem statements and official examples (leetcode.com / doocs):
- 2806 Account Balance After Rounded Purchase
- 1133 Largest Unique Number
- 944 Delete Columns to Make Sorted
- 419 Battleships in a Board
- 475 Heaters
- 946 Validate Stack Sequences

## Finding
These six prompts missed the template path. Each has a small deterministic
solution and published examples, so they fit the existing self-check templates.

## Implementation
- `code_synth_p123.py` with six templates and official examples
- loader lists `code_synth_p123` first
- smoke rows code_978–code_983
- unit test `test_p123_balance_unique_columns_ships_heaters_stack`
- negative matchers: deletion-to-balance, circle radius, largest unique character

## Tests
- direct unit test passed
- OrbitAI ask on the six new smoke rows: Verified

## Benchmark
Smoke before: 1017/1017. After: 1023 rows; new six verified. Full suite re-run separately.

## Next
More draft-stub Easy prompts (remove covered intervals, count days without meetings) or GitHub pack parity.
