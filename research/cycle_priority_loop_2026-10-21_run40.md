# ORBIT Improvement Run 40 — 2026-10-21

## Baseline
- doctor: READY (PyYAML optional, API deps WARNING, Ollama OPTIONAL down)
- smoke accuracy: 1.0 (2101/2101) prior full; targeted 128/128 key/dict+sample; non-coding 69/69; coding sample 80/80
- probes:
  - coding add → coding_agent, `def add` Verified
  - search fusion news → research_agent, honest "No live web available"
  - identity → main_chat_agent, "I'm ORBIT…"
  - delete-key (before this cycle) → coding_agent but wrong `def dict_keys`

## Chosen priority
1. Coding path quality: delete/remove/pop a key from a dict was stolen by dict_keys.

## Changes
Remote already landed the template+matcher (13523bc). This run adds the
eval row and unit test that commit noted as local-only:
- evals/datasets/smoke.jsonl: code_delete_key_1
- tests/unit/test_code_synth.py: test_delete_key_not_dict_keys

## Tests
- match: delete/remove/pop → delete_key verified; keys-of-dict → dict_keys
- targeted smoke (key/dict + category sample): 128/128
- random coding sample: 80/80
- non-coding smoke: 69/69
- probes coding/search/identity/FS-deny still pass

## Benchmark before → after
| Metric | Before | After |
|---|---|---|
| delete-key ask | dict_keys (wrong) | delete_key Verified |
| smoke coverage of delete-key | missing | code_delete_key_1 |
| unit coverage | missing on main | test_delete_key_not_dict_keys |

## GitHub push
YES — smoke row + unit test on top of 13523bc.

## Next priority remaining
Priorities 1–6 green. Optional: full smoke re-run (slow, ~1s/row), more
template quality fixes, fastapi extras.
