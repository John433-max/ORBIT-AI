"""Cycle 626 (p332): Inference BatchNorm with running statistics.

Ioffe & Szegedy 2015: at inference, y = gamma * (x - mu) / sqrt(var + eps) + beta
using the tracked running mean and variance (no mini-batch stats).

Highest pack so "running stats" prefers this over p331 batch_norm_1d.
"""
from __future__ import annotations

import math
import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "batch_norm_running",
            '''def batch_norm_running(x, running_mean, running_var, eps=1e-5, gamma=1.0, beta=0.0):
    """Inference BatchNorm with running statistics (Ioffe & Szegedy 2015).

    y = gamma * (x - running_mean) / sqrt(running_var + eps) + beta.
    Pure inference path: no mini-batch mean/var, no EMA update.
    """
    import math
    inv = 1.0 / math.sqrt(float(running_var) + float(eps))
    g = float(gamma)
    b = float(beta)
    mu = float(running_mean)
    return [g * (float(v) - mu) * inv + b for v in x]
''',
            lambda low: bool(
                re.search(
                    r"\bbatch[ _-]?norm(?:alization)?\b.{0,40}\brunning\b|"
                    r"\brunning[ _-]?(?:mean|var|stats|statistics)\b.{0,40}\bbatch[ _-]?norm|"
                    r"\bbatch_norm_running\b|"
                    r"\binference[ _-]?batch[ _-]?norm\b",
                    low,
                )
            )
            and "group" not in low
            and "instance" not in low,
            (
                # mean=2, var=1, eps=0 → (1-2)/1 = -1, (3-2)/1 = 1
                (([1.0, 3.0], 2.0, 1.0, 0.0), [-1.0, 1.0]),
                # affine: gamma=2, beta=1, mean=0, var=1 → 2*(5-0)/1+1=11, 2*(-1)/1+1=-1
                (([5.0, -1.0], 0.0, 1.0, 0.0, 2.0, 1.0), [11.0, -1.0]),
                # empty
                (([], 0.0, 1.0), []),
            ),
        ),
    ]
