"""Rotary Position Embeddings (RoPE)."""

from __future__ import annotations

import numpy as np

from autograd import Tensor


def rope_cos_sin(seq_len: int, d_head: int, base: float = 10000.0):
    """
    Precompute cos and sin tables for RoPE.
    Returns (cos, sin) each of shape (seq_len, d_head).
    """
    inv_freq = 1.0 / (base ** (np.arange(0, d_head, 2) / d_head))
    t = np.arange(seq_len)
    freqs = np.outer(t, inv_freq)
    cos = np.concatenate([np.cos(freqs), np.cos(freqs)], axis=-1)
    sin = np.concatenate([np.sin(freqs), np.sin(freqs)], axis=-1)
    return cos, sin


def apply_rope(x: Tensor, cos: np.ndarray, sin: np.ndarray) -> Tensor:
    """
    Apply RoPE to x of shape (..., T, d_head).
    """
    d = x.data.shape[-1]
    x1, x2 = x.data[..., : d // 2], x.data[..., d // 2 :]
    rot = np.concatenate([-x2, x1], axis=-1)
    y = x.data * cos + rot * sin
    out = Tensor(y, (x,))

    def _bw():
        g = out.grad
        g1, g2 = g[..., : d // 2], g[..., d // 2 :]
        grot = np.concatenate([g2, -g1], axis=-1)
        dx = g * cos + grot * sin
        x._accum(dx)

    out._backward = _bw
    return out
