"""Cycle 589: lower/upper bound, linear regression, 1D GD, Smith-Waterman, Needleman-Wunsch.

lower_bound, upper_bound, linear_regression, gradient_descent_1d,
smith_waterman, needleman_wunsch.
"""
from __future__ import annotations

import re
from code_synth import Template


def templates() -> list[Template]:
    return [
        Template(
            "lower_bound",
            "def lower_bound(arr, target):\n"
            "    \"\"\"First index i with arr[i] >= target (sorted arr).\"\"\"\n"
            "    lo, hi = 0, len(arr)\n"
            "    while lo < hi:\n"
            "        mid = (lo + hi) // 2\n"
            "        if arr[mid] < target:\n"
            "            lo = mid + 1\n"
            "        else:\n"
            "            hi = mid\n"
            "    return lo\n",
            lambda s: bool(
                re.search(r"\blower[-_ ]?bound\b", s)
                and not re.search(r"\bupper[-_ ]?bound\b", s)
            ),
            examples=((([1, 2, 2, 3], 2), 1), (([1, 3, 5], 4), 2)),
        ),
        Template(
            "upper_bound",
            "def upper_bound(arr, target):\n"
            "    \"\"\"First index i with arr[i] > target (sorted arr).\"\"\"\n"
            "    lo, hi = 0, len(arr)\n"
            "    while lo < hi:\n"
            "        mid = (lo + hi) // 2\n"
            "        if arr[mid] <= target:\n"
            "            lo = mid + 1\n"
            "        else:\n"
            "            hi = mid\n"
            "    return lo\n",
            lambda s: bool(re.search(r"\bupper[-_ ]?bound\b", s)),
            examples=((([1, 2, 2, 3], 2), 3), (([1, 3, 5], 3), 2)),
        ),
        Template(
            "linear_regression",
            "def linear_regression(xs, ys):\n"
            "    \"\"\"Ordinary least-squares slope and intercept for 1-D data.\n\n"
            "    Returns (slope, intercept) rounded to 6 decimals.\n"
            "    Educational pure-Python implementation.\n"
            "    \"\"\"\n"
            "    n = len(xs)\n"
            "    if n == 0:\n"
            "        return (0.0, 0.0)\n"
            "    sx = sum(xs)\n"
            "    sy = sum(ys)\n"
            "    sxx = sum(x * x for x in xs)\n"
            "    sxy = sum(x * y for x, y in zip(xs, ys))\n"
            "    denom = n * sxx - sx * sx\n"
            "    if abs(denom) < 1e-12:\n"
            "        return (0.0, round(sy / n, 6))\n"
            "    slope = (n * sxy - sx * sy) / denom\n"
            "    intercept = (sy - slope * sx) / n\n"
            "    return (round(slope, 6), round(intercept, 6))\n",
            lambda s: bool(
                re.search(r"\blinear[-_ ]?regression\b", s)
                or re.search(r"\bleast[-_ ]?squares\b.{0,40}\b(slope|intercept)\b", s)
            ),
            examples=(
                (([1, 2, 3], [2, 4, 6]), (2.0, 0.0)),
                (([0, 1, 2], [1, 2, 3]), (1.0, 1.0)),
                (([1, 1, 1], [2, 4, 6]), (0.0, 4.0)),
            ),
        ),
        Template(
            "gradient_descent_1d",
            "def gradient_descent_1d(f, df, x0, lr=0.1, steps=20):\n"
            "    \"\"\"1-D gradient descent. Returns final x.\"\"\"\n"
            "    x = float(x0)\n"
            "    for _ in range(steps):\n"
            "        x = x - lr * df(x)\n"
            "    return x\n",
            lambda s: bool(
                re.search(r"\b1[-_ ]?d\b.{0,20}\bgradient[-_ ]?descent\b", s)
                and re.search(r"\b(minimize|function|df)\b", s)
            ),
            examples=(),
        ),
        Template(
            "smith_waterman",
            "def smith_waterman(a, b, match=2, mismatch=-1, gap=-1):\n"
            "    \"\"\"Local alignment score (Smith-Waterman). Returns best score.\"\"\"\n"
            "    n, m = len(a), len(b)\n"
            "    H = [[0] * (m + 1) for _ in range(n + 1)]\n"
            "    best = 0\n"
            "    for i in range(1, n + 1):\n"
            "        for j in range(1, m + 1):\n"
            "            sc = match if a[i - 1] == b[j - 1] else mismatch\n"
            "            H[i][j] = max(0, H[i - 1][j - 1] + sc, H[i - 1][j] + gap, H[i][j - 1] + gap)\n"
            "            if H[i][j] > best:\n"
            "                best = H[i][j]\n"
            "    return best\n",
            lambda s: bool(re.search(r"\bsmith[-_ ]?waterman\b", s)),
            examples=((("ACACACTA", "AGCACACA"), 12),),
        ),
        Template(
            "needleman_wunsch",
            "def needleman_wunsch(a, b, match=1, mismatch=-1, gap=-1):\n"
            "    \"\"\"Global alignment score (Needleman-Wunsch).\"\"\"\n"
            "    n, m = len(a), len(b)\n"
            "    F = [[0] * (m + 1) for _ in range(n + 1)]\n"
            "    for i in range(1, n + 1):\n"
            "        F[i][0] = i * gap\n"
            "    for j in range(1, m + 1):\n"
            "        F[0][j] = j * gap\n"
            "    for i in range(1, n + 1):\n"
            "        for j in range(1, m + 1):\n"
            "            sc = match if a[i - 1] == b[j - 1] else mismatch\n"
            "            F[i][j] = max(F[i - 1][j - 1] + sc, F[i - 1][j] + gap, F[i][j - 1] + gap)\n"
            "    return F[n][m]\n",
            lambda s: bool(re.search(r"\bneedleman[-_ ]?wunsch\b", s)),
            examples=((("GCATGCU", "GATTACA"), 0),),
        ),
    ]
