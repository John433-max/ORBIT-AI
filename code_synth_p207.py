"""Cycle 491: phrase-specific string/list utilities that still fell through the router."""
from __future__ import annotations

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "remove_vowels",
            "def remove_vowels(s):\n"
            '    """Drop aeiou (any case). Other characters stay in order."""\n'
            "    vowels = set('aeiouAEIOU')\n"
            "    return ''.join(ch for ch in str(s) if ch not in vowels)\n",
            lambda low: "vowel" in low and ("remov" in low or "strip" in low) and "count" not in low,
            (
                (("hello",), "hll"),
                (("AEIOU",), ""),
                (("xyz",), "xyz"),
            ),
        ),
        T(
            "every_other",
            "def every_other(items):\n"
            '    """Return items at even indexes (0, 2, 4, ...)."""\n'
            "    return list(items)[::2]\n",
            lambda low: "every other" in low and "string" not in low,
            (
                (([1, 2, 3, 4, 5],), [1, 3, 5]),
                ((["a"],), ["a"]),
                (([],), []),
            ),
        ),
        T(
            "join_list",
            "def join_list(items, sep):\n"
            '    """Join items with sep after stringifying each item."""\n'
            "    return str(sep).join(str(item) for item in items)\n",
            lambda low: (
                "join" in low
                and "list" in low
                and ("separator" in low or "sep" in low)
                and "sql" not in low
            ),
            (
                ((["a", "b", "c"], "-"), "a-b-c"),
                (([1, 2], ","), "1,2"),
                (([], ","), ""),
            ),
        ),
        T(
            "split_whitespace",
            "def split_whitespace(s):\n"
            '    """Split on any whitespace and drop empty pieces."""\n'
            "    return str(s).split()\n",
            lambda low: "whitespace" in low and "split" in low and "join" not in low,
            (
                (("a  b\tc",), ["a", "b", "c"]),
                (("  ",), []),
                (("one",), ["one"]),
            ),
        ),
        T(
            "capitalize_first",
            "def capitalize_first(s):\n"
            '    """Uppercase the first character; leave the rest unchanged."""\n'
            "    s = str(s)\n"
            "    if not s:\n"
            "        return s\n"
            "    return s[0].upper() + s[1:]\n",
            lambda low: (
                "capital" in low
                and "first" in low
                and "letter" in low
                and "word" not in low
            ),
            (
                (("hello",), "Hello"),
                (("A",), "A"),
                (("",), ""),
            ),
        ),
        T(
            "all_equal",
            "def all_equal(items):\n"
            '    """True if every item equals the first. Empty is True."""\n'
            "    items = list(items)\n"
            "    if not items:\n"
            "        return True\n"
            "    head = items[0]\n"
            "    return all(item == head for item in items)\n",
            lambda low: "equal" in low and ("all item" in low or "all items" in low or "all elements" in low),
            (
                (([2, 2, 2],), True),
                (([1, 2],), False),
                (([],), True),
            ),
        ),
    ]
