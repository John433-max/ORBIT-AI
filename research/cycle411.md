# Cycle 411 — grid drafts that still returned NotImplemented

## Problem
Coding probes for add/search/identity already passed. Several graph asks still hit `fallback_source` (`NotImplementedError` draft) instead of a verified template: walls and gates (286), as far from land (1162), maximum probability path (1514), number of enclaves (1020), making a large island (827), minimum genetic mutation (433).

## Research
Multi-source BFS from gates/land (LeetCode 286 / 1162), Dijkstra on probability products (1514), border flood for enclaves (1020), island-id union by one flip (827), gene-bank BFS (433). Same self-check pattern as Cycle 207 (`examples` + `verify_source`).

## Implementation
- `code_synth_p134.py` — six templates, official example triples, phrase matchers so island-count and knight-probability stay on their existing templates.
- Loader lists `code_synth_p134` first.
- Smoke `code_1036`–`code_1041`.
- `test_p134_gates_enclaves`.

## Result
Unit function `test_p134_gates_enclaves` passed. Chat probe for enclaves returned `def numEnclaves` and Verified. Full smoke eval recorded in the run report.
