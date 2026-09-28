# Improvement Cycle 257

## Problem
GitHub `code_synth_p1.py` is 12 098 B / ~24 templates. Local pack is 47 705 B / 68 templates
(`add` … `lis`). Smoke on main already includes coding rows past `is_prime`. Missing p2/p3
still skip via the lazy loader, but mid-eval coding rows need the full p1.

## Research
Local doctor READY; smoke 269/269 (coding 242/242). Probes:
- write a python function that adds two numbers → coding_agent + Verified
- search for recent news about fusion energy → research_agent
- what is your name → main_chat_agent ORBIT identity

## Implementation
Push full local `code_synth_p1.py` to GitHub main. No local behavior change.

## Files
- code_synth_p1.py (68 templates)
- research/cycle257.md

## Tests
- doctor: READY (fastapi/uvicorn warning, Ollama optional)
- smoke: 269/269
- probes pass as above

## Next
Push `code_synth_p2.py` then `code_synth_p3.py`. Do not overwrite GH thinking.py with a placeholder.
Do not overwrite slim GH agents.py with the 80 KB local file until CI-safe slim-parity is prepared.
