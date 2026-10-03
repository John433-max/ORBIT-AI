# Cycle GH-parity p124–p125 [2026-10-03]

## Problem
GitHub main (1889aa0) stopped at code_synth_p123. Local already had p124 (and p125 landed during this run). Smoke on main ended at code_983.

## Probes
- coding "write a python function that adds two numbers" → coding_agent, verified `add`
- search fusion energy → research_agent, honest no live web
- identity → main_chat_agent, "I'm ORBIT"

## Validation
- doctor READY (PyYAML / fastapi / Ollama optional)
- prior full eval 1023/1023 (2026-10-03T22:09:03Z)
- smoke code_984–code_995 scored ok 12/12 via Orchestrator + score_row
- test_p124_triangle_tag_neighbor_rope_squares passed

## Push
code_synth_p124.py, code_synth_p125.py, loader entries, smoke.jsonl, tests/unit/test_code_synth.py
