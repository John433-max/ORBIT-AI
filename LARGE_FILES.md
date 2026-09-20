# Large modules

These full modules are in the complete source archive (`ORBIT-AI-source.zip` in the project folder):

- `agents.py` (~66 KB, 1443 lines) — Orchestrator, MainChatAgent, CalculatorAgent, ResearchAgent, etc.
- `api.py` (~27 KB, 609 lines) — FastAPI OpenAI-compatible server
- `tools/chat_tool.py` (~34 KB) — ChatRetrieveTool / ChatGenerateTool + TinyLM chat path
- `tools_legacy.py` (~18 KB) — python_sandbox, read_sandboxed_file

Until fully pushed via API batches, clone/unzip the archive over this repo:

```bash
unzip ORBIT-AI-source.zip
git add agents.py api.py tools/chat_tool.py tools_legacy.py
git commit -m "Add large core modules from full source archive"
git push
```
