# Improvement Cycle — coding stack class + smoke expect_any

Date: 2026-10-16

## Problem
Smoke accuracy 2016/2020 (99.80%). Four coding failures:
1. code_stack_class_1 — "create a python class for a stack" fell through to NotImplemented draft (stack_class matcher too narrow).
2. code_752 / code_753 / code_824 — expect_contains listed alternate def names as AND, so a single correct template always failed scoring.

## Research
- Local stack_class in code_synth_p131.py only matched "implement a stack" / "stack class".
- evals/runner.py score_row: expect_contains is AND; expect_any is OR (already supported).

## Implementation
- Widened stack_class matcher for create/write/implement + class + stack phrases; exclude min/minmax/queue.
- smoke.jsonl: code_752/753/824 use expect_any for alternate def names + expect_contains Verified.

## Files
- code_synth_p131.py
- evals/datasets/smoke.jsonl

## Tests
- synthesize_and_verify stack class: verified True
- Orchestrator probes: coding_agent / research_agent / ORBIT identity
- score_row on 4 former fails: all ok
- test_eval_score: 2 passed

## Result
Coding path returns real Stack class; name-alias smoke rows no longer false-fail.

## Next
Full smoke re-run to confirm ≥2016/2020; GitHub parity for agents/code_synth packs still open.
