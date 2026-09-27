# Improvement Cycle 235

## Problem
Coding path locally strong, but GitHub `code_synth.py` (~32 templates) lags
local. Also wanted next graph/grid templates (rotting oranges / Pacific-Atlantic).

## Chosen priority
Eval expansion + coding templates (queue 3), then document GH parity gap.

## Implementation
Six new templates (150 total):
- rotting_oranges (copies grid; BFS minutes / -1)
- pacific_atlantic
- flood_fill ("flood fills" matcher)
- update_matrix (01-matrix nearest zero)
- num_provinces
- surrounded_regions

Smoke rows code_130–135.

## Tests
pytest tests/unit/test_code_synth.py test_agents.py: 69 passed

## Benchmark
| Metric | Before | After |
| smoke | 148/148 | 154/154 |
| coding | 129/129 | 135/135 |

## GitHub
Full 160KB code_synth not uploaded this run (connector size). Note only.

## Next
Push full code_synth.py + smoke + tests; then agents.py parity.
