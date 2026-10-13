"""Cycle 589b: educational 1-D GD fixed objective + related optim demos.

gradient_descent_1d (fixed (x-2)**2), coordinate_descent_2d stub helpers.
"""
from __future__ import annotations

import re
from code_synth import Template


def templates() -> list[Template]:
    return [
        Template(
            "gradient_descent_1d",
            "def gradient_descent_1d(start, steps, lr=0.5):\n"
            "    \"\"\"Minimize (x-2)**2 with gradient descent. Returns final x.\"\"\"\n"
            "    x = float(start)\n"
            "    for _ in range(steps):\n"
            "        grad = 2.0 * (x - 2.0)\n"
            "        x = x - lr * grad\n"
            "    return x\n",
            lambda s: bool(
                re.search(r"\b1[-_ ]?d\b.{0,30}\bgradient[-_ ]?descent\b", s)
                or re.search(r"\bgradient[-_ ]?descent\b.{0,30}\b1[-_ ]?d\b", s)
                or re.search(r"\bgradient[-_ ]?descent\b.{0,40}\bminimize\b", s)
            ),
            examples=(((0, 1), 2.0), ((0, 3), 2.0)),
        ),
    ]
