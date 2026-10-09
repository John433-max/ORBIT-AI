# ORBIT Improvement Run — paper lookup routes to search

Date: 2026-10-09

## Problem
`find recent papers on fusion energy` classified as `statement` and returned stored memory (EvalBot / project deadline) instead of ResearchAgent.

## Research
SOURCE: local `thinking.py` `_is_search` (ORBIT Thinker)
TECHNIQUE: extend lookup cues (`find recent/latest`, `papers on/about`) before the short-statement memory path.
WHAT IT IMPROVES: research/search routing for paper and news asks that do not say "search" or "look up".
TRADE-OFFS: a bare "find recent …" phrase is now search, not memory. Code templates still win because `_is_code` runs first (`find the duplicate number` stays code).

## Implementation
- `thinking.py` `_is_search` matches find-recent/latest and papers/articles on/about.
- unit assert in `tests/unit/test_thinking.py`.
- smoke `search_7` forbids memory hedge and requires fusion or honest offline.

## Probe
`find recent papers on fusion energy` → live fusion research snippets, not memory.
