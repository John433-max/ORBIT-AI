# Improvement Cycle — GitHub parity packs 162–170

## Problem
Local coding templates p162–p170 (56 functions) and smoke rows were not on GitHub main (remote max pack 161). Loader, unit tests, and smoke.jsonl were ahead of origin.

## Research
Template packs are the coding-path source of truth. Parity means the remote CI tree can match local `get_templates()` and smoke coding rows. No new algorithm — publish already-verified local packs.

## Implementation
Copied onto main:
- code_synth_p162.py … code_synth_p170.py
- code_synth.py loader order (p170 first)
- tests/unit/test_code_synth.py pack tests
- evals/datasets/smoke.jsonl (+57 lines)

## Tests
- verify_source on 56 new templates: 0 bad
- pytest -k p162..p170: 9 passed
- smoke latest.json before push: 1302/1302 (coding 1257/1257)
- probes: add-two-numbers code, fusion search with sources, identity ORBIT

## Benchmark
| Metric | Before (GH) | After (local, pushed) |
|---|---:|---:|
| packs on main | 161 | 170 |
| new templates | 0 | 56 (all verify ok) |
| smoke rows | smaller file 212088 B | 224167 B / 1302 scored |

## Result
Keep. Push focused files only (no secrets).

## Next
Serve extras remain optional (fastapi/uvicorn warning). Ollama still down; TinyLM fallback is correct. Next coding pack or CI green check on this push.
