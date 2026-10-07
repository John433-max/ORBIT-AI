# Cycle: consecutive_diffs matcher guard

## Problem
Smoke `code_1439` ("write a function that returns consecutive differences") expected `def consecutive_diffs` (pack p198) but pack p206 `running_diff` loads earlier and matched any prompt containing "consecutive" and "difference".

## Research
Template packs are first-match. Later phrase-specific packs must not steal shorter prompts owned by earlier packs (same pattern as multiply vs dot-product, sort_list vs dutch flag).

## Implementation
`code_synth_p206.py` `running_diff` matcher now also requires "list", matching smoke `code_1488` ("consecutive differences of a list") and leaving the shorter prompt on `consecutive_diffs`.

## Tests
- synthesize_and_verify: short prompt → consecutive_diffs verified; "of a list" → running_diff verified.
- OrbitAI.ask + score_row: code_1439 and code_1488 ok after the guard.
- Baseline eval before the guard: 1533/1534 (only code_1439 missing `def consecutive_diffs`).

## Result
Coding path no longer returns the wrong function name for the shorter prompt.
