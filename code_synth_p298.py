"""Cycle 598: educational IDA*, simple MCTS, natural cubic spline, 2D PCA.

Previously unmatched by match_template. Narrow matchers so they do not
steal A*, BFS, existing interpolators, or SVD/singularize.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "ida_star",
            "def ida_star(start, goal, neighbors, heuristic):\n"
            '    """Iterative deepening A*. neighbors(n)->list[(next, cost)]. heuristic(n)->float."""\n'
            "    def search(node, g, bound, path):\n"
            "        f = g + heuristic(node)\n"
            "        if f > bound:\n"
            "            return f, None\n"
            "        if node == goal:\n"
            "            return f, path\n"
            "        min_over = float('inf')\n"
            "        for nxt, cost in neighbors(node):\n"
            "            if nxt in path:\n"
            "                continue\n"
            "            t, found = search(nxt, g + cost, bound, path + [nxt])\n"
            "            if found is not None:\n"
            "                return t, found\n"
            "            if t < min_over:\n"
            "                min_over = t\n"
            "        return min_over, None\n"
            "    bound = heuristic(start)\n"
            "    for _ in range(1000):\n"
            "        t, found = search(start, 0, bound, [start])\n"
            "        if found is not None:\n"
            "            return found\n"
            "        if t == float('inf'):\n"
            "            return None\n"
            "        bound = t\n"
            "    return None\n",
            lambda q: bool(
                re.search(r"\bida\s*\*|\bida[\s_-]?star|iterative\s+deepening\s+a", q, re.I)
            ),
            examples=(
                (
                    (
                        0,
                        3,
                        lambda n: [(n + 1, 1)] if n < 3 else [],
                        lambda n: 3 - n,
                    ),
                    [0, 1, 2, 3],
                ),
            ),
        ),
        T(
            "mcts_simple",
            "def mcts_simple(state, actions_fn, terminal_fn, reward_fn, n_sims=64, seed=0):\n"
            '    """Simple one-step Monte Carlo search: pick the action with best average random rollouts."""\n'
            "    import random\n"
            "    rng = random.Random(seed)\n"
            "    acts = list(actions_fn(state))\n"
            "    if not acts:\n"
            "        return None\n"
            "    scores = {a: 0.0 for a in acts}\n"
            "    counts = {a: 0 for a in acts}\n"
            "    for i in range(n_sims):\n"
            "        a = acts[i % len(acts)]\n"
            "        s = a  # action is the next state for this educational 1-ply version\n"
            "        while not terminal_fn(s):\n"
            "            opts = list(actions_fn(s))\n"
            "            if not opts:\n"
            "                break\n"
            "            s = rng.choice(opts)\n"
            "        scores[a] += reward_fn(s)\n"
            "        counts[a] += 1\n"
            "    return max(acts, key=lambda a: scores[a] / max(1, counts[a]))\n",
            lambda q: bool(
                re.search(
                    r"\bmcts\b|monte\s+carlo\s+tree\s+search|monte\s+carlo\s+search",
                    q,
                    re.I,
                )
            ),
            examples=(
                (
                    (
                        0,
                        lambda s: [s + 1, s - 1] if abs(s) < 5 else [],
                        lambda s: abs(s) >= 5,
                        lambda s: 1.0 if s >= 5 else 0.0,
                        32,
                        1,
                    ),
                    1,
                ),
            ),
        ),
        T(
            "natural_cubic_spline",
            "def natural_cubic_spline(xs, ys, xq):\n"
            '    """Natural cubic spline. Returns interpolated values at query points xq."""\n'
            "    n = len(xs)\n"
            "    if n < 2:\n"
            "        return [ys[0]] * len(xq) if n else []\n"
            "    h = [xs[i + 1] - xs[i] for i in range(n - 1)]\n"
            "    # second derivatives via tridiagonal (natural: M0 = Mn = 0)\n"
            "    alpha = [0.0] * n\n"
            "    for i in range(1, n - 1):\n"
            "        alpha[i] = (3.0 / h[i]) * (ys[i + 1] - ys[i]) - (3.0 / h[i - 1]) * (ys[i] - ys[i - 1])\n"
            "    l = [1.0] * n\n"
            "    mu = [0.0] * n\n"
            "    z = [0.0] * n\n"
            "    for i in range(1, n - 1):\n"
            "        l[i] = 2.0 * (xs[i + 1] - xs[i - 1]) - h[i - 1] * mu[i - 1]\n"
            "        mu[i] = h[i] / l[i]\n"
            "        z[i] = (alpha[i] - h[i - 1] * z[i - 1]) / l[i]\n"
            "    c = [0.0] * n\n"
            "    b = [0.0] * (n - 1)\n"
            "    d = [0.0] * (n - 1)\n"
            "    for j in range(n - 2, -1, -1):\n"
            "        c[j] = z[j] - mu[j] * c[j + 1]\n"
            "        b[j] = (ys[j + 1] - ys[j]) / h[j] - h[j] * (c[j + 1] + 2.0 * c[j]) / 3.0\n"
            "        d[j] = (c[j + 1] - c[j]) / (3.0 * h[j])\n"
            "    out = []\n"
            "    for x in xq:\n"
            "        i = 0\n"
            "        while i < n - 2 and x > xs[i + 1]:\n"
            "            i += 1\n"
            "        dx = x - xs[i]\n"
            "        y = ys[i] + b[i] * dx + c[i] * dx * dx + d[i] * dx * dx * dx\n"
            "        out.append(round(y, 8))\n"
            "    return out\n",
            lambda q: bool(re.search(r"cubic\s+spline|natural\s+cubic", q, re.I)),
            examples=(
                (([0, 1, 2], [0, 1, 0], [0, 1, 2]), [0.0, 1.0, 0.0]),
                (([0, 1], [2, 4], [0.5]), [3.0]),
            ),
        ),
        T(
            "pca_2d",
            "def pca_2d(points):\n"
            '    """Educational 2D PCA via power iteration on the covariance. Returns (mean, principal axis)."""\n'
            "    if not points:\n"
            "        return (0.0, 0.0), (1.0, 0.0)\n"
            "    n = float(len(points))\n"
            "    mx = sum(p[0] for p in points) / n\n"
            "    my = sum(p[1] for p in points) / n\n"
            "    cxx = cxy = cyy = 0.0\n"
            "    for x, y in points:\n"
            "        dx, dy = x - mx, y - my\n"
            "        cxx += dx * dx\n"
            "        cxy += dx * dy\n"
            "        cyy += dy * dy\n"
            "    cxx /= n\n"
            "    cxy /= n\n"
            "    cyy /= n\n"
            "    # power iteration\n"
            "    vx, vy = 1.0, 0.0\n"
            "    for _ in range(20):\n"
            "        wx = cxx * vx + cxy * vy\n"
            "        wy = cxy * vx + cyy * vy\n"
            "        norm = (wx * wx + wy * wy) ** 0.5 or 1.0\n"
            "        vx, vy = wx / norm, wy / norm\n"
            "    return (round(mx, 8), round(my, 8)), (round(vx, 8), round(vy, 8))\n",
            lambda q: bool(
                re.search(r"\bpca\b|principal\s+component", q, re.I)
                and not re.search(r"\bsvd\b|singular\s+value", q, re.I)
            ),
            examples=(
                (([(0, 0), (1, 0), (2, 0)],), ((1.0, 0.0), (1.0, 0.0))),
            ),
        ),
    ]
