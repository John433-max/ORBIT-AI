"""ORBIT code_synth template pack (Cycle 244 split)."""
from __future__ import annotations
import re
from code_synth import Template, _TWO

def templates():
    return [

Template(
            "add",
            "def add(a, b):\n"
            '    """Return the sum of a and b."""\n'
            "    return a + b\n",
            lambda low: bool(
                "binary" not in low
                and "linked" not in low
                and "list" not in low
                and " ii" not in low
                and "leetcode" not in low
                and (
                    re.search(r"add(s|ing)?\b.{0,24}\b" + _TWO + r"\b.{0,24}\b(number|int|value)", low)
                    or "adds two" in low
                )
            ),
            (((1, 2), 3), ((-4, 10), 6)),
        ),
        # ... truncated for brevity in this simulation, but in real it would be full
    ]
