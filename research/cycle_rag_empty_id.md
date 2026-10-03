# Improvement Cycle — honest RAG-empty for any document id

## Problem
`summarize document #99` was in smoke, but only forbade wikiHow. DocumentAgent returns `ok=False` with `I couldn't find document #N`. Thinker rejected every failed docs step, so missing ids fell through to the generic "solid answer" hedge (probe: document #42).

## Research
Same pattern as the search path: an honest negative tool result is the answer, not a signal to continue (ORBIT thinking.py search no-live-web branch).

## Implementation
`thinking.py`: keep docs / docs_check replies that say the document is missing or none are loaded, even when `ok` is false. Stop instead of searching or hedging.

## Files
- thinking.py
- tests/unit/test_thinking.py
- evals/datasets/smoke.jsonl (rag_empty_2, rag_empty_3)

## Tests
- unit: test_think_keeps_honest_missing_document
- probes: #42 / #99 / #7 return "I couldn't find document #N."
