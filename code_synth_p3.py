"""ORBIT code_synth template pack (Cycle 244 split)."""
from __future__ import annotations
import re
from code_synth import Template, _TWO

def templates():
    return [

        Template(
            "split_list_to_parts",
            "def split_list_to_parts(head, k):\n"
            '    """Split a [val, next] list into k consecutive parts."""\n'
            "    def _copy(node):\n"
            "        if node is None:\n"
            "            return None\n"
            "        return [node[0], _copy(node[1] if len(node) > 1 else None)]\n"
            "    vals = []\n"
            "    cur = _copy(head)\n"
            "    while cur is not None:\n"
            "        vals.append(cur[0])\n"
            "        cur = cur[1] if len(cur) > 1 else None\n"
            "    k = int(k)\n"
            "    n = len(vals)\n"
            "    q, r = divmod(n, k) if k else (0, 0)\n"
            "    parts = []\n"
            "    i = 0\n"
            "    for p in range(k):\n"
            "        take = q + (1 if p < r else 0)\n"
            "        chunk = vals[i : i + take]\n"
            "        i += take\n"
            "        node = None\n"
            "        for v in reversed(chunk):\n"
            "            node = [v, node]\n"
            "        parts.append(node)\n"
            "    return parts\n",
            lambda low: bool(
                re.search(
                    r"\bsplit_list_to_parts\b|"
                    r"\bsplit(?:s|ting)? (a )?linked list (in)?to parts\b|"
                    r"\bsplit(?:s|ting)? (a )?linked list into k\b",
                    low,
                )
            ),
            (
                (([1, [2, [3, None]]], 5), [[1, None], [2, None], [3, None], None, None]),
                (([1, [2, [3, [4, [5, [6, [7, None]]]]]]], 3), [[1, [2, [3, None]]], [4, [5, None]], [6, [7, None]]]),
            ),
        ),
        Template(
            "plus_one_linked_list",
            "def plus_one_linked_list(head):\n"
            '    """Add one to a non-negative integer stored MSD-first as [val, next]."""\n'
            "    def _copy(node):\n"
            "        if node is None:\n"
            "            return None\n"
            "        return [node[0], _copy(node[1] if len(node) > 1 else None)]\n"
            "    vals = []\n"
            "    cur = _copy(head)\n"
            "    while cur is not None:\n"
            "        vals.append(cur[0])\n"
            "        cur = cur[1] if len(cur) > 1 else None\n"
            "    if not vals:\n"
            "        return [1, None]\n"
            "    carry = 1\n"
            "    for i in range(len(vals) - 1, -1, -1):\n"
            "        s = vals[i] + carry\n"
            "        vals[i] = s % 10\n"
            "        carry = s // 10\n"
            "    if carry:\n"
            "        vals.insert(0, carry)\n"
            "    node = None\n"
            "    for v in reversed(vals):\n"
            "        node = [v, node]\n"
            "    return node\n",
            lambda low: bool(
                re.search(
                    r"\bplus_one_linked_list\b|"
                    r"\bplus[- ]?one (on |to )?(a )?linked list\b|"
                    r"\badd one to (a )?linked list\b|"
                    r"\bincrement (a )?linked list\b",
                    low,
                )
            ),
            (
                (([1, [2, [3, None]]],), [1, [2, [4, None]]]),
                (([9, [9, None]],), [1, [0, [0, None]]]),
            ),
        ),
        Template(
            "clone_graph",
            "def clone_graph(graph):\n"
            '    """Deep-copy an adjacency-list graph {node: [neighbors]}."""\n'
            "    if not graph:\n"
            "        return {}\n"
            "    cloned = {n: [] for n in graph}\n"
            "    for n, nbrs in graph.items():\n"
            "        cloned[n] = list(nbrs)\n"
            "    return cloned\n",
            lambda low: bool(
                re.search(
                    r"\bclone_graph\b|"
                    r"\bclon(?:e|es|ing)\b.{0,24}\bgraph\b|"
                    r"\bcopy (an? )?undirected graph\b",
                    low,
                )
            ),
            (
                (({1: [2], 2: [1]},), {1: [2], 2: [1]}),
                (({},), {}),
            ),
        ),
        Template(
            "top_k_frequent",
            "def top_k_frequent(nums, k):\n"
            '    """Return the k most frequent elements (stable by first-seen on ties)."""\n'
            "    counts = {}\n"
            "    order = []\n"
            "    for x in nums:\n"
            "        if x not in counts:\n"
            "            order.append(x)\n"
            "            counts[x] = 0\n"
            "        counts[x] += 1\n"
            "    ranked = sorted(order, key=lambda x: (-counts[x], order.index(x)))\n"
            "    return ranked[: int(k)]\n",
            lambda low: bool(
                re.search(
                    r"\btop_k_frequent\b|"
                    r"\btop k frequent\b|"
                    r"\bk most frequent\b|"
                    r"\bmost frequent elements\b",
                    low,
                )
            ),
            (
                (([1, 1, 1, 2, 2, 3], 2), [1, 2]),
                (([1], 1), [1]),
            ),
        ),
        Template(
            "find_kth_largest",
            "def find_kth_largest(nums, k):\n"
            '    """Return the kth largest element in nums."""\n'
            "    return sorted(nums, reverse=True)[int(k) - 1]\n",
            lambda low: bool(
                re.search(
                    r"\bfind_kth_largest\b|"
                    r"\bkth largest\b|"
                    r"\bk-th largest\b",
                    low,
                )
            ),
            (
                (([3, 2, 1, 5, 6, 4], 2), 5),
                (([3, 2, 3, 1, 2, 4, 5, 5, 6], 4), 4),
            ),
        ),
        Template(
            "length_of_longest_substring",
            "def length_of_longest_substring(s):\n"
            '    """Length of the longest substring without repeating characters."""\n'
            "    last = {}\n"
            "    start = 0\n"
            "    best = 0\n"
            "    for i, ch in enumerate(s):\n"
            "        if ch in last and last[ch] >= start:\n"
            "            start = last[ch] + 1\n"
            "        last[ch] = i\n"
            "        best = max(best, i - start + 1)\n"
            "    return best\n",
            lambda low: bool(
                re.search(
                    r"\blength_of_longest_substring\b|"
                    r"\blongest substring without repeating\b|"
                    r"\blongest substring with(?:out)? unique\b|"
                    r"\bno repeating characters\b.{0,16}\bsubstring\b|"
                    r"\bsubstring without repeating characters\b",
                    low,
                )
            ),
            (
                (("abcabcbb",), 3),
                (("bbbbb",), 1),
                (("pwwkew",), 3),
            ),
        ),
        Template(
            "daily_temperatures",
            "def daily_temperatures(temps):\n"
            '    """Days until a warmer temperature; 0 if none."""\n'
            "    n = len(temps)\n"
            "    out = [0] * n\n"
            "    stack = []\n"
            "    for i, t in enumerate(temps):\n"
            "        while stack and temps[stack[-1]] < t:\n"
            "            j = stack.pop()\n"
            "            out[j] = i - j\n"
            "        stack.append(i)\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bdaily_temperatures\b|"
                    r"\bdaily temperatures\b|"
                    r"\bdays until (a )?warmer\b|"
                    r"\bnext warmer (day|temperature)\b",
                    low,
                )
            ),
            (
                (([73, 74, 75, 71, 69, 72, 76, 73],), [1, 1, 4, 2, 1, 1, 0, 0]),
                (([30, 40, 50, 60],), [1, 1, 1, 0]),
            ),
        ),
        Template(
            "merge_k_lists",
            "def merge_k_lists(lists):\n"
            '    """Merge k sorted [val, next] lists into one sorted list."""\n'
            "    vals = []\n"
            "    for head in lists or []:\n"
            "        cur = head\n"
            "        while cur is not None:\n"
            "            vals.append(cur[0])\n"
            "            cur = cur[1] if len(cur) > 1 else None\n"
            "    vals.sort()\n"
            "    node = None\n"
            "    for v in reversed(vals):\n"
            "        node = [v, node]\n"
            "    return node\n",
            lambda low: bool(
                re.search(
                    r"\bmerge_k_lists\b|"
                    r"\bmerg(?:e|es|ing)\b.{0,24}\bk (sorted )?(linked )?lists\b|"
                    r"\bmerg(?:e|es|ing) k sorted linked lists\b",
                    low,
                )
            ),
            (
                (([[1, [4, [5, None]]], [1, [3, [4, None]]], [2, [6, None]]],), [1, [1, [2, [3, [4, [4, [5, [6, None]]]]]]]]),
                (([],), None),
            ),
        ),
        Template(
            "rotting_oranges",
            "def rotting_oranges(grid):\n"
            '    """Minutes until all oranges rot; -1 if impossible."""\n'
            "    grid = [row[:] for row in grid]\n"
            "    if not grid or not grid[0]:\n"
            "        return 0\n"
            "    rows, cols = len(grid), len(grid[0])\n"
            "    q = []\n"
            "    fresh = 0\n"
            "    for r in range(rows):\n"
            "        for c in range(cols):\n"
            "            if grid[r][c] == 2:\n"
            "                q.append((r, c, 0))\n"
            "            elif grid[r][c] == 1:\n"
            "                fresh += 1\n"
            "    minutes = 0\n"
            "    i = 0\n"
            "    while i < len(q):\n"
            "        r, c, t = q[i]\n"
            "        i += 1\n"
            "        minutes = t\n"
            "        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):\n"
            "            nr, nc = r + dr, c + dc\n"
            "            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:\n"
            "                grid[nr][nc] = 2\n"
            "                fresh -= 1\n"
            "                q.append((nr, nc, t + 1))\n"
            "    return minutes if fresh == 0 else -1\n",
            lambda low: bool(
                re.search(
                    r"\brotting_oranges\b|"
                    r"\brotting oranges\b|"
                    r"\boranges? rot\b|"
                    r"\brotten oranges\b",
                    low,
                )
            ),
            (
                (([[2, 1, 1], [1, 1, 0], [0, 1, 1]],), 4),
                (([[2, 1, 1], [0, 1, 1], [1, 0, 1]],), -1),
                (([[0, 2]],), 0),
            ),
        ),
        Template(
            "pacific_atlantic",
            "def pacific_atlantic(heights):\n"
            '    """Cells that can flow to both Pacific and Atlantic."""\n'
            "    if not heights or not heights[0]:\n"
            "        return []\n"
            "    rows, cols = len(heights), len(heights[0])\n"
            "\n"
            "    def flow(starts):\n"
            "        seen = set(starts)\n"
            "        stack = list(starts)\n"
            "        while stack:\n"
            "            r, c = stack.pop()\n"
            "            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):\n"
            "                nr, nc = r + dr, c + dc\n"
            "                if (\n"
            "                    0 <= nr < rows\n"
            "                    and 0 <= nc < cols\n"
            "                    and (nr, nc) not in seen\n"
            "                    and heights[nr][nc] >= heights[r][c]\n"
            "                ):\n"
            "                    seen.add((nr, nc))\n"
            "                    stack.append((nr, nc))\n"
            "        return seen\n"
            "\n"
            "    pac = [(0, c) for c in range(cols)] + [(r, 0) for r in range(rows)]\n"
            "    atl = [(rows - 1, c) for c in range(cols)] + [(r, cols - 1) for r in range(rows)]\n"
            "    both = flow(pac) & flow(atl)\n"
            "    return sorted([r, c] for r, c in both)\n",
            lambda low: bool(
                re.search(
                    r"\bpacific_atlantic\b|"
                    r"\bpacific and atlantic\b|"
                    r"\bpacific atlantic\b|"
                    r"\bwater flow\b.{0,24}\b(pacific|atlantic)\b",
                    low,
                )
            ),
            (
                (
                    (
                        [
                            [1, 2, 2, 3, 5],
                            [3, 2, 3, 4, 4],
                            [2, 4, 5, 3, 1],
                            [6, 7, 1, 4, 5],
                            [5, 1, 1, 2, 4],
                        ],
                    ),
                    [[0, 4], [1, 3], [1, 4], [2, 2], [3, 0], [3, 1], [4, 0]],
                ),
            ),
        ),
        Template(
            "flood_fill",
            "def flood_fill(image, sr, sc, color):\n"
            '    """Flood-fill image from (sr, sc) with color."""\n'
            "    if not image or not image[0]:\n"
            "        return image\n"
            "    rows, cols = len(image), len(image[0])\n"
            "    start = image[sr][sc]\n"
            "    if start == color:\n"
            "        return image\n"
            "    stack = [(sr, sc)]\n"
            "    image[sr][sc] = color\n"
            "    while stack:\n"
            "        r, c = stack.pop()\n"
            "        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):\n"
            "            nr, nc = r + dr, c + dc\n"
            "            if 0 <= nr < rows and 0 <= nc < cols and image[nr][nc] == start:\n"
            "                image[nr][nc] = color\n"
            "                stack.append((nr, nc))\n"
            "    return image\n",
            lambda low: bool(
                re.search(
                    r"\bflood_fill\b|"
                    r"\bflood[- ]fills?\b|"
                    r"\bfill(?:s|ing)?\b.{0,24}\b(image|grid|pixel)\b",
                    low,
                )
                and "island" not in low
            ),
            (
                (([[1, 1, 1], [1, 1, 0], [1, 0, 1]], 1, 1, 2), [[2, 2, 2], [2, 2, 0], [2, 0, 1]]),
            ),
        ),
        Template(
            "update_matrix",
            "def update_matrix(mat):\n"
            '    """Distance of each cell to the nearest 0."""\n'
            "    if not mat or not mat[0]:\n"
            "        return mat\n"
            "    rows, cols = len(mat), len(mat[0])\n"
            "    inf = rows * cols + 1\n"
            "    out = [[inf] * cols for _ in range(rows)]\n"
            "    q = []\n"
            "    for r in range(rows):\n"
            "        for c in range(cols):\n"
            "            if mat[r][c] == 0:\n"
            "                out[r][c] = 0\n"
            "                q.append((r, c))\n"
            "    i = 0\n"
            "    while i < len(q):\n"
            "        r, c = q[i]\n"
            "        i += 1\n"
            "        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):\n"
            "            nr, nc = r + dr, c + dc\n"
            "            if 0 <= nr < rows and 0 <= nc < cols and out[nr][nc] > out[r][c] + 1:\n"
            "                out[nr][nc] = out[r][c] + 1\n"
            "                q.append((nr, nc))\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bupdate_matrix\b|"
                    r"\b01 matrix\b|"
                    r"\b0/1 matrix\b|"
                    r"\bnearest 0\b|"
                    r"\bdistance to (the )?nearest zero\b",
                    low,
                )
            ),
            (
                (([[0, 0, 0], [0, 1, 0], [1, 1, 1]],), [[0, 0, 0], [0, 1, 0], [1, 2, 1]]),
            ),
        ),
        Template(
            "num_provinces",
            "def num_provinces(is_connected):\n"
            '    """Number of connected provinces in an n x n adjacency matrix."""\n'
            "    n = len(is_connected)\n"
            "    seen = [False] * n\n"
            "    provinces = 0\n"
            "    for i in range(n):\n"
            "        if seen[i]:\n"
            "            continue\n"
            "        provinces += 1\n"
            "        stack = [i]\n"
            "        seen[i] = True\n"
            "        while stack:\n"
            "            u = stack.pop()\n"
            "            for v in range(n):\n"
            "                if is_connected[u][v] and not seen[v]:\n"
            "                    seen[v] = True\n"
            "                    stack.append(v)\n"
            "    return provinces\n",
            lambda low: bool(
                re.search(
                    r"\bnum_provinces\b|"
                    r"\bnumber of provinces\b|"
                    r"\bconnected provinces\b|"
                    r"\bfriend circles\b",
                    low,
                )
            ),
            (
                (([[1, 1, 0], [1, 1, 0], [0, 0, 1]],), 2),
                (([[1, 0, 0], [0, 1, 0], [0, 0, 1]],), 3),
            ),
        ),
        Template(
            "surrounded_regions",
            "def surrounded_regions(board):\n"
            '    """Capture surrounded O regions in-place; return the board."""\n'
            "    if not board or not board[0]:\n"
            "        return board\n"
            "    rows, cols = len(board), len(board[0])\n"
            "\n"
            "    def mark(r, c):\n"
            "        stack = [(r, c)]\n"
            "        while stack:\n"
            "            i, j = stack.pop()\n"
            "            if i < 0 or i >= rows or j < 0 or j >= cols or board[i][j] != 'O':\n"
            "                continue\n"
            "            board[i][j] = 'E'\n"
            "            stack.extend(((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)))\n"
            "\n"
            "    for c in range(cols):\n"
            "        mark(0, c)\n"
            "        mark(rows - 1, c)\n"
            "    for r in range(rows):\n"
            "        mark(r, 0)\n"
            "        mark(r, cols - 1)\n"
            "    for r in range(rows):\n"
            "        for c in range(cols):\n"
            "            if board[r][c] == 'O':\n"
            "                board[r][c] = 'X'\n"
            "            elif board[r][c] == 'E':\n"
            "                board[r][c] = 'O'\n"
            "    return board\n",
            lambda low: bool(
                re.search(
                    r"\bsurrounded_regions\b|"
                    r"\bsurrounded regions\b|"
                    r"\bcapture surrounded\b|"
                    r"\bsurrounded o\b",
                    low,
                )
            ),
            (
                (
                    (
                        [
                            ["X", "X", "X", "X"],
                            ["X", "O", "O", "X"],
                            ["X", "X", "O", "X"],
                            ["X", "O", "X", "X"],
                        ],
                    ),
                    [
                        ["X", "X", "X", "X"],
                        ["X", "X", "X", "X"],
                        ["X", "X", "X", "X"],
                        ["X", "O", "X", "X"],
                    ],
                ),
            ),
        ),
        Template(
            "min_depth",
            "def min_depth(root):\n"
            '    """Minimum depth of a [val, left, right] binary tree."""\n'
            "    if root is None:\n"
            "        return 0\n"
            "    left = root[1] if len(root) > 1 else None\n"
            "    right = root[2] if len(root) > 2 else None\n"
            "    if left is None and right is None:\n"
            "        return 1\n"
            "    if left is None:\n"
            "        return 1 + min_depth(right)\n"
            "    if right is None:\n"
            "        return 1 + min_depth(left)\n"
            "    return 1 + min(min_depth(left), min_depth(right))\n",
            lambda low: bool(
                re.search(
                    r"\bmin(?:imum)? depth\b.{0,24}\b(binary )?tree\b|"
                    r"\bmin_depth\b",
                    low,
                )
            ),
            (
                (([3, [9, None, None], [20, [15, None, None], [7, None, None]]],), 2),
                (([2, None, [3, None, [4, None, None]]],), 3),
                ((None,), 0),
            ),
        ),
        Template(
            "kth_smallest",
            "def kth_smallest(root, k):\n"
            '    """k-th smallest value in a [val, left, right] BST (1-based)."""\n'
            "    stack = []\n"
            "    node = root\n"
            "    seen = 0\n"
            "    while stack or node is not None:\n"
            "        while node is not None:\n"
            "            stack.append(node)\n"
            "            node = node[1] if len(node) > 1 else None\n"
            "        node = stack.pop()\n"
            "        seen += 1\n"
            "        if seen == k:\n"
            "            return node[0]\n"
            "        node = node[2] if len(node) > 2 else None\n"
            "    raise ValueError('k out of range')\n",
            lambda low: bool(
                re.search(
                    r"\bkth_smallest\b|"
                    r"\bk-?th smallest\b.{0,32}\b(bst|binary search tree|tree)\b|"
                    r"\bkth smallest element in a bst\b",
                    low,
                )
            ),
            (
                (([3, [1, None, [2, None, None]], [4, None, None]], 1), 1),
                (([5, [3, [2, None, None], [4, None, None]], [6, None, None]], 3), 4),
            ),
        ),
        Template(
            "right_side_view",
            "def right_side_view(root):\n"
            '    """Values visible from the right side of a [val, left, right] tree."""\n'
            "    if root is None:\n"
            "        return []\n"
            "    out = []\n"
            "    q = [root]\n"
            "    while q:\n"
            "        nxt = []\n"
            "        out.append(q[-1][0])\n"
            "        for node in q:\n"
            "            left = node[1] if len(node) > 1 else None\n"
            "            right = node[2] if len(node) > 2 else None\n"
            "            if left is not None:\n"
            "                nxt.append(left)\n"
            "            if right is not None:\n"
            "                nxt.append(right)\n"
            "        q = nxt\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bright_side_view\b|"
                    r"\bright side view\b|"
                    r"\bbinary tree right side\b",
                    low,
                )
            ),
            (
                (([1, [2, None, [5, None, None]], [3, None, [4, None, None]]],), [1, 3, 4]),
                (([1, None, [3, None, None]],), [1, 3]),
                ((None,), []),
            ),
        ),
        Template(
            "sorted_array_to_bst",
            "def sorted_array_to_bst(nums):\n"
            '    """Convert a sorted array to a height-balanced [val, left, right] BST."""\n'
            "    def build(lo, hi):\n"
            "        if lo > hi:\n"
            "            return None\n"
            "        mid = (lo + hi) // 2\n"
            "        return [nums[mid], build(lo, mid - 1), build(mid + 1, hi)]\n"
            "    return build(0, len(nums) - 1)\n",
            lambda low: bool(
                re.search(
                    r"\bsorted_array_to_bst\b|"
                    r"\bconvert(?:s|ing)?\b.{0,24}\bsorted array\b.{0,24}\bbst\b|"
                    r"\bsorted array to (a )?(height-balanced )?bst\b",
                    low,
                )
            ),
            (
                (([-10, -3, 0, 5, 9],), [0, [-10, None, [-3, None, None]], [5, None, [9, None, None]]]),
                (([1, 3],), [1, None, [3, None, None]]),
            ),
        ),
        Template(
            "zigzag_level_order",
            "def zigzag_level_order(root):\n"
            '    """Zigzag level-order traversal of a [val, left, right] tree."""\n'
            "    if root is None:\n"
            "        return []\n"
            "    out = []\n"
            "    q = [root]\n"
            "    left_to_right = True\n"
            "    while q:\n"
            "        level = [node[0] for node in q]\n"
            "        if not left_to_right:\n"
            "            level.reverse()\n"
            "        out.append(level)\n"
            "        nxt = []\n"
            "        for node in q:\n"
            "            left = node[1] if len(node) > 1 else None\n"
            "            right = node[2] if len(node) > 2 else None\n"
            "            if left is not None:\n"
            "                nxt.append(left)\n"
            "            if right is not None:\n"
            "                nxt.append(right)\n"
            "        q = nxt\n"
            "        left_to_right = not left_to_right\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bzigzag_level_order\b|"
                    r"\bzigzag (level[- ]order|traversal)\b|"
                    r"\bbinary tree zigzag\b",
                    low,
                )
                and "right side" not in low
            ),
            (
                (([3, [9, None, None], [20, [15, None, None], [7, None, None]]],), [[3], [20, 9], [15, 7]]),
                (([1, None, None],), [[1]]),
                ((None,), []),
            ),
        ),
        Template(
            "range_sum_bst",
            "def range_sum_bst(root, low, high):\n"
            '    """Sum of BST values in [low, high] on a [val, left, right] tree."""\n'
            "    if root is None:\n"
            "        return 0\n"
            "    val = root[0]\n"
            "    left = root[1] if len(root) > 1 else None\n"
            "    right = root[2] if len(root) > 2 else None\n"
            "    total = 0\n"
            "    if low <= val <= high:\n"
            "        total += val\n"
            "    if val > low:\n"
            "        total += range_sum_bst(left, low, high)\n"
            "    if val < high:\n"
            "        total += range_sum_bst(right, low, high)\n"
            "    return total\n",
            lambda low: bool(
                re.search(
                    r"\brange_sum_bst\b|"
                    r"\brange sum of? bst\b|"
                    r"\brange sum\b.{0,24}\b(bst|binary search tree)\b",
                    low,
                )
            ),
            (
                (([10, [5, [3, None, None], [7, None, None]], [15, None, [18, None, None]]], 7, 15), 32),
                (([10, [5, [3, None, None], [7, None, None]], [15, None, [18, None, None]]], 6, 10), 17),
            ),
        ),
        Template(
            "subsets",
            "def subsets(nums):\n"
            '    """All subsets of nums (power set), stable input order."""\n'
            "    nums = list(nums)\n"
            "    out = []\n"
            "    path = []\n"
            "\n"
            "    def dfs(i):\n"
            "        if i == len(nums):\n"
            "            out.append(list(path))\n"
            "            return\n"
            "        dfs(i + 1)\n"
            "        path.append(nums[i])\n"
            "        dfs(i + 1)\n"
            "        path.pop()\n"
            "\n"
            "    dfs(0)\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bsubsets\b|"
                    r"\bpower set\b|"
                    r"\ball subsets\b",
                    low,
                )
                and "ii" not in low
                and "with dup" not in low
            ),
            (
                (([1, 2],), [[], [2], [1], [1, 2]]),
                (([],), [[]]),
            ),
        ),
        Template(
            "permute",
            "def permute(nums):\n"
            '    """All unique-index permutations of nums."""\n'
            "    nums = list(nums)\n"
            "    out = []\n"
            "    used = [False] * len(nums)\n"
            "    path = []\n"
            "\n"
            "    def dfs():\n"
            "        if len(path) == len(nums):\n"
            "            out.append(list(path))\n"
            "            return\n"
            "        for i, v in enumerate(nums):\n"
            "            if used[i]:\n"
            "                continue\n"
            "            used[i] = True\n"
            "            path.append(v)\n"
            "            dfs()\n"
            "            path.pop()\n"
            "            used[i] = False\n"
            "\n"
            "    dfs()\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bpermut(?:e|es|ations?)\b|"
                    r"\ball permutations\b",
                    low,
                )
                and "next_permutation" not in low
                and "next permutation" not in low
                and "string" not in low
                and "from permutation" not in low
                and "build array from" not in low
            ),
            (
                (([1, 2],), [[1, 2], [2, 1]]),
                (([1],), [[1]]),
            ),
        ),
        Template(
            "letter_combinations",
            "def letter_combinations(digits):\n"
            '    """Phone-letter combinations for digits 2-9."""\n'
            "    if not digits:\n"
            "        return []\n"
            "    pad = {\n"
            "        '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',\n"
            "        '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz',\n"
            "    }\n"
            "    out = ['']\n"
            "    for ch in str(digits):\n"
            "        if ch not in pad:\n"
            "            continue\n"
            "        letters = pad[ch]\n"
            "        nxt = []\n"
            "        for prefix in out:\n"
            "            for L in letters:\n"
            "                nxt.append(prefix + L)\n"
            "        out = nxt\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bletter[- ]?combinations\b|"
                    r"\bphone[- ]?(letter|keypad|number)\b|"
                    r"\bletter combin",
                    low,
                )
            ),
            (
                (("23",), ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"]),
                (("",), []),
            ),
        ),
        Template(
            "combination_sum_ii",
            "def combination_sum_ii(candidates, target):\n"
            '    """Unique combinations that sum to target (each number once)."""\n'
            "    cands = sorted(int(x) for x in candidates)\n"
            "    target = int(target)\n"
            "    out = []\n"
            "    path = []\n"
            "\n"
            "    def dfs(start, remain):\n"
            "        if remain == 0:\n"
            "            out.append(list(path))\n"
            "            return\n"
            "        prev = None\n"
            "        for i in range(start, len(cands)):\n"
            "            v = cands[i]\n"
            "            if v > remain:\n"
            "                break\n"
            "            if prev is not None and v == prev:\n"
            "                continue\n"
            "            path.append(v)\n"
            "            dfs(i + 1, remain - v)\n"
            "            path.pop()\n"
            "            prev = v\n"
            "\n"
            "    dfs(0, target)\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bcombination[- ]?sum[- ]?ii\b|"
                    r"\bcombination[- ]?sum 2\b|"
                    r"\bcombinations? that sum\b.{0,24}\b(once|no reuse|without reuse)\b|"
                    r"\beach number once\b.{0,24}\bcombination",
                    low,
                )
            ),
            (
                (([10, 1, 2, 7, 6, 1, 5], 8), [[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]),
                (([2, 5, 2, 1, 2], 5), [[1, 2, 2], [5]]),
            ),
        ),
        Template(
            "path_sum_ii",
            "def path_sum_ii(root, target):\n"
            '    """All root-to-leaf paths that sum to target on a [val, left, right] tree."""\n'
            "    out = []\n"
            "\n"
            "    def dfs(node, remain, path):\n"
            "        if node is None:\n"
            "            return\n"
            "        val = node[0]\n"
            "        left = node[1] if len(node) > 1 else None\n"
            "        right = node[2] if len(node) > 2 else None\n"
            "        path.append(val)\n"
            "        if left is None and right is None and remain == val:\n"
            "            out.append(list(path))\n"
            "        else:\n"
            "            dfs(left, remain - val, path)\n"
            "            dfs(right, remain - val, path)\n"
            "        path.pop()\n"
            "\n"
            "    dfs(root, int(target), [])\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bpath[- ]?sum[- ]?ii\b|"
                    r"\bpath[- ]?sum 2\b|"
                    r"\ball (root[- ]to[- ]leaf )?paths? that sum\b|"
                    r"\blist of paths\b.{0,24}\bsum\b",
                    low,
                )
            ),
            (
                (([5, [4, [11, [7, None, None], [2, None, None]], None], [8, [13, None, None], [4, None, [1, None, None]]]], 22),
                 [[5, 4, 11, 2]]),
                (([1, [2, None, None], [3, None, None]], 5), []),
            ),
        ),
        Template(
            "binary_tree_paths",
            "def binary_tree_paths(root):\n"
            '    """All root-to-leaf paths as val->val strings on a [val, left, right] tree."""\n'
            "    if root is None:\n"
            "        return []\n"
            "    out = []\n"
            "\n"
            "    def dfs(node, path):\n"
            "        val = node[0]\n"
            "        left = node[1] if len(node) > 1 else None\n"
            "        right = node[2] if len(node) > 2 else None\n"
            "        cur = path + [str(val)]\n"
            "        if left is None and right is None:\n"
            "            out.append('->'.join(cur))\n"
            "            return\n"
            "        if left is not None:\n"
            "            dfs(left, cur)\n"
            "        if right is not None:\n"
            "            dfs(right, cur)\n"
            "\n"
            "    dfs(root, [])\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bbinary_tree_paths\b|"
                    r"\bbinary tree paths\b|"
                    r"\ball root[- ]to[- ]leaf paths\b|"
                    r"\broot to leaf paths as strings\b",
                    low,
                )
                and "sum" not in low
            ),
            (
                (([1, [2, None, [5, None, None]], [3, None, None]],), ["1->2->5", "1->3"]),
                (([1, None, None],), ["1"]),
            ),
        ),
        Template(
            "inorder_traversal",
            "def inorder_traversal(root):\n"
            '    """Inorder values of a [val, left, right] binary tree."""\n'
            "    out = []\n"
            "\n"
            "    def dfs(node):\n"
            "        if node is None:\n"
            "            return\n"
            "        left = node[1] if len(node) > 1 else None\n"
            "        right = node[2] if len(node) > 2 else None\n"
            "        dfs(left)\n"
            "        out.append(node[0])\n"
            "        dfs(right)\n"
            "\n"
            "    dfs(root)\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\binorder[- ]?(traversal|walk|dfs)\b|"
                    r"\bin[- ]?order traversal\b|"
                    r"\binorder_traversal\b",
                    low,
                )
            ),
            (
                (([1, None, [2, [3, None, None], None]],), [1, 3, 2]),
                ((None,), []),
            ),
        ),
        Template(
            "preorder_traversal",
            "def preorder_traversal(root):\n"
            '    """Preorder values of a [val, left, right] binary tree."""\n'
            "    out = []\n"
            "\n"
            "    def dfs(node):\n"
            "        if node is None:\n"
            "            return\n"
            "        left = node[1] if len(node) > 1 else None\n"
            "        right = node[2] if len(node) > 2 else None\n"
            "        out.append(node[0])\n"
            "        dfs(left)\n"
            "        dfs(right)\n"
            "\n"
            "    dfs(root)\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bpreorder[- ]?(traversal|walk|dfs)\b|"
                    r"\bpre[- ]?order traversal\b|"
                    r"\bpreorder_traversal\b",
                    low,
                )
            ),
            (
                (([1, None, [2, [3, None, None], None]],), [1, 2, 3]),
                ((None,), []),
            ),
        ),
        Template(
            "postorder_traversal",
            "def postorder_traversal(root):\n"
            '    """Postorder values of a [val, left, right] binary tree."""\n'
            "    out = []\n"
            "\n"
            "    def dfs(node):\n"
            "        if node is None:\n"
            "            return\n"
            "        left = node[1] if len(node) > 1 else None\n"
            "        right = node[2] if len(node) > 2 else None\n"
            "        dfs(left)\n"
            "        dfs(right)\n"
            "        out.append(node[0])\n"
            "\n"
            "    dfs(root)\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bpostorder[- ]?(traversal|walk|dfs)\b|"
                    r"\bpost[- ]?order traversal\b|"
                    r"\bpostorder_traversal\b",
                    low,
                )
            ),
            (
                (([1, None, [2, [3, None, None], None]],), [3, 2, 1]),
                ((None,), []),
            ),
        ),
        Template(
            "max_path_sum",
            "def max_path_sum(root):\n"
            '    """Maximum any-node-to-any-node path sum on a [val, left, right] tree."""\n'
            "    best = [float('-inf')]\n"
            "\n"
            "    def gain(node):\n"
            "        if node is None:\n"
            "            return 0\n"
            "        left = node[1] if len(node) > 1 else None\n"
            "        right = node[2] if len(node) > 2 else None\n"
            "        lo = max(gain(left), 0)\n"
            "        ro = max(gain(right), 0)\n"
            "        best[0] = max(best[0], node[0] + lo + ro)\n"
            "        return node[0] + max(lo, ro)\n"
            "\n"
            "    gain(root)\n"
            "    return int(best[0]) if root is not None else 0\n",
            lambda low: bool(
                re.search(
                    r"\bmax(?:imum)?[- ]?path[- ]?sum\b|"
                    r"\bmax_path_sum\b|"
                    r"\bmaximum path\b.{0,16}\bsum\b",
                    low,
                )
            ),
            (
                (([1, [2, None, None], [3, None, None]],), 6),
                (([-10, [9, None, None], [20, [15, None, None], [7, None, None]]],), 42),
            ),
        ),
        Template(
            "flatten_binary_tree",
            "def flatten_binary_tree(root):\n"
            '    """Flatten a [val, left, right] tree into a right-linked preorder list."""\n'
            "    if root is None:\n"
            "        return None\n"
            "\n"
            "    def copy(node):\n"
            "        if node is None:\n"
            "            return None\n"
            "        return [\n"
            "            node[0],\n"
            "            copy(node[1]) if len(node) > 1 else None,\n"
            "            copy(node[2]) if len(node) > 2 else None,\n"
            "        ]\n"
            "\n"
            "    node = copy(root)\n"
            "    stack = [node]\n"
            "    prev = None\n"
            "    while stack:\n"
            "        cur = stack.pop()\n"
            "        if cur is None:\n"
            "            continue\n"
            "        right = cur[2] if len(cur) > 2 else None\n"
            "        left = cur[1] if len(cur) > 1 else None\n"
            "        if right is not None:\n"
            "            stack.append(right)\n"
            "        if left is not None:\n"
            "            stack.append(left)\n"
            "        if prev is not None:\n"
            "            prev[1] = None\n"
            "            prev[2] = cur\n"
            "        prev = cur\n"
            "        cur[1] = None\n"
            "    return node\n",
            lambda low: bool(
                re.search(
                    r"\bflatten[- ]?binary[- ]?tree\b|"
                    r"\bflatten(?:s|ed|ing)?\b.{0,32}\bbinary tree\b|"
                    r"\bflatten(?:s|ed|ing)?\b.{0,32}\btree\b.{0,24}\blinked list\b|"
                    r"\bflatten_binary_tree\b",
                    low,
                )
            ),
            (
                (
                    ([1, [2, [3, None, None], [4, None, None]], [5, None, [6, None, None]]],),
                    [1, None, [2, None, [3, None, [4, None, [5, None, [6, None, None]]]]]],
                ),
                ((None,), None),
            ),
        ),
        Template(
            "search_matrix",
            "def search_matrix(matrix, target):\n"
            '    """True if target is in a row-wise sorted 2D matrix with increasing rows."""\n'
            "    if not matrix or not matrix[0]:\n"
            "        return False\n"
            "    m, n = len(matrix), len(matrix[0])\n"
            "    lo, hi = 0, m * n - 1\n"
            "    target = matrix[0][0].__class__(target) if matrix[0] else target\n"
            "    while lo <= hi:\n"
            "        mid = (lo + hi) // 2\n"
            "        val = matrix[mid // n][mid % n]\n"
            "        if val == target:\n"
            "            return True\n"
            "        if val < target:\n"
            "            lo = mid + 1\n"
            "        else:\n"
            "            hi = mid - 1\n"
            "    return False\n",
            lambda low: bool(
                re.search(
                    r"\bsearch(?:es|ed|ing)?[- ]?(a )?(2d )?matrix\b|"
                    r"\bsearch(?:es|ed|ing)?\b.{0,24}\b(a )?(2d |sorted )?matrix\b|"
                    r"\bsearch_matrix\b|"
                    r"\btarget\b.{0,24}\b(2d |sorted )?matrix\b",
                    low,
                )
                and "rotated" not in low
                and "island" not in low
                and "word search" not in low
            ),
            (
                (([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 3), True),
                (([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 13), False),
            ),
        ),
        Template(
            "min_stack",
            "def min_stack(ops):\n"
            '    """Apply MinStack ops: push/pop/top/getMin. Return per-op results."""\n'
            "    stack, mins, out = [], [], []\n"
            "    for op in ops:\n"
            "        kind = op[0]\n"
            "        if kind == 'push':\n"
            "            x = op[1]\n"
            "            stack.append(x)\n"
            "            mins.append(x if not mins else min(mins[-1], x))\n"
            "            out.append(None)\n"
            "        elif kind == 'pop':\n"
            "            if stack:\n"
            "                stack.pop()\n"
            "                mins.pop()\n"
            "            out.append(None)\n"
            "        elif kind == 'top':\n"
            "            out.append(stack[-1] if stack else None)\n"
            "        elif kind == 'getMin':\n"
            "            out.append(mins[-1] if mins else None)\n"
            "        else:\n"
            "            out.append(None)\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bmin(?:imum)?[- ]?stack\b|"
                    r"\bmin_stack\b|"
                    r"\bstack\b.{0,24}\bget[- ]?min\b|"
                    r"\bgetmin\b.{0,16}\bstack\b",
                    low,
                )
            ),
            (
                (
                    (
                        [
                            ("push", -2),
                            ("push", 0),
                            ("push", -3),
                            ("getMin",),
                            ("pop",),
                            ("top",),
                            ("getMin",),
                        ],
                    ),
                    [None, None, None, -3, None, 0, -2],
                ),
                (([("push", 1), ("top",), ("getMin",)],), [None, 1, 1]),
            ),
        ),
        Template(
            "decode_string",
            "def decode_string(s):\n"
            '    """Decode k[encoded] nested strings."""\n'
            "    stack = []\n"
            "    cur_num = 0\n"
            "    cur = []\n"
            "    for ch in s:\n"
            "        if ch.isdigit():\n"
            "            cur_num = cur_num * 10 + int(ch)\n"
            "        elif ch == '[':\n"
            "            stack.append((''.join(cur), cur_num))\n"
            "            cur, cur_num = [], 0\n"
            "        elif ch == ']':\n"
            "            prev, k = stack.pop()\n"
            "            cur = list(prev) + cur * k\n"
            "        else:\n"
            "            cur.append(ch)\n"
            "    return ''.join(cur)\n",
            lambda low: bool(
                re.search(
                    r"\bdecode[- ]?string\b|"
                    r"\bdecode_string\b|"
                    r"\bdecode(?:s|d|ing)?\b.{0,16}\b(a |the |an )?string\b|"
                    r"\bdecode(?:s|d|ing)?\b.{0,24}\bk\[|"
                    r"\bnested encoded string\b",
                    low,
                )
                and "ways" not in low
                and "digit" not in low
                and "numeric" not in low
            ),
            (
                (("3[a]2[bc]",), "aaabcbc"),
                (("3[a2[c]]",), "accaccacc"),
            ),
        ),
        Template(
            "next_greater_element",
            "def next_greater_element(nums1, nums2):\n"
            '    """Next greater of each nums1 value inside nums2, else -1."""\n'
            "    nxt = {}\n"
            "    stack = []\n"
            "    for x in nums2:\n"
            "        while stack and stack[-1] < x:\n"
            "            nxt[stack.pop()] = x\n"
            "        stack.append(x)\n"
            "    return [nxt.get(x, -1) for x in nums1]\n",
            lambda low: bool(
                re.search(
                    r"\bnext[- ]?greater[- ]?element\b|"
                    r"\bnext_greater_element\b|"
                    r"\bnext greater\b.{0,16}\b(element|number|value)\b",
                    low,
                )
                and "ii" not in low
                and "circular" not in low
                and "temperature" not in low
            ),
            (
                (([4, 1, 2], [1, 3, 4, 2]), [-1, 3, -1]),
                (([2, 4], [1, 2, 3, 4]), [3, -1]),
            ),
        ),
        Template(
            "eval_rpn",
            "def eval_rpn(tokens):\n"
            '    """Evaluate reverse Polish notation tokens."""\n'
            "    stack = []\n"
            "    for tok in tokens:\n"
            "        if tok in '+-*/':\n"
            "            b, a = stack.pop(), stack.pop()\n"
            "            if tok == '+':\n"
            "                stack.append(a + b)\n"
            "            elif tok == '-':\n"
            "                stack.append(a - b)\n"
            "            elif tok == '*':\n"
            "                stack.append(a * b)\n"
            "            else:\n"
            "                stack.append(int(a / b))\n"
            "        else:\n"
            "            stack.append(int(tok))\n"
            "    return stack[-1] if stack else 0\n",
            lambda low: bool(
                re.search(
                    r"\beval(?:uate)?[- ]?rpn\b|"
                    r"\breverse polish\b|"
                    r"\bpostfix\b.{0,16}\b(notation|express)\b|"
                    r"\beval_rpn\b",
                    low,
                )
            ),
            (
                ((["2", "1", "+", "3", "*"],), 9),
                ((["4", "13", "5", "/", "+"],), 6),
            ),
        ),
        Template(
            "asteroid_collision",
            "def asteroid_collision(asteroids):\n"
            '    """Simulate asteroid collisions; + right, - left."""\n'
            "    stack = []\n"
            "    for a in asteroids:\n"
            "        alive = True\n"
            "        while alive and a < 0 and stack and stack[-1] > 0:\n"
            "            if stack[-1] < -a:\n"
            "                stack.pop()\n"
            "                continue\n"
            "            if stack[-1] == -a:\n"
            "                stack.pop()\n"
            "            alive = False\n"
            "        if alive:\n"
            "            stack.append(a)\n"
            "    return stack\n",
            lambda low: bool(
                re.search(
                    r"\basteroids?[- ]?collisions?\b|"
                    r"\basteroid_collision\b|"
                    r"\bcolliding asteroids\b",
                    low,
                )
            ),
            (
                (([5, 10, -5],), [5, 10]),
                (([8, -8],), []),
            ),
        ),
        Template(
            "queue_using_stacks",
            "def queue_using_stacks(ops):\n"
            '    """Simulate a FIFO queue with two stacks. Return per-op results."""\n'
            "    inn, out, res = [], [], []\n"
            "    for op in ops:\n"
            "        kind = op[0]\n"
            "        if kind == 'push':\n"
            "            inn.append(op[1])\n"
            "            res.append(None)\n"
            "        elif kind == 'pop':\n"
            "            if not out:\n"
            "                while inn:\n"
            "                    out.append(inn.pop())\n"
            "            res.append(out.pop() if out else None)\n"
            "        elif kind == 'peek':\n"
            "            if not out:\n"
            "                while inn:\n"
            "                    out.append(inn.pop())\n"
            "            res.append(out[-1] if out else None)\n"
            "        elif kind == 'empty':\n"
            "            res.append(not inn and not out)\n"
            "        else:\n"
            "            res.append(None)\n"
            "    return res\n",
            lambda low: bool(
                re.search(
                    r"\bqueue[- ]?using[- ]?stacks\b|"
                    r"\bqueue_using_stacks\b|"
                    r"\bimplement(?:s|ing)?\b.{0,16}\bqueue\b.{0,24}\bstacks?\b|"
                    r"\bqueue from (two )?stacks\b",
                    low,
                )
            ),
            (
                (
                    (
                        [
                            ("push", 1),
                            ("push", 2),
                            ("peek",),
                            ("pop",),
                            ("empty",),
                        ],
                    ),
                    [None, None, 1, 1, False],
                ),
                (([("push", 9), ("pop",), ("empty",)],), [None, 9, True]),
            ),
        ),
        Template(
            "last_stone_weight",
            "def last_stone_weight(stones):\n"
            '    """Smash heaviest pair; remainder is abs(a-b). Return last stone."""\n'
            "    import heapq\n"
            "    heap = [-s for s in stones]\n"
            "    heapq.heapify(heap)\n"
            "    while len(heap) > 1:\n"
            "        a = -heapq.heappop(heap)\n"
            "        b = -heapq.heappop(heap)\n"
            "        if a != b:\n"
            "            heapq.heappush(heap, -(a - b))\n"
            "    return -heap[0] if heap else 0\n",
            lambda low: bool(
                re.search(
                    r"\blast[- ]?stone[- ]?weight\b|"
                    r"\blast_stone_weight\b|"
                    r"\bsmash(?:es|ing)?\b.{0,16}\bstones\b|"
                    r"\bheaviest stones\b",
                    low,
                )
                and "ii" not in low
                and "1049" not in low
            ),
            (
                (([2, 7, 4, 1, 8, 1],), 1),
                (([1],), 1),
            ),
        ),
        Template(
            "task_scheduler",
            "def task_scheduler(tasks, n):\n"
            '    """Min intervals to finish tasks with cooldown n between same letters."""\n'
            "    from collections import Counter\n"
            "    if not tasks:\n"
            "        return 0\n"
            "    freq = Counter(tasks)\n"
            "    mx = max(freq.values())\n"
            "    n_mx = sum(1 for v in freq.values() if v == mx)\n"
            "    return max(len(tasks), (mx - 1) * (n + 1) + n_mx)\n",
            lambda low: bool(
                re.search(
                    r"\btask[- ]?scheduler\b|"
                    r"\btask_scheduler\b|"
                    r"\bcooldown\b.{0,24}\btasks?\b|"
                    r"\bschedule\b.{0,24}\btasks?\b.{0,24}\b(cooldown|idle|n)\b",
                    low,
                )
            ),
            (
                ((["A", "A", "A", "B", "B", "B"], 2), 8),
                ((["A", "A", "A", "B", "B", "B"], 0), 6),
            ),
        ),
        Template(
            "reorganize_string",
            "def reorganize_string(s):\n"
            '    """Rearrange so no two adjacent chars match; empty if impossible."""\n'
            "    import heapq\n"
            "    from collections import Counter\n"
            "    cnt = Counter(s)\n"
            "    if not s:\n"
            "        return ''\n"
            "    if max(cnt.values()) > (len(s) + 1) // 2:\n"
            "        return ''\n"
            "    heap = [(-c, ch) for ch, c in cnt.items()]\n"
            "    heapq.heapify(heap)\n"
            "    out = []\n"
            "    prev = (0, '')\n"
            "    while heap:\n"
            "        c, ch = heapq.heappop(heap)\n"
            "        out.append(ch)\n"
            "        if prev[0] < 0:\n"
            "            heapq.heappush(heap, prev)\n"
            "        prev = (c + 1, ch)\n"
            "    return ''.join(out)\n",
            lambda low: bool(
                re.search(
                    r"\breorganize[- ]?string\b|"
                    r"\breorganize_string\b|"
                    r"\breorganize(?:s|d|ing)?\b.{0,24}\bstring\b|"
                    r"\brearrange(?:s|d|ing)?\b.{0,24}\bstring\b.{0,40}\badjacent\b|"
                    r"\bno two adjacent\b.{0,24}\b(char|letter|character)s?\b",
                    low,
                )
            ),
            (
                (("aab",), "aba"),
                (("aaab",), ""),
            ),
        ),
        Template(
            "sliding_window_maximum",
            "def sliding_window_maximum(nums, k):\n"
            '    """Max of each window of size k (deque of decreasing indices)."""\n'
            "    from collections import deque\n"
            "    if k <= 0 or not nums:\n"
            "        return []\n"
            "    dq, out = deque(), []\n"
            "    for i, x in enumerate(nums):\n"
            "        if dq and dq[0] <= i - k:\n"
            "            dq.popleft()\n"
            "        while dq and nums[dq[-1]] <= x:\n"
            "            dq.pop()\n"
            "        dq.append(i)\n"
            "        if i >= k - 1:\n"
            "            out.append(nums[dq[0]])\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bsliding[- ]?window[- ]?maximum\b|"
                    r"\bsliding window maximum\b|"
                    r"\bsliding_window_maximum\b|"
                    r"\bmax(?:imum)?\b.{0,16}\bsliding window\b|"
                    r"\bmax(?:imum)? (?:of |in )?(?:each |every )?sliding window\b|"
                    r"\bwindow of size k\b.{0,24}\bmax",
                    low,
                )
            ),
            (
                (([1, 3, -1, -3, 5, 3, 6, 7], 3), [3, 3, 5, 5, 6, 7]),
                (([1], 1), [1]),
            ),
        ),
        Template(
            "k_closest",
            "def k_closest(points, k):\n"
            '    """K points closest to origin (heap by squared distance)."""\n'
            "    import heapq\n"
            "    return heapq.nsmallest(k, points, key=lambda p: p[0] * p[0] + p[1] * p[1])\n",
            lambda low: bool(
                re.search(
                    r"\bk[- ]?closest\b|"
                    r"\bk_closest\b|"
                    r"\bclosest\b.{0,16}\bk\b.{0,16}\bpoints?\b|"
                    r"\bk points closest\b",
                    low,
                )
            ),
            (
                (([[1, 3], [-2, 2]], 1), [[-2, 2]]),
                (([[3, 3], [5, -1], [-2, 4]], 2), [[3, 3], [-2, 4]]),
            ),
        ),
        Template(
            "median_finder",
            "def median_finder(ops):\n"
            '    """Two-heap running median. ops: (add, x) or (find,)."""\n'
            "    import heapq\n"
            "    lo, hi, res = [], [], []\n"
            "    for op in ops:\n"
            "        if op[0] == 'add':\n"
            "            x = op[1]\n"
            "            if not lo or x <= -lo[0]:\n"
            "                heapq.heappush(lo, -x)\n"
            "            else:\n"
            "                heapq.heappush(hi, x)\n"
            "            if len(lo) > len(hi) + 1:\n"
            "                heapq.heappush(hi, -heapq.heappop(lo))\n"
            "            elif len(hi) > len(lo):\n"
            "                heapq.heappush(lo, -heapq.heappop(hi))\n"
            "            res.append(None)\n"
            "        else:\n"
            "            if not lo:\n"
            "                res.append(None)\n"
            "            elif len(lo) > len(hi):\n"
            "                res.append(float(-lo[0]))\n"
            "            else:\n"
            "                res.append((-lo[0] + hi[0]) / 2.0)\n"
            "    return res\n",
            lambda low: bool(
                re.search(
                    r"\bmedian[- ]?finder\b|"
                    r"\bmedian_finder\b|"
                    r"\bfind[- ]?median[- ]?from[- ]?data[- ]?stream\b|"
                    r"\bfinds? (the )?median from (a )?data stream\b|"
                    r"\brunning median\b|"
                    r"\bmedian (of|from) (a )?(data )?stream\b",
                    low,
                )
            ),
            (
                (
                    (
                        [
                            ("add", 1),
                            ("add", 2),
                            ("find",),
                            ("add", 3),
                            ("find",),
                        ],
                    ),
                    [None, None, 1.5, None, 2.0],
                ),
                (([("add", 5), ("find",)],), [None, 5.0]),
            ),
        ),
        Template(
            "container_with_most_water",
            "def container_with_most_water(height):\n"
            '    """Max area between two lines (LeetCode 11)."""\n'
            "    i, j, best = 0, len(height) - 1, 0\n"
            "    while i < j:\n"
            "        best = max(best, min(height[i], height[j]) * (j - i))\n"
            "        if height[i] < height[j]:\n"
            "            i += 1\n"
            "        else:\n"
            "            j -= 1\n"
            "    return best\n",
            lambda low: bool(
                re.search(
                    r"\bcontainer[- ]?with[- ]?most[- ]?water\b|"
                    r"\bmax(?:imum)? area (?:of |between )?(?:a )?container\b|"
                    r"\bmost water (?:a )?container\b|"
                    r"\bholds? the most water\b",
                    low,
                )
            ),
            (
                (([1, 8, 6, 2, 5, 4, 8, 3, 7],), 49),
                (([1, 1],), 1),
            ),
        ),
        Template(
            "sort_colors",
            "def sort_colors(nums):\n"
            '    """Dutch-flag sort of 0/1/2 in place; returns nums."""\n'
            "    lo, mid, hi = 0, 0, len(nums) - 1\n"
            "    while mid <= hi:\n"
            "        if nums[mid] == 0:\n"
            "            nums[lo], nums[mid] = nums[mid], nums[lo]\n"
            "            lo += 1\n"
            "            mid += 1\n"
            "        elif nums[mid] == 1:\n"
            "            mid += 1\n"
            "        else:\n"
            "            nums[mid], nums[hi] = nums[hi], nums[mid]\n"
            "            hi -= 1\n"
            "    return nums\n",
            lambda low: bool(
                re.search(
                    r"\bsort[- ]?colors\b|"
                    r"\bdutch[- ]?(national[- ]?)?flag\b|"
                    r"\bsort (?:an? )?(?:array|list) of 0s?,? 1s?,? (and )?2s?\b|"
                    r"\bsort 0.?1.?2\b",
                    low,
                )
            ),
            (
                (([2, 0, 2, 1, 1, 0],), [0, 0, 1, 1, 2, 2]),
                (([2, 0, 1],), [0, 1, 2]),
            ),
        ),
        Template(
            "find_duplicate",
            "def find_duplicate(nums):\n"
            '    """Find the repeated number in 1..n with Floyd cycle."""\n'
            "    slow = fast = nums[0]\n"
            "    while True:\n"
            "        slow = nums[slow]\n"
            "        fast = nums[nums[fast]]\n"
            "        if slow == fast:\n"
            "            break\n"
            "    slow = nums[0]\n"
            "    while slow != fast:\n"
            "        slow = nums[slow]\n"
            "        fast = nums[fast]\n"
            "    return slow\n",
            lambda low: bool(
                re.search(
                    r"\bfinds?[- ]?(the[- ]?)?duplicates?\b|"
                    r"\bfinds?[- ]?duplicate[- ]?number\b|"
                    r"\bduplicate number\b|"
                    r"\brepeated number in 1\s*\.\.\s*n\b",
                    low,
                )
                and "contains" not in low
                and "all duplicate" not in low
                and "all the duplicate" not in low
                and "disappeared" not in low
            ),
            (
                (([1, 3, 4, 2, 2],), 2),
                (([3, 1, 3, 4, 2],), 3),
            ),
        ),
        Template(
            "can_complete_circuit",
            "def can_complete_circuit(gas, cost):\n"
            '    """Start index for a circular gas-station tour, or -1."""\n'
            "    if sum(gas) < sum(cost):\n"
            "        return -1\n"
            "    tank = start = 0\n"
            "    for i, (g, c) in enumerate(zip(gas, cost)):\n"
            "        tank += g - c\n"
            "        if tank < 0:\n"
            "            start = i + 1\n"
            "            tank = 0\n"
            "    return start\n",
            lambda low: bool(
                re.search(
                    r"\bcan[- ]?complete[- ]?circuit\b|"
                    r"\bgas[- ]?station\b|"
                    r"\bcircular (?:tour|circuit) (?:of )?gas\b|"
                    r"\bgas and cost (?:arrays?|lists?)\b",
                    low,
                )
            ),
            (
                (([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]), 3),
                (([2, 3, 4], [3, 4, 3]), -1),
            ),
        ),
        Template(
            "lru_cache",
            "def lru_cache(capacity, ops):\n"
            '    """Simulate LRU cache. ops: (get, k) or (put, k, v)."""\n'
            "    from collections import OrderedDict\n"
            "    cache = OrderedDict()\n"
            "    out = []\n"
            "    for op in ops:\n"
            "        if op[0] == 'get':\n"
            "            k = op[1]\n"
            "            if k not in cache:\n"
            "                out.append(-1)\n"
            "            else:\n"
            "                cache.move_to_end(k)\n"
            "                out.append(cache[k])\n"
            "        else:\n"
            "            k, v = op[1], op[2]\n"
            "            if k in cache:\n"
            "                cache.move_to_end(k)\n"
            "            cache[k] = v\n"
            "            if len(cache) > capacity:\n"
            "                cache.popitem(last=False)\n"
            "            out.append(None)\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\blru[- ]?cache\b|"
                    r"\bleast[- ]?recently[- ]?used cache\b|"
                    r"\bimplement(?:s|ing)? (an? )?lru\b",
                    low,
                )
            ),
            (
                (
                    (
                        2,
                        [
                            ("put", 1, 1),
                            ("put", 2, 2),
                            ("get", 1),
                            ("put", 3, 3),
                            ("get", 2),
                            ("put", 4, 4),
                            ("get", 1),
                            ("get", 3),
                            ("get", 4),
                        ],
                    ),
                    [None, None, 1, None, -1, None, -1, 3, 4],
                ),
            ),
        ),
        Template(
            "implement_trie",
            "def implement_trie(ops):\n"
            '    """Trie insert/search/startsWith. ops return results list."""\n'
            "    class Node:\n"
            "        def __init__(self):\n"
            "            self.ch = {}\n"
            "            self.end = False\n"
            "    root = Node()\n"
            "    out = []\n"
            "    for op in ops:\n"
            "        kind = op[0]\n"
            "        word = op[1]\n"
            "        if kind == 'insert':\n"
            "            n = root\n"
            "            for c in word:\n"
            "                n = n.ch.setdefault(c, Node())\n"
            "            n.end = True\n"
            "            out.append(None)\n"
            "        elif kind == 'search':\n"
            "            n = root\n"
            "            ok = True\n"
            "            for c in word:\n"
            "                if c not in n.ch:\n"
            "                    ok = False\n"
            "                    break\n"
            "                n = n.ch[c]\n"
            "            out.append(bool(ok and n.end))\n"
            "        else:\n"
            "            n = root\n"
            "            ok = True\n"
            "            for c in word:\n"
            "                if c not in n.ch:\n"
            "                    ok = False\n"
            "                    break\n"
            "                n = n.ch[c]\n"
            "            out.append(ok)\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bimplement[- ]?trie\b|"
                    r"\btrie (?:insert|search|prefix)\b|"
                    r"\bprefix[- ]?tree\b|"
                    r"\bimplement(?:s|ing)? (a )?trie\b",
                    low,
                )
            ),
            (
                (
                    (
                        [
                            ("insert", "apple"),
                            ("search", "apple"),
                            ("search", "app"),
                            ("startsWith", "app"),
                            ("insert", "app"),
                            ("search", "app"),
                        ],
                    ),
                    [None, True, False, True, None, True],
                ),
            ),
        ),
        Template(
            "network_delay_time",
            "def network_delay_time(times, n, k):\n"
            '    """Dijkstra: min time for signal from k to all n nodes, else -1."""\n'
            "    from collections import defaultdict\n"
            "    import heapq\n"
            "    g = defaultdict(list)\n"
            "    for u, v, w in times:\n"
            "        g[u].append((v, w))\n"
            "    dist = {k: 0}\n"
            "    pq = [(0, k)]\n"
            "    while pq:\n"
            "        d, u = heapq.heappop(pq)\n"
            "        if d > dist.get(u, 10**18):\n"
            "            continue\n"
            "        for v, w in g[u]:\n"
            "            nd = d + w\n"
            "            if nd < dist.get(v, 10**18):\n"
            "                dist[v] = nd\n"
            "                heapq.heappush(pq, (nd, v))\n"
            "    return max(dist.values()) if len(dist) == n else -1\n",
            lambda low: bool(
                re.search(
                    r"\bnetwork[- ]?delay\b|"
                    r"\bsignal.{0,24}\b(all nodes|every node)\b|"
                    r"\bdelay time\b.{0,16}\bnetwork\b",
                    low,
                )
            ),
            (
                (([[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2), 2),
                (([[1, 2, 1]], 2, 1), 1),
                (([[1, 2, 1]], 2, 2), -1),
            ),
        ),
        Template(
            "meeting_rooms_ii",
            "def meeting_rooms_ii(intervals):\n"
            '    """Min rooms so no two overlapping meetings share a room."""\n'
            "    import heapq\n"
            "    if not intervals:\n"
            "        return 0\n"
            "    intervals = sorted(intervals, key=lambda x: x[0])\n"
            "    rooms = []\n"
            "    for s, e in intervals:\n"
            "        if rooms and rooms[0] <= s:\n"
            "            heapq.heappop(rooms)\n"
            "        heapq.heappush(rooms, e)\n"
            "    return len(rooms)\n",
            lambda low: bool(
                re.search(
                    r"\bmeeting[- ]?rooms?(?:[- ]?ii| 2)?\b|"
                    r"\bmin(?:imum)? (?:number of )?rooms\b.{0,24}\bmeeting",
                    low,
                )
                and "merge_interval" not in low
            ),
            (
                (([[0, 30], [5, 10], [15, 20]],), 2),
                (([[7, 10], [2, 4]],), 1),
                (([],), 0),
            ),
        ),
        Template(
            "cheapest_flights",
            "def cheapest_flights(n, flights, src, dst, k):\n"
            '    """Cheapest price from src to dst with at most k stops (Bellman-Ford)."""\n'
            "    INF = 10**18\n"
            "    dist = [INF] * n\n"
            "    dist[src] = 0\n"
            "    for _ in range(k + 1):\n"
            "        nxt = dist[:]\n"
            "        for u, v, w in flights:\n"
            "            if dist[u] < INF and dist[u] + w < nxt[v]:\n"
            "                nxt[v] = dist[u] + w\n"
            "        dist = nxt\n"
            "    return -1 if dist[dst] >= INF else dist[dst]\n",
            lambda low: bool(
                re.search(
                    r"\bcheapest[- ]?flights?\b|"
                    r"\bk[- ]?stops?\b.{0,24}\bflight|"
                    r"\bflight.{0,24}\bat most k\b",
                    low,
                )
            ),
            (
                ((4, [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]], 0, 3, 1), 700),
                ((3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 1), 200),
                ((3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 0), 500),
            ),
        ),
        Template(
            "word_ladder",
            "def word_ladder(begin_word, end_word, word_list):\n"
            '    """Length of shortest word-ladder from begin to end (0 if none)."""\n'
            "    from collections import deque\n"
            "    words = set(word_list)\n"
            "    if end_word not in words:\n"
            "        return 0\n"
            "    q = deque([(begin_word, 1)])\n"
            "    seen = {begin_word}\n"
            "    while q:\n"
            "        w, d = q.popleft()\n"
            "        if w == end_word:\n"
            "            return d\n"
            "        for i in range(len(w)):\n"
            "            for c in 'abcdefghijklmnopqrstuvwxyz':\n"
            "                nw = w[:i] + c + w[i + 1:]\n"
            "                if nw in words and nw not in seen:\n"
            "                    seen.add(nw)\n"
            "                    q.append((nw, d + 1))\n"
            "    return 0\n",
            lambda low: bool(
                re.search(r"\bword[- ]?ladder\b", low)
                and "search" not in low
                and "board" not in low
            ),
            (
                (("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]), 5),
                (("hit", "cog", ["hot", "dot", "dog", "lot", "log"]), 0),
            ),
        ),
        Template(
            "count_components",
            "def count_components(n, edges):\n"
            '    """Number of connected components in an undirected graph."""\n'
            "    parent = list(range(n))\n"
            "    def find(x):\n"
            "        while parent[x] != x:\n"
            "            parent[x] = parent[parent[x]]\n"
            "            x = parent[x]\n"
            "        return x\n"
            "    for a, b in edges:\n"
            "        pa, pb = find(a), find(b)\n"
            "        if pa != pb:\n"
            "            parent[pa] = pb\n"
            "            n -= 1\n"
            "    return n\n",
            lambda low: bool(
                re.search(
                    r"\b(number|count) of connected components\b|"
                    r"\bconnected[- ]?components?\b",
                    low,
                )
                and "province" not in low
                and "island" not in low
            ),
            (
                ((5, [[0, 1], [1, 2], [3, 4]]), 2),
                ((5, [[0, 1], [1, 2], [2, 3], [3, 4]]), 1),
            ),
        ),
        Template(
            "find_itinerary",
            "def find_itinerary(tickets):\n"
            '    """Reconstruct Eulerian itinerary in lexical order (Hierholzer)."""\n'
            "    from collections import defaultdict\n"
            "    g = defaultdict(list)\n"
            "    for a, b in tickets:\n"
            "        g[a].append(b)\n"
            "    for a in g:\n"
            "        g[a].sort(reverse=True)\n"
            "    route = []\n"
            "    def dfs(u):\n"
            "        while g[u]:\n"
            "            dfs(g[u].pop())\n"
            "        route.append(u)\n"
            "    dfs('JFK')\n"
            "    return route[::-1]\n",
            lambda low: bool(
                re.search(
                    r"\breconstruct(?:s|ing)? (an? )?itinerary\b|"
                    r"\bfind(?:s|ing)? (an? )?itinerary\b|"
                    r"\beuler(?:ian)? (?:path|itinerary)\b",
                    low,
                )
            ),
            (
                (([["MUC", "LHR"], ["JFK", "MUC"], ["SFO", "SJC"], ["LHR", "SFO"]],), ["JFK", "MUC", "LHR", "SFO", "SJC"]),
                (([["JFK", "SFO"], ["JFK", "ATL"], ["SFO", "ATL"], ["ATL", "JFK"], ["ATL", "SFO"]],), ["JFK", "ATL", "JFK", "SFO", "ATL", "SFO"]),
            ),
        ),
        Template(
            "alien_dictionary",
            "def alien_dictionary(words):\n"
            '    """Alien order of letters from a sorted word list, or empty if invalid."""\n'
            "    from collections import defaultdict, deque\n"
            "    graph = defaultdict(set)\n"
            "    indeg = {c: 0 for w in words for c in w}\n"
            "    for a, b in zip(words, words[1:]):\n"
            "        if a.startswith(b) and len(a) > len(b):\n"
            "            return ''\n"
            "        for x, y in zip(a, b):\n"
            "            if x != y:\n"
            "                if y not in graph[x]:\n"
            "                    graph[x].add(y)\n"
            "                    indeg[y] += 1\n"
            "                break\n"
            "    q = deque([c for c in indeg if indeg[c] == 0])\n"
            "    order = []\n"
            "    while q:\n"
            "        c = q.popleft()\n"
            "        order.append(c)\n"
            "        for n in graph[c]:\n"
            "            indeg[n] -= 1\n"
            "            if indeg[n] == 0:\n"
            "                q.append(n)\n"
            "    return ''.join(order) if len(order) == len(indeg) else ''\n",
            lambda low: bool(
                re.search(
                    r"\balien[- ]?(dictionary|order|alphabet)\b|"
                    r"\balien language\b|"
                    r"\border of (?:the )?alien\b",
                    low,
                )
            )
            and "verify" not in low
            and "is_alien_sorted" not in low
            and "is alien sorted" not in low,
            (
                ((["wrt", "wrf", "er", "ett", "rftt"],), "wertf"),
                ((["z", "x"],), "zx"),
                ((["z", "x", "z"],), ""),
            ),
        ),
        Template(
            "accounts_merge",
            "def accounts_merge(accounts):\n"
            '    """Merge accounts that share an email (union-find)."""\n'
            "    parent = {}\n"
            "    def find(x):\n"
            "        parent.setdefault(x, x)\n"
            "        while parent[x] != x:\n"
            "            parent[x] = parent[parent[x]]\n"
            "            x = parent[x]\n"
            "        return x\n"
            "    email_name = {}\n"
            "    for acc in accounts:\n"
            "        name = acc[0]\n"
            "        if len(acc) == 1:\n"
            "            continue\n"
            "        root0 = find(acc[1])\n"
            "        for e in acc[1:]:\n"
            "            email_name[e] = name\n"
            "            parent[find(e)] = root0\n"
            "    groups = {}\n"
            "    for e in email_name:\n"
            "        groups.setdefault(find(e), []).append(e)\n"
            "    out = []\n"
            "    for root, emails in groups.items():\n"
            "        out.append([email_name[root]] + sorted(emails))\n"
            "    out.sort()\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\baccounts?[- ]?merge\b|"
                    r"\bmerge[sd]? accounts\b|"
                    r"\bmerging accounts\b|"
                    r"\bmerge (?:the )?email accounts\b",
                    low,
                )
            ),
            (
                (([["John", "j@a.com", "j@b.com"], ["John", "j@b.com", "j@c.com"], ["Mary", "m@a.com"]],),
                 [["John", "j@a.com", "j@b.com", "j@c.com"], ["Mary", "m@a.com"]]),
                (([["Alex", "a@x.com"]],), [["Alex", "a@x.com"]]),
            ),
        ),
        Template(
            "redundant_connection",
            "def redundant_connection(edges):\n"
            '    """The extra edge that creates a cycle in an undirected graph."""\n'
            "    parent = {}\n"
            "    def find(x):\n"
            "        parent.setdefault(x, x)\n"
            "        while parent[x] != x:\n"
            "            parent[x] = parent[parent[x]]\n"
            "            x = parent[x]\n"
            "        return x\n"
            "    extra = edges[-1]\n"
            "    for a, b in edges:\n"
            "        pa, pb = find(a), find(b)\n"
            "        if pa == pb:\n"
            "            extra = [a, b]\n"
            "        else:\n"
            "            parent[pa] = pb\n"
            "    return extra\n",
            lambda low: bool(
                re.search(
                    r"\bredundant[- ]?connection\b|"
                    r"\bextra edge that (?:creates|forms) a cycle\b|"
                    r"\bedge that creates a cycle\b",
                    low,
                )
            ),
            (
                (([[1, 2], [1, 3], [2, 3]],), [2, 3]),
                (([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]],), [1, 4]),
            ),
        ),
        Template(
            "valid_tree",
            "def valid_tree(n, edges):\n"
            '    """True iff undirected edges form a tree on n nodes."""\n'
            "    if len(edges) != n - 1:\n"
            "        return False\n"
            "    parent = list(range(n))\n"
            "    def find(x):\n"
            "        while parent[x] != x:\n"
            "            parent[x] = parent[parent[x]]\n"
            "            x = parent[x]\n"
            "        return x\n"
            "    for a, b in edges:\n"
            "        pa, pb = find(a), find(b)\n"
            "        if pa == pb:\n"
            "            return False\n"
            "        parent[pa] = pb\n"
            "    return True\n",
            lambda low: bool(
                re.search(
                    r"\bgraph valid tree\b|"
                    r"\bvalid tree\b|"
                    r"\b(is|check) (?:an? )?(?:undirected )?graph (?:a )?tree\b|"
                    r"\bforms? a tree\b",
                    low,
                )
                and "binary" not in low
                and "bst" not in low
            ),
            (
                ((5, [[0, 1], [0, 2], [0, 3], [1, 4]]), True),
                ((5, [[0, 1], [1, 2], [2, 3], [1, 3], [1, 4]]), False),
            ),
        ),
        Template(
            "min_height_trees",
            "def min_height_trees(n, edges):\n"
            '    """Roots of minimum-height trees (peel leaves)."""\n'
            "    from collections import defaultdict, deque\n"
            "    if n <= 2:\n"
            "        return list(range(n))\n"
            "    g = defaultdict(set)\n"
            "    for a, b in edges:\n"
            "        g[a].add(b)\n"
            "        g[b].add(a)\n"
            "    leaves = deque([i for i in range(n) if len(g[i]) <= 1])\n"
            "    remain = n\n"
            "    while remain > 2:\n"
            "        sz = len(leaves)\n"
            "        remain -= sz\n"
            "        for _ in range(sz):\n"
            "            leaf = leaves.popleft()\n"
            "            for nb in list(g[leaf]):\n"
            "                g[nb].discard(leaf)\n"
            "                if len(g[nb]) == 1:\n"
            "                    leaves.append(nb)\n"
            "    return sorted(leaves)\n",
            lambda low: bool(
                re.search(
                    r"\bmin(?:imum)?[- ]?height[- ]?trees?\b|"
                    r"\bmht\b|"
                    r"\broots? of (?:the )?minimum height\b",
                    low,
                )
            ),
            (
                ((4, [[1, 0], [1, 2], [1, 3]]), [1]),
                ((6, [[3, 0], [3, 1], [3, 2], [3, 4], [5, 4]]), [3, 4]),
            ),
        ),
        Template(
            "critical_connections",
            "def critical_connections(n, connections):\n"
            '    """Bridges in an undirected graph (Tarjan)."""\n'
            "    from collections import defaultdict\n"
            "    g = defaultdict(list)\n"
            "    for a, b in connections:\n"
            "        g[a].append(b)\n"
            "        g[b].append(a)\n"
            "    disc = [-1] * n\n"
            "    low = [-1] * n\n"
            "    bridges = []\n"
            "    time = [0]\n"
            "    def dfs(u, parent):\n"
            "        disc[u] = low[u] = time[0]\n"
            "        time[0] += 1\n"
            "        for v in g[u]:\n"
            "            if v == parent:\n"
            "                continue\n"
            "            if disc[v] == -1:\n"
            "                dfs(v, u)\n"
            "                low[u] = min(low[u], low[v])\n"
            "                if low[v] > disc[u]:\n"
            "                    bridges.append([u, v])\n"
            "            else:\n"
            "                low[u] = min(low[u], disc[v])\n"
            "    for i in range(n):\n"
            "        if disc[i] == -1:\n"
            "            dfs(i, -1)\n"
            "    return bridges\n",
            lambda low: bool(
                re.search(
                    r"\bcritical[- ]?connections?\b|"
                    r"\bcritical edges?\b|"
                    r"\bbridges? in (?:an? )?(?:undirected )?graph\b|"
                    r"\btarjan(?:'s)? bridges?\b",
                    low,
                )
            ),
            (
                ((4, [[0, 1], [1, 2], [2, 0], [1, 3]]), [[1, 3]]),
                ((2, [[0, 1]]), [[0, 1]]),
            ),
        ),
        Template(
            "build_tree",
            "def build_tree(preorder, inorder):\n"
            '    """Build a binary tree [val, left, right] from preorder + inorder."""\n'
            "    idx = {v: i for i, v in enumerate(inorder)}\n"
            "    def rec(plo, phi, ilo, ihi):\n"
            "        if plo > phi:\n"
            "            return None\n"
            "        val = preorder[plo]\n"
            "        mid = idx[val]\n"
            "        left_n = mid - ilo\n"
            "        return [\n"
            "            val,\n"
            "            rec(plo + 1, plo + left_n, ilo, mid - 1),\n"
            "            rec(plo + left_n + 1, phi, mid + 1, ihi),\n"
            "        ]\n"
            "    n = len(preorder)\n"
            "    return rec(0, n - 1, 0, n - 1)\n",
            lambda low: bool(
                "binary tree" in low
                and re.search(r"\b(preorder|pre-order)\b", low)
                and re.search(r"\b(inorder|in-order)\b", low)
            )
            or bool(re.search(r"\bbuild(?:s|ing)?[- ]?tree\b.{0,40}\bpreorder\b", low)),
            (
                (([3, 9, 20, 15, 7], [9, 3, 15, 20, 7]), [3, [9, None, None], [20, [15, None, None], [7, None, None]]]),
                (([1, 2], [2, 1]), [1, [2, None, None], None]),
            ),
        ),
        Template(
            "house_robber_iii",
            "def house_robber_iii(root):\n"
            '    """Max rob on a binary tree ([val, left, right]) without adjacent nodes."""\n'
            "    def dfs(node):\n"
            "        if node is None:\n"
            "            return (0, 0)\n"
            "        if not isinstance(node, (list, tuple)):\n"
            "            return (int(node), 0)\n"
            "        val = int(node[0])\n"
            "        left = node[1] if len(node) > 1 else None\n"
            "        right = node[2] if len(node) > 2 else None\n"
            "        lr, ln = dfs(left)\n"
            "        rr, rn = dfs(right)\n"
            "        take = val + ln + rn\n"
            "        skip = max(lr, ln) + max(rr, rn)\n"
            "        return (take, skip)\n"
            "    t, s = dfs(root)\n"
            "    return max(t, s)\n",
            lambda low: bool(
                re.search(r"\bhouse[- ]?robber(?:s)?[- ]?(iii|3|three)\b", low)
                or (
                    "robber" in low
                    and "tree" in low
                    and "ii" not in low.replace("iii", "")
                )
            ),
            (
                (([3, [2, None, [3, None, None]], [3, None, [1, None, None]]],), 7),
                (([3, [4, [1, None, None], [3, None, None]], [5, None, [1, None, None]]],), 9),
            ),
        ),
        Template(
            "longest_increasing_path",
            "def longest_increasing_path(matrix):\n"
            '    """Longest strictly increasing path in a matrix."""\n'
            "    if not matrix or not matrix[0]:\n"
            "        return 0\n"
            "    rows, cols = len(matrix), len(matrix[0])\n"
            "    memo = [[0] * cols for _ in range(rows)]\n"
            "    def dfs(r, c):\n"
            "        if memo[r][c]:\n"
            "            return memo[r][c]\n"
            "        best = 1\n"
            "        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):\n"
            "            nr, nc = r + dr, c + dc\n"
            "            if 0 <= nr < rows and 0 <= nc < cols and matrix[nr][nc] > matrix[r][c]:\n"
            "                best = max(best, 1 + dfs(nr, nc))\n"
            "        memo[r][c] = best\n"
            "        return best\n"
            "    return max(dfs(r, c) for r in range(rows) for c in range(cols))\n",
            lambda low: bool(
                re.search(
                    r"\blongest[- ]?increasing[- ]?path\b|"
                    r"\bincreasing path in (?:a )?matrix\b",
                    low,
                )
            ),
            (
                (([[9, 9, 4], [6, 6, 8], [2, 1, 1]],), 4),
                (([[3, 4, 5], [3, 2, 6], [2, 2, 1]],), 4),
            ),
        ),
        Template(
            "word_break_ii",
            "def word_break_ii(s, word_dict):\n"
            '    """All sentences formed by breaking s with words from word_dict."""\n'
            "    words = set(word_dict)\n"
            "    memo = {}\n"
            "    def dfs(i):\n"
            "        if i == len(s):\n"
            "            return ['']\n"
            "        if i in memo:\n"
            "            return memo[i]\n"
            "        out = []\n"
            "        for j in range(i + 1, len(s) + 1):\n"
            "            w = s[i:j]\n"
            "            if w in words:\n"
            "                for tail in dfs(j):\n"
            "                    out.append(w if not tail else w + ' ' + tail)\n"
            "        memo[i] = out\n"
            "        return out\n"
            "    return sorted(dfs(0))\n",
            lambda low: bool(
                re.search(r"\bword[- ]?break[- ]?(ii|2|two)\b", low)
                or (
                    "word break" in low
                    and re.search(r"\b(all|every|sentences?)\b", low)
                )
            ),
            (
                (("catsanddog", ["cat", "cats", "and", "sand", "dog"]), ["cat sand dog", "cats and dog"]),
                (("pineapplepenapple", ["apple", "pen", "applepen", "pine", "pineapple"]),
                 ["pine apple pen apple", "pine applepen apple", "pineapple pen apple"]),
            ),
        ),
        Template(
            "min_cost_connect_points",
            "def min_cost_connect_points(points):\n"
            '    """MST cost connecting points with Manhattan distance (Prim)."""\n'
            "    n = len(points)\n"
            "    if n <= 1:\n"
            "        return 0\n"
            "    in_mst = [False] * n\n"
            "    dist = [10**18] * n\n"
            "    dist[0] = 0\n"
            "    total = 0\n"
            "    for _ in range(n):\n"
            "        u = -1\n"
            "        best = 10**18\n"
            "        for i in range(n):\n"
            "            if not in_mst[i] and dist[i] < best:\n"
            "                best = dist[i]\n"
            "                u = i\n"
            "        in_mst[u] = True\n"
            "        total += 0 if best >= 10**18 else best\n"
            "        ux, uy = points[u]\n"
            "        for v in range(n):\n"
            "            if in_mst[v]:\n"
            "                continue\n"
            "            vx, vy = points[v]\n"
            "            d = abs(ux - vx) + abs(uy - vy)\n"
            "            if d < dist[v]:\n"
            "                dist[v] = d\n"
            "    return total\n",
            lambda low: bool(
                re.search(
                    r"\bmin(?:imum)?[- ]?cost[- ]?connect(?:ing)?[- ]?points\b|"
                    r"\bconnect(?:s|ing)? (?:all )?points\b|"
                    r"\bpoints\b.{0,32}\bmin(?:imum)? cost\b|"
                    r"\bprim(?:'s)? .{0,16}points\b",
                    low,
                )
            ),
            (
                (([[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]],), 20),
                (([[3, 12], [-2, 5], [-4, 1]],), 18),
            ),
        ),
        Template(
            "num_trees",
            "def num_trees(n):\n"
            '    """Number of unique BSTs with n distinct keys (Catalan)."""\n'
            "    n = int(n)\n"
            "    dp = [0] * (n + 1)\n"
            "    dp[0] = 1\n"
            "    for nodes in range(1, n + 1):\n"
            "        for root in range(1, nodes + 1):\n"
            "            dp[nodes] += dp[root - 1] * dp[nodes - root]\n"
            "    return dp[n]\n",
            lambda low: bool(
                re.search(
                    r"\bunique[- ]?binary[- ]?search[- ]?trees\b|"
                    r"\bnum(?:ber of)?[- ]?trees\b|"
                    r"\bcount(?:s|ing)? unique bst\b|"
                    r"\bcatalan\b.{0,16}\bbst\b",
                    low,
                )
            ),
            (((3,), 5), ((1,), 1), ((4,), 14)),
        ),
        Template(
            "find_median_sorted_arrays",
            "def find_median_sorted_arrays(nums1, nums2):\n"
            '    """Median of two sorted arrays in O(log(m+n)) via binary partition."""\n'
            "    a, b = list(nums1), list(nums2)\n"
            "    if len(a) > len(b):\n"
            "        a, b = b, a\n"
            "    m, n = len(a), len(b)\n"
            "    lo, hi = 0, m\n"
            "    half = (m + n + 1) // 2\n"
            "    while lo <= hi:\n"
            "        i = (lo + hi) // 2\n"
            "        j = half - i\n"
            "        a_left = a[i - 1] if i else -10**18\n"
            "        a_right = a[i] if i < m else 10**18\n"
            "        b_left = b[j - 1] if j else -10**18\n"
            "        b_right = b[j] if j < n else 10**18\n"
            "        if a_left <= b_right and b_left <= a_right:\n"
            "            if (m + n) % 2:\n"
            "                return float(max(a_left, b_left))\n"
            "            return (max(a_left, b_left) + min(a_right, b_right)) / 2.0\n"
            "        if a_left > b_right:\n"
            "            hi = i - 1\n"
            "        else:\n"
            "            lo = i + 1\n"
            "    return 0.0\n",
            lambda low: bool(
                re.search(
                    r"\bmedian of two sorted arrays\b|"
                    r"\bfind[- ]?median[- ]?sorted[- ]?arrays\b|"
                    r"\bmedian\b.{0,24}\btwo sorted arrays\b",
                    low,
                )
            ),
            (
                (([1, 3], [2]), 2.0),
                (([1, 2], [3, 4]), 2.5),
                (([], [1]), 1.0),
            ),
        ),
        Template(
            "largest_rectangle_histogram",
            "def largest_rectangle_histogram(heights):\n"
            '    """Largest rectangle area in a histogram (monotonic stack)."""\n'
            "    heights = list(heights) + [0]\n"
            "    stack = []\n"
            "    best = 0\n"
            "    for i, h in enumerate(heights):\n"
            "        while stack and heights[stack[-1]] > h:\n"
            "            height = heights[stack.pop()]\n"
            "            width = i if not stack else i - stack[-1] - 1\n"
            "            best = max(best, height * width)\n"
            "        stack.append(i)\n"
            "    return best\n",
            lambda low: bool(
                re.search(
                    r"\blargest[- ]?rectangle(?:[- ]?area)?\b.{0,24}\bhistogram\b|"
                    r"\bhistogram\b.{0,24}\blargest[- ]?rectangle\b|"
                    r"\blargest[- ]?rectangle[- ]?in[- ]?histogram\b",
                    low,
                )
            ),
            ((((2, 1, 5, 6, 2, 3),), 10), (((2, 4),), 4), (([],), 0)),
        ),
        Template(
            "maximal_rectangle",
            "def maximal_rectangle(matrix):\n"
            '    """Maximal rectangle of 1s in a binary matrix via histogram DP."""\n'
            "    if not matrix or not matrix[0]:\n"
            "        return 0\n"
            "    cols = len(matrix[0])\n"
            "    height = [0] * cols\n"
            "    best = 0\n"
            "    for row in matrix:\n"
            "        for j, val in enumerate(row):\n"
            "            bit = val == 1 or val == '1' or val is True\n"
            "            height[j] = height[j] + 1 if bit else 0\n"
            "        stack = []\n"
            "        ext = height + [0]\n"
            "        for i, h in enumerate(ext):\n"
            "            while stack and ext[stack[-1]] > h:\n"
            "                hh = ext[stack.pop()]\n"
            "                w = i if not stack else i - stack[-1] - 1\n"
            "                best = max(best, hh * w)\n"
            "            stack.append(i)\n"
            "    return best\n",
            lambda low: bool(
                re.search(
                    r"\bmaximal[- ]?rectangle\b|"
                    r"\bmax(?:imum)? rectangle of 1s\b|"
                    r"\blargest rectangle\b.{0,20}\bbinary matrix\b",
                    low,
                )
                and not re.search(r"\bhistogram\b", low)
            ),
            (
                (([["1", "0", "1", "0", "0"], ["1", "0", "1", "1", "1"], ["1", "1", "1", "1", "1"], ["1", "0", "0", "1", "0"]],), 6),
                (([["0"]],), 0),
                (([["1"]],), 1),
            ),
        ),
        Template(
            "candy",
            "def candy(ratings):\n"
            '    """Min candies so neighbors with higher rating get more."""\n'
            "    ratings = list(ratings)\n"
            "    n = len(ratings)\n"
            "    if n == 0:\n"
            "        return 0\n"
            "    give = [1] * n\n"
            "    for i in range(1, n):\n"
            "        if ratings[i] > ratings[i - 1]:\n"
            "            give[i] = give[i - 1] + 1\n"
            "    for i in range(n - 2, -1, -1):\n"
            "        if ratings[i] > ratings[i + 1]:\n"
            "            give[i] = max(give[i], give[i + 1] + 1)\n"
            "    return sum(give)\n",
            lambda low: bool(
                re.search(
                    r"\bcandy\b.{0,24}\bratings?\b|"
                    r"\bratings?\b.{0,24}\bcand(?:y|ies)\b|"
                    r"\bdistribute cand(?:y|ies)\b",
                    low,
                )
                and "kids" not in low
                and "among children" not in low
                and "2928" not in low
                and "greatest number of candies" not in low
                and "among children" not in low
                and "limit" not in low
            ),
            ((((1, 0, 2),), 5), (((1, 2, 2),), 4), (([],), 0)),
        ),
        Template(
            "longest_valid_parentheses",
            "def longest_valid_parentheses(s):\n"
            '    """Length of the longest well-formed parentheses substring."""\n'
            "    s = str(s)\n"
            "    stack = [-1]\n"
            "    best = 0\n"
            "    for i, ch in enumerate(s):\n"
            "        if ch == '(':\n"
            "            stack.append(i)\n"
            "        else:\n"
            "            stack.pop()\n"
            "            if not stack:\n"
            "                stack.append(i)\n"
            "            else:\n"
            "                best = max(best, i - stack[-1])\n"
            "    return best\n",
            lambda low: bool(
                re.search(
                    r"\blongest[- ]?valid[- ]?parentheses\b|"
                    r"\blongest\b.{0,16}\bvalid parentheses\b|"
                    r"\blongest well[- ]?formed parentheses\b",
                    low,
                )
            ),
            ((("(()",), 2), ((")()())",), 4), (("",), 0)),
        ),
        Template(
            "is_interleave",
            "def is_interleave(s1, s2, s3):\n"
            '    """Whether s3 is an interleaving of s1 and s2 (DP)."""\n'
            "    a, b, c = str(s1), str(s2), str(s3)\n"
            "    n, m = len(a), len(b)\n"
            "    if n + m != len(c):\n"
            "        return False\n"
            "    dp = [False] * (m + 1)\n"
            "    dp[0] = True\n"
            "    for j in range(1, m + 1):\n"
            "        dp[j] = dp[j - 1] and b[j - 1] == c[j - 1]\n"
            "    for i in range(1, n + 1):\n"
            "        dp[0] = dp[0] and a[i - 1] == c[i - 1]\n"
            "        for j in range(1, m + 1):\n"
            "            dp[j] = (dp[j] and a[i - 1] == c[i + j - 1]) or (\n"
            "                dp[j - 1] and b[j - 1] == c[i + j - 1]\n"
            "            )\n"
            "    return bool(dp[m])\n",
            lambda low: bool(
                re.search(
                    r"\binterleaving[- ]?string\b|"
                    r"\bis[- ]?interleave\b|"
                    r"\binterleave(?:s|d)?\b.{0,24}\bstrings?\b|"
                    r"\bwhether .{0,24}interleaving\b",
                    low,
                )
            ),
            (
                (("aabcc", "dbbca", "aadbbcbcac"), True),
                (("aabcc", "dbbca", "aadbbbaccc"), False),
                (("", "", ""), True),
            ),
        ),
        Template(
            "burst_balloons",
            "def burst_balloons(nums):\n"
            '    """Max coins from bursting balloons (LeetCode 312)."""\n'
            "    a = [1] + [int(x) for x in nums] + [1]\n"
            "    n = len(a)\n"
            "    dp = [[0] * n for _ in range(n)]\n"
            "    for length in range(2, n):\n"
            "        for i in range(0, n - length):\n"
            "            j = i + length\n"
            "            best = 0\n"
            "            for k in range(i + 1, j):\n"
            "                best = max(best, a[i] * a[k] * a[j] + dp[i][k] + dp[k][j])\n"
            "            dp[i][j] = best\n"
            "    return dp[0][n - 1]\n",
            lambda low: "arrow" not in low and bool(
                re.search(
                    r"\bburst[- ]?balloons?\b|"
                    r"\bbursts? balloons\b|"
                    r"\bburst(?:ing)? balloons\b|"
                    r"\bmax(?:imum)? coins\b.{0,24}\bballoons?\b",
                    low,
                )
            ),
            ((((3, 1, 5, 8),), 167), (((1, 5),), 10), (([],), 0)),
        ),
        Template(
            "word_search_ii",
            "def word_search_ii(board, words):\n"
            '    """Find all words from a list on the board (LeetCode 212)."""\n'
            "    board = [list(row) for row in board]\n"
            "    words = list(words)\n"
            "    if not board or not board[0] or not words:\n"
            "        return []\n"
            "    trie = {}\n"
            "    for w in words:\n"
            "        node = trie\n"
            "        for ch in str(w):\n"
            "            node = node.setdefault(ch, {})\n"
            "        node['#'] = str(w)\n"
            "    m, n = len(board), len(board[0])\n"
            "    found = []\n"
            "\n"
            "    def dfs(i, j, node):\n"
            "        ch = board[i][j]\n"
            "        nxt = node.get(ch)\n"
            "        if not nxt:\n"
            "            return\n"
            "        word = nxt.pop('#', None)\n"
            "        if word is not None:\n"
            "            found.append(word)\n"
            "        board[i][j] = '#'\n"
            "        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):\n"
            "            ni, nj = i + di, j + dj\n"
            "            if 0 <= ni < m and 0 <= nj < n and board[ni][nj] != '#':\n"
            "                dfs(ni, nj, nxt)\n"
            "        board[i][j] = ch\n"
            "        if not nxt:\n"
            "            node.pop(ch, None)\n"
            "\n"
            "    for r in range(m):\n"
            "        for c in range(n):\n"
            "            dfs(r, c, trie)\n"
            "    return found\n",
            lambda low: bool(
                re.search(
                    r"\bword[- ]?search[- _]*(ii|2)\b|"
                    r"\bwords? from a board\b|"
                    r"\bfind all words\b.{0,20}\bboard\b",
                    low,
                )
            ),
            (
                (
                    (
                        [["o", "a", "a", "n"], ["e", "t", "a", "e"], ["i", "h", "k", "r"], ["i", "f", "l", "v"]],
                        ["oath", "pea", "eat", "rain"],
                    ),
                    ["oath", "eat"],
                ),
                (([["a", "b"], ["c", "d"]], ["abcb"]), []),
            ),
        ),
        Template(
            "palindrome_partition",
            "def palindrome_partition(s):\n"
            '    """Partition s so every substring is a palindrome."""\n'
            "    s = str(s)\n"
            "    n = len(s)\n"
            "    ok = [[False] * n for _ in range(n)]\n"
            "    for i in range(n - 1, -1, -1):\n"
            "        for j in range(i, n):\n"
            "            ok[i][j] = s[i] == s[j] and (j - i < 2 or ok[i + 1][j - 1])\n"
            "    out = []\n"
            "\n"
            "    def dfs(i, path):\n"
            "        if i == n:\n"
            "            out.append(list(path))\n"
            "            return\n"
            "        for j in range(i, n):\n"
            "            if ok[i][j]:\n"
            "                path.append(s[i : j + 1])\n"
            "                dfs(j + 1, path)\n"
            "                path.pop()\n"
            "\n"
            "    dfs(0, [])\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bpalindrome[- ]?partition(?:ing)?\b|"
                    r"\bpartition(?:s|ing)? .{0,16}palindrome\b",
                    low,
                )
            )
            and "linked" not in low,
            ((("aab",), [["a", "a", "b"], ["aa", "b"]]), (("a",), [["a"]])),
        ),
        Template(
            "serialize_tree",
            "def serialize_tree(root):\n"
            '    """Serialize a [val, left, right] binary tree (level order)."""\n'
            "    if root is None:\n"
            "        return 'null'\n"
            "    from collections import deque\n"
            "    q = deque([root])\n"
            "    parts = []\n"
            "    while q:\n"
            "        node = q.popleft()\n"
            "        if node is None:\n"
            "            parts.append('null')\n"
            "            continue\n"
            "        parts.append(str(node[0]))\n"
            "        left = node[1] if len(node) > 1 else None\n"
            "        right = node[2] if len(node) > 2 else None\n"
            "        q.append(left)\n"
            "        q.append(right)\n"
            "    while parts and parts[-1] == 'null':\n"
            "        parts.pop()\n"
            "    return ','.join(parts)\n",
            lambda low: bool(
                re.search(
                    r"\bserialize(?:s|d)? (a )?binary tree\b|"
                    r"\bserialize_tree\b|"
                    r"\btree serialization\b",
                    low,
                )
            ),
            ((([1, [2, None, None], [3, None, None]],), "1,2,3"), ((None,), "null")),
        ),
        Template(
            "count_smaller",
            "def count_smaller(nums):\n"
            '    """Counts of smaller numbers after self (merge sort)."""\n'
            "    a = list(nums)\n"
            "    n = len(a)\n"
            "    ans = [0] * n\n"
            "    idx = list(range(n))\n"
            "\n"
            "    def merge(lo, hi):\n"
            "        if hi - lo <= 1:\n"
            "            return\n"
            "        mid = (lo + hi) // 2\n"
            "        merge(lo, mid)\n"
            "        merge(mid, hi)\n"
            "        tmp = []\n"
            "        i, j = lo, mid\n"
            "        right_taken = 0\n"
            "        while i < mid or j < hi:\n"
            "            if j == hi or (i < mid and a[idx[i]] <= a[idx[j]]):\n"
            "                ans[idx[i]] += right_taken\n"
            "                tmp.append(idx[i])\n"
            "                i += 1\n"
            "            else:\n"
            "                right_taken += 1\n"
            "                tmp.append(idx[j])\n"
            "                j += 1\n"
            "        idx[lo:hi] = tmp\n"
            "\n"
            "    merge(0, n)\n"
            "    return ans\n",
            lambda low: bool(
                re.search(
                    r"\bcount(?:s)? of smaller numbers after self\b|"
                    r"\bcount_smaller\b|"
                    r"\bsmaller numbers after self\b",
                    low,
                )
            ),
            ((((5, 2, 6, 1),), [2, 1, 1, 0]), (([],), [])),
        ),
        Template(
            "max_profit_cooldown",
            "def max_profit_cooldown(prices):\n"
            '    """Best time to buy/sell stock with cooldown."""\n'
            "    hold = float('-inf')\n"
            "    sold = 0\n"
            "    rest = 0\n"
            "    for p in prices:\n"
            "        p = int(p)\n"
            "        hold, sold, rest = max(hold, rest - p), hold + p, max(rest, sold)\n"
            "    return max(sold, rest)\n",
            lambda low: bool(
                re.search(
                    r"\bbuy(?:/| and )sell stock.{0,16}cooldown\b|"
                    r"\bmax_profit_cooldown\b|"
                    r"\bstock.{0,16}cooldown\b|"
                    r"\bcooldown\b.{0,16}\bstock\b",
                    low,
                )
            ),
            ((((1, 2, 3, 0, 2),), 3), (((1,),), 0)),
        ),
        Template(
            "four_sum",
            "def four_sum(nums, target):\n"
            '    """Unique quadruplets that sum to target, sorted."""\n'
            "    nums = sorted(int(x) for x in nums)\n"
            "    n = len(nums)\n"
            "    target = int(target)\n"
            "    out = []\n"
            "    for i in range(n):\n"
            "        if i and nums[i] == nums[i - 1]:\n"
            "            continue\n"
            "        for j in range(i + 1, n):\n"
            "            if j > i + 1 and nums[j] == nums[j - 1]:\n"
            "                continue\n"
            "            lo, hi = j + 1, n - 1\n"
            "            while lo < hi:\n"
            "                s = nums[i] + nums[j] + nums[lo] + nums[hi]\n"
            "                if s == target:\n"
            "                    out.append([nums[i], nums[j], nums[lo], nums[hi]])\n"
            "                    lo += 1\n"
            "                    hi -= 1\n"
            "                    while lo < hi and nums[lo] == nums[lo - 1]:\n"
            "                        lo += 1\n"
            "                    while lo < hi and nums[hi] == nums[hi + 1]:\n"
            "                        hi -= 1\n"
            "                elif s < target:\n"
            "                    lo += 1\n"
            "                else:\n"
            "                    hi -= 1\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bfour[- ]?sum\b|"
                    r"\b4[- ]?sum\b|"
                    r"\bquadruplets? that sum\b",
                    low,
                )
            ),
            (
                (([1, 0, -1, 0, -2, 2], 0), [[-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]]),
                (([2, 2, 2, 2, 2], 8), [[2, 2, 2, 2]]),
            ),
        ),
        Template(
            "three_sum_closest",
            "def three_sum_closest(nums, target):\n"
            '    """Triplet sum closest to target."""\n'
            "    nums = sorted(int(x) for x in nums)\n"
            "    target = int(target)\n"
            "    n = len(nums)\n"
            "    best = nums[0] + nums[1] + nums[2]\n"
            "    for i in range(n - 2):\n"
            "        lo, hi = i + 1, n - 1\n"
            "        while lo < hi:\n"
            "            s = nums[i] + nums[lo] + nums[hi]\n"
            "            if abs(s - target) < abs(best - target):\n"
            "                best = s\n"
            "            if s < target:\n"
            "                lo += 1\n"
            "            elif s > target:\n"
            "                hi -= 1\n"
            "            else:\n"
            "                return s\n"
            "    return best\n",
            lambda low: bool(
                re.search(
                    r"\bthree[- ]?sum closest\b|"
                    r"\b3[- ]?sum closest\b|"
                    r"\bclosest.{0,12}triplet\b|"
                    r"\bthree_sum_closest\b",
                    low,
                )
            ),
            ((([-1, 2, 1, -4], 1), 2), (([0, 0, 0], 1), 0)),
        ),
        Template(
            "find_min_rotated",
            "def find_min_rotated(nums):\n"
            '    """Minimum in a rotated sorted array with unique values."""\n'
            "    nums = list(nums)\n"
            "    lo, hi = 0, len(nums) - 1\n"
            "    while lo < hi:\n"
            "        mid = (lo + hi) // 2\n"
            "        if nums[mid] > nums[hi]:\n"
            "            lo = mid + 1\n"
            "        else:\n"
            "            hi = mid\n"
            "    return nums[lo]\n",
            lambda low: bool(
                re.search(
                    r"\bfind[_ ]min(?:imum)? (?:in )?(?:a )?rotated\b|"
                    r"\bminimum in (?:a )?rotated sorted\b|"
                    r"\bfind_min_rotated\b|"
                    r"\bsmallest (?:element )?in (?:a )?rotated\b",
                    low,
                )
            ),
            ((((3, 4, 5, 1, 2),), 1), (((4, 5, 6, 7, 0, 1, 2),), 0), (((11, 13, 15, 17),), 11)),
        ),
        Template(
            "perfect_squares",
            "def perfect_squares(n):\n"
            '    """Fewest perfect-square numbers that sum to n."""\n'
            "    n = int(n)\n"
            "    dp = [0] + [n + 1] * n\n"
            "    for i in range(1, n + 1):\n"
            "        k = 1\n"
            "        while k * k <= i:\n"
            "            dp[i] = min(dp[i], dp[i - k * k] + 1)\n"
            "            k += 1\n"
            "    return dp[n]\n",
            lambda low: (
                bool(
                    re.search(
                        r"\bfewest.{0,16}square\b|"
                        r"\bperfect_squares\b|"
                        r"\bnum squares?\b|"
                        r"\bsquares? that sum\b",
                        low,
                    )
                )
                or (
                    bool(re.search(r"\bperfect squares\b", low))
                    and not re.search(r"\bis (?:a )?perfect square\b", low)
                )
            ),
            (((12,), 3), ((13,), 2), ((1,), 1)),
        ),
        Template(
            "count_bits",
            "def count_bits(n):\n"
            '    """Number of 1-bits for every integer in [0, n]."""\n'
            "    n = int(n)\n"
            "    ans = [0] * (n + 1)\n"
            "    for i in range(1, n + 1):\n"
            "        ans[i] = ans[i >> 1] + (i & 1)\n"
            "    return ans\n",
            lambda low: bool(
                re.search(
                    r"\bcount_bits\b|"
                    r"\bcounting bits\b|"
                    r"\bcount bits(?: for every| 0 to)\b|"
                    r"\bnumber of 1[- ]?bits for every\b|"
                    r"\bhamming weights?\s+(?:for|of) every\b",
                    low,
                )
                and "hamming weight" not in low
            ),
            (((2,), [0, 1, 1]), ((5,), [0, 1, 1, 2, 1, 2])),
        ),
        Template(
            "subsets_ii",
            "def subsets_ii(nums):\n"
            '    """Unique subsets when nums may contain duplicates."""\n'
            "    nums = sorted(int(x) for x in nums)\n"
            "    out = []\n"
            "    path = []\n"
            "\n"
            "    def dfs(i):\n"
            "        if i == len(nums):\n"
            "            out.append(list(path))\n"
            "            return\n"
            "        path.append(nums[i])\n"
            "        dfs(i + 1)\n"
            "        path.pop()\n"
            "        j = i + 1\n"
            "        while j < len(nums) and nums[j] == nums[i]:\n"
            "            j += 1\n"
            "        dfs(j)\n"
            "\n"
            "    dfs(0)\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bsubsets[_ ]ii\b|"
                    r"\bsubsets with dup(?:licate)?s?\b|"
                    r"\bunique subsets\b",
                    low,
                )
            ),
            (
                (([1, 2, 2],), [[1, 2, 2], [1, 2], [1], [2, 2], [2], []]),
                (([0],), [[0], []]),
            ),
        ),
        Template(
            "wildcard_matching",
            "def wildcard_matching(s, p):\n"
            '    """Return True if s matches wildcard pattern p (? = one, * = any)."""\n'
            "    n, m = len(s), len(p)\n"
            "    dp = [False] * (m + 1)\n"
            "    dp[0] = True\n"
            "    for j in range(1, m + 1):\n"
            "        if p[j - 1] == '*':\n"
            "            dp[j] = dp[j - 1]\n"
            "    for i in range(1, n + 1):\n"
            "        nxt = [False] * (m + 1)\n"
            "        for j in range(1, m + 1):\n"
            "            if p[j - 1] == '*':\n"
            "                nxt[j] = nxt[j - 1] or dp[j]\n"
            "            elif p[j - 1] == '?' or p[j - 1] == s[i - 1]:\n"
            "                nxt[j] = dp[j - 1]\n"
            "        dp = nxt\n"
            "    return dp[m]\n",
            lambda low: bool(
                re.search(r"\bwildcard matching\b|\bwildcard pattern\b", low)
                and "regular" not in low
                and "regex" not in low
            ),
            ((("aa", "a"), False), (("aa", "*"), True), (("adceb", "*a*b"), True)),
        ),
        Template(
            "regex_matching",
            "def regex_matching(s, p):\n"
            '    """Return True if s matches regex pattern p (. = one, * = prev)."""\n'
            "    n, m = len(s), len(p)\n"
            "    dp = [[False] * (m + 1) for _ in range(n + 1)]\n"
            "    dp[0][0] = True\n"
            "    for j in range(2, m + 1):\n"
            "        if p[j - 1] == '*':\n"
            "            dp[0][j] = dp[0][j - 2]\n"
            "    for i in range(1, n + 1):\n"
            "        for j in range(1, m + 1):\n"
            "            if p[j - 1] == '.' or p[j - 1] == s[i - 1]:\n"
            "                dp[i][j] = dp[i - 1][j - 1]\n"
            "            elif p[j - 1] == '*':\n"
            "                dp[i][j] = dp[i][j - 2]\n"
            "                if p[j - 2] == '.' or p[j - 2] == s[i - 1]:\n"
            "                    dp[i][j] = dp[i][j] or dp[i - 1][j]\n"
            "    return dp[n][m]\n",
            lambda low: bool(
                re.search(r"\bregular expression matching\b|\bregex matching\b", low)
            ),
            ((("aa", "a"), False), (("aa", "a*"), True), (("ab", ".*"), True)),
        ),
        Template(
            "distinct_subsequences",
            "def distinct_subsequences(s, t):\n"
            '    """Return how many subsequences of s equal t."""\n'
            "    n, m = len(s), len(t)\n"
            "    dp = [0] * (m + 1)\n"
            "    dp[0] = 1\n"
            "    for i in range(1, n + 1):\n"
            "        for j in range(m, 0, -1):\n"
            "            if s[i - 1] == t[j - 1]:\n"
            "                dp[j] += dp[j - 1]\n"
            "    return dp[m]\n",
            lambda low: bool(re.search(r"\bdistinct subsequences?\b", low)),
            ((("rabbbit", "rabbit"), 3), (("babgbag", "bag"), 5)),
        ),
        Template(
            "longest_common_subsequence",
            "def longest_common_subsequence(text1, text2):\n"
            '    """Return the length of the LCS of text1 and text2."""\n'
            "    n, m = len(text1), len(text2)\n"
            "    dp = [0] * (m + 1)\n"
            "    for i in range(1, n + 1):\n"
            "        prev = 0\n"
            "        for j in range(1, m + 1):\n"
            "            cur = dp[j]\n"
            "            if text1[i - 1] == text2[j - 1]:\n"
            "                dp[j] = prev + 1\n"
            "            else:\n"
            "                dp[j] = max(dp[j], dp[j - 1])\n"
            "            prev = cur\n"
            "    return dp[m]\n",
            lambda low: bool(
                re.search(r"\blongest common subsequence\b|\blcs\b", low)
                and "substring" not in low
            ),
            ((("abcde", "ace"), 3), (("abc", "abc"), 3), (("abc", "def"), 0)),
        ),
        Template(
            "max_product_subarray",
            "def max_product_subarray(nums):\n"
            '    """Return the maximum product of a contiguous subarray."""\n'
            "    if not nums:\n"
            "        return 0\n"
            "    best = lo = hi = nums[0]\n"
            "    for x in nums[1:]:\n"
            "        cand = (x, lo * x, hi * x)\n"
            "        lo, hi = min(cand), max(cand)\n"
            "        if hi > best:\n"
            "            best = hi\n"
            "    return best\n",
            lambda low: bool(re.search(r"\bmax(?:imum)? product subarray\b", low)),
            (
                (([2, 3, -2, 4],), 6),
                (([-2, 0, -1],), 0),
            ),
        ),
        Template(
            "target_sum",
            "def target_sum(nums, target):\n"
            '    """Return ways to assign +/- to nums so the sum equals target."""\n'
            "    total = sum(nums)\n"
            "    if (total + target) % 2 or abs(target) > total:\n"
            "        return 0\n"
            "    need = (total + target) // 2\n"
            "    dp = [0] * (need + 1)\n"
            "    dp[0] = 1\n"
            "    for x in nums:\n"
            "        for s in range(need, x - 1, -1):\n"
            "            dp[s] += dp[s - x]\n"
            "    return dp[need]\n",
            lambda low: bool(
                re.search(r"\btarget sum\b", low)
                and "two sum" not in low
                and "3sum" not in low
                and "three sum" not in low
            ),
            (
                (([1, 1, 1, 1, 1], 3), 5),
                (([1], 1), 1),
            ),
        ),
        Template(
            "subarray_sum",
            "def subarray_sum(nums, k):\n"
            '    """Return the number of contiguous subarrays that sum to k."""\n'
            "    count = 0\n"
            "    running = 0\n"
            "    seen = {0: 1}\n"
            "    for x in nums:\n"
            "        running += x\n"
            "        count += seen.get(running - k, 0)\n"
            "        seen[running] = seen.get(running, 0) + 1\n"
            "    return count\n",
            lambda low: bool(
                re.search(
                    r"\bsubarray sum(?:s)?(?: equals?| equal to)? k\b|"
                    r"\bnumber of (?:contiguous )?subarrays? (?:that )?sum(?:s)? to\b|"
                    r"\bsubarray_sum\b",
                    low,
                )
                and "product" not in low
                and "maximum subarray" not in low
                and "max subarray" not in low
            ),
            (
                (([1, 1, 1], 2), 2),
                (([1, 2, 3], 3), 2),
            ),
        ),
        Template(
            "character_replacement",
            "def character_replacement(s, k):\n"
            '    """Longest substring after replacing at most k characters."""\n'
            "    left = 0\n"
            "    best = 0\n"
            "    freq = {}\n"
            "    maxf = 0\n"
            "    for right, ch in enumerate(s):\n"
            "        freq[ch] = freq.get(ch, 0) + 1\n"
            "        if freq[ch] > maxf:\n"
            "            maxf = freq[ch]\n"
            "        while (right - left + 1) - maxf > k:\n"
            "            freq[s[left]] -= 1\n"
            "            left += 1\n"
            "        span = right - left + 1\n"
            "        if span > best:\n"
            "            best = span\n"
            "    return best\n",
            lambda low: bool(
                re.search(
                    r"\blongest repeating character replacement\b|"
                    r"\bcharacter replacement\b|"
                    r"\breplace(?:ing)? at most k characters\b|"
                    r"\bcharacter_replacement\b",
                    low,
                )
            ),
            (
                (("ABAB", 2), 4),
                (("AABABBA", 1), 4),
            ),
        ),
        Template(
            "find_all_anagrams",
            "def find_all_anagrams(s, p):\n"
            '    """Return start indices of p-anagrams in s."""\n'
            "    need = {}\n"
            "    for ch in p:\n"
            "        need[ch] = need.get(ch, 0) + 1\n"
            "    missing = len(need)\n"
            "    window = {}\n"
            "    out = []\n"
            "    left = 0\n"
            "    for right, ch in enumerate(s):\n"
            "        window[ch] = window.get(ch, 0) + 1\n"
            "        if ch in need and window[ch] == need[ch]:\n"
            "            missing -= 1\n"
            "        if right - left + 1 > len(p):\n"
            "            drop = s[left]\n"
            "            if drop in need and window[drop] == need[drop]:\n"
            "                missing += 1\n"
            "            window[drop] -= 1\n"
            "            left += 1\n"
            "        if missing == 0:\n"
            "            out.append(left)\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bfind all anagrams\b|"
                    r"\banagrams in (?:a )?string\b|"
                    r"\bfind_all_anagrams\b",
                    low,
                )
                and "group" not in low
            ),
            (
                (("cbaebabacd", "abc"), [0, 6]),
                (("abab", "ab"), [0, 1, 2]),
            ),
        ),
        Template(
            "first_missing_positive",
            "def first_missing_positive(nums):\n"
            '    """Return the smallest missing positive integer."""\n'
            "    n = len(nums)\n"
            "    vals = list(nums)\n"
            "    for i in range(n):\n"
            "        while 1 <= vals[i] <= n and vals[vals[i] - 1] != vals[i]:\n"
            "            j = vals[i] - 1\n"
            "            vals[i], vals[j] = vals[j], vals[i]\n"
            "    for i, v in enumerate(vals):\n"
            "        if v != i + 1:\n"
            "            return i + 1\n"
            "    return n + 1\n",
            lambda low: bool(
                re.search(
                    r"\bfirst missing positive\b|"
                    r"\bsmallest missing positive\b|"
                    r"\bfirst_missing_positive\b",
                    low,
                )
                and "missing number" not in low
            ),
            (
                (([1, 2, 0],), 3),
                (([3, 4, -1, 1],), 2),
                (([7, 8, 9, 11, 12],), 1),
            ),
        ),
        Template(
            "n_queens",
            "def n_queens(n):\n"
            '    """Return the number of distinct N-Queens solutions."""\n'
            "    n = int(n)\n"
            "    cols = set()\n"
            "    diag1 = set()\n"
            "    diag2 = set()\n"
            "    total = [0]\n"
            "\n"
            "    def place(r):\n"
            "        if r == n:\n"
            "            total[0] += 1\n"
            "            return\n"
            "        for c in range(n):\n"
            "            if c in cols or (r - c) in diag1 or (r + c) in diag2:\n"
            "                continue\n"
            "            cols.add(c)\n"
            "            diag1.add(r - c)\n"
            "            diag2.add(r + c)\n"
            "            place(r + 1)\n"
            "            cols.remove(c)\n"
            "            diag1.remove(r - c)\n"
            "            diag2.remove(r + c)\n"
            "\n"
            "    place(0)\n"
            "    return total[0]\n",
            lambda low: bool(
                re.search(r"\bn[- ]?queens\b|\btotal n[- ]?queens\b|\bn_queens\b", low)
            ),
            (
                ((4,), 2),
                ((1,), 1),
            ),
        ),
        Template(
            "basic_calculator_ii",
            "def basic_calculator_ii(s):\n"
            '    """Evaluate +, -, *, / over non-negative integers (truncate toward zero)."""\n'
            "    stack = []\n"
            "    num = 0\n"
            "    op = '+'\n"
            "    for i, ch in enumerate(s):\n"
            "        if ch.isdigit():\n"
            "            num = num * 10 + ord(ch) - 48\n"
            "        if ch in '+-*/' or i == len(s) - 1:\n"
            "            if not ch.isdigit() and ch not in '+-*/' and i != len(s) - 1:\n"
            "                continue\n"
            "            if op == '+':\n"
            "                stack.append(num)\n"
            "            elif op == '-':\n"
            "                stack.append(-num)\n"
            "            elif op == '*':\n"
            "                stack.append(stack.pop() * num)\n"
            "            else:\n"
            "                prev = stack.pop()\n"
            "                if prev < 0:\n"
            "                    stack.append(-((-prev) // num))\n"
            "                else:\n"
            "                    stack.append(prev // num)\n"
            "            op = ch\n"
            "            num = 0\n"
            "    return sum(stack)\n",
            lambda low: bool(
                re.search(
                    r"\bbasic calculator ii\b|"
                    r"\bbasic_calculator_ii\b|"
                    r"\bevaluate[^\n]{0,40}[+\-*\/]{2,}",
                    low,
                )
                or (
                    "basic calculator" in low
                    and ("ii" in low or "multiply" in low or "*" in low)
                )
            ),
            (
                (("3+2*2",), 7),
                ((" 3/2 ",), 1),
                ((" 3+5 / 2 ",), 5),
            ),
        ),
        Template(
            "lfu_cache",
            "class _LFUCache:\n"
            '    """Least-frequently-used cache (tie-break: least recent)."""\n'
            "    def __init__(self, capacity):\n"
            "        self.cap = int(capacity)\n"
            "        self.val = {}\n"
            "        self.freq = {}\n"
            "        self.stamp = {}\n"
            "        self.t = 0\n"
            "    def _touch(self, key):\n"
            "        self.t += 1\n"
            "        self.freq[key] = self.freq.get(key, 0) + 1\n"
            "        self.stamp[key] = self.t\n"
            "    def get(self, key):\n"
            "        if key not in self.val:\n"
            "            return -1\n"
            "        self._touch(key)\n"
            "        return self.val[key]\n"
            "    def put(self, key, value):\n"
            "        if self.cap <= 0:\n"
            "            return\n"
            "        if key in self.val:\n"
            "            self.val[key] = value\n"
            "            self._touch(key)\n"
            "            return\n"
            "        if len(self.val) >= self.cap:\n"
            "            victim = min(self.val, key=lambda k: (self.freq[k], self.stamp[k]))\n"
            "            del self.val[victim]\n"
            "            del self.freq[victim]\n"
            "            del self.stamp[victim]\n"
            "        self.val[key] = value\n"
            "        self.freq[key] = 0\n"
            "        self._touch(key)\n"
            "\n"
            "def lfu_cache(ops):\n"
            '    """Replay (op, args) against LFUCache. get→int, put→None omitted."""\n'
            "    cache = None\n"
            "    out = []\n"
            "    for item in ops:\n"
            "        op, args = item[0], item[1]\n"
            "        if op == 'LFUCache':\n"
            "            cache = _LFUCache(*args)\n"
            "            out.append(None)\n"
            "        elif op == 'put':\n"
            "            cache.put(*args)\n"
            "            out.append(None)\n"
            "        else:\n"
            "            out.append(cache.get(*args))\n"
            "    return out\n",
            lambda low: bool(
                re.search(r"\blfu\b|least[- ]frequently[- ]used|\blfu_cache\b", low)
            ),
            (
                (
                    (
                        [
                            ("LFUCache", (2,)),
                            ("put", (1, 1)),
                            ("put", (2, 2)),
                            ("get", (1,)),
                            ("put", (3, 3)),
                            ("get", (2,)),
                            ("get", (3,)),
                        ],
                    ),
                    [None, None, None, 1, None, -1, 3],
                ),
            ),
        ),
        Template(
            "time_based_kv",
            "def time_based_kv(ops):\n"
            '    """Replay TimeMap set/get (largest timestamp <= query)."""\n'
            "    import bisect\n"
            "    store = {}\n"
            "    out = []\n"
            "    for item in ops:\n"
            "        op, args = item[0], item[1]\n"
            "        if op == 'TimeMap':\n"
            "            store = {}\n"
            "            out.append(None)\n"
            "        elif op == 'set':\n"
            "            key, value, ts = args\n"
            "            store.setdefault(key, []).append((ts, value))\n"
            "            out.append(None)\n"
            "        else:\n"
            "            key, ts = args\n"
            "            arr = store.get(key) or []\n"
            "            i = bisect.bisect_right(arr, (ts, chr(255))) - 1\n"
            "            out.append(arr[i][1] if i >= 0 else '')\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\btime[- ]based\b|"
                    r"\btimemap\b|"
                    r"\btime_based_kv\b|"
                    r"\bkey[- ]value store with timestamps\b",
                    low,
                )
            ),
            (
                (
                    (
                        [
                            ("TimeMap", ()),
                            ("set", ("foo", "bar", 1)),
                            ("get", ("foo", 1)),
                            ("get", ("foo", 3)),
                            ("set", ("foo", "bar2", 4)),
                            ("get", ("foo", 4)),
                            ("get", ("foo", 5)),
                        ],
                    ),
                    [None, None, "bar", "bar", None, "bar2", "bar2"],
                ),
            ),
        ),
        Template(
            "insert_delete_getrandom",
            "def insert_delete_getrandom(ops):\n"
            '    """Replay RandomizedSet insert / remove / getRandom."""\n'
            "    import random\n"
            "    vals, idx = [], {}\n"
            "    out = []\n"
            "    rng = random.Random(0)\n"
            "    for item in ops:\n"
            "        op, args = item[0], item[1]\n"
            "        if op == 'RandomizedSet':\n"
            "            vals, idx = [], {}\n"
            "            out.append(None)\n"
            "        elif op == 'insert':\n"
            "            x = args[0]\n"
            "            if x in idx:\n"
            "                out.append(False)\n"
            "            else:\n"
            "                idx[x] = len(vals)\n"
            "                vals.append(x)\n"
            "                out.append(True)\n"
            "        elif op == 'remove':\n"
            "            x = args[0]\n"
            "            if x not in idx:\n"
            "                out.append(False)\n"
            "            else:\n"
            "                i = idx[x]\n"
            "                last = vals[-1]\n"
            "                vals[i] = last\n"
            "                idx[last] = i\n"
            "                vals.pop()\n"
            "                del idx[x]\n"
            "                out.append(True)\n"
            "        else:\n"
            "            out.append(vals[rng.randrange(len(vals))] if vals else None)\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\binsert delete getrandom\b|"
                    r"\brandomized ?set\b|"
                    r"\binsert_delete_getrandom\b|"
                    r"\binsert,? delete,? and getrandom\b",
                    low,
                )
            ),
            (
                (
                    (
                        [
                            ("RandomizedSet", ()),
                            ("insert", (1,)),
                            ("remove", (2,)),
                            ("insert", (2,)),
                            ("remove", (1,)),
                            ("insert", (2,)),
                        ],
                    ),
                    [None, True, False, True, True, False],
                ),
            ),
        ),
        Template(
            "moving_average",
            "def moving_average(size, vals):\n"
            '    """Streaming moving average of the last `size` values."""\n'
            "    from collections import deque\n"
            "    q = deque()\n"
            "    s = 0\n"
            "    out = []\n"
            "    k = int(size)\n"
            "    for x in vals:\n"
            "        q.append(x)\n"
            "        s += x\n"
            "        if len(q) > k:\n"
            "            s -= q.popleft()\n"
            "        out.append(s / len(q))\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bmoving average\b|"
                    r"\bmoving_average\b|"
                    r"\bsliding[- ]window average\b",
                    low,
                )
            ) and "maximum" not in low,
            (
                ((3, [1, 10, 3, 5]), [1.0, 5.5, 14 / 3, 6.0]),
            ),
        ),
        Template(
            "logger_rate_limiter",
            "def logger_rate_limiter(messages):\n"
            '    """(timestamp, message) pairs; True if printed (10s cooldown)."""\n'
            "    last = {}\n"
            "    out = []\n"
            "    for ts, msg in messages:\n"
            "        prev = last.get(msg)\n"
            "        if prev is None or ts - prev >= 10:\n"
            "            last[msg] = ts\n"
            "            out.append(True)\n"
            "        else:\n"
            "            out.append(False)\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\blogger rate limiter\b|"
                    r"\brate limiter\b|"
                    r"\blogger_rate_limiter\b|"
                    r"\bshould print message\b",
                    low,
                )
            ),
            (
                (
                    (
                        [
                            (1, "foo"),
                            (2, "bar"),
                            (3, "foo"),
                            (8, "bar"),
                            (10, "foo"),
                            (11, "foo"),
                        ],
                    ),
                    [True, True, False, False, False, True],
                ),
            ),
        ),
        Template(
            "design_hashmap",
            "def design_hashmap(ops):\n"
            '    """Replay MyHashMap put / get / remove."""\n'
            "    store = {}\n"
            "    out = []\n"
            "    for item in ops:\n"
            "        op, args = item[0], item[1]\n"
            "        if op == 'MyHashMap':\n"
            "            store = {}\n"
            "            out.append(None)\n"
            "        elif op == 'put':\n"
            "            store[args[0]] = args[1]\n"
            "            out.append(None)\n"
            "        elif op == 'get':\n"
            "            out.append(store.get(args[0], -1))\n"
            "        else:\n"
            "            store.pop(args[0], None)\n"
            "            out.append(None)\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bdesigns? (?:a )?hashmap\b|"
                    r"\bmyhashmap\b|"
                    r"\bdesign_hashmap\b|"
                    r"\bimplement(?:s|ing)? (?:a )?hashmap\b",
                    low,
                )
            ),
            (
                (
                    (
                        [
                            ("MyHashMap", ()),
                            ("put", (1, 1)),
                            ("put", (2, 2)),
                            ("get", (1,)),
                            ("get", (3,)),
                            ("put", (2, 1)),
                            ("get", (2,)),
                            ("remove", (2,)),
                            ("get", (2,)),
                        ],
                    ),
                    [None, None, None, 1, -1, None, 1, None, -1],
                ),
            ),
        ),
        Template(
            "range_sum_query",
            "def range_sum_query(nums, queries):\n"
            '    """Prefix-sum range queries [l, r] inclusive on nums."""\n'
            "    pref = [0]\n"
            "    for x in nums:\n"
            "        pref.append(pref[-1] + x)\n"
            "    return [pref[r + 1] - pref[l] for l, r in queries]\n",
            lambda low: bool(
                re.search(
                    r"\brange sum query\b|"
                    r"\bnumarray\b|"
                    r"\brange_sum_query\b|"
                    r"\bprefix sum range\b",
                    low,
                )
            ) and "2d" not in low and "matrix" not in low,
            (
                (([-2, 0, 3, -5, 2, -1], [(0, 2), (2, 5), (0, 5)]), [1, -1, -3]),
            ),
        ),
        Template(
            "snapshot_array",
            "def snapshot_array(ops):\n"
            '    """Replay SnapshotArray set / snap / get (LeetCode 1146)."""\n'
            "    import bisect\n"
            "    hist = {}\n"
            "    snap_id = 0\n"
            "    out = []\n"
            "    for item in ops:\n"
            "        op, args = item[0], item[1]\n"
            "        if op == 'SnapshotArray':\n"
            "            hist, snap_id = {}, 0\n"
            "            out.append(None)\n"
            "        elif op == 'set':\n"
            "            idx, val = args\n"
            "            hist.setdefault(idx, []).append((snap_id, val))\n"
            "            out.append(None)\n"
            "        elif op == 'snap':\n"
            "            out.append(snap_id)\n"
            "            snap_id += 1\n"
            "        else:\n"
            "            idx, sid = args\n"
            "            arr = hist.get(idx, [])\n"
            "            i = bisect.bisect_right(arr, (sid, float('inf'))) - 1\n"
            "            out.append(0 if i < 0 else arr[i][1])\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bsnapshot[- ]?array\b|"
                    r"\bsnapshot_array\b|"
                    r"\bsnapshotarray\b",
                    low,
                )
            ),
            (
                (
                    (
                        [
                            ("SnapshotArray", (3,)),
                            ("set", (0, 5)),
                            ("snap", ()),
                            ("set", (0, 6)),
                            ("get", (0, 0)),
                        ],
                    ),
                    [None, None, 0, None, 5],
                ),
            ),
        ),
        Template(
            "circular_queue",
            "def circular_queue(ops):\n"
            '    """Replay MyCircularQueue enQueue / deQueue / Front / Rear / isEmpty / isFull."""\n'
            "    from collections import deque\n"
            "    q = deque()\n"
            "    cap = 0\n"
            "    out = []\n"
            "    for item in ops:\n"
            "        op, args = item[0], item[1]\n"
            "        if op == 'MyCircularQueue':\n"
            "            cap = args[0]\n"
            "            q = deque()\n"
            "            out.append(None)\n"
            "        elif op == 'enQueue':\n"
            "            if len(q) >= cap:\n"
            "                out.append(False)\n"
            "            else:\n"
            "                q.append(args[0])\n"
            "                out.append(True)\n"
            "        elif op == 'deQueue':\n"
            "            if not q:\n"
            "                out.append(False)\n"
            "            else:\n"
            "                q.popleft()\n"
            "                out.append(True)\n"
            "        elif op == 'Front':\n"
            "            out.append(-1 if not q else q[0])\n"
            "        elif op == 'Rear':\n"
            "            out.append(-1 if not q else q[-1])\n"
            "        elif op == 'isEmpty':\n"
            "            out.append(not q)\n"
            "        else:\n"
            "            out.append(len(q) >= cap)\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bcircular[- ]?queue\b|"
                    r"\bmycircularqueue\b|"
                    r"\bdesign(?:s|ing)? (?:a )?circular queue\b",
                    low,
                )
            ),
            (
                (
                    (
                        [
                            ("MyCircularQueue", (3,)),
                            ("enQueue", (1,)),
                            ("enQueue", (2,)),
                            ("enQueue", (3,)),
                            ("enQueue", (4,)),
                            ("Rear", ()),
                            ("isFull", ()),
                            ("deQueue", ()),
                            ("enQueue", (4,)),
                            ("Rear", ()),
                        ],
                    ),
                    [None, True, True, True, False, 3, True, True, True, 4],
                ),
            ),
        ),
        Template(
            "encode_decode_tinyurl",
            "def encode_decode_tinyurl(urls):\n"
            '    """Encode then decode each URL; decoded list equals the input."""\n'
            "    table = {}\n"
            "    n = 0\n"
            "\n"
            "    def encode(url):\n"
            "        nonlocal n\n"
            "        n += 1\n"
            "        code = 'http://tinyurl.com/' + str(n)\n"
            "        table[code] = url\n"
            "        return code\n"
            "\n"
            "    def decode(short):\n"
            "        return table[short]\n"
            "\n"
            "    return [decode(encode(u)) for u in urls]\n",
            lambda low: bool(
                re.search(
                    r"\btinyurl\b|"
                    r"\bencode(?:/| and | )decode.{0,16}\burl\b|"
                    r"\bencode_decode_tinyurl\b|"
                    r"\bdesign(?:s|ing)? (?:a )?tiny ?url\b",
                    low,
                )
            ),
            (
                ((["https://leetcode.com/problems/design-tinyurl"],), ["https://leetcode.com/problems/design-tinyurl"]),
                ((["a", "b"],), ["a", "b"]),
            ),
        ),
        Template(
            "stack_using_queues",
            "def stack_using_queues(ops):\n"
            '    """Replay MyStack push / pop / top / empty using two queues."""\n'
            "    from collections import deque\n"
            "    q = deque()\n"
            "    out = []\n"
            "    for item in ops:\n"
            "        op, args = item[0], item[1]\n"
            "        if op == 'MyStack':\n"
            "            q = deque()\n"
            "            out.append(None)\n"
            "        elif op == 'push':\n"
            "            q.append(args[0])\n"
            "            for _ in range(len(q) - 1):\n"
            "                q.append(q.popleft())\n"
            "            out.append(None)\n"
            "        elif op == 'pop':\n"
            "            out.append(q.popleft())\n"
            "        elif op == 'top':\n"
            "            out.append(q[0])\n"
            "        else:\n"
            "            out.append(not q)\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bstack using queues?\b|"
                    r"\bimplement(?:s|ing)? (?:a )?stack using queues?\b|"
                    r"\bmystack\b|"
                    r"\bstack_using_queues\b",
                    low,
                )
            ) and "queue using stack" not in low,
            (
                (
                    (
                        [
                            ("MyStack", ()),
                            ("push", (1,)),
                            ("push", (2,)),
                            ("top", ()),
                            ("pop", ()),
                            ("empty", ()),
                        ],
                    ),
                    [None, None, None, 2, 2, False],
                ),
            ),
        ),
        Template(
            "parking_system",
            "def parking_system(ops):\n"
            '    """Replay ParkingSystem addCar by size (big/medium/small)."""\n'
            "    slots = {}\n"
            "    out = []\n"
            "    for item in ops:\n"
            "        op, args = item[0], item[1]\n"
            "        if op == 'ParkingSystem':\n"
            "            slots = {1: args[0], 2: args[1], 3: args[2]}\n"
            "            out.append(None)\n"
            "        else:\n"
            "            t = args[0]\n"
            "            if slots.get(t, 0) > 0:\n"
            "                slots[t] -= 1\n"
            "                out.append(True)\n"
            "            else:\n"
            "                out.append(False)\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bparking[- ]?system\b|"
                    r"\bdesign(?:s|ing)? (?:a )?parking\b|"
                    r"\bparkingsystem\b",
                    low,
                )
            ),
            (
                (
                    (
                        [
                            ("ParkingSystem", (1, 1, 0)),
                            ("addCar", (1,)),
                            ("addCar", (2,)),
                            ("addCar", (3,)),
                            ("addCar", (1,)),
                        ],
                    ),
                    [None, True, True, False, False],
                ),
            ),
        ),
        Template(
            "design_twitter",
            "def design_twitter(ops):\n"
            '    """Replay Twitter post / follow / unfollow / getNewsFeed."""\n'
            "    from collections import defaultdict\n"
            "    posts = []\n"
            "    follows = defaultdict(set)\n"
            "    out = []\n"
            "    clock = 0\n"
            "    for item in ops:\n"
            "        op, args = item[0], item[1]\n"
            "        if op == 'Twitter':\n"
            "            posts, follows, clock = [], defaultdict(set), 0\n"
            "            out.append(None)\n"
            "        elif op == 'postTweet':\n"
            "            clock += 1\n"
            "            posts.append((clock, args[0], args[1]))\n"
            "            out.append(None)\n"
            "        elif op == 'follow':\n"
            "            if args[0] != args[1]:\n"
            "                follows[args[0]].add(args[1])\n"
            "            out.append(None)\n"
            "        elif op == 'unfollow':\n"
            "            follows[args[0]].discard(args[1])\n"
            "            out.append(None)\n"
            "        else:\n"
            "            user = args[0]\n"
            "            seen = follows[user] | {user}\n"
            "            feed = [tid for _, uid, tid in reversed(posts) if uid in seen][:10]\n"
            "            out.append(feed)\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bdesign(?:s|ing)? (?:a )?twitter\b|"
                    r"\bdesign_twitter\b|"
                    r"\btwitter news ?feed\b",
                    low,
                )
            ),
            (
                (
                    (
                        [
                            ("Twitter", ()),
                            ("postTweet", (1, 5)),
                            ("getNewsFeed", (1,)),
                            ("follow", (1, 2)),
                            ("postTweet", (2, 6)),
                            ("getNewsFeed", (1,)),
                            ("unfollow", (1, 2)),
                            ("getNewsFeed", (1,)),
                        ],
                    ),
                    [None, None, [5], None, None, [6, 5], None, [5]],
                ),
            ),
        ),
        Template(
            "browser_history",
            "def browser_history(ops):\n"
            '    """Replay BrowserHistory visit / back / forward (LeetCode 1472)."""\n'
            "    hist, i = [], -1\n"
            "    out = []\n"
            "    for item in ops:\n"
            "        op, args = item[0], item[1]\n"
            "        if op == 'BrowserHistory':\n"
            "            hist, i = [args[0]], 0\n"
            "            out.append(None)\n"
            "        elif op == 'visit':\n"
            "            hist = hist[: i + 1]\n"
            "            hist.append(args[0])\n"
            "            i = len(hist) - 1\n"
            "            out.append(None)\n"
            "        elif op == 'back':\n"
            "            i = max(0, i - int(args[0]))\n"
            "            out.append(hist[i])\n"
            "        else:\n"
            "            i = min(len(hist) - 1, i + int(args[0]))\n"
            "            out.append(hist[i])\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bbrowser[- ]?history\b|"
                    r"\bdesign(?:s|ing)? (?:a )?browser\b|"
                    r"\bvisit.+back.+forward\b",
                    low,
                )
            ),
            (
                (
                    (
                        [
                            ("BrowserHistory", ("leetcode.com",)),
                            ("visit", ("google.com",)),
                            ("visit", ("facebook.com",)),
                            ("visit", ("youtube.com",)),
                            ("back", (1,)),
                            ("back", (1,)),
                            ("forward", (1,)),
                            ("visit", ("linkedin.com",)),
                            ("forward", (2,)),
                            ("back", (2,)),
                            ("back", (7,)),
                        ],
                    ),
                    [
                        None,
                        None,
                        None,
                        None,
                        "facebook.com",
                        "google.com",
                        "facebook.com",
                        None,
                        "linkedin.com",
                        "google.com",
                        "leetcode.com",
                    ],
                ),
            ),
        ),
        Template(
            "underground_system",
            "def underground_system(ops):\n"
            '    """Replay UndergroundSystem check-in / check-out / getAverageTime."""\n'
            "    inn, trips = {}, {}\n"
            "    out = []\n"
            "    for item in ops:\n"
            "        op, args = item[0], item[1]\n"
            "        if op == 'UndergroundSystem':\n"
            "            inn, trips = {}, {}\n"
            "            out.append(None)\n"
            "        elif op == 'checkIn':\n"
            "            inn[args[0]] = (args[1], args[2])\n"
            "            out.append(None)\n"
            "        elif op == 'checkOut':\n"
            "            start, t0 = inn.pop(args[0])\n"
            "            key = (start, args[1])\n"
            "            total, cnt = trips.get(key, (0, 0))\n"
            "            trips[key] = (total + args[2] - t0, cnt + 1)\n"
            "            out.append(None)\n"
            "        else:\n"
            "            total, cnt = trips[(args[0], args[1])]\n"
            "            out.append(total / cnt)\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bunderground[- ]?system\b|"
                    r"\bdesign(?:s|ing)? (?:an? )?underground\b|"
                    r"\baverage travel time\b|"
                    r"\bcheck-?in.+check-?out.+(average|travel)\b",
                    low,
                )
            ),
            (
                (
                    (
                        [
                            ("UndergroundSystem", ()),
                            ("checkIn", (45, "Leyton", 3)),
                            ("checkOut", (45, "Waterloo", 15)),
                            ("getAverageTime", ("Leyton", "Waterloo")),
                        ],
                    ),
                    [None, None, None, 12.0],
                ),
            ),
        ),
        Template(
            "product_of_numbers",
            "def product_of_numbers(ops):\n"
            '    """Replay ProductOfNumbers add / getProduct (prefix products)."""\n'
            "    pref = [1]\n"
            "    out = []\n"
            "    for item in ops:\n"
            "        op, args = item[0], item[1]\n"
            "        if op == 'ProductOfNumbers':\n"
            "            pref = [1]\n"
            "            out.append(None)\n"
            "        elif op == 'add':\n"
            "            x = int(args[0])\n"
            "            if x == 0:\n"
            "                pref = [1]\n"
            "            else:\n"
            "                pref.append(pref[-1] * x)\n"
            "            out.append(None)\n"
            "        else:\n"
            "            k = int(args[0])\n"
            "            if k >= len(pref):\n"
            "                out.append(0)\n"
            "            else:\n"
            "                out.append(pref[-1] // pref[-1 - k])\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bproduct[- ]?of[- ]?(the[- ]?)?(last[- ]?)?(k[- ]?)?numbers\b|"
                    r"\bproductofnumbers\b|"
                    r"\bgetproduct\b",
                    low,
                )
                and not re.search(r"\bexcept self\b|\bproduct_except\b", low)
            ),
            (
                (
                    (
                        [
                            ("ProductOfNumbers", ()),
                            ("add", (3,)),
                            ("add", (0,)),
                            ("add", (2,)),
                            ("add", (5,)),
                            ("add", (4,)),
                            ("getProduct", (2,)),
                            ("getProduct", (3,)),
                            ("getProduct", (4,)),
                            ("add", (8,)),
                            ("getProduct", (2,)),
                        ],
                    ),
                    [None, None, None, None, None, None, 20, 40, 0, None, 32],
                ),
            ),
        ),
        Template(
            "recent_counter",
            "def recent_counter(ops):\n"
            '    """Replay RecentCounter ping — count calls in last 3000 ms."""\n'
            "    from collections import deque\n"
            "    q = deque()\n"
            "    out = []\n"
            "    for item in ops:\n"
            "        op, args = item[0], item[1]\n"
            "        if op == 'RecentCounter':\n"
            "            q = deque()\n"
            "            out.append(None)\n"
            "        else:\n"
            "            t = int(args[0])\n"
            "            q.append(t)\n"
            "            while q and q[0] < t - 3000:\n"
            "                q.popleft()\n"
            "            out.append(len(q))\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\brecent[- ]?counter\b|"
                    r"\bnumber of recent calls\b|"
                    r"\bping(?:s)? (?:in )?(?:the )?last 3000\b",
                    low,
                )
            ),
            (
                (
                    (
                        [
                            ("RecentCounter", ()),
                            ("ping", (1,)),
                            ("ping", (100,)),
                            ("ping", (3001,)),
                            ("ping", (3002,)),
                        ],
                    ),
                    [None, 1, 2, 3, 3],
                ),
            ),
        ),
        Template(
            "peeking_iterator",
            "def peeking_iterator(ops):\n"
            '    """Replay PeekingIterator next / peek / hasNext over a list."""\n'
            "    it, buf = [], None\n"
            "    has_buf = False\n"
            "    out = []\n"
            "    for item in ops:\n"
            "        op, args = item[0], item[1]\n"
            "        if op == 'PeekingIterator':\n"
            "            it = list(args[0])\n"
            "            buf, has_buf = None, False\n"
            "            out.append(None)\n"
            "        elif op == 'peek':\n"
            "            if not has_buf:\n"
            "                buf = it.pop(0)\n"
            "                has_buf = True\n"
            "            out.append(buf)\n"
            "        elif op == 'next':\n"
            "            if has_buf:\n"
            "                has_buf = False\n"
            "                out.append(buf)\n"
            "            else:\n"
            "                out.append(it.pop(0))\n"
            "        else:\n"
            "            out.append(has_buf or bool(it))\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bpeeking[- ]?iterator\b|"
                    r"\bpeek(?:ing)? iterator\b|"
                    r"\biterator (?:with )?peek\b",
                    low,
                )
            ),
            (
                (
                    (
                        [
                            ("PeekingIterator", ([1, 2, 3],)),
                            ("next", ()),
                            ("peek", ()),
                            ("next", ()),
                            ("next", ()),
                            ("hasNext", ()),
                        ],
                    ),
                    [None, 1, 2, 2, 3, False],
                ),
            ),
        ),
        Template(
            "stock_price",
            "def stock_price(ops):\n"
            '    """Replay StockPrice update / current / maximum / minimum."""\n'
            "    import heapq\n"
            "    price = {}\n"
            "    latest = -1\n"
            "    mx, mn = [], []\n"
            "    out = []\n"
            "    for item in ops:\n"
            "        op, args = item[0], item[1]\n"
            "        if op == 'StockPrice':\n"
            "            price, latest, mx, mn = {}, -1, [], []\n"
            "            out.append(None)\n"
            "        elif op == 'update':\n"
            "            t, p = int(args[0]), int(args[1])\n"
            "            price[t] = p\n"
            "            latest = max(latest, t)\n"
            "            heapq.heappush(mx, (-p, t))\n"
            "            heapq.heappush(mn, (p, t))\n"
            "            out.append(None)\n"
            "        elif op == 'current':\n"
            "            out.append(price[latest])\n"
            "        elif op == 'maximum':\n"
            "            while mx and price.get(mx[0][1]) != -mx[0][0]:\n"
            "                heapq.heappop(mx)\n"
            "            out.append(-mx[0][0])\n"
            "        else:\n"
            "            while mn and price.get(mn[0][1]) != mn[0][0]:\n"
            "                heapq.heappop(mn)\n"
            "            out.append(mn[0][0])\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bstock[- ]?price(?:[- ]?fluctuation)?\b|"
                    r"\bdesign(?:s|ing)? (?:a )?stock price\b|"
                    r"\bcurrent.+maximum.+minimum.+stock\b",
                    low,
                )
                and not re.search(r"\bmax_profit\b|\bbuy and sell\b|\bbest time to buy\b", low)
            ),
            (
                (
                    (
                        [
                            ("StockPrice", ()),
                            ("update", (1, 10)),
                            ("update", (2, 5)),
                            ("current", ()),
                            ("maximum", ()),
                            ("update", (1, 3)),
                            ("maximum", ()),
                            ("update", (4, 2)),
                            ("minimum", ()),
                        ],
                    ),
                    [None, None, None, 5, 10, None, 5, None, 2],
                ),
            ),
        ),
        Template(
            "find_all_duplicates",
            "def find_all_duplicates(nums):\n"
            '    """Numbers in 1..n that appear twice (mark-by-index)."""\n'
            "    a = list(nums)\n"
            "    out = []\n"
            "    for x in a:\n"
            "        i = abs(x) - 1\n"
            "        if a[i] < 0:\n"
            "            out.append(abs(x))\n"
            "        else:\n"
            "            a[i] = -a[i]\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bfind(?:s|ing)? all duplicates?\b|"
                    r"\ball duplicate(?:s| numbers?)?\b|"
                    r"\bfind_all_duplicates\b|"
                    r"\bnumbers? that appear twice\b",
                    low,
                )
            ),
            (
                (([4, 3, 2, 7, 8, 2, 3, 1],), [2, 3]),
                (([1, 1, 2],), [1]),
            ),
        ),
        Template(
            "find_disappeared",
            "def find_disappeared(nums):\n"
            '    """All values in 1..n missing from nums."""\n'
            "    n = len(nums)\n"
            "    seen = set(nums)\n"
            "    return [i for i in range(1, n + 1) if i not in seen]\n",
            lambda low: bool(
                re.search(
                    r"\bfind(?:s|ing)? all (?:the )?numbers? disappeared\b|"
                    r"\bdisappeared (?:from|in) (?:an? )?array\b|"
                    r"\bfind_disappeared\b|"
                    r"\bnumbers? disappeared\b|"
                    r"\bmissing numbers? from 1\s*(?:to|\.\.)\s*n\b",
                    low,
                )
            ),
            (
                (([4, 3, 2, 7, 8, 2, 3, 1],), [5, 6]),
                (([1, 1],), [2]),
            ),
        ),
        Template(
            "island_perimeter",
            "def island_perimeter(grid):\n"
            '    """Perimeter of the single island in a binary grid."""\n'
            "    if not grid:\n"
            "        return 0\n"
            "    rows, cols = len(grid), len(grid[0])\n"
            "    perim = 0\n"
            "    for r in range(rows):\n"
            "        for c in range(cols):\n"
            "            if grid[r][c] != 1:\n"
            "                continue\n"
            "            perim += 4\n"
            "            if r and grid[r - 1][c] == 1:\n"
            "                perim -= 2\n"
            "            if c and grid[r][c - 1] == 1:\n"
            "                perim -= 2\n"
            "    return perim\n",
            lambda low: bool(
                re.search(
                    r"\bisland[- ]?perimeter\b|"
                    r"\bperimeter of (?:the |an? )?island\b",
                    low,
                )
            ),
            (
                (([[0, 1, 0, 0], [1, 1, 1, 0], [0, 1, 0, 0], [1, 1, 0, 0]],), 16),
                (([[1]],), 4),
            ),
        ),
        Template(
            "next_greater_ii",
            "def next_greater_ii(nums):\n"
            '    """Next greater element in a circular array (stack)."""\n'
            "    n = len(nums)\n"
            "    ans = [-1] * n\n"
            "    st = []\n"
            "    for i in range(2 * n - 1, -1, -1):\n"
            "        x = nums[i % n]\n"
            "        while st and st[-1] <= x:\n"
            "            st.pop()\n"
            "        if i < n and st:\n"
            "            ans[i] = st[-1]\n"
            "        st.append(x)\n"
            "    return ans\n",
            lambda low: bool(
                re.search(
                    r"\bnext[- ]?greater[- ]?(?:element[- ]?)?ii\b|"
                    r"\bnext_greater_ii\b|"
                    r"\bnext greater.{0,24}circular\b|"
                    r"\bcircular.{0,24}next greater\b",
                    low,
                )
            ),
            (
                (([1, 2, 1],), [2, -1, 2]),
                (([1, 2, 3, 4, 3],), [2, 3, 4, -1, 4]),
            ),
        ),
        Template(
            "delete_and_earn",
            "def delete_and_earn(nums):\n"
            '    """Max points deleting x and removing x-1 / x+1 (house-robber)."""\n'
            "    if not nums:\n"
            "        return 0\n"
            "    m = max(nums)\n"
            "    pts = [0] * (m + 1)\n"
            "    for x in nums:\n"
            "        pts[x] += x\n"
            "    take = skip = 0\n"
            "    for p in pts:\n"
            "        take, skip = skip + p, max(skip, take)\n"
            "    return max(take, skip)\n",
            lambda low: bool(
                re.search(
                    r"\bdelete and earn\b|"
                    r"\bdelete_and_earn\b|"
                    r"\bearn points.{0,24}delet",
                    low,
                )
            ),
            (
                (([3, 4, 2],), 6),
                (([2, 2, 3, 3, 3, 4],), 9),
            ),
        ),
        Template(
            "longest_palindromic_subsequence",
            "def longest_palindromic_subsequence(s):\n"
            '    """Length of the longest palindromic subsequence (LCS with reverse)."""\n'
            "    n = len(s)\n"
            "    rev = s[::-1]\n"
            "    dp = [0] * (n + 1)\n"
            "    for i in range(1, n + 1):\n"
            "        prev = 0\n"
            "        for j in range(1, n + 1):\n"
            "            cur = dp[j]\n"
            "            if s[i - 1] == rev[j - 1]:\n"
            "                dp[j] = prev + 1\n"
            "            else:\n"
            "                dp[j] = max(dp[j], dp[j - 1])\n"
            "            prev = cur\n"
            "    return dp[n]\n",
            lambda low: bool(
                re.search(
                    r"\blongest palindromic subsequence\b|"
                    r"\blongest_palindromic_subsequence\b|"
                    r"\bpalindromic subsequence\b",
                    low,
                )
            ),
            (
                (("bbbab",), 4),
                (("cbbd",), 2),
            ),
        ),
        Template(
            "wiggle_subsequence",
            "def wiggle_subsequence(nums):\n"
            '    """Length of the longest wiggle (up/down) subsequence."""\n'
            "    if not nums:\n"
            "        return 0\n"
            "    up = down = 1\n"
            "    for i in range(1, len(nums)):\n"
            "        if nums[i] > nums[i - 1]:\n"
            "            up = down + 1\n"
            "        elif nums[i] < nums[i - 1]:\n"
            "            down = up + 1\n"
            "    return max(up, down)\n",
            lambda low: bool(
                re.search(
                    r"\bwiggle subsequence\b|"
                    r"\bwiggle_subsequence\b|"
                    r"\blongest wiggle\b",
                    low,
                )
            ),
            (
                (([1, 7, 4, 9, 2, 5],), 6),
                (([1, 17, 5, 10, 13, 15, 10, 5, 16, 8],), 7),
            ),
        ),
        Template(
            "can_place_flowers",
            "def can_place_flowers(flowerbed, n):\n"
            '    """True if n flowers can be planted with no-adjacent rule."""\n'
            "    bed = [0] + list(flowerbed) + [0]\n"
            "    planted = 0\n"
            "    for i in range(1, len(bed) - 1):\n"
            "        if bed[i - 1] == bed[i] == bed[i + 1] == 0:\n"
            "            bed[i] = 1\n"
            "            planted += 1\n"
            "    return planted >= n\n",
            lambda low: bool(
                re.search(
                    r"\bcan place flowers\b|"
                    r"\bcan_place_flowers\b|"
                    r"\bplace n flowers\b|"
                    r"\bflowerbed\b",
                    low,
                )
            ),
            (
                (([1, 0, 0, 0, 1], 1), True),
                (([1, 0, 0, 0, 1], 2), False),
            ),
        ),
        Template(
            "max_consecutive_ones",
            "def max_consecutive_ones(nums):\n"
            '    """Longest run of 1s in a binary array."""\n'
            "    best = cur = 0\n"
            "    for x in nums:\n"
            "        if x == 1:\n"
            "            cur += 1\n"
            "            if cur > best:\n"
            "                best = cur\n"
            "        else:\n"
            "            cur = 0\n"
            "    return best\n",
            lambda low: bool(
                re.search(
                    r"\bmax consecutive ones\b|"
                    r"\bmax_consecutive_ones\b|"
                    r"\blongest consecutive ones\b",
                    low,
                )
            ),
            (
                (([1, 1, 0, 1, 1, 1],), 3),
                (([1, 0, 1, 1, 0, 1],), 2),
            ),
        ),
        Template(
            "find_the_difference",
            "def find_the_difference(s, t):\n"
            '    """The extra character in t versus s (xor)."""\n'
            "    x = 0\n"
            "    for ch in s:\n"
            "        x ^= ord(ch)\n"
            "    for ch in t:\n"
            "        x ^= ord(ch)\n"
            "    return chr(x)\n",
            lambda low: bool(
                re.search(
                    r"\bfind the difference\b|"
                    r"\bfind_the_difference\b|"
                    r"\bextra character in t\b",
                    low,
                )
                and "array" not in low
                and "list" not in low
            ),
            (
                (("abcd", "abcde"), "e"),
                (("", "y"), "y"),
            ),
        ),
        Template(
            "ransom_note",
            "def ransom_note(ransomNote, magazine):\n"
            '    """True if ransomNote can be constructed from magazine letters."""\n'
            "    from collections import Counter\n"
            "    need = Counter(ransomNote)\n"
            "    have = Counter(magazine)\n"
            "    return all(have[ch] >= n for ch, n in need.items())\n",
            lambda low: bool(
                re.search(
                    r"\bransom note\b|"
                    r"\bransom_note\b|"
                    r"\bconstruct.{0,16}from magazine\b",
                    low,
                )
            ),
            (
                (("a", "b"), False),
                (("aa", "aab"), True),
            ),
        ),
        Template(
            "first_bad_version",
            "def first_bad_version(n, is_bad):\n"
            '    """First bad version in 1..n given is_bad(version) predicate."""\n'
            "    lo, hi = 1, n\n"
            "    while lo < hi:\n"
            "        mid = (lo + hi) // 2\n"
            "        if is_bad(mid):\n"
            "            hi = mid\n"
            "        else:\n"
            "            lo = mid + 1\n"
            "    return lo\n",
            lambda low: bool(
                re.search(
                    r"\bfirst bad version\b|"
                    r"\bfirst_bad_version\b",
                    low,
                )
            ),
            (
                ((5, lambda v: v >= 4), 4),
                ((1, lambda v: v >= 1), 1),
            ),
        ),
        Template(
            "min_cost_climbing_stairs",
            "def min_cost_climbing_stairs(cost):\n"
            '    """Min cost to reach the top; start at step 0 or 1."""\n'
            "    n = len(cost)\n"
            "    if n == 0:\n"
            "        return 0\n"
            "    if n == 1:\n"
            "        return int(cost[0])\n"
            "    a, b = int(cost[0]), int(cost[1])\n"
            "    for i in range(2, n):\n"
            "        a, b = b, int(cost[i]) + min(a, b)\n"
            "    return min(a, b)\n",
            lambda low: bool(
                re.search(
                    r"\bmin(?:imum)? cost climb(?:ing)? stairs\b|"
                    r"\bmin_cost_climbing_stairs\b|"
                    r"\bmin(?:imum)? cost to climb\b",
                    low,
                )
            ),
            (
                (([10, 15, 20],), 15),
                (([1, 100, 1, 1, 1, 100, 1, 1, 100, 1],), 6),
            ),
        ),
        Template(
            "search_insert",
            "def search_insert(nums, target):\n"
            '    """Index of target or insertion point in a sorted array."""\n'
            "    lo, hi = 0, len(nums)\n"
            "    while lo < hi:\n"
            "        mid = (lo + hi) // 2\n"
            "        if nums[mid] < target:\n"
            "            lo = mid + 1\n"
            "        else:\n"
            "            hi = mid\n"
            "    return lo\n",
            lambda low: bool(
                re.search(
                    r"\bsearch insert\b|"
                    r"\bsearch_insert\b|"
                    r"\binsertion position\b|"
                    r"\binsert position in (a )?sorted\b",
                    low,
                )
            ),
            (
                (([1, 3, 5, 6], 5), 2),
                (([1, 3, 5, 6], 2), 1),
                (([1, 3, 5, 6], 7), 4),
            ),
        ),
        Template(
            "isomorphic_strings",
            "def isomorphic_strings(s, t):\n"
            '    """True if s and t are isomorphic (1-1 char mapping)."""\n'
            "    if len(s) != len(t):\n"
            "        return False\n"
            "    st, ts = {}, {}\n"
            "    for a, b in zip(s, t):\n"
            "        if st.get(a, b) != b or ts.get(b, a) != a:\n"
            "            return False\n"
            "        st[a] = b\n"
            "        ts[b] = a\n"
            "    return True\n",
            lambda low: bool(
                re.search(
                    r"\bisomorphic strings?\b|"
                    r"\bisomorphic_strings\b|"
                    r"\bis_isomorphic\b|"
                    r"\bstrings? (are|is) isomorphic\b",
                    low,
                )
            ),
            (
                (("egg", "add"), True),
                (("foo", "bar"), False),
                (("paper", "title"), True),
            ),
        ),
        Template(
            "word_pattern",
            "def word_pattern(pattern, s):\n"
            '    """True if s words follow pattern bijection."""\n'
            "    words = s.split()\n"
            "    if len(pattern) != len(words):\n"
            "        return False\n"
            "    pt, tp = {}, {}\n"
            "    for p, w in zip(pattern, words):\n"
            "        if pt.get(p, w) != w or tp.get(w, p) != p:\n"
            "            return False\n"
            "        pt[p] = w\n"
            "        tp[w] = p\n"
            "    return True\n",
            lambda low: bool(
                re.search(
                    r"\bword pattern\b|"
                    r"\bword_pattern\b",
                    low,
                )
            ),
            (
                (("abba", "dog cat cat dog"), True),
                (("abba", "dog cat cat fish"), False),
                (("aaaa", "dog cat cat dog"), False),
            ),
        ),
        Template(
            "reverse_integer",
            "def reverse_integer(x):\n"
            '    """Reverse digits of a 32-bit signed integer; 0 on overflow."""\n'
            "    sign = -1 if x < 0 else 1\n"
            "    n = abs(int(x))\n"
            "    out = 0\n"
            "    while n:\n"
            "        out = out * 10 + n % 10\n"
            "        n //= 10\n"
            "    out *= sign\n"
            "    if out < -(2 ** 31) or out > 2 ** 31 - 1:\n"
            "        return 0\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\breverse(?: an | the )?integers?\b|"
                    r"\breverse_integer\b|"
                    r"\breverse digits of (an? )?int",
                    low,
                )
            ),
            (
                ((123,), 321),
                ((-123,), -321),
                ((120,), 21),
            ),
        ),
        Template(
            "add_strings",
            "def add_strings(num1, num2):\n"
            '    """Add two non-negative integers given as decimal strings."""\n'
            "    i, j, carry = len(num1) - 1, len(num2) - 1, 0\n"
            "    out = []\n"
            "    while i >= 0 or j >= 0 or carry:\n"
            "        a = ord(num1[i]) - 48 if i >= 0 else 0\n"
            "        b = ord(num2[j]) - 48 if j >= 0 else 0\n"
            "        s = a + b + carry\n"
            "        out.append(chr(48 + s % 10))\n"
            "        carry = s // 10\n"
            "        i -= 1\n"
            "        j -= 1\n"
            "    return ''.join(reversed(out))\n",
            lambda low: bool(
                re.search(
                    r"\badd strings\b|"
                    r"\badd_strings\b|"
                    r"\badd two strings (that|which) represent\b",
                    low,
                )
                and "binary" not in low
            ),
            (
                (("11", "123"), "134"),
                (("456", "77"), "533"),
                (("0", "0"), "0"),
            ),
        ),
    ]
