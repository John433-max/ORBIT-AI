"""Cycle 554: Andrew monotone-chain convex hull, Manacher LPS, KMP phrase alias.

knuth_morris_pratt defers to kmp_search (p247) when the prompt also contains
both "kmp" and "search".
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "convex_hull",
            "def convex_hull(points):\n"
            '    """Andrew monotone-chain convex hull (CCW, includes collinear)."""\n'
            "    pts = sorted({(float(x), float(y)) for x, y in points})\n"
            "    if len(pts) <= 1:\n"
            "        return list(pts)\n"
            "\n"
            "    def cross(o, a, b):\n"
            "        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])\n"
            "\n"
            "    lower = []\n"
            "    for p in pts:\n"
            "        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) < 0:\n"
            "            lower.pop()\n"
            "        lower.append(p)\n"
            "    upper = []\n"
            "    for p in reversed(pts):\n"
            "        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) < 0:\n"
            "            upper.pop()\n"
            "        upper.append(p)\n"
            "    return lower[:-1] + upper[:-1]\n",
            lambda low: bool(
                re.search(
                    r"\bconvex[- ]?hull\b|\bmonotone[- ]chain\b|\bandrew.?s? hull\b",
                    low,
                )
            )
            and "graham" not in low,
            (
                (([(0, 0), (1, 0), (0, 1), (1, 1), (0.5, 0.5)],), [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]),
                (([(0, 0), (1, 0), (0.5, 0.1)],), [(0.0, 0.0), (1.0, 0.0), (0.5, 0.1)]),
            ),
        ),
        T(
            "manacher_lps",
            "def manacher_lps(s):\n"
            '    """Longest palindromic substring via Manacher."""\n'
            "    if not s:\n"
            "        return \"\"\n"
            "    t = \"#\" + \"#\".join(s) + \"#\"\n"
            "    n = len(t)\n"
            "    p = [0] * n\n"
            "    c = r = 0\n"
            "    best_r = best_c = 0\n"
            "    for i in range(n):\n"
            "        mirror = 2 * c - i\n"
            "        if i < r:\n"
            "            p[i] = min(r - i, p[mirror])\n"
            "        a = i + p[i] + 1\n"
            "        b = i - p[i] - 1\n"
            "        while a < n and b >= 0 and t[a] == t[b]:\n"
            "            p[i] += 1\n"
            "            a += 1\n"
            "            b -= 1\n"
            "        if i + p[i] > r:\n"
            "            c, r = i, i + p[i]\n"
            "        if p[i] > best_r:\n"
            "            best_r, best_c = p[i], i\n"
            "    start = (best_c - best_r) // 2\n"
            "    return s[start:start + best_r]\n",
            lambda low: bool(
                re.search(
                    r"\bmanacher(?:s|'s)?(?: algorithm)?\b|"
                    r"\blongest palindromic substring\b|"
                    r"\blps via manacher\b",
                    low,
                )
            )
            and "subsequence" not in low
            and "that can be built" not in low
            and "rearrange" not in low,
            (
                (("babad",), "bab"),
                (("cbbd",), "bb"),
                (("",), ""),
            ),
        ),
        T(
            "knuth_morris_pratt",
            "def knuth_morris_pratt(text, pattern):\n"
            '    """First index of pattern in text via KMP, or -1."""\n'
            "    if pattern == '':\n"
            "        return 0\n"
            "    if text == '':\n"
            "        return -1\n"
            "    pi = [0] * len(pattern)\n"
            "    k = 0\n"
            "    for i in range(1, len(pattern)):\n"
            "        while k and pattern[k] != pattern[i]:\n"
            "            k = pi[k - 1]\n"
            "        if pattern[k] == pattern[i]:\n"
            "            k += 1\n"
            "        pi[i] = k\n"
            "    q = 0\n"
            "    for i, ch in enumerate(text):\n"
            "        while q and pattern[q] != ch:\n"
            "            q = pi[q - 1]\n"
            "        if pattern[q] == ch:\n"
            "            q += 1\n"
            "        if q == len(pattern):\n"
            "            return i - q + 1\n"
            "    return -1\n",
            lambda low: (
                bool(
                    re.search(
                        r"\bknuth[- ]morris[- ]pratt\b|"
                        r"\bmorris[- ]pratt\b|"
                        r"\bkmp (?:string |algorithm|matching)\b",
                        low,
                    )
                )
                and "tree" not in low
                # Prefer kmp_search when the request also says "kmp search"
                and not ("kmp" in low and "search" in low)
            ),
            (
                (("ababcababa", "ababa"), 5),
                (("hello", "ll"), 2),
                (("abc", "d"), -1),
                (("", "a"), -1),
            ),
        ),
    ]
