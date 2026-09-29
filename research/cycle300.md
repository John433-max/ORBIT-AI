# Improvement Cycle 300

## Problem
GitHub main missing code_synth packs p28–p32 and p38 while loader already lists them.
Local coding path already routes; GH CI would skip those templates.

## Implementation
- Added `code_synth_p39.py` (6 Easy templates).
- Loader includes p39.
- Smoke 510 → 516 coding rows.

## Tests
- doctor READY
- smoke 516/516
- pytest synth/thinking related 85 passed
- probes: coding sandbox + Verified; search research_agent; identity ORBIT

## Benchmark
| Metric | Before | After |
|---|---:|---:|
| smoke | 510/510 | 516/516 |
| coding rows | 470 | 476 |
| templates | 501 | 507 |

## Next
Push remaining large packs p2/p3 if CI needs them; keep slim agents.py on GH.
