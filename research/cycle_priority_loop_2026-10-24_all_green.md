# Priority loop 2026-10-24 — all-green baseline

## Baseline
- doctor: READY (2 non-blocking: fastapi/uvicorn missing, Ollama connection refused)
- smoke: 2114/2114 accuracy 1.0
  - coding 2032, search 18, permission 12, rag 11, math 9, lab 9, …
- tinylm_lab: available=True, regression_ok=True
- ModelProvider: tinylm checkpoint preset=rope (Ollama optional offline)

## Probes
| Prompt | Agent | Result |
|--------|-------|--------|
| write a python function that adds two numbers | coding_agent | real `add` + Verified |
| implement a function to reverse a string | coding_agent | real `reverse_string` + Verified |
| search for recent news about fusion energy | research_agent | honest no-live-web |
| look up transformer architecture | research_agent | honest no-live-web |
| search the documents for orbit | document | empty RAG message |
| what is your name | main_chat_agent | I'm ORBIT… |

## Changes this run
- No functional code change required (priorities 1–3 already green).
- Git: merged diverged tinylm/regression commit (022e362 ↔ ecffd28) with origin; only research note wording differed.

## GitHub
- Local main ahead of origin by merge commit; content already on origin via ecffd28.
- agents.py / thinking.py line counts match origin (995 / 689).

## Next priority remaining
1. Serve/deps — optional: document or CI-install fastapi/uvicorn (doctor already WARNING only).
2. Model provider — prefer Ollama when healthy (already auto; TinyLM educational fallback).
3. Further eval rows only if new failure modes appear.
4. Keep GitHub agents.py/thinking from PLACEHOLDER regressions (CI history).
