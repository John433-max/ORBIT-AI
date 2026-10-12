# Improvement Cycle — bridges template test alignment (2026-10-12)

## Problem
`tests/unit/test_code_synth.py::test_p248_aho_corasick_and_bridges` failed:
`find bridges in undirected graph` → `find_bridges` but test expected `critical_connections`.

## Root cause
p274 added a dedicated `find_bridges` template (Tarjan low-link) that correctly owns
generic "find bridges" / "tarjan bridges" / "bridges in undirected graph" phrases.
`critical_connections` remains for LeetCode 1192 "critical connection(s)" phrasing.
The older p248 test still asserted the pre-p274 mapping.

## Change
Update `test_p248_aho_corasick_and_bridges` expected names to `find_bridges` for
generic bridge phrases; keep/add `critical connections in a network` → `critical_connections`.

## Files
- tests/unit/test_code_synth.py

## Tests
- test_p248_aho_corasick_and_bridges PASS
- test_p274_classic_greedy_dp PASS

## Probes (unchanged)
- coding add-two-numbers → verified `add`
- find bridges → `find_bridges` synthesis
- search fusion → research results
- identity → ORBIT

## Benchmark
- doctor: READY (API deps optional; Ollama optional)
- smoke/eval prior: 1862/1862 (100%)
- unit: fixed 1 failure in code_synth suite

## GitHub
- Attempted push of full test_code_synth.py failed (payload size); intermediate
  commit 87e08a69 left PLACEHOLDER, then 11ce5682 left a temporary stub.
- **Local source of truth**: `tests/unit/test_code_synth.py` (6416 lines, p248 fixed).
  Restore full file to GH main in a follow-up with chunked push or authenticated upload.
- agents.py / thinking.py already match main (byte-equal content).
