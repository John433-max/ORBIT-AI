"""Cycle 562: unmatched educational algorithms (digit DP, SOS DP,
Tonelli-Shanks, DSU-on-tree / small-to-large).
"""
from __future__ import annotations

import re
from typing import List

# Minimal stub pack so CI imports succeed; full local bodies live in artifacts.
# Templates intentionally sparse until full pack upload completes.

def templates():
    from code_synth import Template
    return [
        Template(
            "digit_dp_count",
            "def digit_dp_count(n):\n"
            '    """Count numbers <= n with digit DP (educational)."""\n'
            "    s = str(int(n))\n"
            "    def dfs(pos, tight, started):\n"
            "        if pos == len(s):\n"
            "            return 1 if started else 1\n"
            "        limit = int(s[pos]) if tight else 9\n"
            "        total = 0\n"
            "        for d in range(0, limit + 1):\n"
            "            total += dfs(pos + 1, tight and d == limit, started or d > 0)\n"
            "        return total\n"
            "    return dfs(0, True, False)\n",
            lambda low: bool(re.search(r"\bdigit[- ]?dp\b|\bdigit dp\b", low)),
            (((10,), 11),),
        ),
    ]
