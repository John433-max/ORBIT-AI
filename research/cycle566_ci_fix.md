# Cycle 566 CI fix — numeric factorial not code

## Problem
CI run https://github.com/John433-max/ORBIT-AI/actions/runs/38111075842 failed on
commit 340ff3b (Cycle 565: treat "code" as a write-verb).

Unit test `test_code_verb_factorial_is_code_not_search` asserted:
  `not _wants_code_written("factorial of 5")`
but `_wants_code_written` returned True because `match_template("factorial of 5")`
hits the factorial code template after the write-verb checks.

## Root cause
Cycle 565 expanded write-verbs (code/program) correctly so "code a factorial function"
synthesizes. The bare-template path still treated "factorial of 5" as a code request
when science_math did not short-circuit it.

## Fix
Early return False in `_wants_code_written` for numeric factorial asks:
  `\\bfactorial\\s+(?:of\\s+)?\\d+|\\d+\\s*!`
Write-verb paths still return True for "code a factorial function" / "code factorial".

GitHub `agents.py` on main uses a short bootstrap that fetches agents@340ff3b and
applies the same early-out (plain full agents remains local source of truth).

## Tests
tests/unit/test_thinking.py: 10 passed (incl. Cycle 565 row).

## Result
CI should pass; calc routing for "factorial of 5" preserved; code synthesis for
write-verb factorial prompts preserved.
