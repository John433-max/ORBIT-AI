# Cycle 382 — code_synth p104

## Problem
Coding probes already returned verified functions, but several Easy asks still fell through to the NotImplemented stub.

## Research
Loader keeps the first template name (Cycle 244 packs). Re-declaring `number_of_lines` / `large_group_positions` in a newer pack shadowed p19/p18 and dropped smoke rows code_347 and code_353 (902/902 → 906/908).

## Implementation
- `code_synth_p104.py`: reverse_only_letters (917), max_number_of_balloons (1189), slowest_key (1629), replace_elements_right (1299). Examples match published samples.
- Loader lists p104 before p103.
- Did not redeclare 806/830; existing phrases already cover them.
- Smoke code_863–code_868.

## Tests
- `test_p104_lines_groups_letters_balloons_slowest_replace` pass
- `test_all_templates_verify` pass
- eval 902/902 → 908/908 (coding 862/862 → 868/868)

## Rejected
Duplicating p18/p19 names in p104. First-name wins, stricter matcher, smoke regression.
