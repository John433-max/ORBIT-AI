# Improvement Cycle 312

## Problem
Coding coverage still grows one Easy pack at a time. Prefix-count prompts collided with `count_words`.

## Research
Continue deterministic template packs + HumanEval-style examples. Tighten overlapping matchers rather than add a second router.

## Implementation
- `code_synth_p50.py`: check_string, capitalize_title, divide_string, count_even, prefix_count, minimum_sum
- Loader lists p50
- `count_words` excludes `prefix`
- smoke code_537–code_542

## Tests
- test_code_synth 86 passed
- doctor READY
- smoke 582/582 (coding 542/542)
- probes coding/search/identity still pass

## Next
GitHub pack parity (p49/p50), slim agents.py, fastapi extras.
