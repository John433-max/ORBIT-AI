# Improvement Cycle 442

## Problem
GitHub Tests run 37262147374 on c6c3f76 failed (3.11 and 3.12):
`test_p160_copy_longest_filter_query_order_none` AssertionError
`('write a function that capitalizes each word', None)`.
p160 and the unit test were published; matcher widenings in p1/p2/p4 were not.

## Implementation
- title_case also matches "capitalize(s/d) each word".
- reverse_words also matches "reverses words …".
- camel_to_snake matches snake_case phrasing and excludes dict asks.
- is_even excludes filter phrasing so "filters even numbers" stays on filter_even.

## Expected
Same unit test passes on CI. No new templates.
