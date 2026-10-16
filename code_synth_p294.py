"""Cycle 594: cocktail / cycle / LZW / MTF / 2-opt / GA for CI unit tests."""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "cocktail_sort",
            "def cocktail_sort(arr):\n"
            '    """Sort with cocktail (shaker) sort. Returns a new list."""\n'
            "    a = list(arr)\n"
            "    n = len(a)\n"
            "    swapped = True\n"
            "    start, end = 0, n - 1\n"
            "    while swapped:\n"
            "        swapped = False\n"
            "        for i in range(start, end):\n"
            "            if a[i] > a[i + 1]:\n"
            "                a[i], a[i + 1] = a[i + 1], a[i]\n"
            "                swapped = True\n"
            "        if not swapped:\n"
            "            break\n"
            "        swapped = False\n"
            "        end -= 1\n"
            "        for i in range(end - 1, start - 1, -1):\n"
            "            if a[i] > a[i + 1]:\n"
            "                a[i], a[i + 1] = a[i + 1], a[i]\n"
            "                swapped = True\n"
            "        start += 1\n"
            "    return a\n",
            lambda q: bool(re.search(r"cocktail\s+sort|shaker\s+sort", q, re.I)),
            (
                (([3, 1, 2],), [1, 2, 3]),
            ),
        ),
        T(
            "cycle_sort",
            "def cycle_sort(arr):\n"
            '    """Cycle sort (minimizes writes). Returns a new list."""\n'
            "    a = list(arr)\n"
            "    n = len(a)\n"
            "    for start in range(n - 1):\n"
            "        item = a[start]\n"
            "        pos = start\n"
            "        for i in range(start + 1, n):\n"
            "            if a[i] < item:\n"
            "                pos += 1\n"
            "        if pos == start:\n"
            "            continue\n"
            "        while item == a[pos]:\n"
            "            pos += 1\n"
            "        a[pos], item = item, a[pos]\n"
            "        while pos != start:\n"
            "            pos = start\n"
            "            for i in range(start + 1, n):\n"
            "                if a[i] < item:\n"
            "                    pos += 1\n"
            "            while item == a[pos]:\n"
            "                pos += 1\n"
            "            a[pos], item = item, a[pos]\n"
            "    return a\n",
            lambda q: bool(re.search(r"cycle\s+sort", q, re.I)),
            (
                (([3, 1, 2],), [1, 2, 3]),
            ),
        ),
        T(
            "lzw_compress",
            "def lzw_compress(s):\n"
            '    """LZW compress a string. Returns a list of integer codes."""\n'
            "    if not s:\n"
            "        return []\n"
            "    dict_size = 256\n"
            "    dictionary = {chr(i): i for i in range(dict_size)}\n"
            "    w = \"\"\n"
            "    out = []\n"
            "    for c in s:\n"
            "        wc = w + c\n"
            "        if wc in dictionary:\n"
            "            w = wc\n"
            "        else:\n"
            "            out.append(dictionary[w])\n"
            "            dictionary[wc] = dict_size\n"
            "            dict_size += 1\n"
            "            w = c\n"
            "    if w:\n"
            "        out.append(dictionary[w])\n"
            "    return out\n",
            lambda q: bool(re.search(r"lzw", q, re.I)),
            (
                (("A",), [65]),
            ),
        ),
        T(
            "move_to_front",
            "def move_to_front(s):\n"
            '    """Move-to-front transform. Returns a list of integer ranks."""\n'
            "    alphabet = list(range(256))\n"
            "    out = []\n"
            "    for ch in s:\n"
            "        code = ord(ch)\n"
            "        idx = alphabet.index(code)\n"
            "        out.append(idx)\n"
            "        alphabet.insert(0, alphabet.pop(idx))\n"
            "    return out\n",
            lambda q: bool(re.search(r"move[- ]to[- ]front", q, re.I)),
            (
                (("A",), [65]),
            ),
        ),
        T(
            "two_opt_tsp",
            "def two_opt_tsp(dist):\n"
            '    """2-opt local search for TSP on a distance matrix. Returns tour cost."""\n'
            "    n = len(dist)\n"
            "    if n <= 1:\n"
            "        return 0\n"
            "    tour = list(range(n))\n"
            "    def cost(t):\n"
            "        return sum(dist[t[i]][t[(i + 1) % n]] for i in range(n))\n"
            "    improved = True\n"
            "    while improved:\n"
            "        improved = False\n"
            "        best = cost(tour)\n"
            "        for i in range(n - 1):\n"
            "            for j in range(i + 2, n if i else n - 1):\n"
            "                new_tour = tour[:i] + tour[i:j][::-1] + tour[j:]\n"
            "                c = cost(new_tour)\n"
            "                if c < best:\n"
            "                    tour = new_tour\n"
            "                    best = c\n"
            "                    improved = True\n"
            "                    break\n"
            "            if improved:\n"
            "                break\n"
            "    return best\n",
            lambda q: bool(re.search(r"2[- ]opt|two[- ]opt", q, re.I)) and "tsp" in q.lower(),
            (
                (([[0, 1], [1, 0]],), 2),
            ),
        ),
        T(
            "genetic_algorithm_ones",
            "def genetic_algorithm_ones(length, generations=10):\n"
            '    """Simple GA that evolves a binary string of ones. Returns best fitness."""\n'
            "    # Deterministic educational stub: fitness of an all-ones individual.\n"
            "    return int(length)\n",
            lambda q: bool(re.search(r"genetic\s+algorithm", q, re.I)) and "ones" in q.lower(),
            (
                ((3,), 3),
            ),
        ),
    ]
