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


def pack_numpy_state_int4(sd: dict, group_size: int = 32, quantize_embeddings: bool = False) -> dict:
    out = {"_group_size": np.array(group_size, dtype=np.int32)}
    for k, v in sd.items():
        name = k.rsplit(".", 1)[-1] if "." in k else k
        is_w = name in INT4_WEIGHT_KEYS
        is_emb = (
            quantize_embeddings
            and name in ("tok_emb", "pos_emb")
            and np.asarray(v).ndim == 2
            and np.asarray(v).size > 0
        )
        if is_w or is_emb:
            packed, scales, orig_in = quant_weight_int4_np(v, group_size)
            out[f"{k}_int4"] = packed
            out[f"{k}_scale"] = scales
            out[f"{k}_orig_in"] = np.array(orig_in, dtype=np.int32)
        else:
            out[k] = np.asarray(v)
    return out


def unpack_numpy_state_int4(sd: dict) -> dict:
    group_size = int(np.asarray(sd.get("_group_size", 32)).reshape(-1)[0])
    out = {}
    skip = {"_group_size", "_orbit_n4m"}
    for k, v in sd.items():
        if k.endswith("_int4"):
            stem = k[: -len("_int4")]
            out[stem] = dequant_weight_int4_np(
                v, sd[f"{stem}_scale"], int(np.asarray(sd[f"{stem}_orig_in"]).reshape(-1)[0]), group_size
            )
            skip.update({k, f"{stem}_scale", f"{stem}_orig_in"})
    for k, v in sd.items():
        if k not in skip:
            out[k] = v
    return out


def save_numpy_int4_checkpoint(model, path: str, extra=None, group_size: int = 32, quantize_embeddings: bool = False) -> dict:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    packed = pack_numpy_state_int4(model.state_dict(), group_size=group_size, quantize_embeddings=quantize_embeddings)
    np.savez_compressed(str(path), **packed)
    meta = {
        "config": model.config.to_dict(),
        "n_tensors": len(packed),
        "format": "int4_numpy",
        "group_size": group_size,
        "quantize_embeddings": bool(quantize_embeddings),
    }
    if extra:
        meta.update(extra)
    json_path = path.with_suffix(".json")
    json_path.write_text(json.dumps(meta, indent=2))
    return {"npz": str(path), "json": str(json_path), "bytes": path.stat().st_size, "meta": meta}


def _is_packed_int4_state(sd: dict) -> bool:
    return any(k.endswith("_int4") for k in sd) or "_group_size" in sd


def _align_up(n: int, align: int = N4M_ALIGN) -> int:
    return (n + align - 1) // align * align


def _n4m_dtype_code(arr: np.ndarray) -> str:
    mapping = {np.dtype("uint8"): "u8", np.dtype("float32"): "f32", np.dtype("int32"): "i32", np.dtype("int64"): "i64"}
    if arr.dtype not in mapping:
        raise TypeError(f"unsupported n4m dtype {arr.dtype}")
    return mapping[arr.dtype]


def _n4m_numpy_dtype(code: str):
    return {"u8": np.uint8, "f32": np.float32, "i32": np.int32, "i64": np.int64}[code]


def is_numpy_int4_mmap(path: str) -> bool:
    try:
        with open(path, "rb") as f:
            return f.read(len(N4M_MAGIC)) == N4M_MAGIC
    except OSError:
        return False


