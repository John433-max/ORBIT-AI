# Cycle 346 — TinyLM on Python 3.10 (bytecode magic fallback)

## Problem
Doctor TinyLM row failed: `TinyLM unavailable: 'NoneType' object is not callable`.
`tinylm.checkpoint` import died because `numpy_model.py` exec'd `_numpy_model_bc.pyc` (magic `0x0dcb` = CPython 3.12) under 3.10.21 (`0x0d6f`). `load_numpy_checkpoint` stayed None. Generate then failed with `No module named 'torch'` because `tinylm/generate.py` imported torch at module level.

## Research
CPython pyc magic is version-locked (3.10 = 3439, 3.12 = 3531). A 3.12 code object cannot be `exec_module`'d on 3.10. The last intact pure-Python body is in `ORBIT-AI-source.zip` (`tinylm/numpy_model.py`, 2026-09-19, 456 lines, PackedInt4 + TinyLMNumPy). Torch is optional for the NumPy educational path; grammar modules already try/except torch.

## Implementation
- `tinylm/_numpy_model_py310.py`: recovered source body.
- `tinylm/numpy_model.py`: on ImportError from the snapshot, bind that module as `_bc`. Skip EAGLE monkeypatch when `attach_eagle` is absent (3.12 snapshot only).
- `tinylm/generate.py`: torch import optional so `generate_numpy` loads without torch.
- Regression: `test_tinylm_py310_fallback_generates`.

## Measurement
- Before: TinyLM health `ok=False`; generate error `No module named 'torch'`.
- After: health `{ok: True, weights: checkpoint}`; generate `ok=True` text `(tinylm decode)`.
- Doctor after PyYAML present: READY (API deps WARNING, Ollama OPTIONAL). PyYAML was already required in requirements.txt; not a code change.

## Not claimed
EAGLE/Medusa heads and fused INT4 kernels that lived only in the 3.12 snapshot are not restored on 3.10. Educational forward + checkpoint load is.
