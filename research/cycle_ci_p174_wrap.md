# Cycle CI-p174 wrap/harmonic

Date: 2026-10-05

## Problem
GitHub Actions Tests run 37412323848 (commit 9ce481c) failed unit tests:

- `wraps text to a width` did not match `word_wrap` (GitHub p165 matcher only had `wrap text` / `word wrap` / `wrap words`).
- `harmonic mean of a list` matched `average` because the mean+list regex fires and no `harmonic_mean` template existed.
- p174 also asked for `unix_to_iso`, `iso_to_unix`, `one_hot`, `quantile`, `population_variance`, `singularize`, `parse_duration`, which were missing or stolen by the unix→ISO matcher.

## Change
- `code_synth_p165.py`: match `wraps text`, `word-wrap`, and `text to a width`.
- `code_synth_p174.py`: add the missing phrase-gated templates; keep unix→ISO from matching the reverse direction.
- `code_synth_p1.py`: average matcher excludes harmonic/geometric/population/quantile.

## Tests
`test_p171`, `test_p172`, `test_p174`, `test_p175` — 4 passed.

## Next
Push p165, p174, p1. Remaining: coding/search probes vs full eval if doctor is green.
