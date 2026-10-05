"""Cycle 433: k-th grammar, pancake sort, revealed deck, advantage shuffle, max chunks, malware spread.

Unmatched medium titles. Matchers are id- or phrase-gated so wiggle-sort, sort-array,
and rain-water templates are not stolen.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "kth_grammar",
            "def kth_grammar(n, k):\n"
            '    """Bit parity of the 1-based index in the grammar row (LeetCode 779)."""\n'
            "    return bin(int(k) - 1).count('1') % 2\n",
            lambda low: bool(
                re.search(r"\bleetcode 779\b", low)
                or "kth grammar" in low
                or "k-th symbol in grammar" in low
                or "kth symbol in grammar" in low
            ),
            (
                ((1, 1), 0),
                ((2, 2), 1),
                ((4, 5), 1),
            ),
        ),
        T(
            "pancake_sort",
            "def pancake_sort(arr):\n"
            '    """Prefix flips that sort a permutation of 1..n (LeetCode 969)."""\n'
            "    arr = [int(x) for x in arr]\n"
            "    res = []\n"
            "    for size in range(len(arr), 1, -1):\n"
            "        idx = arr.index(size)\n"
            "        if idx == size - 1:\n"
            "            continue\n"
            "        if idx != 0:\n"
            "            arr[: idx + 1] = reversed(arr[: idx + 1])\n"
            "            res.append(idx + 1)\n"
            "        arr[:size] = reversed(arr[:size])\n"
            "        res.append(size)\n"
            "    return res\n",
            lambda low: bool(
                re.search(r"\bleetcode 969\b", low)
                or "pancake sort" in low
                or "pancake sorting" in low
            ),
            (
                (([3, 2, 4, 1],), [3, 4, 2, 3, 2]),
                (([1, 2, 3],), []),
            ),
        ),
        T(
            "deck_revealed_increasing",
            "def deck_revealed_increasing(deck):\n"
            '    """Order a deck so revealed cards increase (LeetCode 950)."""\n'
            "    from collections import deque\n"
            "    deck = sorted(int(x) for x in deck)\n"
            "    dq = deque()\n"
            "    for card in reversed(deck):\n"
            "        if dq:\n"
            "            dq.appendleft(dq.pop())\n"
            "        dq.appendleft(card)\n"
            "    return list(dq)\n",
            lambda low: bool(
                re.search(r"\bleetcode 950\b", low)
                or "reveal cards in increasing order" in low
                or "deck revealed increasing" in low
            ),
            (
                (([17, 13, 11, 2, 3, 5, 7],), [2, 13, 3, 11, 5, 17, 7]),
                (([1, 2, 3],), [1, 3, 2]),
            ),
        ),
        T(
            "advantage_shuffle",
            "def advantage_count(nums1, nums2):\n"
            '    """Permute nums1 to beat nums2 as often as possible (LeetCode 870)."""\n'
            "    nums1 = [int(x) for x in nums1]\n"
            "    nums2 = [int(x) for x in nums2]\n"
            "    n = len(nums1)\n"
            "    s1 = sorted(nums1)\n"
            "    order = sorted(range(n), key=lambda i: nums2[i])\n"
            "    res = [0] * n\n"
            "    lo, hi = 0, n - 1\n"
            "    for i in order:\n"
            "        if s1[lo] > nums2[i]:\n"
            "            res[i] = s1[lo]\n"
            "            lo += 1\n"
            "        else:\n"
            "            res[i] = s1[hi]\n"
            "            hi -= 1\n"
            "    return res\n"
            "\n"
            "def advantage_shuffle(nums1, nums2):\n"
            "    return advantage_count(nums1, nums2)\n",
            lambda low: bool(
                re.search(r"\bleetcode 870\b", low)
                or "advantage shuffle" in low
                or "advantage count" in low
            ),
            (
                (([2, 7, 11, 15], [1, 10, 4, 11]), [2, 11, 7, 15]),
                (([12, 24, 8, 32], [13, 25, 32, 11]), [24, 12, 8, 32]),
            ),
        ),
        T(
            "max_chunks_to_sorted",
            "def max_chunks_to_sorted(arr):\n"
            '    """Max chunks of a 0..n-1 permutation that sort independently (LeetCode 769)."""\n'
            "    ans = mx = 0\n"
            "    for i, x in enumerate(arr):\n"
            "        mx = max(mx, int(x))\n"
            "        if mx == i:\n"
            "            ans += 1\n"
            "    return ans\n",
            lambda low: bool(
                re.search(r"\bleetcode 769\b", low)
                or (
                    "max chunks to make sorted" in low
                    and "ii" not in low
                    and "2" not in low
                )
            ),
            (
                (([4, 3, 2, 1, 0],), 1),
                (([1, 0, 2, 3, 4],), 4),
            ),
        ),
        T(
            "min_malware_spread",
            "def min_malware_spread(graph, initial):\n"
            '    """Node to remove to minimize malware spread (LeetCode 924)."""\n'
            "    n = len(graph)\n"
            "    parent = list(range(n))\n"
            "\n"
            "    def find(x):\n"
            "        while parent[x] != x:\n"
            "            parent[x] = parent[parent[x]]\n"
            "            x = parent[x]\n"
            "        return x\n"
            "\n"
            "    def union(a, b):\n"
            "        ra, rb = find(a), find(b)\n"
            "        if ra != rb:\n"
            "            parent[rb] = ra\n"
            "\n"
            "    for i in range(n):\n"
            "        for j in range(i + 1, n):\n"
            "            if graph[i][j]:\n"
            "                union(i, j)\n"
            "    size = {}\n"
            "    for i in range(n):\n"
            "        r = find(i)\n"
            "        size[r] = size.get(r, 0) + 1\n"
            "    infected = {}\n"
            "    for i in initial:\n"
            "        r = find(int(i))\n"
            "        infected[r] = infected.get(r, 0) + 1\n"
            "    best = min(int(i) for i in initial)\n"
            "    best_saved = -1\n"
            "    for i in sorted(int(x) for x in initial):\n"
            "        r = find(i)\n"
            "        saved = size[r] if infected[r] == 1 else 0\n"
            "        if saved > best_saved:\n"
            "            best_saved = saved\n"
            "            best = i\n"
            "    return best\n",
            lambda low: bool(
                re.search(r"\bleetcode 924\b", low)
                or (
                    "minimize malware spread" in low
                    and "ii" not in low
                )
            ),
            (
                (([[1, 1, 0], [1, 1, 0], [0, 0, 1]], [0, 1]), 0),
                (([[1, 0, 0], [0, 1, 0], [0, 0, 1]], [0, 2]), 0),
                (([[1, 1, 1], [1, 1, 1], [1, 1, 1]], [1, 2]), 1),
            ),
        ),
    ]
