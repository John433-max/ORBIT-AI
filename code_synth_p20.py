"""Cycle 278: additional verified Python templates (pack 20)."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "most_common_word",
            "def most_common_word(paragraph, banned):\n"
            '    """Most frequent word in paragraph that is not banned (case-insensitive)."""\n'
            "    from collections import Counter\n"
            "    import re as _re\n"
            "    ban = {str(w).lower() for w in banned}\n"
            "    words = _re.findall(r\"[a-z]+\", str(paragraph).lower())\n"
            "    cnt = Counter(w for w in words if w not in ban)\n"
            "    return cnt.most_common(1)[0][0] if cnt else ''\n",
            lambda low: bool(
                re.search(
                    r"\bmost common word\b|"
                    r"\bmost_common_word\b|"
                    r"\bmost frequent word\b",
                    low,
                )
            )
            and "majority" not in low,
            ((("Bob hit a ball, the hit BALL flew far after it was hit.", ["hit"]), "ball"),),
        ),
        T(
            "construct_rectangle",
            "def construct_rectangle(area):\n"
            '    """L, W with L*W=area, L>=W, L-W minimized."""\n'
            "    import math\n"
            "    w = int(math.isqrt(int(area)))\n"
            "    while int(area) % w:\n"
            "        w -= 1\n"
            "    return [int(area) // w, w]\n",
            lambda low: bool(
                re.search(
                    r"\bconstruct rectangle\b|"
                    r"\bconstruct_rectangle\b|"
                    r"\bconstruct the rectangle\b",
                    low,
                )
            )
            and "overlap" not in low
            and "maximal rectangle" not in low,
            (((4,), [2, 2]), ((37,), [37, 1]), ((122122,), [427, 286])),
        ),
        T(
            "binary_gap",
            "def binary_gap(n):\n"
            '    """Longest distance between two consecutive 1-bits in binary n."""\n'
            "    bits = bin(int(n))[2:]\n"
            "    last = -1\n"
            "    best = 0\n"
            "    for i, ch in enumerate(bits):\n"
            "        if ch == '1':\n"
            "            if last >= 0:\n"
            "                best = max(best, i - last)\n"
            "            last = i\n"
            "    return best\n",
            lambda low: bool(
                re.search(r"\bbinary gap\b|\bbinary_gap\b", low)
            )
            and "hamming" not in low,
            (((22,), 2), ((8,), 0), ((5,), 2)),
        ),
        T(
            "valid_boomerang",
            "def valid_boomerang(points):\n"
            '    """True if three points are distinct and not colinear."""\n'
            "    (x1, y1), (x2, y2), (x3, y3) = points\n"
            "    return (x1 - x2) * (y1 - y3) != (x1 - x3) * (y1 - y2)\n",
            lambda low: bool(
                re.search(r"\bvalid boomerang\b|\bvalid_boomerang\b|\bboomerang points\b", low)
            ),
            (
                (([[1, 1], [2, 3], [3, 2]],), True),
                (([[1, 1], [2, 2], [3, 3]],), False),
            ),
        ),
        T(
            "has_groups_size_x",
            "def has_groups_size_x(deck):\n"
            '    """True if cards can be partitioned into groups of size X>=2."""\n'
            "    from collections import Counter\n"
            "    from math import gcd\n"
            "    from functools import reduce\n"
            "    vals = list(Counter(deck).values())\n"
            "    if not vals:\n"
            "        return False\n"
            "    g = reduce(gcd, vals)\n"
            "    return g >= 2\n",
            lambda low: bool(
                re.search(
                    r"\bhas_groups_size_x\b|"
                    r"\bx of a kind in a deck\b|"
                    r"\bgroups size x\b|"
                    r"\bpartition deck into groups\b",
                    low,
                )
            )
            and "partition equal" not in low
            and "can_partition" not in low,
            (
                (([1, 2, 3, 4, 4, 3, 2, 1],), True),
                (([1, 1, 1, 2, 2, 2, 3, 3],), False),
            ),
        ),
        T(
            "largest_triangle_area",
            "def largest_triangle_area(points):\n"
            '    """Largest triangle area formed by any 3 points."""\n'
            "    best = 0.0\n"
            "    n = len(points)\n"
            "    for i in range(n):\n"
            "        x1, y1 = points[i]\n"
            "        for j in range(i + 1, n):\n"
            "            x2, y2 = points[j]\n"
            "            for k in range(j + 1, n):\n"
            "                x3, y3 = points[k]\n"
            "                area = abs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0\n"
            "                if area > best:\n"
            "                    best = area\n"
            "    return best\n",
            lambda low: bool(
                re.search(
                    r"\blargest triangle area\b|"
                    r"\blargest_triangle_area\b",
                    low,
                )
            )
            and "maximal rectangle" not in low
            and "largest rectangle" not in low,
            (
                (
                    ([[0, 0], [0, 1], [1, 0], [0, 2], [2, 0]],),
                    2.0,
                ),
            ),
        ),
    ]
