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
            "def secant_method(f, x0=0.0, x1=1.0, tol=1e-8, max_iter=50):\n"
            '    """Secant root finder (educational). f is callable float->float.\\n'
            "    Returns approximate root or last iterate if max_iter hit.\\n"
            '    """\n'
            "    x_prev, x = float(x0), float(x1)\n"
            "    for _ in range(max_iter):\n"
            "        f_prev, f_cur = f(x_prev), f(x)\n"
            "        denom = f_cur - f_prev\n"
            "        if abs(denom) < 1e-15:\n"
            "            return x\n"
            "        x_next = x - f_cur * (x - x_prev) / denom\n"
            "        if abs(x_next - x) < tol:\n"
            "            return x_next\n"
            "        x_prev, x = x, x_next\n"
            "    return x\n",
            lambda low: bool(
                re.search(
                    r"\bsecant(?: method| root)?\b|"
                    r"\bsecant[- ]method\b",
                    low,
                )
            )
            and "newton" not in low,
            [
                ((lambda x: x - 2, 0.0, 3.0), 2.0),
            ],
        ),
        T(
            "extended_euclidean",
            "def extended_euclidean(a, b):\n"
            '    """Extended Euclidean algorithm: returns (g, x, y) with a*x + b*y = g = gcd(a,b).\\n'
            "    Educational pure-Python.\\n"
            '    """\n'
            "    if b == 0:\n"
            "        return a, 1, 0\n"
            "    g, x1, y1 = extended_euclidean(b, a % b)\n"
            "    x = y1\n"
            "    y = x1 - (a // b) * y1\n"
            "    return g, x, y\n",
            lambda low: bool(
                re.search(
                    r"\bextended[- ]euclidean\b|"
                    r"\bbézout\b|"
                    r"\bbezout\b|"
                    r"\bgcd with coefficients\b",
                    low,
                )
            ),
            [
                ((30, 18), (6, -1, 2)),
                ((35, 15), (5, 1, -2)),
            ],
        ),
        T(
            "bisection_method",
            "def bisection_method(f, a, b, tol=1e-8, max_iter=100):\n"
            '    """Bisection root finder on [a,b] where f(a)*f(b) < 0 (educational).\\n'
            "    Returns approximate root.\\n"
            '    """\n'
            "    fa, fb = f(a), f(b)\n"
            "    if fa * fb > 0:\n"
            "        raise ValueError('f(a) and f(b) must have opposite signs')\n"
            "    for _ in range(max_iter):\n"
            "        m = 0.5 * (a + b)\n"
            "        fm = f(m)\n"
            "        if abs(fm) < tol or (b - a) / 2 < tol:\n"
            "            return m\n"
            "        if fa * fm < 0:\n"
            "            b, fb = m, fm\n"
            "        else:\n"
            "            a, fa = m, fm\n"
            "    return 0.5 * (a + b)\n",
            lambda low: bool(
                re.search(
                    r"\bbisection(?: method| root)?\b|"
                    r"\bbisection[- ]method\b",
                    low,
                )
            ),
            [
                ((lambda x: x - 2, 0.0, 4.0), 2.0),
            ],
        ),
        T(
            "lagrange_interpolation",
            "def lagrange_interpolation(xs, ys, x):\n"
            '    """Lagrange polynomial interpolation at point x (educational).\\n'
            "    xs, ys: lists of floats of equal length. Returns float.\\n"
            '    """\n'
            "    n = len(xs)\n"
            "    if n != len(ys):\n"
            "        raise ValueError('xs and ys must have same length')\n"
            "    result = 0.0\n"
            "    for i in range(n):\n"
            "        term = ys[i]\n"
            "        for j in range(n):\n"
            "            if i != j:\n"
            "                term *= (x - xs[j]) / (xs[i] - xs[j])\n"
            "        result += term\n"
            "    return result\n",
            # "lagrange polynomial interpolation" is owned by lagrange_interpolate
            # (test_p277). Bare "lagrange interpolation" stays here (smoke).
            lambda low: bool(
                re.search(r"\blagrange[- ]interpolation\b", low)
            ) and "polynomial" not in low,
            [
                (([0.0, 1.0, 2.0], [1.0, 3.0, 7.0], 1.5), 4.75),
            ],
        ),
        T(
            "simpson_rule",
            "def simpson_rule(f, a, b, n=100):\n"
            '    """Composite Simpson rule for integral from a to b of f(x) dx (educational).\\n'
            "    n must be even. Returns float approximation.\\n"
            '    """\n'
            "    if n % 2 != 0:\n"
            "        n += 1\n"
            "    h = (b - a) / n\n"
            "    s = f(a) + f(b)\n"
            "    for i in range(1, n):\n"
            "        x = a + i * h\n"
            "        s += 4 * f(x) if i % 2 else 2 * f(x)\n"
            "    return s * h / 3\n",
            lambda low: bool(
                re.search(
                    r"\bsimpson(?:s)?(?: rule| integration)?\b|"
                    r"\bsimpson[- ]rule\b",
                    low,
                )
            )
            and "romberg" not in low,
            [
                ((lambda x: x * x, 0.0, 1.0, 2), 1.0 / 3.0),
            ],
        ),
        T(
            "monte_carlo_pi",
            "def monte_carlo_pi(n=10000, seed=42):\n"
            '    """Monte Carlo estimate of pi via unit quarter-circle (educational).\\n'
            "    Returns float approximation of pi. Uses simple LCG for reproducibility.\\n"
            '    """\n'
            "    state = int(seed) & 0xFFFFFFFF\n"
            "    inside = 0\n"
            "    for _ in range(int(n)):\n"
            "        state = (1664525 * state + 1013904223) & 0xFFFFFFFF\n"
            "        x = (state / 4294967296.0) * 2 - 1\n"
            "        state = (1664525 * state + 1013904223) & 0xFFFFFFFF\n"
            "        y = (state / 4294967296.0) * 2 - 1\n"
            "        if x * x + y * y <= 1.0:\n"
            "            inside += 1\n"
            "    return 4.0 * inside / n\n",
            lambda low: bool(
                re.search(
                    r"\bmonte[- ]carlo\s+pi\b|"
                    r"\bestimate\s+pi\b.{0,20}\bmonte\b|"
                    r"\bpi\b.{0,20}\bmonte[- ]carlo\b",
                    low,
                )
            ),
            [
                ((1000, 42), 3.136),
            ],
        ),
    ]
