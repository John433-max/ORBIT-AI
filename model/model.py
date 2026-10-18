"""Product model entry point.

`model/__init__.py` exports TinyLM from here. The educational NumPy
implementation lives in `tinylm.numpy_model.TinyLMNumPy`. This module
re-exports it under the product name so `from model import TinyLM`
succeeds for doctor, presets, and legacy scripts.

If the educational backend cannot be imported, a thin stub is provided
so the package import itself does not fail; calling the stub raises.
"""

from __future__ import annotations

try:
    from tinylm.numpy_model import TinyLMNumPy as TinyLM  # noqa: F401
except Exception as _exc:  # pragma: no cover
    _BACKEND_ERROR = _exc

    class TinyLM:  # type: ignore[no-redef]
        """Placeholder when the educational TinyLM backend is unavailable."""

        def __init__(self, *args, **kwargs):
            raise RuntimeError(
                f"TinyLM backend unavailable: {_BACKEND_ERROR}"
            ) from _BACKEND_ERROR

        def __repr__(self) -> str:
            return f"<TinyLM unavailable: {_BACKEND_ERROR}>"


__all__ = ["TinyLM"]
