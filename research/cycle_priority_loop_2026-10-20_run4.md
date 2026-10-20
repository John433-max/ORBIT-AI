# ORBIT Improvement Run — 2026-10-20 run4

## Baseline
- doctor: READY (3 non-blocking: PyYAML optional, fastapi/uvicorn warning, Ollama optional/refused)
- smoke accuracy: 1.0 (2083/2083) from evals/results/latest.json (2026-10-20T02:13:21Z)
- by_category: coding 2021/2021, search 9/9, rag 6/6, permission 10/10, lab 7/7, all others 1.0
- failing probes: none
  - "write a python function that adds two numbers" → coding_agent, code_synth, Verified
  - "search for recent news about fusion energy" → research_agent, honest offline message
  - "what is your name" → main_chat_agent, "I'm ORBIT..."

## Chosen priority
All ordered priorities 1–3 green. Proceeded to #4 GitHub parity: local was ahead 1 (docs-only commit 580e9b6).

## Changes
None to runtime. Confirmed existing routing in agents.py:
- `_wants_code_written` routes write/implement/python function to CodeAgent + code_synth
- ResearchAgent returns offline message when no live web
- Identity stays on MainChatAgent

## Tests
- doctor: READY
- eval: 100% (not re-run this cycle; prior latest.json 2083/2083)
- probes: 3/3 pass
- unit: pytest unavailable in env; no new failures introduced

## Benchmark before → after
No code change. Accuracy remains 1.0. Probes remain correct.

## GitHub push: YES
- Pushed 580e9b6 (docs/research notes from prior confirm runs) to origin/main
- df436db..580e9b6

## Next priority remaining
5. Model provider defaults — Prefer Ollama when healthy (currently optional/refused; TinyLM is active educational fallback).
6. Serve/deps — Document/CI install for fastapi/uvicorn (doctor already treats as optional warning).

## Notes
No runtime regression. ORBIT remains a modular local agent runtime (model + tools + RAG + memory + agents), not a large-scale foundation model.
