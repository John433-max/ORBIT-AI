# CI PLACEHOLDER restore 2026-10-24

## Problem
Tests workflow run 40049234879 (commit 7be0a24) failed in ~21s.
agents.py and thinking.py on main were replaced with the string "PLACEHOLDER"
(0 lines of real code). Subsequent docs commit b497663 left them truncated.

## Cause
The "fix(route): explicit search verbs beat lab topic keywords" push on
origin/main truncated both files instead of applying the small routing diff.

## Fix
Restored full CI-surface agents.py (995 lines) and thinking.py (679 lines)
from local commit 1f0c3bf, which already contained the correct search-over-lab
routing change on top of the full files.

## Verification
- route("look up who invented the transformer") → research
- route("what is a transformer") → lab
- route("write a python function…") → code
- route("search for recent news…") → research (honest no-live-web)
- route("what is your name") → chat (ORBIT identity)
- unit: test_provider_fallback + test_thinking + test_code_route_search +
  test_offline_static_facts → 30 passed

## Push
f9b4474 fix(agents): restore full agents.py + thinking.py after PLACEHOLDER truncation
