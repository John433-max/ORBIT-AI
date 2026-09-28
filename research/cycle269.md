# Improvement Cycle 269

## Problem
Coding coverage still growing locally; GitHub missing packs p5–p12. `sort_list` stole "relative sort array".

## Implementation
- `code_synth_p12.py`: matrix_reshape, di_string_match, relative_sort_array, add_to_array_form, common_chars, projection_area.
- Loader includes p12.
- `sort_list` excludes `relative`.
- Smoke code_309–code_314.

## Tests
- pytest test_code_synth + thinking + agents: 102 passed
- smoke 348/348 → 354/354 (coding 308 → 314)

## Result
Templates 339 → 345. All six new rows Verified.
