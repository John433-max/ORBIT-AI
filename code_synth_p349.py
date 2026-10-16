"""Cycle 638 (p349): bisection_root + simpson_integrate_1d for CI unit/smoke."""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "bisection_root",
            '''def bisection_root(f, a, b, tol=1e-6, max_iter=50):
    """Find a root of f in [a, b] by bisection (educational).

    Assumes f(a) and f(b) have opposite signs.
    """
    fa, fb = f(a), f(b)
    if fa * fb > 0:
        raise ValueError("root not bracketed")
    for _ in range(max_iter):
        mid = (a + b) / 2.0
        fm = f(mid)
        if abs(fm) < tol or (b - a) / 2.0 < tol:
            return mid
        if fa * fm < 0:
            b, fb = mid, fm
        else:
            a, fa = mid, fm
    return (a + b) / 2.0


def bisection_method(f, a, b, tol=1e-6, max_iter=50):
    """Alias for bisection_root (educational)."""
    return bisection_root(f, a, b, tol, max_iter)
''',
            lambda low: bool(
                re.search(r"\bbisection\b", low)
                and re.search(r"\b(finding|zero)\b", low)
            ),
            (
                ((lambda x: x * x - 2, 1.0, 2.0), 1.4142141342163086),
            ),
        ),
        T(
            "simpson_integrate_1d",
            '''def simpson_integrate_1d(f, a, b, n=50):
    """Composite Simpson's rule for integral from a to b of f(x) dx (educational).

    n is the number of subintervals (made even).
    """
    n = int(n)
    if n % 2 == 1:
        n += 1
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        x = a + i * h
        s += (4 if i % 2 else 2) * f(x)
    return s * h / 3.0


def simpson_rule(f, a, b, n=50):
    """Alias for simpson_integrate_1d (educational)."""
    return simpson_integrate_1d(f, a, b, n)
''',
            lambda low: bool(
                re.search(r"\bsimpson\b", low)
                and re.search(r"\bintegrat(?:e|ion)?\b", low)
                and "rule" not in low
            ),
            (
                ((lambda x: x * x, 0.0, 1.0), 1.0 / 3.0),
            ),
        ),
        T(
            "secant_root",
            "def secant_root(f, x0, x1, tol=1e-8, max_iter=50):\n"
            '    """Secant method root finder (educational)."""\n'
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
                re.search(r"\bsecant\b", low)
                and "root" in low
                and "finder" not in low
                and "newton" not in low
            ),
            examples=[((lambda x: x - 2, 0.0, 3.0), 2.0)],
        ),
    ]
