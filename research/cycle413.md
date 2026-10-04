# Cycle 413 — missing graph templates

## Problem
Smoke coding was 1045/1045, but several graph phrases still returned draft stubs (`clones a graph`, `max area of an island`) or had no smoke row (`clone graph`, `graph valid tree`, `possible bipartition`, `flower planting`, `nearest exit`).

## Research
LeetCode 133 / 261 / 886 / 1042 / 1926 / 695 are standard graph checks. Existing p3 templates already cover rotting oranges, flood fill, 01 matrix, provinces, surrounded regions, and accounts merge. A first p136 draft shadowed those and dropped smoke to 1088/1094; it was reverted.

## Implementation
`code_synth_p136.py` with phrase-tight matchers:
- clone graph (also "clones a graph")
- graph valid tree
- possible bipartition (does not steal "is graph bipartite")
- flower planting gardens (does not steal can-place-flowers)
- nearest exit
- max area of island, with both `max_area_of_island` and `maxAreaOfIsland`

Loader registers p136 first. Six smoke rows code_1048–code_1053. Unit `test_p136_missing_graph`.

## Benchmark
- Before: 1088/1088 (100%), coding 1045/1045
- Shadow attempt (reverted): 1088/1094
- After: see eval latest.json

## GitHub
p135 was local-only vs `/tmp/orbit-gh`. Push attempted separately.
