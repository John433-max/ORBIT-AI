"""Overfitting — polynomial fits train points but fails on held-out points."""

from __future__ import annotations

from typing import Any, Dict, List


def run(epochs: int = 500, lr: float = 0.3, k: int = 10) -> Dict[str, Any]:
    xs = [-0.9, -0.6, -0.4, -0.1, 0.1, 0.4, 0.6, 0.9]
    ys = [0.9, 0.6, 0.0, -0.1, 0.1, 0.4, 0.4, 0.6]
    hidden = [
        (-0.8, 0.6), (-0.5, 0.2), (-0.2, 0.1), (0.0, 0.0),
        (0.3, 0.1), (0.5, 0.2), (0.8, 0.6),
    ]
    w = [0.0] * k

    def pred(x: float) -> float:
        return sum(w[i] * (x ** i) for i in range(k))

    for _ in range(epochs):
        for x, y in zip(xs, ys):
            err = pred(x) - y
            for i in range(k):
                w[i] -= lr * err * (x ** i)

    train_mse = sum((pred(x) - y) ** 2 for x, y in zip(xs, ys)) / len(xs)
    test_mse = sum((pred(x) - y) ** 2 for x, y in hidden) / len(hidden)
    overfit = train_mse < 0.05 and test_mse > train_mse * 2
    return {
        "ok": True,
        "metric": f"train_mse={train_mse:.4f} test_mse={test_mse:.4f}",
        "train_mse": round(train_mse, 5),
        "test_mse": round(test_mse, 5),
        "overfit_gap": bool(overfit or test_mse > train_mse),
        "idea": "high-capacity fit on train can fail on hidden points",
    }


if __name__ == "__main__":
    print(run())
