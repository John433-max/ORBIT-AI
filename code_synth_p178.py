"""Cycle 460: algorithm-search helpers that must not fall through to a stub.

Loaded first so linear/rolling/shoelace phrases beat broader search templates.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "rolling_hash",
            "def rolling_hash(s, base=131, mod=1000000007):\n"
            '    """Polynomial rolling hash of a string (Rabin fingerprint)."""\n'
            "    h = 0\n"
            "    b = int(base)\n"
            "    m = int(mod)\n"
            "    for ch in str(s):\n"
            "        h = (h * b + ord(ch)) % m\n"
            "    return h\n",
            lambda low: "rolling hash" in low or "rolling_hash" in low,
            ((("ab",), 12805), (("",), 0), (("a",), 97)),
        ),
        T(
            "linear_search",
            "def linear_search(items, value):\n"
            '    """Return the first index of value, or -1."""\n'
            "    for i, item in enumerate(items):\n"
            "        if item == value:\n"
            "            return i\n"
            "    return -1\n",
            lambda low: bool(
                re.search(r"\blinear[- ]?search\b|\blinear_search\b", low)
                and "binary" not in low
            ),
            ((([4, 1, 7], 1), 1), (([4, 1, 7], 9), -1)),
        ),
        T(
            "triangle_area_points",
            "def triangle_area(a, b, c):\n"
            '    """Shoelace area of a triangle given three (x, y) points."""\n'
            "    (x1, y1), (x2, y2), (x3, y3) = a, b, c\n"
            "    return abs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0\n",
            lambda low: bool(
                re.search(r"\btriangle\b", low)
                and re.search(r"\b(area|shoelace)\b", low)
                and re.search(r"\b(point|points|vertices)\b", low)
                and "largest" not in low
            ),
            ((((0, 0), (4, 0), (0, 3)), 6.0), (((0, 0), (1, 0), (0, 1)), 0.5)),
        ),
        T(
            "shoelace_area",
            "def shoelace_area(points):\n"
            '    """Absolute shoelace area of a simple polygon."""\n'
            "    pts = list(points)\n"
            "    n = len(pts)\n"
            "    if n < 3:\n"
            "        return 0.0\n"
            "    s = 0.0\n"
            "    for i, (x1, y1) in enumerate(pts):\n"
            "        x2, y2 = pts[(i + 1) % n]\n"
            "        s += x1 * y2 - x2 * y1\n"
            "    return abs(s) / 2.0\n",
            lambda low: "shoelace" in low or "polygon area" in low,
            ((([(0, 0), (1, 0), (1, 1), (0, 1)],), 1.0), (([(0, 0), (1, 0)],), 0.0)),
        ),
        T(
            "rabin_karp",
            "def rabin_karp(text, pattern):\n"
            '    """Return start indexes of pattern in text (verified Rabin-Karp)."""\n'
            "    text, pattern = str(text), str(pattern)\n"
            "    n, m = len(text), len(pattern)\n"
            "    if m == 0:\n"
            "        return list(range(n + 1))\n"
            "    if m > n:\n"
            "        return []\n"
            "    base, mod = 256, 1000000007\n"
            "    ph = wh = 0\n"
            "    power = 1\n"
            "    for i in range(m):\n"
            "        ph = (ph * base + ord(pattern[i])) % mod\n"
            "        wh = (wh * base + ord(text[i])) % mod\n"
            "        if i:\n"
            "            power = (power * base) % mod\n"
            "    out = []\n"
            "    for i in range(n - m + 1):\n"
            "        if wh == ph and text[i:i + m] == pattern:\n"
            "            out.append(i)\n"
            "        if i + m < n:\n"
            "            wh = (wh - ord(text[i]) * power) % mod\n"
            "            wh = (wh * base + ord(text[i + m])) % mod\n"
            "    return out\n",
            lambda low: "rabin" in low or "rabin-karp" in low or "rabin karp" in low,
            ((("abcab", "ab"), [0, 3]), (("aaaa", "aa"), [0, 1, 2]), (("abc", "z"), [])),
        ),
    ]
