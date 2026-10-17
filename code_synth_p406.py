"""Cycle 406: nested_list_weight_sum_ii, design_in_memory_file_system,
magic_dictionary, add_and_search_words, max_frequency_stack,
design_stack_with_increment.

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
            "nested_list_weight_sum_ii",
            '''def nested_list_weight_sum_ii(nested_list):
    """Weighted sum of integers in a nested list (LeetCode 364).

    Weight is the inverse of depth: leaves at max depth have weight 1,
    shallower leaves have higher weight. nested_list elements are int or list.
    """
    def max_depth(nl, d=1):
        m = d
        for x in nl:
            if isinstance(x, list):
                m = max(m, max_depth(x, d + 1))
        return m

    def walk(nl, d, md, acc):
        for x in nl:
            if isinstance(x, list):
                walk(x, d + 1, md, acc)
            else:
                acc[0] += x * (md - d + 1)

    md = max_depth(nested_list)
    acc = [0]
    walk(nested_list, 1, md, acc)
    return acc[0]
''',
            lambda low: bool(
                re.search(
                    r"\bnested[- ]list[- ]weight[- ]sum[- ]?(ii|2|two)\b|"
                    r"\bweight(?:ed)? sum\b.*\bnested\b.*\b(ii|2|two)\b|"
                    r"\bleetcode 364\b",
                    low,
                )
            ),
            examples=[
                (([[1, 1], 2, [1, 1]],), 8),
                (([1, [4, [6]]],), 17),
            ],
        ),
        T(
            "design_in_memory_file_system",
            '''def design_in_memory_file_system(ops):
    """In-memory file system (LeetCode 588).

    ops: list of (\"FileSystem\"|\"ls\"|\"mkdir\"|\"addContentToFile\"|\"readContentFromFile\", *args).
    Returns list of results (None for void ops).
    """
    class FileSystem:
        def __init__(self):
            self.root = {}

        def _node(self, path: str, create_dirs: bool = False):
            parts = [p for p in path.split("/") if p]
            cur = self.root
            for i, p in enumerate(parts):
                if p not in cur:
                    if not create_dirs:
                        return None, None
                    cur[p] = {}
                if not isinstance(cur[p], dict):
                    return cur, p  # file
                if i == len(parts) - 1 and create_dirs is False:
                    return cur, p
                cur = cur[p]
            return cur, None

        def ls(self, path: str):
            if path == "/":
                return sorted(self.root.keys())
            parts = [p for p in path.split("/") if p]
            cur = self.root
            for i, p in enumerate(parts):
                if p not in cur:
                    return []
                if not isinstance(cur[p], dict):
                    return [p]
                cur = cur[p]
            return sorted(cur.keys())

        def mkdir(self, path: str):
            self._node(path, create_dirs=True)

        def addContentToFile(self, filePath: str, content: str):
            parts = [p for p in filePath.split("/") if p]
            cur = self.root
            for p in parts[:-1]:
                if p not in cur:
                    cur[p] = {}
                cur = cur[p]
            name = parts[-1]
            if name not in cur or isinstance(cur[name], dict):
                cur[name] = ""
            cur[name] += content

        def readContentFromFile(self, filePath: str):
            parts = [p for p in filePath.split("/") if p]
            cur = self.root
            for p in parts[:-1]:
                cur = cur[p]
            return cur[parts[-1]]

    out = []
    obj = None
    for op in ops:
        name, *args = op
        if name == "FileSystem":
            obj = FileSystem()
            out.append(None)
        else:
            out.append(getattr(obj, name)(*args))
    return out
''',
            lambda low: bool(
                re.search(
                    r"\b(design |implement )?(an? )?(in[- ]memory )?file system\b|"
                    r"\bleetcode 588\b|"
                    r"\bls\b.*\bmkdir\b.*\baddcontenttofile\b",
                    low,
                )
            ),
            examples=[
                (
                    (
                        [
                            ("FileSystem",),
                            ("ls", "/"),
                            ("mkdir", "/a/b/c"),
                            ("addContentToFile", "/a/b/c/d", "hello"),
                            ("ls", "/"),
                            ("readContentFromFile", "/a/b/c/d"),
                        ],
                    ),
                    [None, [], None, None, ["a"], "hello"],
                ),
            ],
        ),
        T(
            "magic_dictionary",
            '''def magic_dictionary(ops):
    """Implement MagicDictionary (LeetCode 676).

    ops: list of (\"MagicDictionary\"|\"buildDict\"|\"search\", *args).
    search returns True if exactly one character differs from a dict word.
    """
    class MagicDictionary:
        def __init__(self):
            self.words = []

        def buildDict(self, dictionary):
            self.words = list(dictionary)

        def search(self, searchWord: str) -> bool:
            for w in self.words:
                if len(w) != len(searchWord):
                    continue
                diff = sum(a != b for a, b in zip(w, searchWord))
                if diff == 1:
                    return True
            return False

    out = []
    obj = None
    for op in ops:
        name, *args = op
        if name == "MagicDictionary":
            obj = MagicDictionary()
            out.append(None)
        else:
            out.append(getattr(obj, name)(*args))
    return out
''',
            lambda low: bool(
                re.search(
                    r"\bmagic dictionary\b|"
                    r"\bimplement magicdictionary\b|"
                    r"\bleetcode 676\b",
                    low,
                )
            ),
            examples=[
                (
                    (
                        [
                            ("MagicDictionary",),
                            ("buildDict", ["hello", "leetcode"]),
                            ("search", "hello"),
                            ("search", "hhllo"),
                            ("search", "hell"),
                            ("search", "leetcoded"),
                        ],
                    ),
                    [None, None, False, True, False, False],
                ),
            ],
        ),
        T(
            "add_and_search_words",
            '''def add_and_search_words(ops):
    """Design add-and-search-words data structure (LeetCode 211).

    Supports '.' wildcard in search. ops: (\"WordDictionary\"|\"addWord\"|\"search\", *args).
    """
    class WordDictionary:
        def __init__(self):
            self.root = {}

        def addWord(self, word: str):
            node = self.root
            for c in word:
                node = node.setdefault(c, {})
            node["#"] = True

        def search(self, word: str) -> bool:
            def dfs(i, node):
                if i == len(word):
                    return "#" in node
                c = word[i]
                if c == ".":
                    return any(
                        dfs(i + 1, node[k]) for k in node if k != "#"
                    )
                if c not in node:
                    return False
                return dfs(i + 1, node[c])

            return dfs(0, self.root)

    out = []
    obj = None
    for op in ops:
        name, *args = op
        if name == "WordDictionary":
            obj = WordDictionary()
            out.append(None)
        else:
            out.append(getattr(obj, name)(*args))
    return out
''',
            lambda low: bool(
                re.search(
                    r"\badd and search word\b|"
                    r"\bdesign add and search words\b|"
                    r"\bword dictionary\b.*\b(wildcard|dot|\.)\b|"
                    r"\bleetcode 211\b",
                    low,
                )
                and "magic" not in low
            ),
            examples=[
                (
                    (
                        [
                            ("WordDictionary",),
                            ("addWord", "bad"),
                            ("addWord", "dad"),
                            ("addWord", "mad"),
                            ("search", "pad"),
                            ("search", "bad"),
                            ("search", ".ad"),
                            ("search", "b.."),
                        ],
                    ),
                    [None, None, None, None, False, True, True, True],
                ),
            ],
        ),
        T(
            "max_frequency_stack",
            '''def max_frequency_stack(ops):
    """Maximum Frequency Stack (LeetCode 895).

    ops: list of (\"FreqStack\"|\"push\"|\"pop\", *args). pop returns most frequent;
    ties break by most recent.
    """
    from collections import defaultdict

    class FreqStack:
        def __init__(self):
            self.freq = defaultdict(int)
            self.group = defaultdict(list)
            self.maxf = 0

        def push(self, val: int):
            f = self.freq[val] + 1
            self.freq[val] = f
            if f > self.maxf:
                self.maxf = f
            self.group[f].append(val)

        def pop(self) -> int:
            val = self.group[self.maxf].pop()
            self.freq[val] -= 1
            if not self.group[self.maxf]:
                self.maxf -= 1
            return val

    out = []
    obj = None
    for op in ops:
        name, *args = op
        if name == "FreqStack":
            obj = FreqStack()
            out.append(None)
        else:
            out.append(getattr(obj, name)(*args))
    return out
''',
            lambda low: bool(
                re.search(
                    r"\bmax(?:imum)? frequency stack\b|"
                    r"\bfreqstack\b|"
                    r"\bleetcode 895\b",
                    low,
                )
            ),
            examples=[
                (
                    (
                        [
                            ("FreqStack",),
                            ("push", 5),
                            ("push", 7),
                            ("push", 5),
                            ("push", 7),
                            ("push", 4),
                            ("push", 5),
                            ("pop",),
                            ("pop",),
                            ("pop",),
                            ("pop",),
                        ],
                    ),
                    [None, None, None, None, None, None, None, 5, 7, 5, 4],
                ),
            ],
        ),
        T(
            "design_stack_with_increment",
            '''def design_stack_with_increment(ops):
    """Design a stack that supports increment on bottom k elements (LeetCode 1381).

    ops: (\"CustomStack\"|\"push\"|\"pop\"|\"increment\", *args).
    """
    class CustomStack:
        def __init__(self, maxSize: int):
            self.maxSize = maxSize
            self.stack = []
            self.inc = []

        def push(self, x: int):
            if len(self.stack) < self.maxSize:
                self.stack.append(x)
                self.inc.append(0)

        def pop(self) -> int:
            if not self.stack:
                return -1
            if len(self.inc) > 1:
                self.inc[-2] += self.inc[-1]
            return self.stack.pop() + self.inc.pop()

        def increment(self, k: int, val: int):
            i = min(k, len(self.stack)) - 1
            if i >= 0:
                self.inc[i] += val

    out = []
    obj = None
    for op in ops:
        name, *args = op
        if name == "CustomStack":
            obj = CustomStack(args[0])
            out.append(None)
        else:
            out.append(getattr(obj, name)(*args))
    return out
''',
            lambda low: bool(
                re.search(
                    r"\bdesign (a )?stack with increment\b|"
                    r"\bcustom stack\b.*\bincrement\b|"
                    r"\bleetcode 1381\b",
                    low,
                )
            ),
            examples=[
                (
                    (
                        [
                            ("CustomStack", 3),
                            ("push", 1),
                            ("push", 2),
                            ("pop",),
                            ("push", 2),
                            ("push", 3),
                            ("push", 4),
                            ("increment", 5, 100),
                            ("increment", 2, 100),
                            ("pop",),
                            ("pop",),
                            ("pop",),
                            ("pop",),
                        ],
                    ),
                    [None, None, None, 2, None, None, None, None, None, 103, 202, 201, -1],
                ),
            ],
        ),
    ]
