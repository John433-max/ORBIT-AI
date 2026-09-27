"""Next-token toy — bigram table learns local word transitions (tiny LM idea)."""

from __future__ import annotations

import math
import random
from typing import Any, Dict, List


def run(seed: int = 1, rounds: int = 500) -> Dict[str, Any]:
    words = "the bird sat on the mat the cat sat on the mat".split()
    vocab = sorted(set(words))
    index = {w: i for i, w in enumerate(vocab)}
    n = len(vocab)
    W = [[0.0] * n for _ in range(n)]

    def chances(a: str) -> List[float]:
        ia = index[a]
        scores = W[ia]
        m = max(scores)
        e = [math.exp(s - m) for s in scores]
        s = sum(e) or 1.0
        return [v / s for v in e]

    pairs = list(zip(words, words[1:]))
    for _ in range(rounds):
        for a, b in pairs:
            P = chances(a)
            ia, ib = index[a], index[b]
            for c in range(n):
                target = 1.0 if c == ib else 0.0
                W[ia][c] -= 0.1 * (P[c] - target)

    random.seed(seed)
    out = ["the"]
    for _ in range(8):
        P = chances(out[-1])
        r = random.random()
        cum = 0.0
        chosen = vocab[0]
        for w, p in zip(vocab, P):
            cum += p
            if r <= cum:
                chosen = w
                break
        out.append(chosen)

    text = " ".join(out)
    p_the = chances("the")
    top = sorted(zip(vocab, p_the), key=lambda t: -t[1])[:3]
    ok = top[0][1] > 0.2
    return {
        "ok": ok,
        "metric": f"top_after_the={top[0][0]}@{top[0][1]:.2f}",
        "sample": text,
        "top_after_the": [(w, round(p, 3)) for w, p in top],
        "idea": "next-token table is the simplest language model",
    }


if __name__ == "__main__":
    print(run())
