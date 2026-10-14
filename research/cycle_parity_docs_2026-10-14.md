# Improvement Cycle — GitHub parity: document inventory routing

## Problem
Local agents.py / thinking.py had document-inventory routing ("what documents do you have")
and stronger honest-RAG-empty stickiness that were not yet on origin/main.

## Changes
- agents.py: DocumentAgent inventory path + route regex for list/what documents
- thinking.py: classify docs before broad search; honest RAG phrases keep answer

## Tests
- test_agents.py + tests/unit/test_code_route_search.py: 42 passed
- doctor READY; smoke 2060/2060
- probes: coding real function; search live fusion news; identity ORBIT;
  "what documents do you have" → Loaded documents list

## Result
Keep. Push focused parity files only.
