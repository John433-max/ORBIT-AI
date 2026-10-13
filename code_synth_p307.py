"""Cycle 604: Gauss-Seidel, Jacobi iterative, Heun, Adams-Bashforth-2, RK2 midpoint, Euler.

Pure-Python educational; no NumPy. Narrow matchers avoid collisions with
existing newton_raphson, rk4_*, gauss_quadrature_2, and euler_tour.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "gauss_seidel",
            "def gauss_seidel(A, b, tol=1e-8, max_iter=100):\n"
            '    """Gauss-Seidel iterative solver for Ax = b (educational).\n'
            "    A is list of lists, b list of floats. Returns approximate solution list.\n"
            "    Uses successive updates within each sweep.\n"
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
            "            x[i] = s / A[i][i]\n"
            "        if max(abs(x[i] - x_old[i]) for i in range(n)) < tol:\n"
            "            break\n"
            "    return x\n",
            lambda low: bool(
                re.search(
                    r"\bgauss[- ]seidel\b|"
                    r"\bseidel method\b|"
                    r"\biterative.*seidel\b",
                    low,
                )
            ),
            [
                (([[4.0, 1.0], [1.0, 3.0]], [1.0, 2.0]), [0.0909090912790855, 0.6363636362403048]),
            ],
        ),
        T(
            "jacobi_iterative",
            "def jacobi_iterative(A, b, tol=1e-8, max_iter=100):\n"
            '    """Jacobi iterative solver for Ax = b (educational).\n'
            "    Uses old values only for the entire sweep. Returns approximate solution.\n"
            '    """\n'
            "    n = len(A)\n"
            "    x = [0.0] * n\n"
            "    for _ in range(max_iter):\n"
            "        x_new = [0.0] * n\n"
            "        for i in range(n):\n"
            "            s = b[i]\n"
            "            for j in range(n):\n"
            "                if j != i:\n"
            "                    s -= A[i][j] * x[j]\n"
            "            x_new[i] = s / A[i][i]\n"
            "        if max(abs(x_new[i] - x[i]) for i in range(n)) < tol:\n"
            "            x = x_new\n"
            "            break\n"
            "        x = x_new\n"
            "    return x\n",
            lambda low: bool(
                re.search(
                    r"\bjacobi(?: iterative| method)?\b|"
                    r"\bjacobi[- ]method\b",
                    low,
                )
            )
            and "eigen" not in low
            and "rotation" not in low,
            [
                (([[4.0, 1.0], [1.0, 3.0]], [1.0, 2.0]), [0.09090909069766542, 0.636363634883658]),
            ],
        ),
        T(
            "heun_method",
            "def heun_method(f, y0, t0, t1, n=20):\n"
            '    """Heun / improved Euler method for y\' = f(t, y) (educational).\n'
            "    Returns y at t1. Predictor-corrector with average slope.\n"
            '    """\n'
            "    h = (t1 - t0) / n\n"
            "    y = float(y0)\n"
            "    t = float(t0)\n"
            "    for _ in range(n):\n"
            "        k1 = f(t, y)\n"
            "        y_pred = y + h * k1\n"
            "        k2 = f(t + h, y_pred)\n"
            "        y = y + 0.5 * h * (k1 + k2)\n"
            "        t += h\n"
            "    return y\n",
            lambda low: bool(
                re.search(
                    r"\bheun(?:s|\'s)?(?: method)?\b|"
                    r"\bimproved[- ]euler\b|"
                    r"\bexplicit[- ]trapezoidal\b",
                    low,
                )
            ),
            [
                ((lambda t, y: y, 1.0, 0.0, 1.0, 10), 2.714080846608224),
            ],
        ),
        T(
            "adams_bashforth_2",
            "def adams_bashforth_2(f, y0, y1, t0, t1, n=20):\n"
            '    """Two-step Adams-Bashforth for y\' = f(t, y) (educational).\n'
            "    Requires two starting values y0, y1. Returns y at t1.\n"
            "    y_{n+1} = y_n + (h/2)*(3*f_n - f_{n-1}).\n"
            '    """\n'
            "    h = (t1 - t0) / n\n"
            "    y_prev = float(y0)\n"
            "    y = float(y1)\n"
            "    t_prev = float(t0)\n"
            "    t = t_prev + h\n"
            "    for i in range(1, n):\n"
            "        f_prev = f(t_prev, y_prev)\n"
            "        f_cur = f(t, y)\n"
            "        y_next = y + 0.5 * h * (3 * f_cur - f_prev)\n"
            "        y_prev, y = y, y_next\n"
            "        t_prev, t = t, t + h\n"
            "    return y\n",
            lambda low: bool(
                re.search(
                    r"\badams[- ]bashforth(?:[- ]2| 2)?\b|"
                    r"\bab2\b|"
                    r"\btwo[- ]step adams\b",
                    low,
                )
            ),
            [
                ((lambda t, y: y, 1.0, 1.105170918, 0.0, 1.0, 10), 2.708813860146136),
            ],
        ),
        T(
            "rk2_midpoint",
            "def rk2_midpoint(f, y0, t0, t1, n=20):\n"
            '    """RK2 midpoint method for y\' = f(t, y) (educational).\n'
            "    Returns y at t1. Second-order explicit Runge-Kutta.\n"
            '    """\n'
            "    h = (t1 - t0) / n\n"
            "    y = float(y0)\n"
            "    t = float(t0)\n"
            "    for _ in range(n):\n"
            "        k1 = f(t, y)\n"
            "        k2 = f(t + 0.5 * h, y + 0.5 * h * k1)\n"
            "        y = y + h * k2\n"
            "        t += h\n"
            "    return y\n",
            lambda low: bool(
                re.search(
                    r"\brk2(?: midpoint)?\b|"
                    r"\bmidpoint[- ]method\b|"
                    r"\brunge[- ]kutta[- ]2\b|"
                    r"\bsecond[- ]order runge\b",
                    low,
                )
            )
            and "rk4" not in low,
            [
                ((lambda t, y: y, 1.0, 0.0, 1.0, 10), 2.714080846608224),
            ],
        ),
        T(
            "forward_euler",
            "def forward_euler(f, y0, t0, t1, n=20):\n"
            '    """Forward Euler method for y\' = f(t, y) (educational).\n'
            "    Returns y at t1. First-order explicit.\n"
            '    """\n'
            "    h = (t1 - t0) / n\n"
            "    y = float(y0)\n"
            "    t = float(t0)\n"
            "    for _ in range(n):\n"
            "        y = y + h * f(t, y)\n"
            "        t += h\n"
            "    return y\n",
            lambda low: bool(
                re.search(
                    r"\bforward[- ]euler\b|"
                    r"\beuler(?:\'s|s)? method\b|"
                    r"\beuler[- ]integration\b",
                    low,
                )
            )
            and "tour" not in low
            and "totient" not in low,
            [
                ((lambda t, y: y, 1.0, 0.0, 1.0, 10), 2.5937424601),
            ],
        ),
    ]
