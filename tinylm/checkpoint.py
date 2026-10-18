"""TinyLM NumPy checkpoint save/load (Cycle 67). INT4 pack + orbit.n4m mmap."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import numpy as np

from .config import TinyLMConfig
from .numpy_model import TinyLMNumPy

N4M_MAGIC = b"ORBITN4\n"
N4M_VERSION = 1
N4M_ALIGN = 64
N4M_FORMAT = "orbit.n4m"
INT4_QMAX = 7
INT4_WEIGHT_KEYS = ("wq", "wk", "wv", "wo", "w1", "w2")


def save_numpy_checkpoint(model: TinyLMNumPy, path: str, extra: Optional[dict] = None) -> dict:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    sd = model.state_dict()
    np.savez_compressed(str(path), **sd)
    meta = {"config": model.config.to_dict(), "n_tensors": len(sd)}
    if extra:
        meta.update(extra)
    json_path = path.with_suffix(".json")
    json_path.write_text(json.dumps(meta, indent=2))
    return {"npz": str(path), "json": str(json_path), "bytes": path.stat().st_size, "meta": meta}


def _pad_in_np(w: np.ndarray, group_size: int):
    out, inn = w.shape
    rem = inn % group_size
    if rem:
        w = np.concatenate([w, np.zeros((out, group_size - rem), dtype=np.float32)], axis=1)
    return w.astype(np.float32, copy=False), inn


def quant_weight_int4_np(w_inout: np.ndarray, group_size: int = 32):
    w = np.asarray(w_inout, dtype=np.float32).T
    wp, orig_in = _pad_in_np(w, group_size)
    out, inn = wp.shape
    n_groups = inn // group_size
    g = wp.reshape(out, n_groups, group_size)
    amax = np.maximum(np.abs(g).max(axis=-1), 1e-8)
    scales = (amax / float(INT4_QMAX)).astype(np.float32)
    q = np.clip(np.rint(g / scales[..., None]), -INT4_QMAX, INT4_QMAX).astype(np.int16).reshape(out, inn)
    even = (q[:, 0::2] + INT4_QMAX).astype(np.uint8)
    odd = (q[:, 1::2] + INT4_QMAX).astype(np.uint8)
    return even | (odd << 4), scales, orig_in


def dequant_weight_int4_np(packed, scales, orig_in, group_size: int = 32):
    packed = np.asarray(packed)
    out, packed_in = packed.shape
    inn = packed_in * 2
    even = (packed & 0x0F).astype(np.int16) - INT4_QMAX
    odd = ((packed >> 4) & 0x0F).astype(np.int16) - INT4_QMAX
    q = np.empty((out, inn), dtype=np.float32)
    q[:, 0::2] = even.astype(np.float32)
    q[:, 1::2] = odd.astype(np.float32)
    n_groups = inn // group_size
    w = q.reshape(out, n_groups, group_size) * np.asarray(scales, dtype=np.float32)[..., None]
    w = w.reshape(out, inn)[:, : int(orig_in)]
    return np.ascontiguousarray(w.T)
