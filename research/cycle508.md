# Improvement Cycle 508

## Problem
Smoke coding path was 1644/1644, but several natural "write a function" asks still fell through to the generic fallback (nth odd, one Collatz step, both diagonal sums, every index of a value, letter grade, sliding window sums).

## Research
Template routing already prefers the first matching pack. New asks need narrow predicates so sum_list, count_words, and collatz step-counts are not stolen. Self-check examples follow the existing verify_source path.

## Implementation
- code_synth_p224.py: nth_odd, collatz_next, diagonal_sums, index_of_all, letter_grade, window_sums
- code_synth.py loads p224 first
- smoke code_1606–code_1611
- tests/unit/test_code_synth.py::test_p224_nth_odd_grade_windows_not_stolen

## Tests
- unit function passed
- new smoke rows 6/6 via OrbitAI.ask
- guards: sum_list and count_words unchanged

## Benchmark
New rows verified. Full eval recorded after runner completes.
