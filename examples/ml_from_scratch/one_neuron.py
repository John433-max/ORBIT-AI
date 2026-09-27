"""One neuron — learns a line that separates two groups (logistic regression)."""

from __future__ import annotations

import math
from typing import Any, Dict, List, Tuple


def run(epochs: int = 200, lr: float = 0.1) -> Dict[str, Any]:
    xs: List[List[float]] = [
        [1, 2], [2, 1], [2, 3], [3, 2],
        [6, 7], [7, 6], [7, 8], [8, 7],
    ]
    ys = [0, 0, 0, 0, 1, 1, 1, 1]
    w1 = w2 = b = 0.0

    for _ in range(epochs):
        for (x0, x1), y in zip(xs, ys):
            z = w1 * x0 + w2 * x1 + b
            p = 1.0 / (1.0 + math.exp(-z))
            err = p - y
            w1 -= lr * err * x0
            w2 -= lr * err * x1
            b -= lr * err

    correct = 0
    preds = []
    for (x0, x1), y in zip(xs, ys):
        z = w1 * x0 + w2 * x1 + b
        p = 1.0 / (1.0 + math.exp(-z))
        pred = 1 if p >= 0.5 else 0
        preds.append(pred)
        if pred == y:
            correct += 1

    return {
        "ok": correct == len(ys),
        "metric": f"{correct}/{len(ys)} correct",
        "weights": (round(w1, 4), round(w2, 4), round(b, 4)),
        "preds": preds,
        "idea": "one sigmoid neuron learns a linear decision boundary",
    }


if __name__ == "__main__":
    print(run())
