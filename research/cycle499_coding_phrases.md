# Improvement Cycle 499

## Problem
Natural-language coding asks missed existing templates and returned no verified function:

- "counts items matching a rule" (LeetCode 1773) — matcher only accepted "count items"
- "asteroids collisions" — matcher only accepted singular "asteroid collision"
- "string can be obtained by rotating another" (LeetCode 796) — no template; left-rotate-by-k must stay separate

## Research
LeetCode 796: goal is a rotation of s iff lengths match and goal is a substring of s+s.
Source: https://leetcode.com/problems/rotate-string/ (standard rotation check).

## Implementation
- Widened `count_items_matching` and `asteroid_collision` matchers.
- Added `can_rotate_to` in `code_synth_p215.py` (loader first).
- Smoke rows code_1549–code_1551 and unit test `test_p215_rotate_goal_and_phrase_aliases`.

## Tests
- unit function passed
- subset score of new rows + add / left-rotate / identity (see run log)

## Result
Those three asks now return verified functions. Left-rotate-by-k still maps to `rotate_string`.
