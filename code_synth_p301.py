"""Cycle 601: MSE / MAE / binary cross-entropy educational losses.

Closes remaining ML-probe gaps after Cycle 600 (cross_entropy_loss is
categorical). Pure-Python; no NumPy required. Matchers are narrow so
they do not steal existing helpers (mean, absolute, cross_entropy).
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "mse_loss",
            "def mse_loss(y_true, y_pred):\n"
            '    """Mean squared error (regression loss, educational).\n'
            "    y_true, y_pred: sequences of numbers, same length.\n"
            "    Returns average of squared differences.\n"
            '    """\n'
            "    if len(y_true) != len(y_pred) or not y_true:\n"
            "        raise ValueError('y_true and y_pred must be non-empty and same length')\n"
            "    total = 0.0\n"
            "    for yt, yp in zip(y_true, y_pred):\n"
            "        d = float(yt) - float(yp)\n"
            "        total += d * d\n"
            "    return total / len(y_true)\n",
            lambda low: bool(
                re.search(
                    r"\bmse\b|\bmean\s+squared\s+error\b|"
                    r"\bsquared\s+error\s+loss\b|\bl2\s+loss\b",
                    low,
                )
            )
            and "mae" not in low
            and "absolute" not in low
            and "cross" not in low
            and "entropy" not in low,
            examples=(
                (([3, -0.5, 2, 7], [2.5, 0.0, 2, 8]), 0.375),
                (([1, 2, 3], [1, 2, 3]), 0.0),
            ),
        ),
        T(
            "mae_loss",
            "def mae_loss(y_true, y_pred):\n"
            '    """Mean absolute error (regression loss, educational).\n'
            "    y_true, y_pred: sequences of numbers, same length.\n"
            "    Returns average of absolute differences.\n"
            '    """\n'
            "    if len(y_true) != len(y_pred) or not y_true:\n"
            "        raise ValueError('y_true and y_pred must be non-empty and same length')\n"
            "    total = 0.0\n"
            "    for yt, yp in zip(y_true, y_pred):\n"
            "        total += abs(float(yt) - float(yp))\n"
            "    return total / len(y_true)\n",
            # Prefer explicit "loss" so p176 `mae` keeps plain
            # "mean absolute error of two lists" / "mae of …".
            lambda low: bool(
                re.search(
                    r"\bmae\s*loss\b|"
                    r"\bmean\s+absolute\s+error\s+loss\b|"
                    r"\babsolute\s+error\s+loss\b|\bl1\s+loss\b",
                    low,
                )
            )
            and "mse" not in low
            and "squared" not in low
            and "cross" not in low
            and "entropy" not in low,
            examples=(
                (([3, -0.5, 2, 7], [2.5, 0.0, 2, 8]), 0.5),
                (([1, 2, 3], [1, 2, 3]), 0.0),
            ),
        ),
        T(
            "binary_cross_entropy",
            "def binary_cross_entropy(y_true, y_pred, eps=1e-12):\n"
            '    """Binary cross-entropy / log-loss (educational).\n'
            "    y_true: 0/1 labels; y_pred: probabilities in (0,1).\n"
            "    Returns mean of -y*log(p) -(1-y)*log(1-p). Clips p for stability.\n"
            '    """\n'
            "    import math\n"
            "    if len(y_true) != len(y_pred) or not y_true:\n"
            "        raise ValueError('y_true and y_pred must be non-empty and same length')\n"
            "    total = 0.0\n"
            "    n = len(y_true)\n"
            "    for yt, yp in zip(y_true, y_pred):\n"
            "        p = min(max(float(yp), eps), 1.0 - eps)\n"
            "        y = float(yt)\n"
            "        total += -y * math.log(p) - (1.0 - y) * math.log(1.0 - p)\n"
            "    return round(total / n, 8)\n",
            lambda low: bool(
                re.search(
                    r"\bbinary\s+cross[-\s]?entropy\b|"
                    r"\bbce\b|\blog\s*loss\b|"
                    r"\bbinary\s+log[-\s]?loss\b",
                    low,
                )
            )
            and "categorical" not in low
            and "multi" not in low
            and "softmax" not in low,
            examples=(
                (
                    ([1, 0, 1], [0.9, 0.1, 0.8]),
                    0.14462153,
                ),
                (
                    ([1, 0], [0.999, 0.001]),
                    0.0010005,
                ),
            ),
        ),
    ]
