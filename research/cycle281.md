# Cycle 281 — code_synth pack 23 + GitHub mid-pack parity

Date: 2026-09-29

## Baseline
- doctor: READY (fastapi/uvicorn warning, Ollama optional)
- smoke: 414/414 (coding 374/374)
- templates: 405
- probes: coding sandbox + Verified; search live/news; identity ORBIT

## Problem
Local coding/search/identity already pass. Highest remaining queue item is GitHub pack parity (missing p9/p10/p11/p16/p18/p19/p22) plus eval expansion.

## Change
- Added `code_synth_p23.py`: tictactoe_winner, num_equiv_domino_pairs, distance_between_bus_stops, day_of_the_year, check_straight_line, count_negatives.
- Wired pack into `code_synth.py` loader.
- Smoke +6 coding rows (code_375–code_380).
- All 6 templates `synthesize_and_verify` ok.

## Result
- templates 405 → 411
- smoke 414 → 420; eval 420/420 coding 380/380
- unit: test_code_synth + test_thinking + test_agents 109 passed
