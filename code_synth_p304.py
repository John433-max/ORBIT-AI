"""Cycle 602b: RK4 exponential, scalar Kalman, power iteration, Walker alias,
1-D convolution, trapezoidal rule — close test_p300_numerical_sampling gaps.

Pure-Python educational; no NumPy required.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "rk4_exponential",
            "def rk4_exponential(y0=1.0, t1=1.0, n_steps=100):\n"
            "    \"\"\"RK4 integrate y'=y from 0 to t1 starting at y0 (educational).\\n"
            "    Returns y(t1) approx e^{t1}*y0.\\n"
            "    \"\"\"\n"
            "    h = t1 / n_steps\n"
            "    t = 0.0\n"
            "    y = float(y0)\n"
            "    for _ in range(n_steps):\n"
            "        k1 = y\n"
            "        k2 = y + 0.5 * h * k1\n"
            "        k3 = y + 0.5 * h * k2\n"
            "        k4 = y + h * k3\n"
            "        y = y + (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)\n"
            "        t += h\n"
            "    return round(y, 10)\n",
            lambda low: bool(
                re.search(
                    r"\brk4\b.*\bexponential\b|"
                    r"\brunge[\s\-]?kutta\b.*\bexponential\b|"
                    r"\bexponential\b.*\brk4\b|"
                    r"\brk4_exponential\b",
                    low,
                )
            ),
            examples=((tuple(), 2.7182818282),),
        ),
        T(
            "kalman_1d",
            "def kalman_1d(measurements, q=1e-5, r=0.1, x0=0.0, p0=1.0):\n"
            "    \"\"\"Scalar Kalman filter (educational).\\n"
            "    measurements: list[float]; q process noise, r measurement noise.\\n"
            "    Returns list of filtered estimates.\\n"
            "    \"\"\"\n"
            "    x, p = float(x0), float(p0)\n"
            "    out = []\n"
            "    for z in measurements:\n"
            "        # predict\n"
            "        p = p + q\n"
            "        # update\n"
            "        k = p / (p + r)\n"
            "        x = x + k * (z - x)\n"
            "        p = (1 - k) * p\n"
            "        out.append(round(x, 10))\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bkalman\b|"
                    r"\bscalar\s+kalman\b|"
                    r"\bkalman\s+filter\b",
                    low,
                )
            )
            and "particle" not in low,
            examples=(),
        ),
        T(
            "power_iteration",
            "def power_iteration(A, n_iter=50, tol=1e-10):\n"
            "    \"\"\"Power iteration for dominant eigenvalue / eigenvector (educational).\\n"
            "    A: list[list[float]] n x n. Returns (eigenvalue, eigenvector).\\n"
            "    \"\"\"\n"
            "    import math\n"
            "    n = len(A)\n"
            "    b = [1.0] * n\n"
            "    for _ in range(n_iter):\n"
            "        # Ab\n"
            "        Ab = [sum(A[i][j] * b[j] for j in range(n)) for i in range(n)]\n"
            "        norm = math.sqrt(sum(x * x for x in Ab))\n"
            "        if norm < 1e-15:\n"
            "            break\n"
            "        b_new = [x / norm for x in Ab]\n"
            "        if max(abs(b_new[i] - b[i]) for i in range(n)) < tol:\n"
            "            b = b_new\n"
            "            break\n"
            "        b = b_new\n"
            "    # Rayleigh quotient\n"
            "    Ab = [sum(A[i][j] * b[j] for j in range(n)) for i in range(n)]\n"
            "    lam = sum(b[i] * Ab[i] for i in range(n))\n"
            "    return round(lam, 10), [round(x, 10) for x in b]\n",
            lambda low: bool(
                re.search(
                    r"\bpower\s+iteration\b|"
                    r"\bpower\s+method\b|"
                    r"\bdominant\s+eigenvalue\b",
                    low,
                )
            ),
            examples=(),
        ),
        T(
            "alias_sample",
            "def alias_sample(probs, n_samples=10, seed=0):\n"
            "    \"\"\"Walker alias method discrete sampling (educational).\\n"
            "    probs: list[float] non-negative (need not sum to 1).\\n"
            "    Returns list of index samples.\\n"
            "    \"\"\"\n"
            "    import random\n"
            "    n = len(probs)\n"
            "    s = sum(probs) or 1.0\n"
            "    scaled = [p * n / s for p in probs]\n"
            "    small, large = [], []\n"
            "    for i, p in enumerate(scaled):\n"
            "        (small if p < 1.0 else large).append(i)\n"
            "    prob = [0.0] * n\n"
            "    alias = [0] * n\n"
            "    while small and large:\n"
            "        s_i = small.pop()\n"
            "        l_i = large.pop()\n"
            "        prob[s_i] = scaled[s_i]\n"
            "        alias[s_i] = l_i\n"
            "        scaled[l_i] = scaled[l_i] - (1.0 - scaled[s_i])\n"
            "        (small if scaled[l_i] < 1.0 else large).append(l_i)\n"
            "    for i in large + small:\n"
            "        prob[i] = 1.0\n"
            "        alias[i] = i\n"
            "    rng = random.Random(seed)\n"
            "    out = []\n"
            "    for _ in range(n_samples):\n"
            "        i = rng.randrange(n)\n"
            "        out.append(i if rng.random() < prob[i] else alias[i])\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\balias\s+(method|sample|sampling)\b|"
                    r"\bwalker\s+alias\b|"
                    r"\balias_sample\b",
                    low,
                )
            ),
            examples=(),
        ),
        T(
            "convolution_1d",
            "def convolution_1d(a, b):\n"
            "    \"\"\"Full 1-D discrete convolution (educational).\\n"
            "    a, b: list[float]. Returns list of length len(a)+len(b)-1.\\n"
            "    \"\"\"\n"
            "    n, m = len(a), len(b)\n"
            "    out = [0.0] * (n + m - 1)\n"
            "    for i in range(n):\n"
            "        for j in range(m):\n"
            "            out[i + j] += a[i] * b[j]\n"
            "    return [round(x, 10) for x in out]\n",
            lambda low: bool(
                re.search(
                    r"\b(1d|1-d|one[\s\-]?dimensional)\s+convolution\b|"
                    r"\bdiscrete\s+convolution\b|"
                    r"\bconvolution_1d\b|"
                    r"\bconvolve\b",
                    low,
                )
            )
            and "fft" not in low
            and "2d" not in low,
            examples=((([1, 2, 3], [0, 1, 0.5]), [0.0, 1.0, 2.5, 4.0, 1.5]),),
        ),
        T(
            "trapezoidal_integrate",
            "def trapezoidal_integrate(f, a, b, n=100):\n"
            "    \"\"\"Composite trapezoidal rule for integral of f on [a,b] (educational).\\n"
            "    f: callable; n subintervals.\\n"
            "    \"\"\"\n"
            "    h = (b - a) / n\n"
            "    s = 0.5 * (f(a) + f(b))\n"
            "    for i in range(1, n):\n"
            "        s += f(a + i * h)\n"
            "    return round(s * h, 10)\n",
            lambda low: bool(
                re.search(
                    r"\btrapezoid(al)?\s*(rule|integrat)?\b|"
                    r"\btrapezoidal_integrate\b",
                    low,
                )
            )
            and "romberg" not in low
            and "simpson" not in low,
            examples=(),
        ),
    ]
