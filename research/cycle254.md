# Improvement Cycle 254

## Problem
Smoke eval coding collapsed to 3/236 (overall 30/263 = 11.41%). `code_synth_p3.py` had an unclosed list (`SyntaxError`). Loader only caught `ImportError`, so pack load aborted.

## Implementation
1. Closed the `return [` list in `code_synth_p3.py` (local).
2. `code_synth._templates` now `except Exception` so one bad pack is skipped.

## Tests
pytest synth+thinking+agents: 91 passed. Smoke 263/263 after local p3 close.

## Next
Push p1/p2/p3 packs to GitHub without overwriting slim agents.py.
