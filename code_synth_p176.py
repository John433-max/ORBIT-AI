"""Cycle 458: Damerau OSA, Euler totient, RMSE, MAE, R^2, FNV-1a 32.

Pack loads first so phrase gates beat levenshtein / mean matchers.
"""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "damerau_levenshtein",
            "def damerau_levenshtein(a, b):\n"
            '    """Optimal string alignment distance (adjacent transposition)."""\n'
            "    s, t = str(a), str(b)\n"
            "    n, m = len(s), len(t)\n"
            "    dp = [[0] * (m + 1) for _ in range(n + 1)]\n"
            "    for i in range(n + 1):\n"
            "        dp[i][0] = i\n"
            "    for j in range(m + 1):\n"
            "        dp[0][j] = j\n"
            "    for i in range(1, n + 1):\n"
            "        for j in range(1, m + 1):\n"
            "            cost = 0 if s[i - 1] == t[j - 1] else 1\n"
            "            dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + cost)\n"
            "            if i > 1 and j > 1 and s[i - 1] == t[j - 2] and s[i - 2] == t[j - 1]:\n"
            "                dp[i][j] = min(dp[i][j], dp[i - 2][j - 2] + 1)\n"
            "    return dp[n][m]\n",
            lambda low: "damerau" in low,
            (
                (("ca", "ac"), 1),
                (("kitten", "sitting"), 3),
                (("", "abc"), 3),
            ),
        ),
        T(
            "euler_totient",
            "def euler_totient(n):\n"
            '    """Euler totient phi(n): count of integers in 1..n coprime to n."""\n'
            "    n = int(n)\n"
            "    if n <= 0:\n"
            "        return 0\n"
            "    result = n\n"
            "    x = n\n"
            "    p = 2\n"
            "    while p * p <= x:\n"
            "        if x % p == 0:\n"
            "            while x % p == 0:\n"
            "                x //= p\n"
            "            result -= result // p\n"
            "        p += 1 if p == 2 else 2\n"
            "    if x > 1:\n"
            "        result -= result // x\n"
            "    return result\n",
            lambda low: "totient" in low or "euler phi" in low or "phi(n)" in low,
            (
                ((1,), 1),
                ((9,), 6),
                ((10,), 4),
                ((36,), 12),
            ),
        ),
        T(
            "rmse",
            "def rmse(y, yhat):\n"
            '    """Root mean squared error, rounded to 6 decimals."""\n'
            "    if len(y) != len(yhat) or not y:\n"
            "        return None\n"
            "    err = sum((float(a) - float(b)) ** 2 for a, b in zip(y, yhat))\n"
            "    return round((err / len(y)) ** 0.5, 6)\n",
            lambda low: "rmse" in low or "root mean square" in low or "root-mean-square" in low,
            (
                (([1, 2, 3], [1, 2, 4]), 0.57735),
                (([1, 2], [1, 2]), 0.0),
            ),
        ),
        T(
            "mae",
            "def mae(y, yhat):\n"
            '    """Mean absolute error, rounded to 6 decimals."""\n'
            "    if len(y) != len(yhat) or not y:\n"
            "        return None\n"
            "    err = sum(abs(float(a) - float(b)) for a, b in zip(y, yhat))\n"
            "    return round(err / len(y), 6)\n",
            lambda low: "mean absolute error" in low or "mae" in low.split() or "mae of" in low,
            (
                (([1, 2, 3], [1, 2, 5]), 0.666667),
                (([1, 2], [1, 2]), 0.0),
            ),
        ),
        T(
            "r2_score",
            "def r2_score(y, yhat):\n"
            '    """Coefficient of determination, rounded to 6 decimals."""\n'
            "    if len(y) != len(yhat) or len(y) < 2:\n"
            "        return None\n"
            "    ys = [float(v) for v in y]\n"
            "    mean = sum(ys) / len(ys)\n"
            "    ss_tot = sum((a - mean) ** 2 for a in ys)\n"
            "    ss_res = sum((a - float(b)) ** 2 for a, b in zip(ys, yhat))\n"
            "    if ss_tot == 0:\n"
            "        return 1.0 if ss_res == 0 else 0.0\n"
            "    return round(1.0 - ss_res / ss_tot, 6)\n",
            lambda low: "r2 score" in low or "r-squared" in low or "r2_score" in low or "coefficient of determination" in low,
            (
                (([1, 2, 3], [1, 2, 3]), 1.0),
                (([1, 2, 3], [1, 2, 4]), 0.5),
            ),
        ),
        T(
            "fnv1a_32",
            "def fnv1a_32(text):\n"
            '    """FNV-1a 32-bit hash (offset basis 2166136261, prime 16777619)."""\n'
            "    h = 2166136261\n"
            "    for b in str(text).encode(\"utf-8\"):\n"
            "        h ^= b\n"
            "        h = (h * 16777619) & 0xFFFFFFFF\n"
            "    return h\n",
            lambda low: "fnv" in low,
            (
                (("",), 2166136261),
                (("a",), 3826002220),
                (("foobar",), 0xBF9CF968),
            ),
        ),
    ]
