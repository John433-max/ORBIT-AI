# Cycle 440 — coding fallthrough: rotation, word frequency, nested dict

## Problem
- "two strings are rotations" matched the NotImplemented draft.
- "frequency of each word" was stolen by `count_words` (whitespace count) and still verified.
- "flatten a nested dictionary" was stolen by one-level list `flatten`.

## Change
- `code_synth_p159.py`: `is_rotation`, `word_frequency`, `flatten_dict` with two examples each.
- Loader lists p159 before p158.
- `count_words` excludes frequency/freq/histogram.
- list `flatten` excludes prompts containing `dict`.

## Check
- synthesize_and_verify: all three new names verified; count_words and list flatten still match their own asks.
- Smoke rows code_1195–1197 added (1231 → 1234 lines).