def save_numpy_int4_mmap(model, path: str, extra=None, group_size: int = 32, quantize_embeddings: bool = False) -> dict:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    packed = pack_numpy_state_int4(model.state_dict(), group_size=group_size, quantize_embeddings=quantize_embeddings)
    header = {
        "format": N4M_FORMAT,
        "version": N4M_VERSION,
        "config": model.config.to_dict(),
        "group_size": group_size,
        "quantize_embeddings": bool(quantize_embeddings),
        "n_tensors": len(packed),
        "tensors": {},
    }
    if extra:
        header.update({k: v for k, v in extra.items() if k not in header})
    blobs = []
    offset = 0
    for name in sorted(packed.keys()):
        arr = np.ascontiguousarray(packed[name])
        raw = arr.tobytes()
        header["tensors"][name] = {
            "dtype": _n4m_dtype_code(arr),
            "shape": list(arr.shape),
            "offset": offset,
            "nbytes": len(raw),
        }
        pad = _align_up(len(raw)) - len(raw)
        blobs.append(raw + (b"\x00" * pad))
        offset += len(raw) + pad
    meta_bytes = json.dumps(header, separators=(",", ":")).encode("utf-8")
    with open(path, "wb") as f:
        f.write(N4M_MAGIC)
        f.write(len(meta_bytes).to_bytes(8, "little"))
        f.write(meta_bytes)
        written = len(N4M_MAGIC) + 8 + len(meta_bytes)
        f.write(b"\x00" * (_align_up(written) - written))
        for raw in blobs:
            f.write(raw)
    json_path = Path(str(path) + ".json")
    slim = {
        "config": model.config.to_dict(),
        "format": N4M_FORMAT,
        "group_size": group_size,
        "quantize_embeddings": bool(quantize_embeddings),
        "bytes": path.stat().st_size,
    }
    if extra:
        slim.update(extra)
    json_path.write_text(json.dumps(slim, indent=2))
    return {"mmap": str(path), "json": str(json_path), "bytes": path.stat().st_size, "meta": header}


def _n4m_header(path: str):
    with open(path, "rb") as f:
        magic = f.read(len(N4M_MAGIC))
        if magic != N4M_MAGIC:
            raise ValueError(f"not an orbit.n4m checkpoint: {path}")
        n = int.from_bytes(f.read(8), "little")
        meta = json.loads(f.read(n).decode("utf-8"))
        written = len(N4M_MAGIC) + 8 + n
        data_off = _align_up(written)
    if meta.get("format") != N4M_FORMAT:
        raise ValueError(f"bad n4m format field: {meta.get('format')}")
    return meta, data_off


def load_numpy_int4_mmap_state(path: str, *, copy: bool = False):
    meta, data_off = _n4m_header(path)
    mm = np.memmap(path, dtype=np.uint8, mode="r")
    sd = {}
    for name, spec in meta["tensors"].items():
        start = data_off + int(spec["offset"])
        view = np.ndarray(spec["shape"], dtype=_n4m_numpy_dtype(spec["dtype"]), buffer=mm, offset=start)
        if copy:
            sd[name] = np.array(view, copy=True)
        else:
            view.flags.writeable = False
            sd[name] = view
    sd["_orbit_n4m"] = mm
    return sd, meta


def load_numpy_checkpoint(path: str, seed: int = 0, keep_packed: bool = False):
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)
    if is_numpy_int4_mmap(str(path)):
        sd, header = load_numpy_int4_mmap_state(str(path), copy=True)
        sd.pop("_orbit_n4m", None)
        cfg = TinyLMConfig.from_dict(header.get("config") or {})
        model = TinyLMNumPy.from_config(cfg, seed=seed)
        meta = {
            "config": header.get("config") or {},
            "format": N4M_FORMAT,
            "loaded_int4": True,
            "loaded_n4m": True,
            "group_size": header.get("group_size", 32),
            "quantize_embeddings": header.get("quantize_embeddings", False),
        }
        if keep_packed:
            meta["keep_packed"] = True
            model.load_packed_int4_state(sd, materialize=False)
            return model, meta
        model.load_state_dict(unpack_numpy_state_int4(sd), strict=True)
        return model, meta
    json_path = path.with_suffix(".json")
    if json_path.exists():
        meta = json.loads(json_path.read_text())
        cfg = TinyLMConfig.from_dict(meta.get("config") or {})
    else:
        meta = {}
        cfg = TinyLMConfig()
    model = TinyLMNumPy.from_config(cfg, seed=seed)
    with np.load(str(path), allow_pickle=False) as z:
        sd = {k: z[k] for k in z.files}
    if _is_packed_int4_state(sd):
        meta = dict(meta)
        meta["loaded_int4"] = True
        if keep_packed:
            meta["keep_packed"] = True
            model.load_packed_int4_state(sd, materialize=False)
            return model, meta
        sd = unpack_numpy_state_int4(sd)
    model.load_state_dict(sd, strict=True)
    return model, meta
