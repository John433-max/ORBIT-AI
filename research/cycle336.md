# Improvement Cycle 336

## Problem
GitHub missing many code_synth packs; local coding coverage can still grow with unused Easy templates.

## Implementation
- Added `code_synth_p72.py` (6 unused Easy templates).
- Loader lists p72.
- Smoke +6 coding rows (code_674–679).

## Tests
- doctor READY
- smoke 713/713 → 719/719 (coding 673→679)
- synthesize_and_verify 6/6

## Next
Push remaining missing GH packs (p2/p3/p28–p32/p44/p47/p49/p53+).
