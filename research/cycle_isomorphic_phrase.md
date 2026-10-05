# Improvement cycle — isomorphic phrase match

## Problem
`implement a function to check if two strings are isomorphic` missed `isomorphic_strings` and fell through to a NotImplemented draft. Smoke only covered the phrase "isomorphic strings".

## Finding
Existing template in `code_synth_p3.py` required `\bisomorphic strings?\b`. Natural "strings are isomorphic" does not match that order. Word-pattern prompts do not contain that phrase, so widening is safe.

## Implementation
- Matcher also accepts `strings? (are|is) isomorphic`.
- Unit case in `test_cycle260_easy_string_dp`.
- Smoke row `code_1194`.

## Validation
- `synthesize_and_verify` verified True, 3 examples.
- Chat probe returns `def isomorphic_strings` and Verified.
- Word-pattern prompt still does not select this template.
