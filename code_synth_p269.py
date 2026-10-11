"""Cycle 572: Directed-graph cycle detection.

Loaded early so educational graph asks beat broader stubs.
Self-checking examples keep CodeAgent verification deterministic.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "detect_cycle_directed",
            "def detect_cycle_directed(n, edges):\n"
            '    """True if the directed graph (0..n-1, list of (u, v) edges) has a cycle."""\n'
            "    g = [[] for _ in range(int(n))]\n"
            "    for u, v in edges:\n"
            "        if 0 <= u < n and 0 <= v < n:\n"
            "            g[u].append(v)\n"
            "    # 0 = white, 1 = gray (on stack), 2 = black\n"
            "    color = [0] * n\n"
            "\n"
            "    def dfs(u):\n"
            "        color[u] = 1\n"
            "        for v in g[u]:\n"
            "            if color[v] == 1:\n"
            "                return True\n"
            "            if color[v] == 0 and dfs(v):\n"
            "                return True\n"
            "        color[u] = 2\n"
            "        return False\n"
            "\n"
            "    for i in range(n):\n"
            "        if color[i] == 0 and dfs(i):\n"
            "            return True\n"
            "    return False\n",
            lambda low: bool(
                re.search(
                    r"\bdetect(?:s|ing)? (?:a )?cycle\b.{0,40}\bdirected\b|"
                    r"\bcycle (?:detection|detect(?:ion|ing)?)\b.{0,32}\bdirected\b|"
                    r"\bcycle (?:in|of) (?:a )?directed (?:graph|digraph)\b|"
                    r"\bdirected (?:graph|digraph).{0,24}(?:has|contains?|have) (?:a )?cycle\b|"
                    r"\bhas[_ ]cycle[_ ]directed\b",
                    low,
                )
            )
            and "undirected" not in low
            and "linked" not in low,
            (
                ((4, [(0, 1), (1, 2), (2, 0)]), True),
                ((3, [(0, 1), (1, 2)]), False),
                ((2, [(0, 1), (1, 0)]), True),
            ),
        ),
    ]
