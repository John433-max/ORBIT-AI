# Improvement Cycle — reverse-string conjugated verb

## Problem
Priority 1 coding path: "implement a python function that reverses a string" returned a NotImplementedError stub instead of `reverse_string`. Bare "reverse a string" already matched.

## Research
code_synth_p1 `reverse_string` matcher used `\breverse\b`, which does not match reverses/reversed/reversing. Same gap class as `_widen_loaded` (swap_case, rotate_string).

## Finding
Widen the loaded matcher only. Keep exclusions for words, vowels, integer, LeetCode 344/541, in-place, prefix.

## Implementation
`code_synth.py` `_widen_loaded` name == reverse_string.

## Tests
- synthesize_and_verify: conjugated prompts → reverse_string verified True
- reverse_words, reverseString (344), reverse_string_prefix still win their prompts
- smoke row code_reverse_phrase_1 scored ok

## Benchmark
Before: stub NotImplementedError
After: `def reverse_string` verified against 2 examples
