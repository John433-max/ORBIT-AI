"""Cycle 605: SOR, Adams-Bashforth-3, RK3, Gauss-Jordan, Brent root, steepest descent 2D.

Pure-Python educational; no NumPy. Narrow matchers avoid collisions with
existing gauss_seidel, adams_bashforth_2, rk4_*, gaussian_elimination, bisection, secant.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "successive_over_relaxation",
            "def successive_over_relaxation(A, b, omega=1.2, tol=1e-8, max_iter=100):\n"
            '    """Successive Over-Relaxation (SOR) for Ax = b (educational).\n'
            "    A is list of lists, b list of floats. omega is the relaxation factor.\n"
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
            "        if max(abs(x[i] - x_old[i]) for i in range(n)) < tol:\n"
            "            break\n"
            "    return x\n",
            lambda low: bool(
                re.search(
                    r"\bsuccessive[- ]over[- ]relaxation\b|"
                    r"\bsor method\b|"
                    r"\bsor solver\b|"
                    r"\bover[- ]relaxation\b",
                    low,
                )
            )
            and "seidel" not in low,
            [
                (([[4.0, 1.0], [1.0, 3.0]], [1.0, 2.0], 1.1, 1e-8, 20),
                 [0.09090909109710088, 0.6363636363565133]),
            ],
        ),
        T(
            "adams_bashforth_3",
            "def adams_bashforth_3(f, y0, y1, y2, t0, t1, n=12):\n"
            '    """Three-step Adams-Bashforth for y\' = f(t, y) (educational).\n'
            "    Requires three starting values y0, y1, y2. Returns y at t1.\n"
            "    y_{n+1} = y_n + (h/12)*(23*f_n - 16*f_{n-1} + 5*f_{n-2}).\n"
            '    """\n'
            "    h = (t1 - t0) / n\n"
            "    ys = [float(y0), float(y1), float(y2)]\n"
            "    ts = [float(t0), float(t0) + h, float(t0) + 2 * h]\n"
            "    for i in range(2, n):\n"
            "        f0 = f(ts[-3], ys[-3])\n"
            "        f1 = f(ts[-2], ys[-2])\n"
            "        f2 = f(ts[-1], ys[-1])\n"
            "        y_next = ys[-1] + h / 12 * (23 * f2 - 16 * f1 + 5 * f0)\n"
            "        ys.append(y_next)\n"
            "        ts.append(ts[-1] + h)\n"
            "    return ys[-1]\n",
            lambda low: bool(
                re.search(
                    r"\badams[- ]bashforth(?:[- ]3| 3)\b|"
                    r"\bab3\b|"
                    r"\bthree[- ]step adams\b|"
                    r"\badams[- ]bashforth[- ]3\b",
                    low,
                )
            ),
            [
                ((lambda t, y: y, 1.0, 1.105170918, 1.221402758, 0.0, 1.0, 12),
                 2.810601207350529),
            ],
        ),
        T(
            "rk3_method",
            "def rk3_method(f, y0, t0, t1, n=10):\n"
            '    """Classic third-order Runge-Kutta (RK3) for y\' = f(t, y) (educational).\n'
            "    Returns y at t1. Three-stage explicit method.\n"
            '    """\n'
            "    h = (t1 - t0) / n\n"
            "    y = float(y0)\n"
            "    t = float(t0)\n"
            "    for _ in range(n):\n"
            "        k1 = f(t, y)\n"
            "        k2 = f(t + 0.5 * h, y + 0.5 * h * k1)\n"
            "        k3 = f(t + h, y - h * k1 + 2 * h * k2)\n"
            "        y = y + h / 6 * (k1 + 4 * k2 + k3)\n"
            "        t += h\n"
            "    return y\n",
            lambda low: bool(
                re.search(
                    r"\brk3(?: method)?\b|"
                    r"\brunke[- ]kutta[- ]3\b|"
                    r"\bthird[- ]order runge\b|"
                    r"\brunge[- ]kutta order 3\b",
                    low,
                )
            )
            and "rk4" not in low
            and "order 4" not in low,
            [
                ((lambda t, y: y, 1.0, 0.0, 1.0, 10), 2.718177262481609),
            ],
        ),
        T(
            "gauss_jordan",
            "def gauss_jordan(A, b):\n"
            '    """Gauss-Jordan elimination for Ax = b (educational).\n'
            "    A is list of lists, b list of floats. Returns solution list.\n"
            "    Reduces the augmented matrix to reduced row-echelon form.\n"
            '    """\n'
            "    n = len(A)\n"
            "    M = [row[:] + [b[i]] for i, row in enumerate(A)]\n"
            "    for col in range(n):\n"
            "        pivot = col\n"
            "        for r in range(col + 1, n):\n"
            "            if abs(M[r][col]) > abs(M[pivot][col]):\n"
            "                pivot = r\n"
            "        M[col], M[pivot] = M[pivot], M[col]\n"
            "        div = M[col][col]\n"
            "        for j in range(col, n + 1):\n"
            "            M[col][j] /= div\n"
            "        for r in range(n):\n"
            "            if r != col:\n"
            "                factor = M[r][col]\n"
            "                for j in range(col, n + 1):\n"
            "                    M[r][j] -= factor * M[col][j]\n"
            "    return [M[i][n] for i in range(n)]\n",
            lambda low: bool(
                re.search(
                    r"\bgauss[- ]jordan\b|"
                    r"\bgauss jordan elimination\b|"
                    r"\breduced row[- ]echelon\b",
                    low,
                )
            ),
            [
                (([[2.0, 1.0], [1.0, 3.0]], [5.0, 7.0]), [1.6, 1.8]),
            ],
        ),
        T(
            "brent_root",
            "def brent_root(f, a, b, tol=1e-10, max_iter=50):\n"
            '    """Simplified Brent-style hybrid root finder (educational).\n'
            "    Combines bisection and secant. Requires f(a)*f(b) < 0.\n"
            "    Returns an approximate root.\n"
            '    """\n'
            "    fa, fb = f(a), f(b)\n"
            "    if fa * fb > 0:\n"
            "        raise ValueError('same sign')\n"
            "    for _ in range(max_iter):\n"
            "        if abs(fb) < abs(fa):\n"
            "            a, b = b, a\n"
            "            fa, fb = fb, fa\n"
            "        m = 0.5 * (a - b)\n"
            "        if abs(fa - fb) > 1e-15:\n"
            "            s = b - fb * (b - a) / (fb - fa)\n"
            "        else:\n"
            "            s = b + m\n"
            "        if (s - b) * (s - (b + m)) > 0 or abs(s - b) >= abs(m):\n"
            "            s = b + m\n"
            "        fs = f(s)\n"
            "        if abs(fs) < tol or abs(s - b) < tol:\n"
            "            return s\n"
            "        if fa * fs < 0:\n"
            "            b, fb = s, fs\n"
            "        else:\n"
            "            a, fa = s, fs\n"
            "    return b\n",
            lambda low: bool(
                re.search(
                    r"\bbrent(?:s|\'s)?(?: method| root)?\b|"
                    r"\bbrent root\b|"
                    r"\bvan wijngaarden\b",
                    low,
                )
            )
            and "factor" not in low,
            [
                ((lambda x: x * x - 2, 1.0, 2.0, 1e-12, 40), 1.4142135623733338),
            ],
        ),
        T(
            "steepest_descent_2d",
            "def steepest_descent_2d(x0, y0, step=0.2, n=10):\n"
            '    """Steepest descent for f(x,y)=(x-1)^2+(y-2)^2 (educational).\n'
            "    Fixed step size, n iterations. Returns [x, y].\n"
            '    """\n'
            "    x, y = float(x0), float(y0)\n"
            "    for _ in range(n):\n"
            "        gx = 2 * (x - 1)\n"
            "        gy = 2 * (y - 2)\n"
            "        x -= step * gx\n"
            "        y -= step * gy\n"
            "    return [x, y]\n",
            lambda low: bool(
                re.search(
                    r"\bsteepest[- ]descent\b|"
                    r"\bgradient[- ]descent[- ]2d\b|"
                    r"\bsteepest descent method\b",
                    low,
                )
            ),
            [
                ((0.0, 0.0, 0.25, 8), [0.99609375, 1.9921875]),
            ],
        ),
    ]
