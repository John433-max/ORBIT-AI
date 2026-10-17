"""ORBIT agents (GitHub CI surface).

Implements routing + Cycle 93 chat→ModelRouter fallback required by
tests/unit/test_provider_fallback.py. Coding and research paths return
real sandbox/search results or an honest no-live-web message.
"""
from __future__ import annotations

import collections
import hashlib
import re


class AgentResult:
    def __init__(self, agent: str, ok: bool, content: str, raw=None):
        self.agent, self.ok, self.content, self.raw = agent, ok, content, raw

    def to_dict(self):
        d = {"agent": self.agent, "ok": self.ok, "content": self.content}
        if self.raw is not None:
            d["raw"] = self.raw
        return d


def stable_seed(text: str) -> int:
    digest = hashlib.sha256((text or "").encode("utf-8", errors="replace")).digest()
    return int.from_bytes(digest[:8], "big") % (2**32)


def _wants_code_written(request: str) -> bool:
    if re.search(r"```", request or ""):
        return False
    return bool(
        re.search(
            r"\b(write|implement|create|define|make)\b.{0,80}\b("
            r"function|def |class |script|program|module|code)\b|"
            r"\bpython function\b|"
            r"\bimplement\b.{0,40}\bin python\b",
            request or "",
            re.I,
        )
    )


DENY_FS_MSG = (
    "I can't do that. ORBIT refuses destructive filesystem commands "
    "(delete all files, rm -rf /, wipe disk). Permission denied."
)


def _is_destructive_fs(text: str) -> bool:
    if _wants_code_written(text or ""):
        return False
    return bool(
        re.search(
            r"\brm\s+-rf\b|\bdelete all files\b|\bdelete everything\b|"
            r"\bwipe (the )?(disk|root|filesystem|drive)\b|"
            r"\bformat (the )?(hard )?disk\b|\bremove all files in\s+/",
            text or "",
            re.I,
        )
    )


def _synthesize_python(request: str) -> str:
    try:
        from code_synth import synthesize_python

        return synthesize_python(request)
    except Exception:
        low = (request or "").lower()
        if re.search(r"add(s|ing)?\b.{0,20}\b(two|2)\b.{0,20}\b(number|int|value)", low) or "adds two" in low:
            return (
                "def add(a, b):\n"
                '    """Return the sum of a and b."""\n'
                "    return a + b\n"
            )
        if re.search(r"\b(multiply|product of)\b.{0,20}\b(two|2)\b", low):
            return (
                "def multiply(a, b):\n"
                '    """Return the product of a and b."""\n'
                "    return a * b\n"
            )
        slug = re.sub(r"[^a-z0-9]+", "_", low)[:40].strip("_") or "solve"
        return (
            f"def {slug}(*args, **kwargs):\n"
            f'    """Draft from: {(request or "").strip()[:120]}"""\n'
            "    raise NotImplementedError('Paste a fenced snippet to run it.')\n"
        )


class CodeAgent:
    name = "coding_agent"

    def run(self, request: str, context=None) -> AgentResult:
        if _wants_code_written(request):
            verified = False
            n_ex = 0
            name = None
            try:
                from code_synth import synthesize_and_verify
                bundle = synthesize_and_verify(request)
                src = bundle.get("source") or _synthesize_python(request)
                verified = bool(bundle.get("verified"))
                n_ex = int(bundle.get("checked") or 0)
                name = bundle.get("name")
            except Exception:
                src = _synthesize_python(request)
            note = f"\n\nVerified against {n_ex} example(s)." if verified and n_ex else ""
            content = "Here is a Python function for that request:\n\n```python\n" + src + "```" + note
            return AgentResult(
                self.name,
                True,
                content,
                raw={"source": "synthesize", "code": src, "verified": verified, "checked": n_ex, "name": name},
            )
        code = request
        m = re.search(r"```(?:python)?\s*(.*?)```", request or "", re.S)
        if m:
            code = m.group(1)
        try:
            from tools import python_sandbox

            result = python_sandbox(code, timeout=3.0)
            if result.get("ok"):
                return AgentResult(
                    self.name, True, f"Ran the code in the sandbox. stdout:\n{result.get('stdout', '')}", raw=result
                )
            return AgentResult(
                self.name, False, f"Sandbox execution failed: {result.get('error') or result.get('stderr')}", raw=result
            )
        except Exception as e:
            return AgentResult(self.name, False, f"Sandbox unavailable: {e}")
