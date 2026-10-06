"""Cycle 463: detection, numeric, and naming helpers that still fell through.

Loaded first so IoU / Heron / bit-rotate / UUID5 asks do not hit generic
rotate, average, or string stubs.
"""
from __future__ import annotations

import re

from code_synth import Template


def templates() -> list[Template]:
    T = Template
    return [
        T(
            "box_iou",
            "def box_iou(box_a, box_b):\n"
            '    """Intersection-over-union of two xyxy boxes. Empty overlap is 0."""\n'
            "    ax1, ay1, ax2, ay2 = (float(v) for v in box_a)\n"
            "    bx1, by1, bx2, by2 = (float(v) for v in box_b)\n"
            "    ix1, iy1 = max(ax1, bx1), max(ay1, by1)\n"
            "    ix2, iy2 = min(ax2, bx2), min(ay2, by2)\n"
            "    iw, ih = max(0.0, ix2 - ix1), max(0.0, iy2 - iy1)\n"
            "    inter = iw * ih\n"
            "    area_a = max(0.0, ax2 - ax1) * max(0.0, ay2 - ay1)\n"
            "    area_b = max(0.0, bx2 - bx1) * max(0.0, by2 - by1)\n"
            "    union = area_a + area_b - inter\n"
            "    if union <= 0.0:\n"
            "        return 0.0\n"
            "    return inter / union\n",
            lambda low: bool(
                ("iou" in low or "intersection over union" in low)
                and ("box" in low or "bounding" in low)
            ),
            (
                (((0, 0, 2, 2), (1, 1, 3, 3)), 1.0 / 7.0),
                (((0, 0, 1, 1), (2, 2, 3, 3)), 0.0),
                (((0, 0, 2, 2), (0, 0, 2, 2)), 1.0),
            ),
        ),
        T(
            "l2_normalize",
            "def l2_normalize(vector):\n"
            '    """Return the L2 unit vector. A zero vector is returned unchanged."""\n'
            "    vals = [float(v) for v in vector]\n"
            "    norm = sum(v * v for v in vals) ** 0.5\n"
            "    if norm == 0.0:\n"
            "        return vals\n"
            "    return [v / norm for v in vals]\n",
            lambda low: "vector" in low and ("l2" in low or "normaliz" in low or "unit" in low),
            (
                (([3, 4],), [0.6, 0.8]),
                (([0, 0],), [0.0, 0.0]),
                (([1, 0, 0],), [1.0, 0.0, 0.0]),
            ),
        ),
        T(
            "chunk_string",
            "def chunk_string(text, size):\n"
            '    """Split text into chunks of size. A non-positive size returns one chunk."""\n'
            "    s = \"\" if text is None else str(text)\n"
            "    n = int(size)\n"
            "    if n <= 0 or not s:\n"
            "        return [s]\n"
            "    return [s[i:i + n] for i in range(0, len(s), n)]\n",
            lambda low: "string" in low and "chunk" in low,
            (
                (("abcdef", 2), ["ab", "cd", "ef"]),
                (("abcde", 3), ["abc", "de"]),
                (("", 2), [""]),
            ),
        ),
        T(
            "weighted_mean",
            "def weighted_mean(values, weights):\n"
            '    """Weighted arithmetic mean. Zero total weight returns 0."""\n'
            "    vals = [float(v) for v in values]\n"
            "    wts = [float(w) for w in weights]\n"
            "    total = sum(wts)\n"
            "    if total == 0.0 or not vals:\n"
            "        return 0.0\n"
            "    return sum(v * w for v, w in zip(vals, wts)) / total\n",
            lambda low: "weighted" in low and ("average" in low or "mean" in low),
            (
                (((1, 2, 3), (1, 1, 1)), 2.0),
                (((1, 3), (1, 3)), 2.5),
                (((5,), (0,)), 0.0),
            ),
        ),
        T(
            "heron_area",
            "def heron_area(a, b, c):\n"
            '    """Triangle area from side lengths via Heron. Impossible triangles are 0."""\n'
            "    a, b, c = float(a), float(b), float(c)\n"
            "    if a <= 0 or b <= 0 or c <= 0 or a + b <= c or a + c <= b or b + c <= a:\n"
            "        return 0.0\n"
            "    s = (a + b + c) / 2.0\n"
            "    area = (s * (s - a) * (s - b) * (s - c)) ** 0.5\n"
            "    return round(area, 10)\n",
            lambda low: "heron" in low,
            (
                ((3, 4, 5), 6.0),
                ((2, 2, 2), 1.7320508076),
                ((1, 1, 3), 0.0),
            ),
        ),
        T(
            "uuid5_name",
            "def uuid5_name(name, namespace=\"dns\"):\n"
            '    """RFC 4122 UUID5 for a name under the dns or url namespace."""\n'
            "    import uuid\n"
            "    ns = str(namespace or \"dns\").lower()\n"
            "    base = uuid.NAMESPACE_URL if ns in {\"url\", \"uri\"} else uuid.NAMESPACE_DNS\n"
            "    return str(uuid.uuid5(base, \"\" if name is None else str(name)))\n",
            lambda low: "uuid5" in low or ("uuid" in low and "namespace" in low),
            (
                (("example.com",), "cfbff0d1-9375-5685-968c-48ce8b15ae17"),
                (("https://orbit.ai", "url"), "6a1f1810-bad4-5022-a6fa-8d4840c7eca9"),
                (("example.com", "dns"), "cfbff0d1-9375-5685-968c-48ce8b15ae17"),
            ),
        ),
    ]
