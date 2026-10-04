"""Cycle 414: graph asks that still fell back to draft stubs.

Matchers are phrase-specific so nearest-exit maze, bipartite, and islands stay put.
- the maze (ball rolls to a wall; LC 490)
- the maze ii (shortest rolling distance; LC 505)
- sentence similarity ii (union-find synonyms; LC 737)
- satisfiability of equality equations (LC 990)
- unreachable node pairs (component sizes; LC 2316)
- closest meeting node on a functional graph (LC 2359)
"""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "the_maze",
            "def hasPath(maze, start, destination):\n"
            '    """True if a ball rolling to walls can stop on destination."""\n'
            "    rows, cols = len(maze), len(maze[0])\n"
            "    er, ec = destination\n"
            "    seen = set()\n"
            "    stack = [tuple(start)]\n"
            "    dirs = ((1, 0), (-1, 0), (0, 1), (0, -1))\n"
            "    while stack:\n"
            "        r, c = stack.pop()\n"
            "        if (r, c) in seen:\n"
            "            continue\n"
            "        seen.add((r, c))\n"
            "        if r == er and c == ec:\n"
            "            return True\n"
            "        for dr, dc in dirs:\n"
            "            nr, nc = r, c\n"
            "            while (\n"
            "                0 <= nr + dr < rows\n"
            "                and 0 <= nc + dc < cols\n"
            "                and maze[nr + dr][nc + dc] == 0\n"
            "            ):\n"
            "                nr += dr\n"
            "                nc += dc\n"
            "            if (nr, nc) not in seen:\n"
            "                stack.append((nr, nc))\n"
            "    return False\n",
            lambda low: (
                "the maze" in low
                and "maze ii" not in low
                and "maze iii" not in low
                and "exit" not in low
            ),
            (
                (
                    (
                        [
                            [0, 0, 1, 0, 0],
                            [0, 0, 0, 0, 0],
                            [0, 0, 0, 1, 0],
                            [1, 1, 0, 1, 1],
                            [0, 0, 0, 0, 0],
                        ],
                        [0, 4],
                        [4, 4],
                    ),
                    True,
                ),
                (
                    (
                        [
                            [0, 0, 1, 0, 0],
                            [0, 0, 0, 0, 0],
                            [0, 0, 0, 1, 0],
                            [1, 1, 0, 1, 1],
                            [0, 0, 0, 0, 0],
                        ],
                        [0, 4],
                        [3, 2],
                    ),
                    False,
                ),
            ),
        ),
        T(
            "the_maze_ii",
            "def shortestDistance(maze, start, destination):\n"
            '    """Shortest distance a rolling ball travels, or -1."""\n'
            "    import heapq\n"
            "    rows, cols = len(maze), len(maze[0])\n"
            "    er, ec = destination\n"
            "    dist = {tuple(start): 0}\n"
            "    heap = [(0, start[0], start[1])]\n"
            "    dirs = ((1, 0), (-1, 0), (0, 1), (0, -1))\n"
            "    while heap:\n"
            "        d, r, c = heapq.heappop(heap)\n"
            "        if d != dist.get((r, c)):\n"
            "            continue\n"
            "        if r == er and c == ec:\n"
            "            return d\n"
            "        for dr, dc in dirs:\n"
            "            nr, nc, steps = r, c, 0\n"
            "            while (\n"
            "                0 <= nr + dr < rows\n"
            "                and 0 <= nc + dc < cols\n"
            "                and maze[nr + dr][nc + dc] == 0\n"
            "            ):\n"
            "                nr += dr\n"
            "                nc += dc\n"
            "                steps += 1\n"
            "            nd = d + steps\n"
            "            if nd < dist.get((nr, nc), 10 ** 9):\n"
            "                dist[(nr, nc)] = nd\n"
            "                heapq.heappush(heap, (nd, nr, nc))\n"
            "    return -1\n",
            lambda low: "maze ii" in low and "maze iii" not in low,
            (
                (
                    (
                        [
                            [0, 0, 1, 0, 0],
                            [0, 0, 0, 0, 0],
                            [0, 0, 0, 1, 0],
                            [1, 1, 0, 1, 1],
                            [0, 0, 0, 0, 0],
                        ],
                        [0, 4],
                        [4, 4],
                    ),
                    12,
                ),
                (
                    (
                        [
                            [0, 0, 1, 0, 0],
                            [0, 0, 0, 0, 0],
                            [0, 0, 0, 1, 0],
                            [1, 1, 0, 1, 1],
                            [0, 0, 0, 0, 0],
                        ],
                        [0, 4],
                        [3, 2],
                    ),
                    -1,
                ),
            ),
        ),
        T(
            "sentence_similarity_ii",
            "def areSentencesSimilarTwo(sentence1, sentence2, similarPairs):\n"
            '    """True if equal-length sentences match under transitive synonyms."""\n'
            "    if len(sentence1) != len(sentence2):\n"
            "        return False\n"
            "    parent = {}\n\n"
            "    def find(x):\n"
            "        parent.setdefault(x, x)\n"
            "        while parent[x] != x:\n"
            "            parent[x] = parent[parent[x]]\n"
            "            x = parent[x]\n"
            "        return x\n\n"
            "    for a, b in similarPairs:\n"
            "        ra, rb = find(a), find(b)\n"
            "        if ra != rb:\n"
            "            parent[ra] = rb\n"
            "    return all(find(a) == find(b) for a, b in zip(sentence1, sentence2))\n",
            lambda low: "sentence similarity" in low,
            (
                (
                    (
                        ["great", "acting", "skills"],
                        ["fine", "drama", "talent"],
                        [["great", "fine"], ["acting", "drama"], ["skills", "talent"]],
                    ),
                    True,
                ),
                (
                    (
                        ["great"],
                        ["great"],
                        [],
                    ),
                    True,
                ),
            ),
        ),
        T(
            "equality_equations",
            "def equationsPossible(equations):\n"
            '    """True if == / != constraints on variables a-z can hold."""\n'
            "    parent = {chr(ord('a') + i): chr(ord('a') + i) for i in range(26)}\n\n"
            "    def find(x):\n"
            "        while parent[x] != x:\n"
            "            parent[x] = parent[parent[x]]\n"
            "            x = parent[x]\n"
            "        return x\n\n"
            "    for eq in equations:\n"
            "        if eq[1] == '=':\n"
            "            parent[find(eq[0])] = find(eq[3])\n"
            "    for eq in equations:\n"
            "        if eq[1] == '!' and find(eq[0]) == find(eq[3]):\n"
            "            return False\n"
            "    return True\n",
            lambda low: "equality equations" in low
            or ("satisfiability" in low and "equation" in low),
            (
                ((["a==b", "b!=a"],), False),
                ((["b==a", "a==b"],), True),
            ),
        ),
        T(
            "unreachable_pairs",
            "def countPairs(n, edges):\n"
            '    """Pairs of nodes that cannot reach each other."""\n'
            "    adj = [[] for _ in range(n)]\n"
            "    for u, v in edges:\n"
            "        adj[u].append(v)\n"
            "        adj[v].append(u)\n"
            "    seen = [False] * n\n"
            "    sizes = []\n"
            "    for i in range(n):\n"
            "        if seen[i]:\n"
            "            continue\n"
            "        stack = [i]\n"
            "        seen[i] = True\n"
            "        size = 0\n"
            "        while stack:\n"
            "            u = stack.pop()\n"
            "            size += 1\n"
            "            for v in adj[u]:\n"
            "                if not seen[v]:\n"
            "                    seen[v] = True\n"
            "                    stack.append(v)\n"
            "        sizes.append(size)\n"
            "    ans = 0\n"
            "    remain = n\n"
            "    for size in sizes:\n"
            "        remain -= size\n"
            "        ans += size * remain\n"
            "    return ans\n",
            lambda low: "unreachable" in low and "pair" in low,
            (
                ((3, [[0, 1], [0, 2], [1, 2]]), 0),
                ((7, [[0, 2], [0, 5], [2, 4], [1, 6], [5, 4]]), 14),
            ),
        ),
        T(
            "closest_meeting_node",
            "def closestMeetingNode(edges, node1, node2):\n"
            '    """Node minimizing the max distance from two starts, or -1."""\n'
            "    def dists(start):\n"
            "        out = {}\n"
            "        step = 0\n"
            "        node = start\n"
            "        while node != -1 and node not in out:\n"
            "            out[node] = step\n"
            "            step += 1\n"
            "            node = edges[node]\n"
            "        return out\n\n"
            "    d1, d2 = dists(node1), dists(node2)\n"
            "    best, ans = 10 ** 9, -1\n"
            "    for i in range(len(edges)):\n"
            "        if i in d1 and i in d2:\n"
            "            score = max(d1[i], d2[i])\n"
            "            if score < best:\n"
            "                best, ans = score, i\n"
            "    return ans\n",
            lambda low: "closest node" in low and "two" in low,
            (
                (([2, 2, 3, -1], 0, 1), 2),
                (([1, 2, -1], 0, 2), 2),
            ),
        ),
    ]
