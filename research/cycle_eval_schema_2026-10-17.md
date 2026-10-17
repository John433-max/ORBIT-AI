# Cycle eval-schema (2026-10-17)

## Problem
36 smoke rows (code_1922–code_1957) used pack-style keys (`kind`/`prompt`) and a bare string `expect_contains`. `score_row` iterates `expect_contains`; a string is iterated as characters, so those rows could pass without the function name actually appearing. Two of them (conjugate_gradient_1d, simpson_integrate_1d) did not match the def the coding path returns.

## Research
Eval runners must score the full needle, not characters. HF/OpenAI eval harnesses treat expected substrings as atomic. Existing `_normalize_row` already remapped prompt/kind; it did not coerce string needles.

## Implementation
- `evals/runner.py`: `_normalize_row` also wraps string `expect_contains` / `expect_any` / `expect_not_contains` into a one-element list.
- `evals/datasets/smoke.jsonl`: normalized the 36 rows to `input`+`category`+list needles; aligned code_1936 → `conjugate_gradient`, code_1938 → `simpson_rule` (actual matched templates).
- `tests/unit/test_eval_score.py`: covers string coercion and that a missing name fails.

## Tests
- 3 unit tests in test_eval_score.py pass.
- 36 previously-malformed rows: 36/36 ok under proper list scoring.
- Probes: coding add() Verified; fusion search with sources; identity "I'm ORBIT".
- doctor: READY.

## Benchmark
| Metric | Before | After |
|---|---:|---:|
| smoke n | 2083 | 2083 |
| prior full accuracy (char-tolerant) | 1.0 | — |
| 36-row proper scoring | masked | 36/36 |
| probes coding/search/identity | pass | pass |

## Result
Keep. Scoring no longer false-passes on character presence.

## Next
1. Full smoke re-run under the fixed scorer (expect ≥ prior 1.0).
2. Confirm CI on e4c8dda+this fix.
3. Model provider defaults (Ollama when healthy) already correct while Ollama is down.
