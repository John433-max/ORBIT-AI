"""Cycle 599: full SVD (Jacobi), QR via Gram-Schmidt, decision tree (Gini).

Previously unmatched or stolen by singularize English noun helper.
Educational pure-Python; no NumPy required.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "full_svd",
            "def full_svd(A, tol=1e-10, max_iter=200):\n"
            '    """Full SVD A ~= U @ diag(S) @ Vt via Jacobi on A.T@A (educational).\n'
            "    A: list[list[float]] m x n. Returns (U, S, Vt) with S descending.\n"
            '    """\n'
            "    import math\n"
            "    m = len(A)\n"
            "    n = len(A[0]) if m else 0\n"
            "    AtA = [[0.0] * n for _ in range(n)]\n"
            "    for i in range(n):\n"
            "        for j in range(n):\n"
            "            s = 0.0\n"
            "            for k in range(m):\n"
            "                s += A[k][i] * A[k][j]\n"
            "            AtA[i][j] = s\n"
            "    V = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]\n"
            "    for _ in range(max_iter):\n"
            "        max_off = 0.0\n"
            "        p = q = 0\n"
            "        for i in range(n):\n"
            "            for j in range(i + 1, n):\n"
            "                if abs(AtA[i][j]) > max_off:\n"
            "                    max_off = abs(AtA[i][j])\n"
            "                    p, q = i, j\n"
            "        if max_off < tol:\n"
            "            break\n"
            "        app, aqq, apq = AtA[p][p], AtA[q][q], AtA[p][q]\n"
            "        if abs(apq) < 1e-18:\n"
            "            continue\n"
            "        tau = (aqq - app) / (2.0 * apq)\n"
            "        t = math.copysign(1.0 / (abs(tau) + math.sqrt(1.0 + tau * tau)), tau)\n"
            "        c = 1.0 / math.sqrt(1.0 + t * t)\n"
            "        s = t * c\n"
            "        for i in range(n):\n"
            "            aip, aiq = AtA[i][p], AtA[i][q]\n"
            "            AtA[i][p] = c * aip - s * aiq\n"
            "            AtA[i][q] = s * aip + c * aiq\n"
            "        for j in range(n):\n"
            "            apj, aqj = AtA[p][j], AtA[q][j]\n"
            "            AtA[p][j] = c * apj - s * aqj\n"
            "            AtA[q][j] = s * apj + c * aqj\n"
            "        AtA[p][p] = c * c * app - 2 * s * c * apq + s * s * aqq\n"
            "        AtA[q][q] = s * s * app + 2 * s * c * apq + c * c * aqq\n"
            "        AtA[p][q] = AtA[q][p] = 0.0\n"
            "        for i in range(n):\n"
            "            vip, viq = V[i][p], V[i][q]\n"
            "            V[i][p] = c * vip - s * viq\n"
            "            V[i][q] = s * vip + c * viq\n"
            "    eig = [AtA[i][i] for i in range(n)]\n"
            "    order = sorted(range(n), key=lambda i: -eig[i])\n"
            "    S = [math.sqrt(max(0.0, eig[i])) for i in order]\n"
            "    Vt = [[V[j][i] for j in range(n)] for i in order]\n"
            "    U = [[0.0] * n for _ in range(m)]\n"
            "    for col, si in enumerate(S):\n"
            "        if si < tol:\n"
            "            continue\n"
            "        for r in range(m):\n"
            "            acc = 0.0\n"
            "            for c in range(n):\n"
            "                acc += A[r][c] * Vt[col][c]\n"
            "            U[r][col] = acc / si\n"
            "    # Round for stable equality in educational self-checks\n"
            "    def _r(x):\n"
            "        return round(x, 8)\n"
            "    U = [[_r(x) for x in row] for row in U]\n"
            "    S = [_r(x) for x in S]\n"
            "    Vt = [[_r(x) for x in row] for row in Vt]\n"
            "    return U, S, Vt\n",
            lambda low: bool(
                re.search(
                    r"\bfull\s+svd\b|"
                    r"\bsingular\s+value\s+decomposition\b|"
                    r"\bsvd\b.*\b(matrix|decomposition|full)\b|"
                    r"\b(matrix|full)\b.*\bsvd\b|"
                    r"\bimplement\s+svd\b|"
                    r"\bsvd\s+decomposition\b|"
                    r"\bpython function for full svd\b",
                    low,
                )
            )
            and "singularize" not in low
            and "noun" not in low,
            examples=(
                (
                    ([[3.0, 0.0], [0.0, 2.0]],),
                    ([[1.0, 0.0], [0.0, 1.0]], [3.0, 2.0], [[1.0, 0.0], [0.0, 1.0]]),
                ),
                (
                    ([[2.0, 0.0], [0.0, 2.0]],),
                    ([[1.0, 0.0], [0.0, 1.0]], [2.0, 2.0], [[1.0, 0.0], [0.0, 1.0]]),
                ),
            ),
        ),
        T(
            "qr_decomposition",
            "def qr_decomposition(A):\n"
            '    """Thin QR via classical Gram-Schmidt. A: m x n list-of-lists, m>=n.\n'
            "    Returns (Q, R) with Q orthonormal columns, R upper-triangular.\n"
            '    """\n'
            "    import math\n"
            "    m = len(A)\n"
            "    n = len(A[0]) if m else 0\n"
            "    Q = [[0.0] * n for _ in range(m)]\n"
            "    R = [[0.0] * n for _ in range(n)]\n"
            "    for j in range(n):\n"
            "        v = [A[i][j] for i in range(m)]\n"
            "        for i in range(j):\n"
            "            rij = sum(Q[k][i] * A[k][j] for k in range(m))\n"
            "            R[i][j] = rij\n"
            "            for k in range(m):\n"
            "                v[k] -= rij * Q[k][i]\n"
            "        norm = math.sqrt(sum(x * x for x in v))\n"
            "        R[j][j] = norm\n"
            "        if norm < 1e-15:\n"
            "            continue\n"
            "        for k in range(m):\n"
            "            Q[k][j] = v[k] / norm\n"
            "    def _r(x):\n"
            "        return round(x, 8)\n"
            "    Q = [[_r(x) for x in row] for row in Q]\n"
            "    R = [[_r(x) for x in row] for row in R]\n"
            "    return Q, R\n",
            lambda low: bool(
                re.search(
                    r"\bqr\s*(decomposition|factorization|factorisation)\b|"
                    r"\bgram[-\s]?schmidt\b.*\bqr\b|"
                    r"\bqr\b.*\bgram[-\s]?schmidt\b|"
                    r"\bimplement\s+qr\b|"
                    r"\bqr\s+decomposition\b",
                    low,
                )
            )
            and "sqrt_decomposition" not in low
            and "range sum" not in low
            and "range_sum" not in low,
            examples=(
                (
                    ([[1.0, 1.0], [0.0, 1.0]],),
                    ([[1.0, 0.0], [0.0, 1.0]], [[1.0, 1.0], [0.0, 1.0]]),
                ),
                (
                    ([[2.0, 0.0], [0.0, 3.0]],),
                    ([[1.0, 0.0], [0.0, 1.0]], [[2.0, 0.0], [0.0, 3.0]]),
                ),
            ),
        ),
        T(
            "decision_tree",
            "def decision_tree(X, y, max_depth=3):\n"
            '    """Train a tiny binary decision-tree classifier (Gini).\n'
            "    X: list of list[float]; y: list[int] labels 0/1.\n"
            "    Returns nested dict: {'feat', 'thr', 'left', 'right'} or {'leaf': class}.\n"
            '    """\n'
            "    def gini(labels):\n"
            "        n = len(labels)\n"
            "        if n == 0:\n"
            "            return 0.0\n"
            "        p1 = sum(1 for v in labels if v == 1) / n\n"
            "        return 1.0 - p1 * p1 - (1 - p1) * (1 - p1)\n"
            "    def majority(labels):\n"
            "        return 1 if sum(labels) >= (len(labels) - sum(labels)) else 0\n"
            "    def split(rows, labels, depth):\n"
            "        if depth <= 0 or len(set(labels)) <= 1 or not rows:\n"
            "            return {'leaf': majority(labels)}\n"
            "        n_feat = len(rows[0])\n"
            "        best = None\n"
            "        best_gain = -1.0\n"
            "        parent = gini(labels)\n"
            "        for j in range(n_feat):\n"
            "            vals = sorted(set(r[j] for r in rows))\n"
            "            for t in vals:\n"
            "                left_i = [i for i, r in enumerate(rows) if r[j] <= t]\n"
            "                right_i = [i for i in range(len(rows)) if i not in set(left_i)]\n"
            "                if not left_i or not right_i:\n"
            "                    continue\n"
            "                gl = gini([labels[i] for i in left_i])\n"
            "                gr = gini([labels[i] for i in right_i])\n"
            "                n = len(rows)\n"
            "                gain = parent - (len(left_i) / n) * gl - (len(right_i) / n) * gr\n"
            "                if gain > best_gain:\n"
            "                    best_gain = gain\n"
            "                    best = (j, t, left_i, right_i)\n"
            "        if best is None or best_gain <= 0:\n"
            "            return {'leaf': majority(labels)}\n"
            "        j, t, li, ri = best\n"
            "        return {\n"
            "            'feat': j,\n"
            "            'thr': t,\n"
            "            'left': split([rows[i] for i in li], [labels[i] for i in li], depth - 1),\n"
            "            'right': split([rows[i] for i in ri], [labels[i] for i in ri], depth - 1),\n"
            "        }\n"
            "    return split(list(X), list(y), max_depth)\n"
            "\n"
            "def decision_tree_predict(tree, row):\n"
            '    """Predict class for one row given a tree from decision_tree."""\n'
            "    node = tree\n"
            "    while 'leaf' not in node:\n"
            "        if row[node['feat']] <= node['thr']:\n"
            "            node = node['left']\n"
            "        else:\n"
            "            node = node['right']\n"
            "    return node['leaf']\n",
            lambda low: bool(
                re.search(
                    r"\bdecision\s*tree\b|"
                    r"\bdecision[-_]?tree\b|"
                    r"\bgini\b.*\btree\b|"
                    r"\btree\b.*\bclassifier\b.*\b(from scratch|gini|train)\b|"
                    r"\bimplement\s+decision\s*tree\b",
                    low,
                )
            )
            and "bst" not in low
            and "binary search" not in low
            and "segment" not in low
            and "fenwick" not in low
            and "trie" not in low
            and "avl" not in low
            and "red black" not in low,
            examples=(
                # Perfect separation on feature 0; depth enough to make pure leaves
                (
                    (
                        [[0.0], [1.0], [0.0], [1.0]],
                        [0, 1, 0, 1],
                        2,
                    ),
                    {
                        "feat": 0,
                        "thr": 0.0,
                        "left": {"leaf": 0},
                        "right": {"leaf": 1},
                    },
                ),
            ),
        ),
    ]
