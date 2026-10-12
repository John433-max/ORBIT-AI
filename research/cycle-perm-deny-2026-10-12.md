# Improvement Cycle — Permission denial expansion

## Problem
Clear destructive filesystem requests ("delete the system files", "wipe everything", "cat /etc/passwd") missed the narrow `_is_destructive_fs` / ROUTES file pattern and fell through to main_chat, producing the generic toy-scale hedge instead of an explicit Permission denied.

## Research
Existing pattern already denied `rm -rf`, "delete all files", "wipe the disk", "format the hard disk". Expanding the same regex (still gated by `_is_code` so "write a function that deletes…" stays on the coding path) is the smallest compatible change.

## Implementation
- thinking.py `_is_destructive_fs`: added patterns for "delete the system files", "wipe/destroy/erase everything|all files", and sensitive `/etc/passwd` reads.
- agents.py ROUTES file pattern: same expansion so Orchestrator.route sends them to FileAgent (which already calls the shared deny helper).

## Files Changed
- thinking.py
- agents.py
- evals/datasets/smoke.jsonl (+5 rows: perm_5–7, search_8, rag_empty_4)

## Tests
- Manual probes: new destructive asks → file_agent + Permission denied; coding/search/identity probes unchanged.
- Full smoke eval after the change (see latest.json).

## Result
Permission path now returns a clear refusal for a broader set of destructive and sensitive-file asks without regressing coding or search.

## Next Research Target
GitHub parity for code_synth.py loader (local includes p280/p281; remote loader starts at p279) and any remaining slim-file gaps.
