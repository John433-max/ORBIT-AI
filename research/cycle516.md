# Improvement Cycle 516

## Problem
Smoke accuracy fell to 1673/1677 after Cycle 515. `min_of_list` (registered ahead of older packs) matched any list prompt containing "minimum" or "min ". That stole:

- code_1428 running minimum → `min_of_list` (missing `def running_minimum`)
- code_1445 cumulative minimum → `min_of_list` (missing `def cumulative_min`)
- code_1619 max minus min span → `min_of_list` (missing `def list_span`)

code_1635 also failed in that same eval (`forbidden:def absolute`). The smoke needle on disk is now `def absolute(`; rescoring the live `absolute_values` answer is ok. The four rows were the only failures.

## Research
SOURCE: Chen et al. 2021, HumanEval, https://arxiv.org/abs/2107.03374
DATE: 2026-10-08
TECHNIQUE: Negative guards on first-match routers
WHAT IT IMPROVES: Precision when a new scalar/list template is inserted ahead of prefix/span templates
TRADE-OFFS: Extra exclusions (`running`, `cumulative`, `prefix`, `span`, `minus`, `max`, `rolling`, `moving`)
RELEVANCE: ORBIT CodeAgent first-match pack order (p229 before p226/p199/p197)

## Implementation
Narrowed `min_of_list` in `code_synth_p229.py`. Extended `test_p229_odds_abs_square_min_digits_not_stolen` with the three stolen asks.

## Files
- code_synth_p229.py
- tests/unit/test_code_synth.py
- research/cycle516.md

## Tests
- direct `test_p229_odds_abs_square_min_digits_not_stolen` pass
- live score of code_1428, code_1445, code_1619, code_1635, code_1637 all ok

## Benchmark

| Metric | Before | After | Difference |
|---|---:|---:|---:|
| smoke n_ok | 1673/1677 | see eval after | |
| running minimum | min_of_list | running_minimum | restored |
| cumulative minimum | min_of_list | cumulative_min | restored |
| max minus min span | min_of_list | list_span | restored |
| minimum of a list | min_of_list | min_of_list | kept |
| absolute of a number | absolute | absolute | kept |

## Result
Kept. Router regression from Cycle 515 fixed without dropping the new min_of_list contract.

## Next
Confirm full smoke returns to 1677/1677. Push p229 + unit test if GitHub credentials allow.
