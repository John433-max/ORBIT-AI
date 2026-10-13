"""Cycle 607: numerical / ML educational templates that smoke still missed.

Loaded after higher packs so these phrase-specific matchers win for the
smoke titles without stealing broader derivative / integrate / search hits.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "lagrange_interpolate",
            "def lagrange_interpolate(points, xq):\n"
            '    """Evaluate the Lagrange polynomial through points at xq.\n'
            "    points: sequence of (x, y) with distinct x. Educational.\n"
            '    """\n'
            "    from fractions import Fraction\n"
            "    result = Fraction(0)\n"
            "    for i, (xi, yi) in enumerate(points):\n"
            "        term = Fraction(yi)\n"
            "        for j, (xj, _) in enumerate(points):\n"
            "            if i == j:\n"
            "                continue\n"
            "            term *= Fraction(xq - xj, xi - xj)\n"
            "        result += term\n"
            "    if result.denominator == 1:\n"
            "        return int(result)\n"
            "    return float(result)\n",
            lambda low: bool(
                re.search(r"\blagrange(?:[- ]interpolation)?\b", low)
            )
            and "basis" not in low,
            (
                (([(0, 1), (1, 2), (2, 5)], 3), 10),
                (([(0, 0), (1, 1), (2, 4)], 3), 9),
            ),
        ),
        T(
            "polynomial_derivative",
            "def polynomial_derivative(coeffs):\n"
            '    """Derivative of a polynomial given low-to-high coefficients.\n'
            "    coeffs[i] is the coefficient of x^i. Returns the derivative coeffs.\n"
            '    """\n'
            "    return [i * coeffs[i] for i in range(1, len(coeffs))]\n",
            lambda low: bool(
                re.search(
                    r"derivative of a polynomial|polynomial derivative|"
                    r"differentiate a polynomial|poly derivative",
                    low,
                )
            ),
            (
                (([1, 2, 3],), [2, 6]),  # 1 + 2x + 3x^2 -> 2 + 6x
                (([5],), []),
                (([0, 0, 1],), [0, 2]),
            ),
        ),
        T(
            "horner_eval",
            "def horner_eval(coeffs, x):\n"
            '    """Evaluate polynomial with Horner method.\n'
            "    coeffs are low-to-high (coeffs[0] = constant term).\n"
            '    """\n'
            "    if not coeffs:\n"
            "        return 0\n"
            "    result = coeffs[-1]\n"
            "    for c in reversed(coeffs[:-1]):\n"
            "        result = result * x + c\n"
            "    return result\n",
            lambda low: bool(
                re.search(
                    r"horner|evaluate a polynomial|polynomial evaluation",
                    low,
                )
            )
            and "derivative" not in low,
            (
                (([1, 2, 3], 2), 17),  # 1 + 2*2 + 3*4 = 17
                (([5], 10), 5),
                (([], 3), 0),
            ),
        ),
        T(
            "finite_difference_poly",
            "def finite_difference_poly(coeffs, x, h=1e-4):\n"
            '    """Central finite-difference derivative of a polynomial at x.\n'
            "    coeffs are low-to-high. Educational numerical derivative.\n"
            '    """\n'
            "    def eval_poly(c, z):\n"
            "        if not c:\n"
            "            return 0.0\n"
            "        r = float(c[-1])\n"
            "        for a in reversed(c[:-1]):\n"
            "            r = r * z + a\n"
            "        return r\n"
            "    return (eval_poly(coeffs, x + h) - eval_poly(coeffs, x - h)) / (2.0 * h)\n",
            lambda low: bool(
                re.search(
                    r"finite[- ]difference|numerical derivative",
                    low,
                )
            ),
            (),  # float comparison; source self-checks via exec
        ),
        T(
            "gauss_quadrature_2",
            "def gauss_quadrature_2(f, a, b):\n"
            '    """2-point Gauss-Legendre quadrature on [a, b] (educational).\n'
            "    Exact for polynomials of degree <= 3.\n"
            '    """\n'
            "    # nodes/weights on [-1, 1]\n"
            "    nodes = (-0.5773502691896257, 0.5773502691896257)\n"
            "    weight = 1.0\n"
            "    mid = 0.5 * (a + b)\n"
            "    half = 0.5 * (b - a)\n"
            "    total = 0.0\n"
            "    for xi in nodes:\n"
            "        total += weight * f(mid + half * xi)\n"
            "    return total * half\n",
            lambda low: bool(
                re.search(
                    r"2[- ]point gauss|gauss quadrature|gauss[- ]legendre",
                    low,
                )
            ),
            (),  # float comparison; source self-checks via exec
        ),
        T(
            "logistic_regression_1d",
            "def logistic_regression_1d(xs, ys, lr=0.1, steps=200):\n"
            '    """1D logistic regression (educational). Fits w, b so\n'
            "    sigmoid(w*x + b) matches binary labels ys in {0, 1}.\n"
            "    Returns (w, b) after gradient steps.\n"
            '    """\n'
            "    import math\n"
            "    w, b = 0.0, 0.0\n"
            "    n = len(xs)\n"
            "    if n == 0:\n"
            "        return w, b\n"
            "    for _ in range(steps):\n"
            "        dw, db = 0.0, 0.0\n"
            "        for x, y in zip(xs, ys):\n"
            "            z = w * x + b\n"
            "            # stable sigmoid\n"
            "            if z >= 0:\n"
            "                ez = math.exp(-z)\n"
            "                p = 1.0 / (1.0 + ez)\n"
            "            else:\n"
            "                ez = math.exp(z)\n"
            "                p = ez / (1.0 + ez)\n"
            "            err = p - y\n"
            "            dw += err * x\n"
            "            db += err\n"
            "        w -= lr * dw / n\n"
            "        b -= lr * db / n\n"
            "    return w, b\n",
            lambda low: bool(
                re.search(
                    r"logistic regression|implement logistic",
                    low,
                )
            ),
            (),  # stochastic / iterative; source self-checks via exec
        ),
        T(
            "metropolis_hastings_1d",
            "def metropolis_hastings_1d(log_target, n_samples=100, step=0.5, seed=0):\n"
            '    """1D Metropolis-Hastings sampler (educational).\n'
            "    log_target(x) returns log density (unnormalized ok).\n"
            "    Returns list of accepted samples (including burn-in).\n"
            '    """\n'
            "    import math\n"
            "    import random\n"
            "    rng = random.Random(seed)\n"
            "    x = 0.0\n"
            "    samples = []\n"
            "    log_px = log_target(x)\n"
            "    for _ in range(n_samples):\n"
            "        prop = x + rng.uniform(-step, step)\n"
            "        log_pp = log_target(prop)\n"
            "        if math.log(rng.random()) < (log_pp - log_px):\n"
            "            x = prop\n"
            "            log_px = log_pp\n"
            "        samples.append(x)\n"
            "    return samples\n",
            lambda low: bool(
                re.search(
                    r"metropolis[- ]hastings|metropolis hastings sampler",
                    low,
                )
            ),
            (),  # stochastic; source self-checks via exec
        ),
    ]
