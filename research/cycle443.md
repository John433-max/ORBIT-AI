# Improvement Cycle 443

## Problem
`code_synth_p161` was local-only. Its `remove_punctuation` matcher required `remove` and missed `removes`, so `test_p161_interleave_digit_unique_swap_punct_pairs` failed. `digit_sum` also stole LeetCode-style "alternating digit sum" (smoke code_602) because the pack loads first.

## Implementation
- Match `removes|strips|drops` as well as `remove|strip|drop`.
- Exclude `alternat` from `digit_sum` so `alternate_digit_sum` keeps code_602.
- Publish pack, loader entry, smoke code_1204–code_1209, and the unit test.

## Validation
Local p161 unit test passed. Orchestrator smoke rows code_602 and code_1204–code_1209 passed (coding_agent, Verified).
