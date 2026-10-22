# ORBIT Improvement Run 58 — 2026-10-22

## Problem
"what is ORBIT" and "who is orbit" fell through MainChatAgent's hedge and were re-routed to ResearchAgent. Offline that produced "no live web"; with live web it could return movie/astronomy results instead of the ORBIT identity. Required identity probe ("what is your name") already passed; these close variants did not.

## Research
Existing identity matchers only covered "what is your name", "who are you", "tell me about yourself", "who created you". Knowledge-fallback in Orchestrator.handle treats the short capability hedge as weak and sends question-shaped asks to research. Expanding the identity matcher (and excluding orbital-mechanics phrases) keeps self-reference on chat without stealing astronomy.

## Implementation
- thinking._is_self_identity: match what/who is you|orbit|orbit ai; exclude "orbit of", "orbital", "orbit around", planetary orbit.
- agents.MainChatAgent.run: same matcher returns the identity sentence with raw.identity=True.
- agents.Orchestrator._route: same matcher returns "chat" before knowledge fallback.
- tests: thinking classify + route/handle identity assertions; astronomy must not set identity.
- smoke: chat_orbit_self, chat_who_orbit.

## Files
thinking.py, agents.py, tests/unit/test_thinking.py, tests/unit/test_code_route_search.py, evals/datasets/smoke.jsonl

## Tests
Unit (manual, no pytest): thinking identity 4/4; test_code_route_search 11/11 including new test_self_identity_orbit_name_not_research; test_thinking 13/13. New smoke rows score ok.

## Result
Identity edges now return "I'm ORBIT. Named after the project that built me, not the other way around." Coding and search probes unchanged. Astronomy stays research_fallback, not identity.

## Next
GitHub parity (push lab commit + this identity fix). Model-provider Ollama preference when healthy. Serve/deps docs.
