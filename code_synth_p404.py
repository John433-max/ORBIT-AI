"""Cycle 404: fill phrase gaps — sum_of_two_integers, encode_decode_strings,
meeting_rooms (can attend), pascals_triangle alias, simplify_path,
remove_invalid_parentheses.

Educational pure-Python with HumanEval-style examples for CodeAgent verify.
Higher pack number wins name collisions (loader discovers descending).
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "sum_of_two_integers",
            '''def sum_of_two_integers(a: int, b: int) -> int:
    """Sum two integers without using + or - operators (LeetCode 371).

    Educational bit-manipulation: XOR for sum bits, AND+shift for carry.
    Python ints are unbounded; mask keeps 32-bit two's-complement semantics.
    """
    mask = 0xFFFFFFFF
    while b & mask:
        carry = (a & b) << 1
        a = a ^ b
        b = carry
    return a & mask if b > mask else a
''',
            lambda low: bool(
                re.search(
                    r"\bsum of two integers\b|"
                    r"\bget[_ ]?sum\b.*\bwithout\b|"
                    r"\badd two integers without\b|"
                    r"\bleetcode 371\b",
                    low,
                )
            )
            and "array" not in low
            and "list" not in low,
            examples=[((1, 2), 3), ((2, 3), 5), ((-1, 1), 0)],
        ),
        T(
            "encode_decode_strings",
            '''def encode_decode_strings(strs):
    """Encode a list of strings to one string and decode it back (LeetCode 271).

    Length-prefix encoding: \"{len}#{s}\" concatenated. Returns the decoded list
    (round-trip) so tests can assert equality with the input.
    """
    def encode(xs):
        return "".join(f"{len(s)}#{s}" for s in xs)

    def decode(s):
        out = []
        i = 0
        n = len(s)
        while i < n:
            j = s.index("#", i)
            length = int(s[i:j])
            out.append(s[j + 1 : j + 1 + length])
            i = j + 1 + length
        return out

    return decode(encode(list(strs)))
''',
            lambda low: bool(
                re.search(
                    r"\bencode (and )?decode strings?\b|"
                    r"\bencode[_ ]decode[_ ]strings?\b|"
                    r"\bleetcode 271\b",
                    low,
                )
            ),
            examples=[
                ((["hello", "world"],), ["hello", "world"]),
                (([""],), [""]),
                ((["a", "bc", "def"],), ["a", "bc", "def"]),
            ],
        ),
        T(
            "meeting_rooms",
            '''def meeting_rooms(intervals):
    """True if a person can attend all meetings (LeetCode 252).

    Sort by start; fail if any meeting starts before the previous ends.
    intervals: list of [start, end].
    """
    if not intervals:
        return True
    intervals = sorted(intervals, key=lambda x: x[0])
    for i in range(1, len(intervals)):
        if intervals[i][0] < intervals[i - 1][1]:
            return False
    return True
''',
            lambda low: bool(
                re.search(
                    r"\bcan attend (all )?meetings?\b|"
                    r"\bmeeting rooms?\b(?!.*\bii\b)(?!.*\b2\b)|"
                    r"\bleetcode 252\b",
                    low,
                )
            )
            and "ii" not in low
            and "minimum" not in low
            and "rooms ii" not in low,
            examples=[
                (([[0, 30], [5, 10], [15, 20]],), False),
                (([[7, 10], [2, 4]],), True),
                (([[1, 5], [5, 6]],), True),
            ],
        ),
        T(
            "pascals_triangle",
            '''def pascals_triangle(numRows: int):
    """Generate the first numRows of Pascal's triangle (LeetCode 118).

    Each entry is the sum of the two entries above it.
    """
    if numRows <= 0:
        return []
    rows = [[1]]
    for i in range(1, numRows):
        prev = rows[-1]
        row = [1]
        for j in range(1, i):
            row.append(prev[j - 1] + prev[j])
        row.append(1)
        rows.append(row)
    return rows
''',
            lambda low: bool(
                re.search(
                    r"\bpascals?[' ]?s? triangle\b|"
                    r"\bgenerate pascals? triangle\b|"
                    r"\bleetcode 118\b",
                    low,
                )
            )
            and "ii" not in low
            and "row" not in low.split("triangle")[-1],
            examples=[
                ((1,), [[1]]),
                ((3,), [[1], [1, 1], [1, 2, 1]]),
                ((5,), [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]),
            ],
        ),
        T(
            "simplify_path",
            '''def simplify_path(path: str) -> str:
    """Simplify a Unix-style absolute path (LeetCode 71).

    Resolve \".\" / \"..\" and collapse multiple slashes.
    """
    stack = []
    for part in path.split("/"):
        if part == "" or part == ".":
            continue
        if part == "..":
            if stack:
                stack.pop()
            continue
        stack.append(part)
    return "/" + "/".join(stack)
''',
            lambda low: bool(
                re.search(
                    r"\bsimplify[_ ]path\b|"
                    r"\bunix[_ ]path\b|"
                    r"\bleetcode 71\b",
                    low,
                )
            ),
            examples=[
                (("/home/",), "/home"),
                (("/../",), "/"),
                (("/home//foo/",), "/home/foo"),
                (("/a/./b/../../c/",), "/c"),
            ],
        ),
        T(
            "remove_invalid_parentheses",
            '''def remove_invalid_parentheses(s: str):
    """Remove the minimum number of invalid parentheses (LeetCode 301).

    Returns a list of unique valid strings after minimum removals.
    BFS over deletion states; first level that yields valid strings wins.
    """
    def is_valid(t):
        bal = 0
        for ch in t:
            if ch == "(":
                bal += 1
            elif ch == ")":
                bal -= 1
                if bal < 0:
                    return False
        return bal == 0

    from collections import deque
    seen = {s}
    q = deque([s])
    found = False
    out = []
    while q:
        cur = q.popleft()
        if is_valid(cur):
            out.append(cur)
            found = True
        if found:
            continue
        for i, ch in enumerate(cur):
            if ch not in "()":
                continue
            nxt = cur[:i] + cur[i + 1 :]
            if nxt not in seen:
                seen.add(nxt)
                q.append(nxt)
    return out
''',
            lambda low: bool(
                re.search(
                    r"\bremove invalid parentheses\b|"
                    r"\bminimum (number of )?invalid parentheses\b|"
                    r"\bleetcode 301\b",
                    low,
                )
            ),
            examples=[
                (("()())()",), ["(())()", "()()()"]),
                (("(a)())()",), ["(a())()", "(a)()()"]),
                ((")(",), [""]),
            ],
        ),
    ]
