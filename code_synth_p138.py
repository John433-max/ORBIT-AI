"""Cycle 416: graph asks that still fell back after maze / union-find.

Matchers stay phrase-specific so maze, maze II, nearest-exit, and
smallest-string-from-leaf stay on earlier templates.
- the maze iii (lex-smallest rolling path; LC 499)
- regions cut by slashes (4-triangle union-find; LC 959)
- smallest string with swaps (index union-find; LC 1202)
- accounts merge (email union-find; LC 721)
- redundant connection (first cycle edge; LC 684)
- similar string groups (swap-similar union-find; LC 839)
"""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "the_maze_iii",
            "def findShortestWay(maze, ball, hole):\n"
            '    """Lex-smallest shortest path of a rolling ball, or impossible."""\n'
            "    import heapq\n"
            "    rows, cols = len(maze), len(maze[0])\n"
            "    hr, hc = hole\n"
            "    dirs = (('d', 1, 0), ('l', 0, -1), ('r', 0, 1), ('u', -1, 0))\n"
            "    best = {}\n"
            "    heap = [(0, '', ball[0], ball[1])]\n"
            "    while heap:\n"
            "        dist, path, r, c = heapq.heappop(heap)\n"
            "        if (r, c) in best:\n"
            "            continue\n"
            "        best[(r, c)] = (dist, path)\n"
            "        if r == hr and c == hc:\n"
            "            return path\n"
            "        for letter, dr, dc in dirs:\n"
            "            nr, nc, steps = r, c, 0\n"
            "            while (\n"
            "                0 <= nr + dr < rows\n"
            "                and 0 <= nc + dc < cols\n"
            "                and maze[nr + dr][nc + dc] == 0\n"
            "            ):\n"
            "                nr += dr\n"
            "                nc += dc\n"
            "                steps += 1\n"
            "                if nr == hr and nc == hc:\n"
            "                    break\n"
            "            if steps == 0:\n"
            "                continue\n"
            "            nd, npth = dist + steps, path + letter\n"
            "            if (nr, nc) not in best:\n"
            "                heapq.heappush(heap, (nd, npth, nr, nc))\n"
            "    return 'impossible'\n",
            lambda low: "maze iii" in low,
            (
                (
                    (
                        [
                            [0, 0, 0, 0, 0],
                            [1, 1, 0, 0, 1],
                            [0, 0, 0, 0, 0],
                            [0, 1, 0, 0, 1],
                            [0, 1, 0, 0, 0],
                        ],
                        [4, 3],
                        [0, 1],
                    ),
                    "lul",
                ),
                (
                    (
                        [
                            [0, 0, 0, 0, 0],
                            [1, 1, 0, 0, 1],
                            [0, 0, 0, 0, 0],
                            [0, 1, 0, 0, 1],
                            [0, 1, 0, 0, 0],
                        ],
                        [4, 3],
                        [3, 0],
                    ),
                    "impossible",
                ),
            ),
        ),
        T(
            "regions_cut_by_slashes",
            "def regionsBySlashes(grid):\n"
            '    """Regions after splitting each cell with / or \\\\ (LC 959)."""\n'
            "    n = len(grid)\n"
            "    parent = list(range(4 * n * n))\n"
            "\n"
            "    def find(x):\n"
            "        while parent[x] != x:\n"
            "            parent[x] = parent[parent[x]]\n"
            "            x = parent[x]\n"
            "        return x\n"
            "\n"
            "    def union(a, b):\n"
            "        ra, rb = find(a), find(b)\n"
            "        if ra == rb:\n"
            "            return False\n"
            "        parent[ra] = rb\n"
            "        return True\n"
            "\n"
            "    comps = 4 * n * n\n"
            "\n"
            "    def uid(i, j, k):\n"
            "        return (i * n + j) * 4 + k\n"
            "\n"
            "    for i in range(n):\n"
            "        for j in range(n):\n"
            "            base = uid(i, j, 0)\n"
            "            ch = grid[i][j]\n"
            "            if ch == '/':\n"
            "                pairs = ((0, 3), (1, 2))\n"
            "            elif ch == '\\\\':\n"
            "                pairs = ((0, 1), (2, 3))\n"
            "            else:\n"
            "                pairs = ((0, 1), (1, 2), (2, 3))\n"
            "            for a, b in pairs:\n"
            "                if union(base + a, base + b):\n"
            "                    comps -= 1\n"
            "            if i + 1 < n and union(base + 2, uid(i + 1, j, 0)):\n"
            "                comps -= 1\n"
            "            if j + 1 < n and union(base + 1, uid(i, j + 1, 3)):\n"
            "                comps -= 1\n"
            "    return comps\n",
            lambda low: "regions cut by slashes" in low or "cut by slashes" in low,
            (
                (([" /", "/ "],), 2),
                (([" /", "  "],), 1),
                ((["/\\", "\\/"],), 5),
            ),
        ),
        T(
            "smallest_string_with_swaps",
            "def smallestStringWithSwaps(s, pairs):\n"
            '    """Smallest string after swapping indices in the same component."""\n'
            "    n = len(s)\n"
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
            "            parent[ra] = rb\n"
            "\n"
            "    for a, b in pairs:\n"
            "        union(a, b)\n"
            "    groups = {}\n"
            "    for i in range(n):\n"
            "        groups.setdefault(find(i), []).append(i)\n"
            "    out = list(s)\n"
            "    for idxs in groups.values():\n"
            "        chars = sorted(out[i] for i in idxs)\n"
            "        for i, ch in zip(sorted(idxs), chars):\n"
            "            out[i] = ch\n"
            "    return ''.join(out)\n",
            lambda low: "smallest string with swaps" in low,
            (
                (("dcab", [[0, 3], [1, 2]]), "bacd"),
                (("dcab", [[0, 3], [1, 2], [0, 2]]), "abcd"),
                (("cba", [[0, 1], [1, 2]]), "abc"),
            ),
        ),
        T(
            "accounts_merge",
            "def accountsMerge(accounts):\n"
            '    """Merge accounts that share an email address."""\n'
            "    parent = {}\n"
            "\n"
            "    def find(x):\n"
            "        parent.setdefault(x, x)\n"
            "        while parent[x] != x:\n"
            "            parent[x] = parent[parent[x]]\n"
            "            x = parent[x]\n"
            "        return x\n"
            "\n"
            "    def union(a, b):\n"
            "        ra, rb = find(a), find(b)\n"
            "        if ra != rb:\n"
            "            parent[ra] = rb\n"
            "\n"
            "    email_to_name = {}\n"
            "    for acc in accounts:\n"
            "        name = acc[0]\n"
            "        first = acc[1]\n"
            "        for email in acc[1:]:\n"
            "            email_to_name[email] = name\n"
            "            union(first, email)\n"
            "    groups = {}\n"
            "    for email in email_to_name:\n"
            "        groups.setdefault(find(email), []).append(email)\n"
            "    res = []\n"
            "    for emails in groups.values():\n"
            "        emails.sort()\n"
            "        res.append([email_to_name[emails[0]]] + emails)\n"
            "    res.sort(key=lambda row: (row[0], row[1:]))\n"
            "    return res\n"
            "\n"
            "def accounts_merge(accounts):\n"
            "    return accountsMerge(accounts)\n",
            lambda low: (
                "accounts merge" in low or "merge accounts" in low or "merges accounts" in low
            ),
            (
                (
                    (
                        [
                            ["John", "johnsmith@mail.com", "john_newyork@mail.com"],
                            ["John", "johnsmith@mail.com", "john00@mail.com"],
                            ["Mary", "mary@mail.com"],
                            ["John", "johnnybravo@mail.com"],
                        ],
                    ),
                    [
                        ["John", "john00@mail.com", "john_newyork@mail.com", "johnsmith@mail.com"],
                        ["John", "johnnybravo@mail.com"],
                        ["Mary", "mary@mail.com"],
                    ],
                ),
            ),
        ),
        T(
            "redundant_connection",
            "def findRedundantConnection(edges):\n"
            '    """Edge that closes the first cycle in an undirected graph."""\n'
            "    parent = {}\n"
            "\n"
            "    def find(x):\n"
            "        parent.setdefault(x, x)\n"
            "        while parent[x] != x:\n"
            "            parent[x] = parent[parent[x]]\n"
            "            x = parent[x]\n"
            "        return x\n"
            "\n"
            "    def union(a, b):\n"
            "        ra, rb = find(a), find(b)\n"
            "        if ra == rb:\n"
            "            return False\n"
            "        parent[ra] = rb\n"
            "        return True\n"
            "\n"
            "    last = []\n"
            "    for a, b in edges:\n"
            "        if not union(a, b):\n"
            "            last = [a, b]\n"
            "    return last\n"
            "\n"
            "def redundant_connection(edges):\n"
            "    return findRedundantConnection(edges)\n",
            lambda low: "redundant connection" in low and "redundant connection ii" not in low,
            (
                (([[1, 2], [1, 3], [2, 3]],), [2, 3]),
                (([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]],), [1, 4]),
            ),
        ),
        T(
            "similar_string_groups",
            "def numSimilarGroups(strs):\n"
            '    """Groups of strings equal after at most one swap of two chars."""\n'
            "    n = len(strs)\n"
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
            "            parent[ra] = rb\n"
            "\n"
            "    def similar(a, b):\n"
            "        diff = [i for i in range(len(a)) if a[i] != b[i]]\n"
            "        return len(diff) == 0 or (\n"
            "            len(diff) == 2 and a[diff[0]] == b[diff[1]] and a[diff[1]] == b[diff[0]]\n"
            "        )\n"
            "\n"
            "    for i in range(n):\n"
            "        for j in range(i + 1, n):\n"
            "            if similar(strs[i], strs[j]):\n"
            "                union(i, j)\n"
            "    return len({find(i) for i in range(n)})\n",
            lambda low: "similar string groups" in low,
            (
                ((["tars", "rats", "arts", "star"],), 2),
                ((["omv", "ovm"],), 1),
            ),
        ),
    ]
