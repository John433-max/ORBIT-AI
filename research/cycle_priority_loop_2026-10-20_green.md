# ORBIT Improvement Run — 2026-10-20 (priority loop green)

## Baseline
- doctor: READY (PyYAML optional, API deps optional warning, Ollama connection refused)
- smoke accuracy: 1.0 (2083/2083) from evals/results/latest.json
- probes:
  - coding: real Verified add() function
  - search: honest "No live web available…"
  - identity: "I'm ORBIT. Named after the project that built me…"

## Chosen priority
None failing. Highest remaining was GitHub parity (local ahead 1 docs commit).

## Changes
No runtime code change. Confirmed existing routing, auto provider (Ollama preferred when healthy → TinyLM → Echo), and optional API deps docs already correct.

## Tests
- doctor READY
- probes all green
- smoke 2083/2083 accuracy 1.0

## Benchmark before → after
No code change; accuracy remains 1.0.

## GitHub push
YES — d68b190 docs(research): priority-loop baseline 2026-10-20 + CI agents restore notes
Pushed c09962b..d68b190 to origin/main.

## Next priority remaining
All listed priorities green. Next: watch CI on d68b190; if new coding/search/identity regressions appear, fix routing; otherwise optional eval expansion or serve extras install in CI.
