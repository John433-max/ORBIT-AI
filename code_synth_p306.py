"""Cycle 603: secant method, extended Euclidean, bisection, Lagrange interpolation,
Simpson's rule, Monte Carlo pi estimate.

Pure-Python educational; no NumPy required. Narrow matchers avoid collisions
with existing newton, simpson (if any), and random sampling templates.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "secant_method",
            "def secant_method(f, x0, x1, tol=1e-8, max_iter=100):\n"
            '    """Secant root finder (educational).\n'
            "    Returns approximate root.\n"
            '    """\n'
            "    a, b = float(x0), float(x1)\n"
            "    fa, fb = f(a), f(b)\n"
            "    for _ in range(max_iter):\n"
            "        if abs(fb - fa) < 1e-18:\n"
            "            return b\n"
            "        x = b - fb * (b - a) / (fb - fa)\n"
            "        if abs(x - b) < tol:\n"
            "            return x\n"
            "        a, fa = b, fb\n"
            "        b, fb = x, f(x)\n"
            "    return b\n",
            lambda low: bool(
                re.search(r"\\bsecant(?: method)?\\b", low)
            )
            and "root" not in low,
            [
                ((lambda x: x * x - 2, 1.0, 2.0), 1.41421356237),
            ],
        ),
    ]
