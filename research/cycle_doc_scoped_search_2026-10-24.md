# Improvement Cycle — document-scoped search stays local

## Problem
CI run 40049234885 failed on commit 7be0a24 ("fix(route): explicit search verbs beat lab topic keywords") because the push wrote agents.py and thinking.py as PLACEHOLDER (pytest exit code 2 on import). Restore commit f9b4474 put the real files back on main.

The routing change itself had a real regression: the research early-return was placed before the document/RAG check, so "search from the documents" and "search the documents" hit ResearchAgent instead of DocumentAgent (honest empty-RAG). The comment in agents.py even said document should win for that phrase.

## Research
- Routing order: explicit search verbs must beat lab topic keywords ("look up who invented the transformer" → research, bare "what is a transformer" → lab).
- Document-scoped asks ("search from/the documents", inventory) must stay on the local DocumentAgent path so RAG-empty returns the honest "no documents loaded" message instead of a web-search miss.

## Implementation
- agents.py: move the document/RAG match before the research early-return; add "search/look/query the documents" to the document pattern.
- thinking.py: exclude document-scoped asks from the search early-return so classify still reaches the docs path.
- tests/unit/test_code_route_search.py: cover search-over-lab vs document-scoped.

## Tests
- tests/unit (excl. code_synth): 96 passed, 1 skipped
- Probes: coding → real add(); search → honest no-live-web; identity → ORBIT

## Result
Document-scoped search stays local; lab keywords still lose to explicit search verbs; identity stays ORBIT.
