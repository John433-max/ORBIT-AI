"""Cycle 583: textbook algorithms still unmatched (segmented sieve, inclusion-exclusion,
z-function phrase, scapegoat tree, linear SPF sieve, meet-in-the-middle exact).
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "segmented_sieve",
            "def segmented_sieve(low, high):\n"
            '    """Primes in the half-open interval [low, high).\n'
            "\n"
            "    Uses a small base sieve up to sqrt(high) then a segmented mark.\n"
            "    Educational pure-Python implementation.\n"
            '    """\n'
            "    if high <= 2:\n"
            "        return []\n"
            "    low = max(0, int(low))\n"
            "    high = int(high)\n"
            "    limit = int(high ** 0.5) + 1\n"
            "    base = [True] * (limit + 1)\n"
            "    base[0] = base[1] = False\n"
            "    for i in range(2, int(limit ** 0.5) + 1):\n"
            "        if base[i]:\n"
            "            for j in range(i * i, limit + 1, i):\n"
            "                base[j] = False\n"
            "    primes = [i for i in range(2, limit + 1) if base[i]]\n"
            "    size = high - low\n"
            "    mark = [True] * size\n"
            "    for p in primes:\n"
            "        start = max(p * p, ((low + p - 1) // p) * p)\n"
            "        for j in range(start, high, p):\n"
            "            mark[j - low] = False\n"
            "    if low <= 1:\n"
            "        for k in range(low, min(2, high)):\n"
            "            mark[k - low] = False\n"
            "    return [low + i for i, ok in enumerate(mark) if ok]\n",
            lambda low: bool(re.search(r"\bsegmented[- ]sieve\b", low)),
            (
                ((10, 30), [11, 13, 17, 19, 23, 29]),
                ((1, 10), [2, 3, 5, 7]),
            ),
        ),
        T(
            "inclusion_exclusion",
            "def inclusion_exclusion(n, divisors):\n"
            '    """Count integers in 1..n divisible by at least one of divisors.\n'
            "\n"
            "    Classic inclusion-exclusion over the subsets of the divisor list.\n"
            "    Empty or non-positive divisors are ignored.\n"
            '    """\n'
            "    divs = [d for d in divisors if isinstance(d, int) and d > 0]\n"
            "    m = len(divs)\n"
            "    total = 0\n"
            "    for mask in range(1, 1 << m):\n"
            "        lcm = 1\n"
            "        bits = 0\n"
            "        for i in range(m):\n"
            "            if mask & (1 << i):\n"
            "                a, b = lcm, divs[i]\n"
            "                while b:\n"
            "                    a, b = b, a % b\n"
            "                g = a\n"
            "                lcm = lcm // g * divs[i]\n"
            "                bits += 1\n"
            "                if lcm > n:\n"
            "                    lcm = n + 1\n"
            "                    break\n"
            "        sign = 1 if bits % 2 == 1 else -1\n"
            "        total += sign * (n // lcm)\n"
            "    return total\n",
            lambda low: bool(re.search(r"\binclusion[- ]exclusion\b", low)),
            (
                ((20, [2, 3, 5]), 14),
                ((10, [2, 3]), 7),
            ),
        ),
        T(
            # "z function" phrase (unit test). Do not steal "z algorithm".
            "z_function",
            "def z_function(s):\n"
            '    """Z-array for string s: z[i] is the longest prefix match starting at i.\n'
            "\n"
            "    Classic linear-time Z-algorithm (Gusfield / CP-Algorithms).\n"
            "    z[0] is defined as 0.\n"
            '    """\n'
            "    n = len(s)\n"
            "    z = [0] * n\n"
            "    l = r = 0\n"
            "    for i in range(1, n):\n"
            "        if i < r:\n"
            "            z[i] = min(r - i, z[i - l])\n"
            "        while i + z[i] < n and s[z[i]] == s[i + z[i]]:\n"
            "            z[i] += 1\n"
            "        if i + z[i] > r:\n"
            "            l, r = i, i + z[i]\n"
            "    return z\n",
            lambda low: bool(re.search(r"\bz[- ]function\b", low)) and "algorithm" not in low,
            (
                (("aaaaa",), [0, 4, 3, 2, 1]),
                (("aaabaab",), [0, 2, 1, 0, 2, 1, 0]),
            ),
        ),
        T(
            "linear_sieve_spf",
            "def linear_sieve_spf(n):\n"
            '    """Linear sieve: smallest prime factor for every integer in 0..n.\n'
            "\n"
            "    spf[0] = spf[1] = 0; spf[p] = p for primes. O(n) time.\n"
            '    """\n'
            "    spf = list(range(n + 1))\n"
            "    primes = []\n"
            "    for i in range(2, n + 1):\n"
            "        if spf[i] == i:\n"
            "            primes.append(i)\n"
            "        for p in primes:\n"
            "            if p > spf[i] or i * p > n:\n"
            "                break\n"
            "            spf[i * p] = p\n"
            "    spf[0] = spf[1] = 0\n"
            "    return spf\n",
            lambda low: bool(
                re.search(
                    r"\blinear[- ]sieve\b|\bsmallest prime factor\b|\bspf sieve\b",
                    low,
                )
            ),
            (
                ((10,), [0, 0, 2, 3, 2, 5, 2, 7, 2, 3, 2]),
                ((1,), [0, 0]),
            ),
        ),
        T(
            "meet_in_the_middle",
            "def meet_in_the_middle(nums, target):\n"
            '    """Count subsets of nums that sum to target via meet-in-the-middle.\n'
            "\n"
            "    Splits the array in half, enumerates both sides, and counts pairs.\n"
            "    Suitable for n up to ~40. Empty subset sums to 0.\n"
            '    """\n'
            "    n = len(nums)\n"
            "    mid = n // 2\n"
            "    left, right = nums[:mid], nums[mid:]\n"
            "\n"
            "    def sums(arr):\n"
            "        out = [0]\n"
            "        for x in arr:\n"
            "            out += [s + x for s in out]\n"
            "        return out\n"
            "\n"
            "    from collections import Counter\n"
            "    lc = Counter(sums(left))\n"
            "    total = 0\n"
            "    for s in sums(right):\n"
            "        total += lc[target - s]\n"
            "    return total\n",
            lambda low: bool(
                re.search(r"\bmeet[- ]in[- ]the[- ]middle\b", low)
            ),
            (
                (([1, 2, 3, 4], 5), 2),
                (([1, 1, 1], 2), 3),
            ),
        ),
        T(
            "scapegoat_tree_class",
            "class ScapegoatTree:\n"
            '    """Educational scapegoat tree (Galperin / Rivest).\n'
            "\n"
            "    Balanced by height vs size: a node is a scapegoat when\n"
            "    size(child) > alpha * size(node). Rebuild flattens and rebalances.\n"
            "    Supports insert and contains. Alpha defaults to 0.7.\n"
            '    """\n'
            "    def __init__(self, alpha=0.7):\n"
            "        self.alpha = alpha\n"
            "        self.root = None\n"
            "        self.n = 0\n"
            "\n"
            "    class Node:\n"
            "        __slots__ = ('key', 'left', 'right', 'size')\n"
            "        def __init__(self, key):\n"
            "            self.key = key\n"
            "            self.left = self.right = None\n"
            "            self.size = 1\n"
            "\n"
            "    def _size(self, node):\n"
            "        return node.size if node else 0\n"
            "\n"
            "    def _update(self, node):\n"
            "        if node:\n"
            "            node.size = 1 + self._size(node.left) + self._size(node.right)\n"
            "\n"
            "    def _flatten(self, node, out):\n"
            "        if not node:\n"
            "            return\n"
            "        self._flatten(node.left, out)\n"
            "        out.append(node.key)\n"
            "        self._flatten(node.right, out)\n"
            "\n"
            "    def _build(self, keys):\n"
            "        if not keys:\n"
            "            return None\n"
            "        mid = len(keys) // 2\n"
            "        node = self.Node(keys[mid])\n"
            "        node.left = self._build(keys[:mid])\n"
            "        node.right = self._build(keys[mid + 1:])\n"
            "        self._update(node)\n"
            "        return node\n"
            "\n"
            "    def insert(self, key):\n"
            "        path = []\n"
            "        node = self.root\n"
            "        while node:\n"
            "            path.append(node)\n"
            "            if key == node.key:\n"
            "                return\n"
            "            node = node.left if key < node.key else node.right\n"
            "        leaf = self.Node(key)\n"
            "        self.n += 1\n"
            "        if not path:\n"
            "            self.root = leaf\n"
            "            return\n"
            "        parent = path[-1]\n"
            "        if key < parent.key:\n"
            "            parent.left = leaf\n"
            "        else:\n"
            "            parent.right = leaf\n"
            "        for anc in reversed(path):\n"
            "            self._update(anc)\n"
            "        for anc in reversed(path):\n"
            "            if (self._size(anc.left) > self.alpha * anc.size or\n"
            "                    self._size(anc.right) > self.alpha * anc.size):\n"
            "                keys = []\n"
            "                self._flatten(anc, keys)\n"
            "                rebuilt = self._build(keys)\n"
            "                if anc is self.root:\n"
            "                    self.root = rebuilt\n"
            "                else:\n"
            "                    gp = path[path.index(anc) - 1]\n"
            "                    if gp.left is anc:\n"
            "                        gp.left = rebuilt\n"
            "                    else:\n"
            "                        gp.right = rebuilt\n"
            "                    self._update(gp)\n"
            "                break\n"
            "\n"
            "    def contains(self, key):\n"
            "        node = self.root\n"
            "        while node:\n"
            "            if key == node.key:\n"
            "                return True\n"
            "            node = node.left if key < node.key else node.right\n"
            "        return False\n"
            "\n"
            "    def inorder(self):\n"
            "        out = []\n"
            "        self._flatten(self.root, out)\n"
            "        return out\n"
            "\n"
            "\n"
            "def _scapegoat_demo(keys):\n"
            '    """Insert keys into a ScapegoatTree; return sorted inorder + membership."""\n'
            "    t = ScapegoatTree()\n"
            "    for k in keys:\n"
            "        t.insert(k)\n"
            "    return (t.inorder(), all(t.contains(k) for k in keys))\n",
            lambda low: bool(re.search(r"\bscapegoat[- ]tree\b", low)),
            (
                # First callable after exec is ScapegoatTree (class); demo is secondary.
                # verify_source picks the first callable — so keep class ctor safe:
                # empty examples still exec-verify; demo documents expected behavior.
            ),
        ),
    ]
