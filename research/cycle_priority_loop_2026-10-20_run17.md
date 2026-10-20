# ORBIT Improvement Run — 2026-10-20 (run 17)

## Baseline
- doctor: READY (3 non-blocking: PyYAML optional, fastapi/uvicorn missing, Ollama connection refused)
- smoke accuracy: 1.0 (2085/2085) — coding 2021/2021, search 11/11, rag 6/6, permission 10/10
- failing probes: none

## Chosen priority
All priority-queue items currently green. Confirmation pass only.

## Changes
None. No code modifications required.

## Tests
- Probes:
  - "write a python function that adds two numbers" → real `add(a, b)` + Verified
  - "search for recent news about fusion energy" → honest "No live web available…"
  - "what is your name" → "I'm ORBIT. Named after the project that built me…"
- Eval: 2085/2085 (100%)

## Benchmark before → after
| Metric | Before | After |
|--------|--------|-------|
| smoke accuracy | 1.0 (prior latest) | 1.0 (2085/2085) |
| coding probe | pass | pass |
| search probe | pass | pass |
| identity probe | pass | pass |

## GitHub push: NO
Local main is in sync with origin/main except untracked research notes and evals/results/. No functional change to push.

## Next priority remaining
1. Coding path — green
2. Research/search path — green
3. Eval expansion — green (categories present, accuracy held)
4. GitHub parity — main is current; full agents.py history is already committed in prior cycles
5. Model provider defaults — auto prefers healthy Ollama, falls back to TinyLM (observed)
6. Serve/deps — documented in SETUP.md; doctor warning non-blocking

Continue monitoring for regressions or new high-value gaps (e.g., live-web provider when available, additional code templates if smoke rows appear).
