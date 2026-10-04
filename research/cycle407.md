# Improvement Cycle 407

## Problem
Unmatched medium asks still drafted: swim in rising water (778), shortest path in a binary matrix (1091), path with minimum effort (1631), cherry pickup (741), odd even jumps (975), bus routes (815), snakes and ladders (909), sequence reconstruction (444).

## Research
LeetCode official examples only (not copied solutions):
- 778: [[0,2],[1,3]] -> 3; the 5x5 height grid -> 16.
- 1091: [[0,1],[1,0]] -> 2; [[0,0,0],[1,1,0],[1,1,0]] -> 4; blocked start -> -1.
- 1631: [[1,2,2],[3,8,2],[5,3,5]] -> 2; effort-1 grid -> 1; zero-effort path -> 0.
- 741: [[0,1,-1],[1,0,-1],[1,1,1]] -> 5; blocked grid -> 0.
- 975: [10,13,12,14,15] -> 2; [2,3,1,1,4] -> 3; [5,1,3,4,2] -> 3.
- 815: [[1,2,7],[3,6,7]] 1->6 -> 2; unreachable -> -1.
- 909: 6x6 portal board -> 4; [[-1,-1],[-1,3]] -> 1.
- 444: [[1,2],[1,3],[2,3]] uniquely rebuilds [1,2,3]; missing 2->3 does not.

## Finding
`iter_matching` was empty for these prompts, so pack order cannot steal existing smoke rows if matchers stay phrase-specific. Meeting-rooms II and `add` stay on their existing functions.

## Implementation
- `code_synth_p130.py` with the eight functions above.
- Loader lists p130 first.
- Smoke code_1016–code_1023.
- Unit test `test_p130_graph_dp_board`.

## Files Changed
- code_synth.py
- code_synth_p130.py
- evals/datasets/smoke.jsonl
- tests/unit/test_code_synth.py
- research/cycle407.md

## Tests
Direct call of `test_p130_graph_dp_board` passed. `synthesize_and_verify` true on all eight. Probes: add returns `def add` + Verified; fusion search returns live sources; identity is ORBIT.

## Benchmark

| Metric | Before | After | Difference |
|---|---:|---:|---:|
| Smoke rows | 1055 | 1063 | +8 |
| New asks | draft stubs | verified templates | fixed |
| add / meeting rooms II | existing functions | unchanged | no steal |

## Result
Kept. Eval accuracy recorded in the run report after the suite finishes.

## Problems
Name-token upgrade can still override pack order if a new name is a token superset of an existing hit. These matchers do not overlap current hits.

## Next Research Target
Cheapest flights is already templated. Remaining drafts: minimum taps (1326), shortest path visiting all nodes (847), job scheduling (1235) which is stolen by generic max_profit. GitHub pack parity.
