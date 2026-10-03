"""Cycle 402: coding prompts that previously returned draft stubs.

Official examples:
- LeetCode 2806 Account Balance After Rounded Purchase: 9 -> 90; 15 -> 80.
  Start at 100; round purchase to nearest 10, ties round up.
- LeetCode 1133 Largest Unique Number: [5,7,3,9,4,9,8,3,1] -> 8; [9,9,8,8] -> -1.
- LeetCode 944 Delete Columns to Make Sorted: ["cba","daf","ghi"] -> 1;
  ["a","b"] -> 0; ["zyx","wvu","tsr"] -> 3.
- LeetCode 419 Battleships in a Board:
  [["X",".",".","X"],[".",".",".","X"],[".",".",".","X"]] -> 2.
- LeetCode 475 Heaters: houses [1,2,3] heaters [2] -> 1;
  houses [1,2,3,4] heaters [1,4] -> 1.
- LeetCode 946 Validate Stack Sequences:
  pushed [1,2,3,4,5] popped [4,5,3,2,1] -> true;
  pushed [1,2,3,4,5] popped [4,3,5,1,2] -> false.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "account_balance_after_purchase",
            "def account_balance_after_purchase(purchaseAmount):\n"
            '    """Balance after rounding a purchase to nearest 10, ties up (LeetCode 2806)."""\n'
            "    rounded = ((purchaseAmount + 5) // 10) * 10\n"
            "    return 100 - rounded\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*2806\b", low)
                or "account balance after rounded purchase" in low
                or "account balance after purchase" in low
            ),
            examples=(( (9,), 90), ((15,), 80)),
        ),
        T(
            "largest_unique_number",
            "def largest_unique_number(nums):\n"
            '    """Largest value that occurs once, else -1 (LeetCode 1133)."""\n'
            "    from collections import Counter\n"
            "    cnt = Counter(nums)\n"
            "    best = -1\n"
            "    for value, count in cnt.items():\n"
            "        if count == 1 and value > best:\n"
            "            best = value\n"
            "    return best\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*1133\b", low)
                or "largest unique number" in low
            ),
            examples=(
                (([5, 7, 3, 9, 4, 9, 8, 3, 1],), 8),
                (([9, 9, 8, 8],), -1),
            ),
        ),
        T(
            "min_deletion_size",
            "def min_deletion_size(strs):\n"
            '    """Columns to delete so each column is non-decreasing (LeetCode 944)."""\n'
            "    if not strs:\n"
            "        return 0\n"
            "    rows, cols = len(strs), len(strs[0])\n"
            "    bad = 0\n"
            "    for c in range(cols):\n"
            "        for r in range(1, rows):\n"
            "            if strs[r][c] < strs[r - 1][c]:\n"
            "                bad += 1\n"
            "                break\n"
            "    return bad\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*944\b", low)
                or "delete columns to make sorted" in low
                or "minimum deletion size" in low
            ),
            examples=(
                ((["cba", "daf", "ghi"],), 1),
                ((["a", "b"],), 0),
                ((["zyx", "wvu", "tsr"],), 3),
            ),
        ),
        T(
            "count_battleships",
            "def count_battleships(board):\n"
            '    """Count battleships; ships are straight and separated (LeetCode 419)."""\n'
            "    if not board:\n"
            "        return 0\n"
            "    ans = 0\n"
            "    for i, row in enumerate(board):\n"
            "        for j, cell in enumerate(row):\n"
            "            if cell != 'X':\n"
            "                continue\n"
            "            if i and board[i - 1][j] == 'X':\n"
            "                continue\n"
            "            if j and board[i][j - 1] == 'X':\n"
            "                continue\n"
            "            ans += 1\n"
            "    return ans\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*419\b", low)
                or "battleships in a board" in low
            ),
            examples=(
                (([["X", ".", ".", "X"], [".", ".", ".", "X"], [".", ".", ".", "X"]],), 2),
                (([["."]],), 0),
            ),
        ),
        T(
            "find_radius",
            "def find_radius(houses, heaters):\n"
            '    """Minimum heater radius that covers every house (LeetCode 475)."""\n'
            "    import bisect\n"
            "    heaters = sorted(heaters)\n"
            "    ans = 0\n"
            "    for house in houses:\n"
            "        i = bisect.bisect_left(heaters, house)\n"
            "        best = 10 ** 18\n"
            "        if i < len(heaters):\n"
            "            best = min(best, heaters[i] - house)\n"
            "        if i:\n"
            "            best = min(best, house - heaters[i - 1])\n"
            "        ans = max(ans, best)\n"
            "    return ans\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*475\b", low)
                or re.search(r"\bheaters\b", low)
            ),
            examples=(
                (([1, 2, 3], [2]), 1),
                (([1, 2, 3, 4], [1, 4]), 1),
            ),
        ),
        T(
            "validate_stack_sequences",
            "def validate_stack_sequences(pushed, popped):\n"
            '    """True if popped is a valid stack order of pushed (LeetCode 946)."""\n'
            "    stack = []\n"
            "    i = 0\n"
            "    for value in pushed:\n"
            "        stack.append(value)\n"
            "        while stack and i < len(popped) and stack[-1] == popped[i]:\n"
            "            stack.pop()\n"
            "            i += 1\n"
            "    return i == len(popped)\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*946\b", low)
                or "validate stack sequences" in low
            ),
            examples=(
                (([1, 2, 3, 4, 5], [4, 5, 3, 2, 1]), True),
                (([1, 2, 3, 4, 5], [4, 3, 5, 1, 2]), False),
            ),
        ),
    ]
