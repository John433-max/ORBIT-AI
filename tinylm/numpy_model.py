from __future__ import annotations

from typing import Optional, Union

import numpy as np

from .config import TinyLMConfig
from .rope import rope_inv_freq, yarn_attn_scale


class PackedInt4:
    """Group-wise INT4 weight kept packed until first matmul (Cycle 75).

    Layout matches `quant_weight_int4_np`: packed uint8 (out, in_pad/2),
    scales (out, n_groups), orig_in. `materialize()` returns (in, out) FP32
    and caches it so decode stays BLAS-speed after one unpack.
    """

    __slots__ = ("packed", "scales", "orig_in", "group_size", "_fp32")

    def __init__(
        self,
        packed: np.ndarray,
        scales: np.ndarray,
        orig_in: int,
        group_size: int = 32,
    ):
        self.packed = np.asarray(packed)
        self.scales = np.asarray(scales, dtype=np.float32)
        self.orig_in = int(orig_in)
        self.group_size = int(group_size)
        self._fp32: Optional[np.ndarray] = None

    def materialize(self) -> np.ndarray:
        if self._fp32 is None:
            from .checkpoint import dequant_weight_int4_np

            self._fp32 = dequant_weight_int4_np(
                self.packed, self.scales, self.orig_in, self.group_size
            )
        return self._fp32

    def drop_packed(self) -> None:
        """Free uint8 codes after materialize (scales stay for export)."""
        self.materialize()
        self.packed = np.zeros((0, 0), dtype=np.uint8)

    def packed_nbytes(self) -> int:
        return int(self.packed.nbytes) + int(self.scales.nbytes)

    def cache_nbytes(self) -> int:
        return 0 if self._fp32 is None else int(self._fp32.nbytes)

    @property
    def T(self) -> np.ndarray:
        return self.materialize().T

    def __getitem__(self, idx):
        return self.materialize()[idx]


Weight = Union[np.ndarray, PackedInt4]


def _fp32(w: Weight) -> np.ndarray:
    return w.materialize() if isinstance(w, PackedInt4) else w


def _matmul(x: np.ndarray, w: Weight) -> np.ndarray:
    return x @ _fp32(w)


def packed_int4_numpy_bytes(model: "TinyLMNumPy") -> tuple[int, int, int]:
    """(packed+scale bytes, leftover FP32 linear bytes, FP32 cache bytes)."""
    packed = 0
    leftover = 0
    cache = 0
    keys = ("wq", "wk", "wv", "wo", "w1", "w2")
    for layer in model.layers:
        for k in keys:
            w = layer[k]
            if isinstance(w, PackedInt4):
                packed += w.packed_nbytes()
                cache += w.cache_nbytes()
            else:
                leftover += int(np.asarray(w).nbytes)
    for name in ("tok_emb", "pos_emb"):
        w = getattr(model, name)
        if isinstance(w, PackedInt4):
            packed += w.packed_nbytes()
            cache += w.cache_nbytes()
    return packed, leftover, cache


def _rms_norm(x: np.ndarray, weight: np.ndarray, eps: float) -> np.ndarray:
    rms = np.sqrt(np.mean(x * x, axis=-1, keepdims=True) + eps)
    return (x / rms) * weight


def _softmax(x: np.ndarray, axis: int = -1) -> np.ndarray:
    x = x - np.max(x, axis=axis, keepdims=True)
    e = np.exp(x)
    return e / np.sum(e, axis=axis, keepdims=True)


def _softcap(logits: np.ndarray, cap: float) -> np.ndarray:
    if cap <= 0:
        return logits
    return cap * np.tanh(logits / cap)


