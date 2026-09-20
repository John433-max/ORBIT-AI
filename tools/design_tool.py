"""HTML layout skeleton as a ToolRegistry tool (Cycle 61)."""

from __future__ import annotations

from html import escape

from tools.base import BaseTool, ToolResult


def layout_skeleton(request: str) -> dict:
    title = escape((request or "Untitled")[:60])
    html = (
        "<div class=\"card\">\n"
        f"  <h2>{title}</h2>\n"
        "  <p>Generated layout skeleton — placeholder content.</p>\n"
        "</div>"
    )
    return {
        "ok": True,
        "html": html,
        "title": title,
        "pretty": (
            "Generated a basic HTML layout skeleton "
            "(no visual-validation pass — see DESIGN.md Part 13)."
        ),
    }


class DesignLayoutTool(BaseTool):
    name = "design.layout"
    description = "Generate a minimal HTML card skeleton from a design request."
    permission_level = "SAFE"
    parameters = {
        "type": "object",
        "properties": {
            "request": {"type": "string", "description": "Design brief or page title"},
        },
        "required": ["request"],
    }
    timeout_s = 5.0

    def execute(self, request: str = "", **_):
        out = layout_skeleton(request or "")
        return ToolResult(ok=True, content=out["pretty"], data=out)
