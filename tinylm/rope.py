"""RoPE frequency helpers shared by NumPy and Torch TinyLM."""

from __future__ import annotations

import numpy as np


def rope_inv_freq(
    head_dim: int,
    theta: float,
    scaling: str = "none",
    factor: float = 1.0,
    orig_ctx: int = 64,
    yarn_alpha: float = 1.0,
    yarn_beta: float = 32.0,
) -> np.ndarray:
    """Inverse frequencies for even/odd RoPE pairs, shape (head_dim/2,).

    scaling:
      - none: standard RoPE (factor ignored)
      - linear: position interpolation (divide frequencies by factor)
      - ntk: NTK-aware base rescale  theta * factor^(d/(d-2))
      - yarn: blend linear-interp (low freq) and original (high freq)
    """
    dim_ids = np.arange(0, head_dim, 2, dtype=np.float64)
    d = float(head_dim)
    inv = theta ** (-dim_ids / d)
    scaling = (scaling or "none").lower()
    if factor <= 1.0 or scaling in ("none", "", "off"):
        return inv.astype(np.float32)
    if scaling == "linear":
        return (inv / factor).astype(np.float32)
    if scaling == "ntk":
        theta_s = theta * (factor ** (d / (d - 2.0)))
        return (theta_s ** (-dim_ids / d)).astype(np.float32)
    if scaling == "yarn":
        wavelength = 2.0 * np.pi / np.maximum(inv, 1e-20)
        r = orig_ctx / wavelength
        ramp = np.clip((r - yarn_alpha) / max(yarn_beta - yarn_alpha, 1e-6), 0.0, 1.0)
        mixed = (1.0 - ramp) * (inv / factor) + ramp * inv
        return mixed.astype(np.float32)
    raise ValueError(f"unknown rope_scaling {scaling!r}")


def yarn_attn_scale(scaling: str, factor: float) -> float:
    """YaRN attention temperature t = 0.1 ln(s) + 1; scores *= 1/t."""
    if (scaling or "none").lower() != "yarn" or factor <= 1.0:
        return 1.0
    t = 0.1 * float(np.log(factor)) + 1.0
    return 1.0 / t
