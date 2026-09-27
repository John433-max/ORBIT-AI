# Improvement Cycle 236

## Problem
Coding coverage still growing; GitHub `code_synth.py` remains ~32 templates vs local 156.

## Research
LeetCode-style tree/BST primitives (min depth, kth smallest BST, right side view, sorted array → BST, zigzag level order, range sum BST) are common "write a function" asks and fit existing `[val, left, right]` tree encoding.

## Implementation
- Added 6 templates to `code_synth.py` (156 total).
- Tightened `max_depth` (exclude min) and `level_order` (exclude zigzag).
- `sorted_array_to_bst` examples match mid=`(lo+hi)//2`.
- Smoke + unit rows code_136–code_141.

## Tests
- `pytest tests/unit/test_code_synth.py test_agents.py` → 70 passed
- smoke eval recorded in this run

## GitHub
Full `code_synth.py` (~160KB) still not on main (`b4b534cd`, ~32 templates). Slim `agents.py` kept for CI. Next: push full `code_synth.py` + smoke + tests when the push payload fits.

## Next
GitHub parity for `code_synth.py`, fastapi serve extras, or restore numpy/torch from `_bc.pyc`.
