# ORBIT Improvement Run 39 — 2026-10-21

## Baseline
- doctor: READY (API deps WARNING, Ollama OPTIONAL)
- smoke/eval: accuracy 1.0 (2101/2101)
- probes: coding / search (honest no-live-web) / identity ORBIT — all pass
- Priorities 1–6 from the queue: coding, search, eval, GH PLACEHOLDER guard, auto→Ollama-then-TinyLM, serve docs/CI — already green

## Chosen priority
Coding-path quality: "delete a key from a dict" was matched by dict_keys (returned list(d.keys())).

## Changes
- code_synth_p408.py: new `delete_key` template (copy+pop, original unchanged)
- code_synth_p232.py: dict_keys matcher requires "keys" (plural) and excludes delete/remove/pop/drop
- evals/datasets/smoke.jsonl: code_delete_key_1 row (local; push with next batch if needed)
- tests/unit/test_code_synth.py: test_delete_key_not_dict_keys (local)

## Tests
- test_delete_key_not_dict_keys PASS
- test_coding_delete_function_not_denied PASS
- CLI probe returns def delete_key + Verified

## Benchmark before → after
| Metric | Before | After |
|---|---|---|
| delete-key ask | dict_keys / wrong | delete_key Verified |
| keys-of-dict ask | dict_keys | dict_keys (unchanged) |
| Eval accuracy | 1.0 (2101) | +1 smoke row local |

## GitHub push
Focused template + matcher + research note.

## Next
Push smoke/unit row when practical; keep provider auto + serve optional path documented.
