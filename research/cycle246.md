# Cycle 246 — burst balloons / word search II / cooldown stock

Date: 2026-09-27

## Problem
Coding coverage after Cycle 245 stopped at 210 templates / 195 coding eval rows.
GitHub `code_synth.py` is still the 18 KB monolith (~32 templates).

## Change
Added 6 templates in `code_synth_p3.py`:
- burst_balloons (LC 312)
- word_search_ii (LC 212; word_search excludes II)
- palindrome_partition (is_palindrome excludes partition)
- serialize_tree
- count_smaller
- max_profit_cooldown (max_profit excludes cooldown)

## Tests
- pytest test_code_synth + test_thinking + test_agents: 85 passed
- smoke 222/222 → 228/228 (coding 195 → 201)

## GitHub
Push slim `code_synth.py` loader + p1/p2/p3 packs + smoke + unit test.
Do not overwrite slim remote `agents.py`.
