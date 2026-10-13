"""Cycle 601: residual block, GELU, SiLU/Swish, RMSNorm, sinusoidal PE, dropout.

Closes probe gaps from Cycle 600 next-target list. Pure-Python educational;
no NumPy required.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "residual_block",
            "def residual_block(x, weight1, bias1, weight2, bias2):\n"
            '    """Two-layer residual (MLP) block: x + W2*relu(W1*x+b1)+b2 (educational).\n'
            "    x, bias*: list[float]; weight*: list[list[float]] (out x in).\n"
            "    Returns list[float] same length as x (requires matching dims).\n"
            '    """\n'
            "    def matvec(W, v):\n"
            "        return [sum(W[i][j] * v[j] for j in range(len(v))) for i in range(len(W))]\n"
            "    def add(a, b):\n"
            "        return [a[i] + b[i] for i in range(len(a))]\n"
            "    def relu(v):\n"
            "        return [max(0.0, t) for t in v]\n"
            "    h = relu(add(matvec(weight1, x), bias1))\n"
            "    y = add(matvec(weight2, h), bias2)\n"
            "    return add(x, y)\n",
            lambda low: bool(
                re.search(
                    r"\bresidual\s+block\b|"
                    r"\bresnet\s+block\b|"
                    r"\bskip\s+connection\s+block\b|"
                    r"\bimplement\s+residual\b",
                    low,
                )
            )
            and "tree" not in low
            and "path" not in low,
            examples=(
                (
                    (
                        [1.0, 2.0],
                        [[1.0, 0.0], [0.0, 1.0]],
                        [0.0, 0.0],
                        [[1.0, 0.0], [0.0, 1.0]],
                        [0.0, 0.0],
                    ),
                    [2.0, 4.0],
                ),
            ),
        ),
        T(
            "gelu",
            "def gelu(x):\n"
            '    """Gaussian Error Linear Unit (approximate) for scalar or list (educational).\n'
            "    Uses tanh approximation: 0.5*x*(1+tanh(sqrt(2/pi)*(x+0.044715*x^3))).\n"
            '    """\n'
            "    import math\n"
            "    def _g(t):\n"
            "        return 0.5 * t * (1.0 + math.tanh(math.sqrt(2.0 / math.pi) * (t + 0.044715 * t * t * t)))\n"
            "    if isinstance(x, (list, tuple)):\n"
            "        return [round(_g(float(t)), 10) for t in x]\n"
            "    return round(_g(float(x)), 10)\n",
            lambda low: bool(
                re.search(
                    r"\bgelu\b|"
                    r"\bgaussian\s+error\s+linear\s+unit\b|"
                    r"\bgelu\s+activation\b",
                    low,
                )
            )
            and "relu" not in low
            and "silu" not in low,
            examples=(
                ((0.0,), 0.0),
                ((1.0,), round(0.5 * 1.0 * (1.0 + __import__("math").tanh(__import__("math").sqrt(2.0 / __import__("math").pi) * (1.0 + 0.044715))), 10)),
            ),
        ),
        T(
            "silu",
            "def silu(x):\n"
            '    """SiLU / Swish activation: x * sigmoid(x) for scalar or list (educational).\n'
            '    """\n'
            "    import math\n"
            "    def _s(t):\n"
            "        return t / (1.0 + math.exp(-t))\n"
            "    if isinstance(x, (list, tuple)):\n"
            "        return [round(_s(float(t)), 10) for t in x]\n"
            "    return round(_s(float(x)), 10)\n",
            lambda low: bool(
                re.search(
                    r"\bsilu\b|"
                    r"\bswish\b|"
                    r"\bsilu\s+activation\b|"
                    r"\bswish\s+activation\b",
                    low,
                )
            )
            and "gelu" not in low
            and "relu" not in low,
            examples=(
                ((0.0,), 0.0),
                ((1.0,), round(1.0 / (1.0 + __import__("math").exp(-1.0)), 10)),
            ),
        ),
        T(
            "rmsnorm",
            "def rmsnorm(x, weight=None, eps=1e-6):\n"
            '    """Root-mean-square layer norm (no mean centering) (educational).\n'
            "    x: list[float]; weight: optional list[float] scale (same len).\n"
            "    Returns normalized list[float].\n"
            '    """\n'
            "    import math\n"
            "    n = len(x)\n"
            "    ms = sum(t * t for t in x) / n\n"
            "    inv = 1.0 / math.sqrt(ms + eps)\n"
            "    y = [t * inv for t in x]\n"
            "    if weight is not None:\n"
            "        y = [y[i] * weight[i] for i in range(n)]\n"
            "    return [round(t, 10) for t in y]\n",
            lambda low: bool(
                re.search(
                    r"\brmsnorm\b|"
                    r"\brms\s*norm\b|"
                    r"\broot\s*mean\s*square\s*(layer\s*)?norm\b|"
                    r"\brms\s+layer\s+norm\b",
                    low,
                )
            )
            and "batch" not in low
            and "layer_normalization" not in low,
            examples=(
                (([3.0, 4.0],), [0.8485281035, 1.1313708046]),
            ),
        ),
        T(
            "sinusoidal_positional_encoding",
            "def sinusoidal_positional_encoding(seq_len, d_model):\n"
            '    """Sinusoidal positional encodings (Vaswani et al.) (educational).\n'
            "    Returns list[list[float]] of shape (seq_len, d_model).\n"
            '    """\n'
            "    import math\n"
            "    pe = [[0.0] * d_model for _ in range(seq_len)]\n"
            "    for pos in range(seq_len):\n"
            "        for i in range(0, d_model, 2):\n"
            "            div = 10000.0 ** (i / d_model)\n"
            "            pe[pos][i] = math.sin(pos / div)\n"
            "            if i + 1 < d_model:\n"
            "                pe[pos][i + 1] = math.cos(pos / div)\n"
            "    def _r(row):\n"
            "        return [round(v, 8) for v in row]\n"
            "    return [_r(row) for row in pe]\n",
            lambda low: bool(
                re.search(
                    r"\bsinusoidal\s+positional\s+encoding\b|"
                    r"\bpositional\s+encoding\s+sinusoidal\b|"
                    r"\bsine\s+positional\s+encoding\b|"
                    r"\btransformer\s+positional\s+encoding\b|"
                    r"\bwrite\s+positional\s+encoding\b",
                    low,
                )
            )
            and "rope" not in low
            and "rotary" not in low,
            examples=(
                (
                    (2, 4),
                    [
                        [0.0, 1.0, 0.0, 1.0],
                        [
                            round(__import__("math").sin(1.0), 8),
                            round(__import__("math").cos(1.0), 8),
                            round(__import__("math").sin(1.0 / 100.0), 8),
                            round(__import__("math").cos(1.0 / 100.0), 8),
                        ],
                    ],
                ),
            ),
        ),
        T(
            "dropout",
            "def dropout(x, p=0.5, seed=0):\n"
            '    """Inverted dropout (train-time) with fixed seed (educational).\n'
            "    x: list[float]; p: drop probability; returns scaled surviving values.\n"
            "    Deterministic via seed for self-check.\n"
            '    """\n'
            "    import random\n"
            "    rng = random.Random(seed)\n"
            "    if p <= 0.0:\n"
            "        return list(x)\n"
            "    if p >= 1.0:\n"
            "        return [0.0] * len(x)\n"
            "    scale = 1.0 / (1.0 - p)\n"
            "    out = []\n"
            "    for t in x:\n"
            "        if rng.random() < p:\n"
            "            out.append(0.0)\n"
            "        else:\n"
            "            out.append(round(t * scale, 10))\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bdropout\b|"
                    r"\bdropout\s+layer\b|"
                    r"\binverted\s+dropout\b|"
                    r"\bimplement\s+dropout\b",
                    low,
                )
            )
            and "rate" not in low
            and "schedule" not in low,
            examples=(
                (([1.0, 1.0, 1.0, 1.0], 0.0, 0), [1.0, 1.0, 1.0, 1.0]),
            ),
        ),
    ]