def ring_store_gather(
    pk: np.ndarray,
    pv: np.ndarray,
    k: np.ndarray,
    v: np.ndarray,
    cache_pos: int,
    used: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Cycle 71: write K/V into a ring and gather chronological last-n via
    at most two contiguous slices (no fancy index).

    ``pk``/``pv`` shape (B, H, cap, D); ``k``/``v`` (B, H, t, D).
    """
    cap = pk.shape[2]
    t = k.shape[2]
    s = int(cache_pos) % cap
    if t == 1:
        pk[:, :, s : s + 1] = k
        pv[:, :, s : s + 1] = v
    elif s + t <= cap:
        pk[:, :, s : s + t] = k
        pv[:, :, s : s + t] = v
    else:
        n1 = cap - s
        pk[:, :, s:] = k[:, :, :n1]
        pk[:, :, : t - n1] = k[:, :, n1:]
        pv[:, :, s:] = v[:, :, :n1]
        pv[:, :, : t - n1] = v[:, :, n1:]
    n = min(int(used), cap)
    start_slot = (int(used) - n) % cap
    if start_slot + n <= cap:
        return pk[:, :, start_slot : start_slot + n], pv[:, :, start_slot : start_slot + n]
    n1 = cap - start_slot
    k_out = np.concatenate([pk[:, :, start_slot:], pk[:, :, : n - n1]], axis=2)
    v_out = np.concatenate([pv[:, :, start_slot:], pv[:, :, : n - n1]], axis=2)
    return k_out, v_out


def rope_cos_sin(
    positions: np.ndarray,
    head_dim: int,
    theta: float,
    scaling: str = "none",
    factor: float = 1.0,
    orig_ctx: int = 64,
) -> tuple[np.ndarray, np.ndarray]:
    """Cos/sin tables for RoPE. positions: (T,), returns (T, D/2) each."""
    inv_freq = rope_inv_freq(head_dim, theta, scaling=scaling, factor=factor, orig_ctx=orig_ctx)
    freqs = positions.astype(np.float32)[:, None] * inv_freq[None, :]
    return np.cos(freqs), np.sin(freqs)


def apply_rope(x: np.ndarray, cos: np.ndarray, sin: np.ndarray) -> np.ndarray:
    """Rotate pairs of even/odd dims. x: (B, H, T, D); cos/sin: (T, D/2)."""
    x1 = x[..., 0::2]
    x2 = x[..., 1::2]
    c = cos[None, None, :, :]
    s = sin[None, None, :, :]
    out = np.empty_like(x)
    out[..., 0::2] = x1 * c - x2 * s
    out[..., 1::2] = x1 * s + x2 * c
    return out


class TinyLMNumPy:
    """Decoder-only TinyLM in NumPy with optional QK-Norm and KV cache."""

    def __init__(self, config: TinyLMConfig, seed: int = 0):
        self.config = config
        rng = np.random.default_rng(seed)
        c = config
        std = c.init_std
        rscale = c.residual_scale()

        self.tok_emb = rng.normal(0, std, (c.vocab_size, c.n_embd)).astype(np.float32)
        # Learned absolute positions only when not using RoPE (Cycle 21).
        if c.use_rope:
            self.pos_emb = np.zeros((0, c.n_embd), dtype=np.float32)
        else:
            self.pos_emb = rng.normal(0, std, (c.block_size, c.n_embd)).astype(np.float32)
        self.ln_f_w = np.ones(c.n_embd, dtype=np.float32)

        kv_dim = c.n_kv_head * c.head_dim
        ff = c.ffn_dim()
        self.layers = []
        for _ in range(c.n_layer):
            if c.use_swiglu:
                w1 = rng.normal(0, std, (c.n_embd, 2 * ff)).astype(np.float32)
                w2 = rng.normal(0, std * rscale, (ff, c.n_embd)).astype(np.float32)
            else:
                w1 = rng.normal(0, std, (c.n_embd, ff)).astype(np.float32)
                w2 = rng.normal(0, std * rscale, (ff, c.n_embd)).astype(np.float32)
            layer = {
                "ln1_w": np.ones(c.n_embd, dtype=np.float32),
                "ln2_w": np.ones(c.n_embd, dtype=np.float32),
                "wq": rng.normal(0, std, (c.n_embd, c.n_embd)).astype(np.float32),
                "wk": rng.normal(0, std, (c.n_embd, kv_dim)).astype(np.float32),
                "wv": rng.normal(0, std, (c.n_embd, kv_dim)).astype(np.float32),
                "wo": rng.normal(0, std * rscale, (c.n_embd, c.n_embd)).astype(np.float32),
                "w1": w1,
                "w2": w2,
                "q_norm": np.ones(c.head_dim, dtype=np.float32),
                "k_norm": np.ones(c.head_dim, dtype=np.float32),
            }
            self.layers.append(layer)

    @classmethod
    def from_config(cls, config: TinyLMConfig, seed: int = 0) -> "TinyLMNumPy":
        return cls(config, seed=seed)

    def state_dict(self) -> dict:
        """Flat numpy arrays + layer_* keys (Cycle 67). Packed INT4 is materialized."""
        out = {
            "tok_emb": _fp32(self.tok_emb),
            "pos_emb": _fp32(self.pos_emb),
            "ln_f_w": self.ln_f_w,
        }
        for i, layer in enumerate(self.layers):
            for k, v in layer.items():
                out[f"layers.{i}.{k}"] = _fp32(v) if isinstance(v, PackedInt4) else v
        return out

    def load_packed_int4_state(self, sd: dict, materialize: bool = False) -> None:
        """Install PackedInt4 wrappers from a packed checkpoint dict."""
        group_size = int(np.asarray(sd.get("_group_size", 32)).reshape(-1)[0])
        if "ln_f_w" in sd:
            self.ln_f_w = np.array(sd["ln_f_w"], dtype=np.float32)
        if "tok_emb_int4" in sd:
            self.tok_emb = PackedInt4(
                sd["tok_emb_int4"], sd["tok_emb_scale"], int(np.asarray(sd["tok_emb_orig_in"]).reshape(-1)[0]), group_size
            )
        elif "tok_emb" in sd:
            self.tok_emb = np.array(sd["tok_emb"], dtype=np.float32)
        if "pos_emb_int4" in sd:
            self.pos_emb = PackedInt4(
                sd["pos_emb_int4"], sd["pos_emb_scale"], int(np.asarray(sd["pos_emb_orig_in"]).reshape(-1)[0]), group_size
            )
        elif "pos_emb" in sd:
            self.pos_emb = np.array(sd["pos_emb"], dtype=np.float32)
        for i, layer in enumerate(self.layers):
            for k in list(layer.keys()):
                stem = f"layers.{i}.{k}"
                if f"{stem}_int4" in sd:
                    layer[k] = PackedInt4(
                        sd[f"{stem}_int4"],
                        sd[f"{stem}_scale"],
                        int(np.asarray(sd[f"{stem}_orig_in"]).reshape(-1)[0]),
                        group_size,
                    )
                elif stem in sd:
                    layer[k] = np.array(sd[stem], dtype=np.float32)
        if materialize:
            self.materialize_packed()

    def materialize_packed(self, drop_packed: bool = False) -> None:
        """Force-unpack every PackedInt4 (optional drop of uint8 codes)."""
        for name in ("tok_emb", "pos_emb"):
            w = getattr(self, name)
            if isinstance(w, PackedInt4):
                w.materialize()
                if drop_packed:
                    w.drop_packed()
        for layer in self.layers:
            for k, v in layer.items():
                if isinstance(v, PackedInt4):
                    v.materialize()
                    if drop_packed:
                        v.drop_packed()

    def load_state_dict(self, sd: dict, strict: bool = True) -> list:
        """Copy matching arrays in-place. Returns missing keys."""
        missing = []
        if "tok_emb" in sd:
            self.tok_emb = np.array(sd["tok_emb"], dtype=np.float32)
        else:
            missing.append("tok_emb")
        if "pos_emb" in sd:
            self.pos_emb = np.array(sd["pos_emb"], dtype=np.float32)
        else:
            missing.append("pos_emb")
        if "ln_f_w" in sd:
            self.ln_f_w = np.array(sd["ln_f_w"], dtype=np.float32)
        else:
            missing.append("ln_f_w")
        for i, layer in enumerate(self.layers):
            for k in list(layer.keys()):
                key = f"layers.{i}.{k}"
                if key in sd:
                    layer[k] = np.array(sd[key], dtype=np.float32)
                else:
                    missing.append(key)
        if strict and missing:
            raise KeyError(f"TinyLMNumPy missing keys: {missing[:8]}")
        return missing

    def alloc_kv_caches(self, batch: int, max_len: int) -> list:
        """Preallocated (k, v) buffers shaped (B, n_kv_head, cap, D).

        Cycle 54: when sliding_window W>0, cap = min(max_len, W) (ring buffer).
        """
        c = self.config
        cap = int(max_len)
        if c.sliding_window > 0:
            cap = min(cap, int(c.sliding_window))
        caches = []
        for _ in range(c.n_layer):
            k = np.zeros((batch, c.n_kv_head, cap, c.head_dim), dtype=np.float32)
            v = np.zeros_like(k)
            caches.append((k, v))
        return caches

    def _attn(
        self,
        x: np.ndarray,
        layer: dict,
        kv_cache: Optional[tuple] = None,
        cache_pos: Optional[int] = None,
        positions: Optional[np.ndarray] = None,
    ) -> tuple[np.ndarray, tuple[np.ndarray, np.ndarray]]:
        c = self.config
        b, t, _ = x.shape
        h, kvh, d = c.n_head, c.n_kv_head, c.head_dim

        q = _matmul(x, layer["wq"])
        k = _matmul(x, layer["wk"])
        v = _matmul(x, layer["wv"])
        q = q.reshape(b, t, h, d).transpose(0, 2, 1, 3)
        k = k.reshape(b, t, kvh, d).transpose(0, 2, 1, 3)
        v = v.reshape(b, t, kvh, d).transpose(0, 2, 1, 3)

        if c.qk_norm:
            q = _rms_norm(q, layer["q_norm"], c.rms_eps)
            k = _rms_norm(k, layer["k_norm"], c.rms_eps)

        if c.use_rope:
            if positions is None:
                raise ValueError("positions required when use_rope=True")
            cos, sin = rope_cos_sin(
                positions,
                d,
                c.rope_theta,
                scaling=c.rope_scaling,
                factor=c.rope_factor,
                orig_ctx=c.block_size,
            )
            q = apply_rope(q, cos, sin)
            k = apply_rope(k, cos, sin)

        if kv_cache is not None and cache_pos is not None:
            pk, pv = kv_cache
            cap = pk.shape[2]
            win = int(c.sliding_window)
            used = cache_pos + t
            if win > 0 and cap <= win:
                k, v = ring_store_gather(pk, pv, k, v, cache_pos, used)
            else:
                pk[:, :, cache_pos : cache_pos + t] = k
                pv[:, :, cache_pos : cache_pos + t] = v
                k = pk[:, :, :used]
                v = pv[:, :, :used]
            new_cache = kv_cache
        elif kv_cache is not None:
            pk, pv = kv_cache
            k = np.concatenate([pk, k], axis=2)
            v = np.concatenate([pv, v], axis=2)
            new_cache = (k, v)
        else:
            new_cache = (k, v)

        # Decode-only: drop keys outside the sliding window to shrink QK.
        win_trim = int(c.sliding_window)
        if win_trim > 0 and t == 1 and k.shape[2] > win_trim:
            k = k[:, :, -win_trim:]
            v = v[:, :, -win_trim:]

        if kvh != h:
            rep = h // kvh
            k = np.repeat(k, rep, axis=1)
            v = np.repeat(v, rep, axis=1)

        scores = (q @ np.swapaxes(k, -1, -2)) / np.sqrt(d)
        scores = scores * yarn_attn_scale(c.rope_scaling, c.rope_factor)
        scores = _softcap(scores, c.attn_logit_softcap)

        klen = k.shape[2]
        qlen = q.shape[2]
        past = klen - qlen
        q_pos = np.arange(qlen)[:, None] + past
        k_pos = np.arange(klen)[None, :]
        mask = k_pos > q_pos
        w = int(c.sliding_window)
        if w > 0:
            mask = mask | ((q_pos - k_pos) >= w)
        scores = np.where(mask[None, None, :, :], -1e9, scores)
        w = _softmax(scores, axis=-1)
        out = (w @ v).transpose(0, 2, 1, 3).reshape(b, t, c.n_embd)
        return _matmul(out, layer["wo"]), new_cache

    def forward(
        self,
        idx: np.ndarray,
        kv_caches: Optional[list] = None,
        cache_pos: Optional[int] = None,
    ) -> tuple[np.ndarray, list]:
        c = self.config
        b, t = idx.shape
        if cache_pos is not None:
            pos0 = cache_pos
        elif kv_caches is None:
            pos0 = 0
        else:
            pos0 = kv_caches[0][0].shape[2]
        limit = c.max_seq_len()
        if pos0 + t > limit:
            raise ValueError(
                f"sequence length {pos0 + t} exceeds max_seq_len {limit} (block_size={c.block_size})"
            )
        pos = np.arange(pos0, pos0 + t)
        x = _fp32(self.tok_emb)[idx]
        if not c.use_rope:
            x = x + _fp32(self.pos_emb)[pos][None, :, :]

        new_caches = []
        for i, layer in enumerate(self.layers):
            n1 = _rms_norm(x, layer["ln1_w"], c.rms_eps)
            cache = None if kv_caches is None else kv_caches[i]
            attn_out, new_c = self._attn(
                n1, layer, cache, cache_pos=cache_pos, positions=pos
            )
            x = x + attn_out
            n2 = _rms_norm(x, layer["ln2_w"], c.rms_eps)
            h_ff = _matmul(n2, layer["w1"])
            if c.use_swiglu:
                ff = h_ff.shape[-1] // 2
                gate, up = h_ff[..., :ff], h_ff[..., ff:]
                # SiLU
                gate = gate / (1.0 + np.exp(-np.clip(gate, -60, 60)))
                x = x + _matmul(gate * up, layer["w2"])
            else:
                x = x + _matmul(h_ff.clip(min=0), layer["w2"])
            new_caches.append(new_c)

        x = _rms_norm(x, self.ln_f_w, c.rms_eps)
        logits = _matmul(x, _fp32(self.tok_emb).T)
        return logits.astype(np.float32), new_caches
