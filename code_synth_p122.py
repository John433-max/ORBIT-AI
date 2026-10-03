"""Cycle 401: unmatched coding prompts that miss the template path.

Official examples (leetcode.doocs.org problem statements):
- 3295 Report Spam Message: ["hello","world","leetcode"] / ["world","hello"] -> true;
  ["hello","programming","fun"] / ["world","programming","leetcode"] -> false.
- 3318 Find X-Sum of All K-Long Subarrays I:
  [1,1,2,2,3,4,2,3], k=6, x=2 -> [6,10,12];
  [3,8,7,8,7,5], k=2, x=2 -> [11,15,15,15,12].
- 3324 Find the Sequence of Strings Appeared on the Screen:
  "abc" -> ["a","aa","ab","aba","abb","abc"];
  "he" -> ["a","b","c","d","e","f","g","h","ha","hb","hc","hd","he"].
- 3471 Find the Largest Almost Missing Integer:
  [3,9,2,1,7], k=3 -> 7; [3,9,7,2,1,7], k=4 -> 3; [0,0], k=1 -> -1.
- 3576 Transform Array to All Equal Elements:
  [1,-1,1,-1,1], k=3 -> true; [-1,-1,-1,1,1,1], k=5 -> false.
- 3643 Flip Square Submatrix Vertically:
  [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]], x=1, y=0, k=3
  -> [[1,2,3,4],[13,14,15,8],[9,10,11,12],[5,6,7,16]];
  [[3,4,2,3],[2,3,4,2]], x=0, y=2, k=2 -> [[3,4,4,2],[2,3,2,3]].
3289/3300 already have templates in p57 and are not repeated.
"""
from __future__ import annotations

import re
from collections import Counter

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "report_spam",
            "def report_spam(message, banned_words):\n"
            '    """True if at least two message words are banned (LeetCode 3295)."""\n'
            "    banned = set(banned_words)\n"
            "    return sum(word in banned for word in message) >= 2\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*3295\b", low)
                or "report spam message" in low
            ),
            examples=(
                ((["hello", "world", "leetcode"], ["world", "hello"]), True),
                ((["hello", "programming", "fun"], ["world", "programming", "leetcode"]), False),
            ),
        ),
        T(
            "find_x_sum",
            "def find_x_sum(nums, k, x):\n"
            '    """X-sum of each k-window; ties keep the larger value (LeetCode 3318)."""\n'
            "    from collections import Counter\n"
            "    ans = []\n"
            "    for i in range(len(nums) - k + 1):\n"
            "        window = nums[i:i + k]\n"
            "        cnt = Counter(window)\n"
            "        keep = set(sorted(cnt, key=lambda v: (cnt[v], v), reverse=True)[:x])\n"
            "        ans.append(sum(v for v in window if v in keep))\n"
            "    return ans\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*3318\b", low)
                or "x-sum" in low
                or "x sum of all k-long" in low
            ),
            examples=(
                (([1, 1, 2, 2, 3, 4, 2, 3], 6, 2), [6, 10, 12]),
                (([3, 8, 7, 8, 7, 5], 2, 2), [11, 15, 15, 15, 12]),
            ),
        ),
        T(
            "string_sequence",
            "def string_sequence(target):\n"
            '    """Strings on screen while typing target with key1/key2 (LeetCode 3324)."""\n'
            "    ans = []\n"
            "    screen = []\n"
            "    for ch in target:\n"
            "        screen.append('a')\n"
            "        ans.append(''.join(screen))\n"
            "        for code in range(ord('b'), ord(ch) + 1):\n"
            "            screen[-1] = chr(code)\n"
            "            ans.append(''.join(screen))\n"
            "    return ans\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*3324\b", low)
                or "sequence of strings appeared on the screen" in low
            ),
            examples=(
                (("abc",), ["a", "aa", "ab", "aba", "abb", "abc"]),
                (("he",), ["a", "b", "c", "d", "e", "f", "g", "h", "ha", "hb", "hc", "hd", "he"]),
            ),
        ),
        T(
            "largest_almost_missing",
            "def largest_almost_missing(nums, k):\n"
            '    """Largest value in exactly one k-window, else -1 (LeetCode 3471)."""\n'
            "    from collections import Counter\n"
            "    n = len(nums)\n"
            "    if k == 1:\n"
            "        cnt = Counter(nums)\n"
            "        return max((x for x, v in cnt.items() if v == 1), default=-1)\n"
            "    if k == n:\n"
            "        return max(nums)\n"
            "    def end(i):\n"
            "        for j, x in enumerate(nums):\n"
            "            if j != i and x == nums[i]:\n"
            "                return -1\n"
            "        return nums[i]\n"
            "    return max(end(0), end(n - 1))\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*3471\b", low)
                or "almost missing integer" in low
            ),
            examples=(
                (([3, 9, 2, 1, 7], 3), 7),
                (([3, 9, 7, 2, 1, 7], 4), 3),
                (([0, 0], 1), -1),
            ),
        ),
        T(
            "can_make_equal",
            "def can_make_equal(nums, k):\n"
            '    """At most k adjacent sign flips can make all equal (LeetCode 3576)."""\n'
            "    def check(target):\n"
            "        cnt, sign = 0, 1\n"
            "        for i in range(len(nums) - 1):\n"
            "            if nums[i] * sign == target:\n"
            "                sign = 1\n"
            "            else:\n"
            "                sign = -1\n"
            "                cnt += 1\n"
            "        return cnt <= k and nums[-1] * sign == target\n"
            "    return check(nums[0]) or check(-nums[0])\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*3576\b", low)
                or "transform array to all equal elements" in low
            ),
            examples=(
                (([1, -1, 1, -1, 1], 3), True),
                (([-1, -1, -1, 1, 1, 1], 5), False),
            ),
        ),
        T(
            "reverse_submatrix",
            "def reverse_submatrix(grid, x, y, k):\n"
            '    """Flip a kxk submatrix vertically from (x, y) (LeetCode 3643)."""\n'
            "    g = [row[:] for row in grid]\n"
            "    for i in range(x, x + k // 2):\n"
            "        i2 = x + k - 1 - (i - x)\n"
            "        for j in range(y, y + k):\n"
            "            g[i][j], g[i2][j] = g[i2][j], g[i][j]\n"
            "    return g\n",
            lambda low: bool(
                re.search(r"\bleetcode\s*3643\b", low)
                or "flip square submatrix vertically" in low
            ),
            examples=(
                (
                    ([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]], 1, 0, 3),
                    [[1, 2, 3, 4], [13, 14, 15, 8], [9, 10, 11, 12], [5, 6, 7, 16]],
                ),
                (
                    ([[3, 4, 2, 3], [2, 3, 4, 2]], 0, 2, 2),
                    [[3, 4, 4, 2], [2, 3, 2, 3]],
                ),
            ),
        ),
    ]
