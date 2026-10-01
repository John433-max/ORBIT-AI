# Cycle 355: divide matcher must not steal digit-divide prompts

## Problem
CI run 36939498839 (Cycle 352, commit 608654bc) failed `tests/unit/test_code_synth.py` because GitHub `code_synth_p1.py` was the 12KB stub. Cycle 354 (0e2dcc4) restored pack parity and CI 36941002424 succeeded.

Residual: GH `divide` still matches any "divid… two" phrase and only excludes the literal "leetcode 2520". Prompt "count the digits that divide the number 2520" can still lose to `divide`.

## Change
`code_synth_p1.py` divide matcher requires a word boundary after the two-number pattern and excludes "2520" (not only "leetcode 2520"), plus existing "digits that divide" / "count_digits" guards.

## Tests
Local `tests/unit/test_code_synth.py`: 116 passed.
Probe: add → `def add` Verified; fusion search → honest no-live-web; identity → ORBIT.
