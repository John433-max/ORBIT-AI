"""ORBIT code_synth template pack (Cycle 244 split)."""
from __future__ import annotations
import re
from code_synth import Template, _TWO

def templates():
    return [

        Template(
            "min_path_sum",
            "def min_path_sum(grid):\n"
            '    """Minimum path sum from top-left to bottom-right (right/down)."""\n'
            "    grid = [list(row) for row in grid]\n"
            "    if not grid or not grid[0]:\n"
            "        return 0\n"
            "    m, n = len(grid), len(grid[0])\n"
            "    dp = [0] * n\n"
            "    acc = 0\n"
            "    for j in range(n):\n"
            "        acc += grid[0][j]\n"
            "        dp[j] = acc\n"
            "    for i in range(1, m):\n"
            "        dp[0] += grid[i][0]\n"
            "        for j in range(1, n):\n"
            "            dp[j] = grid[i][j] + min(dp[j], dp[j - 1])\n"
            "    return dp[-1]\n",
            lambda low: bool(
                re.search(
                    r"\bmin(?:imum)?[- ]?path[- ]?sum\b|"
                    r"\bminimum path sum\b|"
                    r"\bpath sum in a grid\b",
                    low,
                )
            ),
            (
                (([[1, 3, 1], [1, 5, 1], [4, 2, 1]],), 7),
                (([[1, 2, 3], [4, 5, 6]],), 12),
            ),
        ),
        Template(
            "unique_paths",
            "def unique_paths(m, n):\n"
            '    """Number of right/down paths on an m x n grid."""\n'
            "    m, n = int(m), int(n)\n"
            "    if m <= 0 or n <= 0:\n"
            "        return 0\n"
            "    row = [1] * n\n"
            "    for _ in range(1, m):\n"
            "        for j in range(1, n):\n"
            "            row[j] += row[j - 1]\n"
            "    return row[-1]\n",
            lambda low: bool(
                re.search(
                    r"\bunique[- ]?paths\b|"
                    r"\bpaths on an? (?:m x n |grid)\b|"
                    r"\bgrid paths\b",
                    low,
                )
                and "obstacle" not in low
                and not re.search(r"\bunique[- ]?paths\s*(ii|2)\b", low)
            ),
            (((3, 7), 28), ((3, 2), 3), ((1, 1), 1)),
        ),
        Template(
            "word_break",
            "def word_break(s, word_dict):\n"
            '    """True if s can be segmented into dictionary words."""\n'
            "    s = str(s)\n"
            "    words = set(word_dict)\n"
            "    n = len(s)\n"
            "    ok = [False] * (n + 1)\n"
            "    ok[0] = True\n"
            "    for i in range(1, n + 1):\n"
            "        for j in range(i):\n"
            "            if ok[j] and s[j:i] in words:\n"
            "                ok[i] = True\n"
            "                break\n"
            "    return ok[n]\n",
            lambda low: bool(
                re.search(
                    r"\bword[- ]?break\b|"
                    r"\bsegment(?:ed|s)? into dictionary\b|"
                    r"\bword dict(?:ionary)?\b",
                    low,
                )
                and not re.search(r"\b(ii|2|two|all|every|sentences?)\b", low)
            ),
            (
                (("leetcode", ["leet", "code"]), True),
                (("applepenapple", ["apple", "pen"]), True),
                (("catsandog", ["cats", "dog", "sand", "and", "cat"]), False),
            ),
        ),
        Template(
            "search_rotated",
            "def search_rotated(nums, target):\n"
            '    """Index of target in a rotated sorted array, or -1."""\n'
            "    nums = list(nums)\n"
            "    lo, hi = 0, len(nums) - 1\n"
            "    while lo <= hi:\n"
            "        mid = (lo + hi) // 2\n"
            "        if nums[mid] == target:\n"
            "            return mid\n"
            "        if nums[lo] <= nums[mid]:\n"
            "            if nums[lo] <= target < nums[mid]:\n"
            "                hi = mid - 1\n"
            "            else:\n"
            "                lo = mid + 1\n"
            "        else:\n"
            "            if nums[mid] < target <= nums[hi]:\n"
            "                lo = mid + 1\n"
            "            else:\n"
            "                hi = mid - 1\n"
            "    return -1\n",
            lambda low: bool(
                re.search(
                    r"\bsearch(?:es|ing)? (?:in )?(?:a )?rotated\b|"
                    r"\brotated sorted\b|"
                    r"\bsearch_rotated\b",
                    low,
                )
                and not re.search(r"\b(min(?:imum)?|smallest|find min)\b", low)
            ),
            (
                (([4, 5, 6, 7, 0, 1, 2], 0), 4),
                (([4, 5, 6, 7, 0, 1, 2], 3), -1),
                (([1], 0), -1),
            ),
        ),
        Template(
            "three_sum",
            "def three_sum(nums):\n"
            '    """Unique triplets that sum to zero, sorted."""\n'
            "    nums = sorted(int(x) for x in nums)\n"
            "    n = len(nums)\n"
            "    out = []\n"
            "    for i in range(n):\n"
            "        if i and nums[i] == nums[i - 1]:\n"
            "            continue\n"
            "        lo, hi = i + 1, n - 1\n"
            "        while lo < hi:\n"
            "            s = nums[i] + nums[lo] + nums[hi]\n"
            "            if s == 0:\n"
            "                out.append([nums[i], nums[lo], nums[hi]])\n"
            "                lo += 1\n"
            "                hi -= 1\n"
            "                while lo < hi and nums[lo] == nums[lo - 1]:\n"
            "                    lo += 1\n"
            "                while lo < hi and nums[hi] == nums[hi + 1]:\n"
            "                    hi -= 1\n"
            "            elif s < 0:\n"
            "                lo += 1\n"
            "            else:\n"
            "                hi -= 1\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bthree[- ]?sum\b|"
                    r"\b3[- ]?sum\b|"
                    r"\btriplets? that sum\b",
                    low,
                )
                and "closest" not in low
                and not re.search(r"\b(four|4)[- ]?sum\b", low)
            ),
            (
                (([-1, 0, 1, 2, -1, -4],), [[-1, -1, 2], [-1, 0, 1]]),
                (([0, 1, 1],), []),
                (([0, 0, 0],), [[0, 0, 0]]),
            ),
        ),
        Template(
            "edit_distance",
            "def edit_distance(a, b):\n"
            '    """Levenshtein distance between a and b."""\n'
            "    a, b = str(a), str(b)\n"
            "    m, n = len(a), len(b)\n"
            "    prev = list(range(n + 1))\n"
            "    for i, ca in enumerate(a, 1):\n"
            "        cur = [i] + [0] * n\n"
            "        for j, cb in enumerate(b, 1):\n"
            "            if ca == cb:\n"
            "                cur[j] = prev[j - 1]\n"
            "            else:\n"
            "                cur[j] = 1 + min(prev[j], cur[j - 1], prev[j - 1])\n"
            "        prev = cur\n"
            "    return prev[n]\n",
            lambda low: bool(
                re.search(
                    r"\bedit[- ]?distance\b|"
                    r"\blevenshtein\b|"
                    r"\bstring distance\b",
                    low,
                )
            ),
            ((("horse", "ros"), 3), (("intention", "execution"), 5), (("", "a"), 1)),
        ),
        Template(
            "course_schedule",
            "def course_schedule(num_courses, prerequisites):\n"
            '    """True if all courses can be finished given prereqs."""\n'
            "    n = int(num_courses)\n"
            "    graph = [[] for _ in range(n)]\n"
            "    indeg = [0] * n\n"
            "    for a, b in prerequisites:\n"
            "        graph[b].append(a)\n"
            "        indeg[a] += 1\n"
            "    q = [i for i in range(n) if indeg[i] == 0]\n"
            "    seen = 0\n"
            "    while q:\n"
            "        u = q.pop()\n"
            "        seen += 1\n"
            "        for v in graph[u]:\n"
            "            indeg[v] -= 1\n"
            "            if indeg[v] == 0:\n"
            "                q.append(v)\n"
            "    return seen == n\n",
            lambda low: bool(
                re.search(
                    r"\bcourse[- ]?schedule\b|"
                    r"\bcan finish (?:all )?courses\b|"
                    r"\bprerequisites?\b.{0,24}\bcourses?\b|"
                    r"\bcourses?\b.{0,24}\bprerequisites?\b",
                    low,
                )
                and not re.search(
                    r"\b(ii|2|order|ordering|topolog)\b",
                    low,
                )
            ),
            (
                ((2, [[1, 0]]), True),
                ((2, [[1, 0], [0, 1]]), False),
                ((1, []), True),
            ),
        ),
        Template(
            "combination_sum",
            "def combination_sum(candidates, target):\n"
            '    """Unique combinations that sum to target (reuse allowed)."""\n'
            "    cands = sorted({int(x) for x in candidates})\n"
            "    target = int(target)\n"
            "    out = []\n"
            "    path = []\n"
            "\n"
            "    def dfs(start, remain):\n"
            "        if remain == 0:\n"
            "            out.append(list(path))\n"
            "            return\n"
            "        for i in range(start, len(cands)):\n"
            "            v = cands[i]\n"
            "            if v > remain:\n"
            "                break\n"
            "            path.append(v)\n"
            "            dfs(i, remain - v)\n"
            "            path.pop()\n"
            "\n"
            "    dfs(0, target)\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bcombination[- ]?sum\b|"
                    r"\bcombinations? that sum\b|"
                    r"\bcoin combinations\b",
                    low,
                )
                and "ii" not in low
                and "2" not in low.split("sum")[-1]
                and "without reuse" not in low
                and "no reuse" not in low
                and "each number once" not in low
            ),
            (
                (([2, 3, 6, 7], 7), [[2, 2, 3], [7]]),
                (([2, 3, 5], 8), [[2, 2, 2, 2], [2, 3, 3], [3, 5]]),
                (([2], 1), []),
            ),
        ),
        Template(
            "group_anagrams",
            "def group_anagrams(strs):\n"
            '    """Group strings that are anagrams of each other."""\n'
            "    groups = {}\n"
            "    order = []\n"
            "    for s in strs:\n"
            "        key = ''.join(sorted(s))\n"
            "        if key not in groups:\n"
            "            groups[key] = []\n"
            "            order.append(key)\n"
            "        groups[key].append(s)\n"
            "    return [groups[k] for k in order]\n",
            lambda low: bool(
                re.search(
                    r"\bgroup[- ]?anagrams\b|"
                    r"\bgroup(?:s|ing)? (?:the )?anagrams\b|"
                    r"\banagram groups\b",
                    low,
                )
            ),
            (
                ((["eat", "tea", "tan", "ate", "nat", "bat"],), [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]),
                (([""],), [[""]]),
                ((["a"],), [["a"]]),
            ),
        ),
        Template(
            "merge_intervals",
            "def merge_intervals(intervals):\n"
            '    """Merge overlapping [start, end] intervals."""\n'
            "    items = sorted(([int(a), int(b)] for a, b in intervals), key=lambda x: x[0])\n"
            "    if not items:\n"
            "        return []\n"
            "    out = [items[0]]\n"
            "    for lo, hi in items[1:]:\n"
            "        if lo <= out[-1][1]:\n"
            "            if hi > out[-1][1]:\n"
            "                out[-1][1] = hi\n"
            "        else:\n"
            "            out.append([lo, hi])\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bmerge[- ]?intervals\b|"
                    r"\bmerge(?:s|ing)? overlapping\b|"
                    r"\boverlapping intervals\b",
                    low,
                )
            ),
            (
                (([[1, 3], [2, 6], [8, 10], [15, 18]],), [[1, 6], [8, 10], [15, 18]]),
                (([[1, 4], [4, 5]],), [[1, 5]]),
                (([],), []),
            ),
        ),
        Template(
            "is_subsequence",
            "def is_subsequence(s, t):\n"
            '    """True if s is a subsequence of t."""\n'
            "    i = 0\n"
            "    for ch in t:\n"
            "        if i < len(s) and ch == s[i]:\n"
            "            i += 1\n"
            "    return i == len(s)\n",
            lambda low: bool(
                re.search(
                    r"\bis[- ]?subsequence\b|"
                    r"\bsubsequence of\b|"
                    r"\bcheck(?:s|ing)? if .{0,24}subsequence\b",
                    low,
                )
            ),
            (
                (("abc", "ahbgdc"), True),
                (("axc", "ahbgdc"), False),
                (("", "ahbgdc"), True),
            ),
        ),
        Template(
            "happy_number",
            "def happy_number(n):\n"
            '    """True if n is a happy number (sum of squared digits reaches 1)."""\n'
            "    seen = set()\n"
            "    n = int(n)\n"
            "    while n != 1 and n not in seen:\n"
            "        seen.add(n)\n"
            "        n = sum(int(d) ** 2 for d in str(n))\n"
            "    return n == 1\n",
            lambda low: bool(re.search(r"\bhappy[- ]?number\b|\bis[- ]?happy\b", low)),
            (
                ((19,), True),
                ((2,), False),
                ((1,), True),
            ),
        ),
        Template(
            "add_binary",
            "def add_binary(a, b):\n"
            '    """Add two binary strings and return the binary sum."""\n'
            "    i, j, carry = len(a) - 1, len(b) - 1, 0\n"
            "    out = []\n"
            "    while i >= 0 or j >= 0 or carry:\n"
            "        if i >= 0:\n"
            "            carry += 1 if a[i] == '1' else 0\n"
            "            i -= 1\n"
            "        if j >= 0:\n"
            "            carry += 1 if b[j] == '1' else 0\n"
            "            j -= 1\n"
            "        out.append('1' if carry & 1 else '0')\n"
            "        carry >>= 1\n"
            "    return ''.join(reversed(out))\n",
            lambda low: bool(
                re.search(
                    r"\badd[- ]?binary\b|"
                    r"\badd(?:s|ing)? two binary\b|"
                    r"\bbinary strings?\b.{0,16}\badd\b|"
                    r"\badd\b.{0,24}\bbinary strings?\b",
                    low,
                )
            ),
            (
                (("11", "1"), "100"),
                (("1010", "1011"), "10101"),
                (("0", "0"), "0"),
            ),
        ),
        Template(
            "reverse_words",
            "def reverse_words(s):\n"
            '    """Reverse the order of words in a string."""\n'
            "    return ' '.join(reversed(s.split()))\n",
            lambda low: bool(
                re.search(
                    r"\breverse[- ]?words\b|"
                    r"\breverse(?:s|ing)? the (?:order of )?words\b|"
                    r"\bwords in (?:a |the )?string\b.{0,16}\breverse\b|"
                    r"\breverse\b.{0,24}\bwords in\b|"
                    r"\brevers(?:e|es|ing)\b.{0,32}\bwords\b",
                    low,
                )
                and "list" not in low
            ),
            (
                (("the sky is blue",), "blue is sky the"),
                (("  hello world  ",), "world hello"),
                (("a",), "a"),
            ),
        ),
        Template(
            "str_str",
            "def str_str(haystack, needle):\n"
            '    """Index of the first occurrence of needle in haystack, else -1."""\n'
            "    if needle == '':\n"
            "        return 0\n"
            "    n, m = len(haystack), len(needle)\n"
            "    for i in range(n - m + 1):\n"
            "        if haystack[i:i + m] == needle:\n"
            "            return i\n"
            "    return -1\n",
            lambda low: bool(
                re.search(
                    r"\bstr[-_ ]?str\b|"
                    r"\bindex of (?:the )?first occurrence\b|"
                    r"\bfind (?:the )?needle in (?:the )?haystack\b|"
                    r"\bfirst occurrence of .{0,24}in .{0,24}string\b",
                    low,
                )
            ),
            (
                (("sadbutsad", "sad"), 0),
                (("leetcode", "leeto"), -1),
                (("hello", "ll"), 2),
            ),
        ),
        Template(
            "generate_parentheses",
            "def generate_parentheses(n):\n"
            '    """All combinations of n pairs of well-formed parentheses."""\n'
            "    n = int(n)\n"
            "    out = []\n"
            "\n"
            "    def dfs(s, op, cl):\n"
            "        if len(s) == 2 * n:\n"
            "            out.append(s)\n"
            "            return\n"
            "        if op < n:\n"
            "            dfs(s + '(', op + 1, cl)\n"
            "        if cl < op:\n"
            "            dfs(s + ')', op, cl + 1)\n"
            "\n"
            "    dfs('', 0, 0)\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bgenerate[- ]?parentheses\b|"
                    r"\bgenerate(?:s|ing)? (?:all )?(?:valid )?parentheses\b|"
                    r"\bwell[- ]?formed parentheses\b",
                    low,
                )
            ),
            (
                ((1,), ["()"]),
                ((2,), ["(())", "()()"]),
                ((3,), ["((()))", "(()())", "(())()", "()(())", "()()()"]),
            ),
        ),
        Template(
            "ugly_number",
            "def ugly_number(n):\n"
            '    """Return the n-th ugly number (1 and products of 2, 3, 5)."""\n'
            "    n = int(n)\n"
            "    if n <= 0:\n"
            "        return 0\n"
            "    nums = [1]\n"
            "    i2 = i3 = i5 = 0\n"
            "    while len(nums) < n:\n"
            "        n2, n3, n5 = nums[i2] * 2, nums[i3] * 3, nums[i5] * 5\n"
            "        nxt = min(n2, n3, n5)\n"
            "        nums.append(nxt)\n"
            "        if nxt == n2:\n"
            "            i2 += 1\n"
            "        if nxt == n3:\n"
            "            i3 += 1\n"
            "        if nxt == n5:\n"
            "            i5 += 1\n"
            "    return nums[-1]\n",
            lambda low: bool(
                re.search(
                    r"\b(nth |n-th |n th )?ugly numbers?\b|"
                    r"\bugly_number\b",
                    low,
                )
            ),
            (((1,), 1), ((10,), 12), ((7,), 8)),
        ),
        Template(
            "has_cycle",
            "def has_cycle(next_index):\n"
            '    """True if next-index pointers form a cycle (-1 is None)."""\n'
            "    nxt = list(next_index)\n"
            "    slow = fast = 0\n"
            "    n = len(nxt)\n"
            "    if n == 0:\n"
            "        return False\n"
            "    while True:\n"
            "        if slow < 0 or slow >= n or nxt[slow] < 0:\n"
            "            return False\n"
            "        slow = nxt[slow]\n"
            "        for _ in range(2):\n"
            "            if fast < 0 or fast >= n or nxt[fast] < 0:\n"
            "                return False\n"
            "            fast = nxt[fast]\n"
            "        if slow == fast:\n"
            "            return True\n",
            lambda low: bool(
                re.search(
                    r"\b(detect|find|has|check(?:s|ing)?)\b.{0,32}\bcycle\b.{0,24}\b(linked list|list)\b|"
                    r"\blinked list\b.{0,24}\bcycle\b|"
                    r"\bhas[- ]?cycle\b|"
                    r"\bfloyd.?s cycle\b",
                    low,
                )
            ),
            (
                (([1, 2, 0],), True),
                (([1, 2, -1],), False),
                (([],), False),
            ),
        ),
        Template(
            "pascal_triangle",
            "def pascal_triangle(num_rows):\n"
            '    """Return the first num_rows of Pascal\'s triangle."""\n'
            "    n = int(num_rows)\n"
            "    if n <= 0:\n"
            "        return []\n"
            "    rows = [[1]]\n"
            "    for i in range(1, n):\n"
            "        prev = rows[-1]\n"
            "        row = [1]\n"
            "        for j in range(1, i):\n"
            "            row.append(prev[j - 1] + prev[j])\n"
            "        row.append(1)\n"
            "        rows.append(row)\n"
            "    return rows\n",
            lambda low: bool(
                re.search(
                    r"\bpascal(?:'s)? triangle\b|"
                    r"\bpascal_triangle\b",
                    low,
                )
                and " ii" not in low
                and "row index" not in low
                and "get row" not in low
                and "nth row" not in low
            ),
            (
                ((1,), [[1]]),
                ((5,), [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]),
            ),
        ),
        Template(
            "spiral_order",
            "def spiral_order(matrix):\n"
            '    """Return matrix values in clockwise spiral order."""\n'
            "    grid = [list(row) for row in matrix]\n"
            "    out = []\n"
            "    while grid and grid[0]:\n"
            "        out.extend(grid.pop(0))\n"
            "        if grid and grid[0]:\n"
            "            for row in grid:\n"
            "                out.append(row.pop())\n"
            "        if grid:\n"
            "            out.extend(reversed(grid.pop()))\n"
            "        if grid and grid[0]:\n"
            "            for row in reversed(grid):\n"
            "                out.append(row.pop(0))\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\bspiral[- ]?order\b|"
                    r"\bspiral (?:matrix|traversal)\b|"
                    r"\bmatrix in spiral\b",
                    low,
                )
            ),
            (
                (([[1, 2, 3], [4, 5, 6], [7, 8, 9]],), [1, 2, 3, 6, 9, 8, 7, 4, 5]),
                (([[1, 2], [3, 4]],), [1, 2, 4, 3]),
            ),
        ),
        Template(
            "set_zeroes",
            "def set_zeroes(matrix):\n"
            '    """Zero out rows and columns that contain a 0; return the matrix."""\n'
            "    grid = [list(row) for row in matrix]\n"
            "    if not grid:\n"
            "        return grid\n"
            "    m, n = len(grid), len(grid[0])\n"
            "    rows = set()\n"
            "    cols = set()\n"
            "    for i in range(m):\n"
            "        for j in range(n):\n"
            "            if grid[i][j] == 0:\n"
            "                rows.add(i)\n"
            "                cols.add(j)\n"
            "    for i in range(m):\n"
            "        for j in range(n):\n"
            "            if i in rows or j in cols:\n"
            "                grid[i][j] = 0\n"
            "    return grid\n",
            lambda low: bool(
                re.search(
                    r"\bsets?[- ]?zeroe?s\b|"
                    r"\bsets? .{0,24}zeroe?s\b|"
                    r"\bzero(?:es|s)? out .{0,24}(row|column|matrix)\b|"
                    r"\bmatrix .{0,16}sets? zero",
                    low,
                )
            ),
            (
                (([[1, 1, 1], [1, 0, 1], [1, 1, 1]],), [[1, 0, 1], [0, 0, 0], [1, 0, 1]]),
                (([[0, 1], [1, 1]],), [[0, 0], [0, 1]]),
            ),
        ),
        Template(
            "longest_palindrome",
            "def longest_palindrome(s):\n"
            '    """Length of the longest palindrome that can be built from s."""\n'
            "    counts = {}\n"
            "    for ch in str(s):\n"
            "        counts[ch] = counts.get(ch, 0) + 1\n"
            "    length = 0\n"
            "    odd = False\n"
            "    for c in counts.values():\n"
            "        length += c - (c % 2)\n"
            "        if c % 2:\n"
            "            odd = True\n"
            "    return length + (1 if odd else 0)\n",
            lambda low: bool(
                re.search(
                    r"\blongest palindrome\b|"
                    r"\bpalindrome that can be built\b",
                    low,
                )
                and "substring" not in low
            ),
            (
                (("abccccdd",), 7),
                (("a",), 1),
                (("bb",), 2),
            ),
        ),
        Template(
            "decode_ways",
            "def decode_ways(s):\n"
            '    """Number of ways to decode a digit string (A=1 … Z=26)."""\n'
            "    s = str(s)\n"
            "    n = len(s)\n"
            "    if n == 0 or s[0] == '0':\n"
            "        return 0\n"
            "    prev2, prev1 = 1, 1\n"
            "    for i in range(1, n):\n"
            "        cur = 0\n"
            "        if s[i] != '0':\n"
            "            cur += prev1\n"
            "        two = int(s[i - 1 : i + 1])\n"
            "        if 10 <= two <= 26:\n"
            "            cur += prev2\n"
            "        prev2, prev1 = prev1, cur\n"
            "    return prev1\n",
            lambda low: bool(
                re.search(
                    r"\bdecode ways\b|"
                    r"\bways to decode\b|"
                    r"\bdecode(?:s|d|ing)?\b.{0,24}\b(digit|numeric|encoded)\s*string\b|"
                    r"\bdecode_ways\b",
                    low,
                )
            ),
            (
                (("12",), 2),
                (("226",), 3),
                (("06",), 0),
            ),
        ),
        Template(
            "trap_rain_water",
            "def trap_rain_water(height):\n"
            '    """Units of rain water trapped between bars."""\n'
            "    h = list(height)\n"
            "    n = len(h)\n"
            "    if n < 3:\n"
            "        return 0\n"
            "    left = [0] * n\n"
            "    right = [0] * n\n"
            "    left[0] = h[0]\n"
            "    for i in range(1, n):\n"
            "        left[i] = left[i - 1] if left[i - 1] > h[i] else h[i]\n"
            "    right[-1] = h[-1]\n"
            "    for i in range(n - 2, -1, -1):\n"
            "        right[i] = right[i + 1] if right[i + 1] > h[i] else h[i]\n"
            "    water = 0\n"
            "    for i in range(n):\n"
            "        bound = left[i] if left[i] < right[i] else right[i]\n"
            "        water += bound - h[i]\n"
            "    return water\n",
            lambda low: bool(
                re.search(
                    r"\btrap(?:s|ping)?\b.{0,24}\b(rain|water)\b|"
                    r"\brain water\b|"
                    r"\btrapping rain\b|"
                    r"\btrap_rain",
                    low,
                )
            ),
            (
                (([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1],), 6),
                (([4, 2, 0, 3, 2, 5],), 9),
                (([1, 1],), 0),
            ),
        ),
        Template(
            "next_permutation",
            "def next_permutation(nums):\n"
            '    """Rearrange nums into the next lexicographic permutation (in place)."""\n'
            "    a = list(nums)\n"
            "    n = len(a)\n"
            "    i = n - 2\n"
            "    while i >= 0 and a[i] >= a[i + 1]:\n"
            "        i -= 1\n"
            "    if i >= 0:\n"
            "        j = n - 1\n"
            "        while a[j] <= a[i]:\n"
            "            j -= 1\n"
            "        a[i], a[j] = a[j], a[i]\n"
            "    lo, hi = i + 1, n - 1\n"
            "    while lo < hi:\n"
            "        a[lo], a[hi] = a[hi], a[lo]\n"
            "        lo += 1\n"
            "        hi -= 1\n"
            "    return a\n",
            lambda low: bool(
                re.search(
                    r"\bnext permutation\b|"
                    r"\bnext lexicograph\b|"
                    r"\bnext_permutation\b",
                    low,
                )
            ),
            (
                (([1, 2, 3],), [1, 3, 2]),
                (([3, 2, 1],), [1, 2, 3]),
                (([1, 1, 5],), [1, 5, 1]),
            ),
        ),
        Template(
            "longest_consecutive",
            "def longest_consecutive(nums):\n"
            '    """Length of the longest consecutive-elements sequence."""\n'
            "    s = set(nums)\n"
            "    best = 0\n"
            "    for x in s:\n"
            "        if x - 1 in s:\n"
            "            continue\n"
            "        y = x\n"
            "        while y in s:\n"
            "            y += 1\n"
            "        length = y - x\n"
            "        if length > best:\n"
            "            best = length\n"
            "    return best\n",
            lambda low: bool(
                re.search(
                    r"\blongest consecutive\b|"
                    r"\bconsecutive (elements? )?sequence\b|"
                    r"\blongest_consecutive\b",
                    low,
                )
            )
            and "identical" not in low
            and "characters" not in low
            and "max power" not in low
            and "max_power" not in low,
            (
                (([100, 4, 200, 1, 3, 2],), 4),
                (([0, 3, 7, 2, 5, 8, 4, 6, 0, 1],), 9),
                (([],), 0),
            ),
        ),
        Template(
            "rotate_image",
            "def rotate_image(matrix):\n"
            '    """Rotate an n×n matrix 90 degrees clockwise; return the matrix."""\n'
            "    m = [list(row) for row in matrix]\n"
            "    n = len(m)\n"
            "    for i in range(n):\n"
            "        for j in range(i + 1, n):\n"
            "            m[i][j], m[j][i] = m[j][i], m[i][j]\n"
            "    for i in range(n):\n"
            "        m[i].reverse()\n"
            "    return m\n",
            lambda low: bool(
                re.search(
                    r"\brotate(?:s|d|ing)?\b.{0,24}\b(image|matrix|grid)\b|"
                    r"\b(image|matrix|grid)\b.{0,20}\brotate|"
                    r"\brotate_image\b|"
                    r"\b90 degrees clockwise\b",
                    low,
                )
                and "list" not in low
                and "array" not in low
            ),
            (
                (([[1, 2, 3], [4, 5, 6], [7, 8, 9]],), [[7, 4, 1], [8, 5, 2], [9, 6, 3]]),
                (([[1, 2], [3, 4]],), [[3, 1], [4, 2]]),
            ),
        ),
        Template(
            "min_window",
            "def min_window(s, t):\n"
            '    """Smallest substring of s that covers every character in t."""\n'
            "    if not t:\n"
            "        return ''\n"
            "    need = {}\n"
            "    for ch in t:\n"
            "        need[ch] = need.get(ch, 0) + 1\n"
            "    missing = len(t)\n"
            "    have = {}\n"
            "    best = ''\n"
            "    best_len = None\n"
            "    left = 0\n"
            "    for right, ch in enumerate(s):\n"
            "        have[ch] = have.get(ch, 0) + 1\n"
            "        if ch in need and have[ch] <= need[ch]:\n"
            "            missing -= 1\n"
            "        while missing == 0 and left <= right:\n"
            "            cur_len = right - left + 1\n"
            "            if best_len is None or cur_len < best_len:\n"
            "                best_len = cur_len\n"
            "                best = s[left : right + 1]\n"
            "            drop = s[left]\n"
            "            have[drop] = have.get(drop, 0) - 1\n"
            "            if drop in need and have[drop] < need[drop]:\n"
            "                missing += 1\n"
            "            left += 1\n"
            "    return best\n",
            lambda low: bool(
                re.search(
                    r"\bminimum window substring\b|"
                    r"\bmin(?:imum)? window\b|"
                    r"\bsmallest substring\b.{0,32}\bcover|"
                    r"\bmin_window\b",
                    low,
                )
            ),
            (
                (("ADOBECODEBANC", "ABC"), "BANC"),
                (("a", "a"), "a"),
                (("a", "aa"), ""),
            ),
        ),
        Template(
            "jump_game_ii",
            "def jump_game_ii(nums):\n"
            '    """Minimum jumps to reach the last index (LeetCode 45)."""\n'
            "    nums = list(nums)\n"
            "    n = len(nums)\n"
            "    if n <= 1:\n"
            "        return 0\n"
            "    jumps = 0\n"
            "    end = 0\n"
            "    farthest = 0\n"
            "    for i in range(n - 1):\n"
            "        farthest = max(farthest, i + int(nums[i]))\n"
            "        if i == end:\n"
            "            jumps += 1\n"
            "            end = farthest\n"
            "            if end >= n - 1:\n"
            "                break\n"
            "    return jumps\n",
            lambda low: bool(
                re.search(
                    r"\bjump game\s*(ii|2)\b|"
                    r"\bmin(?:imum)? jumps\b|"
                    r"\bjump_game_ii\b",
                    low,
                )
            ),
            ((([2, 3, 1, 1, 4],), 2), (([2, 3, 0, 1, 4],), 2), (([1],), 0)),
        ),
        Template(
            "unique_paths_ii",
            "def unique_paths_ii(grid):\n"
            '    """Right/down paths on a grid with 1-obstacles (LeetCode 63)."""\n'
            "    grid = [list(row) for row in grid]\n"
            "    if not grid or not grid[0]:\n"
            "        return 0\n"
            "    m, n = len(grid), len(grid[0])\n"
            "    dp = [0] * n\n"
            "    dp[0] = 0 if grid[0][0] else 1\n"
            "    for i in range(m):\n"
            "        for j in range(n):\n"
            "            if grid[i][j]:\n"
            "                dp[j] = 0\n"
            "            elif j == 0:\n"
            "                if i:\n"
            "                    dp[j] = dp[j]  # inherit from above (same cell)\n"
            "            else:\n"
            "                dp[j] += dp[j - 1]\n"
            "    return dp[-1]\n",
            lambda low: bool(
                re.search(
                    r"\bunique[- ]?paths\s*(ii|2)\b|"
                    r"\bunique[- ]?paths\b.{0,24}\bobstacle|"
                    r"\bpaths.{0,24}\bobstacle",
                    low,
                )
            ),
            (
                (([[0, 0, 0], [0, 1, 0], [0, 0, 0]],), 2),
                (([[0, 1], [0, 0]],), 1),
                (([[1]],), 0),
            ),
        ),
        Template(
            "word_search",
            "def word_search(board, word):\n"
            '    """True if word exists on the board via adjacent cells (LeetCode 79)."""\n'
            "    board = [list(row) for row in board]\n"
            "    word = str(word)\n"
            "    if not board or not board[0] or not word:\n"
            "        return False\n"
            "    m, n = len(board), len(board[0])\n"
            "\n"
            "    def dfs(i, j, k):\n"
            "        if k == len(word):\n"
            "            return True\n"
            "        if i < 0 or i >= m or j < 0 or j >= n or board[i][j] != word[k]:\n"
            "            return False\n"
            "        ch = board[i][j]\n"
            "        board[i][j] = '#'\n"
            "        found = (\n"
            "            dfs(i + 1, j, k + 1)\n"
            "            or dfs(i - 1, j, k + 1)\n"
            "            or dfs(i, j + 1, k + 1)\n"
            "            or dfs(i, j - 1, k + 1)\n"
            "        )\n"
            "        board[i][j] = ch\n"
            "        return found\n"
            "\n"
            "    for r in range(m):\n"
            "        for c in range(n):\n"
            "            if dfs(r, c, 0):\n"
            "                return True\n"
            "    return False\n",
            lambda low: bool(
                re.search(
                    r"\bword search\b|"
                    r"\bword_search\b|"
                    r"\bexist(?:s)? on the board\b|"
                    r"\bword.{0,16}\badjacent cells\b",
                    low,
                )
            )
            and not re.search(r"\bword[- ]?search[- _]*(ii|2)\b|\bwords? from a board\b", low),
            (
                (([["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]], "ABCCED"), True),
                (([["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]], "SEE"), True),
                (([["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]], "ABCB"), False),
            ),
        ),
        Template(
            "num_islands",
            "def num_islands(grid):\n"
            '    """Count 4-connected islands of \'1\' cells (LeetCode 200)."""\n'
            "    grid = [list(row) for row in grid]\n"
            "    if not grid or not grid[0]:\n"
            "        return 0\n"
            "    m, n = len(grid), len(grid[0])\n"
            "    count = 0\n"
            "\n"
            "    def sink(i, j):\n"
            "        if i < 0 or i >= m or j < 0 or j >= n or grid[i][j] != '1':\n"
            "            return\n"
            "        grid[i][j] = '0'\n"
            "        sink(i + 1, j)\n"
            "        sink(i - 1, j)\n"
            "        sink(i, j + 1)\n"
            "        sink(i, j - 1)\n"
            "\n"
            "    for i in range(m):\n"
            "        for j in range(n):\n"
            "            if grid[i][j] == '1':\n"
            "                count += 1\n"
            "                sink(i, j)\n"
            "    return count\n",
            lambda low: bool(
                re.search(
                    r"\bnum(?:ber)? of islands\b|"
                    r"\bcount(?:s|ing)? islands\b|"
                    r"\bnum_islands\b",
                    low,
                )
            ),
            (
                (([["1", "1", "1", "1", "0"], ["1", "1", "0", "1", "0"], ["1", "1", "0", "0", "0"], ["0", "0", "0", "0", "0"]],), 1),
                (([["1", "1", "0", "0", "0"], ["1", "1", "0", "0", "0"], ["0", "0", "1", "0", "0"], ["0", "0", "0", "1", "1"]],), 3),
                (([["0"]],), 0),
            ),
        ),
        Template(
            "can_partition",
            "def can_partition(nums):\n"
            '    """True if nums splits into two subsets with equal sum (LeetCode 416)."""\n'
            "    nums = [int(x) for x in nums]\n"
            "    total = sum(nums)\n"
            "    if total % 2:\n"
            "        return False\n"
            "    target = total // 2\n"
            "    reachable = 1\n"
            "    for n in nums:\n"
            "        reachable |= reachable << n\n"
            "    return bool((reachable >> target) & 1)\n",
            lambda low: bool(
                re.search(
                    r"\bcan[- ]?partition\b|"
                    r"\bpartition equal subset\b|"
                    r"\bequal subset sum\b|"
                    r"\bsplit.{0,24}\bequal sum\b",
                    low,
                )
                and "linked" not in low
            ),
            ((([1, 5, 11, 5],), True), (([1, 2, 3, 5],), False), (([1, 1],), True)),
        ),
        Template(
            "maximal_square",
            "def maximal_square(matrix):\n"
            '    """Largest square of 1s; return its area (LeetCode 221)."""\n'
            "    matrix = [list(row) for row in matrix]\n"
            "    if not matrix or not matrix[0]:\n"
            "        return 0\n"
            "    m, n = len(matrix), len(matrix[0])\n"
            "    prev = [0] * (n + 1)\n"
            "    best = 0\n"
            "    for i in range(1, m + 1):\n"
            "        cur = [0] * (n + 1)\n"
            "        for j in range(1, n + 1):\n"
            "            cell = matrix[i - 1][j - 1]\n"
            "            if str(cell) in ('1', 'True') or cell == 1:\n"
            "                cur[j] = min(prev[j], cur[j - 1], prev[j - 1]) + 1\n"
            "                if cur[j] > best:\n"
            "                    best = cur[j]\n"
            "        prev = cur\n"
            "    return best * best\n",
            lambda low: bool(
                re.search(
                    r"\bmaximal square\b|"
                    r"\blargest square\b.{0,24}\b(1|ones)\b|"
                    r"\bmaximal_square\b",
                    low,
                )
            ),
            (
                (([["1", "0", "1", "0", "0"], ["1", "0", "1", "1", "1"], ["1", "1", "1", "1", "1"], ["1", "0", "0", "1", "0"]],), 4),
                (([["0", "1"], ["1", "0"]],), 1),
                (([["0"]],), 0),
            ),
        ),
        Template(
            "house_robber_ii",
            "def house_robber_ii(nums):\n"
            '    """Max non-adjacent sum on a circular street of houses."""\n'
            "    nums = list(nums)\n"
            "    n = len(nums)\n"
            "    if n == 0:\n"
            "        return 0\n"
            "    if n == 1:\n"
            "        return int(nums[0])\n"
            "\n"
            "    def _line(arr):\n"
            "        prev = cur = 0\n"
            "        for v in arr:\n"
            "            prev, cur = cur, max(cur, prev + int(v))\n"
            "        return cur\n"
            "\n"
            "    return max(_line(nums[:-1]), _line(nums[1:]))\n",
            lambda low: bool(
                re.search(
                    r"\bhouse[- ]?robber\s*(ii|2)\b|"
                    r"\brob houses\b.{0,24}\b(circular|circle)\b|"
                    r"\bcircular\b.{0,24}\bhouse[- ]?robber\b|"
                    r"\bhouse_robber_ii\b",
                    low,
                )
            ),
            ((([2, 3, 2],), 3), (([1, 2, 3, 1],), 4), (([1, 2, 3],), 3)),
        ),
        Template(
            "coin_change_ii",
            "def coin_change_ii(amount, coins):\n"
            '    """Number of combinations that sum to amount."""\n'
            "    amount = int(amount)\n"
            "    dp = [1] + [0] * amount\n"
            "    for coin in coins:\n"
            "        c = int(coin)\n"
            "        if c <= 0:\n"
            "            continue\n"
            "        for x in range(c, amount + 1):\n"
            "            dp[x] += dp[x - c]\n"
            "    return dp[amount]\n",
            lambda low: bool(
                re.search(
                    r"\bcoin[- ]?change\s*(ii|2)\b|"
                    r"\bcoin[- ]?change\b.{0,32}\b(combination|combinations|number of ways)\b|"
                    r"\bnumber of (coin )?combinations\b|"
                    r"\bcoin_change_ii\b",
                    low,
                )
            ),
            (((5, [1, 2, 5]), 4), ((3, [2]), 0), ((10, [10]), 1)),
        ),
        Template(
            "invert_binary_tree",
            "def invert_binary_tree(root):\n"
            '    """Invert a binary tree encoded as [val, left, right] or None."""\n'
            "    if root is None:\n"
            "        return None\n"
            "    val = root[0]\n"
            "    left = root[1] if len(root) > 1 else None\n"
            "    right = root[2] if len(root) > 2 else None\n"
            "    return [val, invert_binary_tree(right), invert_binary_tree(left)]\n",
            lambda low: bool(
                re.search(
                    r"\binvert(?:s|ing)?\b.{0,24}\bbinary tree\b|"
                    r"\bflip(?:s|ping)?\b.{0,16}\bbinary tree\b|"
                    r"\binvert_binary_tree\b",
                    low,
                )
            ),
            (
                (([4, [2, [1, None, None], [3, None, None]], [7, [6, None, None], [9, None, None]]],),
                 [4, [7, [9, None, None], [6, None, None]], [2, [3, None, None], [1, None, None]]]),
                (([2, [1, None, None], [3, None, None]],), [2, [3, None, None], [1, None, None]]),
                ((None,), None),
            ),
        ),
        Template(
            "level_order",
            "def level_order(root):\n"
            '    """Level-order values of a [val, left, right] binary tree."""\n'
            "    if root is None:\n"
            "        return []\n"
            "    out = []\n"
            "    q = [root]\n"
            "    while q:\n"
            "        node = q.pop(0)\n"
            "        if node is None:\n"
            "            continue\n"
            "        out.append(node[0])\n"
            "        if len(node) > 1 and node[1] is not None:\n"
            "            q.append(node[1])\n"
            "        if len(node) > 2 and node[2] is not None:\n"
            "            q.append(node[2])\n"
            "    return out\n",
            lambda low: bool(
                re.search(
                    r"\blevel[- ]?order\b|"
                    r"\bbreadth[- ]?first\b.{0,16}\b(tree|traversal)\b|"
                    r"\bbfs traversal\b.{0,16}\btree\b|"
                    r"\blevel_order\b",
                    low,
                )
                and "zigzag" not in low
            ),
            (
                (([3, [9, None, None], [20, [15, None, None], [7, None, None]]],), [3, 9, 20, 15, 7]),
                (([1, None, None],), [1]),
                ((None,), []),
            ),
        ),
        Template(
            "max_depth",
            "def max_depth(root):\n"
            '    """Maximum depth of a [val, left, right] binary tree."""\n'
            "    if root is None:\n"
            "        return 0\n"
            "    left = root[1] if len(root) > 1 else None\n"
            "    right = root[2] if len(root) > 2 else None\n"
            "    return 1 + max(max_depth(left), max_depth(right))\n",
            lambda low: bool(
                re.search(
                    r"\bmax(?:imum)? depth\b.{0,24}\b(binary )?tree\b|"
                    r"\bheight of\b.{0,16}\bbinary tree\b|"
                    r"\bmax_depth\b",
                    low,
                )
                and "min" not in low
            ),
            (
                (([3, [9, None, None], [20, [15, None, None], [7, None, None]]],), 3),
                (([1, None, [2, None, None]],), 2),
                ((None,), 0),
            ),
        ),
        Template(
            "diameter_of_binary_tree",
            "def diameter_of_binary_tree(root):\n"
            '    """Longest node-to-node path length in a [val, left, right] tree."""\n'
            "    best = [0]\n"
            "\n"
            "    def _depth(node):\n"
            "        if node is None:\n"
            "            return 0\n"
            "        left = node[1] if len(node) > 1 else None\n"
            "        right = node[2] if len(node) > 2 else None\n"
            "        lh = _depth(left)\n"
            "        rh = _depth(right)\n"
            "        if lh + rh > best[0]:\n"
            "            best[0] = lh + rh\n"
            "        return 1 + max(lh, rh)\n"
            "\n"
            "    _depth(root)\n"
            "    return best[0]\n",
            lambda low: bool(
                re.search(
                    r"\bdiameter\b.{0,24}\b(binary )?tree\b|"
                    r"\blongest path\b.{0,24}\bbinary tree\b|"
                    r"\bdiameter_of_binary_tree\b",
                    low,
                )
            ),
            (
                (([1, [2, [4, None, None], [5, None, None]], [3, None, None]],), 3),
                (([1, [2, None, None], None],), 1),
                ((None,), 0),
            ),
        ),
        Template(
            "course_schedule_ii",
            "def course_schedule_ii(num_courses, prerequisites):\n"
            '    """One valid course order, or [] if a cycle exists."""\n'
            "    n = int(num_courses)\n"
            "    graph = [[] for _ in range(n)]\n"
            "    indeg = [0] * n\n"
            "    for a, b in prerequisites:\n"
            "        graph[b].append(a)\n"
            "        indeg[a] += 1\n"
            "    q = [i for i in range(n) if indeg[i] == 0]\n"
            "    order = []\n"
            "    while q:\n"
            "        u = q.pop()\n"
            "        order.append(u)\n"
            "        for v in graph[u]:\n"
            "            indeg[v] -= 1\n"
            "            if indeg[v] == 0:\n"
            "                q.append(v)\n"
            "    return order if len(order) == n else []\n",
            lambda low: bool(
                re.search(
                    r"\bcourse[- ]?schedule\s*(ii|2)\b|"
                    r"\bcourse[- ]?order\b|"
                    r"\btopolog(?:ical|y)\b.{0,24}\bcourses?\b|"
                    r"\border(?:ing)?\b.{0,24}\bcourses?\b|"
                    r"\bcourse_schedule_ii\b",
                    low,
                )
            ),
            (
                ((2, [[1, 0]]), [0, 1]),
                ((4, [[1, 0], [2, 0], [3, 1], [3, 2]]), [0, 2, 1, 3]),
                ((2, [[1, 0], [0, 1]]), []),
            ),
        ),
        Template(
            "is_same_tree",
            "def is_same_tree(p, q):\n"
            '    """True if two [val, left, right] trees are identical."""\n'
            "    if p is None or q is None:\n"
            "        return p is None and q is None\n"
            "    if p[0] != q[0]:\n"
            "        return False\n"
            "    pl = p[1] if len(p) > 1 else None\n"
            "    pr = p[2] if len(p) > 2 else None\n"
            "    ql = q[1] if len(q) > 1 else None\n"
            "    qr = q[2] if len(q) > 2 else None\n"
            "    return is_same_tree(pl, ql) and is_same_tree(pr, qr)\n",
            lambda low: bool(
                re.search(
                    r"\bsame tree\b|"
                    r"\bidentical (binary )?trees?\b|"
                    r"\bis_same_tree\b",
                    low,
                )
            ),
            (
                (([1, [2, None, None], [3, None, None]], [1, [2, None, None], [3, None, None]]), True),
                (([1, [2, None, None], None], [1, None, [2, None, None]]), False),
                ((None, None), True),
            ),
        ),
        Template(
            "is_symmetric",
            "def is_symmetric(root):\n"
            '    """True if a [val, left, right] tree is a mirror of itself."""\n'
            "    def _mir(a, b):\n"
            "        if a is None or b is None:\n"
            "            return a is None and b is None\n"
            "        if a[0] != b[0]:\n"
            "            return False\n"
            "        al = a[1] if len(a) > 1 else None\n"
            "        ar = a[2] if len(a) > 2 else None\n"
            "        bl = b[1] if len(b) > 1 else None\n"
            "        br = b[2] if len(b) > 2 else None\n"
            "        return _mir(al, br) and _mir(ar, bl)\n"
            "    if root is None:\n"
            "        return True\n"
            "    left = root[1] if len(root) > 1 else None\n"
            "    right = root[2] if len(root) > 2 else None\n"
            "    return _mir(left, right)\n",
            lambda low: bool(
                re.search(
                    r"\bsymmetric (binary )?tree\b|"
                    r"\bmirror (binary )?tree\b|"
                    r"\bis_symmetric\b",
                    low,
                )
            ),
            (
                (([1, [2, [3, None, None], [4, None, None]], [2, [4, None, None], [3, None, None]]],), True),
                (([1, [2, None, [3, None, None]], [2, None, [3, None, None]]],), False),
                ((None,), True),
            ),
        ),
        Template(
            "path_sum",
            "def path_sum(root, target):\n"
            '    """True if a root-to-leaf path sums to target."""\n'
            "    if root is None:\n"
            "        return False\n"
            "    val = root[0]\n"
            "    left = root[1] if len(root) > 1 else None\n"
            "    right = root[2] if len(root) > 2 else None\n"
            "    if left is None and right is None:\n"
            "        return val == target\n"
            "    return path_sum(left, target - val) or path_sum(right, target - val)\n",
            lambda low: bool(
                re.search(
                    r"\bpath[- ]?sum\b|"
                    r"\bhas path\b.{0,24}\bsum\b|"
                    r"\broot[- ]to[- ]leaf\b.{0,24}\bsum\b|"
                    r"\bpath_sum\b",
                    low,
                )
                and "ii" not in low
                and "all path" not in low
                and "paths that sum" not in low
                and "list of paths" not in low
                and "max path" not in low
                and "maximum path" not in low
                and "max_path" not in low
            ),
            (
                (([5, [4, [11, [7, None, None], [2, None, None]], None], [8, [13, None, None], [4, None, [1, None, None]]]], 22), True),
                (([1, [2, None, None], [3, None, None]], 5), False),
                ((None, 0), False),
            ),
        ),
        Template(
            "is_valid_bst",
            "def is_valid_bst(root):\n"
            '    """True if a [val, left, right] tree is a BST."""\n'
            "    def _ok(node, lo, hi):\n"
            "        if node is None:\n"
            "            return True\n"
            "        v = node[0]\n"
            "        if (lo is not None and v <= lo) or (hi is not None and v >= hi):\n"
            "            return False\n"
            "        left = node[1] if len(node) > 1 else None\n"
            "        right = node[2] if len(node) > 2 else None\n"
            "        return _ok(left, lo, v) and _ok(right, v, hi)\n"
            "    return _ok(root, None, None)\n",
            lambda low: bool(
                re.search(
                    r"\bvalidat(?:e|es|ed|ing)?\b.{0,24}\b(binary search tree|bst)\b|"
                    r"\bvalid (binary search tree|bst)\b|"
                    r"\bis_valid_bst\b|"
                    r"\bis a bst\b",
                    low,
                )
            ),
            (
                (([2, [1, None, None], [3, None, None]],), True),
                (([5, [1, None, None], [4, [3, None, None], [6, None, None]]],), False),
                ((None,), True),
            ),
        ),
        Template(
            "lowest_common_ancestor",
            "def lowest_common_ancestor(root, p, q):\n"
            '    """LCA value of p and q in a [val, left, right] tree."""\n'
            "    if root is None:\n"
            "        return None\n"
            "    if root[0] in (p, q):\n"
            "        return root[0]\n"
            "    left = root[1] if len(root) > 1 else None\n"
            "    right = root[2] if len(root) > 2 else None\n"
            "    L = lowest_common_ancestor(left, p, q)\n"
            "    R = lowest_common_ancestor(right, p, q)\n"
            "    if L is not None and R is not None:\n"
            "        return root[0]\n"
            "    return L if L is not None else R\n",
            lambda low: bool(
                re.search(
                    r"\blowest common ancestor\b|"
                    r"\blca\b|"
                    r"\blowest_common_ancestor\b",
                    low,
                )
            )
            and not re.search(r"\bbst\b|\bbinary search tree\b", low),
            (
                (([3, [5, [6, None, None], [2, [7, None, None], [4, None, None]]], [1, [0, None, None], [8, None, None]]], 5, 1), 3),
                (([3, [5, [6, None, None], [2, [7, None, None], [4, None, None]]], [1, [0, None, None], [8, None, None]]], 5, 4), 5),
                (([1, [2, None, None], None], 1, 2), 1),
            ),
        ),
        Template(
            "reverse_linked_list",
            "def reverse_linked_list(head):\n"
            '    """Reverse a [val, next] linked list."""\n'
            "    prev = None\n"
            "    cur = head\n"
            "    while cur is not None:\n"
            "        nxt = cur[1] if len(cur) > 1 else None\n"
            "        node = [cur[0], prev]\n"
            "        prev = node\n"
            "        cur = nxt\n"
            "    return prev\n",
            lambda low: bool(
                re.search(
                    r"\brevers(?:e|es|ed|ing)\b.{0,24}\b(singly )?linked list\b|"
                    r"\breverse_linked_list\b|"
                    r"\blinked list\b.{0,16}\brevers",
                    low,
                )
                and "words" not in low
                and "between" not in low
                and "position" not in low
                and "reverse linked list ii" not in low
            ),
            (
                (([1, [2, [3, None]]],), [3, [2, [1, None]]]),
                (([1, None],), [1, None]),
                ((None,), None),
            ),
        ),
        Template(
            "merge_two_lists",
            "def merge_two_lists(a, b):\n"
            '    """Merge two sorted [val, next] lists."""\n'
            "    dummy = [0, None]\n"
            "    tail = dummy\n"
            "    while a is not None and b is not None:\n"
            "        if a[0] <= b[0]:\n"
            "            tail[1] = [a[0], None]\n"
            "            tail = tail[1]\n"
            "            a = a[1] if len(a) > 1 else None\n"
            "        else:\n"
            "            tail[1] = [b[0], None]\n"
            "            tail = tail[1]\n"
            "            b = b[1] if len(b) > 1 else None\n"
            "    rest = a if a is not None else b\n"
            "    while rest is not None:\n"
            "        tail[1] = [rest[0], None]\n"
            "        tail = tail[1]\n"
            "        rest = rest[1] if len(rest) > 1 else None\n"
            "    return dummy[1]\n",
            lambda low: bool(
                re.search(
                    r"\bmerg(?:e|es|ed|ing)\b.{0,28}\btwo (sorted )?linked lists\b|"
                    r"\bmerge_two_lists\b|"
                    r"\bmerg(?:e|es|ed|ing)\b.{0,24}\bsorted linked lists\b",
                    low,
                )
                and not re.search(r"\bk\b|\bmerge_k\b|\bmultiple\b", low)
            ),
            (
                (([1, [3, None]], [2, [4, None]]), [1, [2, [3, [4, None]]]]),
                ((None, [0, None]), [0, None]),
                ((None, None), None),
            ),
        ),
        Template(
            "middle_node",
            "def middle_node(head):\n"
            '    """Return the middle [val, next] node (second middle if even)."""\n'
            "    slow = head\n"
            "    fast = head\n"
            "    while fast is not None and (fast[1] if len(fast) > 1 else None) is not None:\n"
            "        slow = slow[1] if len(slow) > 1 else None\n"
            "        nxt = fast[1] if len(fast) > 1 else None\n"
            "        fast = nxt[1] if nxt is not None and len(nxt) > 1 else None\n"
            "    return slow\n",
            lambda low: bool(
                re.search(
                    r"\bmiddle (of )?(the |a )?(linked )?list\b|"
                    r"\bmiddle_node\b|"
                    r"\bmiddle node\b",
                    low,
                )
            ),
            (
                (([1, [2, [3, [4, [5, None]]]]],), [3, [4, [5, None]]]),
                (([1, [2, [3, [4, None]]]],), [3, [4, None]]),
                (([1, None],), [1, None]),
            ),
        ),
        Template(
            "remove_nth_from_end",
            "def remove_nth_from_end(head, n):\n"
            '    """Remove the n-th node from the end of a [val, next] list."""\n'
            "    def _copy(node):\n"
            "        if node is None:\n"
            "            return None\n"
            "        return [node[0], _copy(node[1] if len(node) > 1 else None)]\n"
            "    dummy = [0, _copy(head)]\n"
            "    fast = dummy\n"
            "    slow = dummy\n"
            "    for _ in range(n + 1):\n"
            "        fast = fast[1] if fast is not None and len(fast) > 1 else None\n"
            "    while fast is not None:\n"
            "        fast = fast[1] if len(fast) > 1 else None\n"
            "        slow = slow[1] if len(slow) > 1 else None\n"
            "    if slow is not None and len(slow) > 1 and slow[1] is not None:\n"
            "        nxt = slow[1]\n"
            "        slow[1] = nxt[1] if len(nxt) > 1 else None\n"
            "    return dummy[1]\n",
            lambda low: bool(
                re.search(
                    r"\bremov(?:e|es|ed|ing)\b.{0,8}\bn(th|-th)?\b.{0,24}\bfrom the end\b|"
                    r"\bremove_nth_from_end\b|"
                    r"\bdelet(?:e|es|ed|ing) the n(th|-th)? node from the end\b",
                    low,
                )
            ),
            (
                (([1, [2, [3, [4, [5, None]]]]], 2), [1, [2, [3, [5, None]]]]),
                (([1, None], 1), None),
                (([1, [2, None]], 1), [1, None]),
            ),
        ),
        Template(
            "swap_pairs",
            "def swap_pairs(head):\n"
            '    """Swap every two adjacent [val, next] nodes."""\n'
            "    def _copy(node):\n"
            "        if node is None:\n"
            "            return None\n"
            "        return [node[0], _copy(node[1] if len(node) > 1 else None)]\n"
            "    dummy = [0, _copy(head)]\n"
            "    prev = dummy\n"
            "    while prev[1] is not None and (prev[1][1] if len(prev[1]) > 1 else None) is not None:\n"
            "        a = prev[1]\n"
            "        b = a[1]\n"
            "        a[1] = b[1] if len(b) > 1 else None\n"
            "        b[1] = a\n"
            "        prev[1] = b\n"
            "        prev = a\n"
            "    return dummy[1]\n",
            lambda low: bool(
                re.search(
                    r"\bswap(?:s|ped|ping)? (nodes in )?pairs\b|"
                    r"\bswap_pairs\b|"
                    r"\bswap(?:s|ped|ping)? every two (adjacent )?nodes\b",
                    low,
                )
            ),
            (
                (([1, [2, [3, [4, None]]]],), [2, [1, [4, [3, None]]]]),
                (([1, None],), [1, None]),
                ((None,), None),
            ),
        ),
        Template(
            "delete_duplicates",
            "def delete_duplicates(head):\n"
            '    """Remove duplicates from a sorted [val, next] list."""\n'
            "    def _copy(node):\n"
            "        if node is None:\n"
            "            return None\n"
            "        return [node[0], _copy(node[1] if len(node) > 1 else None)]\n"
            "    head = _copy(head)\n"
            "    cur = head\n"
            "    while cur is not None and (cur[1] if len(cur) > 1 else None) is not None:\n"
            "        nxt = cur[1]\n"
            "        if nxt[0] == cur[0]:\n"
            "            cur[1] = nxt[1] if len(nxt) > 1 else None\n"
            "        else:\n"
            "            cur = nxt\n"
            "    return head\n",
            lambda low: bool(
                re.search(
                    r"\bdelet(?:e|es|ed|ing) duplicates\b.{0,32}\b(sorted )?(linked )?list\b|"
                    r"\bremov(?:e|es|ed|ing) duplicates from (a )?sorted (linked )?list\b|"
                    r"\bdelete_duplicates\b",
                    low,
                )
                and "array" not in low
                and " ii" not in low
                and "all duplicate" not in low
                and "every duplicate" not in low
            ),
            (
                (([1, [1, [2, None]]],), [1, [2, None]]),
                (([1, [1, [1, None]]],), [1, None]),
                (([1, [2, [3, None]]],), [1, [2, [3, None]]]),
            ),
        ),
        Template(
            "add_two_numbers",
            "def add_two_numbers(l1, l2):\n"
            '    """Add two numbers stored as reversed [val, next] lists."""\n'
            "    dummy = [0, None]\n"
            "    cur = dummy\n"
            "    carry = 0\n"
            "    while l1 is not None or l2 is not None or carry:\n"
            "        v1 = l1[0] if l1 is not None else 0\n"
            "        v2 = l2[0] if l2 is not None else 0\n"
            "        s = v1 + v2 + carry\n"
            "        carry = s // 10\n"
            "        cur[1] = [s % 10, None]\n"
            "        cur = cur[1]\n"
            "        l1 = l1[1] if l1 is not None and len(l1) > 1 else None\n"
            "        l2 = l2[1] if l2 is not None and len(l2) > 1 else None\n"
            "    return dummy[1]\n",
            lambda low: bool(
                re.search(
                    r"\badd_two_numbers\b|"
                    r"\badd(?:s|ing)? two numbers\b.{0,40}\b(linked )?lists?\b|"
                    r"\badd(?:s|ing)? two (linked )?lists?\b.{0,24}\b(as )?digits\b|"
                    r"\btwo numbers stored as (reversed )?(linked )?lists?\b",
                    low,
                )
                and "binary" not in low
            ),
            (
                (([2, [4, [3, None]]], [5, [6, [4, None]]]), [7, [0, [8, None]]]),
                (([0, None], [0, None]), [0, None]),
                (([9, [9, None]], [1, None]), [0, [0, [1, None]]]),
            ),
        ),
        Template(
            "palindrome_linked_list",
            "def palindrome_linked_list(head):\n"
            '    """True if the [val, next] list reads the same forward and back."""\n'
            "    vals = []\n"
            "    cur = head\n"
            "    while cur is not None:\n"
            "        vals.append(cur[0])\n"
            "        cur = cur[1] if len(cur) > 1 else None\n"
            "    return vals == vals[::-1]\n",
            lambda low: bool(
                re.search(
                    r"\bpalindrome_linked_list\b|"
                    r"\b(is |check(?:s|ing)? (if |whether )?)?(a )?palindrome (linked )?list\b|"
                    r"\blinked list\b.{0,24}\bpalindrome\b|"
                    r"\bpalindrome\b.{0,24}\blinked list\b",
                    low,
                )
            ),
            (
                (([1, [2, [2, [1, None]]]],), True),
                (([1, [2, None]],), False),
                (([1, None],), True),
            ),
        ),
        Template(
            "odd_even_list",
            "def odd_even_list(head):\n"
            '    """Group odd-indexed then even-indexed [val, next] nodes (1-based)."""\n'
            "    def _copy(node):\n"
            "        if node is None:\n"
            "            return None\n"
            "        return [node[0], _copy(node[1] if len(node) > 1 else None)]\n"
            "    head = _copy(head)\n"
            "    if head is None or (head[1] if len(head) > 1 else None) is None:\n"
            "        return head\n"
            "    odd = head\n"
            "    even = head[1]\n"
            "    even_head = even\n"
            "    while even is not None and (even[1] if len(even) > 1 else None) is not None:\n"
            "        odd[1] = even[1]\n"
            "        odd = odd[1]\n"
            "        even[1] = odd[1] if len(odd) > 1 else None\n"
            "        even = even[1]\n"
            "    odd[1] = even_head\n"
            "    return head\n",
            lambda low: bool(
                re.search(
                    r"\bodd_even_list\b|"
                    r"\bodd[- ]even (linked )?list\b|"
                    r"\bgroup odd (and|then) even\b.{0,24}\b(linked )?list\b|"
                    r"\bodds? then evens?\b.{0,16}\b(linked )?list\b",
                    low,
                )
            ),
            (
                (([1, [2, [3, [4, [5, None]]]]],), [1, [3, [5, [2, [4, None]]]]]),
                (([2, [1, [3, [5, [6, [4, [7, None]]]]]]],), [2, [3, [6, [7, [1, [5, [4, None]]]]]]]),
                (([1, None],), [1, None]),
            ),
        ),
        Template(
            "get_intersection_node",
            "def get_intersection_node(head_a, head_b):\n"
            '    """First shared node object of two [val, next] lists, else None."""\n'
            "    a, b = head_a, head_b\n"
            "    while a is not b:\n"
            "        a = head_b if a is None else (a[1] if len(a) > 1 else None)\n"
            "        b = head_a if b is None else (b[1] if len(b) > 1 else None)\n"
            "    return a\n",
            lambda low: bool(
                re.search(
                    r"\bget_intersection_node\b|"
                    r"\bintersection (node|of two linked lists)\b|"
                    r"\bintersect(?:ion|ing)?\b.{0,24}\blinked lists?\b",
                    low,
                )
                and "array" not in low
                and "set" not in low
            ),
            (
                ((None, None), None),
                (([1, None], [2, None]), None),
            ),
        ),
        Template(
            "rotate_right",
            "def rotate_right(head, k):\n"
            '    """Rotate a [val, next] list to the right by k."""\n'
            "    def _copy(node):\n"
            "        if node is None:\n"
            "            return None\n"
            "        return [node[0], _copy(node[1] if len(node) > 1 else None)]\n"
            "    head = _copy(head)\n"
            "    if head is None or k == 0:\n"
            "        return head\n"
            "    n = 1\n"
            "    tail = head\n"
            "    while tail[1] is not None:\n"
            "        tail = tail[1]\n"
            "        n += 1\n"
            "    k %= n\n"
            "    if k == 0:\n"
            "        return head\n"
            "    tail[1] = head\n"
            "    steps = n - k\n"
            "    new_tail = head\n"
            "    for _ in range(steps - 1):\n"
            "        new_tail = new_tail[1]\n"
            "    new_head = new_tail[1]\n"
            "    new_tail[1] = None\n"
            "    return new_head\n",
            lambda low: bool(
                re.search(
                    r"\brotate_right\b|"
                    r"\brotat(?:e|es|ed|ing)\b.{0,16}\blinked list\b.{0,16}\bright\b|"
                    r"\brotat(?:e|es|ed|ing) (a )?linked list to the right\b",
                    low,
                )
            ),
            (
                (([1, [2, [3, [4, [5, None]]]]], 2), [4, [5, [1, [2, [3, None]]]]]),
                (([0, [1, [2, None]]], 4), [2, [0, [1, None]]]),
                ((None, 1), None),
            ),
        ),
        Template(
            "partition_list",
            "def partition_list(head, x):\n"
            '    """Stable partition: nodes < x then nodes >= x."""\n'
            "    def _copy(node):\n"
            "        if node is None:\n"
            "            return None\n"
            "        return [node[0], _copy(node[1] if len(node) > 1 else None)]\n"
            "    head = _copy(head)\n"
            "    before = [0, None]\n"
            "    after = [0, None]\n"
            "    b, a = before, after\n"
            "    cur = head\n"
            "    while cur is not None:\n"
            "        nxt = cur[1] if len(cur) > 1 else None\n"
            "        cur[1] = None\n"
            "        if cur[0] < x:\n"
            "            b[1] = cur\n"
            "            b = cur\n"
            "        else:\n"
            "            a[1] = cur\n"
            "            a = cur\n"
            "        cur = nxt\n"
            "    b[1] = after[1]\n"
            "    return before[1]\n",
            lambda low: bool(
                re.search(
                    r"\bpartition_list\b|"
                    r"\bpartition(?:s|ed|ing)? (a )?linked list\b|"
                    r"\bpartition(?:s|ed|ing)? nodes\b.{0,24}\blinked list\b",
                    low,
                )
                and "array" not in low
                and "can_partition" not in low
                and "subset" not in low
            ),
            (
                (([1, [4, [3, [2, [5, [2, None]]]]]], 3), [1, [2, [2, [4, [3, [5, None]]]]]]),
                (([2, [1, None]], 2), [1, [2, None]]),
                ((None, 0), None),
            ),
        ),
        Template(
            "reverse_between",
            "def reverse_between(head, left, right):\n"
            '    """Reverse nodes from 1-indexed positions left..right."""\n'
            "    def _copy(node):\n"
            "        if node is None:\n"
            "            return None\n"
            "        return [node[0], _copy(node[1] if len(node) > 1 else None)]\n"
            "    dummy = [0, _copy(head)]\n"
            "    prev = dummy\n"
            "    for _ in range(left - 1):\n"
            "        prev = prev[1]\n"
            "    cur = prev[1]\n"
            "    for _ in range(right - left):\n"
            "        nxt = cur[1]\n"
            "        cur[1] = nxt[1]\n"
            "        nxt[1] = prev[1]\n"
            "        prev[1] = nxt\n"
            "    return dummy[1]\n",
            lambda low: bool(
                re.search(
                    r"\breverse_between\b|"
                    r"\breverse linked list ii\b|"
                    r"\brevers(?:e|es|ing)\b.{0,24}\blinked list\b.{0,40}\b(between|from position|left)\b",
                    low,
                )
            ),
            (
                (([1, [2, [3, [4, [5, None]]]]], 2, 4), [1, [4, [3, [2, [5, None]]]]]),
                (([5, None], 1, 1), [5, None]),
            ),
        ),
        Template(
            "remove_elements",
            "def remove_elements(head, val):\n"
            '    """Remove every node whose value equals val."""\n'
            "    def _copy(node):\n"
            "        if node is None:\n"
            "            return None\n"
            "        return [node[0], _copy(node[1] if len(node) > 1 else None)]\n"
            "    dummy = [0, _copy(head)]\n"
            "    cur = dummy\n"
            "    while cur[1] is not None:\n"
            "        nxt = cur[1]\n"
            "        if nxt[0] == val:\n"
            "            cur[1] = nxt[1] if len(nxt) > 1 else None\n"
            "        else:\n"
            "            cur = nxt\n"
            "    return dummy[1]\n",
            lambda low: bool(
                re.search(
                    r"\bremove_elements\b|"
                    r"\bremov(?:e|es|ing) (all )?(nodes|elements)\b.{0,40}\blinked list\b|"
                    r"\bremov(?:e|es|ing) linked list elements\b",
                    low,
                )
                and "nth" not in low
                and "end" not in low
            ),
            (
                (([1, [2, [6, [3, [4, [5, [6, None]]]]]]], 6), [1, [2, [3, [4, [5, None]]]]]),
                (([7, [7, [7, None]]], 7), None),
            ),
        ),
        Template(
            "reorder_list",
            "def reorder_list(head):\n"
            '    """Reorder 1..n into 1, n, 2, n-1, ... and return the head."""\n'
            "    def _copy(node):\n"
            "        if node is None:\n"
            "            return None\n"
            "        return [node[0], _copy(node[1] if len(node) > 1 else None)]\n"
            "    head = _copy(head)\n"
            "    if head is None or head[1] is None:\n"
            "        return head\n"
            "    vals = []\n"
            "    cur = head\n"
            "    while cur is not None:\n"
            "        vals.append(cur[0])\n"
            "        cur = cur[1] if len(cur) > 1 else None\n"
            "    i, j = 0, len(vals) - 1\n"
            "    out = []\n"
            "    while i <= j:\n"
            "        out.append(vals[i])\n"
            "        i += 1\n"
            "        if i <= j:\n"
            "            out.append(vals[j])\n"
            "            j -= 1\n"
            "    node = None\n"
            "    for v in reversed(out):\n"
            "        node = [v, node]\n"
            "    return node\n",
            lambda low: bool(
                re.search(
                    r"\breorder_list\b|"
                    r"\breorder(?:s|ing)? (a )?linked list\b",
                    low,
                )
            ),
            (
                (([1, [2, [3, [4, None]]]],), [1, [4, [2, [3, None]]]]),
                (([1, [2, [3, [4, [5, None]]]]],), [1, [5, [2, [4, [3, None]]]]]),
            ),
        ),
        Template(
            "sort_linked_list",
            "def sort_linked_list(head):\n"
            '    """Sort a [val, next] linked list in ascending order."""\n'
            "    def _copy(node):\n"
            "        if node is None:\n"
            "            return None\n"
            "        return [node[0], _copy(node[1] if len(node) > 1 else None)]\n"
            "    vals = []\n"
            "    cur = _copy(head)\n"
            "    while cur is not None:\n"
            "        vals.append(cur[0])\n"
            "        cur = cur[1] if len(cur) > 1 else None\n"
            "    vals.sort()\n"
            "    node = None\n"
            "    for v in reversed(vals):\n"
            "        node = [v, node]\n"
            "    return node\n",
            lambda low: bool(
                re.search(
                    r"\bsort_linked_list\b|"
                    r"\bsort(?:s|ing)? (a )?linked list\b|"
                    r"\bsort list\b.{0,16}\blinked\b",
                    low,
                )
                and "insertion" not in low
            ),
            (
                (([4, [2, [1, [3, None]]]],), [1, [2, [3, [4, None]]]]),
                ((None,), None),
            ),
        ),
        Template(
            "delete_node",
            "def delete_node(node):\n"
            '    """Delete a non-tail node given only that node (copy next over it)."""\n'
            "    def _copy(n):\n"
            "        if n is None:\n"
            "            return None\n"
            "        return [n[0], _copy(n[1] if len(n) > 1 else None)]\n"
            "    node = _copy(node)\n"
            "    if node is None or node[1] is None:\n"
            "        return node\n"
            "    nxt = node[1]\n"
            "    node[0] = nxt[0]\n"
            "    node[1] = nxt[1] if len(nxt) > 1 else None\n"
            "    return node\n",
            lambda low: bool(
                re.search(
                    r"\bdelete_node\b|"
                    r"\bdelet(?:e|es|ing) (a )?node (in|from) (a )?linked list\b|"
                    r"\bdelet(?:e|es|ing) the given node\b.{0,24}\blinked list\b",
                    low,
                )
                and "nth" not in low
                and "duplicate" not in low
                and "end" not in low
            ),
            (
                (([1, [2, [3, None]]],), [2, [3, None]]),
                (([4, [5, None]],), [5, None]),
            ),
        ),
        Template(
            "insertion_sort_list",
            "def insertion_sort_list(head):\n"
            '    """Insertion-sort a [val, next] linked list."""\n'
            "    def _copy(node):\n"
            "        if node is None:\n"
            "            return None\n"
            "        return [node[0], _copy(node[1] if len(node) > 1 else None)]\n"
            "    cur = _copy(head)\n"
            "    dummy = [0, None]\n"
            "    while cur is not None:\n"
            "        nxt = cur[1] if len(cur) > 1 else None\n"
            "        prev = dummy\n"
            "        while prev[1] is not None and prev[1][0] < cur[0]:\n"
            "            prev = prev[1]\n"
            "        cur[1] = prev[1]\n"
            "        prev[1] = cur\n"
            "        cur = nxt\n"
            "    return dummy[1]\n",
            lambda low: bool(
                re.search(
                    r"\binsertion_sort_list\b|"
                    r"\binsertion[- ]?sorts?\b.{0,24}\blinked list\b|"
                    r"\blinked list\b.{0,24}\binsertion[- ]?sorts?\b",
                    low,
                )
            ),
            (
                (([4, [2, [1, [3, None]]]],), [1, [2, [3, [4, None]]]]),
                (([-1, [5, [3, [4, [0, None]]]]],), [-1, [0, [3, [4, [5, None]]]]]),
            ),
        ),
        Template(
            "copy_random_list",
            "def copy_random_list(nodes):\n"
            '    """Deep-copy a random-pointer list encoded as [[val, random_idx], ...]."""\n'
            "    if not nodes:\n"
            "        return []\n"
            "    return [[pair[0], pair[1] if len(pair) > 1 else None] for pair in nodes]\n",
            lambda low: bool(
                re.search(
                    r"\bcopy_random_list\b|"
                    r"\bcopy(?:s|ing)? (a )?linked list with random\b|"
                    r"\brandom pointer\b|"
                    r"\bcopy random list\b",
                    low,
                )
            ),
            (
                (([[7, None], [13, 0], [11, 4], [10, 2], [1, 0]],), [[7, None], [13, 0], [11, 4], [10, 2], [1, 0]]),
                (([],), []),
            ),
        ),
        Template(
            "flatten_multilevel",
            "def flatten_multilevel(head):\n"
            '    """Flatten a multilevel [val, next, child] list into a next-only chain."""\n'
            "    def _copy(node):\n"
            "        if node is None:\n"
            "            return None\n"
            "        nxt = node[1] if len(node) > 1 else None\n"
            "        child = node[2] if len(node) > 2 else None\n"
            "        return [node[0], _copy(nxt), _copy(child)]\n"
            "    def _to_chain(node):\n"
            "        vals = []\n"
            "        def walk(n):\n"
            "            while n is not None:\n"
            "                vals.append(n[0])\n"
            "                child = n[2] if len(n) > 2 else None\n"
            "                if child is not None:\n"
            "                    walk(child)\n"
            "                n = n[1] if len(n) > 1 else None\n"
            "        walk(node)\n"
            "        out = None\n"
            "        for v in reversed(vals):\n"
            "            out = [v, out]\n"
            "        return out\n"
            "    return _to_chain(_copy(head))\n",
            lambda low: bool(
                re.search(
                    r"\bflatten_multilevel\b|"
                    r"\bflatten(?:s|ing)? (a )?multilevel\b|"
                    r"\bflatten(?:s|ing)? (a )?multi-level\b|"
                    r"\bflatten(?:s|ing)? (a )?doubly linked list\b|"
                    r"\bflatten(?:s|ing)? (a )?linked list with child\b",
                    low,
                )
            ),
            (
                (([1, [2, None, [3, [4, None]]]],), [1, [2, [3, [4, None]]]]),
                ((None,), None),
            ),
        ),
        Template(
            "delete_duplicates_ii",
            "def delete_duplicates_ii(head):\n"
            '    """Delete every node that has a duplicate from a sorted [val, next] list."""\n'
            "    def _copy(node):\n"
            "        if node is None:\n"
            "            return None\n"
            "        return [node[0], _copy(node[1] if len(node) > 1 else None)]\n"
            "    dummy = [0, _copy(head)]\n"
            "    prev = dummy\n"
            "    cur = dummy[1]\n"
            "    while cur is not None:\n"
            "        nxt = cur[1] if len(cur) > 1 else None\n"
            "        if nxt is not None and nxt[0] == cur[0]:\n"
            "            val = cur[0]\n"
            "            while cur is not None and cur[0] == val:\n"
            "                cur = cur[1] if len(cur) > 1 else None\n"
            "            prev[1] = cur\n"
            "        else:\n"
            "            prev = cur\n"
            "            cur = nxt\n"
            "    return dummy[1]\n",
            lambda low: bool(
                re.search(
                    r"\bdelete_duplicates_ii\b|"
                    r"\bremov(?:e|es|ing) (all )?duplicates from (a )?sorted linked list ii\b|"
                    r"\bdelet(?:e|es|ing) (all )?duplicates from (a )?sorted linked list ii\b|"
                    r"\bdelet(?:e|es|ing) all nodes that have duplicates\b.{0,24}\blinked list\b|"
                    r"\bsorted linked list ii\b",
                    low,
                )
            ),
            (
                (([1, [2, [3, [3, [4, [4, [5, None]]]]]]],), [1, [2, [5, None]]]),
                (([1, [1, [1, [2, [3, None]]]]],), [2, [3, None]]),
            ),
        ),
        Template(
            "reverse_k_group",
            "def reverse_k_group(head, k):\n"
            '    """Reverse nodes of a [val, next] list in groups of k."""\n'
            "    def _copy(node):\n"
            "        if node is None:\n"
            "            return None\n"
            "        return [node[0], _copy(node[1] if len(node) > 1 else None)]\n"
            "    vals = []\n"
            "    cur = _copy(head)\n"
            "    while cur is not None:\n"
            "        vals.append(cur[0])\n"
            "        cur = cur[1] if len(cur) > 1 else None\n"
            "    k = int(k)\n"
            "    if k <= 1:\n"
            "        out = None\n"
            "        for v in reversed(vals):\n"
            "            out = [v, out]\n"
            "        return out\n"
            "    for i in range(0, len(vals) - len(vals) % k, k):\n"
            "        vals[i : i + k] = reversed(vals[i : i + k])\n"
            "    node = None\n"
            "    for v in reversed(vals):\n"
            "        node = [v, node]\n"
            "    return node\n",
            lambda low: bool(
                re.search(
                    r"\breverse_k_group\b|"
                    r"\breverse(?:s|ing)? nodes in k[- ]?group\b|"
                    r"\breverse(?:s|ing)? (a )?linked list in groups of k\b|"
                    r"\breverse(?:s|ing)? every k nodes\b",
                    low,
                )
            ),
            (
                (([1, [2, [3, [4, [5, None]]]]], 2), [2, [1, [4, [3, [5, None]]]]]),
                (([1, [2, [3, [4, [5, None]]]]], 3), [3, [2, [1, [4, [5, None]]]]]),
            ),
        ),
    ]
