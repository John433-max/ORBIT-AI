# ORBIT Improvement Run — 2026-10-20

## Baseline
- doctor: READY (2 non-blocking: fastapi/uvicorn missing; Ollama connection refused)
- smoke accuracy: 1.0 (2083/2083) — coding 2021, search 9, rag 6, permission 10, lab 7 all 1.0
- probes:
  - coding ("write a python function that adds two numbers") → real `def add` + Verified
  - search ("search for recent news about fusion energy") → honest "No live web"
  - identity ("what is your name") → "I'm ORBIT..."
  - RAG empty ("summarize the document") → "No documents loaded..."
  - coding variants (sort/binary_search/fibonacci) → real code + Verified

## Chosen priority
All of priority queue 1–6 currently green on local + origin/main @ c09962b.
- Coding path routes to code agent / code_synth (Verified)
- Research/search honest offline message
- Eval already expanded (coding + search + RAG-empty + permission)
- GitHub agents.py / thinking.py / code_synth.py sizes match origin/main
- Model provider auto: Ollama when healthy → TinyLM → Echo
- Serve deps: requirements-api.txt + SETUP.md document optional fastapi/uvicorn; doctor WARNING only

## Changes
None required this run (no failing probe). Documented baseline + confirmation.

## Tests
- tests/unit/test_provider_fallback.py + test_thinking.py: 13 passed
- test_code_route_search + test_permissions_and_state + test_doctor_api_deps: 8 passed

## Benchmark before → after
Unchanged (already 1.0 smoke; no code change).

## GitHub push
NO (main already in parity; research notes only local this cycle)

## Next priority remaining
- Optional: install fastapi/uvicorn in CI for serve smoke (still non-blocking)
- Optional: more Easy code_synth packs if GH pack parity incomplete
- Keep agents.py out of accidental PLACEHOLDER truncate on future CI restores
- When Ollama is available in env, verify auto-preference switches off TinyLM
