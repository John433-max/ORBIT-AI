# agents.py restore required

**Incident (2026-10-17):** Two commits replaced `agents.py` with placeholder text (`PLACEHOLDER` / `SEE_FILE`) during an MCP push that failed to embed the full ~103KB file body.

**Broken commits:** `78696b35`, `31154b44`

**Additional broken (2026-10-23):** commit `a8b03f316e5040c9c318038ed0ebc9f0c9822bae` titled "fix(agents): restore full agents.py after empty push" actually wrote only `PLACEHOLDER_SEE_NEXT` (20 bytes). CI Tests run 40038822119 failed with exit code 2 on Python 3.11/3.12 (unit tests core step).

**Last good remote agents.py:** commit `0f8523425cf4b0ad2c785fe15044620523596c59` (full ~108KB file with Orchestrator, CodeAgent, ResearchAgent, etc.).

**Local source of truth:** `/home/workdir/artifacts/orbit/agents.py`

**Restore (from a machine with the full tree or git):**
```bash
cd /path/to/ORBIT-AI
git checkout 0f8523425cf4b0ad2c785fe15044620523596c59 -- agents.py
# or cp from local full copy
git add agents.py
git commit -m "fix: restore full agents.py from 0f85234 after placeholder pushes"
git push origin main
```

**Do not** leave `agents.py` as PLACEHOLDER — CI and runtime will break (import/syntax/test collection fail).

MCP `push_files` has repeatedly truncated large `agents.py` payloads to a placeholder string; use native git for files >~50KB.
