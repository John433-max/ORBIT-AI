# Cycle 358: GitHub parity for honest offline search reply

## Problem
Cycle 357 dropped the generic `search failed` suffix from `_offline_search_reply` locally. GitHub `agents.py` (a941566, 85303 B) still concatenated that note onto the honest sentence.

## Implementation
Pushed the tested local `agents.py` (86155 B). No secrets. Behavior unchanged locally.

## Tests
Local doctor READY. Smoke already 785/785 after Cycle 357. Direct probes: coding returns verified `add`, fusion search returns sources, identity stays ORBIT.

## Result
Remote ResearchAgent now uses the same helper as local.
