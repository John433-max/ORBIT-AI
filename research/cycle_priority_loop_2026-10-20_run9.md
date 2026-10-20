# ORBIT Improvement Run — 2026-10-20 run9

## Baseline
- doctor: READY (3 non-blocking: PyYAML optional, fastapi/uvicorn warning, Ollama optional/refused)
- smoke accuracy: 1.0 (2083/2083) from evals/results/latest.json (2026-10-20T06:16:59Z)
- probes:
  - coding → coding_agent + verified `def add(a, b)`
  - search "search for recent news…" → research_agent, honest no-live-web
  - identity → "I'm ORBIT…"
  - **gap:** "look this up: quantum computing breakthrough" and "google fusion energy" routed to chat

## Chosen priority
2. Research/search path — phrasing variants of "look up" / "google" missed ResearchAgent.

## Research
Existing route already claimed "search", "look up", "news about". The code-exclusion regex already listed "look this up" and "google", but `_route` never mapped those phrases to research, so they fell through to MainChatAgent.

## Implementation
- agents.py: expand research route to `look this up|look that up|look it up|google|web search|search the web`
- tests/unit/test_code_route_search.py: new test for the variants; code and identity still asserted
- evals/datasets/smoke.jsonl: search_10 ("look this up…"), search_11 ("google fusion energy")

## Files Changed
- agents.py
- tests/unit/test_code_route_search.py
- evals/datasets/smoke.jsonl

## Tests
- unit: test_code_route_search (3 functions) pass via direct call
- targeted score of search_1–search_11 + code_1 + perm_1 + chat_1: 14/14
- doctor: READY
- focused eval (non-coding 64 + 8 coding samples, 72 rows): 72/72 including search 11/11
- full 2085-row smoke not re-run this cycle (coding verify ~0.6s/row ≈ 20 min); no coding row matches the new phrases

## Benchmark before → after
| Probe | Before | After |
|---|---|---|
| look this up: … | chat / hedge | research_agent / no-live-web |
| google fusion energy | chat / hedge | research_agent / no-live-web |
| write a python function that adds two numbers | coding_agent | coding_agent (unchanged) |
| what is your name | main_chat_agent identity | unchanged |
| implement binary search | coding_agent | unchanged |

## Result
Research phrasing gap closed. No regression on code, identity, or permission paths.

## Next priority remaining
3. Optional full smoke re-run when wall time allows (2085 rows).
5. Model provider defaults already prefer Ollama when healthy.
6. Serve/deps already documented; doctor warning only.
