"""
Calculator tool (Phase 16). Deliberately NOT `eval()`-based — arithmetic
expressions are parsed with `ast.parse` and walked by hand, allowing only a
fixed whitelist of numeric operations. This is the same security posture as
tools.py's python_sandbox (no bare eval/exec on user input), just applied to
a narrower, purpose-built evaluator instead of general Python.
"""
import ast
import math
import operator
import re
import statistics


class CalculatorError(ValueError):
    pass


_BIN_OPS = {
    ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
    ast.Div: operator.truediv, ast.Pow: operator.pow, ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv,
}
_UNARY_OPS = {ast.UAdd: operator.pos, ast.USub: operator.neg}
_FUNCS = {
    "sqrt": math.sqrt, "abs": abs, "round": round,
    "log": math.log, "log10": math.log10, "log2": math.log2,
    "sin": math.sin, "cos": math.cos, "tan": math.tan,
    "mean": statistics.mean, "median": statistics.median,
    "stdev": lambda xs: statistics.stdev(xs) if len(xs) > 1 else 0.0,
    "variance": lambda xs: statistics.variance(xs) if len(xs) > 1 else 0.0,
    "min": min, "max": max, "sum": sum,
}
_CONSTANTS = {"pi": math.pi, "e": math.e}
_MAX_EXPR_LEN = 500


def _eval_node(node):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise CalculatorError(f"unsupported constant: {node.value!r}")
    if isinstance(node, ast.BinOp):
        op_fn = _BIN_OPS.get(type(node.op))
        if op_fn is None:
            raise CalculatorError(f"unsupported operator: {type(node.op).__name__}")
        left, right = _eval_node(node.left), _eval_node(node.right)
        if isinstance(node.op, (ast.Div, ast.FloorDiv, ast.Mod)) and right == 0:
            raise CalculatorError("division by zero")
        return op_fn(left, right)
    if isinstance(node, ast.UnaryOp):
        op_fn = _UNARY_OPS.get(type(node.op))
        if op_fn is None:
            raise CalculatorError(f"unsupported unary operator: {type(node.op).__name__}")
        return op_fn(_eval_node(node.operand))
    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name) or node.func.id not in _FUNCS:
            raise CalculatorError(f"unsupported function call")
        args = []
        for a in node.args:
            if isinstance(a, ast.List):
                args.append([_eval_node(e) for e in a.elts])
            else:
                args.append(_eval_node(a))
        try:
            return _FUNCS[node.func.id](*args)
        except (ValueError, ZeroDivisionError, statistics.StatisticsError) as e:
            raise CalculatorError(str(e))
    if isinstance(node, ast.Name):
        if node.id in _CONSTANTS:
            return _CONSTANTS[node.id]
        raise CalculatorError(f"unknown identifier: {node.id!r}")
    if isinstance(node, ast.List):
        return [_eval_node(e) for e in node.elts]
    raise CalculatorError(f"unsupported expression element: {type(node).__name__}")


def calculate(expression: str) -> dict:
    if not expression or not expression.strip():
        return {"ok": False, "error": "empty expression"}
    if len(expression) > _MAX_EXPR_LEN:
        return {"ok": False, "error": f"expression too long (max {_MAX_EXPR_LEN} chars)"}
    try:
        tree = ast.parse(expression, mode="eval")
        result = _eval_node(tree.body)
        return {"ok": True, "result": result, "expression": expression}
    except SyntaxError:
        return {"ok": False, "error": "could not parse as a math expression"}
    except CalculatorError as e:
        return {"ok": False, "error": str(e)}
    except (OverflowError, RecursionError) as e:
        return {"ok": False, "error": f"expression too large to evaluate: {e}"}


_PERCENT_OF_RE = re.compile(
    r"what\s+is\s+([\d.]+)\s*%\s+of\s+([\d.]+)|([\d.]+)\s*%\s+of\s+([\d.]+)", re.IGNORECASE)
_MATH_DETECT_RE = re.compile(r"[\d].*[\+\-\*/\^%]|sqrt|square root|percent|average|mean|median")


def looks_like_math(text: str) -> bool:
    return bool(_MATH_DETECT_RE.search(text.lower()))


def calculate_percentage_of(percent: float, value: float) -> float:
    return (percent / 100.0) * value


def _normalize_math_words(text: str) -> str:
    s = text
    replacements = [
        (r"\bdivided\s+by\b", " / "),
        (r"\bdivide\s+by\b", " / "),
        (r"\bdivides\b", " / "),
        (r"\bdivide\b", " / "),
        (r"\bmultiplied\s+by\b", " * "),
        (r"\btimes\b", " * "),
        (r"\bmultiply\s+by\b", " * "),
        (r"\bmultiply\b", " * "),
        (r"\bplus\b", " + "),
        (r"\bminus\b", " - "),
        (r"\bmodulo\b", " % "),
        (r"\bmod\b", " % "),
        (r"\bto the power of\b", " ** "),
        (r"×", "*"),
        (r"÷", "/"),
        (r"\bx\b", " * "),
    ]
    for pat, rep in replacements:
        s = re.sub(pat, rep, s, flags=re.I)
    m = re.search(r"\bsubtract\s+(-?\d+(?:\.\d+)?)\s+from\s+(-?\d+(?:\.\d+)?)", s, re.I)
    if m:
        s = f"{m.group(2)} - {m.group(1)}"
    return s


def parse_and_calculate(text: str) -> dict:
    m = _PERCENT_OF_RE.search(text)
    if m:
        groups = [g for g in m.groups() if g is not None]
        if len(groups) == 2:
            percent, value = float(groups[0]), float(groups[1])
            return {"ok": True, "result": calculate_percentage_of(percent, value),
                    "expression": f"{percent}% of {value}"}
    normalized = _normalize_math_words(text)
    candidates = re.findall(r"[\d\.\s\+\-\*/\(\)%\^]+", normalized)
    candidates = [c.strip() for c in candidates if any(ch.isdigit() for ch in c)]
    if not candidates:
        return {"ok": False, "error": "no arithmetic expression found in text"}
    expr = max(candidates, key=len).replace("^", "**")
    expr = re.sub(r"\s+", " ", expr).strip()
    out = calculate(expr)
    if out.get("ok"):
        out = dict(out, expression=expr)
    return out
