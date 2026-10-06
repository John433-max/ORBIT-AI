# Cycle 462 — geometry / text helpers that still missed

## Problem
Smoke was 1362/1362 and coding/search/identity probes passed, but several natural-language "write a function" asks still fell through `match_template` (rotate point, cartesian→polar, hashtags, mask last four, days in month, Catalan).

## Implementation
- `code_synth_p180.py` — 6 verified templates, loaded before p179 so catalan/days-in-month do not hit factorial or leap-year stubs.
- `code_synth.py` — pack list includes `code_synth_p180` first.
- `evals/datasets/smoke.jsonl` — `code_1325`–`code_1330`.

## Benchmark
Smoke 1362/1362 → 1368/1368 (coding 1317 → 1323). New rows code_1325–code_1330 verified.

