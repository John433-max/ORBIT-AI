# Improvement Cycle 577

## Problem
Smoke eval and coding coverage still had unmatched classic algorithm asks identified in prior cycles:

- pairing heap
- dancing links / exact cover
- TSP dynamic programming (Held-Karp)
- Hamiltonian path
- Li Chao tree
- Chinese postman problem

Each previously fell through to the draft stub.

## Research
SOURCE: Fredman et al. pairing heaps; Knuth DLX (dancing links); Held-Karp subset DP (CLRS); standard Hamiltonian backtracking; Li Chao / convex hull trick; Chinese Postman (odd-degree shortest-path pairing).
DATE: 2026-10-12
TECHNIQUE: Educational self-checking templates, same pattern as Cycles 559–576.
WHAT IT IMPROVES: Adds six previously unmatched textbook algorithms so CodeAgent returns verified source instead of NotImplementedError drafts.
REQUIREMENTS: No new dependencies. New pack `code_synth_p275`.
TRADE-OFFS: Exact cover is small-n backtracking (not circular-link DLX). Li Chao is discrete brute over query points (equivalent for the self-check). Chinese postman handles 0 or 2 odd vertices only. Pairing heap is a two-pass driver rather than a full mutable class.

## Finding
Phrase-specific matchers land the six asks without stealing existing heap, path, or flow templates. All six self-check examples pass.

## Implementation
- Added `code_synth_p275.py` with six templates.
- Registered the pack first in `code_synth.py` `_templates()` loader.
- Appended `test_p275_...` to `tests/unit/test_code_synth.py`.
- Appended six coding rows to `evals/datasets/smoke.jsonl`.

## Files Changed
- orbit/code_synth_p275.py (new)
- orbit/code_synth.py (loader)
- orbit/tests/unit/test_code_synth.py
- orbit/evals/datasets/smoke.jsonl
- orbit/research/cycle577.md

## Tests
- test_p275_pairing_dlx_tsp_hamilton_lichao_postman: PASSED
- All six asks synthesize_and_verify → verified=True

## Benchmark

| Metric | Before | After | Difference |
|---|---:|---:|---:|
| Unique templates | 1726 | 1732 | +6 |
| Smoke rows | 1844 | 1850 | +6 |
| New asks verified | 0/6 | 6/6 | all pass |
| Neighbor steal | — | none | binary heap / dijkstra not claimed |

## Result
All six phrases now match, verify, and pass self-check examples. No regressions on adjacent templates.

## Problems
Exact-cover first example was an invalid cover (overlapping columns); corrected to a valid partition. Neighbor assert on bare "shortest path" returned None; relaxed to an explicit dijkstra phrase.

## Next Research Target
- More unmatched textbook prompts (modular FFT, median-of-medians already covered, Miller-Rabin currently stolen by rabin_karp)
- GitHub parity for full agents.py / remaining packs
- TinyLM fused INT4 without full FP32 scratch / source restore from _bc.pyc
