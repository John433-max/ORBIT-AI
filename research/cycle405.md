# Cycle 405 — bare problem titles routed to verified templates

## Problem
Titles such as "minimum rounds to complete all tasks" matched no write/implement cue, so Thinker treated them as statements and CodeAgent exec'd them (syntax error → hedge).

## Research
ORBIT already self-checks templates (Cycle 207). The miss was routing, not generation. LeetCode 1433 / 1886 / 2047 / 2264 / 2405 / 2244 had no template.

## Implementation
- `code_synth_p151.py` (6 templates, examples verified)
- loader lists `code_synth_p151` first
- `_is_code` and `_wants_code_written` treat a template hit as code unless the ask is a search or a question
- smoke `code_1138`–`code_1143`

## Result
Those six asks return verified functions. Add, identity, and fusion search unchanged.
