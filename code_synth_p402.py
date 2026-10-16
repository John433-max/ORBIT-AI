"""Cycle 402: skip_list, weighted_choice, and bloom_filter widen for phrase gaps.

Educational self-checking templates. Skip list is a classic probabilistic
structure; weighted_choice covers alias-free weighted sampling; bloom matcher
gaps closed via pack matcher (loader keeps first unique name, so this pack
is numbered high enough to win when names differ, and _widen handles class).
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "skip_list",
            '''def skip_list_ops(ops):
    """Educational skip list (probabilistic ordered set).

    ops: list of (\"insert\"|\"search\"|\"delete\", key).
    Returns list of results for search ops (True/False) and final sorted keys.
    Max level 8; p=0.5 via deterministic hash for reproducibility in tests.
    """
    MAX_LEVEL = 8

    class Node:
        __slots__ = ("key", "forward")
        def __init__(self, key, level):
            self.key = key
            self.forward = [None] * (level + 1)

    class SkipList:
        def __init__(self):
            self.header = Node(None, MAX_LEVEL)
            self.level = 0
            self._size = 0

        def _random_level(self, key):
            # Deterministic "random" from key for self-check stability.
            h = abs(hash((key, "skip"))) % (2 ** 16)
            lvl = 0
            while lvl < MAX_LEVEL and (h & 1):
                lvl += 1
                h >>= 1
            return lvl

        def insert(self, key):
            update = [None] * (MAX_LEVEL + 1)
            cur = self.header
            for i in range(self.level, -1, -1):
                while cur.forward[i] and cur.forward[i].key < key:
                    cur = cur.forward[i]
                update[i] = cur
            nxt = cur.forward[0]
            if nxt and nxt.key == key:
                return  # already present
            lvl = self._random_level(key)
            if lvl > self.level:
                for i in range(self.level + 1, lvl + 1):
                    update[i] = self.header
                self.level = lvl
            node = Node(key, lvl)
            for i in range(lvl + 1):
                node.forward[i] = update[i].forward[i]
                update[i].forward[i] = node
            self._size += 1

        def search(self, key):
            cur = self.header
            for i in range(self.level, -1, -1):
                while cur.forward[i] and cur.forward[i].key < key:
                    cur = cur.forward[i]
            cur = cur.forward[0]
            return cur is not None and cur.key == key

        def delete(self, key):
            update = [None] * (MAX_LEVEL + 1)
            cur = self.header
            for i in range(self.level, -1, -1):
                while cur.forward[i] and cur.forward[i].key < key:
                    cur = cur.forward[i]
                update[i] = cur
            tgt = cur.forward[0]
            if not tgt or tgt.key != key:
                return False
            for i in range(self.level + 1):
                if update[i].forward[i] is not tgt:
                    break
                update[i].forward[i] = tgt.forward[i]
            while self.level > 0 and self.header.forward[self.level] is None:
                self.level -= 1
            self._size -= 1
            return True

        def keys(self):
            out = []
            cur = self.header.forward[0]
            while cur:
                out.append(cur.key)
                cur = cur.forward[0]
            return out

    sl = SkipList()
    results = []
    for op in ops:
        kind, key = op[0], op[1]
        if kind == "insert":
            sl.insert(key)
        elif kind == "delete":
            results.append(sl.delete(key))
        elif kind == "search":
            results.append(sl.search(key))
    return results, sl.keys()
''',
            lambda low: bool(
                re.search(
                    r"\bskip[-_ ]?list\b|"
                    r"\bskiplist\b|"
                    r"\bimplement(?: a)? skip list\b|"
                    r"\bwrite(?: a)?(?: python)? skip list\b",
                    low,
                )
            )
            and "linked" not in low,
            (
                (
                    (
                        [
                            ("insert", 3),
                            ("insert", 1),
                            ("insert", 2),
                            ("search", 2),
                            ("search", 9),
                            ("delete", 1),
                            ("search", 1),
                        ],
                    ),
                    ([True, False, True, False], [2, 3]),
                ),
            ),
        ),
        T(
            "weighted_choice",
            '''def weighted_choice(items, weights, n=1, seed=0):
    """Sample n items with replacement proportional to weights (educational).

    Uses cumulative weights + binary search (no external RNG libs).
    Deterministic via a simple LCG seeded by ``seed``.
    Returns a list of length n.
    """
    if not items or not weights or len(items) != len(weights):
        raise ValueError("items and weights must be non-empty and same length")
    if any(w < 0 for w in weights):
        raise ValueError("weights must be non-negative")
    total = float(sum(weights))
    if total <= 0:
        raise ValueError("sum of weights must be positive")
    cum = []
    s = 0.0
    for w in weights:
        s += float(w)
        cum.append(s)

    # LCG (Numerical Recipes)
    state = int(seed) & 0xFFFFFFFF

    def _rand():
        nonlocal state
        state = (1664525 * state + 1013904223) & 0xFFFFFFFF
        return state / 4294967296.0

    out = []
    for _ in range(int(n)):
        r = _rand() * total
        # binary search first cum >= r
        lo, hi = 0, len(cum) - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if cum[mid] < r:
                lo = mid + 1
            else:
                hi = mid
        out.append(items[lo])
    return out


def weighted_random_sample(items, weights, n=1, seed=0):
    """Alias for weighted_choice (educational)."""
    return weighted_choice(items, weights, n=n, seed=seed)
''',
            lambda low: bool(
                re.search(
                    r"\bweighted[_ ](?:choice|random|sample|sampling)\b|"
                    r"\bsample(?:s|ing)?\b.{0,24}\bweight",
                    low,
                )
            )
            and "reservoir" not in low
            and "without replacement" not in low,
            (
                ((["a", "b", "c"], [1, 0, 0], 3, 1), ["a", "a", "a"]),
                ((["x", "y"], [0, 5], 2, 0), ["y", "y"]),
            ),
        ),
        T(
            "bloom_filter",
            '''def bloom_filter_ops(capacity, error_rate, ops):
    """Educational Bloom filter (bit array + multiple hashes).

    ops: list of (\"add\"|\"might_contain\", item).
    Returns list of bool results for might_contain queries.
    Uses double hashing over a fixed bit array; educational only.
    """
    import math

    capacity = max(1, int(capacity))
    error_rate = float(error_rate)
    if not (0 < error_rate < 1):
        error_rate = 0.01
    # m bits, k hashes
    m = max(8, int(-capacity * math.log(error_rate) / (math.log(2) ** 2)))
    k = max(1, int((m / capacity) * math.log(2)))
    bits = [0] * m

    def _hashes(item):
        h1 = abs(hash((item, "bf1"))) % m
        h2 = abs(hash((item, "bf2"))) % m or 1
        for i in range(k):
            yield (h1 + i * h2) % m

    results = []
    for op in ops:
        kind, item = op[0], op[1]
        if kind == "add":
            for idx in _hashes(item):
                bits[idx] = 1
        elif kind in ("might_contain", "contains", "query"):
            results.append(all(bits[idx] for idx in _hashes(item)))
    return results
''',
            lambda low: bool(
                re.search(
                    r"\bbloom[-_ ]?filter\b|"
                    r"\bbloomfilter\b",
                    low,
                )
            )
            and "cuckoo" not in low
            and "counting" not in low
            and "class" not in low,
            (
                (
                    (
                        50,
                        0.01,
                        [
                            ("add", "apple"),
                            ("add", "banana"),
                            ("might_contain", "apple"),
                            ("might_contain", "carrot"),
                        ],
                    ),
                    [True, False],
                ),
            ),
        ),
    ]
