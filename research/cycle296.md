# Improvement Cycle 296

## Problem
Coding eval was 452 templates / 492 smoke. Need more Easy templates with unique matchers.

## Implementation
- `code_synth_p36.py`: shuffle_string, max_power, count_good_rectangles, interpret, busy_student, min_time_to_visit_all_points.
- Tightened local p2 `longest_consecutive` so it does not steal max-power prompts.
- Smoke +6 coding rows (code_453–458).

## Tests
- pytest test_code_synth + test_thinking: 81 passed
- eval 498/498 (coding 458/458)

## Next
Push remaining mid packs (p2/p3/p28–p35) to GitHub; keep slim agents.py on remote.
