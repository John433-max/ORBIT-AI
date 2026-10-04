# Cycle 430 — search "for … in" stolen by code route; creator identity web-fell-through

## Problem
`search the web for today's weather in tokyo` scored code at 1.0 because ROUTES treated English `for … in` as a Python for-loop (`for .* in`). Non-thinking `Orchestrator.handle` exec'd the sentence and failed on the apostrophe in `today's`, then appended a search. `who created you` missed the identity pattern, hedged, and the question fallback returned Bible verses about Jacob.

## Research
Existing ORBIT rule (instruction smoke + `_is_self_identity`): name/identity stays on chat, not web. Code route should match syntax, not English prepositions. Tie-break already prefers earlier ROUTES entries, so a false code hit beat research.

## Implementation
- `agents.py` code pattern: `for \w+ in` (still matches `for i in range`).
- Explicit search/look-up/news wins a code/research score tie.
- Identity patterns include who created/made/built you.
- MainChatAgent returns a fixed ORBIT-runtime creator reply (no web).
- smoke `search_3`, `instruction_5`.

## Tests
Probes: weather routes research_agent (no sandbox error); who created you stays ORBIT and does not mention Jacob; add-two-numbers still coding; `for i in range` still code.
