# Improvement Cycle 548

## Problem
Coding path still returned draft stubs for Kruskal / Prim, and "implement minimum spanning tree" was stolen by `list_span` (matcher used bare `"span" in low`, which hits "spanning"). "write a function for binary search tree insert" also stubbed even though `insert_into_bst` exists.

## Research
- Kruskal: sort edges by weight, Union-Find with path compression / union-by-rank, accumulate weight until n-1 edges (CLRS ch. 23).
- Prim: grow a cut from vertex 0 with a binary heap (same MST weight on the undirected examples).
- Phrase routing: first-loaded pack wins; excluding "spanning"/"mst"/"tree" from list_span is the safety net.

## Finding
Adding a first-loaded pack for Kruskal (also matching MST phrases) and Prim, plus widening list_span and insert_into_bst, closes the stubs without changing statistical-range behavior.

## Implementation
- New pack `code_synth_p245.py`: `kruskal`, `prim` (self-checked examples).
- Loader lists `code_synth_p245` first.
- `_widen_loaded` excludes spanning/mst/tree from `list_span`.
- `_widen_loaded` accepts "binary search tree insert" on `insert_into_bst`.
- Unit `test_p245_mst_and_bst_phrase`.
- Smoke rows for Kruskal, MST, Prim, BST insert phrase.

## Files Changed
- code_synth_p245.py (new)
- code_synth.py
- tests/unit/test_code_synth.py
- evals/datasets/smoke.jsonl
- research/cycle548.md

## Tests
- test_p245_mst_and_bst_phrase: pass
- New smoke rows 4/4 via OrbitAI.ask
- Orchestrator probes: Kruskal, MST, Prim, BST insert, add, identity all correct

## Benchmark

| Metric | Before | After | Difference |
|---|---:|---:|---:|
| "write a function for kruskal" | draft stub | Verified kruskal | fixed |
| "implement minimum spanning tree" | list_span (wrong) | Verified kruskal | fixed |
| "implement prim's algorithm" | draft stub | Verified prim | fixed |
| "binary search tree insert" | draft stub | Verified insert_into_bst | fixed |
| statistical range of a list | list_span | list_span | unchanged |
| smoke rows | 1751 | 1755 | +4 |

## Result
Keep. MST asks no longer hit the statistical-range template; Kruskal and Prim return real verified functions.

## Problems
None observed on the targeted probes. Full smoke re-run recorded separately if completed.

## Next Research Target
Aho-Corasick / remaining graph stubs, or GitHub pack parity for p245.
