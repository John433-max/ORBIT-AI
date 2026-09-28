# Cycle 275 — code_synth pack 17 + GH mid-pack parity

Date: 2026-09-28

## Baseline
- doctor: READY (fastapi/uvicorn warning; Ollama optional down)
- smoke: 372/372 prior latest.json; dataset already 378 then 384 after this cycle
- probes: coding → coding_agent verified add(); search → research_agent no live web; identity → ORBIT

## Problem
Highest remaining queue item after passing probes is coding-eval expansion + GitHub pack parity (p2/p3 still local-only due to size; mid packs missing on main).

## Change
- Added `code_synth_p17.py` (relative_ranks, can_three_parts_equal_sum, image_smoother, smallest_range_i, largest_perimeter, surface_area).
- Wired pack into `code_synth.py` loader.
- Smoke +6 coding rows (code_339–code_344).
- All 6 templates `verify_source` ok; matchers unique vs existing packs.

## Result
- templates 369 → 375
- smoke 378 → 384; eval 384/384 coding 344/344
- unit: 69 passed (code_synth + thinking + agents-related)
