"""Activation functions — none / sigmoid / relu change what one neuron can express."""

from __future__ import annotations

import math
from typing import Any, Callable, Dict, List


def none(z: float) -> float:
    return z


def sigmoid(z: float) -> float:
    if z >= 0:
        return 1.0 / (1.0 + math.exp(-z))
    e = math.exp(z)
    return e / (1.0 + e)


def relu(z: float) -> float:
    return max(0.0, z)


def neuron(x: List[float], w: List[float], b: float, act: Callable[[float], float]) -> float:
    z = w[0] * x[0] + w[1] * x[1] + b
    return act(z)


def run() -> Dict[str, Any]:
    w = [1.0, -1.0]
    b = 0.0
    xs = [[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]]
    table = {}
    for name, act in [("none", none), ("sigmoid", sigmoid), ("relu", relu)]:
        table[name] = [round(neuron(x, w, b, act), 4) for x in xs]
    return {
        "ok": table["relu"][0] == 0.0 and table["sigmoid"][0] == 0.5,
        "metric": f"relu[0]={table['relu'][0]} sigmoid[0]={table['sigmoid'][0]}",
        "table": table,
        "idea": "activation bends the weighted sum; ReLU zeros negatives",
    }


if __name__ == "__main__":
    print(run())
