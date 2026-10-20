# ORBIT Improvement Run — 2026-10-20 (priority loop, second confirm)

## Baseline
- doctor: READY (PyYAML optional warning, API deps fastapi/uvicorn warning, Ollama connection refused)
- smoke accuracy: 2083/2083 = 1.0 (fresh eval 2026-10-20_021321_eval.json, 459s)
- by_category: coding 2021/2021, search 9/9, rag 6/6, permission 10/10, lab 7/7, math 9/9, science 5/5, chat 5/5, instruction 5/5, memory 3/3, tool_selection 2/2, hallucination 1/1
- failing probes: none

## Probes (OrbitAI.chat)
1. "write a python function that adds two numbers"
   → agent=coding_agent, real code `def add(a, b): return a + b` + Verified.
2. "search for recent news about fusion energy"
   → agent=research_agent, honest "No live web available in this environment…"
3. "what is your name"
   → agent=main_chat_agent, "I'm ORBIT. Named after the project that built me…"

## Chosen priority
None of priorities 1–6 failing.
- Coding path routes to coding_agent and returns real code.
- Research/search path routes to research_agent with honest no-live-web.
- Eval already covers coding/search/RAG-empty/permission; accuracy remains 1.0.
- GitHub: HEAD df436db == origin/main (docs commit already pushed).
- Provider auto: Ollama if healthy, else TinyLM (Ollama down here, TinyLM correct).
- Serve/deps: doctor treats missing API deps as warning; CI installs requirements-api.txt.

## Changes
None. Confirmed green baseline; no regression to fix.

## Tests
- doctor READY
- probes green
- eval 2083/2083 accuracy 1.0

## Benchmark before → after
No code change. Accuracy remains 1.0 (previous latest.json also 1.0).

## GitHub push: NO
main tracks origin/main at df436db. Only untracked: evals/results/, agents_ci_compact.py, prior research notes.

## Next priority remaining
- All listed priorities green.
- Watch for regressions in coding/search/identity.
- Optional: additional edge-case smoke rows only if new failure modes appear.
- Optional: keep full local agents.py out of main until deliberate CI-compatible merge.
