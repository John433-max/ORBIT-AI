# Cycle 523 — line count, tabs, vowel, indices, list rotation, inclusive sum

## Problem
Six natural-language coding asks returned NotImplemented drafts:

- number of lines in a string
- replace tabs with spaces
- starts with a vowel
- indices of a value
- two lists are rotations of each other
- sum of a range inclusive

## Research
HumanEval-style self-check (already in Cycle 207): a template is kept only if tiny examples pass. Phrase matchers must load before broader packs (`rotate_string`, `is_even`) so they do not steal string rotation or even-checks.

## Implementation
- `code_synth_p234.py`: `line_count`, `tabs_to_spaces`, `starts_with_vowel`, `indices_of`, `is_list_rotation`, `inclusive_range_sum`
- Loader prefers `code_synth_p234`
- Smoke `code_1663`–`code_1668`
- `test_cycle523_lines_tabs_vowel_indices_rotation_range` also guards `rotate_string` and `is_even`

## Tests
- Unit function passed (pytest unavailable; invoked directly)
- CodeAgent probes for the six asks return Verified sources

## Next
GitHub parity for p234 + smoke rows. Zip-three lists still misses.
