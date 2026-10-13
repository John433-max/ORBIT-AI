"""Cycle 607: QR algorithm, full conjugate gradient, Adams-Moulton 2,
trust-region Cauchy point, Gauss-Newton, Broyden.

Pure-Python educational; no NumPy. Narrow matchers + sibling-token upgrade
avoid stealing qr_decomposition, conjugate_gradient_1d, adams_bashforth_*,
and existing Newton/root finders.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "qr_algorithm",
            "def qr_algorithm(A, max_iter=8):\n"
            '    """Unshifted QR algorithm for eigenvalues (educational).\n'
            "    Repeatedly replaces A with R@Q from a Gram-Schmidt QR factorization.\n"
            "    Returns the diagonal of the final iterate (approximate eigenvalues).\n"
            '    """\n'
            "    import math\n"
            "    n = len(A)\n"
            "    Ak = [row[:] for row in A]\n"
            "    for _ in range(max_iter):\n"
            "        Q = [[0.0] * n for _ in range(n)]\n"
            "        R = [[0.0] * n for _ in range(n)]\n"
            "        for i in range(n):\n"
            "            v = [Ak[r][i] for r in range(n)]\n"
            "            for j in range(i):\n"
            "                R[j][i] = sum(Q[r][j] * v[r] for r in range(n))\n"
            "                for r in range(n):\n"
            "                    v[r] -= R[j][i] * Q[r][j]\n"
            "            R[i][i] = math.sqrt(sum(x * x for x in v)) or 1.0\n"
            "            for r in range(n):\n"
            "                Q[r][i] = v[r] / R[i][i]\n"
            "        newA = [[0.0] * n for _ in range(n)]\n"
            "        for i in range(n):\n"
            "            for j in range(n):\n"
            "                newA[i][j] = sum(R[i][k] * Q[k][j] for k in range(n))\n"
            "        Ak = newA\n"
            "    return [Ak[i][i] for i in range(n)]\n",
            lambda low: bool(
                re.search(
                    r"\bqr[- ]algorithm\b|"
                    r"\bqr[- ]iteration\b|"
                    r"\bqr[- ]method for eigenvalues\b",
                    low,
                )
            )
            and "decomposition" not in low
            and "householder" not in low,
            [
                (([[2.0, 1.0], [1.0, 3.0]], 8),
                 [3.6180327868852458, 1.381967213114754]),
            ],
        ),
        T(
            "conjugate_gradient",
            "def conjugate_gradient(A, b, max_iter=10, tol=1e-10):\n"
            '    """Conjugate gradient for SPD Ax = b (educational).\n'
            "    Returns the approximate solution list. Stops early on residual tolerance.\n"
            '    """\n'
            "    import math\n"
            "    n = len(b)\n"
            "    x = [0.0] * n\n"
            "    r = b[:]\n"
            "    p = r[:]\n"
            "    rsold = sum(ri * ri for ri in r)\n"
            "    for _ in range(max_iter):\n"
            "        Ap = [sum(A[i][j] * p[j] for j in range(n)) for i in range(n)]\n"
            "        pAp = sum(p[i] * Ap[i] for i in range(n)) or 1.0\n"
            "        alpha = rsold / pAp\n"
            "        x = [x[i] + alpha * p[i] for i in range(n)]\n"
            "        r = [r[i] - alpha * Ap[i] for i in range(n)]\n"
            "        rsnew = sum(ri * ri for ri in r)\n"
            "        if math.sqrt(rsnew) < tol:\n"
            "            break\n"
            "        beta = rsnew / (rsold or 1.0)\n"
            "        p = [r[i] + beta * p[i] for i in range(n)]\n"
            "        rsold = rsnew\n"
            "    return x\n",
            lambda low: bool(
                re.search(
                    r"\bconjugate[- ]gradient\b|"
                    r"\bcg method\b|"
                    r"\bcg solver\b",
                    low,
                )
            )
            and "1d" not in low
            and "one-dimensional" not in low
            and "one d" not in low,
            [
                (([[4.0, 1.0], [1.0, 3.0]], [1.0, 2.0]),
                 [0.09090909090909091, 0.6363636363636364]),
            ],
        ),
        T(
            "adams_moulton_2",
            "def adams_moulton_2(f, t0, y0, h, n_steps):\n"
            '    """Two-step Adams-Moulton via AB2 predict + one AM2 correct (educational).\n'
            "    Uses one forward-Euler starter. Returns the list of y values including y0.\n"
            "    AM2: y_{n+1} = y_n + (h/2)*(f_n + f_{n+1}).\n"
            '    """\n'
            "    ys = [float(y0)]\n"
            "    ts = [float(t0)]\n"
            "    y1 = y0 + h * f(t0, y0)\n"
            "    ys.append(y1)\n"
            "    ts.append(t0 + h)\n"
            "    for _ in range(1, n_steps):\n"
            "        t = ts[-1]\n"
            "        y = ys[-1]\n"
            "        f0 = f(ts[-2], ys[-2])\n"
            "        f1 = f(t, y)\n"
            "        y_pred = y + h * (1.5 * f1 - 0.5 * f0)\n"
            "        f_pred = f(t + h, y_pred)\n"
            "        y_new = y + 0.5 * h * (f1 + f_pred)\n"
            "        ys.append(y_new)\n"
            "        ts.append(t + h)\n"
            "    return ys\n",
            lambda low: bool(
                re.search(
                    r"\badams[- ]moulton(?:[- ]2| 2)?\b|"
                    r"\bam2\b|"
                    r"\btwo[- ]step adams[- ]moulton\b",
                    low,
                )
            )
            and "bashforth" not in low,
            [
                ((lambda t, y: y, 0.0, 1.0, 0.1, 3),
                 [1.0, 1.1, 1.21575, 1.3436931250000002]),
            ],
        ),
        T(
            "trust_region_cauchy",
            "def trust_region_cauchy(g, H, delta=1.0):\n"
            '    """Cauchy point of a quadratic model in a trust region (educational).\n'
            "    m(s) = g·s + 0.5 s·H·s subject to ||s|| <= delta.\n"
            "    Returns the step list (negative gradient direction scaled by tau).\n"
            '    """\n'
            "    import math\n"
            "    n = len(g)\n"
            "    ng = math.sqrt(sum(gi * gi for gi in g)) or 1.0\n"
            "    Hg = [sum(H[i][j] * g[j] for j in range(n)) for i in range(n)]\n"
            "    gHg = sum(g[i] * Hg[i] for i in range(n))\n"
            "    if gHg <= 0.0:\n"
            "        tau = 1.0\n"
            "    else:\n"
            "        tau = min(1.0, (ng ** 3) / (delta * gHg))\n"
            "    return [-tau * delta * g[i] / ng for i in range(n)]\n",
            lambda low: bool(
                re.search(
                    r"\btrust[- ]region[- ]cauchy\b|"
                    r"\bcauchy[- ]point\b|"
                    r"\btrust region cauchy\b",
                    low,
                )
            ),
            [
                (([1.0, -0.5], [[2.0, 0.0], [0.0, 1.0]], 1.0),
                 [-0.5555555555555557, 0.27777777777777785]),
            ],
        ),
        T(
            "gauss_newton",
            "def gauss_newton(residual, jacobian, x0, max_iter=4):\n"
            '    """Gauss-Newton for nonlinear least squares (educational).\n'
            "    residual(x) -> list of residuals; jacobian(x) -> list of rows.\n"
            "    Solves the normal equations with a small dense Gaussian elimination.\n"
            "    Returns the final parameter list.\n"
            '    """\n'
            "    def _solve(A, b):\n"
            "        n = len(b)\n"
            "        M = [A[i][:] + [b[i]] for i in range(n)]\n"
            "        for i in range(n):\n"
            "            piv = max(range(i, n), key=lambda k: abs(M[k][i]))\n"
            "            M[i], M[piv] = M[piv], M[i]\n"
            "            for k in range(i + 1, n):\n"
            "                fac = M[k][i] / (M[i][i] or 1.0)\n"
            "                for j in range(i, n + 1):\n"
            "                    M[k][j] -= fac * M[i][j]\n"
            "        x = [0.0] * n\n"
            "        for i in range(n - 1, -1, -1):\n"
            "            s = M[i][n]\n"
            "            for j in range(i + 1, n):\n"
            "                s -= M[i][j] * x[j]\n"
            "            x[i] = s / (M[i][i] or 1.0)\n"
            "        return x\n"
            "    x = [float(v) for v in x0]\n"
            "    n = len(x)\n"
            "    for _ in range(max_iter):\n"
            "        r = residual(x)\n"
            "        J = jacobian(x)\n"
            "        m = len(r)\n"
            "        JTJ = [[sum(J[k][i] * J[k][j] for k in range(m)) for j in range(n)] for i in range(n)]\n"
            "        JTr = [sum(J[k][i] * r[k] for k in range(m)) for i in range(n)]\n"
            "        dx = _solve(JTJ, [-v for v in JTr])\n"
            "        x = [x[i] + dx[i] for i in range(n)]\n"
            "    return x\n",
            lambda low: bool(
                re.search(
                    r"\bgauss[- ]newton\b|"
                    r"\bgauss newton method\b",
                    low,
                )
            ),
            [
                (
                    (
                        lambda x: [x[0] * t + x[1] - y for t, y in ((0, 1), (1, 3), (2, 5))],
                        lambda x: [[t, 1.0] for t, y in ((0, 1), (1, 3), (2, 5))],
                        [0.0, 0.0],
                        4,
                    ),
                    [2.0, 1.0],
                ),
            ],
        ),
        T(
            "broyden_method",
            "def broyden_method(F, x0, max_iter=6, tol=1e-10):\n"
            '    """Broyden rank-1 update for nonlinear systems F(x) = 0 (educational).\n'
            "    Starts with the identity Jacobian approximation. Returns the final x.\n"
            '    """\n'
            "    def _solve(A, b):\n"
            "        n = len(b)\n"
            "        M = [A[i][:] + [b[i]] for i in range(n)]\n"
            "        for i in range(n):\n"
            "            piv = max(range(i, n), key=lambda k: abs(M[k][i]))\n"
            "            M[i], M[piv] = M[piv], M[i]\n"
            "            for k in range(i + 1, n):\n"
            "                fac = M[k][i] / (M[i][i] or 1.0)\n"
            "                for j in range(i, n + 1):\n"
            "                    M[k][j] -= fac * M[i][j]\n"
            "        x = [0.0] * n\n"
            "        for i in range(n - 1, -1, -1):\n"
            "            s = M[i][n]\n"
            "            for j in range(i + 1, n):\n"
            "                s -= M[i][j] * x[j]\n"
            "            x[i] = s / (M[i][i] or 1.0)\n"
            "        return x\n"
            "    n = len(x0)\n"
            "    x = [float(v) for v in x0]\n"
            "    B = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]\n"
            "    Fx = F(x)\n"
            "    for _ in range(max_iter):\n"
            "        s = _solve(B, [-v for v in Fx])\n"
            "        x_new = [x[i] + s[i] for i in range(n)]\n"
            "        Fx_new = F(x_new)\n"
            "        y = [Fx_new[i] - Fx[i] for i in range(n)]\n"
            "        Bs = [sum(B[i][j] * s[j] for j in range(n)) for i in range(n)]\n"
            "        ss = sum(si * si for si in s) or 1.0\n"
            "        for i in range(n):\n"
            "            for j in range(n):\n"
            "                B[i][j] += (y[i] - Bs[i]) * s[j] / ss\n"
            "        x, Fx = x_new, Fx_new\n"
            "        if max(abs(v) for v in Fx) < tol:\n"
            "            break\n"
            "    return x\n",
            lambda low: bool(
                re.search(
                    r"\bbroyden\b|"
                    r"\bbroyden[- ]method\b|"
                    r"\brank[- ]1 update\b",
                    low,
                )
            ),
            [
                (
                    (
                        lambda x: [x[0] + x[1] - 3.0, x[0] - x[1] - 1.0],
                        [0.0, 0.0],
                        5,
                    ),
                    [2.0, 1.0000000000000002],
                ),
            ],
        ),
    ]
