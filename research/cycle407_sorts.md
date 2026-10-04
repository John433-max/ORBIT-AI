# Improvement Cycle 407

## Problem
Coding asks for merge sort, quicksort, a stack class, and CSV line parsing returned `NotImplementedError` drafts from `fallback_source` instead of runnable code.

## Research
Merge sort and Lomuto quicksort are standard divide-and-conquer sorts (CLRS). A list-backed stack matches the usual ADT. Quoted CSV fields follow the simple RFC 4180 case (comma delimiter, doubled quotes). No new dependency.

## Implementation
`code_synth_p131.py` templates: `merge_sort`, `quick_sort`, `stack_class` (`stack_demo` + `Stack`), `parse_csv_line`. Matchers exclude merge-sorted and min-stack. Loader registers `code_synth_p131` first.

## Tests
Template self-check verified. Prior merge-sorted prompt still hits `merge_sorted`. Smoke rows code_1016–1019.

## Benchmark
Before: those four probes returned draft stubs (not Verified).
After: chat returns verified source for all four.
