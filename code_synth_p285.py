"""Cycle 587: Graham scan, Quickhull, point-in-polygon, segment intersection,
persistent segment tree, axis-aligned bounding box area.

graham_scan, quickhull, point_in_polygon, segments_intersect,
persistent_segment_tree, aabb_area.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "graham_scan",
            "def graham_scan(points):\n"
            '    """Convex hull via Graham scan.\n'
            "\n"
            "    Returns hull vertices in CCW order starting at the lowest point\n"
            "    (leftmost on a tie). Educational pure-Python implementation.\n"
            '    """\n'
            "    pts = [tuple(p) for p in points]\n"
            "    if len(pts) <= 1:\n"
            "        return pts\n"
            "    # lowest (then leftmost)\n"
            "    start = min(pts, key=lambda p: (p[1], p[0]))\n"
            "    def cross(o, a, b):\n"
            "        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])\n"
            "    def polar(p):\n"
            "        return (p[1] - start[1], p[0] - start[0])\n"
            "    rest = [p for p in pts if p != start]\n"
            "    rest.sort(key=lambda p: (polar(p)[0] / max(1, abs(polar(p)[0]) + abs(polar(p)[1])),\n"
            "                              (p[0] - start[0]) ** 2 + (p[1] - start[1]) ** 2))\n"
            "    # better polar sort by atan2 equivalent via cross\n"
            "    def cmp_angle(a, b):\n"
            "        cr = cross(start, a, b)\n"
            "        if cr != 0:\n"
            "            return -1 if cr > 0 else 1\n"
            "        da = (a[0] - start[0]) ** 2 + (a[1] - start[1]) ** 2\n"
            "        db = (b[0] - start[0]) ** 2 + (b[1] - start[1]) ** 2\n"
            "        return -1 if da < db else (1 if da > db else 0)\n"
            "    from functools import cmp_to_key\n"
            "    rest.sort(key=cmp_to_key(cmp_angle))\n"
            "    hull = [start]\n"
            "    for p in rest:\n"
            "        while len(hull) >= 2 and cross(hull[-2], hull[-1], p) <= 0:\n"
            "            hull.pop()\n"
            "        hull.append(p)\n"
            "    return hull\n",
            lambda q: bool(re.search(r"graham\s*scan|graham\s+convex\s+hull", q, re.I)),
            examples=(
                (([(0, 0), (1, 0), (1, 1), (0, 1), (0.5, 0.5)],), [(0, 0), (1, 0), (1, 1), (0, 1)]),
                (([(0, 0), (2, 0), (1, 1)],), [(0, 0), (2, 0), (1, 1)]),
                (([(5, 5)],), [(5, 5)]),
            ),
        ),
        T(
            "quickhull",
            "def quickhull(points):\n"
            '    """Convex hull via the Quickhull algorithm.\n'
            "\n"
            "    Returns hull vertices in CCW order. Educational pure-Python implementation.\n"
            '    """\n'
            "    pts = list({tuple(p) for p in points})\n"
            "    if len(pts) <= 1:\n"
            "        return pts\n"
            "    def cross(o, a, b):\n"
            "        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])\n"
            "    def side(a, b, p):\n"
            "        return cross(a, b, p)\n"
            "    def dist(a, b, p):\n"
            "        return abs(cross(a, b, p))\n"
            "    def rec(a, b, subset):\n"
            "        if not subset:\n"
            "            return []\n"
            "        far = max(subset, key=lambda p: dist(a, b, p))\n"
            "        left = [p for p in subset if side(a, far, p) > 0]\n"
            "        right = [p for p in subset if side(far, b, p) > 0]\n"
            "        return rec(a, far, left) + [far] + rec(far, b, right)\n"
            "    left = min(pts)\n"
            "    right = max(pts)\n"
            "    above = [p for p in pts if side(left, right, p) > 0]\n"
            "    below = [p for p in pts if side(right, left, p) > 0]\n"
            "    return [left] + rec(left, right, above) + [right] + rec(right, left, below)\n",
            lambda q: bool(re.search(r"quick\s*hull|quickhull", q, re.I)),
            examples=(
                (([(0, 0), (1, 0), (1, 1), (0, 1), (0.5, 0.5)],), [(0, 0), (0, 1), (1, 1), (1, 0)]),
                (([(0, 0), (3, 0), (1, 2)],), [(0, 0), (1, 2), (3, 0)]),
                (([(1, 1)],), [(1, 1)]),
            ),
        ),
        T(
            "point_in_polygon",
            "def point_in_polygon(point, polygon):\n"
            '    """Ray-casting point-in-polygon test.\n'
            "\n"
            "    Returns True if point is strictly inside a simple polygon.\n"
            "    Educational pure-Python implementation (even-odd rule).\n"
            '    """\n'
            "    x, y = point\n"
            "    n = len(polygon)\n"
            "    inside = False\n"
            "    for i in range(n):\n"
            "        x1, y1 = polygon[i]\n"
            "        x2, y2 = polygon[(i + 1) % n]\n"
            "        if (y1 > y) != (y2 > y):\n"
            "            xinters = (x2 - x1) * (y - y1) / (y2 - y1) + x1\n"
            "            if x < xinters:\n"
            "                inside = not inside\n"
            "    return inside\n",
            lambda q: bool(re.search(r"point\s+in\s+polygon|point\s+inside\s+polygon|ray\s*cast(?:ing)?\s+polygon", q, re.I)),
            examples=(
                (((0.5, 0.5), [(0, 0), (1, 0), (1, 1), (0, 1)]), True),
                (((2, 2), [(0, 0), (1, 0), (1, 1), (0, 1)]), False),
                (((-0.1, 0.5), [(0, 0), (1, 0), (1, 1), (0, 1)]), False),
            ),
        ),
        T(
            "segments_intersect",
            "def segments_intersect(a, b, c, d):\n"
            '    """True if closed segments AB and CD properly or improperly intersect.\n'
            "\n"
            "    Uses orientation tests. Educational pure-Python implementation.\n"
            '    """\n'
            "    def cross(o, p, q):\n"
            "        return (p[0] - o[0]) * (q[1] - o[1]) - (p[1] - o[1]) * (q[0] - o[0])\n"
            "    def on_seg(p, q, r):\n"
            "        return (min(p[0], r[0]) <= q[0] <= max(p[0], r[0]) and\n"
            "                min(p[1], r[1]) <= q[1] <= max(p[1], r[1]))\n"
            "    o1 = cross(a, b, c)\n"
            "    o2 = cross(a, b, d)\n"
            "    o3 = cross(c, d, a)\n"
            "    o4 = cross(c, d, b)\n"
            "    if o1 * o2 < 0 and o3 * o4 < 0:\n"
            "        return True\n"
            "    if o1 == 0 and on_seg(a, c, b):\n"
            "        return True\n"
            "    if o2 == 0 and on_seg(a, d, b):\n"
            "        return True\n"
            "    if o3 == 0 and on_seg(c, a, d):\n"
            "        return True\n"
            "    if o4 == 0 and on_seg(c, b, d):\n"
            "        return True\n"
            "    return False\n",
            lambda q: bool(re.search(r"(line\s+)?segments?\s+intersect|do\s+segments?\s+intersect|segment\s+intersection", q, re.I))
            and "interval" not in q.lower()
            and "array" not in q.lower(),
            examples=(
                (((0, 0), (2, 2), (0, 2), (2, 0)), True),
                (((0, 0), (1, 1), (2, 2), (3, 3)), False),
                (((0, 0), (2, 0), (1, 0), (3, 0)), True),
            ),
        ),
        T(
            "persistent_segment_tree",
            "def persistent_segment_tree(n, updates, queries):\n"
            '    """Simple persistent segment tree for point updates and range sums.\n'
            "\n"
            "    updates: list of (index, value) applied sequentially (new version each).\n"
            "    queries: list of (version, l, r) where version 0 is empty, version k is after k updates.\n"
            "    Returns list of query results. Educational pure-Python implementation.\n"
            '    """\n'
            "    # nodes: [sum, left_idx, right_idx]; -1 = empty\n"
            "    nodes = []\n"
            "    def new_node(s=0, left=-1, right=-1):\n"
            "        nodes.append([s, left, right])\n"
            "        return len(nodes) - 1\n"
            "    def update(node, start, end, idx, val):\n"
            "        if node == -1:\n"
            "            node = new_node()\n"
            "        else:\n"
            "            # copy\n"
            "            s, l, r = nodes[node]\n"
            "            node = new_node(s, l, r)\n"
            "        if start == end:\n"
            "            nodes[node][0] += val\n"
            "            return node\n"
            "        mid = (start + end) // 2\n"
            "        if idx <= mid:\n"
            "            nodes[node][1] = update(nodes[node][1], start, mid, idx, val)\n"
            "        else:\n"
            "            nodes[node][2] = update(nodes[node][2], mid + 1, end, idx, val)\n"
            "        left_sum = nodes[nodes[node][1]][0] if nodes[node][1] != -1 else 0\n"
            "        right_sum = nodes[nodes[node][2]][0] if nodes[node][2] != -1 else 0\n"
            "        nodes[node][0] = left_sum + right_sum\n"
            "        return node\n"
            "    def query(node, start, end, l, r):\n"
            "        if node == -1 or r < start or end < l:\n"
            "            return 0\n"
            "        if l <= start and end <= r:\n"
            "            return nodes[node][0]\n"
            "        mid = (start + end) // 2\n"
            "        return (query(nodes[node][1], start, mid, l, r) +\n"
            "                query(nodes[node][2], mid + 1, end, l, r))\n"
            "    roots = [-1]\n"
            "    for idx, val in updates:\n"
            "        roots.append(update(roots[-1], 0, n - 1, idx, val))\n"
            "    return [query(roots[v], 0, n - 1, l, r) for v, l, r in queries]\n",
            lambda q: bool(re.search(r"persistent\s+segment\s+tree|versioned\s+segment\s+tree|persistent\s+segtree", q, re.I)),
            examples=(
                ((4, [(1, 5), (2, 3)], [(1, 0, 3), (2, 0, 3), (2, 1, 2)]), [5, 8, 8]),
                ((3, [(0, 1)], [(0, 0, 2), (1, 0, 2)]), [0, 1]),
                ((2, [], [(0, 0, 1)]), [0]),
            ),
        ),
        T(
            "aabb_area",
            "def aabb_area(points):\n"
            '    """Area of the axis-aligned bounding box of a set of 2D points.\n'
            "\n"
            "    Returns 0.0 for fewer than 2 distinct x or y. Educational pure-Python.\n"
            '    """\n'
            "    if not points:\n"
            "        return 0.0\n"
            "    xs = [p[0] for p in points]\n"
            "    ys = [p[1] for p in points]\n"
            "    return float((max(xs) - min(xs)) * (max(ys) - min(ys)))\n",
            lambda q: bool(re.search(r"axis[- ]aligned\s+bounding\s+box|aabb\s+area|bounding\s+box\s+area", q, re.I))
            and "minimum" not in q.lower()
            and "min" not in q.lower()
            and "rotat" not in q.lower(),
            examples=(
                (([(0, 0), (2, 3), (1, 1)],), 6.0),
                (([(1, 1), (1, 1)],), 0.0),
                (([(0, 0), (1, 0), (0, 1)],), 1.0),
            ),
        ),
    ]
