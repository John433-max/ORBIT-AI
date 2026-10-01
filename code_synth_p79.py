"""Cycle 343: unused Easy — chessboard color / balls in a box /
base-k digit sum / longest button push / ones-vs-zeros runs / word sum."""

from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "square_is_white",
            "def square_is_white(coordinates):\n"
            '    """True when the chessboard square is white (LeetCode 1812)."""\n'
            "    file = ord(coordinates[0]) - ord('a')\n"
            "    rank = int(coordinates[1])\n"
            "    return (file + rank) % 2 == 0\n",
            lambda low: "color of a chessboard square" in low,
            (
                (("a1",), False),
                (("h3",), True),
                (("c7",), False),
            ),
        ),
        T(
            "count_balls",
            "def count_balls(low_limit, high_limit):\n"
            '    """Max balls sharing a digit-sum box (LeetCode 1742)."""\n'
            "    boxes = {}\n"
            "    best = 0\n"
            "    for n in range(low_limit, high_limit + 1):\n"
            "        digit_sum = 0\n"
            "        value = n\n"
            "        while value:\n"
            "            digit_sum += value % 10\n"
            "            value //= 10\n"
            "        boxes[digit_sum] = boxes.get(digit_sum, 0) + 1\n"
            "        if boxes[digit_sum] > best:\n"
            "            best = boxes[digit_sum]\n"
            "    return best\n",
            lambda low: "balls in a box" in low,
            (
                ((1, 10), 2),
                ((5, 15), 2),
                ((19, 28), 2),
            ),
        ),
        T(
            "sum_base",
            "def sum_base(n, k):\n"
            '    """Sum of base-k digits of n (LeetCode 1837)."""\n'
            "    total = 0\n"
            "    while n:\n"
            "        total += n % k\n"
            "        n //= k\n"
            "    return total\n",
            lambda low: "digits in base" in low,
            (
                ((34, 6), 9),
                ((10, 10), 1),
            ),
        ),
        T(
            "button_with_longest_time",
            "def button_with_longest_time(events):\n"
            '    """Button index with the longest press; ties take the smaller index (LeetCode 3386)."""\n'
            "    best_button = events[0][0]\n"
            "    best = events[0][1]\n"
            "    prev = events[0][1]\n"
            "    for index, time in events[1:]:\n"
            "        duration = time - prev\n"
            "        if duration > best or (duration == best and index < best_button):\n"
            "            best = duration\n"
            "            best_button = index\n"
            "        prev = time\n"
            "    return best_button\n",
            lambda low: "longest push" in low,
            (
                (([[1, 2], [2, 5], [3, 9], [1, 15]],), 1),
                (([[10, 5], [1, 7]],), 10),
                (([[1, 2], [2, 4]],), 1),
            ),
        ),
        T(
            "check_zero_ones",
            "def check_zero_ones(s):\n"
            '    """Longest contiguous ones run is longer than the zeros run (LeetCode 1869)."""\n'
            "    ones = zeros = run = 0\n"
            "    prev = ''\n"
            "    for ch in s + 'x':\n"
            "        if ch == prev:\n"
            "            run += 1\n"
            "        else:\n"
            "            if prev == '1':\n"
            "                ones = max(ones, run)\n"
            "            elif prev == '0':\n"
            "                zeros = max(zeros, run)\n"
            "            run = 1\n"
            "            prev = ch\n"
            "    return ones > zeros\n",
            lambda low: "contiguous segments of ones" in low,
            (
                (("1101",), True),
                (("111000",), False),
                (("110100010",), False),
            ),
        ),
        T(
            "is_sum_equal",
            "def is_sum_equal(first_word, second_word, target_word):\n"
            '    """Word values (a=0..j=9) satisfy first + second == target (LeetCode 1880)."""\n'
            "    def value(word):\n"
            "        number = 0\n"
            "        for ch in word:\n"
            "            number = number * 10 + (ord(ch) - 97)\n"
            "        return number\n"
            "    return value(first_word) + value(second_word) == value(target_word)\n",
            lambda low: "summation of two words" in low,
            (
                (("acb", "cba", "cdb"), True),
                (("aaa", "a", "aab"), False),
                (("aaa", "a", "aaaa"), True),
            ),
        ),
    ]
