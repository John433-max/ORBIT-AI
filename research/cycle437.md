# Improvement Cycle 437

## Problem
Smoke search_3 (`search the web for today's weather in tokyo`) failed. ResearchAgent correctly refused live web, but the user-facing line did not echo the query, so expect_contains `Tokyo` missed. Coding and identity probes already passed.

## Research
Honest offline search should still name the attempted subject (query echo). Title-casing the query surfaces proper nouns without inventing weather.

## Implementation
`_offline_search_reply(note, query=None)` appends `Asked: <Query.Title()>.` when the query is not already in the reply. ResearchAgent.run passes the request. Generic failure notes still omitted (Cycle 357).

## Tests
- doctor: READY (PyYAML, fastapi/uvicorn, Ollama optional)
- probe weather: contains `Tokyo`; fusion still honest no-live-web; identity ORBIT; add() verified
- eval: 1218/1219 (99.92%, search 2/3) → 1219/1219 (100%, search 3/3)

## Benchmark
| Metric | Before | After |
|---|---|---|
| smoke | 1218/1219 | 1219/1219 |
| search | 2/3 | 3/3 |

## Next
Serve extras still optional (fastapi/uvicorn warning). Ollama still down; TinyLM is the live fallback.
