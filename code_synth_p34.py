"""Cycle 294: identical pairs / target array / XOR array / consistent strings / sum-zero ints / split score."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "num_identical_pairs",
            "def num_identical_pairs(nums):\n"
            '    """Number of good pairs where nums[i] == nums[j] and i < j (LeetCode 1512)."""\n'
            "    counts = {}\n"
            "    pairs = 0\n"
            "    for n in nums:\n"
            "        c = counts.get(n, 0)\n"
            "        pairs += c\n"
            "        counts[n] = c + 1\n"
            "    return pairs\n",
            lambda low: bool(
                re.search(
                    r"\bnum[_ ]identical[_ ]pairs\b|"
                    r"\bidentical pairs in (?:an? )?array\b|"
                    r"\bnumber of identical pairs\b",
                    low,
                )
            ),
            (
                (([1, 2, 3, 1, 1, 3],), 4),
                (([1, 1, 1, 1],), 6),
                (([1, 2, 3],), 0),
            ),
        ),
        T(
            "create_target_array",
            "def create_target_array(nums, index):\n"
            '    """Build target by inserting nums[i] at index[i] (LeetCode 1389)."""\n'
            "    target = []\n"
            "    for n, i in zip(nums, index):\n"
            "        target.insert(i, n)\n"
            "    return target\n",
            lambda low: bool(
                re.search(
                    r"\bcreate[_ ]target[_ ]array\b|"
                    r"\btarget array in (?:the )?given order\b|"
                    r"\bcreate target array\b",
                    low,
                )
            ),
            (
                (([0, 1, 2, 3, 4], [0, 1, 2, 2, 1]), [0, 4, 1, 3, 2]),
                (([1, 2, 3, 4, 0], [0, 1, 2, 3, 0]), [0, 1, 2, 3, 4]),
                (([1], [0]), [1]),
            ),
        ),
        T(
            "xor_operation",
            "def xor_operation(n, start):\n"
            '    """XOR of n nums: start, start+2, ... (LeetCode 1486)."""\n'
            "    acc = 0\n"
            "    for i in range(n):\n"
            "        acc ^= start + 2 * i\n"
            "    return acc\n",
            lambda low: bool(
                re.search(
                    r"\bxor[_ ]operation\b|"
                    r"\bxor operation in an array\b|"
                    r"\bxor of (?:an? )?array (?:from start|starting)\b",
                    low,
                )
            ),
            (
                ((5, 0), 8),
                ((4, 3), 8),
                ((1, 7), 7),
            ),
        ),
        T(
            "count_consistent_strings",
            "def count_consistent_strings(allowed, words):\n"
            '    """Count words whose characters are all in allowed (LeetCode 1684)."""\n'
            "    ok = set(allowed)\n"
            "    return sum(1 for w in words if set(w) <= ok)\n",
            lambda low: bool(
                re.search(
                    r"\bcount[_ ]consistent[_ ]strings\b|"
                    r"\bcount (?:the )?number of consistent strings\b|"
                    r"\bconsistent strings\b",
                    low,
                )
            ),
            (
                (("ab", ["ad", "bd", "aaab", "baa", "badab"]), 2),
                (("abc", ["a", "b", "c", "ab", "ac", "bc", "abc"]), 7),
                (("cad", ["cc", "acd", "b", "ba", "bac", "bad", "ac", "d"]), 4),
            ),
        ),
        T(
            "unique_ints_sum_zero",
            "def unique_ints_sum_zero(n):\n"
            '    """n unique integers that sum to zero (LeetCode 1304)."""\n'
            "    out = []\n"
            "    for i in range(1, n // 2 + 1):\n"
            "        out.append(i)\n"
            "        out.append(-i)\n"
            "    if n % 2:\n"
            "        out.append(0)\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bunique[_ ]ints[_ ]sum[_ ]zero\b|"
                    r"\bfind n unique integers sum up to zero\b|"
                    r"\bunique integers (?:that )?sum(?:ming)? to zero\b|"
                    r"\bn unique integers sum to zero\b",
                    low,
                )
            ),
            (
                ((5,), [1, -1, 2, -2, 0]),
                ((3,), [1, -1, 0]),
                ((1,), [0]),
            ),
        ),
        T(
            "max_score_after_splitting",
            "def max_score_after_splitting(s):\n"
            '    """Max score splitting binary string into two non-empty parts (LeetCode 1422)."""\n'
            "    best = 0\n"
            "    for i in range(1, len(s)):\n"
            "        left = s[:i].count('0')\n"
            "        right = s[i:].count('1')\n"
            "        best = max(best, left + right)\n"
            "    return best\n",
            lambda low: bool(
                re.search(
                    r"\bmax[_ ]score[_ ]after[_ ]splitting\b|"
                    r"\bmaximum score after splitting (?:a )?string\b|"
                    r"\bmax score after splitting\b",
                    low,
                )
            ),
            (
                (("011101",), 5),
                (("00111",), 5),
                (("1111",), 3),
            ),
        ),
    ]
