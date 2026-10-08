# Improvement Cycle 513

## Problem
GitHub main stopped at code_synth_p227. Local p228 (mean_list, sum_evens) was unregistered remotely. The first mean_list matcher also stole geometric mean, MAE, MAD, column means, and harmonic mean because those prompts contain "mean" and "list".

## Research
Pack order is first-match (p228 ahead of p227). Arithmetic mean is sum/len (empty -> 0.0). Sum of evens is a filter, not sum_list. Special means already have templates (geometric_mean, mae, mean_absolute_deviation, column_means, harmonic_mean) and must stay excluded.

## Implementation
Tightened mean_list exclusions: geometric, harmonic, absolute, column, matrix, error, deviation. Registered p228 on GitHub and appended smoke code_1630-1632.

## Files
- code_synth_p228.py
- code_synth.py (pack list only on GitHub; local already listed p228)
- evals/datasets/smoke.jsonl
- GitHub commit 21bbac5

## Tests
- synthesize_and_verify: mean_list, sum_evens, geometric_mean, mae, mean_absolute_deviation, column_means, harmonic_mean all verified on the intended names
- add / fusion search / identity probes unchanged

## Benchmark
| Metric | Before | After | Difference |
|---|---:|---:|---:|
| GitHub packs | max p227 | p228 registered | mean_list shipped |
| geometric mean route | mean_list (steal) | geometric_mean verified | regression fixed |
| smoke file | 1668 rows on GH | 1671 | +3 coding rows |

## Result
Kept. Matcher tighten is local and on main.

## Next
Re-run full smoke on the settled tree (do not overlap pack writes). Then any packs after p228.
