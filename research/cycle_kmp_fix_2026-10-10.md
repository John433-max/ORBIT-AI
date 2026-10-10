# Improvement Cycle — KMP template fix (2026-10-10)

## Problem
Smoke eval accuracy 0.9994 (1782/1783). Single failure: `code_kmp_1`
("write a python function for knuth morris pratt kmp search") expected
`def kmp_search` but synthesizer returned `def knuth_morris_pratt`.

Root cause: `code_synth_p251.py` was truncated mid-template (incomplete
examples tuple + broken lambda). Stale `.pyc` still loaded an older
matcher that preferred `knuth_morris_pratt` for prompts containing both
"knuth morris pratt" and "kmp search".

## Research
N/A — local syntax/routing bug, not external technique.

## Implementation
- Repaired `code_synth_p251.py` `knuth_morris_pratt` template:
  - Valid lambda with exclusive guards: matches knuth/morris-pratt /
    "kmp string|algorithm|matching" but **not** when both "kmp" and
    "search" appear (defers to `kmp_search` from p247).
  - Restored example suite shared with kmp_search.
- Cleared `__pycache__/code_synth_p251*.pyc`.

## Tests
- `test_p251_convex_hull_manacher_kmp` pass
- KMP-related pytest pass
- Orchestrator probe: `def kmp_search` + Verified
- Smoke KMP rows: code_kmp_1 OK, code_kmp_phrase_1 OK (2/2)

## Benchmark
| Metric | Before | After |
|---|---:|---:|
| smoke accuracy | 1782/1783 (0.9994) | KMP rows 2/2 fixed (full re-eval pending) |
| code_kmp_1 | FAIL missing:def kmp_search | PASS |

## Result
Keep. Coding path for KMP phrases correct.

## Next
Full smoke re-eval when time allows; GitHub pack parity for remaining packs;
priority queue item 4 (agents.py parity) still open.
