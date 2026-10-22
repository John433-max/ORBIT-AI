"""Educational ML-from-scratch LabAgent for ORBIT."""
from __future__ import annotations
import re


class AgentResult:
    def __init__(self, agent: str, ok: bool, content: str, raw=None):
        self.agent, self.ok, self.content, self.raw = agent, ok, content, raw

    def to_dict(self):
        d = {"agent": self.agent, "ok": self.ok, "content": self.content}
        if self.raw is not None:
            d["raw"] = self.raw
        return d


def looks_like_lab(text: str) -> bool:
    low = (text or "").lower()
    return bool(
        re.search(
            r"\b(from scratch|ml from scratch|three neurons|one neuron|"
            r"run the (from scratch |ml )?lab|scratch lab|"
            r"gradient descent|overfitting|backpropagation|backprop|"
            r"activation functions?|next token|tiny language model|"
            r"xor demo|does ai think|"
            r"neural network|"
            r"(self[- ])?attention|"
            r"transformers?\b|"
            r"how (does|do) (a |an )?(neural|transformer)|"
            r"what is (a |an )?(neural network|transformer|self[- ]?attention)|"
            r"explain (a |an |the )?(neural network|transformer|attention))\b",
            low,
        )
    )


class LabAgent:
    """Educational ML-from-scratch curriculum (examples/ml_from_scratch)."""

    name = "lab_agent"

    def run(self, request: str, context=None):
        low = (request or "").lower()
        try:
            from examples.ml_from_scratch import DEMOS, summary
        except Exception as e:
            return AgentResult(self.name, False, f"scratch lab unavailable: {e}")

        want = None
        for key in DEMOS:
            if key.replace("_", " ") in low or key in low:
                want = key
                break
        if "xor" in low or "three neuron" in low:
            want = "three_neurons"
        if "one neuron" in low and "three" not in low:
            want = "one_neuron"
        if "gradient" in low:
            want = "gradient_descent"
        if "overfit" in low:
            want = "overfitting"
        if "backprop" in low:
            want = "backprop"
        if "activation" in low or "relu" in low or "sigmoid" in low:
            want = "activations"
        if (
            "next token" in low
            or "tiny llm" in low
            or "does ai think" in low
            or "tiny language model" in low
            or "tiny model" in low
        ):
            want = "next_token"
        # Conceptual NN / transformer / attention explainers → nearest educational demo
        if want is None and re.search(r"\bneural network\b", low):
            want = "three_neurons"
        if want is None and re.search(r"\btransformers?\b", low):
            want = "next_token"
        if want is None and re.search(r"\b(self[- ]?)?attention\b", low):
            want = "next_token"

        teach = {
            "one_neuron": (
                "A single sigmoid neuron learns a straight decision boundary. "
                "It can separate two clusters with a line — nothing more."
            ),
            "three_neurons": (
                "XOR cannot be solved by one line. Two hidden neurons + one output "
                "bend the decision surface so all four XOR cases work."
            ),
            "gradient_descent": (
                "Gradient descent walks downhill on the loss surface: measure how "
                "error changes with each weight, then step opposite that slope."
            ),
            "overfitting": (
                "A high-capacity model can nail training points and still fail on "
                "held-out points — low train error, higher test error."
            ),
            "activations": (
                "Activations bend the weighted sum: linear (none), smooth 0–1 "
                "(sigmoid), or zero-out negatives (ReLU)."
            ),
            "backprop": (
                "Backpropagation applies the chain rule so each weight gets a share "
                "of the output error — forward for predictions, backward for gradients."
            ),
            "next_token": (
                "The simplest language model is a next-token table: after each word, "
                "scores for what comes next are updated from training pairs."
            ),
        }
        try:
            if want and want in DEMOS:
                out = DEMOS[want]()
                lesson = teach.get(want, out.get("idea") or "")
                msg = f"{lesson} (demo `{want}`: {out.get('metric')})"
                return AgentResult(self.name, bool(out.get("ok")), msg, raw=out)
            s = summary()
            lines = [f"{k}: {v.get('metric')}" for k, v in (s.get("demos") or {}).items()]
            msg = "ML from scratch lab (" + str(s.get("n")) + " demos): " + "; ".join(lines)
            return AgentResult(self.name, bool(s.get("ok")), msg, raw=s)
        except Exception as e:
            return AgentResult(self.name, False, f"scratch lab failed: {e}")
