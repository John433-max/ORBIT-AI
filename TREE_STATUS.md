# Tree status (post-upload fix)

## What was fixed

- Confirmed **flat repo root** (not stuck under `ORBIT-AI-pack/`)
- Documented layout in `SOURCE.md`
- Added/restored `autograd.py` surface
- Identified truncated modules still needing full restore from the zip

## Still truncated vs local archive

| Path | On GitHub | Full in zip |
|------|-----------|-------------|
| `agents.py` | ~19 KB surface | ~66 KB |
| `api.py` | ~2 KB mount stub | ~27 KB |
| `tools/chat_tool.py` | ~4 KB | ~34 KB |
| `tools_legacy.py` | ~4 KB | ~18 KB |
| `DESIGN.md` | missing/partial | ~36 KB |
| `webui/index.html` | may be missing | ~22 KB |

Restore with:

```bash
unzip -o ORBIT-AI-github-ready.zip
cp ORBIT-AI-pack/agents.py ORBIT-AI-pack/api.py ORBIT-AI-pack/DESIGN.md .
cp ORBIT-AI-pack/tools_legacy.py .
cp ORBIT-AI-pack/tools/chat_tool.py tools/
mkdir -p webui && cp ORBIT-AI-pack/webui/index.html webui/
git add -A && git commit -m "Restore full modules from archive" && git push
```

## Structure is valid for

- `python -m pytest tests/ -q` (with deps)
- `uvicorn api:app` (health + mounted routers)
- `from agents import Orchestrator`
