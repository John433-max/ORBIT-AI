"""Cycle 571: Tower of Hanoi and unweighted shortest-path templates.

Loaded first so educational graph/recursion asks beat broader stubs.
Self-checking examples keep CodeAgent verification deterministic.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "tower_of_hanoi",
            "def tower_of_hanoi(n, src='A', aux='B', dst='C'):\n"
            '    """Return the list of (from, to) moves that solve Tower of Hanoi."""\n'
            "    moves = []\n"
            "\n"
            "    def rec(k, a, b, c):\n"
            "        if k == 0:\n"
            "            return\n"
            "        rec(k - 1, a, c, b)\n"
            "        moves.append((a, c))\n"
            "        rec(k - 1, b, a, c)\n"
            "\n"
            "    rec(int(n), src, aux, dst)\n"
            "    return moves\n",
            lambda low: bool(
                re.search(
                    r"\btower(?:s)?[- ]?of[- ]?hanoi\b|"
                    r"\bhanoi(?: towers?)?\b|"
                    r"\btowers? of hanoi\b",
                    low,
                )
            )
            and "champagne" not in low,
            (
                ((1,), [("A", "C")]),
                ((2,), [("A", "B"), ("A", "C"), ("B", "C")]),
                ((3,), [("A", "C"), ("A", "B"), ("C", "B"), ("A", "C"), ("B", "A"), ("B", "C"), ("A", "C")]),
            ),
        ),
        T(
            "shortest_path_unweighted",
            "def shortest_path_unweighted(graph, start, goal):\n"
            '    """BFS shortest path on an unweighted adjacency-list graph."""\n'
            "    from collections import deque\n"
            "    if start == goal:\n"
            "        return [start]\n"
            "    q = deque([(start, [start])])\n"
            "    seen = {start}\n"
            "    while q:\n"
            "        node, path = q.popleft()\n"
            "        for nei in graph.get(node, []):\n"
            "            if nei in seen:\n"
            "                continue\n"
            "            seen.add(nei)\n"
            "            nxt = path + [nei]\n"
            "            if nei == goal:\n"
            "                return nxt\n"
            "            q.append((nei, nxt))\n"
            "    return None\n",
            lambda low: bool(
                re.search(
                    r"\bshortest[- ]?path\b.{0,40}\bunweighted\b|"
                    r"\bunweighted\b.{0,24}\b(shortest[- ]?path|graph)\b|"
                    r"\bbfs\b.{0,16}\bshortest[- ]?path\b|"
                    r"\bshortest[- ]?path\b.{0,16}\bbfs\b",
                    low,
                )
            )
            and not re.search(r"\bweighted\b", low)
            and "dijkstra" not in low
            and "food" not in low
            and "keys" not in low
            and "obstacles" not in low,
            (
                (
                    ({"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}, "A", "D"),
                    ["A", "B", "D"],
                ),
                (
                    ({"S": ["A", "B"], "A": ["C"], "B": ["C"], "C": []}, "S", "C"),
                    ["S", "A", "C"],
                ),
                (
                    ({"X": ["Y"], "Y": []}, "X", "Z"),
                    None,
                ),
            ),
        ),
    ]
