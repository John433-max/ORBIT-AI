# Cycle GH parity p87–p96

Date: 2026-10-02

## Problem
GitHub `main` loader stopped at `code_synth_p92` and was missing pack files
`code_synth_p1c.py`, `p87`–`p91`, and `p93`–`p96`. Smoke on main was behind
the local 859-row set.

## Change
Push those packs, the loader entries, matching unit tests, and `smoke.jsonl`.
No secrets. Agents/thinking unchanged (already same size as main).

## Local check
- doctor: READY
- eval: 859/859 accuracy 1.0
- probes: add-two-numbers returns verified `def add`; fusion search honest no-live-web; identity ORBIT
- pack `verify_source`: 0 failures on the pushed packs
