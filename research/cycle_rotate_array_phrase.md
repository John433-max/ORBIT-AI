# Improvement Cycle — rotate an array right by k

## Problem
Coding path: "write a function to rotate an array right by k" missed `rotate_array` (`rotate (the )?array` does not match "rotate an array") and returned a draft stub `write_a_function_to_rotate_an_array_righ`.

## Research
Local matcher in `code_synth_p25.py` already implements LeetCode 189 right-rotate. Gap was the phrase, not the algorithm.

## Implementation
`code_synth._widen_loaded` override for `rotate_array` adds `rotate an array right` / `rotating an array right`, and excludes matrix, image, linked, string, and list so siblings stay put.

## Tests
- `tests/unit/test_code_synth.py::test_rotate_array_right_by_k_phrase` pass (pytest missing; function called directly)
- Agent probe: coding_agent, `def rotate_array`, Verified against 2 examples
- New smoke row `code_rotate_array_phrase_1` score_row ok=True

## Benchmark
Baseline smoke (before row): 1734/1734 = 100% (`evals/results/2026-10-09_211031_eval.json`)
After: new row scored ok; full 1735 suite not re-run this cycle.

## Next
GitHub parity for this matcher, or another stub-fallthrough phrase.
