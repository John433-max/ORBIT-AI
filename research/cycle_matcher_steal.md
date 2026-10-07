# Cycle: matcher steal fix (p210 / p211 / p214)

Date: 2026-10-07

## Problem
Smoke 1574/1580 (99.62%). Six coding rows missed because newer packs stole older asks:

- `is_subset` matched any "subset" (`subsets`, `subsets_ii`)
- `number_lines` treated "line" as a substring, so "linearly" and "number of lines to write" hit it
- `all_equal` in p211 required "all equal" (missed "all items are equal") and stole LeetCode 3576 "to all equal elements"; the p207 matcher was dropped by the name-dedupe loader

## Change
- p214 `is_subset`: require a subset check, exclude power-set / duplicates phrasing
- p210 `number_lines`: word-boundary `lines`, exclude interpolation / widths / "number of lines"
- p211 `all_equal`: accept "all items are equal", exclude transform / leetcode / make-equal
- Restored CI `_widen_loaded` for swap_case / chunk_list / rotate_string (main 7bdb051) while keeping p208–p214 in the loader

## Benchmark
| Metric | Before | After |
|---|---:|---:|
| smoke | 1574/1580 (99.62%) | 1580/1580 (100%) |
| coding | 1529/1535 | 1535/1535 |

Doctor stayed READY. Identity / search / add probes unchanged.
