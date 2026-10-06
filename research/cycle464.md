# Improvement Cycle 464

## Problem
Local coding coverage for box IoU, L2 normalize, chunk string, weighted mean, Heron area, and UUID5 (Cycle 463) was not on GitHub main. `code_synth_p181.py` 404'd. Smoke on main stopped at `code_1330`. Repeat-request match cache was local-only.

Priority probes (add-two-numbers, fusion search, identity) already passed. Stale `latest.json` still listed `code_1294` (`unix_to_iso8601`); current matcher returns that name and verifies.

## Research
GitHub contents API: main tree has packs through `code_synth_p180` (180 pack files). Local loader lists `code_synth_p181` first. Smoke ids on main are a strict prefix of local (1368 vs 1374).

## Finding
Push the already-tested pack and the small `match_template` memo (256 entries, cleared on template reload). Do not replace slim `agents.py`.

## Implementation
- Add `code_synth_p181.py` on main.
- Update `code_synth.py` loader + `_MATCH_CACHE`.
- Append smoke rows `code_1331`–`code_1336`.
- Append `test_p181_iou_l2_chunk_weighted_heron_uuid5` to the GitHub unit file (not a full overwrite).

## Files Changed
- code_synth.py
- code_synth_p181.py
- evals/datasets/smoke.jsonl
- tests/unit/test_code_synth.py
- research/cycle464.md

## Tests
- `test_p181_iou_l2_chunk_weighted_heron_uuid5` PASS (direct call)
- Six new asks + unix_to_iso8601: verified True

## Benchmark
Recorded after GitHub push and local eval in the run report.

## Result
Kept locally. GitHub push attempted in this cycle.

## Next Research Target
Cold first-match is still ~120 ms. Annotate matchers with required tokens, or keep GitHub pack parity as new packs land.
