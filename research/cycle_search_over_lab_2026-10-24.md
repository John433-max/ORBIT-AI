# Improvement Cycle — search intent over lab topic keywords

Date: 2026-10-24

## Problem
Explicit research asks containing lab curriculum keywords (e.g. "look up who invented the transformer architecture") routed to LabAgent instead of ResearchAgent, because `_looks_like_lab` / `_is_lab` matched "transformer" before search verbs were considered.

## Research
Priority queue #2: search / look up / news about must hit ResearchAgent with honest no-live-web when offline.

## Finding
Classify/route order: code → (was lab) → search. Lab topic regex includes `transformers?`, `(self-)?attention`, `neural network`, so any "look up … transformer" became lab.

## Implementation
- `thinking.py` `Thinker.classify`: return `"search"` immediately after code, before lab checks.
- `agents.py` `Orchestrator._route`: run Priority-2 research regex before broad `_looks_like_lab`; require conceptual lab path not to match search verbs.

## Files Changed
- thinking.py
- agents.py

## Tests
- pytest tests/unit/test_thinking.py test_code_route_search.py test_provider_fallback.py: 26 passed
- Manual probes 8/8 (coding, search×2 including transformer look-up, chat identity, lab conceptual, docs, memory)

## Benchmark before → after
| Case | Before | After |
|---|---|---|
| look up who invented the transformer architecture | lab_agent (educational hedge) | research_agent (honest no live web) |
| search for recent news about fusion energy | research_agent | research_agent (unchanged) |
| what is a transformer | lab_agent | lab_agent (unchanged) |
| write a python function that adds two numbers | coding_agent | coding_agent (unchanged) |
| what is your name | main_chat_agent ORBIT | main_chat_agent ORBIT (unchanged) |

## Result
Search intent wins over lab topic keywords; educational conceptual asks stay on lab.

## Next priority remaining
GitHub parity push of thinking.py + agents.py; model provider defaults (Ollama when healthy); serve/deps docs.
