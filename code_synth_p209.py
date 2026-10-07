"""Cycle 493: list ends, drop ends, swap ends, and split words.

first/last element require element or item so first_missing_positive and
last_stone_weight stay put. drop_* require the word drop. drop_last ignores last-n tails so last_n keeps them. swap_ends requires
both first and last and declines adjacent swaps. split_words requires split
and word so list splits stay with earlier packs.
"""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "first_element",
            "def first_element(items):\n"
            '    """Return the first item, or None if empty."""\n'
            "    items = list(items)\n"
            "    if not items:\n"
            "        return None\n"
            "    return items[0]\n",
            lambda low: (
                "first" in low
                and ("element" in low or "item" in low)
                and "missing" not in low
                and "bad" not in low
                and "version" not in low
                and "positive" not in low
                and "unique" not in low
                and "linked" not in low
                and "node" not in low
                and "drop" not in low
                and "swap" not in low
                and "remove" not in low
                and "last" not in low
            ),
            (
                (([1, 2, 3],), 1),
                ((["a"],), "a"),
                (([],), None),
            ),
        ),
        T(
            "last_element",
            "def last_element(items):\n"
            '    """Return the last item, or None if empty."""\n'
            "    items = list(items)\n"
            "    if not items:\n"
            "        return None\n"
            "    return items[-1]\n",
            lambda low: (
                "last" in low
                and ("element" in low or "item" in low)
                and "stone" not in low
                and "word" not in low
                and "drop" not in low
                and "swap" not in low
                and "remove" not in low
                and "linked" not in low
                and "first" not in low
            ),
            (
                (([1, 2, 3],), 3),
                ((["a"],), "a"),
                (([],), None),
            ),
        ),
        T(
            "drop_first",
            "def drop_first(items):\n"
            '    """Return a copy without the first item."""\n'
            "    return list(items)[1:]\n",
            lambda low: "drop" in low and "first" in low and "last" not in low,
            (
                (([1, 2, 3],), [2, 3]),
                (([1],), []),
                (([],), []),
            ),
        ),
        T(
            "drop_last",
            "def drop_last(items):\n"
            '    """Return a copy without the last item."""\n'
            "    return list(items)[:-1]\n",
            lambda low: (
                "drop" in low
                and "last" in low
                and "first" not in low
                and "last n" not in low
                and "n element" not in low
                and "n item" not in low
            ),
            (
                (([1, 2, 3],), [1, 2]),
                (([1],), []),
                (([],), []),
            ),
        ),
        T(
            "swap_ends",
            "def swap_ends(items):\n"
            '    """Swap the first and last items. Short lists are copied."""\n'
            "    items = list(items)\n"
            "    if len(items) < 2:\n"
            "        return items\n"
            "    items[0], items[-1] = items[-1], items[0]\n"
            "    return items\n",
            lambda low: (
                "swap" in low
                and "first" in low
                and "last" in low
                and "adjacent" not in low
            ),
            (
                (([1, 2, 3, 4],), [4, 2, 3, 1]),
                (([1, 2],), [2, 1]),
                (([1],), [1]),
            ),
        ),
        T(
            "split_words",
            "def split_words(text):\n"
            '    """Split on whitespace. Empty text returns an empty list."""\n'
            "    return str(text).split()\n",
            lambda low: (
                "split" in low
                and "word" in low
                and "list" not in low
                and "linked" not in low
            ),
            (
                (("a b  c",), ["a", "b", "c"]),
                (("",), []),
                (("one",), ["one"]),
            ),
        ),
    ]
