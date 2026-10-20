# Cycle: CI failure on f9fec90 + document routing polish

## Problem
CI run 39333846655 (commit f9fec90) failed unit tests (core) because agents.py was a minimal stub (Orchestrator only returned "I'm ORBIT.", agents=object). Subsequent merge 4141e89 restored the full routing surface.

## Local baseline
- doctor: READY (API deps optional)
- unit (core excl code_synth): 78 passed, 1 skipped
- probes:
  - write a python function that adds two numbers → coding_agent + real code
  - search for recent news about fusion energy → research_agent, honest "No live web"
  - what is your name → main_chat_agent, ORBIT identity
  - summarize the documents → was chat hedge; now document agent honest empty

## Change
agents.py route regex: added `\bsummarize (the )?documents?\b` so empty-RAG asks hit DocumentAgent before chat/research.

## Tests
- After edit: document probes route correctly
- test_provider_fallback + test_thinking: 13 passed

## GitHub
Original failure on stub commit; full agents.py already on main via 4141e89. Local polish not yet pushed.

## Next
- Confirm latest CI green on full agents.py
- Optional: push the summarize-the-documents matcher
