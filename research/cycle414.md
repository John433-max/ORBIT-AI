# Cycle 414 — maze and union-find graph fallbacks

## Problem
After Cycle 413, smoke coding was 1051/1051, but several graph phrases still returned draft stubs: `the maze`, `the maze ii`, `sentence similarity ii`, `satisfiability of equality equations`, `count unreachable pairs`, and `find closest node to given two nodes`.

## Research
SOURCE: LeetCode 490 / 505 / 737 / 990 / 2316 / 2359 problem statements (official examples).
DATE: 2026-10-04
TECHNIQUE: Phrase-specific verified templates (rolling-ball BFS/Dijkstra, union-find, component-size pairs, functional-graph distances).
PROBLEM SOLVED: CodeAgent fallback on those asks.
HOW IT WORKS: Match a tight phrase, emit a self-checked function, report Verified when examples match.
REQUIREMENTS: Existing Template loader; no new dependencies.
TRADE-OFFS: Educational implementations, not production graph libraries. Maze III (lexicographic path) left out to avoid a weak partial matcher.
RELEVANCE TO ORBIT: Coding-task success is the measured smoke metric.
EXPECTED BENEFIT: +6 verified coding rows without stealing nearest-exit or bipartite.

## Implementation
`code_synth_p137.py` registered first in `code_synth.py`. Smoke `code_1054`–`code_1059`. Unit `test_p137_maze_union`.

## Validation
Unit examples match official LC samples (maze reach True/False, maze II distance 12 / -1, unreachable pairs 0 and 14, closest node 2). Collision checks keep nearest-exit and bipartite.

## Benchmark
| Metric | Before | After | Difference |
|---|---:|---:|---:|
| smoke rows | 1094 | 1100 | +6 |
| smoke pass | 1094/1094 | 1100/1100 | +6 |
| coding pass | 1051/1051 | 1057/1057 | +6 |
| smoke wall | — | 131.6 s | new rows only 1.58 s |

Unit `test_p137_maze_union` and `test_p136_missing_graph` passed (direct call; pytest not installed).

## Result
Kept. Six former draft stubs now return verified functions. Nearest-exit maze and bipartite matchers unchanged.

## Next
Maze III, regions cut by slashes, or smallest string with swaps — still fallbacks.
