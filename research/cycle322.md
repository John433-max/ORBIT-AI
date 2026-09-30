# Improvement Cycle 322

## Problem
Coding coverage still grows via Easy templates; GitHub loader lagged local packs.

## Implementation
- Added `code_synth_p60.py` (6 Easy templates): faulty keyboard, take gifts, min common value, trailing zeros string, row with max ones, alternating digit sum.
- Loader includes `code_synth_p60`.
- Smoke coding 596 → 602.

## Tests
- test_code_synth: 95 passed
- smoke: 642/642 (coding 602/602)
- probes: coding sandbox + Verified; search honest no-live-web; identity ORBIT

## Benchmark
| Metric | Before | After |
| smoke | 630/630 (latest prior) / dataset 636 | 642/642 |
| templates | 623 | 629 |

## Next
Push remaining missing GH packs. Slim agents.py still local-only.
