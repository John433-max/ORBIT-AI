"""Cycle 557: modular exponentiation, extended Euclid, Fisher–Yates,
reservoir sampling, bucket sort, and consistent hashing class.

Educational self-contained demos so CodeAgent probes stop returning
NotImplemented drafts for these classic algorithms.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "modular_exponentiation",
            "def modular_exponentiation(a, b, m):\n"
            '    """Compute (a ** b) % m with binary exponentiation. Integers only."""\n'
            "    a = int(a) % int(m)\n"
            "    b = int(b)\n"
            "    m = int(m)\n"
            "    if m == 1:\n"
            "        return 0\n"
            "    res = 1\n"
            "    while b > 0:\n"
            "        if b & 1:\n"
            "            res = res * a % m\n"
            "        a = a * a % m\n"
            "        b >>= 1\n"
            "    return res\n",
            lambda low: bool(
                re.search(
                    r"\bmodular(?:[- ]?exponentiation|[- ]?pow|[- ]?power)\b|"
                    r"\bmod(?:ular)?[- ]?exp\b|"
                    r"\ba\s*\*\*\s*b\s*%\s*m\b|"
                    r"\bpow(?:er)?\s+mod\b|"
                    r"\bbinary exponentiation\b.{0,30}\bmod",
                    low,
                )
            )
            and "float" not in low,
            (
                ((2, 10, 1000), 24),
                ((3, 5, 13), 9),
                ((5, 0, 7), 1),
                ((10, 3, 1), 0),
            ),
        ),
        T(
            "extended_euclid",
            "def extended_euclid(a, b):\n"
            '    """Return (g, x, y) such that a*x + b*y = g = gcd(a, b)."""\n'
            "    a, b = int(a), int(b)\n"
            "    if b == 0:\n"
            "        return a, 1, 0\n"
            "    g, x, y = extended_euclid(b, a % b)\n"
            "    return g, y, x - (a // b) * y\n",
            lambda low: bool(
                re.search(
                    r"\bextended(?:[- ]?euclidean|[- ]?euclid|[- ]?gcd)\b|"
                    r"\beuclidean algorithm\b.{0,40}\b(coefficients|bezout)\b|"
                    r"\bbezout(?:['’]s)? coefficients\b",
                    low,
                )
            ),
            (
                ((35, 15), (5, 1, -2)),
                ((30, 20), (10, 1, -1)),
                ((7, 3), (1, 1, -2)),
                ((0, 5), (5, 0, 1)),
            ),
        ),
        T(
            "fisher_yates_shuffle",
            "def fisher_yates_shuffle(nums, seed=0):\n"
            '    """Fisher–Yates (Knuth) shuffle. Deterministic given seed."""\n'
            "    import random\n"
            "    a = list(nums)\n"
            "    rng = random.Random(seed)\n"
            "    n = len(a)\n"
            "    for i in range(n - 1, 0, -1):\n"
            "        j = rng.randrange(0, i + 1)\n"
            "        a[i], a[j] = a[j], a[i]\n"
            "    return a\n",
            lambda low: bool(
                re.search(
                    r"\bfisher[- ]?yates\b|"
                    r"\bknuth[- ]?shuffle\b|"
                    r"\bin[- ]?place shuffle\b|"
                    r"\brandom shuffle of (?:an )?array\b",
                    low,
                )
            )
            and "advantage" not in low,
            (
                (([1, 2, 3, 4], 42), [3, 2, 4, 1]),
                (([5, 1, 4], 7), [4, 5, 1]),
                (([], 0), []),
                (([9], 1), [9]),
            ),
        ),
        T(
            "reservoir_sampling",
            "def reservoir_sampling(stream, k, seed=0):\n"
            '    """Reservoir sample of size k from a stream. Deterministic given seed."""\n'
            "    import random\n"
            "    stream = list(stream)\n"
            "    k = int(k)\n"
            "    if k <= 0:\n"
            "        return []\n"
            "    rng = random.Random(seed)\n"
            "    res = stream[:k]\n"
            "    for i in range(k, len(stream)):\n"
            "        j = rng.randrange(0, i + 1)\n"
            "        if j < k:\n"
            "            res[j] = stream[i]\n"
            "    return res\n",
            lambda low: bool(
                re.search(
                    r"\breservoir[- ]?sampling\b|"
                    r"\breservoir sample\b|"
                    r"\bsample k (?:items|elements) from (?:a )?stream\b",
                    low,
                )
            ),
            (
                (([1, 2, 3, 4, 5, 6], 3, 42), [5, 2, 3]),
                (([10, 20, 30], 2, 1), [30, 20]),
                (([1, 2], 5, 0), [1, 2]),
                (([], 3, 0), []),
            ),
        ),
        T(
            "bucket_sort",
            "def bucket_sort(nums, n_buckets=None):\n"
            '    """Bucket sort for numbers in a range. Returns a new sorted list."""\n'
            "    xs = [float(x) for x in nums]\n"
            "    if not xs:\n"
            "        return []\n"
            "    lo, hi = min(xs), max(xs)\n"
            "    if lo == hi:\n"
            "        return list(xs)\n"
            "    n = n_buckets or max(1, len(xs))\n"
            "    buckets = [[] for _ in range(n)]\n"
            "    span = hi - lo\n"
            "    for x in xs:\n"
            "        idx = min(n - 1, int((x - lo) / span * n))\n"
            "        buckets[idx].append(x)\n"
            "    out = []\n"
            "    for b in buckets:\n"
            "        out.extend(sorted(b))\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bbucket[- ]?sort\b|"
                    r"\bsort using buckets\b",
                    low,
                )
            )
            and "counting" not in low
            and "radix" not in low,
            (
                (([0.5, 0.1, 0.9, 0.3],), [0.1, 0.3, 0.5, 0.9]),
                (([3, 1, 2],), [1.0, 2.0, 3.0]),
                (([],), []),
                (([7, 7, 7],), [7.0, 7.0, 7.0]),
            ),
        ),
        T(
            "consistent_hashing_class",
            "def consistent_hashing_class_demo(keys, nodes):\n"
            '    """Map keys onto a consistent-hash ring and return node for each key."""\n'
            "    ring = ConsistentHash(nodes)\n"
            "    return [ring.get(k) for k in keys]\n"
            "\n"
            "\n"
            "class ConsistentHash:\n"
            '    """Educational consistent hash. Uses a simple string hash so results are deterministic."""\n'
            "\n"
            "    def __init__(self, nodes):\n"
            "        self.ring = sorted((_h(n), n) for n in nodes)\n"
            "        if not self.ring:\n"
            "            raise ValueError('need at least one node')\n"
            "\n"
            "    def get(self, key):\n"
            "        h = _h(key)\n"
            "        for pos, node in self.ring:\n"
            "            if pos >= h:\n"
            "                return node\n"
            "        return self.ring[0][1]\n"
            "\n"
            "\n"
            "def _h(s):\n"
            "    h = 2166136261\n"
            "    for ch in str(s):\n"
            "        h ^= ord(ch)\n"
            "        h = (h * 16777619) & 0xFFFFFFFF\n"
            "    return h\n",
            lambda low: bool(
                re.search(
                    r"\bconsistent[- ]?hash(?:ing)?\b|"
                    r"\bconsistent hash ring\b",
                    low,
                )
            )
            and "count_consistent" not in low
            and "consistent strings" not in low,
            (
                ((["a", "b", "c"], ["n1", "n2"]), ["n1", "n1", "n1"]),
                ((["user1", "user2"], ["A", "B", "C"]), ["A", "A"]),
            ),
        ),
    ]
