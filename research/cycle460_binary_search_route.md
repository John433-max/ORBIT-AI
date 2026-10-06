# Improvement Cycle 460

## Problem
"write/implement … binary search" routed to ResearchAgent because the word `search` boosted research over code. Rolling-hash and triangle-from-points asks hit the NotImplemented stub.

## Research
Routing should treat algorithm names (binary/linear search) as code when the user asked to write or implement a function, and keep explicit web cues (`search for`, `look up`, `news about`, `google`) on ResearchAgent.

## Sources
- Local `agents.py` `Orchestrator.route` research-tie boost (pre-change).
- Local `thinking.py` `_is_code` / `_is_search`.

## Finding
A code-write pattern plus no explicit web cue should win. Template pack p178 covers the stub misses.

## Implementation
- `agents.py`: research boost only on explicit web lookup, and only when the request is not a code-write.
- `thinking.py`: algorithm-search titles can still match a template.
- `code_synth_p178.py`: rolling_hash, linear_search, triangle_area_points, shoelace_area, rabin_karp.
- Smoke rows code_1313–code_1318.
- `tests/unit/test_code_route_search.py`.

## Benchmark
See run report after eval.
