# ORBIT source layout

Repository root is the **runnable package** (not nested under `ORBIT-AI-pack/`).

## Layout

```
ORBIT-AI/
  api.py              FastAPI entry
  agents.py           Orchestrator + agents
  orbit_ai.py         Unified facade
  tools/              ToolRegistry tools
  tools_legacy.py     Sandbox / legacy search helpers
  tinylm/             Educational TinyLM
  orbit/              Model providers, state, MCP
  webui/              Chat UI (index.html)
  tests/              unit + security
  configs/            YAML model sizes
  docs/               Architecture notes
  DESIGN.md           Design history (large)
```

## Large / full local copies

Some modules on GitHub are size-trimmed for API upload. Full local sources:

| File | Full size | Notes |
|------|-----------|--------|
| `agents.py` | ~66 KB | Full in `ORBIT-AI-github-ready.zip` |
| `api.py` | ~27 KB | Expand via zip or local |
| `tools/chat_tool.py` | ~34 KB | Full in zip |
| `tools_legacy.py` | ~18 KB | Full in zip |

```bash
unzip ORBIT-AI-github-ready.zip
cp ORBIT-AI-pack/agents.py ORBIT-AI-pack/api.py .
cp ORBIT-AI-pack/tools/chat_tool.py tools/
cp ORBIT-AI-pack/tools_legacy.py .
git add -A && git commit -m "Restore full large modules from archive" && git push
```

Checkpoints (`*.npz`) are intentionally not in the repo.
