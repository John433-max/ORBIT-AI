"""Cycle 606: SSOR, inverse power iteration, Rayleigh quotient iteration,
Nelder-Mead, Halley, Muller.

Pure-Python educational; no NumPy. Narrow matchers + sibling-token upgrade
avoid stealing successive_over_relaxation, power_iteration, steepest_descent_2d.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "symmetric_successive_over_relaxation",
            "def symmetric_successive_over_relaxation(A, b, omega=1.1, tol=1e-8, max_iter=30):\n"
            '    """Symmetric Successive Over-Relaxation (SSOR) for Ax = b (educational).\n'
            "    Forward then backward SOR sweep with the same relaxation factor omega.\n"
            "    Reduces to Gauss-Seidel when omega == 1. Returns approximate solution list.\n"
            '    """\n'
            "    n = len(A)\n"
            "    x = [0.0] * n\n"
            "    for _ in range(max_iter):\n"
            "        x_old = x[:]\n"
            "        for i in range(n):\n"
            "            s = b[i]\n"
            "            for j in range(n):\n"
            "                if j != i:\n"
            "                    s -= A[i][j] * x[j]\n"
            "            x[i] = (1 - omega) * x[i] + omega * (s / A[i][i])\n"
            "        for i in range(n - 1, -1, -1):\n"
            "            s = b[i]\n"
            "            for j in range(n):\n"
            "                if j != i:\n"
            "                    s -= A[i][j] * x[j]\n"
            "            x[i] = (1 - omega) * x[i] + omega * (s / A[i][i])\n"
            "        if max(abs(x[i] - x_old[i]) for i in range(n)) < tol:\n"
            "            break\n"
            "    return x\n",
            lambda low: bool(
                re.search(
                    r"\bssor\b|"
                    r"\bsymmetric[- ]successive[- ]over[- ]relaxation\b|"
                    r"\bsymmetric[- ]over[- ]relaxation\b",
                    low,
                )
            ),
            [
                (([[4.0, 1.0], [1.0, 3.0]], [1.0, 2.0], 1.1, 1e-8, 30),
                 [0.09090909091055663, 0.6363636356546896]),
            ],
        ),
        T(
            "inverse_power_iteration",
            "def inverse_power_iteration(A, mu=0.0, tol=1e-10, max_iter=20):\n"
            '    """Inverse power iteration for an eigenvalue near mu (educational).\n'
            "    Solves (A - mu I) y = v each step with Gaussian elimination, then normalizes.\n"
            "    Returns (eigenvector, Rayleigh quotient).\n"
            '    """\n'
            "    n = len(A)\n"
            "    v = [1.0] * n\n"
            "    def solve(M, rhs):\n"
            "        M = [row[:] for row in M]\n"
            "        r = rhs[:]\n"
            "        for i in range(n):\n"
            "            piv = i\n"
            "            for k in range(i + 1, n):\n"
            "                if abs(M[k][i]) > abs(M[piv][i]):\n"
            "                    piv = k\n"
            "            M[i], M[piv] = M[piv], M[i]\n"
            "            r[i], r[piv] = r[piv], r[i]\n"
            "            diag = M[i][i]\n"
            "            for j in range(i, n):\n"
            "                M[i][j] /= diag\n"
            "            r[i] /= diag\n"
            "            for k in range(n):\n"
            "                if k == i:\n"
            "                    continue\n"
            "                factor = M[k][i]\n"
            "                for j in range(i, n):\n"
            "                    M[k][j] -= factor * M[i][j]\n"
            "                r[k] -= factor * r[i]\n"
            "        return r\n"
            "    for _ in range(max_iter):\n"
            "        v_old = v[:]\n"
            "        M = [[A[i][j] - (mu if i == j else 0.0) for j in range(n)] for i in range(n)]\n"
            "        y = solve(M, v)\n"
            "        norm = max(abs(yi) for yi in y) or 1.0\n"
            "        v = [yi / norm for yi in y]\n"
            "        if max(abs(v[i] - v_old[i]) for i in range(n)) < tol:\n"
            "            break\n"
            "    Av = [sum(A[i][j] * v[j] for j in range(n)) for i in range(n)]\n"
            "    rq = sum(v[i] * Av[i] for i in range(n)) / (sum(v[i] * v[i] for i in range(n)) or 1.0)\n"
            "    return v, rq\n",
            lambda low: bool(
                re.search(
                    r"\binverse[- ]power[- ]iteration\b|"
                    r"\binverse[- ]iteration\b|"
                    r"\binverse power\b",
                    low,
                )
            )
            and "rayleigh" not in low,
            [
                (([[2.0, 1.0], [1.0, 2.0]], 0.0, 1e-10, 20),
                 ([1.0, 0.9999999999999999], 3.0000000000000004)),
            ],
        ),
        T(
            "rayleigh_quotient_iteration",
            "def rayleigh_quotient_iteration(A, v0=None, tol=1e-10, max_iter=12):\n"
            '    """Rayleigh quotient iteration for an eigenvalue (educational).\n'
            "    Updates the shift with the Rayleigh quotient each step and solves with a\n"
            "    small jitter if the shifted matrix is singular. Returns (vector, quotient).\n"
            '    """\n'
            "    n = len(A)\n"
            "    v = [1.0] * n if v0 is None else list(v0)\n"
            "    def solve(M, rhs):\n"
            "        M = [row[:] for row in M]\n"
            "        r = rhs[:]\n"
            "        for i in range(n):\n"
            "            piv = max(range(i, n), key=lambda k: abs(M[k][i]))\n"
            "            M[i], M[piv] = M[piv], M[i]\n"
            "            r[i], r[piv] = r[piv], r[i]\n"
            "            diag = M[i][i]\n"
            "            if abs(diag) < 1e-14:\n"
            "                diag = 1e-12\n"
            "                M[i][i] = diag\n"
            "            for j in range(i, n):\n"
            "                M[i][j] /= diag\n"
            "            r[i] /= diag\n"
            "            for k in range(n):\n"
            "                if k == i:\n"
            "                    continue\n"
            "                factor = M[k][i]\n"
            "                for j in range(i, n):\n"
            "                    M[k][j] -= factor * M[i][j]\n"
            "                r[k] -= factor * r[i]\n"
            "        return r\n"
            "    for _ in range(max_iter):\n"
            "        Av = [sum(A[i][j] * v[j] for j in range(n)) for i in range(n)]\n"
            "        rq = sum(v[i] * Av[i] for i in range(n)) / (sum(v[i] * v[i] for i in range(n)) or 1.0)\n"
            "        M = [[A[i][j] - (rq if i == j else 0.0) for j in range(n)] for i in range(n)]\n"
            "        y = solve(M, v)\n"
            "        norm = max(abs(yi) for yi in y) or 1.0\n"
            "        v_new = [yi / norm for yi in y]\n"
            "        if max(abs(abs(v_new[i]) - abs(v[i])) for i in range(n)) < tol:\n"
            "            v = v_new\n"
            "            break\n"
            "        v = v_new\n"
            "    Av = [sum(A[i][j] * v[j] for j in range(n)) for i in range(n)]\n"
            "    rq = sum(v[i] * Av[i] for i in range(n)) / (sum(v[i] * v[i] for i in range(n)) or 1.0)\n"
            "    return v, rq\n",
            lambda low: bool(
                re.search(
                    r"\brayleigh[- ]quotient[- ]iteration\b|"
                    r"\brayleigh[- ]iteration\b|"
                    r"\brayleigh[- ]quotient\b|"
                    r"\brayleigh method\b",
                    low,
                )
            ),
            [
                (([[2.0, 1.0], [1.0, 2.0]], [1.0, 0.5], 1e-10, 12),
                 ([0.9999999999994995, 1.0], 3.0)),
            ],
        ),
        T(
            "nelder_mead",
            "def nelder_mead(f, x0, y0, step=0.4, max_iter=40, tol=1e-8):\n"
            '    """Nelder-Mead simplex method for a 2-D function (educational).\n'
            "    f(x, y) -> float. Starts a right triangle of side step. Returns best (x, y).\n"
            '    """\n'
            "    s = [(float(x0), float(y0)), (float(x0) + step, float(y0)), (float(x0), float(y0) + step)]\n"
            "    alpha, gamma, rho, sigma = 1.0, 2.0, 0.5, 0.5\n"
            "    for _ in range(max_iter):\n"
            "        s.sort(key=lambda p: f(p[0], p[1]))\n"
            "        if abs(f(*s[0]) - f(*s[-1])) < tol:\n"
            "            break\n"
            "        xc = ((s[0][0] + s[1][0]) / 2.0, (s[0][1] + s[1][1]) / 2.0)\n"
            "        xr = (xc[0] + alpha * (xc[0] - s[2][0]), xc[1] + alpha * (xc[1] - s[2][1]))\n"
            "        fr = f(*xr)\n"
            "        fb, fs = f(*s[0]), f(*s[1])\n"
            "        if fb <= fr < fs:\n"
            "            s[2] = xr\n"
            "            continue\n"
            "        if fr < fb:\n"
            "            xe = (xc[0] + gamma * (xr[0] - xc[0]), xc[1] + gamma * (xr[1] - xc[1]))\n"
            "            s[2] = xe if f(*xe) < fr else xr\n"
            "            continue\n"
            "        xc2 = (xc[0] + rho * (s[2][0] - xc[0]), xc[1] + rho * (s[2][1] - xc[1]))\n"
            "        if f(*xc2) < f(*s[2]):\n"
            "            s[2] = xc2\n"
            "            continue\n"
            "        s[1] = (s[0][0] + sigma * (s[1][0] - s[0][0]), s[0][1] + sigma * (s[1][1] - s[0][1]))\n"
            "        s[2] = (s[0][0] + sigma * (s[2][0] - s[0][0]), s[0][1] + sigma * (s[2][1] - s[0][1]))\n"
            "    s.sort(key=lambda p: f(p[0], p[1]))\n"
            "    return s[0]\n",
            lambda low: bool(
                re.search(
                    r"\bnelder[- ]mead\b|"
                    r"\bnelder mead\b|"
                    r"\bsimplex method\b.{0,24}\b(2d|two[- ]d|optimization)\b",
                    low,
                )
            )
            and "linear" not in low
            and "lp" not in low,
            [
                (
                    (
                        lambda x, y: (x - 1.0) ** 2 + (y - 2.0) ** 2,
                        0.0,
                        0.0,
                        0.4,
                        40,
                        1e-8,
                    ),
                    (0.9999748997513618, 2.000089786927572),
                ),
            ],
        ),
        T(
            "halley_method",
            "def halley_method(f, df, d2f, x0, tol=1e-12, max_iter=8):\n"
            '    """Halley method for a root of f (educational).\n'
            "    Uses f, df, d2f. Returns the approximate root.\n"
            '    """\n'
            "    x = float(x0)\n"
            "    for _ in range(max_iter):\n"
            "        fx = f(x)\n"
            "        dfx = df(x)\n"
            "        d2x = d2f(x)\n"
            "        denom = 2.0 * dfx * dfx - fx * d2x\n"
            "        if abs(denom) < 1e-15:\n"
            "            break\n"
            "        dx = (2.0 * fx * dfx) / denom\n"
            "        x -= dx\n"
            "        if abs(dx) < tol:\n"
            "            break\n"
            "    return x\n",
            lambda low: bool(
                re.search(
                    r"\bhalley(?:'s)?[- ]method\b|"
                    r"\bhalley method\b|"
                    r"\bhalley\\'s method\b",
                    low,
                )
            ),
            [
                (
                    (
                        lambda x: x ** 3 - 2.0,
                        lambda x: 3.0 * x ** 2,
                        lambda x: 6.0 * x,
                        1.5,
                        1e-12,
                        8,
                    ),
                    1.2599210498948732,
                ),
            ],
        ),
        T(
            "muller_method",
            "def muller_method(f, x0, x1, x2, tol=1e-10, max_iter=10):\n"
            '    """Muller method for a root of f (educational).\n'
            "    Quadratic interpolation from three starting points. Returns the approximate root.\n"
            '    """\n'
            "    xs = [float(x0), float(x1), float(x2)]\n"
            "    for _ in range(max_iter):\n"
            "        f0, f1, f2 = f(xs[0]), f(xs[1]), f(xs[2])\n"
            "        h0, h1 = xs[1] - xs[0], xs[2] - xs[1]\n"
            "        d0, d1 = (f1 - f0) / h0, (f2 - f1) / h1\n"
            "        a = (d1 - d0) / (h1 + h0)\n"
            "        b = a * h1 + d1\n"
            "        c = f2\n"
            "        disc = b * b - 4 * a * c\n"
            "        if disc < 0:\n"
            "            disc = 0.0\n"
            "        den = b + (disc ** 0.5 if b >= 0 else -disc ** 0.5)\n"
            "        if abs(den) < 1e-15:\n"
            "            break\n"
            "        dx = -2 * c / den\n"
            "        x3 = xs[2] + dx\n"
            "        xs = [xs[1], xs[2], x3]\n"
            "        if abs(dx) < tol:\n"
            "            break\n"
            "    return xs[2]\n",
            lambda low: bool(
                re.search(
                    r"\bmuller(?:'s)?[- ]method\b|"
                    r"\bmuller method\b|"
                    r"\bmuller root\b",
                    low,
                )
            ),
            [
                (
                    (
                        lambda x: x ** 3 - 2.0,
                        1.0,
                        1.2,
                        1.5,
                        1e-10,
                        10,
                    ),
                    1.2599210498948732,
                ),
            ],
        ),
    ]
