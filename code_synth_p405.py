"""Cycle 405: design_circular_deque, different_ways_add_parentheses,
design_hit_counter, exam_room, range_module, nested_list_weight_sum.

Educational pure-Python with examples for CodeAgent verify.
Higher pack number wins name collisions (loader discovers descending).
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "design_circular_deque",
            '''def design_circular_deque(ops):
    """Design a circular double-ended queue (LeetCode 641).

    ops: list of (\"MyCircularDeque\"|\"insertFront\"|\"insertLast\"|
    \"deleteFront\"|\"deleteLast\"|\"getFront\"|\"getRear\"|\"isEmpty\"|\"isFull\", *args).
    First op constructs with capacity. Returns list of results (None for void).
    """
    class MyCircularDeque:
        def __init__(self, k: int):
            self.k = k
            self.q = [0] * k
            self.head = 0
            self.tail = 0
            self.size = 0

        def insertFront(self, value: int) -> bool:
            if self.isFull():
                return False
            self.head = (self.head - 1) % self.k
            self.q[self.head] = value
            self.size += 1
            return True

        def insertLast(self, value: int) -> bool:
            if self.isFull():
                return False
            self.q[self.tail] = value
            self.tail = (self.tail + 1) % self.k
            self.size += 1
            return True

        def deleteFront(self) -> bool:
            if self.isEmpty():
                return False
            self.head = (self.head + 1) % self.k
            self.size -= 1
            return True

        def deleteLast(self) -> bool:
            if self.isEmpty():
                return False
            self.tail = (self.tail - 1) % self.k
            self.size -= 1
            return True

        def getFront(self) -> int:
            return -1 if self.isEmpty() else self.q[self.head]

        def getRear(self) -> int:
            return -1 if self.isEmpty() else self.q[(self.tail - 1) % self.k]

        def isEmpty(self) -> bool:
            return self.size == 0

        def isFull(self) -> bool:
            return self.size == self.k

    out = []
    obj = None
    for op in ops:
        name, *args = op
        if name == "MyCircularDeque":
            obj = MyCircularDeque(args[0])
            out.append(None)
        else:
            out.append(getattr(obj, name)(*args))
    return out
''',
            lambda low: bool(
                re.search(
                    r"\bdesign (a )?circular deque\b|"
                    r"\bcircular double[- ]ended queue\b|"
                    r"\bmycirculardeque\b|"
                    r"\bleetcode 641\b",
                    low,
                )
            ),
            examples=[
                (
                    (
                        [
                            ("MyCircularDeque", 3),
                            ("insertLast", 1),
                            ("insertLast", 2),
                            ("insertFront", 3),
                            ("insertFront", 4),
                            ("getRear",),
                            ("isFull",),
                            ("deleteLast",),
                            ("insertFront", 4),
                            ("getFront",),
                        ],
                    ),
                    [None, True, True, True, False, 2, True, True, True, 4],
                ),
            ],
        ),
        T(
            "different_ways_add_parentheses",
            '''def different_ways_add_parentheses(expression: str):
    """All possible results from computing expression with different
    parenthesizations (LeetCode 241).

    expression contains digits and operators +, -, *.
    """
    memo = {}

    def ways(s: str):
        if s in memo:
            return memo[s]
        if s.isdigit():
            memo[s] = [int(s)]
            return memo[s]
        res = []
        for i, ch in enumerate(s):
            if ch in "+-*":
                left = ways(s[:i])
                right = ways(s[i + 1 :])
                for a in left:
                    for b in right:
                        if ch == "+":
                            res.append(a + b)
                        elif ch == "-":
                            res.append(a - b)
                        else:
                            res.append(a * b)
        memo[s] = res
        return res

    return sorted(ways(expression))
''',
            lambda low: bool(
                re.search(
                    r"\bdifferent ways to add parentheses\b|"
                    r"\bways to add parentheses\b|"
                    r"\bleetcode 241\b",
                    low,
                )
            ),
            examples=[
                (("2-1-1",), [0, 2]),
                (("2*3-4*5",), [-34, -14, -10, -10, 10]),
            ],
        ),
        T(
            "design_hit_counter",
            '''def design_hit_counter(ops):
    """Design a hit counter that counts hits in the past 5 minutes (LeetCode 362).

    ops: list of (\"HitCounter\"|\"hit\"|\"getHits\", *args). Times are seconds.
    Window is 300 seconds. Returns list of results (None for void).
    """
    from collections import deque

    class HitCounter:
        def __init__(self):
            self.q = deque()

        def hit(self, timestamp: int) -> None:
            self.q.append(timestamp)

        def getHits(self, timestamp: int) -> int:
            while self.q and self.q[0] <= timestamp - 300:
                self.q.popleft()
            return len(self.q)

    out = []
    obj = None
    for op in ops:
        name, *args = op
        if name == "HitCounter":
            obj = HitCounter()
            out.append(None)
        else:
            out.append(getattr(obj, name)(*args))
    return out
''',
            lambda low: bool(
                re.search(
                    r"\bdesign (a )?hit counter\b|"
                    r"\bhit counter\b|"
                    r"\bleetcode 362\b",
                    low,
                )
            )
            and "rate" not in low,
            examples=[
                (
                    (
                        [
                            ("HitCounter",),
                            ("hit", 1),
                            ("hit", 2),
                            ("hit", 3),
                            ("getHits", 4),
                            ("hit", 300),
                            ("getHits", 300),
                            ("getHits", 301),
                        ],
                    ),
                    [None, None, None, None, 3, None, 4, 3],
                ),
            ],
        ),
        T(
            "exam_room",
            '''def exam_room(ops):
    """Exam room seat allocation maximizing distance to closest person (LeetCode 855).

    ops: list of (\"ExamRoom\"|\"seat\"|\"leave\", *args). n seats 0..n-1.
    Returns list of results (None for void leave).
    """
    import bisect

    class ExamRoom:
        def __init__(self, n: int):
            self.n = n
            self.seats = []

        def seat(self) -> int:
            if not self.seats:
                self.seats.append(0)
                return 0
            max_dist = self.seats[0]
            pos = 0
            for i in range(1, len(self.seats)):
                d = (self.seats[i] - self.seats[i - 1]) // 2
                if d > max_dist:
                    max_dist = d
                    pos = self.seats[i - 1] + d
            if self.n - 1 - self.seats[-1] > max_dist:
                pos = self.n - 1
            bisect.insort(self.seats, pos)
            return pos

        def leave(self, p: int) -> None:
            self.seats.remove(p)

    out = []
    obj = None
    for op in ops:
        name, *args = op
        if name == "ExamRoom":
            obj = ExamRoom(args[0])
            out.append(None)
        else:
            out.append(getattr(obj, name)(*args))
    return out
''',
            lambda low: bool(
                re.search(
                    r"\bexam room\b|"
                    r"\bleetcode 855\b",
                    low,
                )
            ),
            examples=[
                (
                    (
                        [
                            ("ExamRoom", 10),
                            ("seat",),
                            ("seat",),
                            ("seat",),
                            ("seat",),
                            ("leave", 4),
                            ("seat",),
                        ],
                    ),
                    [None, 0, 9, 4, 2, None, 5],
                ),
            ],
        ),
        T(
            "range_module",
            '''def range_module(ops):
    """Track ranges of numbers under add/remove/query (LeetCode 715).

    ops: list of (\"RangeModule\"|\"addRange\"|\"removeRange\"|\"queryRange\", *args).
    Half-open intervals [left, right). Returns list of results.
    """
    import bisect

    class RangeModule:
        def __init__(self):
            self.intervals = []

        def addRange(self, left: int, right: int) -> None:
            i = bisect.bisect_left(self.intervals, left)
            j = bisect.bisect_right(self.intervals, right)
            new = []
            if i % 2 == 1:
                i -= 1
                left = self.intervals[i]
            if j % 2 == 1:
                right = self.intervals[j]
                j += 1
            new = self.intervals[:i] + [left, right] + self.intervals[j:]
            self.intervals = new

        def queryRange(self, left: int, right: int) -> bool:
            i = bisect.bisect_right(self.intervals, left)
            j = bisect.bisect_left(self.intervals, right)
            return i == j and i % 2 == 1

        def removeRange(self, left: int, right: int) -> None:
            i = bisect.bisect_left(self.intervals, left)
            j = bisect.bisect_right(self.intervals, right)
            new = []
            if i % 2 == 1:
                i -= 1
                new = self.intervals[: i + 1] + [left]
            else:
                new = self.intervals[:i]
            if j % 2 == 1:
                new += [right] + self.intervals[j:]
            else:
                new += self.intervals[j:]
            self.intervals = new

    out = []
    obj = None
    for op in ops:
        name, *args = op
        if name == "RangeModule":
            obj = RangeModule()
            out.append(None)
        else:
            out.append(getattr(obj, name)(*args))
    return out
''',
            lambda low: bool(
                re.search(
                    r"\brange module\b|"
                    r"\bleetcode 715\b",
                    low,
                )
            ),
            examples=[
                (
                    (
                        [
                            ("RangeModule",),
                            ("addRange", 10, 20),
                            ("removeRange", 14, 16),
                            ("queryRange", 10, 14),
                            ("queryRange", 13, 15),
                            ("queryRange", 16, 17),
                        ],
                    ),
                    [None, None, None, True, False, True],
                ),
            ],
        ),
        T(
            "nested_list_weight_sum",
            '''def nested_list_weight_sum(nestedList):
    """Weighted sum of all integers in nested list (LeetCode 339).

    nestedList is a nested list of integers; weight = depth (1-based).
    Educational: nestedList elements are int or list.
    """
    def dfs(lst, depth):
        total = 0
        for x in lst:
            if isinstance(x, list):
                total += dfs(x, depth + 1)
            else:
                total += x * depth
        return total

    return dfs(nestedList, 1)
''',
            lambda low: bool(
                re.search(
                    r"\bnested list weight sum\b|"
                    r"\bweight sum of nested list\b|"
                    r"\bleetcode 339\b",
                    low,
                )
            )
            and "ii" not in low
            and "2" not in low.split("sum")[-1][:4],
            examples=[
                (([[1, 1], 2, [1, 1]],), 10),
                (([1, [4, [6]]],), 27),
            ],
        ),
    ]
