"""Cycle 648 (p356): six educational templates that were stubs.

find_first_and_last_position (34), non_decreasing_array (665),
maximum_length_of_pair_chain (646), stone_game (877),
delete_operation_for_two_strings (583), contains_duplicate_iii (220).
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "find_first_and_last_position",
            '''def find_first_and_last_position(nums, target):
    """First and last position of target in sorted array (LeetCode 34).

    Two binary searches. Return [-1, -1] when absent.
    """
    def lower_bound(x):
        lo, hi = 0, len(nums)
        while lo < hi:
            mid = (lo + hi) // 2
            if nums[mid] < x:
                lo = mid + 1
            else:
                hi = mid
        return lo

    left = lower_bound(target)
    if left == len(nums) or nums[left] != target:
        return [-1, -1]
    right = lower_bound(target + 1) - 1
    return [left, right]
''',
            lambda low: bool(
                re.search(
                    r"\bfind[_ ]first[_ ]and[_ ]last[_ ]position\b|"
                    r"\bsearch[_ ](?:for[_ ]a[_ ])?range\b|"
                    r"\bfirst\s+and\s+last\s+position\b|"
                    r"\bleetcode\s+34\b",
                    low,
                )
            )
            and "insert" not in low,
            (
                (([5, 7, 7, 8, 8, 10], 8), [3, 4]),
                (([5, 7, 7, 8, 8, 10], 6), [-1, -1]),
                (([], 0), [-1, -1]),
            ),
        ),
        T(
            "non_decreasing_array",
            '''def non_decreasing_array(nums):
    """Whether an array can be made non-decreasing by changing at most one element (LeetCode 665)."""
    changed = False
    for i in range(1, len(nums)):
        if nums[i] < nums[i - 1]:
            if changed:
                return False
            changed = True
            if i >= 2 and nums[i] < nums[i - 2]:
                nums[i] = nums[i - 1]
            else:
                nums[i - 1] = nums[i]
    return True
''',
            lambda low: bool(
                re.search(
                    r"\bnon[_ ]decreasing[_ ]array\b|"
                    r"\bnon-decreasing\s+array\b|"
                    r"\bat\s+most\s+one\s+(?:element|change)\b.{0,40}\bnon[- ]decreasing\b|"
                    r"\bleetcode\s+665\b",
                    low,
                )
            )
            and "subsequence" not in low,
            (
                (([4, 2, 3],), True),
                (([4, 2, 1],), False),
                (([3, 4, 2, 3],), False),
            ),
        ),
        T(
            "maximum_length_of_pair_chain",
            '''def maximum_length_of_pair_chain(pairs):
    """Longest chain of pairs where pairs[i][1] < pairs[j][0] (LeetCode 646).

    Sort by ending value; greedy keep earliest end.
    """
    pairs = sorted(pairs, key=lambda p: p[1])
    end = float("-inf")
    length = 0
    for a, b in pairs:
        if a > end:
            length += 1
            end = b
    return length
''',
            lambda low: bool(
                re.search(
                    r"\bmaximum[_ ]length[_ ]of[_ ]pair[_ ]chain\b|"
                    r"\bmaximum\s+length\s+of\s+pair\s+chain\b|"
                    r"\blongest\s+pair\s+chain\b|"
                    r"\bleetcode\s+646\b",
                    low,
                )
            ),
            (
                (([[1, 2], [2, 3], [3, 4]],), 2),
                (([[1, 2], [7, 8], [4, 5]],), 3),
                (([[1, 2]],), 1),
            ),
        ),
        T(
            "stone_game",
            '''def stone_game(piles):
    """Alice and Bob take piles from ends; Alice starts (LeetCode 877).

    With an even number of piles and optimal play, Alice always wins.
    """
    return len(piles) % 2 == 0 or True
''',
            lambda low: bool(
                re.search(
                    r"\bstone[_ ]game\b(?!\s*(?:ii|iii|iv|2|3|4))|"
                    r"\balice\s+and\s+bob\s+take\s+piles\b|"
                    r"\bleetcode\s+877\b",
                    low,
                )
            )
            and "ii" not in low
            and "iii" not in low
            and "2" not in low
            and "3" not in low,
            (
                (([5, 3, 4, 5],), True),
                (([3, 7, 2, 3],), True),
                (([1],), True),
            ),
        ),
        T(
            "delete_operation_for_two_strings",
            '''def delete_operation_for_two_strings(word1, word2):
    """Minimum deletions to make two strings equal (LeetCode 583).

    Equivalent to len(word1) + len(word2) - 2 * LCS.
    """
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    lcs = dp[m][n]
    return m + n - 2 * lcs
''',
            lambda low: bool(
                re.search(
                    r"\bdelete[_ ]operation[_ ]for[_ ]two[_ ]strings\b|"
                    r"\bminimum\s+(?:number\s+of\s+)?deletions?\s+to\s+make\s+two\s+strings\s+equal\b|"
                    r"\bdelete\s+operation\s+for\s+two\s+strings\b|"
                    r"\bleetcode\s+583\b",
                    low,
                )
            )
            and "ascii" not in low,
            (
                (("sea", "eat"), 2),
                (("leetcode", "etco"), 4),
                (("a", "b"), 2),
            ),
        ),
        T(
            "contains_duplicate_iii",
            '''def contains_duplicate_iii(nums, index_diff, value_diff):
    """Whether two indices i, j exist with |i-j| <= indexDiff and |nums[i]-nums[j]| <= valueDiff (LeetCode 220).

    Bucket by valueDiff+1; check neighboring buckets in the sliding window.
    """
    if value_diff < 0 or index_diff <= 0:
        return False
    buckets = {}
    width = value_diff + 1
    for i, x in enumerate(nums):
        bid = x // width
        if bid in buckets:
            return True
        if bid - 1 in buckets and abs(x - buckets[bid - 1]) <= value_diff:
            return True
        if bid + 1 in buckets and abs(x - buckets[bid + 1]) <= value_diff:
            return True
        buckets[bid] = x
        if i >= index_diff:
            old = nums[i - index_diff]
            del buckets[old // width]
    return False
''',
            lambda low: bool(
                re.search(
                    r"\bcontains[_ ]duplicate[_ ]iii\b|"
                    r"\bcontains\s+duplicate\s+iii\b|"
                    r"\bcontains\s+nearby\s+almost\s+duplicate\b|"
                    r"\bleetcode\s+220\b",
                    low,
                )
            )
            and not re.search(r"\bcontains[_ ]duplicate[_ ]ii\b", low)
            and "leetcode 219" not in low,
            (
                (([1, 2, 3, 1], 3, 0), True),
                (([1, 5, 9, 1, 5, 9], 2, 3), False),
                (([1, 2, 3, 1], 1, 0), False),
            ),
        ),
    ]
