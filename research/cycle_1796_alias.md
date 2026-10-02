# Improvement Cycle — 1796 name alias

## Problem
Smoke `code_758` failed (852/853). Prompt "second largest digit … leetcode 1796" expected `def second_highest`. Pack p92 (later, last-match wins) emitted `second_largest_digit` + camelCase `secondHighest` only, so the p86 name never appeared.

## Research
LeetCode 1796 official method name is `secondHighest`. Local smoke rows require both `def second_highest` (code_758) and `def second_largest_digit` (code_790). Last-registered template wins; aliases must live on the winning pack.

## Implementation
`code_synth_p92.py` already defines `second_highest` as an alias of `second_largest_digit`. Locked with a regression assert in `test_p92_digit_nice_rotated_swap_population_freq` that one synthesis contains both defs.

## Validation
OrbitAI.ask score_row: code_758 ok, code_790 ok. Unit functions p86+p92 pass.
