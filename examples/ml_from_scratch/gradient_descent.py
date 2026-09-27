"""Gradient descent — walk downhill on the MSE loss surface for linear regression."""

from __future__ import annotations

from typing import Any, Dict, Tuple


def run(steps: int = 300, rate: float = 0.05) -> Dict[str, Any]:
    xs = [1.0, 2.0, 3.0, 4.0, 5.0]
    ys = [2.9, 5.2, 7.1, 8.8, 11.1]

    def loss(w: float, b: float) -> float:
        err = 0.0
        for x, y in zip(xs, ys):
            err += (w * x + b - y) ** 2
        return err / len(xs)

    def slope(w: float, b: float, h: float = 1e-6) -> Tuple[float, float]:
        dw = (loss(w + h, b) - loss(w, b)) / h
        db = (loss(w, b + h) - loss(w, b)) / h
        return dw, db

    w = b = 0.0
    for _ in range(steps):
        dw, db = slope(w, b)
        w -= rate * dw
        b -= rate * db

    final = loss(w, b)
    return {
        "ok": final < 0.1,
        "metric": f"loss={final:.4f} w={w:.2f} b={b:.2f}",
        "w": round(w, 3),
        "b": round(b, 3),
        "loss": round(final, 5),
        "idea": "numerical gradients step downhill until MSE is small",
    }


if __name__ == "__main__":
    print(run())
