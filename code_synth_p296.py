"""Cycle 596: comb sort, gnome sort, odd-even (brick) sort,
Gale-Shapley stable marriage, bead sort, pigeonhole sort.

Educational pure-Python classics previously unmatched by match_template.
Matchers kept narrow so they do not steal existing sort / matching templates.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "comb_sort",
            "def comb_sort(items):\n"
            '    """Comb sort with shrink factor 1.3. Returns a new list."""\n'
            "    a = list(items)\n"
            "    n = len(a)\n"
            "    gap = n\n"
            "    shrink = 1.3\n"
            "    sorted_flag = False\n"
            "    while not sorted_flag:\n"
            "        gap = max(1, int(gap / shrink))\n"
            "        sorted_flag = gap == 1\n"
            "        i = 0\n"
            "        while i + gap < n:\n"
            "            if a[i] > a[i + gap]:\n"
            "                a[i], a[i + gap] = a[i + gap], a[i]\n"
            "                sorted_flag = False\n"
            "            i += 1\n"
            "    return a\n",
            lambda q: bool(re.search(r"comb\s+sort", q, re.I)),
            examples=(
                (([8, 4, 1, 56, 3, -44, 23, -6, 28, 0],), [-44, -6, 0, 1, 3, 4, 8, 23, 28, 56]),
                (([1, 2, 3],), [1, 2, 3]),
            ),
        ),
        T(
            "gnome_sort",
            "def gnome_sort(items):\n"
            '    """Gnome sort (garden gnome). Returns a new list."""\n'
            "    a = list(items)\n"
            "    i = 0\n"
            "    while i < len(a):\n"
            "        if i == 0 or a[i] >= a[i - 1]:\n"
            "            i += 1\n"
            "        else:\n"
            "            a[i], a[i - 1] = a[i - 1], a[i]\n"
            "            i -= 1\n"
            "    return a\n",
            lambda q: bool(re.search(r"gnome\s+sort", q, re.I)),
            examples=(
                (([4, 2, 7, 1],), [1, 2, 4, 7]),
                (([],), []),
            ),
        ),
        T(
            "odd_even_sort",
            "def odd_even_sort(items):\n"
            '    """Odd-even (brick) sort. Returns a new list."""\n'
            "    a = list(items)\n"
            "    n = len(a)\n"
            "    sorted_flag = False\n"
            "    while not sorted_flag:\n"
            "        sorted_flag = True\n"
            "        for i in range(1, n - 1, 2):\n"
            "            if a[i] > a[i + 1]:\n"
            "                a[i], a[i + 1] = a[i + 1], a[i]\n"
            "                sorted_flag = False\n"
            "        for i in range(0, n - 1, 2):\n"
            "            if a[i] > a[i + 1]:\n"
            "                a[i], a[i + 1] = a[i + 1], a[i]\n"
            "                sorted_flag = False\n"
            "    return a\n",
            lambda q: bool(re.search(r"(odd[\s-]*even|brick)\s+sort", q, re.I)),
            examples=(
                (([5, 3, 1, 4, 2],), [1, 2, 3, 4, 5]),
                (([1],), [1]),
            ),
        ),
        T(
            "gale_shapley",
            "def gale_shapley(men_prefs, women_prefs):\n"
            '    """Gale-Shapley deferred acceptance. Returns men->woman matching (0-based)."""\n'
            "    n = len(men_prefs)\n"
            "    free = list(range(n))\n"
            "    next_prop = [0] * n\n"
            "    engaged = [-1] * n  # woman -> man\n"
            "    man_of = [-1] * n\n"
            "    rank = [{w: r for r, w in enumerate(prefs)} for prefs in women_prefs]\n"
            "    while free:\n"
            "        m = free.pop(0)\n"
            "        w = men_prefs[m][next_prop[m]]\n"
            "        next_prop[m] += 1\n"
            "        if engaged[w] == -1:\n"
            "            engaged[w] = m\n"
            "            man_of[m] = w\n"
            "        else:\n"
            "            m2 = engaged[w]\n"
            "            if rank[w][m] < rank[w][m2]:\n"
            "                engaged[w] = m\n"
            "                man_of[m] = w\n"
            "                man_of[m2] = -1\n"
            "                free.append(m2)\n"
            "            else:\n"
            "                free.append(m)\n"
            "    return man_of\n",
            lambda q: bool(re.search(r"(gale[\s-]*shapley|stable\s+marriage)", q, re.I)),
            examples=(
                (([[0, 1], [1, 0]], [[0, 1], [1, 0]]), [0, 1]),
                (([[1, 0], [0, 1]], [[0, 1], [1, 0]]), [1, 0]),
            ),
        ),
        T(
            "bead_sort",
            "def bead_sort(items):\n"
            '    """Bead (gravity / abacus) sort for non-negative integers. Returns new list."""\n'
            "    xs = [int(x) for x in items]\n"
            "    if not xs:\n"
            "        return []\n"
            "    if any(x < 0 for x in xs):\n"
            "        raise ValueError('bead sort expects non-negative ints')\n"
            "    max_v = max(xs)\n"
            "    if max_v == 0:\n"
            "        return xs[:]\n"
            "    beads = [0] * max_v\n"
            "    for x in xs:\n"
            "        for i in range(x):\n"
            "            beads[i] += 1\n"
            "    # Collect from the bottom so the result is ascending\n"
            "    out = [0] * len(xs)\n"
            "    for level in range(max_v):\n"
            "        count = beads[level]\n"
            "        for k in range(count):\n"
            "            out[len(xs) - 1 - k] += 1\n"
            "    return out\n",
            lambda q: bool(re.search(r"bead\s+sort", q, re.I)),
            examples=(
                (([3, 1, 4, 2],), [1, 2, 3, 4]),
                (([0, 0, 1],), [0, 0, 1]),
            ),
        ),
        T(
            "pigeonhole_sort",
            "def pigeonhole_sort(items):\n"
            '    """Pigeonhole sort for integers (small range). Returns a new list."""\n'
            "    xs = [int(x) for x in items]\n"
            "    if not xs:\n"
            "        return []\n"
            "    lo, hi = min(xs), max(xs)\n"
            "    size = hi - lo + 1\n"
            "    holes = [0] * size\n"
            "    for x in xs:\n"
            "        holes[x - lo] += 1\n"
            "    out = []\n"
            "    for i, c in enumerate(holes):\n"
            "        out.extend([i + lo] * c)\n"
            "    return out\n",
            lambda q: bool(re.search(r"pigeonhole\s+sort", q, re.I)),
            examples=(
                (([5, 1, 3, 1, 4],), [1, 1, 3, 4, 5]),
                (([-2, 0, -1],), [-2, -1, 0]),
            ),
        ),
    ]
