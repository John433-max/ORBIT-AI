# Cycle 252 — LFU / sliding-window max / burst / word-search II / median stream

Date: 2026-09-27

## Problem
Coding coverage stopped at Cycle 251 (234 templates, smoke 246).
GitHub still lacks full p2/p3 packs (payload too large for one contents
push); local coding path can still grow with design/hard DP templates.

## Implementation
Added 5 verified templates to `code_synth_p3.py`:
- lfu_cache (class hidden as `_LFUCache` so verify picks the driver)
- sliding_window_maximum
- burst_balloons
- word_search_ii (does not steal plain word_search)
- median_finder

## Tests
- test_cycle252_* unit
- smoke 246/246 → 251/251 (coding 219 → 224)
- pytest test_code_synth 45 passed

## GitHub
Pushed `research/cycle251.md` (218bb2e). Did not overwrite agents.py.
Full p1/p2/p3 still local-only (~47/88/132 KB).
