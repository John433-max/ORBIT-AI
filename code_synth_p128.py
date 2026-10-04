"""Cycle 406: verified templates for unmatched medium graph/interval asks.

Official examples (not copied solutions):
- LeetCode 406 Queue Reconstruction by Height:
  [[7,0],[4,4],[7,1],[5,0],[6,1],[5,2]] ->
  [[5,0],[7,0],[5,2],[6,1],[4,4],[7,1]].
  Sort height desc, k asc, insert at index k.
- LeetCode 253 Meeting Rooms II:
  [[0,30],[5,10],[15,20]] -> 2; [[7,10],[2,4]] -> 1.
- LeetCode 875 Koko Eating Bananas:
  [3,6,7,11], h=8 -> 4; [30,11,23,4,20], h=5 -> 30; h=6 -> 23.
- LeetCode 316 Remove Duplicate Letters:
  "bcabc" -> "abc"; "cbacdcbc" -> "acdb".
- LeetCode 354 Russian Doll Envelopes:
  [[5,4],[6,4],[6,7],[2,3]] -> 3; [[1,1],[1,1],[1,1]] -> 1.
- LeetCode 399 Evaluate Division:
  a/b=2, b/c=3; a/c=6, b/a=0.5, a/e=-1, a/a=1, x/x=-1.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "reconstruct_queue",
            "def reconstructQueue(people):\n"
            '    """Rebuild queue by height and people in front (LeetCode 406)."""\n'
            "    ordered = sorted(people, key=lambda p: (-int(p[0]), int(p[1])))\n"
            "    out = []\n"
            "    for person in ordered:\n"
            "        out.insert(int(person[1]), [int(person[0]), int(person[1])])\n"
            "    return out\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*406\b", low)
                or "queue reconstruction" in low
                or "reconstruct queue" in low
            ),
            examples=(
                (
                    ([[7, 0], [4, 4], [7, 1], [5, 0], [6, 1], [5, 2]],),
                    [[5, 0], [7, 0], [5, 2], [6, 1], [4, 4], [7, 1]],
                ),
                (([[6, 0], [5, 0], [4, 0], [3, 2], [2, 2], [1, 4]],), [[4, 0], [5, 0], [2, 2], [3, 2], [1, 4], [6, 0]]),
            ),
        ),
        T(
            "serialize_binary_tree",
            "def serialize(root):\n"
            '    """Round-trip a level-order binary tree (LeetCode 297)."""\n'
            "    def build(vals):\n"
            "        if not vals or vals[0] is None:\n"
            "            return None\n"
            "        nodes = [None if v is None else {'v': int(v), 'l': None, 'r': None} for v in vals]\n"
            "        kids = 1\n"
            "        for node in nodes:\n"
            "            if node is None:\n"
            "                continue\n"
            "            if kids < len(nodes):\n"
            "                node['l'] = nodes[kids]\n"
            "                kids += 1\n"
            "            if kids < len(nodes):\n"
            "                node['r'] = nodes[kids]\n"
            "                kids += 1\n"
            "        return nodes[0]\n"
            "    def dump(node):\n"
            "        if node is None:\n"
            "            return 'null'\n"
            "        return str(node['v']) + ',' + dump(node['l']) + ',' + dump(node['r'])\n"
            "    def parse(it):\n"
            "        tok = next(it)\n"
            "        if tok == 'null':\n"
            "            return None\n"
            "        return {'v': int(tok), 'l': parse(it), 'r': parse(it)}\n"
            "    def to_list(node):\n"
            "        if node is None:\n"
            "            return []\n"
            "        out, q = [], [node]\n"
            "        while q:\n"
            "            cur = q.pop(0)\n"
            "            if cur is None:\n"
            "                out.append(None)\n"
            "                continue\n"
            "            out.append(cur['v'])\n"
            "            q.append(cur['l'])\n"
            "            q.append(cur['r'])\n"
            "        while out and out[-1] is None:\n"
            "            out.pop()\n"
            "        return out\n"
            "    data = dump(build(root))\n"
            "    return to_list(parse(iter(data.split(','))))\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*297\b", low)
                or "serialize and deserialize binary tree" in low
                or "serialize binary tree" in low
            ),
            examples=(
                (([1, 2, 3, None, None, 4, 5],), [1, 2, 3, None, None, 4, 5]),
                (([],), []),
            ),
        ),
        T(
            "min_eating_speed",
            "def minEatingSpeed(piles, h):\n"
            '    """Minimum integer bananas/hour to finish in h hours (LeetCode 875)."""\n'
            "    piles = [int(p) for p in piles]\n"
            "    h = int(h)\n"
            "    lo, hi = 1, max(piles)\n"
            "    while lo < hi:\n"
            "        mid = (lo + hi) // 2\n"
            "        hours = sum((p + mid - 1) // mid for p in piles)\n"
            "        if hours <= h:\n"
            "            hi = mid\n"
            "        else:\n"
            "            lo = mid + 1\n"
            "    return lo\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*875\b", low)
                or "koko" in low
                or "eating bananas" in low
            ),
            examples=(
                (([3, 6, 7, 11], 8), 4),
                (([30, 11, 23, 4, 20], 5), 30),
                (([30, 11, 23, 4, 20], 6), 23),
            ),
        ),
        T(
            "remove_duplicate_letters",
            "def removeDuplicateLetters(s):\n"
            '    """Smallest lexicographic subsequence with unique letters (LeetCode 316)."""\n'
            "    last = {ch: i for i, ch in enumerate(s)}\n"
            "    stack = []\n"
            "    seen = set()\n"
            "    for i, ch in enumerate(s):\n"
            "        if ch in seen:\n"
            "            continue\n"
            "        while stack and stack[-1] > ch and last[stack[-1]] > i:\n"
            "            seen.remove(stack.pop())\n"
            "        stack.append(ch)\n"
            "        seen.add(ch)\n"
            "    return ''.join(stack)\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*316\b", low)
                or "remove duplicate letters" in low
            ),
            examples=(
                (("bcabc",), "abc"),
                (("cbacdcbc",), "acdb"),
            ),
        ),
        T(
            "max_envelopes",
            "def maxEnvelopes(envelopes):\n"
            '    """Longest chain of envelopes that nest (LeetCode 354)."""\n'
            "    env = sorted((int(w), int(h)) for w, h in envelopes)\n"
            "    # widths ascending, heights descending so equal widths cannot nest\n"
            "    env.sort(key=lambda wh: (wh[0], -wh[1]))\n"
            "    tails = []\n"
            "    for _, h in env:\n"
            "        lo, hi = 0, len(tails)\n"
            "        while lo < hi:\n"
            "            mid = (lo + hi) // 2\n"
            "            if tails[mid] < h:\n"
            "                lo = mid + 1\n"
            "            else:\n"
            "                hi = mid\n"
            "        if lo == len(tails):\n"
            "            tails.append(h)\n"
            "        else:\n"
            "            tails[lo] = h\n"
            "    return len(tails)\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*354\b", low)
                or "russian doll" in low
            ),
            examples=(
                (([[5, 4], [6, 4], [6, 7], [2, 3]],), 3),
                (([[1, 1], [1, 1], [1, 1]],), 1),
            ),
        ),
        T(
            "calc_equation",
            "def calcEquation(equations, values, queries):\n"
            '    """Evaluate division queries on a weighted equation graph (LeetCode 399)."""\n'
            "    from collections import defaultdict\n"
            "    graph = defaultdict(list)\n"
            "    for (a, b), val in zip(equations, values):\n"
            "        graph[a].append((b, float(val)))\n"
            "        graph[b].append((a, 1.0 / float(val)))\n"
            "    def dfs(src, dst, seen):\n"
            "        if src not in graph or dst not in graph:\n"
            "            return -1.0\n"
            "        if src == dst:\n"
            "            return 1.0\n"
            "        seen.add(src)\n"
            "        for nxt, w in graph[src]:\n"
            "            if nxt in seen:\n"
            "                continue\n"
            "            got = dfs(nxt, dst, seen)\n"
            "            if got != -1.0:\n"
            "                return w * got\n"
            "        return -1.0\n"
            "    return [dfs(a, b, set()) for a, b in queries]\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*399\b", low)
                or "evaluate division" in low
                or "calc equation" in low
            ),
            examples=(
                (
                    (
                        [["a", "b"], ["b", "c"]],
                        [2.0, 3.0],
                        [["a", "c"], ["b", "a"], ["a", "e"], ["a", "a"], ["x", "x"]],
                    ),
                    [6.0, 0.5, -1.0, 1.0, -1.0],
                ),
            ),
        ),
    ]
