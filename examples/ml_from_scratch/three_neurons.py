"""Three neurons — XOR: the smallest network that solves what no line can."""

from __future__ import annotations

import math
from typing import Any, Dict, List, Tuple


def run(epochs: int = 3000, lr: float = 0.5) -> Dict[str, Any]:
    data: List[Tuple[float, float, float]] = [
        (0.0, 0.0, 0.0),
        (0.0, 1.0, 1.0),
        (1.0, 0.0, 1.0),
        (1.0, 1.0, 0.0),
    ]
    sig = lambda z: 1.0 / (1.0 + math.exp(-z))
    w = [0.3, -0.8, 0.5, -0.2, 0.9, 0.1, 0.7, -0.6, 0.2]

    for _ in range(epochs):
        for x0, x1, y in data:
            a = sig(w[0] * x0 + w[1] * x1 + w[2])
            b = sig(w[3] * x0 + w[4] * x1 + w[5])
            p = sig(w[6] * a + w[7] * b + w[8])
            err = p - y
            ga = err * w[6] * a * (1.0 - a)
            gb = err * w[7] * b * (1.0 - b)
            grad = [
                ga * x0, ga * x1, ga,
                gb * x0, gb * x1, gb,
                err * a, err * b, err,
            ]
            for i in range(9):
                w[i] -= lr * grad[i]

    correct = 0
    preds = []
    for x0, x1, y in data:
        a = sig(w[0] * x0 + w[1] * x1 + w[2])
        b = sig(w[3] * x0 + w[4] * x1 + w[5])
        p = sig(w[6] * a + w[7] * b + w[8])
        pred = 1 if p >= 0.5 else 0
        preds.append((x0, x1, pred, round(p, 3)))
        if pred == int(y):
            correct += 1

    return {
        "ok": correct == 4,
        "metric": f"{correct}/4 XOR correct",
        "preds": preds,
        "idea": "two hidden neurons + output: nonlinear boundary (XOR)",
    }


if __name__ == "__main__":
    print(run())
