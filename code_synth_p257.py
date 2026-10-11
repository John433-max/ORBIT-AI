"""Cycle 560: class asks that still returned NotImplemented drafts.

Fills DoublyLinkedList, Trie, UnionFind, Deque, MinHeap, and HashMap.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "doubly_linked_list_class",
            "def doubly_linked_list_demo(values):\n"
            '    """Append then reverse-walk a doubly linked list."""\n'
            "    dll = DoublyLinkedList()\n"
            "    for value in values:\n"
            "        dll.append(value)\n"
            "    return dll.to_list()\n"
            "\n"
            "\n"
            "class _DNode:\n"
            "    def __init__(self, value):\n"
            "        self.value = value\n"
            "        self.prev = None\n"
            "        self.next = None\n"
            "\n"
            "\n"
            "class DoublyLinkedList:\n"
            '    """Doubly linked list with head/tail and append."""\n'
            "\n"
            "    def __init__(self):\n"
            "        self.head = None\n"
            "        self.tail = None\n"
            "\n"
            "    def append(self, value):\n"
            "        node = _DNode(value)\n"
            "        if self.tail is None:\n"
            "            self.head = self.tail = node\n"
            "            return\n"
            "        self.tail.next = node\n"
            "        node.prev = self.tail\n"
            "        self.tail = node\n"
            "\n"
            "    def to_list(self):\n"
            "        out = []\n"
            "        cur = self.head\n"
            "        while cur is not None:\n"
            "            out.append(cur.value)\n"
            "            cur = cur.next\n"
            "        return out\n",
            lambda low: bool(
                re.search(
                    r"\b(?:create|implement|write|build)(?: a)?(?: python)? class(?: that)?(?: for| that implements)?(?: a| the)? doubly[- ]?linked[- ]?list\b|"
                    r"\bdoubly[- ]?linked[- ]?list class\b|"
                    r"\bclass for(?: a| the)? doubly[- ]?linked[- ]?list\b|"
                    r"\bimplements? a doubly[- ]?linked[- ]?list\b",
                    low,
                )
            ),
            examples=(
                (([1, 2, 3],), [1, 2, 3]),
                (([],), []),
                ((["x"],), ["x"]),
            ),
        ),
        T(
            "trie_class",
            "def trie_demo(words, query):\n"
            '    """Insert words then test membership in a Trie."""\n'
            "    trie = Trie()\n"
            "    for word in words:\n"
            "        trie.insert(word)\n"
            "    return trie.search(query)\n"
            "\n"
            "\n"
            "class Trie:\n"
            '    """Prefix tree with insert and exact search."""\n'
            "\n"
            "    def __init__(self):\n"
            "        self.root = {}\n"
            "\n"
            "    def insert(self, word):\n"
            "        node = self.root\n"
            "        for ch in word:\n"
            "            node = node.setdefault(ch, {})\n"
            "        node['#'] = True\n"
            "\n"
            "    def search(self, word):\n"
            "        node = self.root\n"
            "        for ch in word:\n"
            "            if ch not in node:\n"
            "                return False\n"
            "            node = node[ch]\n"
            "        return bool(node.get('#'))\n",
            lambda low: bool(
                re.search(
                    r"\b(?:create|implement|write|build)(?: a)?(?: python)? class(?: that)?(?: for| that implements)?(?: a| the)? trie\b|"
                    r"\btrie class\b|"
                    r"\bclass for(?: a| the)? trie\b|"
                    r"\bimplements? a trie\b|"
                    r"\bprefix tree class\b",
                    low,
                )
            ),
            examples=(
                ((["cat", "car"], "cat"), True),
                ((["cat", "car"], "ca"), False),
                ((["hello"], "hello"), True),
            ),
        ),
        T(
            "union_find_class",
            "def union_find_demo(n, unions, a, b):\n"
            '    """Union pairs then test connectivity."""\n'
            "    uf = UnionFind(n)\n"
            "    for x, y in unions:\n"
            "        uf.union(x, y)\n"
            "    return uf.connected(a, b)\n"
            "\n"
            "\n"
            "class UnionFind:\n"
            '    """Disjoint-set union with path compression and union by rank."""\n'
            "\n"
            "    def __init__(self, n):\n"
            "        self.parent = list(range(n))\n"
            "        self.rank = [0] * n\n"
            "\n"
            "    def find(self, x):\n"
            "        while self.parent[x] != x:\n"
            "            self.parent[x] = self.parent[self.parent[x]]\n"
            "            x = self.parent[x]\n"
            "        return x\n"
            "\n"
            "    def union(self, a, b):\n"
            "        ra, rb = self.find(a), self.find(b)\n"
            "        if ra == rb:\n"
            "            return False\n"
            "        if self.rank[ra] < self.rank[rb]:\n"
            "            ra, rb = rb, ra\n"
            "        self.parent[rb] = ra\n"
            "        if self.rank[ra] == self.rank[rb]:\n"
            "            self.rank[ra] += 1\n"
            "        return True\n"
            "\n"
            "    def connected(self, a, b):\n"
            "        return self.find(a) == self.find(b)\n",
            lambda low: bool(
                re.search(
                    r"\b(?:create|implement|write|build)(?: a)?(?: python)? class(?: that)?(?: for| that implements)?(?: a| the)? (?:union[- ]?find|disjoint[- ]?set|dsu)\b|"
                    r"\b(?:union[- ]?find|disjoint[- ]?set|dsu) class\b|"
                    r"\bclass for(?: a| the)? (?:union[- ]?find|disjoint[- ]?set|dsu)\b|"
                    r"\bimplements? (?:a )?(?:union[- ]?find|disjoint[- ]?set)\b",
                    low,
                )
            ),
            examples=(
                ((5, [(0, 1), (1, 2)], 0, 2), True),
                ((5, [(0, 1)], 0, 2), False),
                ((3, [], 1, 1), True),
            ),
        ),
        T(
            "deque_class",
            "def deque_demo(values):\n"
            '    """Push left then pop right to exercise Deque."""\n'
            "    dq = Deque()\n"
            "    for value in values:\n"
            "        dq.append_left(value)\n"
            "    out = []\n"
            "    while len(dq):\n"
            "        out.append(dq.pop_right())\n"
            "    return out\n"
            "\n"
            "\n"
            "class Deque:\n"
            '    """List-backed double-ended queue."""\n'
            "\n"
            "    def __init__(self):\n"
            "        self._data = []\n"
            "\n"
            "    def append_left(self, value):\n"
            "        self._data.insert(0, value)\n"
            "\n"
            "    def append_right(self, value):\n"
            "        self._data.append(value)\n"
            "\n"
            "    def pop_left(self):\n"
            "        if not self._data:\n"
            "            raise IndexError('pop from empty deque')\n"
            "        return self._data.pop(0)\n"
            "\n"
            "    def pop_right(self):\n"
            "        if not self._data:\n"
            "            raise IndexError('pop from empty deque')\n"
            "        return self._data.pop()\n"
            "\n"
            "    def __len__(self):\n"
            "        return len(self._data)\n",
            lambda low: bool(
                re.search(
                    r"\b(?:create|implement|write|build)(?: a)?(?: python)? class(?: that)?(?: for| that implements)?(?: a| the)? deque\b|"
                    r"\bdeque class\b|"
                    r"\bclass for(?: a| the)? deque\b|"
                    r"\bimplements? a deque\b|"
                    r"\bdouble[- ]ended queue class\b",
                    low,
                )
            )
            and "circular" not in low,
            examples=(
                (([1, 2, 3],), [1, 2, 3]),
                (([],), []),
                ((["a", "b"],), ["a", "b"]),
            ),
        ),
        T(
            "min_heap_class",
            "def min_heap_demo(values):\n"
            '    """Push then pop to exercise MinHeap (sorted ascending)."""\n'
            "    h = MinHeap()\n"
            "    for value in values:\n"
            "        h.push(value)\n"
            "    out = []\n"
            "    while len(h):\n"
            "        out.append(h.pop())\n"
            "    return out\n"
            "\n"
            "\n"
            "class MinHeap:\n"
            '    """Binary min-heap using list + heapq."""\n'
            "\n"
            "    def __init__(self):\n"
            "        import heapq\n"
            "        self._data = []\n"
            "        self._heapq = heapq\n"
            "\n"
            "    def push(self, value):\n"
            "        self._heapq.heappush(self._data, value)\n"
            "\n"
            "    def pop(self):\n"
            "        if not self._data:\n"
            "            raise IndexError('pop from empty heap')\n"
            "        return self._heapq.heappop(self._data)\n"
            "\n"
            "    def peek(self):\n"
            "        if not self._data:\n"
            "            raise IndexError('peek from empty heap')\n"
            "        return self._data[0]\n"
            "\n"
            "    def __len__(self):\n"
            "        return len(self._data)\n",
            lambda low: bool(
                re.search(
                    r"\b(?:create|implement|write|build)(?: a)?(?: python)? class(?: that)?(?: for| that implements)?(?: a| the)? (?:min[- ]?heap|heap|binary heap)\b|"
                    r"\b(?:min[- ]?heap|binary heap|heap) class\b|"
                    r"\bclass for(?: a| the)? (?:min[- ]?heap|heap|binary heap)\b|"
                    r"\bimplements? a (?:min[- ]?)?heap\b",
                    low,
                )
            )
            and "priority" not in low,
            examples=(
                (([3, 1, 2],), [1, 2, 3]),
                (([],), []),
                (([5],), [5]),
            ),
        ),
        T(
            "hash_map_class",
            "def hashmap_demo(pairs, key):\n"
            '    """Put pairs then get a key from HashMap."""\n'
            "    hm = HashMap()\n"
            "    for k, v in pairs:\n"
            "        hm.put(k, v)\n"
            "    return hm.get(key)\n"
            "\n"
            "\n"
            "class HashMap:\n"
            '    """Dict-backed hash map with put/get."""\n'
            "\n"
            "    def __init__(self):\n"
            "        self._data = {}\n"
            "\n"
            "    def put(self, key, value):\n"
            "        self._data[key] = value\n"
            "\n"
            "    def get(self, key, default=None):\n"
            "        return self._data.get(key, default)\n"
            "\n"
            "    def __contains__(self, key):\n"
            "        return key in self._data\n"
            "\n"
            "    def __len__(self):\n"
            "        return len(self._data)\n",
            lambda low: bool(
                re.search(
                    r"\b(?:create|implement|write|build)(?: a)?(?: python)? class(?: that)?(?: for| that implements)?(?: a| the)? (?:hash[- ]?map|hashmap)\b|"
                    r"\b(?:hash[- ]?map|hashmap) class\b|"
                    r"\bclass for(?: a| the)? (?:hash[- ]?map|hashmap)\b|"
                    r"\bimplements? a (?:hash[- ]?map|hashmap)\b",
                    low,
                )
            )
            and "table" not in low,
            examples=(
                (([("a", 1), ("b", 2)], "a"), 1),
                (([("a", 1)], "missing"), None),
                (([], "x"), None),
            ),
        ),
    ]
