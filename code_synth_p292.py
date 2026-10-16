"""Cycle 592: Adam, Nesterov, CG, Monte-Carlo integrate, Simpson, DE (1-D educational).

Pure-Python first-order / numerical methods with fixed seeds where stochastic.
"""
from __future__ import annotations

import math
import random
import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "adam_1d",
            "def adam_1d(f, df, x0, lr=0.1, beta1=0.9, beta2=0.999, steps=50, eps=1e-8):\n"
            "    import math\n"
            '    """Minimize f(x) with Adam (1-D educational).\n'
            "\n"
            "    Returns (x, f(x)) rounded to 5 decimals.\n"
            '    """\n'
            "    x = float(x0)\n"
            "    m = 0.0\n"
            "    v = 0.0\n"
            "    for t in range(1, steps + 1):\n"
            "        g = df(x)\n"
            "        m = beta1 * m + (1.0 - beta1) * g\n"
            "        v = beta2 * v + (1.0 - beta2) * g * g\n"
            "        mhat = m / (1.0 - beta1 ** t)\n"
            "        vhat = v / (1.0 - beta2 ** t)\n"
            "        x = x - lr * mhat / (math.sqrt(vhat) + eps)\n"
            "    return round(x, 5), round(f(x), 5)\n",
            lambda q: bool(re.search(r"\\badam\\b.{0,20}(optim|1d|1-d|minimize)|adam optimizer", q, re.I)),
            examples=(
                ((lambda x: (x - 2) ** 2, lambda x: 2 * (x - 2), 0.0), (2.07576, 0.00574)),
                ((lambda x: (x - 2) ** 2, lambda x: 2 * (x - 2), 5.0, 0.1, 0.9, 0.999, 100), (2.01934, 0.00037)),
            ),
        ),
        T(
            "nesterov_1d",
            "def nesterov_1d(f, df, x0, lr=0.1, beta=0.9, steps=50):\n"
            '    """Minimize f(x) with Nesterov accelerated gradient (1-D educational).\n'
            "\n"
            "    Look-ahead gradient. Returns (x, f(x)) rounded to 5 decimals.\n"
            '    """\n'
            "    x = float(x0)\n"
            "    v = 0.0\n"
            "    for _ in range(steps):\n"
            "        x_ahead = x + beta * v\n"
            "        g = df(x_ahead)\n"
            "        v = beta * v - lr * g\n"
            "        x = x + v\n"
            "    return round(x, 5), round(f(x), 5)\n",
            lambda q: bool(re.search(r"nesterov|nagh?b|accelerated\\s+gradient", q, re.I)),
            examples=(
                ((lambda x: (x - 2) ** 2, lambda x: 2 * (x - 2), 0.0), (2.00032, 0.0)),
                ((lambda x: (x - 2) ** 2, lambda x: 2 * (x - 2), 5.0, 0.1, 0.9, 80), (2.0, 0.0)),
            ),
        ),
        T(
            "conjugate_gradient_1d",
            "def conjugate_gradient_1d(f, df, x0, steps=20):\n"
            '    """Educational 1-D conjugate gradient (Fletcher-Reeves, fixed step).\n'
            "\n"
            "    Returns (x, f(x)) rounded to 5 decimals.\n"
            '    """\n'
            "    x = float(x0)\n"
            "    g = df(x)\n"
            "    d = -g\n"
            "    for _ in range(steps):\n"
            "        alpha = 0.5\n"
            "        x = x + alpha * d\n"
            "        g_new = df(x)\n"
            "        beta = (g_new * g_new) / (g * g + 1e-12)\n"
            "        d = -g_new + beta * d\n"
            "        g = g_new\n"
            "        if abs(g) < 1e-8:\n"
            "            break\n"
            "    return round(x, 5), round(f(x), 5)\n",
            lambda q: bool(
                re.search(r"conjugate\\s+gradient|fletcher[- ]reeves", q, re.I)
                and re.search(r"1[- ]?d|one[- ]d|scalar", q, re.I)
            ),
            examples=(
                ((lambda x: (x - 2) ** 2, lambda x: 2 * (x - 2), 0.0), (2.0, 0.0)),
                ((lambda x: (x - 2) ** 2, lambda x: 2 * (x - 2), 10.0, 30), (2.0, 0.0)),
            ),
        ),
        T(
            "monte_carlo_integrate_1d",
            "def monte_carlo_integrate_1d(f, a, b, n=10000, seed=0):\n"
            "    import random\n"
            '    """1-D Monte Carlo integration with fixed RNG seed.\n'
            "\n"
            "    Returns estimate rounded to 5 decimals.\n"
            '    """\n'
            "    rng = random.Random(seed)\n"
            "    s = 0.0\n"
            "    for _ in range(n):\n"
            "        x = rng.uniform(a, b)\n"
            "        s += f(x)\n"
            "    return round((b - a) * s / n, 5)\n",
            lambda q: bool(re.search(r"monte[- ]carlo.{0,16}integrat", q, re.I)),
            examples=(
                ((lambda x: x ** 2, 0.0, 1.0, 5000, 1), 0.33554),
                ((lambda x: x ** 2, 0.0, 1.0, 10000, 42), 0.33301),
            ),
        ),
        T(
            "simpson_integrate_1d",
            "def simpson_integrate_1d(f, a, b, n=100):\n"
            '    """Simpson rule 1-D integration (n forced even).\n'
            "\n"
            "    Returns integral rounded to 5 decimals.\n"
            '    """\n'
            "    if n % 2:\n"
            "        n += 1\n"
            "    h = (b - a) / n\n"
            "    s = f(a) + f(b)\n"
            "    for i in range(1, n):\n"
            "        x = a + i * h\n"
            "        s += 4.0 * f(x) if i % 2 else 2.0 * f(x)\n"
            "    return round(s * h / 3.0, 5)\n",
            lambda q: bool(re.search(r"simpson.{0,12}(rule|integrat)", q, re.I)),
            examples=(
                ((lambda x: x ** 2, 0.0, 1.0, 100), 0.33333),
                ((lambda x: x ** 2, 0.0, 1.0, 50), 0.33333),
            ),
        ),
        T(
            "differential_evolution_1d",
            "def differential_evolution_1d(f, bounds, pop=10, steps=30, seed=0, F=0.8, CR=0.9):\n"
            "    import random\n"
            '    """1-D differential evolution (educational, fixed seed).\n'
            "\n"
            "    Returns (best_x, best_f) rounded to 5 decimals.\n"
            '    """\n'
            "    rng = random.Random(seed)\n"
            "    lo, hi = bounds\n"
            "    pop_x = [rng.uniform(lo, hi) for _ in range(pop)]\n"
            "    pop_f = [f(x) for x in pop_x]\n"
            "    for _ in range(steps):\n"
            "        for i in range(pop):\n"
            "            idxs = list(range(pop))\n"
            "            idxs.remove(i)\n"
            "            a, b, c = rng.sample(idxs, 3)\n"
            "            mutant = pop_x[a] + F * (pop_x[b] - pop_x[c])\n"
            "            mutant = max(lo, min(hi, mutant))\n"
            "            trial = mutant if rng.random() < CR else pop_x[i]\n"
            "            ft = f(trial)\n"
            "            if ft < pop_f[i]:\n"
            "                pop_x[i], pop_f[i] = trial, ft\n"
            "    best_i = min(range(pop), key=lambda i: pop_f[i])\n"
            "    return round(pop_x[best_i], 5), round(pop_f[best_i], 5)\n",
            lambda q: bool(re.search(r"differential\\s+evolution|\\bde\\b.{0,12}optim", q, re.I)),
            examples=(
                ((lambda x: (x - 2) ** 2, (-5, 5), 10, 30, 1), (2.0, 0.0)),
                ((lambda x: (x - 2) ** 2, (0, 10), 8, 40, 42), (2.0, 0.0)),
            ),
        ),
    ]
