# Full source

This GitHub repo is being filled from the ORBIT project workspace.

**Complete source archive** (no large `.npz` weights):

- Local path in the Grok project: `artifacts/ORBIT-AI-source.zip` (~352 KB)
- Extract, then from that folder:

```bash
pip install -r requirements.txt
python run_orbit.py
```

Large checkpoint `.npz` files are intentionally gitignored (see `.gitignore`).

## Already on this branch

- README, UNIFIED, requirements, CI workflow
- Package stubs: agent/, chat/, api_routes/
- run_orbit.py launcher

More modules (agents.py, tinylm/, tools/, webui/, tests/) are in the zip and can be pushed in follow-up commits.
