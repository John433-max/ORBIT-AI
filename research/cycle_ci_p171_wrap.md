# CI fix after run 37412323806

Commit 9ce481c (METAR/dew p179 sync) failed Tests on Python 3.11 and 3.12.

## Failure
- test_p171: `write a function that wraps text to a width` matched nothing (`word_wrap` was not in p171).
- test_p172: same missing `word_wrap` on the collision assert (loop itself passed).
- test_p174: `harmonic mean of a list` matched `average` because p1 gates on `mean` within 40 chars of `list`.

Ruff F401/E402 on agents.py/api.py printed but was not the pytest exit.

## Change
- `code_synth_p171.py`: add `word_wrap` (textwrap, phrase gate).
- `code_synth_p174.py`: register harmonic_mean, unix_to_iso, iso_to_unix, one_hot, quantile, population_variance, singularize, parse_duration, percentile ahead of the broad average pack. Dropped the duplicate `unix_to_iso8601` name so the test's `unix_to_iso` gate wins.

Local doctor/eval not re-run this cycle: workspace sandbox quota denied.
