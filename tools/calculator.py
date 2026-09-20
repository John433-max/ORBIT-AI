"""Calculator tool — wraps the existing calculator.py."""

from __future__ import annotations

from tools.base import BaseTool, ToolResult


class CalculatorTool(BaseTool):
    name = "calculator"
    description = (
        'Evaluate a math expression safely (no eval). '
        'Use for arithmetic, e.g. expression="(2+3)*4". '
        'Returns the numeric result as text.'
    )
    permission_level = "SAFE"
    parameters = {
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "Arithmetic expression, e.g. '2 + 3 * (4 - 1)'",
            }
        },
        "required": ["expression"],
    }
    timeout_s = 5.0

    def execute(self, expression: str = "", **_) -> ToolResult:
        from calculator import parse_and_calculate
        expr = (expression or "").strip()
        if not expr:
            return ToolResult(ok=False, content="", error="expression is empty")
        try:
            from science_math import solve_science_math
            sci = solve_science_math(expr)
            if isinstance(sci, dict) and sci.get("ok"):
                msg = sci.get("pretty") or f"{sci.get('kind')}: {sci.get('result')}"
                return ToolResult(ok=True, content=str(msg), data=sci)
        except Exception:
            pass
        if not any(c.isdigit() for c in expr):
            return ToolResult(ok=False, content="", error="expression must contain a number")
        try:
            value = parse_and_calculate(expr)
            if isinstance(value, dict):
                if not value.get("ok", True):
                    return ToolResult(
                        ok=False, content="",
                        error=str(value.get("error") or value), data=value,
                    )
                result = value.get("result", value)
                return ToolResult(ok=True, content=str(result), data=value)
            return ToolResult(ok=True, content=str(value), data=value)
        except Exception as e:
            return ToolResult(ok=False, content="", error=str(e))
