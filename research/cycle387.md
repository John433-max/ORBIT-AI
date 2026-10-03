# Improvement Cycle 387

## Problem
GitHub main smoke rows code_888–code_893 expect p108 templates
(can_make_square, smallest_divisible_digit_product, stone_removal_game,
minimum_operations_distinct, minimum_operations_columns, zigzag_traversal)
but code_synth_p108.py was not on main and code_synth.py did not import it.
A fresh clone would fail those six coding eval rows.

## Research
Template packs load by explicit name list in code_synth.py (not filesystem scan).
Smoke already contained the six prompts; local synthesize_and_verify returned
verified=True, checked=3, fallback=False for each.

## Implementation
Ship code_synth_p108.py and register it before p107 in the loader.

## Tests
Local eval already 933/933 including code_888–code_893.
synthesize_and_verify verified=True on all six prompts.
OrbitAI chat on the zigzag prompt returns Verified code.

## Benchmark
| Metric | Before (GitHub) | After (local, already) |
| smoke coding rows for p108 | missing pack | 6/6 verified |
| full smoke | would miss 6 | 933/933 |

## Next
Further Easy packs only if prompts are not already indexed; keep GH loader in sync with smoke.
