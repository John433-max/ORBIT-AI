"""Cycle 559: classic data-structure class asks that returned NotImplemented drafts.

Fills natural-language class requests for Queue, LinkedList, BST, HashTable,
PriorityQueue, and Graph that previously fell through to stubs.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "queue_class",
            "def queue_demo(values):\n"
            '    """Enqueue then dequeue (FIFO) to exercise Queue."""\n'
            "    q = Queue()\n"
            "    for value in values:\n"
            "        q.enqueue(value)\n"
            "    out = []\n"
            "    while len(q):\n"
            "        out.append(q.dequeue())\n"
            "    return out\n"
            "\n"
            "\n"
            "class Queue:\n"
            '    """List-backed FIFO queue."""\n'
            "\n"
            "    def __init__(self):\n"
            "        self._data = []\n"
            "\n"
            "    def enqueue(self, value):\n"
            "        self._data.append(value)\n"
            "\n"
            "    def dequeue(self):\n"
            "        if not self._data:\n"
            "            raise IndexError('dequeue from empty queue')\n"
            "        return self._data.pop(0)\n"
            "\n"
            "    def peek(self):\n"
            "        if not self._data:\n"
            "            raise IndexError('peek from empty queue')\n"
            "        return self._data[0]\n"
            "\n"
            "    def __len__(self):\n"
            "        return len(self._data)\n",
            lambda low: bool(
                re.search(
                    r"\b(?:create|implement|write|build)(?: a)?(?: python)? class(?: that)?(?: for| that implements)?(?: a| the)? queue\b|"
                    r"\bqueue class\b|"
                    r"\bclass for(?: a| the)? queue\b|"
                    r"\bimplements? a queue\b",
                    low,
                )
            )
            and "stack" not in low
            and "circular" not in low
            and "using stacks" not in low
            and "priority" not in low,
            examples=(
                (([1, 2, 3],), [1, 2, 3]),
                (([],), []),
                ((["a", "b"],), ["a", "b"]),
            ),
        ),
        T(
            "linked_list_class",
            "def linked_list_demo(values):\n"
            '    """Append values then materialize the list."""\n'
            "    ll = LinkedList()\n"
            "    for value in values:\n"
            "        ll.append(value)\n"
            "    return ll.to_list()\n"
            "\n"
            "\n"
            "class ListNode:\n"
            "    def __init__(self, val=0, next=None):\n"
            "        self.val = val\n"
            "        self.next = next\n"
            "\n"
            "\n"
            "class LinkedList:\n"
            '    """Singly linked list with append and materialize."""\n'
            "\n"
            "    def __init__(self):\n"
            "        self.head = None\n"
            "\n"
            "    def append(self, val):\n"
            "        node = ListNode(val)\n"
            "        if self.head is None:\n"
            "            self.head = node\n"
            "            return\n"
            "        cur = self.head\n"
            "        while cur.next is not None:\n"
            "            cur = cur.next\n"
            "        cur.next = node\n"
            "\n"
            "    def to_list(self):\n"
            "        out = []\n"
            "        cur = self.head\n"
            "        while cur is not None:\n"
            "            out.append(cur.val)\n"
            "            cur = cur.next\n"
            "        return out\n",
            lambda low: bool(
                re.search(
                    r"\b(?:create|implement|write|build)(?: a)?(?: python)? class(?: that)?(?: for| that implements)?(?: a| the)? linked[- ]?list\b|"
                    r"\blinked[- ]?list class\b|"
                    r"\bclass for(?: a| the)? linked[- ]?list\b|"
                    r"\bimplements? a linked[- ]?list\b",
                    low,
                )
            )
            and "reverse" not in low
            and "palindrome" not in low
            and "sort" not in low
            and "doubly" not in low
            and "cycle" not in low,
            examples=(
                (([1, 2, 3],), [1, 2, 3]),
                (([],), []),
                (([9],), [9]),
            ),
        ),
        T(
            "bst_class",
            "def bst_demo(values):\n"
            '    """Insert then inorder to exercise BST."""\n'
            "    tree = BST()\n"
            "    for value in values:\n"
            "        tree.insert(value)\n"
            "    return tree.inorder()\n"
            "\n"
            "\n"
            "class _Node:\n"
            "    def __init__(self, val):\n"
            "        self.val = val\n"
            "        self.left = None\n"
            "        self.right = None\n"
            "\n"
            "\n"
            "class BST:\n"
            '    """Binary search tree with insert and inorder."""\n'
            "\n"
            "    def __init__(self):\n"
            "        self.root = None\n"
            "\n"
            "    def insert(self, val):\n"
            "        def _ins(node, val):\n"
            "            if node is None:\n"
            "                return _Node(val)\n"
            "            if val < node.val:\n"
            "                node.left = _ins(node.left, val)\n"
            "            elif val > node.val:\n"
            "                node.right = _ins(node.right, val)\n"
            "            return node\n"
            "        self.root = _ins(self.root, val)\n"
            "\n"
            "    def inorder(self):\n"
            "        out = []\n"
            "        def _walk(node):\n"
            "            if node is None:\n"
            "                return\n"
            "            _walk(node.left)\n"
            "            out.append(node.val)\n"
            "            _walk(node.right)\n"
            "        _walk(self.root)\n"
            "        return out\n",
            lambda low: bool(
                re.search(
                    r"\b(?:create|implement|write|build)(?: a)?(?: python)? class(?: that)?(?: for| that implements)?(?: a| the)? (?:binary[-_ ]?search[-_ ]?tree|binarysearchtree|bst)\b|"
                    r"\b(?:binary[-_ ]?search[-_ ]?tree|binarysearchtree|bst) class\b|"
                    r"\bclass for(?: a| the)? (?:binary[-_ ]?search[-_ ]?tree|binarysearchtree|bst)\b|"
                    r"\bimplements? a (?:binary[-_ ]?search[-_ ]?tree|binarysearchtree|bst)\b",
                    low,
                )
            )
            and "insert into" not in low
            and "delete" not in low
            and "validate" not in low
            and "valid" not in low,
            examples=(
                (([3, 1, 4, 2],), [1, 2, 3, 4]),
                (([],), []),
                (([5],), [5]),
            ),
        ),
        T(
            "hash_table_class",
            "def hash_table_demo(pairs):\n"
            '    """Put then get to exercise HashTable."""\n'
            "    ht = HashTable()\n"
            "    for key, value in pairs:\n"
            "        ht.put(key, value)\n"
            "    return [ht.get(key) for key, _ in pairs]\n"
            "\n"
            "\n"
            "class HashTable:\n"
            '    """Chaining hash table with put/get."""\n'
            "\n"
            "    def __init__(self, capacity=8):\n"
            "        self._buckets = [[] for _ in range(capacity)]\n"
            "\n"
            "    def _idx(self, key):\n"
            "        return hash(key) % len(self._buckets)\n"
            "\n"
            "    def put(self, key, value):\n"
            "        bucket = self._buckets[self._idx(key)]\n"
            "        for i, (k, _) in enumerate(bucket):\n"
            "            if k == key:\n"
            "                bucket[i] = (key, value)\n"
            "                return\n"
            "        bucket.append((key, value))\n"
            "\n"
            "    def get(self, key, default=None):\n"
            "        for k, v in self._buckets[self._idx(key)]:\n"
            "            if k == key:\n"
            "                return v\n"
            "        return default\n",
            lambda low: bool(
                re.search(
                    r"\b(?:create|implement|write|build)(?: a)?(?: python)? class(?: that)?(?: for| that implements)?(?: a| the)? (?:hash[- ]?table|hashtable|hash map|hashmap)\b|"
                    r"\b(?:hash[- ]?table|hashtable|hash map) class\b|"
                    r"\bclass for(?: a| the)? (?:hash[- ]?table|hashtable|hash map)\b|"
                    r"\bimplements? a (?:hash[- ]?table|hashtable|hash map)\b",
                    low,
                )
            )
            and "design hashmap" not in low
            and "design_hashmap" not in low,
            examples=(
                (((("a", 1), ("b", 2)),), [1, 2]),
                (((),), []),
                (((("x", 9),),), [9]),
            ),
        ),
        T(
            "priority_queue_class",
            "def priority_queue_demo(values):\n"
            '    """Push then pop to exercise min PriorityQueue."""\n'
            "    pq = PriorityQueue()\n"
            "    for value in values:\n"
            "        pq.push(value)\n"
            "    out = []\n"
            "    while len(pq):\n"
            "        out.append(pq.pop())\n"
            "    return out\n"
            "\n"
            "\n"
            "class PriorityQueue:\n"
            '    """Min-heap priority queue."""\n'
            "\n"
            "    def __init__(self):\n"
            "        self._data = []\n"
            "\n"
            "    def push(self, value):\n"
            "        self._data.append(value)\n"
            "        self._sift_up(len(self._data) - 1)\n"
            "\n"
            "    def pop(self):\n"
            "        if not self._data:\n"
            "            raise IndexError('pop from empty priority queue')\n"
            "        top = self._data[0]\n"
            "        last = self._data.pop()\n"
            "        if self._data:\n"
            "            self._data[0] = last\n"
            "            self._sift_down(0)\n"
            "        return top\n"
            "\n"
            "    def __len__(self):\n"
            "        return len(self._data)\n"
            "\n"
            "    def _sift_up(self, i):\n"
            "        while i > 0:\n"
            "            parent = (i - 1) // 2\n"
            "            if self._data[i] >= self._data[parent]:\n"
            "                break\n"
            "            self._data[i], self._data[parent] = self._data[parent], self._data[i]\n"
            "            i = parent\n"
            "\n"
            "    def _sift_down(self, i):\n"
            "        n = len(self._data)\n"
            "        while True:\n"
            "            left = 2 * i + 1\n"
            "            right = 2 * i + 2\n"
            "            smallest = i\n"
            "            if left < n and self._data[left] < self._data[smallest]:\n"
            "                smallest = left\n"
            "            if right < n and self._data[right] < self._data[smallest]:\n"
            "                smallest = right\n"
            "            if smallest == i:\n"
            "                break\n"
            "            self._data[i], self._data[smallest] = self._data[smallest], self._data[i]\n"
            "            i = smallest\n",
            lambda low: bool(
                re.search(
                    r"\b(?:create|implement|write|build)(?: a)?(?: python)? class(?: that)?(?: for| that implements)?(?: a| the)? priority[- ]?queue\b|"
                    r"\bpriority[- ]?queue class\b|"
                    r"\bclass for(?: a| the)? priority[- ]?queue\b|"
                    r"\bimplements? a priority[- ]?queue\b|"
                    r"\bpriority[- ]?queue(?: operations?)?(?: with)?(?: push|pop|peek|insert|extract)\b|"
                    r"\b(?:push|pop|peek).{0,24}priority[- ]?queue\b|"
                    r"\b(?:implement|write|build|create)(?: a)?(?: min)? priority[- ]?queue\b|"
                    r"\bpq (?:push|pop|peek)\b",
                    low,
                )
            )
            and "decrease" not in low
            and "fibonacci" not in low
            and "binary heap" not in low
            and "max-heap" not in low
            and "max heap" not in low,
            examples=(
                (([3, 1, 2],), [1, 2, 3]),
                (([],), []),
                (([5, 5, 1],), [1, 5, 5]),
            ),
        ),
        T(
            "graph_class",
            "def graph_demo(edges):\n"
            '    """Add undirected edges then return sorted adjacency lists."""\n'
            "    g = Graph()\n"
            "    for u, v in edges:\n"
            "        g.add_edge(u, v)\n"
            "    return {node: sorted(nbrs) for node, nbrs in sorted(g.adj.items())}\n"
            "\n"
            "\n"
            "class Graph:\n"
            '    """Undirected adjacency-list graph."""\n'
            "\n"
            "    def __init__(self):\n"
            "        self.adj = {}\n"
            "\n"
            "    def add_edge(self, u, v):\n"
            "        self.adj.setdefault(u, set()).add(v)\n"
            "        self.adj.setdefault(v, set()).add(u)\n",
            lambda low: bool(
                re.search(
                    r"\b(?:create|implement|write|build)(?: a)?(?: python)? class(?: that)?(?: for| that implements)?(?: a| the)? graph\b|"
                    r"\bgraph class\b|"
                    r"\bclass for(?: a| the)? graph\b|"
                    r"\bimplements? a graph\b",
                    low,
                )
            )
            and "clone" not in low
            and "valid" not in low
            and "bipartite" not in low
            and "course" not in low,
            examples=(
                (([(1, 2), (2, 3)],), {1: [2], 2: [1, 3], 3: [2]}),
                (([],), {}),
                (([(0, 0)],), {0: [0]}),
            ),
        ),
    ]
