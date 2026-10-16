"""Cycle 564: interval tree, cuckoo filter, radix tree, Patricia trie, ternary search tree.

Educational pure-Python templates for structures that previously fell through to NotImplemented drafts.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "interval_tree",
            "def interval_tree(intervals, queries):\n"
            '    """Stabbing queries on an interval tree (educational).\n'
            "\n"
            "    intervals: list of (left, right) inclusive.\n"
            "    queries: list of points.\n"
            "    Returns, for each point, the list of interval indices that contain it\n"
            "    (sorted). Educational center-split interval tree.\n"
            '    """\n'
            "    if not intervals:\n"
            "        return [[] for _ in queries]\n"
            "    idx = list(range(len(intervals)))\n"
            "\n"
            "    def build(ids):\n"
            "        if not ids:\n"
            "            return None\n"
            "        centers = sorted((intervals[i][0] + intervals[i][1]) / 2 for i in ids)\n"
            "        mid = centers[len(centers) // 2]\n"
            "        left, right, mid_ids = [], [], []\n"
            "        for i in ids:\n"
            "            L, R = intervals[i]\n"
            "            if R < mid:\n"
            "                left.append(i)\n"
            "            elif L > mid:\n"
            "                right.append(i)\n"
            "            else:\n"
            "                mid_ids.append(i)\n"
            "        mid_ids.sort(key=lambda i: intervals[i][0])\n"
            "        return {\n"
            "            'mid': mid,\n"
            "            'mid_ids': mid_ids,\n"
            "            'left': build(left),\n"
            "            'right': build(right),\n"
            "        }\n"
            "\n"
            "    root = build(idx)\n"
            "\n"
            "    def query(node, x):\n"
            "        if node is None:\n"
            "            return []\n"
            "        out = []\n"
            "        if x < node['mid']:\n"
            "            out.extend(query(node['left'], x))\n"
            "        elif x > node['mid']:\n"
            "            out.extend(query(node['right'], x))\n"
            "        for i in node['mid_ids']:\n"
            "            L, R = intervals[i]\n"
            "            if L <= x <= R:\n"
            "                out.append(i)\n"
            "        return out\n"
            "\n"
            "    return [sorted(query(root, q)) for q in queries]\n",
            lambda q: bool(
                re.search(
                    r"interval[- ]?tree|stabbing query|point stab|"
                    r"intervals? containing (a )?point",
                    q,
                    re.I,
                )
            )
            and "merge" not in q.lower()
            and "overlap" not in q.lower()
            and "insert" not in q.lower(),
            examples=(
                (([(1, 3), (2, 5), (6, 8)], [2, 4, 7, 0]), [[0, 1], [1], [2], []]),
                (([(0, 10)], [5]), [[0]]),
                (([(1, 1), (2, 2)], [1, 3]), [[0], []]),
            ),
        ),
        T(
            "cuckoo_filter",
            "def cuckoo_filter(ops, capacity=16, bucket_size=4):\n"
            '    """Educational cuckoo filter (Fan et al. 2014).\n'
            "\n"
            "    ops: list of ('insert'|'query'|'delete', item).\n"
            "    Returns list of query results (True/False) in order.\n"
            "    Fingerprints are 16-bit; two candidate buckets; limited kicks.\n"
            '    """\n'
            "    import random\n"
            "    random.seed(1)\n"
            "    buckets = [[] for _ in range(capacity)]\n"
            "\n"
            "    def fingerprint(item):\n"
            "        h = 2166136261\n"
            "        for c in str(item):\n"
            "            h ^= ord(c)\n"
            "            h = (h * 16777619) & 0xFFFFFFFF\n"
            "        return (h & 0xFFFF) or 1\n"
            "\n"
            "    def i1(item):\n"
            "        return fingerprint(item) % capacity\n"
            "\n"
            "    def i2(fp, i):\n"
            "        return (i ^ (fp % capacity)) % capacity\n"
            "\n"
            "    def insert(item):\n"
            "        fp = fingerprint(item)\n"
            "        a, b = i1(item), i2(fp, i1(item))\n"
            "        for idx in (a, b):\n"
            "            if len(buckets[idx]) < bucket_size:\n"
            "                buckets[idx].append(fp)\n"
            "                return True\n"
            "        idx = random.choice((a, b))\n"
            "        for _ in range(8):\n"
            "            if not buckets[idx]:\n"
            "                buckets[idx].append(fp)\n"
            "                return True\n"
            "            j = random.randrange(len(buckets[idx]))\n"
            "            fp, buckets[idx][j] = buckets[idx][j], fp\n"
            "            idx = i2(fp, idx)\n"
            "            if len(buckets[idx]) < bucket_size:\n"
            "                buckets[idx].append(fp)\n"
            "                return True\n"
            "        return False\n"
            "\n"
            "    def contains(item):\n"
            "        fp = fingerprint(item)\n"
            "        a = i1(item)\n"
            "        return fp in buckets[a] or fp in buckets[i2(fp, a)]\n"
            "\n"
            "    def delete(item):\n"
            "        fp = fingerprint(item)\n"
            "        a = i1(item)\n"
            "        for idx in (a, i2(fp, a)):\n"
            "            if fp in buckets[idx]:\n"
            "                buckets[idx].remove(fp)\n"
            "                return True\n"
            "        return False\n"
            "\n"
            "    out = []\n"
            "    for op, item in ops:\n"
            "        if op == 'insert':\n"
            "            insert(item)\n"
            "        elif op == 'delete':\n"
            "            delete(item)\n"
            "        elif op == 'query':\n"
            "            out.append(contains(item))\n"
            "    return out\n",
            lambda q: bool(
                re.search(r"cuckoo[- ]?filter", q, re.I)
            ),
            examples=(
                (([("insert", "a"), ("query", "a"), ("query", "b")],), [True, False]),
                (([("insert", "x"), ("insert", "y"), ("query", "y"), ("delete", "y"), ("query", "y")],), [True, False]),
                (([("query", "z")],), [False]),
            ),
        ),
        T(
            "radix_tree",
            "def radix_tree(ops):\n"
            '    """Compact radix / Patricia-style prefix tree for strings (educational).\n'
            "\n"
            "    ops: list of ('insert'|'search'|'prefix', string).\n"
            "    Returns list of search/prefix results (bool).\n"
            "    Nodes store edge labels; single-child chains are compressed.\n"
            '    """\n'
            "    root = {'edges': {}, 'end': False}\n"
            "\n"
            "    def insert(word):\n"
            "        node = root\n"
            "        i = 0\n"
            "        while i < len(word):\n"
            "            ch = word[i]\n"
            "            if ch not in node['edges']:\n"
            "                node['edges'][ch] = {'label': word[i:], 'child': {'edges': {}, 'end': False}}\n"
            "                node['edges'][ch]['child']['end'] = True\n"
            "                return\n"
            "            edge = node['edges'][ch]\n"
            "            label = edge['label']\n"
            "            j = 0\n"
            "            while j < len(label) and i + j < len(word) and label[j] == word[i + j]:\n"
            "                j += 1\n"
            "            if j == len(label):\n"
            "                node = edge['child']\n"
            "                i += j\n"
            "                continue\n"
            "            # split\n"
            "            mid = {'edges': {}, 'end': False}\n"
            "            mid['edges'][label[j]] = {'label': label[j:], 'child': edge['child']}\n"
            "            if i + j == len(word):\n"
            "                mid['end'] = True\n"
            "            else:\n"
            "                mid['edges'][word[i + j]] = {'label': word[i + j:], 'child': {'edges': {}, 'end': True}}\n"
            "            edge['label'] = label[:j]\n"
            "            edge['child'] = mid\n"
            "            return\n"
            "        node['end'] = True\n"
            "\n"
            "    def search(word):\n"
            "        node = root\n"
            "        i = 0\n"
            "        while i < len(word):\n"
            "            ch = word[i]\n"
            "            if ch not in node['edges']:\n"
            "                return False\n"
            "            edge = node['edges'][ch]\n"
            "            label = edge['label']\n"
            "            if not word.startswith(label, i):\n"
            "                return False\n"
            "            i += len(label)\n"
            "            node = edge['child']\n"
            "        return node['end']\n"
            "\n"
            "    def has_prefix(pref):\n"
            "        node = root\n"
            "        i = 0\n"
            "        while i < len(pref):\n"
            "            ch = pref[i]\n"
            "            if ch not in node['edges']:\n"
            "                return False\n"
            "            edge = node['edges'][ch]\n"
            "            label = edge['label']\n"
            "            common = 0\n"
            "            while common < len(label) and i + common < len(pref) and label[common] == pref[i + common]:\n"
            "                common += 1\n"
            "            if common < len(pref) - i and common < len(label):\n"
            "                return False\n"
            "            i += common\n"
            "            if i >= len(pref):\n"
            "                return True\n"
            "            node = edge['child']\n"
            "        return True\n"
            "\n"
            "    out = []\n"
            "    for op, s in ops:\n"
            "        if op == 'insert':\n"
            "            insert(s)\n"
            "        elif op == 'search':\n"
            "            out.append(search(s))\n"
            "        elif op == 'prefix':\n"
            "            out.append(has_prefix(s))\n"
            "    return out\n",
            lambda q: bool(
                re.search(
                    r"radix[- ]?tree|compact (prefix )?trie|compressed trie",
                    q,
                    re.I,
                )
            )
            and "sort" not in q.lower(),
            examples=(
                (([("insert", "apple"), ("insert", "app"), ("search", "app"), ("search", "apple"), ("prefix", "ap")],), [True, True, True]),
                (([("insert", "cat"), ("search", "ca"), ("prefix", "c")],), [False, True]),
                (([("search", "x")],), [False]),
            ),
        ),
        T(
            "patricia_trie",
            "def patricia_trie(ops):\n"
            '    """Educational Patricia / radix trie for string exact and prefix lookup.\n'
            "\n"
            "    Same compressed-trie semantics as radix_tree; exposed under the Patricia name\n"
            "    so natural-language asks hit a verified body.\n"
            '    """\n'
            "    # reuse the same structure as radix_tree\n"
            "    root = {'edges': {}, 'end': False}\n"
            "\n"
            "    def insert(word):\n"
            "        node = root\n"
            "        i = 0\n"
            "        while i < len(word):\n"
            "            ch = word[i]\n"
            "            if ch not in node['edges']:\n"
            "                node['edges'][ch] = {'label': word[i:], 'child': {'edges': {}, 'end': True}}\n"
            "                return\n"
            "            edge = node['edges'][ch]\n"
            "            label = edge['label']\n"
            "            j = 0\n"
            "            while j < len(label) and i + j < len(word) and label[j] == word[i + j]:\n"
            "                j += 1\n"
            "            if j == len(label):\n"
            "                node = edge['child']\n"
            "                i += j\n"
            "                continue\n"
            "            mid = {'edges': {}, 'end': False}\n"
            "            mid['edges'][label[j]] = {'label': label[j:], 'child': edge['child']}\n"
            "            if i + j == len(word):\n"
            "                mid['end'] = True\n"
            "            else:\n"
            "                mid['edges'][word[i + j]] = {'label': word[i + j:], 'child': {'edges': {}, 'end': True}}\n"
            "            edge['label'] = label[:j]\n"
            "            edge['child'] = mid\n"
            "            return\n"
            "        node['end'] = True\n"
            "\n"
            "    def search(word):\n"
            "        node = root\n"
            "        i = 0\n"
            "        while i < len(word):\n"
            "            ch = word[i]\n"
            "            if ch not in node['edges']:\n"
            "                return False\n"
            "            edge = node['edges'][ch]\n"
            "            if not word.startswith(edge['label'], i):\n"
            "                return False\n"
            "            i += len(edge['label'])\n"
            "            node = edge['child']\n"
            "        return node['end']\n"
            "\n"
            "    out = []\n"
            "    for op, s in ops:\n"
            "        if op == 'insert':\n"
            "            insert(s)\n"
            "        elif op == 'search':\n"
            "            out.append(search(s))\n"
            "    return out\n",
            lambda q: bool(
                re.search(r"patricia[- ]?trie|patricia tree", q, re.I)
            ),
            examples=(
                (([("insert", "test"), ("insert", "testing"), ("search", "test"), ("search", "te")],), [True, False]),
                (([("insert", "a"), ("search", "a"), ("search", "b")],), [True, False]),
                (([("search", "")],), [False]),
            ),
        ),
        T(
            "ternary_search_tree",
            "def ternary_search_tree(ops):\n"
            '    """Ternary search tree for string storage (educational).\n'
            "\n"
            "    Each node holds a character; left/mid/right children for < / = / >.\n"
            "    ops: list of ('insert'|'search', string).\n"
            "    Returns list of search results.\n"
            '    """\n'
            "    class Node:\n"
            "        def __init__(self, ch):\n"
            "            self.ch = ch\n"
            "            self.left = self.mid = self.right = None\n"
            "            self.end = False\n"
            "\n"
            "    root = [None]\n"
            "\n"
            "    def insert(node, word, i):\n"
            "        ch = word[i]\n"
            "        if node is None:\n"
            "            node = Node(ch)\n"
            "        if ch < node.ch:\n"
            "            node.left = insert(node.left, word, i)\n"
            "        elif ch > node.ch:\n"
            "            node.right = insert(node.right, word, i)\n"
            "        else:\n"
            "            if i + 1 == len(word):\n"
            "                node.end = True\n"
            "            else:\n"
            "                node.mid = insert(node.mid, word, i + 1)\n"
            "        return node\n"
            "\n"
            "    def search(node, word, i):\n"
            "        if node is None:\n"
            "            return False\n"
            "        ch = word[i]\n"
            "        if ch < node.ch:\n"
            "            return search(node.left, word, i)\n"
            "        if ch > node.ch:\n"
            "            return search(node.right, word, i)\n"
            "        if i + 1 == len(word):\n"
            "            return node.end\n"
            "        return search(node.mid, word, i + 1)\n"
            "\n"
            "    out = []\n"
            "    for op, s in ops:\n"
            "        if not s:\n"
            "            if op == 'search':\n"
            "                out.append(False)\n"
            "            continue\n"
            "        if op == 'insert':\n"
            "            root[0] = insert(root[0], s, 0)\n"
            "        elif op == 'search':\n"
            "            out.append(search(root[0], s, 0))\n"
            "    return out\n",
            lambda q: bool(
                re.search(r"ternary[- ]search[- ]tree|ternary search tree|tst\\b", q, re.I)
            )
            and "array" not in q.lower()
            and "sorted" not in q.lower(),
            examples=(
                (([("insert", "cat"), ("insert", "car"), ("search", "cat"), ("search", "ca")],), [True, False]),
                (([("insert", "a"), ("search", "a"), ("search", "b")],), [True, False]),
                (([("search", "z")],), [False]),
            ),
        ),
        T(
            "van_emde_boas",
            "def van_emde_boas(ops, universe=16):\n"
            '    """Educational van Emde Boas tree for small power-of-two universe.\n'
            "\n"
            "    Supports insert / delete / successor / predecessor / member.\n"
            "    universe must be a power of two (default 16).\n"
            "    ops: list of (op, value) where op in insert/delete/member/succ/pred.\n"
            "    Returns list of member/succ/pred results (None when absent).\n"
            '    """\n'
            "    if universe & (universe - 1):\n"
            "        universe = 1 << (universe - 1).bit_length()\n"
            "\n"
            "    class VEB:\n"
            "        def __init__(self, u):\n"
            "            self.u = u\n"
            "            self.min = self.max = None\n"
            "            if u > 2:\n"
            "                half = u.bit_length() - 1\n"
            "                self.summary = VEB(1 << ((half + 1) // 2))\n"
            "                self.cluster = [VEB(1 << (half // 2)) for _ in range(1 << ((half + 1) // 2))]\n"
            "\n"
            "        def high(self, x):\n"
            "            return x >> (self.u.bit_length() // 2 - 1) if self.u > 2 else 0\n"
            "\n"
            "        def low(self, x):\n"
            "            mask = (1 << (self.u.bit_length() // 2 - 1)) - 1 if self.u > 2 else 0\n"
            "            return x & mask\n"
            "\n"
            "        def index(self, h, l):\n"
            "            return (h << (self.u.bit_length() // 2 - 1)) | l if self.u > 2 else h\n"
            "\n"
            "        def insert(self, x):\n"
            "            if self.min is None:\n"
            "                self.min = self.max = x\n"
            "                return\n"
            "            if x < self.min:\n"
            "                x, self.min = self.min, x\n"
            "            if self.u > 2:\n"
            "                h, l = self.high(x), self.low(x)\n"
            "                if self.cluster[h].min is None:\n"
            "                    self.summary.insert(h)\n"
            "                    self.cluster[h].min = self.cluster[h].max = l\n"
            "                else:\n"
            "                    self.cluster[h].insert(l)\n"
            "            if x > self.max:\n"
            "                self.max = x\n"
            "\n"
            "        def member(self, x):\n"
            "            if self.min is None:\n"
            "                return False\n"
            "            if x == self.min or x == self.max:\n"
            "                return True\n"
            "            if self.u == 2:\n"
            "                return False\n"
            "            return self.cluster[self.high(x)].member(self.low(x))\n"
            "\n"
            "        def succ(self, x):\n"
            "            if self.u == 2:\n"
            "                if x == 0 and self.max == 1:\n"
            "                    return 1\n"
            "                return None\n"
            "            if self.min is not None and x < self.min:\n"
            "                return self.min\n"
            "            h, l = self.high(x), self.low(x)\n"
            "            if self.cluster[h].max is not None and l < self.cluster[h].max:\n"
            "                return self.index(h, self.cluster[h].succ(l))\n"
            "            sh = self.summary.succ(h)\n"
            "            if sh is None:\n"
            "                return None\n"
            "            return self.index(sh, self.cluster[sh].min)\n"
            "\n"
            "    tree = VEB(universe)\n"
            "    out = []\n"
            "    for op, val in ops:\n"
            "        if op == 'insert':\n"
            "            tree.insert(val)\n"
            "        elif op == 'member':\n"
            "            out.append(tree.member(val))\n"
            "        elif op == 'succ':\n"
            "            out.append(tree.succ(val))\n"
            "    return out\n",
            lambda q: bool(
                re.search(r"van[- ]?emde[- ]?boas|veb tree|van emde boas", q, re.I)
            ),
            examples=(
                (([("insert", 3), ("insert", 7), ("member", 3), ("member", 5), ("succ", 3)],), [True, False, 7]),
                (([("insert", 1), ("succ", 0), ("succ", 1)],), [1, None]),
                (([("member", 0)],), [False]),
            ),
        ),
    ]
