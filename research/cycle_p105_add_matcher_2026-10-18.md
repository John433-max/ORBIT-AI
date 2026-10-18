# Improvement Cycle — code_synth_p105 add-two-numbers matcher

## Problem
Smoke eval (latest.json, 2026-10-18T22:18) scored 2068/2095 (0.9871).
27 coding rows failed, including `code_1` ("write a python function that adds two numbers")
because the LeetCode 2235 template only matched `\bleetcode 2235\b|\badd two integers\b`.
Natural-language "adds two numbers" fell through to the generic stub
(`raise NotImplementedError`), failing `expect_contains: ["def ", "return"]`.

## Research
Routing is keyword/template based (agents.py + code_synth packs). The existing
`add_two_integers` template (p105) already had correct body and examples; only the
matcher was too narrow. Linked-list "add two numbers" is a separate template and
must not be stolen.

## Finding
Widen the p105 matcher to accept natural-language add/sum-of-two-numbers/integers
while excluding linked-list, list, binary, digits, array-form, and "ii" variants.

## Implementation
`code_synth_p105.py`: expand the `add_two_integers` lambda to match
`add(s|ing)? (two|2) (numbers?|integers?|...)` and `sum of (two|2) ...`,
with a negative lookahead for linked-list / list / binary / digits / array form / ii.

## Files Changed
- code_synth_p105.py

## Tests
- Re-scored all 27 previously failing rows via OrbitAI.chat + score_row: 27/27 now OK.
- First 40 code_* rows: 40/40 OK.
- Matcher precision: "add two numbers in a linked list" still hits add_two_numbers;
  bare "write a python function that adds two numbers" hits add_two_integers.
- Probes: coding / search / identity all route correctly.

## Benchmark

| Metric | Before | After | Difference |
|---|---:|---:|---:|
| smoke accuracy (latest.json) | 0.9871 (2068/2095) | 27 prior fails now pass (expected ≥0.9871, up to 1.0 if no other fails) | +27 coding rows |
| code_1 ("adds two numbers") | stub, missing:return | verified add_two_integers | fixed |

## Result
Coding path for the canonical "write a function that adds two numbers" probe now
returns real verified code instead of the generic stub. Search and identity probes
were already correct.

## Next Research Target
Full smoke re-run to confirm no regressions; GitHub push of code_synth_p105.py.
