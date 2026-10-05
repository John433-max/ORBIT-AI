# Improvement Cycle 442

## Problem
CI run 37262147378 (commit c6c3f761) failed both Python 3.11 and 3.12 on
`tests/unit/test_code_synth.py::test_p160_copy_longest_filter_query_order_none`.

Assertion: `('write a function that capitalizes each word', None)`.

The p160 pack shipped deep_copy / longest_word / filter_even / parse_query /
equal_ignore_order / drop_none, but the unit test also requires title_case,
reverse_words, and camel_to_snake. Those names exist in older packs that are
not all published, and p160 is loaded first, so GitHub returned None.

## Research
Matcher order is first-hit across packs (`code_synth.py` loads p160 before p1).
A missing template cannot be rescued by a later unpublished pack.

## Implementation
Added three templates to `code_synth_p160.py`:
- title_case — "capitalizes each word" / title case
- reverse_words — reverse word order (does not exclude the word "string")
- camel_to_snake — camel-to-snake or "snake_case" + convert, not snake-to-camel

## Tests
- test_p160 and test_subseq word-reverse: pass
- tests/unit/test_code_synth.py: 188 passed
- smoke eval: 1240/1240

## Next
Confirm CI on the follow-up commit.
