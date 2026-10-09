# Cycle eval search expand — 2026-10-09

## Baseline
- doctor: READY (API deps warning; Ollama optional offline)
- smoke: 1729/1729 accuracy 1.0 (~241s)
- probes: coding → real function + Verified; search → honest no-live-web; identity → ORBIT

## Chosen priority
Eval expansion (priority 3) — search honesty rows were thin (4).

## Changes
- Appended `search_5` (inertial confinement fusion research)
- Appended `search_6` (google news SPARC tokamak)
- Schema matches existing search rows: expect_any live-or-honest, expect_not_contains toy-scale hedge

## Tests
- Targeted OrbitAI.chat: 4/4 PASS (search_5, search_6, coding add, identity)
- Classify: code / search / chat correct

## Benchmark
| Metric | Before | After |
|--------|--------|-------|
| smoke n | 1729 | 1731 |
| targeted probes | 4/4 | 4/4 |
| coding path | real code | real code |
| search path | honest offline | honest offline |

## Result
Keep. No regression risk on existing rows.

## Next
GitHub parity push of smoke.jsonl if desired; model provider auto already prefers Ollama when healthy; serve deps documented.
