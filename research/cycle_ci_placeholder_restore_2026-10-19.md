# Improvement Cycle: CI agents.py PLACEHOLDER restore

Date: 2026-10-19

## Problem
GitHub Actions Tests run 39333627001 failed (exit 2) on commit 9b9afeb.
Root cause: agents.py on main was replaced with the literal string
`PLACEHOLDER_WILL_FAIL` (later `PLACEHOLDER_WILL_REPLACE` at 5f37629).
pytest collection then fails (EOF/syntax), exit code 2.

## Finding
Remote agents.py was 24 bytes of placeholder text. Local CI surface
(589 lines) already has:
- coding route → real sandbox/code_synth output
- research route → honest "no live web"
- identity → ORBIT (not web)
- document/RAG before research → honest empty-doc message

## Implementation
Restored full local agents.py onto origin/main (5f37629).

## Tests
- test_provider_fallback + test_code_route_search: 3 passed
- Probes: code / research / chat / document all correct

## Result
CI collection should succeed again. Coding, search honesty, identity,
and empty-doc paths preserved.
