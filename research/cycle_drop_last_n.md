# Improvement Cycle — drop_last vs last_n routing (2026-10-09)

## Problem
Smoke eval `code_1679` failed (1728/1729 = 99.94%):
input: "write a function that drops the last n elements"
answer used `def last_n` (keep last n) instead of `def drop_last` (remove last n).
Eval criteria correctly required `def drop_last` and forbade `def last_n`.

## Root cause
- `code_synth_p4.last_n` matched `\blast n\b` including drop language.
- `code_synth_p237.drop_last` explicitly excluded `"last n"` / `"n element"` / `"n item"`.
- Unit tests incorrectly asserted last_n for "drops the last n elements".

## Fix
1. `code_synth_p4.py`: last_n matcher excludes `\bdrop(?:s|ping)?\b|\bwithout the last\b`.
2. `code_synth_p237.py`: drop_last matcher accepts `drop(s|ping)? the last n? (element|item|elements|items)?`.
3. `tests/unit/test_code_synth.py`: four assertions updated last_n → drop_last for drop phrases.

## Validation
- match_template("write a function that drops the last n elements") → drop_last
- returns_last_n / takes_last_n still → last_n
- drop the last element → drop_last
- Orchestrator probe returns Verified drop_last
- test_cycle525 + test_cycle527 pass
- Full smoke: 1729/1729 (100%)

## Result
Correct semantic routing: "drop last n" = remove; "last n" / "return last n" = keep.
