"""ORBIT educational TinyLM.

Torch and full generate/checkpoint stacks are optional so a slim CI
checkout (no torch, partial tree) can still `from tinylm import TinyLMConfig`.
"""

from .config import TinyLMConfig
from .seed_utils import seed_everything
from .model_card import build_model_card

try:
    from .numpy_model import TinyLMNumPy, PackedInt4, packed_int4_numpy_bytes
except Exception:  # pragma: no cover
    TinyLMNumPy = None  # type: ignore
    PackedInt4 = None  # type: ignore
    packed_int4_numpy_bytes = None  # type: ignore

try:
    from .torch_model import TinyLMTorch
except Exception:  # pragma: no cover
    TinyLMTorch = None  # type: ignore

try:
    from .checkpoint import (
        save_numpy_checkpoint,
        load_numpy_checkpoint,
        save_numpy_int4_checkpoint,
        save_numpy_int4_mmap,
        is_numpy_int4_mmap,
        pack_numpy_state_int4,
        unpack_numpy_state_int4,
    )
except Exception:  # pragma: no cover
    save_numpy_checkpoint = None  # type: ignore
    load_numpy_checkpoint = None  # type: ignore
    save_numpy_int4_checkpoint = None  # type: ignore
    save_numpy_int4_mmap = None  # type: ignore
    is_numpy_int4_mmap = None  # type: ignore
    pack_numpy_state_int4 = None  # type: ignore
    unpack_numpy_state_int4 = None  # type: ignore

try:
    from .generate import generate_numpy, generate_torch, sample_numpy, sample_torch
except Exception:  # pragma: no cover
    generate_numpy = None  # type: ignore
    generate_torch = None  # type: ignore
    sample_numpy = None  # type: ignore
    sample_torch = None  # type: ignore

try:
    from .kv_report import kv_cache_bytes_report
except Exception:  # pragma: no cover
    kv_cache_bytes_report = None  # type: ignore

try:
    from .train import train_persona_chat  # noqa: F401
except Exception:  # pragma: no cover
    train_persona_chat = None  # type: ignore

__all__ = [
    "TinyLMConfig",
    "TinyLMNumPy",
    "TinyLMTorch",
    "generate_numpy",
    "generate_torch",
    "sample_numpy",
    "sample_torch",
    "seed_everything",
    "build_model_card",
    "kv_cache_bytes_report",
    "save_numpy_checkpoint",
    "load_numpy_checkpoint",
    "save_numpy_int4_checkpoint",
    "save_numpy_int4_mmap",
    "is_numpy_int4_mmap",
    "train_persona_chat",
]
