"""Backpropagation — error runs backward through every weight (2-layer net)."""

from __future__ import annotations

import math
from typing import Any, Dict, List


def run() -> Dict[str, Any]:
    x = [1.0, 0.5]
    y = 1.0
    W1 = [[0.5, -0.4], [0.8, 0.3]]  # layer one (2 hidden)
    W2 = [0.9, 0.46]  # layer two

    def sig(z: float) -> float:
        return 1.0 / (1.0 + math.exp(-z))

    # forward
    h = [
        sig(W1[j][0] * x[0] + W1[j][1] * x[1])
        for j in range(2)
    ]
    o = sig(W2[0] * h[0] + W2[1] * h[1])
    loss = (o - y) ** 2

    # backward
    d_o = 2.0 * (o - y) * o * (1.0 - o)
    d_h = [d_o * W2[j] * h[j] * (1.0 - h[j]) for j in range(2)]
    gW2 = [d_o * h[j] for j in range(2)]
    gW1 = [[d_h[j] * x[i] for i in range(2)] for j in range(2)]

    return {
        "ok": loss >= 0.0 and abs(sum(gW2)) > 0,
        "metric": f"o={o:.3f} loss={loss:.3f}",
        "output": round(o, 4),
        "loss": round(loss, 4),
        "gW2": [round(g, 5) for g in gW2],
        "idea": "chain rule: d_loss/d_w from output back through hidden units",
    }


if __name__ == "__main__":
    print(run())
