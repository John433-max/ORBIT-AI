# ORBIT Improvement Run 45

## Baseline
- doctor: READY (3 non-blocking: PyYAML warning, API deps warning, Ollama optional refused)
- smoke accuracy: 1.0 (2100/2100 from latest.json 2026-10-22_002352)
- failing probes: none
  - coding "write a python function that adds two numbers" → coding_agent, real add() code, Verified
  - search "search for recent news about fusion energy" → honest "No live web available"
  - identity "what is your name" → "I'm ORBIT..."

## Chosen priority
Priority 4: GitHub parity — local was ahead 1 commit (9ebab13 fix(chat): expand sandbox file inventory phrases)

## Changes
Pushed existing tested commit 9ebab13 to origin/main.
No new code changes this run (probes 1-3 already green).

## Tests
- doctor READY
- probes all pass
- previous eval 2100/2100
- unit coverage for file inventory already in tests/unit/test_code_route_search.py

## Benchmark before → after
No code change; parity only.
file inventory probe: routes to main_chat_agent (correct)
coding probe: routes to coding_agent + verified source

## GitHub push: YES
commit 9ebab1327bbdb042995f3b00e75fb45f09f4be79
c2d3a52..9ebab13  main -> main

## Next priority remaining
1-3 green. 5: Ollama not running (tinylm correct fallback). 6: fastapi/uvicorn optional warning already documented.
Possible next: serve extras install docs, or additional edge-case routing probes, or wait for full eval completion.
