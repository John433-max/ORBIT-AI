"""Cycle 591: 1D metaheuristics and adaptive optimizers.

Educational pure-Python templates for asks that previously returned None:
  - simulated annealing (1D discrete)
  - particle swarm (1D)
  - hill climbing (1D)
  - RMSprop (1D)
  - Adagrad (1D)
  - momentum gradient descent (1D)

Matchers are phrase-gated so they do not steal gradient_descent_1d or k_means.
"""
from __future__ import annotations

import re

from code_synth import Template

T = Template


def templates() -> list[Template]:
    return [
        T(
            "simulated_annealing_1d",
            "def simulated_annealing_1d(costs):\n"
            '    """Minimize a discrete 1D cost array with greedy-accept annealing.\n'
            "\n"
            "    Educational: always accept a better neighbor, reject worse.\n"
            "    Returns the index of the best cost found.\n"
            '    """\n'
            "    n = len(costs)\n"
            "    if n == 0:\n"
            "        return 0\n"
            "    best = cur = 0\n"
            "    for i in range(1, n):\n"
            "        if costs[i] <= costs[cur]:\n"
            "            cur = i\n"
            "        if costs[cur] < costs[best]:\n"
            "            best = cur\n"
            "    return best\n",
            lambda q: bool(
                re.search(
                    r"simulated\s+annealing|annealing\s+to\s+minimize",
                    q,
                    re.I,
                )
            ),
            examples=(
                (([5, 3, 4, 1, 2],), 3),
                (([2, 2, 2],), 0),
            ),
        ),
        T(
            "particle_swarm_1d",
            "def particle_swarm_1d(positions, scores):\n"
            '    """Pick the global best of a 1D particle swarm.\n'
            "\n"
            "    Educational stand-in: the swarm's best is the argmin of scores.\n"
            "    Returns the position of the best particle.\n"
            '    """\n'
            "    if not scores:\n"
            "        return 0.0\n"
            "    best = 0\n"
            "    for i in range(1, len(scores)):\n"
            "        if scores[i] < scores[best]:\n"
            "            best = i\n"
            "    return positions[best]\n",
            lambda q: bool(
                re.search(r"particle\s+swarm|pso\b", q, re.I)
            )
            and "k means" not in q.lower()
            and "k-means" not in q.lower(),
            examples=(
                (([0.0, 1.5, -0.5], [2.0, 0.4, 1.0]), 1.5),
                (([3.0], [1.0]), 3.0),
            ),
        ),
        T(
            "hill_climbing_1d",
            "def hill_climbing_1d(f, x0, step=1, limit=20):\n"
            '    """Discrete 1D hill climbing to minimize f.\n'
            "\n"
            "    From x0, move by +/- step while the neighbor is strictly better.\n"
            "    Returns the final x (integer when step is integer).\n"
            '    """\n'
            "    x = x0\n"
            "    for _ in range(limit):\n"
            "        cur = f(x)\n"
            "        left, right = x - step, x + step\n"
            "        fl, fr = f(left), f(right)\n"
            "        if fl < cur and fl <= fr:\n"
            "            x = left\n"
            "        elif fr < cur:\n"
            "            x = right\n"
            "        else:\n"
            "            break\n"
            "    return x\n",
            lambda q: bool(
                re.search(r"hill[\s_-]?climbing", q, re.I)
            ),
            examples=(
                ((lambda x: (x - 3) ** 2, 0), 3),
                ((lambda x: abs(x + 1), 4), -1),
            ),
        ),
        T(
            "rmsprop_1d",
            "def rmsprop_1d(grads, lr=0.1, rho=0.9, eps=1e-8):\n"
            '    """RMSprop parameter update on a 1D scalar starting at 0.\n'
            "\n"
            "    acc <- rho*acc + (1-rho)*g^2\n"
            "    x   <- x - lr * g / (sqrt(acc)+eps)\n"
            "    Returns the final x rounded to 6 decimals.\n"
            '    """\n'
            "    x = 0.0\n"
            "    acc = 0.0\n"
            "    for g in grads:\n"
            "        acc = rho * acc + (1.0 - rho) * (g * g)\n"
            "        x = x - lr * g / ((acc ** 0.5) + eps)\n"
            "    return round(x, 6)\n",
            lambda q: bool(
                re.search(r"\brmsprop\b", q, re.I)
            )
            and "step" not in q.lower(),
            examples=(
                (([1.0, 1.0],), -0.545643),
                (([0.0],), 0.0),
            ),
        ),
        T(
            "adagrad_1d",
            "def adagrad_1d(grads, lr=0.1, eps=1e-8):\n"
            '    """Adagrad parameter update on a 1D scalar starting at 0.\n'
            "\n"
            "    acc <- acc + g^2\n"
            "    x   <- x - lr * g / (sqrt(acc)+eps)\n"
            "    Returns the final x rounded to 6 decimals.\n"
            '    """\n'
            "    x = 0.0\n"
            "    acc = 0.0\n"
            "    for g in grads:\n"
            "        acc = acc + g * g\n"
            "        x = x - lr * g / ((acc ** 0.5) + eps)\n"
            "    return round(x, 6)\n",
            lambda q: bool(
                re.search(r"\badagrad\b", q, re.I)
            )
            and "step" not in q.lower(),
            examples=(
                (([1.0, 1.0],), -0.170711),
                (([2.0],), -0.1),
            ),
        ),
        T(
            "momentum_gd_1d",
            "def momentum_gd_1d(grads, lr=0.1, mu=0.9):\n"
            '    """Momentum gradient descent on a 1D scalar starting at 0.\n'
            "\n"
            "    v <- mu*v + g\n"
            "    x <- x - lr*v\n"
            "    Returns the final x rounded to 6 decimals.\n"
            '    """\n'
            "    x = 0.0\n"
            "    v = 0.0\n"
            "    for g in grads:\n"
            "        v = mu * v + g\n"
            "        x = x - lr * v\n"
            "    return round(x, 6)\n",
            lambda q: bool(
                re.search(r"momentum\s+gradient\s+descent|momentum\s+gd\b", q, re.I)
            ),
            examples=(
                (([1.0, 1.0],), -0.29),
                (([0.0, 0.0],), 0.0),
            ),
        ),
    ]
