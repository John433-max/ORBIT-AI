"""Cycle 602: Gram-Schmidt, modified Gram-Schmidt, Householder QR,
Romberg integration, classic RK4, BFGS 1-D (educational).

Pure-Python; no NumPy required.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "gram_schmidt",
            "def gram_schmidt(vectors):\n"
            "    \"\"\"Classical Gram-Schmidt orthogonalization (educational).\n"
            "    vectors: list of list[float] (row vectors), linearly independent.\n"
            "    Returns list of orthonormal vectors.\n"
            "    \"\"\"\n"
            "    import math\n"
            "    basis = []\n"
            "    for v in vectors:\n"
            "        u = list(v)\n"
            "        for b in basis:\n"
            "            proj = sum(ui * bi for ui, bi in zip(u, b))\n"
            "            u = [ui - proj * bi for ui, bi in zip(u, b)]\n"
            "        norm = math.sqrt(sum(x * x for x in u))\n"
            "        if norm < 1e-12:\n"
            "            raise ValueError('vectors are linearly dependent')\n"
            "        basis.append([x / norm for x in u])\n"
            "    def _r(x):\n"
            "        return round(x, 10)\n"
            "    return [[_r(x) for x in row] for row in basis]\n",
            lambda low: bool(
                re.search(
                    r"\bgram[\s\-]?schmidt\b|"
                    r"\bclassical\s+gram[\s\-]?schmidt\b|"
                    r"\bgram[\s\-]?schmidt\s+orthogonal",
                    low,
                )
            )
            and "modified" not in low
            and "householder" not in low,
            examples=(
                (
                    ([[1.0, 1.0, 0.0], [1.0, 0.0, 1.0]],),
                    [
                        [0.7071067812, 0.7071067812, 0.0],
                        [0.4082482905, -0.4082482905, 0.8164965809],
                    ],
                ),
            ),
        ),
        T(
            "modified_gram_schmidt",
            "def modified_gram_schmidt(vectors):\n"
            "    \"\"\"Modified Gram-Schmidt orthogonalization (numerically stabler).\n"
            "    vectors: list of list[float] (row vectors).\n"
            "    Returns list of orthonormal vectors.\n"
            "    \"\"\"\n"
            "    import math\n"
            "    V = [list(v) for v in vectors]\n"
            "    n = len(V)\n"
            "    basis = []\n"
            "    for i in range(n):\n"
            "        u = V[i]\n"
            "        norm = math.sqrt(sum(x * x for x in u))\n"
            "        if norm < 1e-12:\n"
            "            raise ValueError('vectors are linearly dependent')\n"
            "        b = [x / norm for x in u]\n"
            "        basis.append(b)\n"
            "        for j in range(i + 1, n):\n"
            "            proj = sum(V[j][k] * b[k] for k in range(len(b)))\n"
            "            V[j] = [V[j][k] - proj * b[k] for k in range(len(b))]\n"
            "    def _r(x):\n"
            "        return round(x, 10)\n"
            "    return [[_r(x) for x in row] for row in basis]\n",
            lambda low: bool(
                re.search(
                    r"\bmodified\s+gram[\s\-]?schmidt\b|"
                    r"\bmgs\b(?!\w)|"
                    r"\bmodified\s+gs\b",
                    low,
                )
            ),
            examples=(
                (
                    ([[1.0, 1.0, 0.0], [1.0, 0.0, 1.0]],),
                    [
                        [0.7071067812, 0.7071067812, 0.0],
                        [0.4082482905, -0.4082482905, 0.8164965809],
                    ],
                ),
            ),
        ),
        T(
            "householder_qr",
            "def householder_qr(A):\n"
            "    \"\"\"Thin Householder QR: returns R (upper triangular) only (educational).\n"
            "    A: list[list[float]] m x n, m >= n.\n"
            "    Returns R as list[list[float]] (n x n upper).\n"
            "    \"\"\"\n"
            "    import math\n"
            "    m = len(A)\n"
            "    n = len(A[0]) if m else 0\n"
            "    R = [row[:] for row in A]\n"
            "    for k in range(min(m - 1, n)):\n"
            "        x = [R[i][k] for i in range(k, m)]\n"
            "        normx = math.sqrt(sum(t * t for t in x))\n"
            "        if normx < 1e-15:\n"
            "            continue\n"
            "        sign = 1.0 if x[0] >= 0 else -1.0\n"
            "        u0 = x[0] + sign * normx\n"
            "        u = [u0] + x[1:]\n"
            "        normu = math.sqrt(sum(t * t for t in u))\n"
            "        if normu < 1e-15:\n"
            "            continue\n"
            "        v = [t / normu for t in u]\n"
            "        for j in range(k, n):\n"
            "            col = [R[i][j] for i in range(k, m)]\n"
            "            dot = 2.0 * sum(v[i] * col[i] for i in range(len(v)))\n"
            "            for i in range(len(v)):\n"
            "                R[k + i][j] -= dot * v[i]\n"
            "    out = [[round(R[i][j], 10) if i <= j else 0.0 for j in range(n)] for i in range(n)]\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bhouseholder\s*(qr|reflection|reflector)?\b|"
                    r"\bqr\s+via\s+householder\b|"
                    r"\bhouseholder\s+qr\b",
                    low,
                )
            )
            and "gram" not in low,
            examples=(),
        ),
        T(
            "romberg_integrate",
            "def romberg_integrate(f, a, b, max_levels=6):\n"
            "    \"\"\"Romberg integration of f over [a, b] (educational).\n"
            "    f: callable; a, b endpoints; max_levels Richardson table depth.\n"
            "    Returns approximate integral (float).\n"
            "    \"\"\"\n"
            "    def trap(n):\n"
            "        h = (b - a) / n\n"
            "        s = 0.5 * (f(a) + f(b))\n"
            "        for i in range(1, n):\n"
            "            s += f(a + i * h)\n"
            "        return s * h\n"
            "    R = [[0.0] * max_levels for _ in range(max_levels)]\n"
            "    R[0][0] = trap(1)\n"
            "    for k in range(1, max_levels):\n"
            "        R[k][0] = trap(2 ** k)\n"
            "        for j in range(1, k + 1):\n"
            "            R[k][j] = R[k][j - 1] + (R[k][j - 1] - R[k - 1][j - 1]) / (4 ** j - 1)\n"
            "    return round(R[max_levels - 1][max_levels - 1], 10)\n",
            lambda low: bool(
                re.search(
                    r"\bromberg\b|"
                    r"\bromberg\s+(integration|integrate|method)\b",
                    low,
                )
            )
            and "simpson" not in low
            and "trapez" not in low,
            examples=(),
        ),
        T(
            "rk4_integrate",
            "def rk4_integrate(f, y0, t0, t1, n_steps=100):\n"
            "    \"\"\"Classic 4th-order Runge-Kutta for dy/dt = f(t, y) (scalar).\n"
            "    f: callable(t, y); y0 initial; integrate from t0 to t1.\n"
            "    Returns y(t1) rounded.\n"
            "    \"\"\"\n"
            "    h = (t1 - t0) / n_steps\n"
            "    t = float(t0)\n"
            "    y = float(y0)\n"
            "    for _ in range(n_steps):\n"
            "        k1 = f(t, y)\n"
            "        k2 = f(t + 0.5 * h, y + 0.5 * h * k1)\n"
            "        k3 = f(t + 0.5 * h, y + 0.5 * h * k2)\n"
            "        k4 = f(t + h, y + h * k3)\n"
            "        y = y + (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)\n"
            "        t += h\n"
            "    return round(y, 10)\n",
            lambda low: bool(
                re.search(
                    r"\brk4\b|"
                    r"\brunge[\s\-]?kutta\b|"
                    r"\bclassic(al)?\s+rk4\b|"
                    r"\b4th[\s\-]?order\s+runge\b|"
                    r"\bfourth[\s\-]?order\s+runge\b",
                    low,
                )
            )
            and "adaptive" not in low
            and "rk45" not in low
            and "rk23" not in low
            and "exponential" not in low,
            examples=(),
        ),
        T(
            "bfgs_minimize_1d",
            "def bfgs_minimize_1d(f, grad, x0=0.0, max_iter=50, tol=1e-8):\n"
            "    \"\"\"1-D BFGS / quasi-Newton minimize of f (educational).\n"
            "    f: callable(x); grad: callable(x) -> derivative.\n"
            "    Returns (x_min, f(x_min)).\n"
            "    \"\"\"\n"
            "    x = float(x0)\n"
            "    H = 1.0\n"
            "    g = grad(x)\n"
            "    for _ in range(max_iter):\n"
            "        if abs(g) < tol:\n"
            "            break\n"
            "        p = -H * g\n"
            "        alpha = 1.0\n"
            "        fx = f(x)\n"
            "        for _ls in range(20):\n"
            "            if f(x + alpha * p) <= fx + 1e-4 * alpha * g * p:\n"
            "                break\n"
            "            alpha *= 0.5\n"
            "        s = alpha * p\n"
            "        x_new = x + s\n"
            "        g_new = grad(x_new)\n"
            "        y = g_new - g\n"
            "        if abs(y) > 1e-16 and abs(s) > 1e-16:\n"
            "            H = (s / y) if abs(y) > 1e-16 else H\n"
            "            if H <= 0:\n"
            "                H = 1.0\n"
            "        x, g = x_new, g_new\n"
            "    return round(x, 10), round(f(x), 10)\n",
            lambda low: bool(
                re.search(
                    r"\bbfgs\b|"
                    r"\bquasi[\s\-]?newton\b|"
                    r"\bbroyden\s+fletcher\b",
                    low,
                )
            )
            and "lbfgs" not in low
            and "l-bfgs" not in low,
            examples=(),
        ),
    ]
