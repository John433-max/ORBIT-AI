"""Cycle 561: Cartesian tree, Count-Min Sketch, HyperLogLog educational gaps.

Natural-language probes for these classic structures still fell through to
NotImplemented fallbacks after Cycle 560.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "cartesian_tree",
            "def cartesian_tree(arr):\n"
            '    """Build a Cartesian tree from array values (min-heap order).\n'
            "\n"
            "    Returns parent list: parent[i] is the parent index of i, or -1 for root.\n"
            "    Inorder traversal of the tree recovers the original array order.\n"
            "    Uses a monotonic stack in O(n).\n"
            '    """\n'
            "    n = len(arr)\n"
            "    parent = [-1] * n\n"
            "    stack = []\n"
            "    for i in range(n):\n"
            "        last = -1\n"
            "        while stack and arr[stack[-1]] > arr[i]:\n"
            "            last = stack.pop()\n"
            "        if stack:\n"
            "            parent[i] = stack[-1]\n"
            "        if last != -1:\n"
            "            parent[last] = i\n"
            "        stack.append(i)\n"
            "    return parent\n",
            lambda low: bool(
                re.search(r"\bcartesian[- ]tree\b", low)
                or re.search(r"\bbuild[- ]cartesian\b", low)
            )
            and "product" not in low
            and "polar" not in low
            and "to polar" not in low
            and "to cartesian" not in low,
            examples=(
                (([9, 3, 7, 1, 8, 12, 10, 20, 15, 18, 5],), [1, 3, 1, -1, 10, 6, 4, 8, 6, 8, 3]),
                (([1, 2, 3],), [-1, 0, 1]),
                (([3, 2, 1],), [1, 2, -1]),
                (([5],), [-1]),
            ),
        ),
        T(
            "count_min_sketch",
            "def count_min_sketch(stream, width=8, depth=3, queries=None):\n"
            '    """Count-Min Sketch approximate frequency estimator.\n'
            "\n"
            "    stream: iterable of hashable items.\n"
            "    width, depth: table dimensions (depth independent hash rows).\n"
            "    queries: optional list of items to estimate; default = unique stream items.\n"
            "    Returns dict item -> estimated count (never underestimates true count\n"
            "    in the classic CMS, but may overestimate due to collisions).\n"
            "    Uses a deterministic FNV-1a style hash so results are reproducible.\n"
            '    """\n'
            "    def _dhash(item, salt):\n"
            "        s = str(item) + '#' + str(salt)\n"
            "        h = 2166136261\n"
            "        for ch in s:\n"
            "            h ^= ord(ch)\n"
            "            h = (h * 16777619) & 0xFFFFFFFF\n"
            "        return h\n"
            "\n"
            "    table = [[0] * width for _ in range(depth)]\n"
            "    salts = [i * 0x9E3779B9 + 0x85EBCA6B for i in range(depth)]\n"
            "\n"
            "    def _idx(item, row):\n"
            "        return _dhash(item, salts[row]) % width\n"
            "\n"
            "    seen = []\n"
            "    seen_set = set()\n"
            "    for x in stream:\n"
            "        if x not in seen_set:\n"
            "            seen_set.add(x)\n"
            "            seen.append(x)\n"
            "        for r in range(depth):\n"
            "            table[r][_idx(x, r)] += 1\n"
            "\n"
            "    if queries is None:\n"
            "        queries = seen\n"
            "    out = {}\n"
            "    for q in queries:\n"
            "        est = min(table[r][_idx(q, r)] for r in range(depth))\n"
            "        out[q] = est\n"
            "    return out\n",
            lambda low: bool(
                re.search(r"\bcount[- ]?min[- ]sketch\b", low)
                or re.search(r"\bcms\b.{0,20}\b(sketch|frequency|count)\b", low)
                or re.search(r"\bcount[- ]min\b.{0,16}\b(sketch|frequency)\b", low)
            ),
            examples=(
                ((["a", "b", "a", "c", "a", "b"], 32, 5, ["a", "b", "c", "z"]), {"a": 3, "b": 2, "c": 1, "z": 0}),
                (([1, 1, 2], 16, 4, [1, 2, 3]), {1: 2, 2: 1, 3: 0}),
            ),
        ),
        T(
            "hyperloglog",
            "def hyperloglog(stream, p=4):\n"
            '    """HyperLogLog cardinality estimate (educational, small p).\n'
            "\n"
            "    p: precision bits (m = 2^p registers). Returns estimated distinct count\n"
            "    using the classic harmonic-mean estimator with alpha_m correction.\n"
            "    Uses a deterministic FNV-1a style hash so results are reproducible.\n"
            '    """\n'
            "    import math\n"
            "\n"
            "    def _dhash(item, salt):\n"
            "        s = str(item) + '#' + str(salt)\n"
            "        h = 2166136261\n"
            "        for ch in s:\n"
            "            h ^= ord(ch)\n"
            "            h = (h * 16777619) & 0xFFFFFFFF\n"
            "        return h\n"
            "\n"
            "    m = 1 << p\n"
            "    registers = [0] * m\n"
            "    mask = m - 1\n"
            "    salt = 0x9E3779B97F4A7C15\n"
            "\n"
            "    def _rho(w, max_bits=32):\n"
            "        if w == 0:\n"
            "            return max_bits + 1\n"
            "        r = 1\n"
            "        while (w & 1) == 0:\n"
            "            w >>= 1\n"
            "            r += 1\n"
            "        return r\n"
            "\n"
            "    for x in stream:\n"
            "        h = _dhash(x, salt)\n"
            "        idx = h & mask\n"
            "        w = h >> p\n"
            "        registers[idx] = max(registers[idx], _rho(w))\n"
            "\n"
            "    if m == 16:\n"
            "        alpha = 0.673\n"
            "    elif m == 32:\n"
            "        alpha = 0.697\n"
            "    elif m == 64:\n"
            "        alpha = 0.709\n"
            "    else:\n"
            "        alpha = 0.7213 / (1.0 + 1.079 / m)\n"
            "\n"
            "    inv_sum = sum(2.0 ** (-r) for r in registers)\n"
            "    raw = alpha * m * m / inv_sum\n"
            "\n"
            "    if raw <= 2.5 * m:\n"
            "        zeros = registers.count(0)\n"
            "        if zeros > 0:\n"
            "            raw = m * math.log(m / zeros)\n"
            "    return int(round(raw))\n",
            lambda low: bool(
                re.search(r"\bhyperloglog\b", low)
                or re.search(r"\bhll\b.{0,24}\b(cardin|estimate|distinct|unique)\b", low)
                or re.search(r"\bcardinality[- ]estimat", low)
            )
            and "email" not in low,
            examples=(
                ((["a", "b", "c", "a", "b"], 4), 3),
                ((list(range(20)), 5), 31),
                ((["x"] * 10, 4), 1),
            ),
        ),
    ]
