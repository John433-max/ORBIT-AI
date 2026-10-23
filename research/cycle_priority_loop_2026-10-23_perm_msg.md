# ORBIT Improvement Run — 2026-10-23 permission message precision

## Baseline
- doctor: READY (API deps WARNING optional; Ollama OPTIONAL)
- smoke: 2105/2105 accuracy 1.0 (evals/results/latest.json 2026-10-23T02:11:24)
- probes: coding real Verified code; search honest no-live-web; identity ORBIT

## Chosen priority
Permission path quality (adjacent to coding + permission eval). Deny message only mentioned destructive wipe/rm; sensitive path reads (`cat /etc/passwd`, private keys) used the same text.

## Changes
- `agents.py` and `thinking.py`: `DENY_FS_MSG` now says "destructive or sensitive filesystem access" and lists `/etc/passwd` and private keys alongside wipe/rm examples.
- Still contains the substring `Permission denied` so existing smoke permission rows stay green.

## Tests
- probes: coding / search / identity / cat /etc/passwd / delete / read id_rsa — all correct
- pytest tests/unit/test_permissions_and_state.py + test_thinking.py + test_code_route_search.py: 28 passed

## Benchmark before → after
- smoke accuracy: 1.0 → 1.0 (message-only change)
- no latency change intended

## GitHub push
Pending focused commit of agents.py + thinking.py only (no secrets).

## Next priority remaining
GitHub parity hygiene / optional serve deps already documented; further eval rows only if a new weak path appears.
