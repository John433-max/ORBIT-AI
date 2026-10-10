"""Cycle 547: URL parse, topo sort, BFS, DFS, union-find, sieve primes."""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "parse_url",
            "def parse_url(url):\n"
            '    """Parse a URL into scheme, host, port, path, and query."""\n'
            "    from urllib.parse import urlparse\n"
            "    parsed = urlparse(str(url))\n"
            "    return {\n"
            '        "scheme": parsed.scheme,\n'
            '        "host": parsed.hostname or "",\n'
            '        "port": parsed.port,\n'
            '        "path": parsed.path,\n'
            '        "query": parsed.query,\n'
            "    }\n",
            lambda low: bool(
                re.search(
                    r"\bpars(?:e|es|ing)[_ ](?:a |the )?url\b|"
                    r"\burl[_ ]parse\b|"
                    r"\bparse[_ ]url\b|"
                    r"\burlparse\b|"
                    r"\bparse a web address\b",
                    low,
                )
            )
            and "decode" not in low
            and "encode" not in low
            and "join" not in low,
            (
                (
                    ("https://example.com/a?x=1",),
                    {"scheme": "https", "host": "example.com", "port": None, "path": "/a", "query": "x=1"},
                ),
                (
                    ("http://localhost:8080/health",),
                    {"scheme": "http", "host": "localhost", "port": 8080, "path": "/health", "query": ""},
                ),
            ),
        ),
        T(
            "topological_sort",
            "def topological_sort(graph):\n"
            '    """Kahn topological order. graph is {node: [outgoing neighbors]}."""\n'
            "    from collections import deque\n"
            "    nodes = set(graph)\n"
            "    for nbrs in graph.values():\n"
            "        nodes.update(nbrs)\n"
            "    indeg = {node: 0 for node in nodes}\n"
            "    adj = {node: [] for node in nodes}\n"
            "    for src, nbrs in graph.items():\n"
            "        for dst in nbrs:\n"
            "            adj[src].append(dst)\n"
            "            indeg[dst] += 1\n"
            "    queue = deque(sorted(node for node in nodes if indeg[node] == 0))\n"
            "    order = []\n"
            "    while queue:\n"
            "        src = queue.popleft()\n"
            "        order.append(src)\n"
            "        for dst in adj[src]:\n"
            "            indeg[dst] -= 1\n"
            "            if indeg[dst] == 0:\n"
            "                queue.append(dst)\n"
            "    if len(order) != len(nodes):\n"
            '        raise ValueError("cycle")\n'
            "    return order\n",
            lambda low: bool(
                re.search(
                    r"\btopological[_ ]sort\b|"
                    r"\btopo[_ ]sort\b|"
                    r"\btopological order\b|"
                    r"\bkahn(?:'s)? algorithm\b",
                    low,
                )
            ),
            (
                (({"A": ["B"], "B": ["C"], "C": []},), ["A", "B", "C"]),
                (({"cook": ["eat"], "shop": ["cook"], "eat": []},), ["shop", "cook", "eat"]),
            ),
        ),
        T(
            "bfs",
            "def bfs(graph, start):\n"
            '    """Breadth-first visit order from start. graph is {node: [neighbors]}."""\n'
            "    from collections import deque\n"
            "    seen = set()\n"
            "    order = []\n"
            "    queue = deque([start])\n"
            "    while queue:\n"
            "        node = queue.popleft()\n"
            "        if node in seen:\n"
            "            continue\n"
            "        seen.add(node)\n"
            "        order.append(node)\n"
            "        for nxt in graph.get(node, []):\n"
            "            if nxt not in seen:\n"
            "                queue.append(nxt)\n"
            "    return order\n",
            lambda low: bool(
                re.search(
                    r"\bbfs\b|"
                    r"\bbreadth[- ]first(?: search)?\b|"
                    r"\bbreadth first\b",
                    low,
                )
            )
            and "dfs" not in low
            and "depth" not in low
            and "topolog" not in low,
            (
                (({"A": ["B", "C"], "B": ["D"], "C": [], "D": []}, "A"), ["A", "B", "C", "D"]),
                (({"1": ["2"], "2": ["3"], "3": []}, "1"), ["1", "2", "3"]),
            ),
        ),
        T(
            "dfs",
            "def dfs(graph, start):\n"
            '    """Depth-first visit order from start. graph is {node: [neighbors]}."""\n'
            "    seen = set()\n"
            "    order = []\n"
            "\n"
            "    def walk(node):\n"
            "        if node in seen:\n"
            "            return\n"
            "        seen.add(node)\n"
            "        order.append(node)\n"
            "        for nxt in graph.get(node, []):\n"
            "            walk(nxt)\n"
            "\n"
            "    walk(start)\n"
            "    return order\n",
            lambda low: bool(
                re.search(
                    r"\bdfs\b|"
                    r"\bdepth[- ]first(?: search)?\b|"
                    r"\bdepth first\b",
                    low,
                )
            )
            and "bfs" not in low
            and "breadth" not in low
            and "topolog" not in low,
            (
                (({"A": ["B", "C"], "B": ["D"], "C": [], "D": []}, "A"), ["A", "B", "D", "C"]),
                (({"1": ["2"], "2": ["3"], "3": []}, "1"), ["1", "2", "3"]),
            ),
        ),
        T(
            "union_find",
            "def union_find(n, unions):\n"
            '    """Union-find on 0..n-1. Return the compressed parent of each index."""\n'
            "    parent = list(range(int(n)))\n"
            "\n"
            "    def find(x):\n"
            "        while parent[x] != x:\n"
            "            parent[x] = parent[parent[x]]\n"
            "            x = parent[x]\n"
            "        return x\n"
            "\n"
            "    for a, b in unions:\n"
            "        ra, rb = find(a), find(b)\n"
            "        if ra != rb:\n"
            "            parent[rb] = ra\n"
            "    return [find(i) for i in range(len(parent))]\n",
            lambda low: bool(
                re.search(
                    r"\bunion[- ]find\b|"
                    r"\bdisjoint[- ]set\b|"
                    r"\bunion find\b|"
                    r"\bdsu\b",
                    low,
                )
            )
            and "list union" not in low,
            (
                ((5, [(0, 1), (1, 2), (3, 4)]), [0, 0, 0, 3, 3]),
                ((3, []), [0, 1, 2]),
            ),
        ),
        T(
            "sieve_primes",
            "def sieve_primes(n):\n"
            '    """Return all prime numbers less than or equal to n."""\n'
            "    n = int(n)\n"
            "    if n < 2:\n"
            "        return []\n"
            "    sieve = [True] * (n + 1)\n"
            "    sieve[0] = sieve[1] = False\n"
            "    p = 2\n"
            "    while p * p <= n:\n"
            "        if sieve[p]:\n"
            "            start = p * p\n"
            "            sieve[start:n + 1:p] = [False] * (((n - start) // p) + 1)\n"
            "        p += 1\n"
            "    return [i for i in range(n + 1) if sieve[i]]\n",
            lambda low: bool(
                re.search(
                    r"\ball primes? (?:up to|<=|less than or equal)\b|"
                    r"\bprimes? up to\b|"
                    r"\blist (?:of )?primes?\b|"
                    r"\bsieve_primes\b|"
                    r"\bprime numbers? (?:up to|<=)\b",
                    low,
                )
            )
            and "count" not in low
            and "number of primes" not in low,
            (
                ((10,), [2, 3, 5, 7]),
                ((2,), [2]),
                ((1,), []),
            ),
        ),
    ]
