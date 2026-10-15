"""Cycle 586: Newton interpolation, linear algebra, SAM, geometry, lazy segtree.

newton_interpolation, matrix_determinant, solve_linear_system,
count_distinct_substrings (suffix automaton), min_area_bounding_rectangle,
lazy_segment_tree.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "newton_interpolation",
            "def newton_interpolation(xs, ys, x):\n"
            '    """Newton divided-difference interpolation. Returns p(x).\n'
            "\n"
            "    Builds divided-difference coefficients then evaluates the Newton form.\n"
            "    Educational pure-Python implementation.\n"
            '    """\n'
            "    n = len(xs)\n"
            "    if n == 0 or n != len(ys):\n"
            "        raise ValueError('xs and ys must be non-empty and same length')\n"
            "    coef = list(ys)\n"
            "    for j in range(1, n):\n"
            "        for i in range(n - 1, j - 1, -1):\n"
            "            denom = xs[i] - xs[i - j]\n"
            "            if denom == 0:\n"
            "                raise ValueError('duplicate x')\n"
            "            coef[i] = (coef[i] - coef[i - 1]) / denom\n"
            "    result = coef[-1]\n"
            "    for i in range(n - 2, -1, -1):\n"
            "        result = result * (x - xs[i]) + coef[i]\n"
            "    return result\n",
            lambda q: bool(re.search(r"newton.{0,24}interpolat|divided[- ]difference", q, re.I)),
            examples=(
                (([0, 1, 2], [1, 2, 4], 1), 2),
                (([0, 1, 2], [1, 3, 7], 1.5), 4.75),
                (([1, 2], [3, 5], 1.5), 4.0),
            ),
        ),
        T(
            "matrix_determinant",
            "def matrix_determinant(a):\n"
            '    """Determinant of a square matrix via Gaussian elimination with partial pivoting.\n'
            "\n"
            "    Returns 0.0 for a singular matrix. Educational pure-Python implementation.\n"
            '    """\n'
            "    n = len(a)\n"
            "    if n == 0 or any(len(row) != n for row in a):\n"
            "        raise ValueError('square matrix required')\n"
            "    m = [row[:] for row in a]\n"
            "    det = 1.0\n"
            "    for i in range(n):\n"
            "        pivot = i\n"
            "        for k in range(i + 1, n):\n"
            "            if abs(m[k][i]) > abs(m[pivot][i]):\n"
            "                pivot = k\n"
            "        if abs(m[pivot][i]) < 1e-12:\n"
            "            return 0.0\n"
            "        if pivot != i:\n"
            "            m[i], m[pivot] = m[pivot], m[i]\n"
            "            det = -det\n"
            "        det *= m[i][i]\n"
            "        for k in range(i + 1, n):\n"
            "            factor = m[k][i] / m[i][i]\n"
            "            for j in range(i, n):\n"
            "                m[k][j] -= factor * m[i][j]\n"
            "    return round(det, 9)\n",
            lambda q: bool(re.search(r"matrix\s+determinant|determinant\s+of\s+(a\s+)?matrix|compute\s+the\s+determinant", q, re.I))
            and "gaussian" not in q.lower(),
            examples=(
                (([[1, 2], [3, 4]],), -2.0),
                (([[1, 0], [0, 1]],), 1.0),
                (([[1, 2, 3], [0, 1, 4], [5, 6, 0]],), 1.0),
            ),
        ),
        T(
            "solve_linear_system",
            "def solve_linear_system(a, b):\n"
            '    """Solve Ax = b by Gaussian elimination. Returns the solution list, or None if singular.\n'
            "\n"
            "    Educational pure-Python implementation with partial pivoting.\n"
            '    """\n'
            "    n = len(a)\n"
            "    if n == 0 or len(b) != n or any(len(row) != n for row in a):\n"
            "        return None\n"
            "    m = [row[:] + [b[i]] for i, row in enumerate(a)]\n"
            "    for i in range(n):\n"
            "        pivot = i\n"
            "        for k in range(i + 1, n):\n"
            "            if abs(m[k][i]) > abs(m[pivot][i]):\n"
            "                pivot = k\n"
            "        if abs(m[pivot][i]) < 1e-12:\n"
            "            return None\n"
            "        m[i], m[pivot] = m[pivot], m[i]\n"
            "        for k in range(i + 1, n):\n"
            "            factor = m[k][i] / m[i][i]\n"
            "            for j in range(i, n + 1):\n"
            "                m[k][j] -= factor * m[i][j]\n"
            "    x = [0.0] * n\n"
            "    for i in range(n - 1, -1, -1):\n"
            "        s = m[i][n]\n"
            "        for j in range(i + 1, n):\n"
            "            s -= m[i][j] * x[j]\n"
            "        x[i] = s / m[i][i]\n"
            "    return x\n",
            lambda q: bool(re.search(r"solve\s+(a\s+)?linear\s+system|solve\s+ax\s*=\s*b|linear\s+system\s+solver", q, re.I)),
            examples=(
                (([[2, 1], [1, 3]], [5, 10]), [1.0, 3.0]),
                (([[1, 0], [0, 1]], [4, 7]), [4.0, 7.0]),
                (([[1, 1], [2, 2]], [1, 3]), None),
            ),
        ),
        T(
            "count_distinct_substrings",
            "def count_distinct_substrings(s):\n"
            '    """Number of distinct substrings via a suffix automaton.\n'
            "\n"
            "    Builds the SAM online and sums (length[v] - length[link[v]]) over states.\n"
            "    Educational pure-Python implementation.\n"
            '    """\n'
            "    if not s:\n"
            "        return 0\n"
            "    length = [0]\n"
            "    link = [-1]\n"
            "    trans = [{}]\n"
            "    last = 0\n"
            "\n"
            "    def sam_extend(c):\n"
            "        nonlocal last\n"
            "        cur = len(length)\n"
            "        length.append(length[last] + 1)\n"
            "        link.append(-1)\n"
            "        trans.append({})\n"
            "        p = last\n"
            "        while p != -1 and c not in trans[p]:\n"
            "            trans[p][c] = cur\n"
            "            p = link[p]\n"
            "        if p == -1:\n"
            "            link[cur] = 0\n"
            "        else:\n"
            "            q = trans[p][c]\n"
            "            if length[p] + 1 == length[q]:\n"
            "                link[cur] = q\n"
            "            else:\n"
            "                clone = len(length)\n"
            "                length.append(length[p] + 1)\n"
            "                link.append(link[q])\n"
            "                trans.append(dict(trans[q]))\n"
            "                while p != -1 and trans[p].get(c) == q:\n"
            "                    trans[p][c] = clone\n"
            "                    p = link[p]\n"
            "                link[q] = link[cur] = clone\n"
            "        last = cur\n"
            "\n"
            "    for ch in s:\n"
            "        sam_extend(ch)\n"
            "    total = 0\n"
            "    for v in range(1, len(length)):\n"
            "        total += length[v] - length[link[v]]\n"
            "    return total\n",
            lambda q: bool(re.search(r"suffix\s+automaton|distinct\s+substrings?.{0,32}suffix|count\s+distinct\s+substrings", q, re.I))
            and "prefix" not in q.lower(),
            examples=(
                (("aba",), 5),
                (("abc",), 6),
                (("",), 0),
            ),
        ),
        T(
            "min_area_bounding_rectangle",
            "def min_area_bounding_rectangle(points):\n"
            '    """Minimum-area bounding rectangle of a point set (convex hull + rotating calipers).\n'
            "\n"
            "    Returns the area as a float. Educational pure-Python implementation.\n"
            '    """\n'
            "    import math\n"
            "    pts = list({(float(x), float(y)) for x, y in points})\n"
            "    if len(pts) <= 1:\n"
            "        return 0.0\n"
            "    pts.sort()\n"
            "\n"
            "    def cross(o, a, b):\n"
            "        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])\n"
            "\n"
            "    lower = []\n"
            "    for p in pts:\n"
            "        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:\n"
            "            lower.pop()\n"
            "        lower.append(p)\n"
            "    upper = []\n"
            "    for p in reversed(pts):\n"
            "        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:\n"
            "            upper.pop()\n"
            "        upper.append(p)\n"
            "    hull = lower[:-1] + upper[:-1]\n"
            "    if len(hull) <= 1:\n"
            "        return 0.0\n"
            "    if len(hull) == 2:\n"
            "        return 0.0\n"
            "    n = len(hull)\n"
            "    best = float('inf')\n"
            "    for i in range(n):\n"
            "        dx = hull[(i + 1) % n][0] - hull[i][0]\n"
            "        dy = hull[(i + 1) % n][1] - hull[i][1]\n"
            "        length = math.hypot(dx, dy)\n"
            "        if length == 0:\n"
            "            continue\n"
            "        ux, uy = dx / length, dy / length\n"
            "        vx, vy = -uy, ux\n"
            "        min_u = min_v = float('inf')\n"
            "        max_u = max_v = float('-inf')\n"
            "        for p in hull:\n"
            "            pu = ux * p[0] + uy * p[1]\n"
            "            pv = vx * p[0] + vy * p[1]\n"
            "            min_u = min(min_u, pu)\n"
            "            max_u = max(max_u, pu)\n"
            "            min_v = min(min_v, pv)\n"
            "            max_v = max(max_v, pv)\n"
            "        area = (max_u - min_u) * (max_v - min_v)\n"
            "        if area < best:\n"
            "            best = area\n"
            "    return best if best < float('inf') else 0.0\n",
            lambda q: bool(re.search(r"min(?:imum)?[- ]area\s+bounding\s+rectangle|minimum\s+area\s+bounding\s+box|rotating\s+calipers.{0,24}min(?:imum)?[- ]area", q, re.I)),
            examples=(
                (([(0, 0), (1, 0), (1, 1), (0, 1)],), 1.0),
                (([(0, 0), (2, 0), (2, 1), (0, 1)],), 2.0),
                (([(0, 0), (1, 0)],), 0.0),
            ),
        ),
        T(
            "lazy_segment_tree",
            "def lazy_segment_tree(n, ops):\n"
            '    """Segment tree with lazy range-add and range-sum.\n'
            "\n"
            "    ops are ('add', l, r, v) or ('sum', l, r), 0-based inclusive.\n"
            "    Returns the list of sum results. Educational pure-Python implementation.\n"
            '    """\n'
            "    if n <= 0:\n"
            "        return [0 for op in ops if op[0] == 'sum']\n"
            "    tree = [0] * (4 * n)\n"
            "    lazy = [0] * (4 * n)\n"
            "\n"
            "    def push(node, start, end):\n"
            "        if lazy[node] != 0:\n"
            "            tree[node] += (end - start + 1) * lazy[node]\n"
            "            if start != end:\n"
            "                lazy[2 * node] += lazy[node]\n"
            "                lazy[2 * node + 1] += lazy[node]\n"
            "            lazy[node] = 0\n"
            "\n"
            "    def update(node, start, end, l, r, v):\n"
            "        push(node, start, end)\n"
            "        if start > r or end < l:\n"
            "            return\n"
            "        if l <= start and end <= r:\n"
            "            lazy[node] += v\n"
            "            push(node, start, end)\n"
            "            return\n"
            "        mid = (start + end) // 2\n"
            "        update(2 * node, start, mid, l, r, v)\n"
            "        update(2 * node + 1, mid + 1, end, l, r, v)\n"
            "        tree[node] = tree[2 * node] + tree[2 * node + 1]\n"
            "\n"
            "    def query(node, start, end, l, r):\n"
            "        if start > r or end < l:\n"
            "            return 0\n"
            "        push(node, start, end)\n"
            "        if l <= start and end <= r:\n"
            "            return tree[node]\n"
            "        mid = (start + end) // 2\n"
            "        return query(2 * node, start, mid, l, r) + query(2 * node + 1, mid + 1, end, l, r)\n"
            "\n"
            "    out = []\n"
            "    for op in ops:\n"
            "        if op[0] == 'add':\n"
            "            _, l, r, v = op\n"
            "            update(1, 0, n - 1, l, r, v)\n"
            "        elif op[0] == 'sum':\n"
            "            _, l, r = op\n"
            "            out.append(query(1, 0, n - 1, l, r))\n"
            "    return out\n",
            lambda q: bool(re.search(r"lazy\s+(propagation|range)|segment\s+tree.{0,32}lazy|lazy\s+segment\s+tree", q, re.I)),
            examples=(
                ((5, [("add", 0, 4, 1), ("sum", 0, 4), ("add", 1, 3, 2), ("sum", 0, 4), ("sum", 2, 2)]), [5, 11, 3]),
                ((3, [("sum", 0, 2)]), [0]),
                ((1, [("add", 0, 0, 5), ("sum", 0, 0)]), [5]),
            ),
        ),
    ]
