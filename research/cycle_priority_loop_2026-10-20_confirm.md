# ORBIT Improvement Run — 2026-10-20 (confirm green)

## Baseline
- doctor: READY (2 non-blocking: API deps fastapi/uvicorn missing, Ollama connection refused)
- smoke accuracy: 2083/2083 = 1.0 (coding 2021, search 9, rag 6, permission 10, …)
- failing probes: none

## Probes (OrbitAI.ask)
1. "write a python function that adds two numbers"
   → real code + Verified (`def add(a, b): …`)
2. "search for recent news about fusion energy"
   → honest "No live web available in this environment…"
3. "what is your name"
   → "I'm ORBIT. Named after the project that built me…"

## Chosen priority
None of priorities 1–6 failing. Coding, research/search, eval expansion, GitHub CI surface, provider defaults, and serve/deps docs are all satisfied.

## Changes
None. Confirmed current main CI agents.py (slim ~22KB) routes correctly; fuller local copies under /home/workdir/artifacts/agents*.py remain local-only and are not required for green probes/smoke.

## Tests
- doctor READY
- probes green
- latest.json accuracy 1.0

## Benchmark before → after
No code change. Accuracy remains 1.0.

## GitHub push: NO
main tracks origin/main; only untracked generated evals/results/ and local working copies.

## Next priority remaining
- Optional: add a few more edge-case smoke rows (RAG-empty variants, permission phrasing) if new failure modes appear
- Optional: CI job that installs requirements-api.txt when testing serve
- Keep full local agents.py out of main until a deliberate CI-compatible merge is planned
- Continue only if a regression appears in coding/search/identity
