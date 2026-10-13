"""Cycle 600: Cholesky, symmetric eigenvalues (Jacobi), naive Bayes,
cross-entropy, layer norm, scaled dot-product attention.

Closes probe gaps from Cycle 599 next-target list. Pure-Python educational;
no NumPy required.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "cholesky_decomposition",
            "def cholesky_decomposition(A):\n"
            '    """Cholesky factorization A = L @ L.T for SPD matrix (educational).\n'
            "    A: list[list[float]] n x n symmetric positive-definite.\n"
            "    Returns lower-triangular L. Raises ValueError if not SPD.\n"
            '    """\n'
            "    import math\n"
            "    n = len(A)\n"
            "    L = [[0.0] * n for _ in range(n)]\n"
            "    for i in range(n):\n"
            "        for j in range(i + 1):\n"
            "            s = sum(L[i][k] * L[j][k] for k in range(j))\n"
            "            if i == j:\n"
            "                val = A[i][i] - s\n"
            "                if val <= 0:\n"
            "                    raise ValueError('Matrix is not positive-definite')\n"
            "                L[i][j] = math.sqrt(val)\n"
            "            else:\n"
            "                L[i][j] = (A[i][j] - s) / L[j][j]\n"
            "    def _r(x):\n"
            "        return round(x, 10)\n"
            "    return [[_r(x) for x in row] for row in L]\n",
            lambda low: bool(
                re.search(
                    r"\bcholesky\b|"
                    r"\bcholesky\s+(decomposition|factorization|factor)\b|"
                    r"\bLLT\b|\bL\s*\*\s*L\.T\b",
                    low,
                )
            )
            and "qr" not in low
            and "svd" not in low,
            examples=(
                (
                    ([[4.0, 12.0, -16.0], [12.0, 37.0, -43.0], [-16.0, -43.0, 98.0]],),
                    [[2.0, 0.0, 0.0], [6.0, 1.0, 0.0], [-8.0, 5.0, 3.0]],
                ),
            ),
        ),
        T(
            "symmetric_eigenvalues",
            "def symmetric_eigenvalues(A, tol=1e-10, max_iter=200):\n"
            '    """Eigenvalues of symmetric matrix via Jacobi rotations (educational).\n'
            "    A: list[list[float]] n x n symmetric. Returns eigenvalues descending.\n"
            '    """\n'
            "    import math\n"
            "    n = len(A)\n"
            "    M = [row[:] for row in A]\n"
            "    for _ in range(max_iter):\n"
            "        max_off = 0.0\n"
            "        p = q = 0\n"
            "        for i in range(n):\n"
            "            for j in range(i + 1, n):\n"
            "                if abs(M[i][j]) > max_off:\n"
            "                    max_off = abs(M[i][j])\n"
            "                    p, q = i, j\n"
            "        if max_off < tol:\n"
            "            break\n"
            "        app, aqq, apq = M[p][p], M[q][q], M[p][q]\n"
            "        if abs(apq) < 1e-18:\n"
            "            continue\n"
            "        tau = (aqq - app) / (2.0 * apq)\n"
            "        t = math.copysign(1.0 / (abs(tau) + math.sqrt(1.0 + tau * tau)), tau)\n"
            "        c = 1.0 / math.sqrt(1.0 + t * t)\n"
            "        s = t * c\n"
            "        for i in range(n):\n"
            "            if i == p or i == q:\n"
            "                continue\n"
            "            aip, aiq = M[i][p], M[i][q]\n"
            "            M[i][p] = M[p][i] = c * aip - s * aiq\n"
            "            M[i][q] = M[q][i] = s * aip + c * aiq\n"
            "        M[p][p] = c * c * app - 2 * s * c * apq + s * s * aqq\n"
            "        M[q][q] = s * s * app + 2 * s * c * apq + c * c * aqq\n"
            "        M[p][q] = M[q][p] = 0.0\n"
            "    eigs = sorted((round(M[i][i], 8) for i in range(n)), reverse=True)\n"
            "    return eigs\n",
            lambda low: bool(
                re.search(
                    r"\b(symmetric\s+)?eigenvalues?\b|"
                    r"\beigen\s*values?\s+of\s+(a\s+)?symmetric\b|"
                    r"\bjacobi\s+(eigen|method)\b|"
                    r"\beigenvalues?\s+of\s+(symmetric\s+)?matrix\b",
                    low,
                )
            )
            and "svd" not in low
            and "singular" not in low
            and "is_symmetric" not in low,
            examples=(
                (
                    ([[2.0, 1.0], [1.0, 2.0]],),
                    [3.0, 1.0],
                ),
            ),
        ),
        T(
            "naive_bayes",
            "def naive_bayes_predict(X_train, y_train, x):\n"
            '    """Gaussian Naive Bayes single-sample predict (educational).\n'
            "    X_train: list[list[float]], y_train: list[label], x: list[float].\n"
            "    Returns predicted class label (majority on ties).\n"
            '    """\n'
            "    import math\n"
            "    classes = sorted(set(y_train))\n"
            "    n = len(y_train)\n"
            "    feat = len(x)\n"
            "    means = {}\n"
            "    vars_ = {}\n"
            "    priors = {}\n"
            "    for c in classes:\n"
            "        rows = [X_train[i] for i in range(n) if y_train[i] == c]\n"
            "        priors[c] = len(rows) / n\n"
            "        means[c] = [sum(r[j] for r in rows) / len(rows) for j in range(feat)]\n"
            "        vars_[c] = []\n"
            "        for j in range(feat):\n"
            "            m = means[c][j]\n"
            "            v = sum((r[j] - m) ** 2 for r in rows) / max(1, len(rows) - 1)\n"
            "            vars_[c].append(max(v, 1e-9))\n"
            "    best_c, best_log = None, float('-inf')\n"
            "    for c in classes:\n"
            "        logp = math.log(priors[c] + 1e-12)\n"
            "        for j in range(feat):\n"
            "            v = vars_[c][j]\n"
            "            diff = x[j] - means[c][j]\n"
            "            logp += -0.5 * (math.log(2 * math.pi * v) + diff * diff / v)\n"
            "        if logp > best_log:\n"
            "            best_log = logp\n"
            "            best_c = c\n"
            "    return best_c\n",
            lambda low: bool(
                re.search(
                    r"\bnaive\s*bayes\b|"
                    r"\bgaussian\s+naive\s*bayes\b|"
                    r"\bnb\s+classifier\b",
                    low,
                )
            ),
            examples=(
                (
                    (
                        [[1.0, 2.0], [1.5, 1.8], [5.0, 8.0], [6.0, 9.0]],
                        [0, 0, 1, 1],
                        [1.2, 1.9],
                    ),
                    0,
                ),
            ),
        ),
        T(
            "cross_entropy_loss",
            "def cross_entropy_loss(y_true, y_pred, eps=1e-12):\n"
            '    """Mean categorical cross-entropy (educational).\n'
            "    y_true: list[list[float]] one-hot, y_pred: list[list[float]] probabilities.\n"
            "    Returns scalar mean loss.\n"
            '    """\n'
            "    import math\n"
            "    n = len(y_true)\n"
            "    if n == 0:\n"
            "        return 0.0\n"
            "    total = 0.0\n"
            "    for yt, yp in zip(y_true, y_pred):\n"
            "        for t, p in zip(yt, yp):\n"
            "            p = min(1.0 - eps, max(eps, p))\n"
            "            total -= t * math.log(p)\n"
            "    return round(total / n, 10)\n",
            lambda low: bool(
                re.search(
                    r"\bcross[- ]?entropy\b|"
                    r"\bcategorical\s+cross[- ]?entropy\b|"
                    r"\blog\s*loss\b",
                    low,
                )
            )
            and "binary" not in low,
            examples=(
                (
                    ([[1.0, 0.0], [0.0, 1.0]], [[0.9, 0.1], [0.2, 0.8]]),
                    0.1642520335,
                ),
            ),
        ),
        T(
            "layer_normalization",
            "def layer_normalization(x, eps=1e-5):\n"
            '    """Layer norm over last dimension (educational, no affine).\n'
            "    x: list[float] or list[list[float]]. Returns same shape, mean~0 var~1.\n"
            '    """\n'
            "    import math\n"
            "    def _norm_vec(v):\n"
            "        n = len(v)\n"
            "        if n == 0:\n"
            "            return []\n"
            "        mean = sum(v) / n\n"
            "        var = sum((a - mean) ** 2 for a in v) / n\n"
            "        inv = 1.0 / math.sqrt(var + eps)\n"
            "        return [round((a - mean) * inv, 8) for a in v]\n"
            "    if not x:\n"
            "        return []\n"
            "    if isinstance(x[0], (list, tuple)):\n"
            "        return [_norm_vec(list(row)) for row in x]\n"
            "    return _norm_vec(list(x))\n",
            lambda low: bool(
                re.search(
                    r"\blayer[- ]?norm(?:alization)?\b|"
                    r"\blayernorm\b",
                    low,
                )
            )
            and "batch" not in low,
            examples=(
                (
                    ([1.0, 2.0, 3.0],),
                    [-1.22473569, 0.0, 1.22473569],
                ),
            ),
        ),
        T(
            "scaled_dot_product_attention",
            "def scaled_dot_product_attention(Q, K, V):\n"
            '    """Scaled dot-product attention (Vaswani et al., educational).\n'
            "    Q,K,V: list[list[float]] (seq, d). Returns (seq, d_v) attended values.\n"
            '    """\n'
            "    import math\n"
            "    def matmul(A, B):\n"
            "        return [\n"
            "            [sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))]\n"
            "            for i in range(len(A))\n"
            "        ]\n"
            "    def transpose(M):\n"
            "        return [list(row) for row in zip(*M)]\n"
            "    def softmax_rows(M):\n"
            "        out = []\n"
            "        for row in M:\n"
            "            m = max(row)\n"
            "            ex = [math.exp(x - m) for x in row]\n"
            "            s = sum(ex) or 1.0\n"
            "            out.append([e / s for e in ex])\n"
            "        return out\n"
            "    d = len(K[0]) if K else 1\n"
            "    scale = 1.0 / math.sqrt(d)\n"
            "    scores = matmul(Q, transpose(K))\n"
            "    scores = [[x * scale for x in row] for row in scores]\n"
            "    weights = softmax_rows(scores)\n"
            "    out = matmul(weights, V)\n"
            "    return [[round(x, 8) for x in row] for row in out]\n",
            lambda low: bool(
                re.search(
                    r"\bscaled\s+dot[- ]?product\s+attention\b|"
                    r"\battention\s+scores?\b|"
                    r"\bdot[- ]?product\s+attention\b|"
                    r"\bself[- ]?attention\b|"
                    r"\bmulti[- ]?head\s+attention\b",
                    low,
                )
            ),
            examples=(
                (
                    (
                        [[1.0, 0.0], [0.0, 1.0]],
                        [[1.0, 0.0], [0.0, 1.0]],
                        [[1.0, 2.0], [3.0, 4.0]],
                    ),
                    [[1.6604769, 2.6604769], [2.3395231, 3.3395231]],
                ),
            ),
        ),
    ]
