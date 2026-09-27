"""
Machine Learning From Scratch — educational demos for ORBIT.

These are tiny, dependency-free illustrations of core ideas
(one neuron, XOR network, gradient descent, overfitting,
activations, backprop, next-token prediction).

They are NOT production models. They exist so ORBIT can teach
and verify the same concepts its TinyLM lab builds on.

Run:
  python -m examples.ml_from_scratch
  python -m examples.ml_from_scratch one_neuron
"""

from __future__ import annotations

from typing import Any, Callable, Dict, List

from . import one_neuron
from . import three_neurons
from . import gradient_descent
from . import overfitting
from . import activations
from . import backprop
from . import next_token

DEMOS: Dict[str, Callable[[], Dict[str, Any]]] = {
    "one_neuron": one_neuron.run,
    "three_neurons": three_neurons.run,
    "gradient_descent": gradient_descent.run,
    "overfitting": overfitting.run,
    "activations": activations.run,
    "backprop": backprop.run,
    "next_token": next_token.run,
}


def run_all() -> List[Dict[str, Any]]:
    results = []
    for name, fn in DEMOS.items():
        out = fn()
        out["demo"] = name
        results.append(out)
    return results


def summary() -> Dict[str, Any]:
    rows = run_all()
    return {
        "ok": all(r.get("ok") for r in rows),
        "n": len(rows),
        "demos": {r["demo"]: {"ok": r.get("ok"), "metric": r.get("metric")} for r in rows},
    }
