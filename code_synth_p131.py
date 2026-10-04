"""Cycle 407: classic algorithm asks that returned NotImplemented drafts.

Probes:
- implement merge sort
- implement quicksort in python
- create a class that implements a stack
- write code to parse a CSV line into fields

Matchers exclude merge-sorted arrays and min-stack so existing rows stay put.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "merge_sort",
            "def merge_sort(items):\n"
            '    """Return a new list sorted with merge sort."""\n'
            "    data = list(items)\n"
            "    if len(data) <= 1:\n"
            "        return data\n"
            "    mid = len(data) // 2\n"
            "    left = merge_sort(data[:mid])\n"
            "    right = merge_sort(data[mid:])\n"
            "    out = []\n"
            "    i = j = 0\n"
            "    while i < len(left) and j < len(right):\n"
            "        if left[i] <= right[j]:\n"
            "            out.append(left[i])\n"
            "            i += 1\n"
            "        else:\n"
            "            out.append(right[j])\n"
            "            j += 1\n"
            "    out.extend(left[i:])\n"
            "    out.extend(right[j:])\n"
            "    return out\n",
            lambda low: bool(re.search(r"\bmerge\s*sort\b", low) or "mergesort" in low)
            and "sorted" not in low
            and "array" not in low,
            examples=(
                (([3, 1, 2],), [1, 2, 3]),
                (([],), []),
                (([5, 5, 1],), [1, 5, 5]),
            ),
        ),
        T(
            "quick_sort",
            "def quick_sort(items):\n"
            '    """Return a new list sorted with quicksort (Lomuto)."""\n'
            "    data = list(items)\n"
            "\n"
            "    def _sort(lo, hi):\n"
            "        if lo >= hi:\n"
            "            return\n"
            "        pivot = data[hi]\n"
            "        i = lo\n"
            "        for j in range(lo, hi):\n"
            "            if data[j] <= pivot:\n"
            "                data[i], data[j] = data[j], data[i]\n"
            "                i += 1\n"
            "        data[i], data[hi] = data[hi], data[i]\n"
            "        _sort(lo, i - 1)\n"
            "        _sort(i + 1, hi)\n"
            "\n"
            "    _sort(0, len(data) - 1)\n"
            "    return data\n",
            lambda low: bool(re.search(r"\bquick\s*sort\b", low) or "quicksort" in low),
            examples=(
                (([3, 1, 4, 2],), [1, 2, 3, 4]),
                (([1],), [1]),
                (([2, 2, 1],), [1, 2, 2]),
            ),
        ),
        T(
            "stack_class",
            "def stack_demo(values):\n"
            '    """Push values then pop them (LIFO) to exercise Stack."""\n'
            "    st = Stack()\n"
            "    for value in values:\n"
            "        st.push(value)\n"
            "    out = []\n"
            "    while len(st):\n"
            "        out.append(st.pop())\n"
            "    return out\n"
            "\n"
            "\n"
            "class Stack:\n"
            '    """List-backed stack."""\n'
            "\n"
            "    def __init__(self):\n"
            "        self._data = []\n"
            "\n"
            "    def push(self, value):\n"
            "        self._data.append(value)\n"
            "\n"
            "    def pop(self):\n"
            "        if not self._data:\n"
            "            raise IndexError('pop from empty stack')\n"
            "        return self._data.pop()\n"
            "\n"
            "    def peek(self):\n"
            "        if not self._data:\n"
            "            raise IndexError('peek from empty stack')\n"
            "        return self._data[-1]\n"
            "\n"
            "    def __len__(self):\n"
            "        return len(self._data)\n",
            lambda low: bool(
                (
                    "implement a stack" in low
                    or "implements a stack" in low
                    or "class that implements a stack" in low
                    or re.search(r"\bstack class\b", low)
                )
                and "min stack" not in low
                and "min_stack" not in low
                and "queue" not in low
            ),
            examples=(
                (([1, 2, 3],), [3, 2, 1]),
                (([],), []),
            ),
        ),
        T(
            "parse_csv_line",
            "def parse_csv_line(line):\n"
            '    """Split one CSV line into fields, honoring simple quotes."""\n'
            "    fields = []\n"
            "    buf = []\n"
            "    in_quotes = False\n"
            "    i = 0\n"
            "    text = '' if line is None else str(line)\n"
            "    while i < len(text):\n"
            "        ch = text[i]\n"
            "        if ch == '\"':\n"
            "            if in_quotes and i + 1 < len(text) and text[i + 1] == '\"':\n"
            "                buf.append('\"')\n"
            "                i += 2\n"
            "                continue\n"
            "            in_quotes = not in_quotes\n"
            "        elif ch == ',' and not in_quotes:\n"
            "            fields.append(''.join(buf))\n"
            "            buf = []\n"
            "        else:\n"
            "            buf.append(ch)\n"
            "        i += 1\n"
            "    fields.append(''.join(buf))\n"
            "    return fields\n",
            lambda low: bool(
                ("csv" in low and ("parse" in low or "split" in low or "fields" in low))
                and "file" not in low
            ),
            examples=(
                (("a,b,c",), ["a", "b", "c"]),
                (('x,"y,z",w',), ["x", "y,z", "w"]),
                (("",), [""]),
            ),
        ),
    ]
