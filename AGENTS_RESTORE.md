# agents.py restore required

**Incident (2026-10-17):** Two commits replaced `agents.py` with placeholder text (`PLACEHOLDER` / `SEE_FILE`) during an MCP push that failed to embed the full ~103KB file body.

**Broken commits:** `78696b35`, `31154b44`

**Last good remote agents.py:** commit `0f8523425cf4b0ad2c785fe15044620523596c59` (before those two).

**Local source of truth:** `/home/workdir/artifacts/orbit/agents.py` (~103KB) includes:
- Full orchestrator + agents
- RAG-empty fix: route `summarize my uploaded report` → `document_agent` with honest empty message

**Restore (from a machine with the full tree):**
```bash
cd /path/to/ORBIT-AI
cp /home/workdir/artifacts/orbit/agents.py ./agents.py   # or from your local copy
git add agents.py
git commit -m "fix: restore full agents.py after placeholder incident + RAG-empty report route"
git push origin main
```

Or reset file from last good commit then re-apply the ROUTES/AGENT_SIGNALS/DocumentAgent empty-path edits in `research/cycle_rag_empty_route.md`.

**Do not** leave `agents.py` as PLACEHOLDER — CI and runtime will break.
