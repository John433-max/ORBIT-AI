# ORBIT Improvement Run 44

## Baseline
- doctor: READY (2 non-blocking: fastapi/uvicorn, Ollama refused)
- smoke accuracy: 1.0 (2100/2100 from latest.json 2026-10-22T00:23)
- probes: coding add → coding_agent Verified; search fusion → research no-live-web; identity → I'm ORBIT
- failing: "what files are in the sandbox" → research no-live-web (should be sandbox listing)

## Chosen priority
Coding/chat path quality: local file inventory phrases must stay sandbox, not weak-fall to ResearchAgent.

## Research
- Run 43 claimed expanded list-files patterns but only `\blist files\b` remained in MainChatAgent.
- "what files are in the sandbox" routes to chat → generic hedge → `_looks_like_knowledge` true (question form) → research offline note.
- Document inventory is already routed separately; sandbox file listing is a distinct MainChat concern.

## Changes
- `agents.py`: expand MainChatAgent file-inventory regex (what/which/show files, files in sandbox/workspace, what's in the sandbox).
- `agents.py`: add `_looks_like_file_inventory`; exclude those from `_looks_like_knowledge` so weak fallback never hijacks them.
- `tests/unit/test_code_route_search.py`: `test_file_inventory_phrases_stay_sandbox_not_research`.

## Tests
- unit test_code_route_search: 9 passed
- probes: what files / list files → sandbox listing; coding/search/identity/tell-me-about/binary-search unchanged

## Benchmark before → after
| Metric | Before | After |
|---|---|---|
| "what files are in the sandbox" | research "no live web" | "Files in the sandbox: …" |
| "list files" | sandbox listing | sandbox listing (unchanged) |
| unit route tests | 8 | 9 passed |
| full smoke (prior) | 1.0 (2100) | not re-run (targeted only) |

## GitHub push
pending (git push needs credentials; local ahead + this fix uncommitted)

## Next priority remaining
Priorities 1–3 green. GitHub parity (push agents.py + tests when auth available). Optional: fastapi serve extras, Ollama preference when healthy.
