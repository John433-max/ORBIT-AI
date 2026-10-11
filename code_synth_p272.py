"""Cycle 560: Priority-queue decrease-key + functional PQ ops gaps.

Widens educational coverage for min priority queues with decrease-key
and natural 'push/pop/peek' phrasing that does not require 'class'.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "priority_queue_decrease_key",
            "def priority_queue_decrease_key(ops):\n"
            '    """Min priority queue supporting push, decrease_key, and pop_min.\n'
            "\n"
            "    ops is a list of tuples:\n"
            "      ('push', item, priority)\n"
            "      ('decrease', item, new_priority)  # only if item is present\n"
            "      ('pop',)\n"
            "    Returns the list of values produced by pop ops (None if empty).\n"
            '    """\n'
            "    # item -> (priority, heap_index); heap stores (priority, item)\n"
            "    heap = []\n"
            "    index = {}\n"
            "\n"
            "    def _sift_up(i):\n"
            "        while i > 0:\n"
            "            p = (i - 1) // 2\n"
            "            if heap[i][0] >= heap[p][0]:\n"
            "                break\n"
            "            heap[i], heap[p] = heap[p], heap[i]\n"
            "            index[heap[i][1]] = i\n"
            "            index[heap[p][1]] = p\n"
            "            i = p\n"
            "\n"
            "    def _sift_down(i):\n"
            "        n = len(heap)\n"
            "        while True:\n"
            "            l, r = 2 * i + 1, 2 * i + 2\n"
            "            smallest = i\n"
            "            if l < n and heap[l][0] < heap[smallest][0]:\n"
            "                smallest = l\n"
            "            if r < n and heap[r][0] < heap[smallest][0]:\n"
            "                smallest = r\n"
            "            if smallest == i:\n"
            "                break\n"
            "            heap[i], heap[smallest] = heap[smallest], heap[i]\n"
            "            index[heap[i][1]] = i\n"
            "            index[heap[smallest][1]] = smallest\n"
            "            i = smallest\n"
            "\n"
            "    out = []\n"
            "    for op in ops:\n"
            "        kind = op[0]\n"
            "        if kind == 'push':\n"
            "            item, pr = op[1], op[2]\n"
            "            if item in index:\n"
            "                continue\n"
            "            heap.append((pr, item))\n"
            "            index[item] = len(heap) - 1\n"
            "            _sift_up(len(heap) - 1)\n"
            "        elif kind == 'decrease':\n"
            "            item, pr = op[1], op[2]\n"
            "            if item not in index:\n"
            "                continue\n"
            "            i = index[item]\n"
            "            if pr >= heap[i][0]:\n"
            "                continue\n"
            "            heap[i] = (pr, item)\n"
            "            _sift_up(i)\n"
            "        elif kind == 'pop':\n"
            "            if not heap:\n"
            "                out.append(None)\n"
            "                continue\n"
            "            pr, item = heap[0]\n"
            "            last = heap.pop()\n"
            "            del index[item]\n"
            "            if heap:\n"
            "                heap[0] = last\n"
            "                index[last[1]] = 0\n"
            "                _sift_down(0)\n"
            "            out.append(item)\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\b(?:min[- ]?)?priority[- ]?queue.{0,40}decrease[- ]?key\b|"
                    r"\bdecrease[- ]?key.{0,40}priority[- ]?queue\b|"
                    r"\bpriority[- ]?queue with decrease\b|"
                    r"\bdecrease.?key (?:on )?(?:a )?min(?:imum)? (?:priority[- ]?)?queue\b",
                    low,
                )
            )
            and "fibonacci" not in low,
            examples=(
                (
                    (
                        [
                            ("push", "a", 5),
                            ("push", "b", 3),
                            ("decrease", "a", 1),
                            ("pop",),
                            ("pop",),
                        ],
                    ),
                    ["a", "b"],
                ),
                (
                    (
                        [
                            ("push", "x", 10),
                            ("pop",),
                            ("pop",),
                        ],
                    ),
                    ["x", None],
                ),
                (
                    (
                        [
                            ("push", "c", 2),
                            ("push", "d", 4),
                            ("decrease", "d", 1),
                            ("pop",),
                        ],
                    ),
                    ["d"],
                ),
            ),
        ),
        T(
            "priority_queue_ops",
            "def priority_queue_ops(values):\n"
            '    """Push all values into a min priority queue then pop until empty."""\n'
            "    import heapq\n"
            "    h = []\n"
            "    for v in values:\n"
            "        heapq.heappush(h, v)\n"
            "    out = []\n"
            "    while h:\n"
            "        out.append(heapq.heappop(h))\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bpriority[- ]?queue ops\b|"
                    r"\bpq ops\b|"
                    r"\bpriority[- ]?queue (?:push.?pop|pop.?push)\b",
                    low,
                )
            )
            and "decrease" not in low
            and "class" not in low,
            examples=(
                (([3, 1, 2],), [1, 2, 3]),
                (([],), []),
                (([4, 4, 0],), [0, 4, 4]),
            ),
        ),
    ]
