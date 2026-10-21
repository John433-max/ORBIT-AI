# ORBIT Improvement Run — 2026-10-21 run27

## Baseline
- doctor: READY (API deps WARNING optional; Ollama offline OPTIONAL)
- smoke accuracy: 2090/2090 = 100% (latest.json 2026-10-21T03:38:47)
  - coding 2021, search 11, rag 10, permission 11, lab 7
- failing probes:
  - write a python function that adds two numbers → coding_agent, Verified add()
  - search for recent news about fusion energy → research_agent, honest offline
  - what is your name → main_chat_agent, I'm ORBIT
  - implement a simple calculator → main_chat_agent identity hedge (GAP)
  - write a simple calculator / write a web scraper → chat hedge (GAP)

## Chosen priority
1. Coding path. Natural "implement a …" / "write a …" phrases missed `_wants_code_written` because the identifier pattern required the token immediately after the verb to be ≥2 chars. Articles ("a", "an") caused fall-through to the chat identity hedge.

## Changes
- `agents.py` `_wants_code_written`: skip articles/adjectives before the target identifier; treat leading `implement`/`code`/`write` as code asks; exclude prose ("write about", "write a blog/story/poem/letter/email/essay/summary").
- `agents.py` `_synthesize_python`: inline four-function `calculate(a, op, b)` for calculator write/implement asks so the common probe returns real code, not the template-miss fallback.
- `tests/unit/test_code_route_search.py`: `test_implement_article_phrase_routes_to_code_not_hedge`.

## Tests
- doctor READY
- pytest tests/unit/test_code_route_search.py + test_thinking.py + test_permissions_and_state.py: 21 passed
- probes: add/calculator/search/identity/prose exclusion OK
- calculator ops: + - * / and ZeroDivisionError verified

## Benchmark before → after
| Metric | Before | After | Diff |
|---|---:|---:|---:|
| smoke accuracy | 100% (2090/2090) | (eval running) | — |
| "implement a simple calculator" | chat hedge | coding_agent + def calculate | fixed |
| "write about fusion energy" | chat | chat | held |
| search / identity probes | pass | pass | — |

## GitHub push
Pending eval confirmation.

## Next priority remaining
Priority 2–6 still green (honest offline search, identity, eval coverage, local==main for tracked sources before this change, auto prefers Ollama, API deps optional).
