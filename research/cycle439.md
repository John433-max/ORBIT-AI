# Improvement Cycle 439

## Problem
Natural-language coding asks for dictionary helpers fell through to the NotImplemented draft (`write_a_python_function_that_merges_two`). Priority-1 coding path, not the toy-scale hedge, but not real code.

## Research
Existing packs already cover count_words, flatten, chunk_list, and title_case. No template matched merge/invert/zip/sorted-by-value dictionary phrasing. Mechanism: phrase-gated templates loaded first, with negative filters so merge-intervals and alien-dictionary stay on their packs.

## Implementation
- `code_synth_p158.py`: merge_dicts, keys_sorted_by_value, invert_dict, zip_to_dict. Each self-checks two examples.
- `code_synth.py`: load p158 first.
- Smoke `code_1190`-`code_1193`. Unit `test_p158_merge_invert_zip_sorted_keys`.

## Tests
- unit function: PASS
- chat probes: four asks return def and Verified; identity still ORBIT

## Benchmark
| Metric | Before | After |
|---|---|---|
| merge two dictionaries | NotImplemented draft | merge_dicts, verified |
| invert / zip / keys-by-value | NotImplemented draft | verified templates |
| smoke | 1219/1219 | 1230/1230 |
| coding | 1174/1174 | 1185/1185 |
