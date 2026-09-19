"""RMSNorm (Root Mean Square Layer Normalization)."""

from __future__ import annotations

from autograd import Tensor


def rmsnorm(x: Tensor, weight: Tensor, eps: float = 1e-6) -> Tensor:
    """
    RMSNorm: x * weight / sqrt(mean(x^2) + eps)
    No mean subtraction, no bias — standard in modern decoder-only models.
    x: (..., D)
    weight: (D,)
    """
    ms = (x * x).mean(axis=-1, keepdims=True)
    inv = (ms + eps).sqrt().pow(-1.0)
    return x * inv * weight
