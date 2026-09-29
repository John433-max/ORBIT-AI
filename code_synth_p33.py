"""Cycle 293: check-tree / eval boolean tree / merge alternately / wealth / altitude / pangram."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "check_tree",
            "def check_tree(root):\n"
            '    """True if root value equals left+right children (LeetCode 2236)."""\n'
            "    if root is None:\n"
            "        return False\n"
            "    left = root[1] if len(root) > 1 else None\n"
            "    right = root[2] if len(root) > 2 else None\n"
            "    lv = 0 if left is None else left[0]\n"
            "    rv = 0 if right is None else right[0]\n"
            "    return root[0] == lv + rv\n",
            lambda low: bool(
                re.search(
                    r"\bcheck[_ ]tree\b|"
                    r"\broot[_ ]equals[_ ]sum[_ ]of[_ ]children\b|"
                    r"\broot equals sum of children\b|"
                    r"\bcheck if (?:the )?root equals? (?:the )?sum of (?:its )?children\b",
                    low,
                )
            ),
            (
                (([10, [4, None, None], [6, None, None]],), True),
                (([5, [2, None, None], [3, None, None]],), True),
                (([5, [6, None, None], [1, None, None]],), False),
            ),
        ),
        T(
            "evaluate_tree",
            "def evaluate_tree(root):\n"
            '    """Evaluate a full boolean binary tree (LeetCode 2331)."""\n'
            "    if root is None:\n"
            "        return False\n"
            "    val = root[0]\n"
            "    left = root[1] if len(root) > 1 else None\n"
            "    right = root[2] if len(root) > 2 else None\n"
            "    if left is None and right is None:\n"
            "        return bool(val)\n"
            "    lv = evaluate_tree(left)\n"
            "    rv = evaluate_tree(right)\n"
            "    if val == 2:\n"
            "        return lv or rv\n"
            "    return lv and rv\n",
            lambda low: bool(
                re.search(
                    r"\bevaluate[_ ]tree\b|"
                    r"\bevaluate[_ ]boolean[_ ](?:binary[_ ])?tree\b|"
                    r"\bevaluate (?:a |the )?(?:boolean )?(?:binary )?tree\b|"
                    r"\bboolean binary tree\b",
                    low,
                )
            ),
            (
                (([2, [1, None, None], [3, [0, None, None], [1, None, None]]],), True),
                (([0, None, None],), False),
                (([1, None, None],), True),
            ),
        ),
        T(
            "merge_alternately",
            "def merge_alternately(word1, word2):\n"
            '    """Merge two strings by alternating characters (LeetCode 1768)."""\n'
            "    out = []\n"
            "    n = max(len(word1), len(word2))\n"
            "    for i in range(n):\n"
            "        if i < len(word1):\n"
            "            out.append(word1[i])\n"
            "        if i < len(word2):\n"
            "            out.append(word2[i])\n"
            "    return ''.join(out)\n",
            lambda low: bool(
                re.search(
                    r"\bmerge[_ ]alternately\b|"
                    r"\bmerge strings? alternately\b|"
                    r"\balternating(?:ly)? merge (?:two )?strings?\b|"
                    r"\bmerge two strings? (?:by )?alternat",
                    low,
                )
            ),
            (
                (("abc", "pqr"), "apbqcr"),
                (("ab", "pqrs"), "apbqrs"),
                (("abcd", "pq"), "apbqcd"),
            ),
        ),
        T(
            "richest_customer_wealth",
            "def richest_customer_wealth(accounts):\n"
            '    """Maximum row-sum wealth (LeetCode 1672)."""\n'
            "    return max((sum(row) for row in accounts), default=0)\n",
            lambda low: bool(
                re.search(
                    r"\brichest[_ ]customer[_ ]wealth\b|"
                    r"\brichest customer(?:'s)? wealth\b|"
                    r"\bmaximum wealth\b|"
                    r"\bwealthiest customer\b",
                    low,
                )
            ),
            (
                (([[1, 2, 3], [3, 2, 1]],), 6),
                (([[1, 5], [7, 3], [3, 5]],), 10),
                (([[2, 8, 7], [7, 1, 3], [1, 9, 5]],), 17),
            ),
        ),
        T(
            "highest_altitude",
            "def highest_altitude(gain):\n"
            '    """Highest altitude after prefix gains (LeetCode 1732)."""\n'
            "    alt = 0\n"
            "    best = 0\n"
            "    for g in gain:\n"
            "        alt += g\n"
            "        if alt > best:\n"
            "            best = alt\n"
            "    return best\n",
            lambda low: bool(
                re.search(
                    r"\bhighest[_ ]altitude\b|"
                    r"\bfind (?:the )?highest altitude\b|"
                    r"\bmaximum altitude\b|"
                    r"\baltitude from gain\b",
                    low,
                )
            ),
            (
                (([-5, 1, 5, 0, -7],), 1),
                (([-4, -3, -2, -1, 4, 3, 2],), 0),
                (([1, 2, 3],), 6),
            ),
        ),
        T(
            "check_pangram",
            "def check_pangram(sentence):\n"
            '    """True if sentence uses every letter a-z (LeetCode 1832)."""\n'
            "    seen = set()\n"
            "    for ch in sentence.lower():\n"
            "        if 'a' <= ch <= 'z':\n"
            "            seen.add(ch)\n"
            "    return len(seen) == 26\n",
            lambda low: bool(
                re.search(
                    r"\bcheck[_ ]pangram\b|"
                    r"\bis[_ ]pangram\b|"
                    r"\bpangram\b|"
                    r"\bsentence is (?:a )?pangram\b|"
                    r"\bcheck if (?:the )?sentence is (?:a )?pangram\b",
                    low,
                )
            ),
            (
                (("thequickbrownfoxjumpsoverthelazydog",), True),
                (("leetcode",), False),
                (("abcdefghijklmnopqrstuvwxyz",), True),
            ),
        ),
    ]
