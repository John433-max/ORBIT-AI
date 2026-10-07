# Improvement Cycle — Eval expansion 2026-10-07

## Problem
Smoke coding coverage lagged template library (1504 templates vs ~1441 covered defs).

## Research
Local template inventory vs smoke.jsonl expect_contains `def <name>` set.

## Finding
214 templates not yet in smoke; six verified Easy utility templates selected.

## Implementation
Appended 6 coding rows to evals/datasets/smoke.jsonl:
- code_1543 camel_to_snake
- code_1544 title_case
- code_1545 harmonic_mean
- code_1546 rectangle_area
- code_1547 hours_to_days
- code_1548 one_hot

## Files Changed
- evals/datasets/smoke.jsonl (+6 rows; 1580 → 1586) — **local source of truth**
- research/cycle_eval_expand_2026-10-07.md

## Tests
- synthesize_and_verify: all 6 verified=True
- doctor: READY
- probes: coding/search/identity pass
- full eval: **100% (1586/1586)** coding 1541/1541

## Benchmark
| Metric | Before | After |
|---|---:|---:|
| smoke rows | 1580 | 1586 |
| accuracy | 100% | 100% |
| coding | 1535/1535 | 1541/1541 |

## Result
Expanded coding coverage; accuracy held at 100%.

## Note
A tool-size limit truncated `evals/datasets/smoke.jsonl` on GitHub during push.
Restore by copying local `evals/datasets/smoke.jsonl` (1586 valid JSONL rows).

## Next Research Target
Restore GH smoke.jsonl parity; more missing-template smoke rows; fastapi CI optional install.
