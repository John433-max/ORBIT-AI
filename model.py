"""
Compatibility shim for the original top-level `model.py`.

ORBIT v2 moved the educational NumPy implementation to
`model_numpy_legacy.py` and exposed a modular package at `model/`.

This file exists so that:
  - `ls model.py` / docs / scripts that expect the classic path still work
  - `import model` continues to resolve (the `model/` package takes
    precedence when both exist; this module mirrors the same public API)

Prefer:
  from model import TinyLM, get_preset, ModelConfig
"""

from model_numpy_legacy import (  # noqa: F401
    TinyLM,
    CausalSelfAttentionGQA,
    SwiGLUMLP,
    Block,
    ReasoningBlock,
    rmsnorm,
    rope_cos_sin,
    apply_rope,
    check_finite,
    init_linear,
)

# Config system lives in the package
try:
    from model.config import (  # noqa: F401
        ModelConfig,
        TrainingConfig,
        RuntimeConfig,
        DatasetMixConfig,
        OrbitConfig,
        get_preset,
        GenerationConfig,
        PRESET_NAMES,
    )
except Exception:  # pragma: no cover
    pass

__all__ = [
    "TinyLM",
    "CausalSelfAttentionGQA",
    "SwiGLUMLP",
    "Block",
    "ReasoningBlock",
    "rmsnorm",
    "rope_cos_sin",
    "apply_rope",
    "check_finite",
    "init_linear",
]
