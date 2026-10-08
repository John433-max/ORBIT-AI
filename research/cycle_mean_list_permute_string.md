# Improvement Cycle — mean-of-list route + string permutations

## Problem
Coding path returned the wrong function for "mean of a list" (`average(a, b)`), and "permutations of a string" fell through to NotImplemented. List permute explicitly excludes "string". mean_list excluded the phrase "mean of a list" and only matched "average".

## Implementation
- `code_synth_p228.py` mean_list matches mean/average of a list, array, or numbers, excluding two/pair and specialized averages.
- `code_synth_p1.py` average matches only two/2, and rejects list/array.
- `code_synth_p235.py` permute_string; registered first in `code_synth.py`.
- Smoke `code_1669`–`code_1671`.

## Tests
Slice eval of new rows plus average-of-levels, max average, geometric mean: 6/6.
OrbitAI.ask returns mean_list / permute_string / average, not the hedge.
