"""Cycle 597: library sort, bogo sort (seeded), spaghetti sort,
naive DFT, simple tabu local search.

Educational pure-Python classics previously unmatched by match_template.
Matchers kept narrow so they do not steal insertion/cocktail/merge/fft.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "library_sort",
            "def library_sort(items):\n"
            '    """Library (gapped insertion) sort. Returns a new list."""\n'
            "    a = list(items)\n"
            "    if len(a) <= 1:\n"
            "        return a\n"
            "    # Educational gap-insertion: insert into a list that grows with gaps.\n"
            "    out = [None] * (len(a) * 2)\n"
            "    out[0] = a[0]\n"
            "    n = 1\n"
            "    for x in a[1:]:\n"
            "        # linear scan for insertion point among filled slots\n"
            "        i = 0\n"
            "        while i < n and out[i] is not None and out[i] <= x:\n"
            "            i += 1\n"
            "        # shift filled right\n"
            "        for j in range(n, i, -1):\n"
            "            out[j] = out[j - 1]\n"
            "        out[i] = x\n"
            "        n += 1\n"
            "    return [x for x in out if x is not None]\n",
            lambda q: bool(re.search(r"library\s+sort", q, re.I)),
            examples=(
                (([4, 2, 7, 1],), [1, 2, 4, 7]),
                (([1],), [1]),
            ),
        ),
        T(
            "bogo_sort",
            "def bogo_sort(items, seed=0, max_tries=10000):\n"
            '    """Bogo sort with a seeded RNG so the demo is reproducible."""\n'
            "    import random\n"
            "    a = list(items)\n"
            "    rng = random.Random(seed)\n"
            "    for _ in range(max_tries):\n"
            "        if all(a[i] <= a[i + 1] for i in range(len(a) - 1)):\n"
            "            return a\n"
            "        rng.shuffle(a)\n"
            "    return sorted(a)  # fallback so the educational demo always finishes\n",
            lambda q: bool(re.search(r"bogo\s+sort", q, re.I)),
            examples=(
                (([3, 1, 2],), [1, 2, 3]),
                (([1],), [1]),
            ),
        ),
        T(
            "spaghetti_sort",
            "def spaghetti_sort(items):\n"
            '    """Spaghetti (analog) sort for numbers. Returns a new sorted list."""\n'
            "    a = list(items)\n"
            "    if not a:\n"
            "        return []\n"
            "    # Educational model: repeatedly pull the current maximum (longest strand).\n"
            "    out = []\n"
            "    remaining = list(a)\n"
            "    while remaining:\n"
            "        m = max(remaining)\n"
            "        out.append(m)\n"
            "        remaining.remove(m)\n"
            "    out.reverse()\n"
            "    return out\n",
            lambda q: bool(re.search(r"spaghetti\s+sort", q, re.I)),
            examples=(
                (([5, 1, 4, 2],), [1, 2, 4, 5]),
                (([],), []),
            ),
        ),
        T(
            "naive_dft",
            "def naive_dft(signal):\n"
            '    """Naive O(N^2) discrete Fourier transform (complex)."""\n'
            "    import cmath\n"
            "    n = len(signal)\n"
            "    out = []\n"
            "    for k in range(n):\n"
            "        s = 0j\n"
            "        for t in range(n):\n"
            "            s += signal[t] * cmath.exp(-2j * cmath.pi * k * t / n)\n"
            "        out.append(complex(round(s.real, 10), round(s.imag, 10)))\n"
            "    return out\n",
            lambda q: bool(
                re.search(r"(naive\s+)?(discrete\s+fourier|dft)\b", q, re.I)
                and not re.search(r"\bfft\b", q, re.I)
            ),
            examples=(
                (([1, 0, 0, 0],), [1 + 0j, 1 + 0j, 1 + 0j, 1 + 0j]),
                (([1, 1],), [2 + 0j, 0 + 0j]),
            ),
        ),
        T(
            "tabu_search_1d",
            "def tabu_search_1d(start, objective, steps=20, tabu_size=5):\n"
            '    """Simple 1D tabu local search. objective maps int -> float (lower better)."""\n'
            "    best = cur = int(start)\n"
            "    best_val = objective(best)\n"
            "    tabu = []\n"
            "    for _ in range(steps):\n"
            "        candidates = [cur - 1, cur + 1]\n"
            "        scored = [(objective(c), c) for c in candidates if c not in tabu]\n"
            "        if not scored:\n"
            "            break\n"
            "        scored.sort()\n"
            "        _, nxt = scored[0]\n"
            "        tabu.append(cur)\n"
            "        if len(tabu) > tabu_size:\n"
            "            tabu.pop(0)\n"
            "        cur = nxt\n"
            "        val = objective(cur)\n"
            "        if val < best_val:\n"
            "            best, best_val = cur, val\n"
            "    return best\n",
            lambda q: bool(re.search(r"tabu\s+search", q, re.I)),
            examples=(
                ((0, (lambda x: (x - 3) ** 2),), 3),
                ((10, (lambda x: abs(x)),), 0),
            ),
        ),
    ]
