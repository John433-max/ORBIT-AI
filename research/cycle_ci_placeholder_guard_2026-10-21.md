# ORBIT Improvement Cycle — CI PLACEHOLDER guard (2026-10-21)

## Trigger
Workflow run Tests failed on commit 1bd16d5
(https://github.com/John433-max/ORBIT-AI/actions/runs/39677407382)
Title: fix(security): expand destructive-FS deny for path/file reads

## Root cause
Commit 1bd16d5 replaced `agents.py` and `thinking.py` with the literal
string `PLACEHOLDER` (762 / 650 lines deleted). Import and unit tests
failed with SyntaxError / missing symbols.

## Recovery (already on main)
- 93fe76e: restore full agents.py/thinking.py
- cd08527: docs research note; probes 100%

Security path patterns from the intended 1bd16d5 change are present in
the restored files.

## This cycle
Add regression tests so PLACEHOLDER corruption fails CI immediately:

- `test_agents_thinking_not_placeholder`
- `test_destructive_fs_deny_path_reads` (delete the file /…, /etc/shadow, .ssh)
- `test_coding_delete_function_not_denied` (code path not blocked)

## Baseline
- doctor: READY (API deps optional warning, Ollama optional)
- smoke: 2098+/2098 accuracy 1.0
- probes: coding real def; search honest no-live-web; identity ORBIT
- security suite: 13 passed

## Result
3 new tests pass; full security 13 pass; probes ok. No runtime change.

## Next priority
Eval expansion / keep coding+search green; optional full agents.py parity
on GitHub remains lower priority while CI surface works.
