# ORBIT Improvement Run 42

## Baseline
- doctor: READY (3 non-blocking: PyYAML optional, fastapi/uvicorn warning, Ollama connection refused)
- smoke accuracy: 1.0 (2100/2100, 405s)
- probes: coding add → coding_agent `def add` Verified; search fusion → research honest no-live-web; identity → I'm ORBIT
- failing: "tell me about SPARC tokamak" → generic "How can I help?" hedge

## Chosen priority
Research/search path quality for knowledge asks that lack an explicit search verb.

## Research
- Explicit search verbs already route to ResearchAgent (priority 2 green).
- Question-form unmatched asks ("what is the capital of France") already fall back to research (run 41).
- "tell me about SPARC tokamak" is not a question and not a search verb, so it hit MainChatAgent and returned the generic hedge.
- "write about fusion energy" is required to stay on route=chat (unit contract); the hedge is still weak when no capable model is available.

## Changes
- `agents.py`: route `tell me about X` to ResearchAgent (exclude identity and lab).
- `agents.py`: MainChatAgent treats "tell me about yourself/you" as identity.
- `agents.py`: weak-chat fallback uses `_looks_like_knowledge` so prose/knowledge hedges ("write about …", "tell me about …") prefer research's honest offline note. Route for prose stays chat.
- smoke row `search_tell_about_1`; unit test `test_tell_me_about_routes_to_research_not_hedge`.

## Tests
- unit: test_code_route_search + test_provider_fallback + test_thinking — 22 passed
- probes: tell-me-about SPARC → research no-live-web; yourself → ORBIT; write about → honest note, route chat; coding/search/identity/lab/math/rag/permission unchanged
- targeted eval (all non-coding + 20 coding): 91/91

## Benchmark before → after
| Metric | Before | After |
|---|---|---|
| "tell me about SPARC tokamak" | generic hedge | honest "No live web available…" (research) |
| "write about fusion energy" | generic hedge (route chat) | honest no-live-web (route chat) |
| "tell me about yourself" | hedge | "I'm ORBIT…" |
| targeted smoke | — | 91/91 |
| full smoke (prior) | 1.0 (2100) | +1 search row; non-coding still green |

## GitHub push
pending focused files if credentials allow.

## Next priority remaining
Priorities 1–3 green. Optional: full smoke re-run, fastapi extras already in CI, longer TinyLM persona quality.
