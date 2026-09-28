# Cycle 261 — GitHub pack-4 + loader parity

Date: 2026-09-28

## Baseline
- doctor: READY (fastapi/uvicorn warning; Ollama optional refused)
- smoke: 306/306 (coding 266/266)
- probes: coding_agent add(); research_agent fusion news; identity ORBIT
- GitHub main @ bc2e254: code_synth.py loads p1/p1b/p2/p3; only p1+p1b files exist
- Local templates: 297 unique (p1 68 + p1b 12 + p2 68 + p3 135 + p4 27)

## Problem
Remote coding path only ships ~80 templates. Local p2/p3/p4 never landed on main.

## Change this cycle
- Ship `code_synth_p4.py` (27 verified templates).
- Loader includes `code_synth_p4` after p3 (missing pack still skipped).
- Did not overwrite GitHub `agents.py` / `thinking.py` (local still ahead).

## Next
Push `code_synth_p2.py` (68) then `code_synth_p3.py` (135) in size-limited commits.
