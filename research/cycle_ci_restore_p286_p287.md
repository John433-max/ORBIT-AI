# ORBIT Improvement Run — CI restore PLACEHOLDER packs p286/p287

Date: 2026-10-15

## Problem
GitHub Actions Tests failed on main (run 38670074253, commit c5dfaee docs parity;
also Cycle 631 dd818fe still failed unit tests).

Root cause: `code_synth_p286.py` and `code_synth_p287.py` on origin/main were
stub files containing only `PLACEHOLDER_WILL_REPLACE`. Unit test
`test_p287_pagerank_kmeans_bwt_tortoise_lz77_hits` expects real templates.

## Chosen priority
GitHub parity / CI green — restore real local packs without secrets.

## Implementation
Push local full `code_synth_p286.py` and `code_synth_p287.py` to main.

## Local verification
- synthesize_python: page_rank, k_means, burrows_wheeler_transform,
  tortoise_hare, lz77_compress, hits_algorithm, newton_interpolation OK
- doctor READY; coding/search/identity probes OK
- Cycle 631 packs p337/p338 already on main for GPTQ/AWQ/GQA/MMR/L2

## Next
Confirm Tests workflow green after this push; re-run full smoke eval.
