# Improvement Cycle — CI code_synth matcher fixes (2026-10-19)

## Problem
GitHub Actions run 39195723974 (commit ce18004) and the follow-up run 39196347512 (41eda0f) both failed on `Unit tests (code_synth)`. Core unit tests passed. Origin/main code_synth matchers were too strict or colliding, so several `test_code_synth.py` assertions failed.

## Research
Deterministic template routing uses first-hit plus token score. Equal/greedy matchers steal more specific asks when exclusions are missing. Official pattern: tighten the greedy matcher and widen the specific one (same approach as prior cycle notes).

## Finding
Reproduced on a clean origin/main clone. Failures included:
- `lis n log n` / `patience sorting lis` -> `longest_increasing_subsequence` (expected `lis_nlogn`)
- `write a function to rotate an array` -> no match (expected `rotate_array`)
- `write a function for binary search tree insert` -> no match (expected `insert_into_bst`)
- `tree diameter of an undirected tree` -> `diameter_of_binary_tree` (expected `tree_diameter`)
- `counts primes less than n` / `detect capital use` -> no template
- `design a hash map` -> no match (expected `design_hashmap`)
- `counts students doing homework at a query time` -> no match (expected `busy_student`)

## Implementation
- `code_synth_p355.py`: LIS excludes `patience` and `n log n`
- `code_synth_p25.py`: rotate_array accepts `rotate an array`
- `code_synth_p30.py`: insert_into_bst accepts `binary search tree insert`
- `code_synth_p4.py`: add `count_primes` + `detect_capital`; reverse_vowels phrase widen kept
- `code_synth_p3.py`: design_hashmap accepts `hash map`; inorder excludes construct/build
- `code_synth_p36.py`: busy_student accepts query-time / counts-students phrases
- Also carried local matcher diffs for p0/p161/p162/p2/p230/p237/p26/p407

## Validation
Previously failing subset: 8 passed. Full suite run recorded after.
