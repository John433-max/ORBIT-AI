"""Cycle 563: sqrt-tree RMQ and related educational templates (pack 290).

Placeholder text removed after accidental CI push. Full 6-template pack
lives in local artifacts; this minimal module keeps import/loader healthy.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "sqrt_tree_rmq",
            "def sqrt_tree_rmq(arr, queries):\n"
            '    """Range minimum queries via square-root decomposition.\n'
            "    Educational pure-Python.\n"
            '    """\n'
            "    n = len(arr)\n"
            "    if n == 0:\n"
            "        return []\n"
            "    B = max(1, int(n ** 0.5))\n"
            "    blocks = [min(arr[i:i + B]) for i in range(0, n, B)]\n"
            "    out = []\n"
            "    for l, r in queries:\n"
            "        if l > r:\n"
            "            l, r = r, l\n"
            "        ans = float('inf')\n"
            "        while l <= r and (l % B) != 0:\n"
            "            ans = min(ans, arr[l])\n"
            "            l += 1\n"
            "        while l + B - 1 <= r:\n"
            "            ans = min(ans, blocks[l // B])\n"
            "            l += B\n"
            "        while l <= r:\n"
            "            ans = min(ans, arr[l])\n"
            "            l += 1\n"
            "        out.append(ans if ans != float('inf') else None)\n"
            "    return out\n",
            lambda q: bool(
                re.search(
                    r"sqrt[- ]?tree|square[- ]root[- ]tree|"
                    r"sqrt[- ]?decomposition.{0,24}(rmq|range|min|query)|"
                    r"range (min|minimum).{0,16}sqrt",
                    q,
                    re.I,
                )
            )
            and "wavelet" not in q.lower(),
            examples=(
                (([3, 1, 4, 1, 5, 9, 2, 6], [(0, 3), (2, 5), (1, 1)]), [1, 1, 1]),
                (([5, 2, 8, 1, 9], [(0, 4), (1, 3)]), [1, 1]),
                (([7], [(0, 0)]), [7]),
            ),
        ),
    ]
