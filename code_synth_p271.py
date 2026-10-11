"""Cycle 573: Palindromic tree (eertree) + basic wavelet tree k-th.

Loaded early so educational asks for eertree / palindromic tree and
wavelet-tree range selection beat generic stubs.
Self-checking examples keep CodeAgent verification deterministic.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "eertree_distinct_palindromes",
            "def eertree_distinct_palindromes(s):\n"
            '    """Number of distinct palindromic substrings via eertree (palindromic tree)."""\n'
            "    if not s:\n"
            "        return 0\n"
            "    # nodes: 0 = odd root (len -1), 1 = even root (len 0)\n"
            "    length = [-1, 0]\n"
            "    link = [0, 0]\n"
            "    nxt = [{}, {}]\n"
            "    last = 1\n"
            "    for i, ch in enumerate(s):\n"
            "        cur = last\n"
            "        while True:\n"
            "            clen = length[cur]\n"
            "            if i - clen - 1 >= 0 and s[i - clen - 1] == ch:\n"
            "                break\n"
            "            cur = link[cur]\n"
            "        if ch in nxt[cur]:\n"
            "            last = nxt[cur][ch]\n"
            "            continue\n"
            "        new_node = len(length)\n"
            "        length.append(length[cur] + 2)\n"
            "        nxt.append({})\n"
            "        nxt[cur][ch] = new_node\n"
            "        if length[new_node] == 1:\n"
            "            link.append(1)\n"
            "        else:\n"
            "            suf = link[cur]\n"
            "            while True:\n"
            "                slen = length[suf]\n"
            "                if i - slen - 1 >= 0 and s[i - slen - 1] == ch:\n"
            "                    break\n"
            "                suf = link[suf]\n"
            "            link.append(nxt[suf].get(ch, 1))\n"
            "        last = new_node\n"
            "    return len(length) - 2\n",
            lambda low: bool(
                re.search(
                    r"\beertree\b|"
                    r"\bpalindrom(?:ic|e)[- ]?tree\b|"
                    r"\bcount distinct palindromic substrings?\b|"
                    r"\bnumber of distinct palindromes?\b",
                    low,
                )
            )
            and "manacher" not in low,
            (
                (("ababa",), 5),
                (("aaa",), 3),
                (("abc",), 3),
                (("",), 0),
            ),
        ),
        T(
            "wavelet_kth_smallest",
            "def wavelet_kth_smallest(arr, l, r, k):\n"
            '    """0-based k-th smallest (0 <= k < r-l+1) in arr[l..r] via wavelet tree."""\n'
            "    if not arr or l > r or k < 0 or k >= r - l + 1:\n"
            "        return None\n"
            "    a = list(arr)\n"
            "    lo, hi = min(a), max(a)\n"
            "\n"
            "    class Node:\n"
            "        def __init__(self, vals, x, y):\n"
            "            self.lo, self.hi = x, y\n"
            "            self.freq = [0]\n"
            "            if not vals or x == y:\n"
            "                for _ in vals:\n"
            "                    self.freq.append(self.freq[-1] + 1)\n"
            "                self.left = self.right = None\n"
            "                return\n"
            "            mid = (x + y) // 2\n"
            "            left_vals, right_vals = [], []\n"
            "            for v in vals:\n"
            "                if v <= mid:\n"
            "                    left_vals.append(v)\n"
            "                    self.freq.append(self.freq[-1] + 1)\n"
            "                else:\n"
            "                    right_vals.append(v)\n"
            "                    self.freq.append(self.freq[-1])\n"
            "            self.left = Node(left_vals, x, mid)\n"
            "            self.right = Node(right_vals, mid + 1, y)\n"
            "\n"
            "        def kth(self, L, R, kk):\n"
            "            if L > R:\n"
            "                return None\n"
            "            if self.lo == self.hi:\n"
            "                return self.lo\n"
            "            left_count = self.freq[R + 1] - self.freq[L]\n"
            "            if kk < left_count:\n"
            "                return self.left.kth(self.freq[L], self.freq[R + 1] - 1, kk)\n"
            "            return self.right.kth(\n"
            "                L - self.freq[L], R - self.freq[R + 1], kk - left_count\n"
            "            )\n"
            "\n"
            "    root = Node(a, lo, hi)\n"
            "    return root.kth(l, r, k)\n",
            lambda low: bool(
                re.search(
                    r"\bwavelet[- ]?tree\b|"
                    r"\bk[- ]?th smallest.{0,24}wavelet\b|"
                    r"\bwavelet.{0,24}(?:kth|k-th|range)\b",
                    low,
                )
            ),
            (
                (([3, 1, 4, 1, 5], 0, 4, 0), 1),
                (([3, 1, 4, 1, 5], 0, 4, 2), 3),
                (([3, 1, 4, 1, 5], 1, 3, 1), 1),
                (([5, 4, 3, 2, 1], 0, 4, 4), 5),
            ),
        ),
    ]
