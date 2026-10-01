"""Cycle 306: reformat date / generate odd-count string / special integer / day of week / straight line / n-repeated."""

from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "reformat_date",
            "def reformat_date(date):\n"
            '    """Reformat Day MonthName Year → YYYY-MM-DD (LeetCode 1507)."""\n'
            "    months = {\n"
            "        'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',\n"
            "        'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',\n"
            "        'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12',\n"
            "    }\n"
            "    day, mon, year = date.split()\n"
            "    d = ''.join(ch for ch in day if ch.isdigit()).zfill(2)\n"
            "    return f'{year}-{months[mon]}-{d}'\n",
            lambda low: bool(
                re.search(
                    r"\breformat[_ ]date\b|"
                    r"\breformat the date\b|"
                    r"\bconvert date to yyyy-mm-dd\b",
                    low,
                )
            ),
            (
                (("20th Oct 2052",), "2052-10-20"),
                (("6th Jun 1933",), "1933-06-06"),
                (("26th May 1960",), "1960-05-26"),
            ),
        ),
        T(
            "generate_the_string",
            "def generate_the_string(n):\n"
            '    """String of length n with all odd character counts (LeetCode 1374)."""\n'
            "    n = int(n)\n"
            "    if n % 2 == 1:\n"
            "        return 'a' * n\n"
            "    return 'a' * (n - 1) + 'b'\n",
            lambda low: bool(
                re.search(
                    r"\bgenerate[_ ]the[_ ]string\b|"
                    r"\bgenerate a string with characters that have odd counts\b|"
                    r"\bstring with odd counts\b",
                    low,
                )
            ),
            (
                ((4,), "aaab"),
                ((2,), "ab"),
                ((7,), "aaaaaaa"),
            ),
        ),
        T(
            "find_special_integer",
            "def find_special_integer(arr):\n"
            '    """Element appearing more than 25% of the time (LeetCode 1287)."""\n'
            "    n = len(arr)\n"
            "    need = n // 4 + 1\n"
            "    for i in range(n - need + 1):\n"
            "        if arr[i] == arr[i + need - 1]:\n"
            "            return arr[i]\n"
            "    return arr[-1]\n",
            lambda low: bool(
                re.search(
                    r"\bfind[_ ]special[_ ]integer\b|"
                    r"\belement appearing more than 25\b|"
                    r"\bspecial integer\b",
                    low,
                )
            ),
            (
                (([1, 2, 2, 6, 6, 6, 6, 7, 10],), 6),
                (([1, 1],), 1),
            ),
        ),
        T(
            "day_of_the_week",
            "def day_of_the_week(day, month, year):\n"
            '    """Weekday name for a Gregorian date (LeetCode 1185)."""\n'
            "    import datetime\n"
            "    names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']\n"
            "    return names[datetime.date(year, month, day).weekday()]\n",
            lambda low: bool(
                re.search(
                    r"\bday[_ ]of[_ ]the[_ ]week\b|"
                    r"\bday of the week\b|"
                    r"\bwhat day of the week\b",
                    low,
                )
                and not re.search(r"\bday[_ ]of[_ ](?:the[_ ])?year\b", low)
            ),
            (
                ((31, 8, 2019), "Saturday"),
                ((18, 7, 1999), "Sunday"),
                ((15, 8, 1993), "Sunday"),
            ),
        ),
        T(
            "check_straight_line",
            "def check_straight_line(coordinates):\n"
            '    """True if all points lie on one straight line (LeetCode 1232)."""\n'
            "    (x0, y0), (x1, y1) = coordinates[0], coordinates[1]\n"
            "    dx, dy = x1 - x0, y1 - y0\n"
            "    for x, y in coordinates[2:]:\n"
            "        if dy * (x - x0) != dx * (y - y0):\n"
            "            return False\n"
            "    return True\n",
            lambda low: bool(
                re.search(
                    r"\bcheck[_ ]straight[_ ]line\b|"
                    r"\bcheck if it is a straight line\b|"
                    r"\bpoints (?:are |lie )?on a straight line\b",
                    low,
                )
            ),
            (
                (([[1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7]],), True),
                (([[1, 1], [2, 2], [3, 4], [4, 5], [5, 6], [7, 7]],), False),
            ),
        ),
        T(
            "n_repeated_element",
            "def n_repeated_element(nums):\n"
            '    """The unique element repeated N times in a 2N array (LeetCode 961)."""\n'
            "    seen = set()\n"
            "    for x in nums:\n"
            "        if x in seen:\n"
            "            return x\n"
            "        seen.add(x)\n"
            "    return nums[-1]\n",
            lambda low: bool(
                re.search(
                    r"\bn[_ ]repeated[_ ]element\b|"
                    r"\bn-repeated element\b|"
                    r"\brepeated n times in size 2n\b|"
                    r"\bn repeated element in size 2n\b",
                    low,
                )
            ),
            (
                (([1, 2, 3, 3],), 3),
                (([2, 1, 2, 5, 3, 2],), 2),
                (([5, 1, 5, 2, 5, 3, 5, 4],), 5),
            ),
        ),
    ]
