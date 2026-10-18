"""Cycle 646 (p354): six classic educational templates.

largest_number (179), remove_k_digits (402), longest_turbulent_subarray (978),
exclusive_time_of_functions (636), my_calendar_book (729), replace_words (648).
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "largest_number",
            '''def largest_number(nums):
    """Arrange non-negative integers to form the largest number (LeetCode 179).

    Custom order: a before b when a+b > b+a. Leading zeros collapse to "0".
    """
    from functools import cmp_to_key

    parts = [str(n) for n in nums]
    if not parts:
        return "0"

    def cmp(a, b):
        ab, ba = a + b, b + a
        if ab > ba:
            return -1
        if ab < ba:
            return 1
        return 0

    parts.sort(key=cmp_to_key(cmp))
    if parts[0] == "0":
        return "0"
    return "".join(parts)
''',
            lambda low: bool(
                re.search(
                    r"\bform(?:\s+the)?\s+largest\s+number\b|"
                    r"\barrange\s+(?:numbers\s+)?to\s+form\s+(?:the\s+)?largest\b|"
                    r"\bleetcode\s+179\b",
                    low,
                )
            )
            and "values" not in low
            and "good integer" not in low
            and "population" not in low
            and "twice" not in low
            and "second" not in low
            and "parity" not in low
            and "swaps" not in low,
            (
                (([10, 2],), "210"),
                (([3, 30, 34, 5, 9],), "9534330"),
                (([0, 0],), "0"),
            ),
        ),
        T(
            "remove_k_digits",
            '''def remove_k_digits(num, k):
    """Remove k digits so the remaining number is smallest (LeetCode 402).

    Monotonic increasing stack; strip leading zeros; empty becomes "0".
    """
    stack = []
    for d in num:
        while stack and k and stack[-1] > d:
            stack.pop()
            k -= 1
        stack.append(d)
    while k and stack:
        stack.pop()
        k -= 1
    res = "".join(stack).lstrip("0")
    return res or "0"
''',
            lambda low: bool(
                re.search(
                    r"\bremove[_ ]k[_ ]digits?\b|"
                    r"\bremove\s+\d+\s+digits?\b|"
                    r"\bsmallest\s+number\s+by\s+removing\s+k\b|"
                    r"\bleetcode\s+402\b",
                    low,
                )
            )
            and "adjacent" not in low,
            (
                (("1432219", 3), "1219"),
                (("10200", 1), "200"),
                (("10", 2), "0"),
            ),
        ),
        T(
            "longest_turbulent_subarray",
            '''def longest_turbulent_subarray(arr):
    """Longest turbulent subarray; comparisons alternate > < > < (LeetCode 978)."""
    n = len(arr)
    if n < 2:
        return n
    best = 1
    inc = dec = 1
    for i in range(1, n):
        if arr[i] > arr[i - 1]:
            inc = dec + 1
            dec = 1
        elif arr[i] < arr[i - 1]:
            dec = inc + 1
            inc = 1
        else:
            inc = dec = 1
        best = max(best, inc, dec)
    return best
''',
            lambda low: bool(
                re.search(
                    r"\bturbulent(?:[_ ]subarray)?\b|"
                    r"\blongest[_ ]turbulent\b|"
                    r"\bleetcode\s+978\b",
                    low,
                )
            ),
            (
                (([9, 4, 2, 10, 7, 8, 8, 1, 9],), 5),
                (([4, 8, 12, 16],), 2),
                (([100],), 1),
            ),
        ),
        T(
            "exclusive_time_of_functions",
            '''def exclusive_time_of_functions(n, logs):
    """Exclusive time of n functions from start/end logs (LeetCode 636).

    Stack of active function ids; credit time slices on start/end.
    """
    times = [0] * n
    stack = []
    prev = 0
    for log in logs:
        fid_s, typ, ts_s = log.split(":")
        fid, ts = int(fid_s), int(ts_s)
        if typ == "start":
            if stack:
                times[stack[-1]] += ts - prev
            stack.append(fid)
            prev = ts
        else:
            times[stack.pop()] += ts - prev + 1
            prev = ts + 1
    return times
''',
            lambda low: bool(
                re.search(
                    r"\bexclusive[_ ]time(?:[_ ]of[_ ]functions?)?\b|"
                    r"\bfunction[_ ]exclusive[_ ]time\b|"
                    r"\bleetcode\s+636\b",
                    low,
                )
            ),
            (
                (
                    (2, ["0:start:0", "1:start:2", "1:end:5", "0:end:6"]),
                    [3, 4],
                ),
                (
                    (1, ["0:start:0", "0:end:0"]),
                    [1],
                ),
            ),
        ),
        T(
            "my_calendar_book",
            '''def my_calendar_book(bookings):
    """Process booking requests; return success flags (LeetCode 729 My Calendar I).

    A booking [start, end) is accepted only if it overlaps no prior booking.
    """
    booked = []
    result = []
    for start, end in bookings:
        ok = True
        for s, e in booked:
            if start < e and end > s:
                ok = False
                break
        if ok:
            booked.append((start, end))
        result.append(ok)
    return result
''',
            lambda low: bool(
                re.search(
                    r"\bmy[_ ]calendar(?:[_ ]i)?\b|"
                    r"\bbook(?:ing)?\s+(?:intervals|appointments)\b|"
                    r"\bcalendar\s+book\b|"
                    r"\bleetcode\s+729\b",
                    low,
                )
            )
            and "ii" not in low
            and "iii" not in low,
            (
                (([[10, 20], [15, 25], [20, 30]],), [True, False, True]),
                (([[10, 20]],), [True]),
            ),
        ),
        T(
            "replace_words",
            '''def replace_words(dictionary, sentence):
    """Replace each word with the shortest dictionary root that is a prefix (LeetCode 648)."""
    roots = sorted(dictionary, key=len)
    words = sentence.split()
    for i, w in enumerate(words):
        for root in roots:
            if w.startswith(root):
                words[i] = root
                break
    return " ".join(words)
''',
            lambda low: bool(
                re.search(
                    r"\breplace[_ ]words?\b|"
                    r"\breplace\s+(?:each\s+)?word\s+with\s+(?:its\s+)?(?:root|prefix)\b|"
                    r"\bdictionary\s+(?:root|prefix)\s+replace\b|"
                    r"\bleetcode\s+648\b",
                    low,
                )
            )
            and "elements" not in low
            and "value" not in low,
            (
                (
                    (["cat", "bat", "rat"], "the cattle was rattled by the battery"),
                    "the cat was rat by the bat",
                ),
                ((["a", "b", "c"], "aadsfasf absbs bbab cadsfafs"), "a a b c"),
            ),
        ),
    ]
