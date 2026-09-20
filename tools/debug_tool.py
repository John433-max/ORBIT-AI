"""Rule-based traceback diagnosis as a ToolRegistry tool (Cycle 60)."""

from __future__ import annotations

from tools.base import BaseTool, ToolResult


class DebugDiagnoseTool(BaseTool):
    name = "debug.diagnose"
    description = "Diagnose a Python traceback or error message with a fixed lookup table."
    permission_level = "SAFE"
    parameters = {
        "type": "object",
        "properties": {
            "text": {"type": "string", "description": "Traceback or error text"},
        },
        "required": ["text"],
    }
    timeout_s = 5.0

    def execute(self, text: str = "", **_):
        from debugging import diagnose_traceback

        diagnosis = diagnose_traceback(text or "")
        if diagnosis.get("error_type") is None:
            return ToolResult(
                ok=False,
                content="I couldn't identify a specific Python error type in that text.",
                data=diagnosis,
            )
        lines = [f"Error type: {diagnosis['error_type']}", diagnosis.get("explanation") or ""]
        if diagnosis.get("likely_causes"):
            lines.append("Likely causes: " + "; ".join(diagnosis["likely_causes"]))
        if diagnosis.get("suggestions"):
            lines.append("Suggestions: " + "; ".join(diagnosis["suggestions"]))
        return ToolResult(ok=True, content="\n".join(lines), data=diagnosis)
