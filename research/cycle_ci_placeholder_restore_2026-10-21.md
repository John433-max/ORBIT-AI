# ORBIT Improvement Run — CI PLACEHOLDER restore + perm smoke IDs

## Baseline
- doctor: READY (API deps warning optional; Ollama offline optional)
- smoke accuracy: 2101/2101 = 100% (coding 2029, search 11, rag 10, permission 14, lab 7, …)
- failing probes: none (local)
- CI failure on commit 1bd16d5: agents.py/thinking.py replaced with PLACEHOLDER (11 B) → unit tests exit 2

## Chosen priority
GitHub parity / CI recovery (queue #4). Root cause of failed run 39677407425 was accidental truncation of agents.py + thinking.py to PLACEHOLDER on the security-deny commit.

## Changes
1. Confirmed origin/main already restored via 93fe76e (full agents.py/thinking.py, 30949/24423 B) + cd08527 docs.
2. Local security patterns present: `_is_destructive_fs` covers `delete the file /…`, `read the file /etc/…`, `cat …id_rsa`.
3. Fixed duplicate smoke IDs: new rows renumbered perm_12–perm_14 (were colliding with existing perm_9/perm_11).
4. Unit: tests/unit/test_thinking.py + test_permissions_and_state.py + tests/security → 26 passed.

## Tests
- doctor READY
- destructive FS helper: True for delete/read/cat sensitive paths; False for "write a function that deletes…"
- pytest security/thinking/permissions: 26 passed
- smoke eval: 2101/2101 (100%)

## Benchmark before → after
| Metric | Before (bad CI commit) | After (restored main) |
|---|---:|---:|
| agents.py size | 11 B PLACEHOLDER | 30949 B |
| thinking.py size | ~PLACEHOLDER | 24423 B |
| smoke accuracy (local) | n/a | 2101/2101 100% |
| permission rows | 11 unique | 14 unique (perm_12–14) |

## GitHub push
YES — smoke ID fix + this research note (after restore already on main).

## Next priority remaining
1. Confirm CI #752/#753 green on restored agents
2. Coding/search/identity probes remain green
3. Optional: serve extras / fastapi CI install docs
