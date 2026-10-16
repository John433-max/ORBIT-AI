"""Cycle 590: golden-section search, geohash decode, DBSCAN for CI unit tests.

Educational pure-Python. Matchers kept narrow.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "golden_section_search",
            "def golden_section_search(f, a, b, tol=1e-5):\n"
            '    """Golden-section search for a minimum of f on [a, b] (educational)."""\n'
            "    phi = (1 + 5 ** 0.5) / 2\n"
            "    c = b - (b - a) / phi\n"
            "    d = a + (b - a) / phi\n"
            "    while abs(b - a) > tol:\n"
            "        if f(c) < f(d):\n"
            "            b = d\n"
            "        else:\n"
            "            a = c\n"
            "        c = b - (b - a) / phi\n"
            "        d = a + (b - a) / phi\n"
            "    return (a + b) / 2\n",
            lambda low: "golden" in low and "section" in low,
            examples=[((lambda x: (x - 2) ** 2, 0.0, 5.0), 2.0000019054494933)],
        ),
        T(
            "geohash_decode",
            "def geohash_decode(h):\n"
            '    """Decode a geohash string to (lat, lon) center (educational)."""\n'
            "    base32 = '0123456789bcdefghjkmnpqrstuvwxyz'\n"
            "    lat_min, lat_max = -90.0, 90.0\n"
            "    lon_min, lon_max = -180.0, 180.0\n"
            "    even = True\n"
            "    for c in h:\n"
            "        idx = base32.index(c)\n"
            "        for bit in range(4, -1, -1):\n"
            "            if even:\n"
            "                mid = (lon_min + lon_max) / 2\n"
            "                if idx & (1 << bit):\n"
            "                    lon_min = mid\n"
            "                else:\n"
            "                    lon_max = mid\n"
            "            else:\n"
            "                mid = (lat_min + lat_max) / 2\n"
            "                if idx & (1 << bit):\n"
            "                    lat_min = mid\n"
            "                else:\n"
            "                    lat_max = mid\n"
            "            even = not even\n"
            "    return ((lat_min + lat_max) / 2, (lon_min + lon_max) / 2)\n",
            lambda low: "geohash" in low and "decode" in low,
            examples=[(("u4pruydqqvj",), (57.64911063015461, 10.407439693808556))],
        ),
        T(
            "dbscan_demo",
            "def dbscan_demo(points, eps=1.0, min_pts=2):\n"
            '    """Simple DBSCAN demo returning cluster labels (educational)."""\n'
            "    n = len(points)\n"
            "    labels = [-1] * n\n"
            "    def dist(i, j):\n"
            "        return abs(points[i] - points[j])\n"
            "    cid = 0\n"
            "    for i in range(n):\n"
            "        if labels[i] != -1:\n"
            "            continue\n"
            "        neigh = [j for j in range(n) if dist(i, j) <= eps]\n"
            "        if len(neigh) < min_pts:\n"
            "            continue\n"
            "        labels[i] = cid\n"
            "        seed = neigh[:]\n"
            "        for j in seed:\n"
            "            if labels[j] == -1:\n"
            "                labels[j] = cid\n"
            "                nn = [k for k in range(n) if dist(j, k) <= eps]\n"
            "                if len(nn) >= min_pts:\n"
            "                    seed.extend(k for k in nn if k not in seed)\n"
            "        cid += 1\n"
            "    return labels\n",
            lambda low: "dbscan" in low,
            examples=[(([0.0, 0.1, 5.0],), [0, 0, -1])],
        ),
    ]
