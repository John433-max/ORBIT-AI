# Cycle 507 — coding steals and prefix/duplicate drafts

## Problem
Natural-language coding asks that should return a verified function were either
matched to a broader template or fell through to the NotImplemented draft:

- "sum of squares" → `sum_list`
- "cartesian product" → `list_product`
- "vowels and consonants" → `count_vowels`
- "words of each length" → `count_words`
- "prefixes of a string" → fallback
- "consecutive duplicates" → fallback

## Research
Template routers should prefer the more specific phrase when a broad matcher
already covers a token (sum, product, count, word). This is the same
specificity rule already used in `match_template` (Cycle 283), but the broad
matchers never excluded the distinctive tokens, so the specific template never
existed to win.

## Implementation
- `code_synth_p223.py`: six verified templates.
- Matcher exclusions: `square` on `sum_list`, `cartesian` on `list_product`,
  `consonant` on `count_vowels`, `length` on `count_words`.
- Loader registers `code_synth_p223` first.
- Smoke `code_1600`–`code_1605`.

## Validation
Unit: `test_p223_squares_cartesian_prefixes_not_stolen`,
`test_all_templates_verify`, add probe. Orchestrator routes the squares ask
to `coding_agent` and returns `sum_of_squares` verified against 3 examples.
