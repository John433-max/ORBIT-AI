# Improvement Cycle 547

## Problem
Priority-1 coding path returned draft stubs (NotImplementedError / "Draft from") for common natural-language asks:
- "write a python function that parses a URL"
- "implement topological sort" / "implement a function for topological sort"
- "write a python function for bfs" / "implement dfs"
- "write a function for union find"
- "write a python function that finds all primes up to n"
- "write a function to rotate an array" (rotate_array existed but matcher required "right" or "rotate array")

## Research
- Kahn's algorithm for topological sort on a DAG (indegree queue).
- BFS/DFS visit order on an adjacency-list graph.
- Union-find with path compression.
- Sieve of Eratosthenes returning the prime list (distinct from existing count_primes).
- urllib.parse.urlparse for URL components.
- Existing rotate_array already implements right-rotate by k; only the phrase matcher was too strict (`rotate (the )?array` missed "an").

## Finding
Adding six focused templates (loaded first) and relaxing the rotate_array regex closes the gaps. Tight matchers avoid stealing count_primes ("count" excluded) and list_union.

## Implementation
- New pack `code_synth_p244.py`: parse_url, topological_sort, bfs, dfs, union_find, sieve_primes
- Loader lists `code_synth_p244` first
- `_widen_loaded` rotate_array accepts "rotate an array" / "rotates an array"
- Unit `test_p244_graph_url_and_rotate_phrase`
- Smoke rows for the seven asks

## Files Changed
- code_synth_p244.py (new)
- code_synth.py
- tests/unit/test_code_synth.py
- evals/datasets/smoke.jsonl
- research/cycle547.md

## Tests
- New unit test passed
- Prior cycle-541/542 unit tests passed
- Chat probes for the six asks + add: Verified, no stub
- New smoke rows 7/7 pass via OrbitAI.ask
- doctor: READY

## Benchmark
| Metric | Before | After |
|---|---:|---:|
| smoke rows | 1741 | 1751 |
| coding stubs on these asks | 6 draft stubs | 0 (Verified) |
| doctor | READY | READY |

## Result
Coding path now returns real verified functions for URL parse, topo sort, BFS, DFS, union-find, sieve primes, and "rotate an array".

## Next Research Target
- More graph/string stubs that still fall through (if any)
- GitHub pack parity for p244
- Model provider defaults (Ollama when healthy) — already auto; Ollama down in this env


## Follow-up (same cycle)
Smoke 1750/1751 failed on `code_recover_bst_1` ("recover binary search tree").
The p243 template matched, but:
1. Orchestrator.route treated `\bsearch\b` as a web lookup and skipped the template→code boost.
2. `_wants_code_written` returned False for the same reason, so CodeAgent tried to exec the title as Python (syntax error → Thinker hedge).

Fix: algorithm names containing "search" (binary/linear/interpolation/exponential/ternary/fibonacci search) do not count as web lookups when a verified template hits.
- agents.py `route` template boost
- agents.py `_wants_code_written`
- tests/unit/test_code_route_search.py

Identity and fusion-news probes still route correctly.
