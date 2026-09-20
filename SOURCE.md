# Source layout

Repository root is the runnable package.

Key modules: `api.py`, `agents.py`, `orbit_ai.py`, `tools/`, `tinylm/`, `orbit/models/`, `webui/`, `tests/`.

`DESIGN.md` is **historical research notes** about possible future large-model training. It does **not** mean ORBIT ships 100B parameters.

Binary checkpoints (`*.npz`, `*.gguf`, …) are gitignored; train or download separately.
