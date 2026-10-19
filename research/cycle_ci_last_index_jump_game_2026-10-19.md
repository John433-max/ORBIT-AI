# Cycle CI: last_index vs jump_game_ii (2026-10-19)

## Problem
CI Tests run https://github.com/John433-max/ORBIT-AI/actions/runs/39292274638
(commit 186045e) failed on `tests/unit/test_code_synth.py::test_p144_bfs_maze_home`:

```
AssertionError: assert 'last_index' == 'jump_game_ii'
```

Prompt: `"jump game ii minimum jumps to last index"` matched `last_index` instead of `jump_game_ii`.

## Root cause
`code_synth_p213.py` template `last_index` used:

```python
lambda low: "last index" in low and "first" not in low
```

That substring matches LeetCode 45 phrasing ("minimum jumps to last index").
`match_template` ranks by score but only upgrades when score >= best + 2;
`last_index` scored 2.0 and appeared first, `jump_game_ii` scored 3.0 (+1) so it lost.

## Fix
Narrow `last_index` matcher to exclude jump-related prompts:

```python
lambda low: (
    "last index" in low
    and "first" not in low
    and "jump" not in low
    and "jumps" not in low
)
```

Legitimate asks ("last index of a value") still match `last_index`.

## Validation
- `match_template("jump game ii minimum jumps to last index").name == "jump_game_ii"`
- `match_template("write a function that returns the last index of a value").name == "last_index"`
- `pytest tests/unit/test_code_synth.py::test_p144_bfs_maze_home` → pass
- Probes: coding / search (honest no-live-web) / identity (ORBIT) ok
- Smoke latest.json: 2083/2083 accuracy 1.0

## Files
- `code_synth_p213.py` (matcher only)
