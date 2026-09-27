# Cycle 233 — GitHub code_synth parity

Date: 2026-09-27

## Problem
Local coding path is complete (138 templates, smoke 142/142 coding 123/123).
GitHub `code_synth.py` still stopped at the early ~32-template set while
`evals/datasets/smoke.jsonl` on main already lists later coding rows.
CI/eval on a clone would fail those extra coding cases.

## Change
Push local tested files:
- code_synth.py (138 templates, synthesize_and_verify)
- evals/datasets/smoke.jsonl (142 rows)
- tests/unit/test_code_synth.py
- research/cycle233.md

agents.py remains local-full (75KB) vs GH slim — next parity target.

## Tests
doctor READY
eval 142/142
pytest test_code_synth + test_agents + test_thinking: 72 passed
probes: coding sandbox + Verified; search research_agent; identity ORBIT
