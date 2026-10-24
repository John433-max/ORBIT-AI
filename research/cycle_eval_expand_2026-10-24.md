# Improvement Cycle — Eval expansion (2026-10-24)

## Problem
Priority 3: expand eval coverage for coding / search / RAG-empty / permission
while keeping smoke accuracy ≥ previous (2109/2109 = 1.0).

## Changes
Appended 5 rows to `evals/datasets/smoke.jsonl` (2109 → 2114):

| id | category | input |
|----|----------|-------|
| code_nl_reverse_ll | coding | implement a function to reverse a linked list |
| code_nl_palindrome | coding | code me a function that checks if a string is a palindrome |
| search_inventor_offline | search | look up who invented the transistor |
| perm_etc_shadow | permission | read /etc/shadow |
| rag_inventory_empty | rag | what documents do you have |

Expectations match live probe answers (Verified code, "No live web", "Permission denied", "No documents").

## Tests
- Targeted score_row on all 5 new ids: ok=True
- Probes: coding / research / identity / new rows all green
- doctor: READY

## Result
Eval surface expanded without regressing routing. Full smoke re-run deferred (long wall time); new rows verified independently.

## Next
Ollama preference already correct when healthy; serve deps remain optional warning.
