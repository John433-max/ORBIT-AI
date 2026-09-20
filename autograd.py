"""
Minimal reverse-mode autograd engine, NumPy-only.

Educational engine for TinyLM training without requiring a full PyTorch install.
"""
from __future__ import annotations

from typing import Callable, Optional, Tuple

import numpy as np


class Tensor:
    """Scalar/array with optional gradient tracking."""

    def __init__(self, data, parents: Tuple["Tensor", ...] = (), requires_grad: bool = True):
        self.data = np.asarray(data, dtype=np.float64)
        self.grad = np.zeros_like(self.data) if requires_grad else None
        self._parents = parents
        self._backward: Optional[Callable[[], None]] = None
        self.requires_grad = requires_grad and any(
            getattr(p, "requires_grad", False) for p in parents
        ) if parents else requires_grad

    def _accum(self, g):
        if self.grad is not None:
            self.grad = self.grad + g

    def backward(self):
        """Reverse-mode AD from this node."""
        order = []
        seen = set()

        def topo(v):
            if id(v) in seen:
                return
            seen.add(id(v))
            for p in v._parents:
                topo(p)
            order.append(v)

        topo(self)
        if self.grad is None:
            self.grad = np.ones_like(self.data)
        else:
            self.grad = np.ones_like(self.data)
        for v in reversed(order):
            if v._backward is not None:
                v._backward()

    def __add__(self, other):
        other = other if isinstance(other, Tensor) else Tensor(other, requires_grad=False)
        out = Tensor(self.data + other.data, (self, other))

        def _bw():
            if self.requires_grad:
                self._accum(out.grad)
            if other.requires_grad:
                other._accum(out.grad)

        out._backward = _bw
        return out

    def __mul__(self, other):
        other = other if isinstance(other, Tensor) else Tensor(other, requires_grad=False)
        out = Tensor(self.data * other.data, (self, other))

        def _bw():
            if self.requires_grad:
                self._accum(other.data * out.grad)
            if other.requires_grad:
                other._accum(self.data * out.grad)

        out._backward = _bw
        return out

    def __matmul__(self, other):
        other = other if isinstance(other, Tensor) else Tensor(other, requires_grad=False)
        out = Tensor(self.data @ other.data, (self, other))

        def _bw():
            if self.requires_grad:
                self._accum(out.grad @ other.data.T)
            if other.requires_grad:
                other._accum(self.data.T @ out.grad)

        out._backward = _bw
        return out

    def transpose(self, *axes):
        if not axes:
            axes = (1, 0)
        out = Tensor(self.data.transpose(axes), (self,))

        def _bw():
            self._accum(out.grad.transpose(axes))

        out._backward = _bw
        return out

    def relu(self):
        out = Tensor(np.maximum(0, self.data), (self,))

        def _bw():
            self._accum((self.data > 0).astype(np.float64) * out.grad)

        out._backward = _bw
        return out

    def sum(self):
        out = Tensor(np.array(self.data.sum()), (self,))

        def _bw():
            self._accum(np.ones_like(self.data) * out.grad)

        out._backward = _bw
        return out

    def __repr__(self):
        return f"Tensor(shape={self.data.shape}, requires_grad={self.requires_grad})"
