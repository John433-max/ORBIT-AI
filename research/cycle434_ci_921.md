# Cycle 434 — CI Tests failure on LeetCode 921 name collision

## Problem
GitHub Actions Tests run 37239136825 (commit 7a17ad3) failed on 3.11 and 3.12.

## Failure
`tests/unit/test_code_synth.py::test_p103_circular_similar_ends_fish_lunch_parens_teemo`

Prompt `minimum add to make parentheses valid leetcode 921` matched p154 `min_add_to_make_valid` (loader checks newer packs first). The p103 test still required `def min_add_parentheses`. Result: 1 failed, 244 passed, 2 skipped.

## Fix
Alias `min_add_parentheses` to `min_add_to_make_valid` in `code_synth_p154.py` so both the p103 needle and the p154 name assertion hold. Examples still run against the first callable (`min_add_to_make_valid`).

## Tests
- `test_p103_...` passed
- `test_p154_elimination_parens_ramp_tokens_boats_fleet` passed
- doctor: READY (PyYAML, API deps, Ollama optional)
