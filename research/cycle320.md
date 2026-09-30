# Cycle 320 — GitHub code_synth pack parity

Date: 2026-09-30

## Problem
Local coding path is healthy (smoke 630/630, 623 verified templates).
GitHub main is missing packs: p2, p3, p28–p32, p44, p47, p49, p52–p57, p59.
Remote loader only listed through p50.

## Plan
Push loader (p1–p59, skip-missing) plus small missing packs.
Do not push 88KB p2 / 187KB p3 in this commit.

## Local baseline
- doctor: READY (fastapi/uvicorn warning, Ollama optional)
- smoke: 630/630 accuracy 1.0
- probes: coding_agent add(); research_agent fusion news; identity ORBIT
- templates: 623, verify_source fail=0

## Next
Push remaining missing packs p28–p32, p44, p47, p49, p53–p57, p59, then p2/p3.
Keep full local agents.py off remote until slim-parity is planned.
