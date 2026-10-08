"""Cycle: string permutations were excluded from list permute and fell through.

List permute still owns non-string asks. This pack loads first.
"""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "permute_string",
            "def permute_string(s):\n"
            '    """All permutations of the characters in s (index-unique)."""\n'
            "    chars = list(s)\n"
            "    out = []\n"
            "    used = [False] * len(chars)\n"
            "    path = []\n"
            "\n"
            "    def dfs():\n"
            "        if len(path) == len(chars):\n"
            "            out.append(''.join(path))\n"
            "            return\n"
            "        for i, ch in enumerate(chars):\n"
            "            if used[i]:\n"
            "                continue\n"
            "            used[i] = True\n"
            "            path.append(ch)\n"
            "            dfs()\n"
            "            path.pop()\n"
            "            used[i] = False\n"
            "\n"
            "    dfs()\n"
            "    return out\n",
            lambda low: (
                "permut" in low
                and "string" in low
                and "next" not in low
                and "from permutation" not in low
            ),
            (
                (("ab",), ["ab", "ba"]),
                (("a",), ["a"]),
                (("",), [""]),
            ),
        ),
    ]
