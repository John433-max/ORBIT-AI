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


    def matmul(self, other):
        """Explicit matmul (alias of @) for call-site compatibility."""
        return self @ other

    def mean(self, axis=None, keepdims=False):
        data = self.data.mean(axis=axis, keepdims=keepdims)
        out = Tensor(data, (self,))
        def _bw():
            g = out.grad
            if axis is None:
                self._accum(np.ones_like(self.data) * g / self.data.size)
            else:
                ax = axis if isinstance(axis, tuple) else (axis,)
                factor = 1.0
                for a in ax:
                    aa = a if a >= 0 else a + self.data.ndim
                    factor *= self.data.shape[aa]
                shape = list(self.data.shape)
                for a in sorted([a if a >= 0 else a + self.data.ndim for a in ax]):
                    if not keepdims:
                        shape[a] = 1
                g_b = np.reshape(g, shape) if not keepdims else g
                self._accum(np.ones_like(self.data) * g_b / factor)
        out._backward = _bw
        return out

    def pow(self, n):
        n = float(n)
        out = Tensor(np.power(self.data, n), (self,))
        def _bw():
            self._accum(n * np.power(self.data, n - 1.0) * out.grad)
        out._backward = _bw
        return out

    def sqrt(self):
        return self.pow(0.5)

    def reshape(self, *shape):
        if len(shape) == 1 and isinstance(shape[0], (tuple, list)):
            shape = tuple(shape[0])
        out = Tensor(self.data.reshape(shape), (self,))
        def _bw():
            self._accum(out.grad.reshape(self.data.shape))
        out._backward = _bw
        return out

    def softmax(self, axis=-1):
        x = self.data - self.data.max(axis=axis, keepdims=True)
        e = np.exp(x)
        s = e / e.sum(axis=axis, keepdims=True)
        out = Tensor(s, (self,))
        def _bw():
            g = out.grad
            sum_gs = (g * s).sum(axis=axis, keepdims=True)
            self._accum(s * (g - sum_gs))
        out._backward = _bw
        return out

    def silu(self):
        sig = 1.0 / (1.0 + np.exp(-self.data))
        y = self.data * sig
        out = Tensor(y, (self,))
        def _bw():
            self._accum((sig + self.data * sig * (1.0 - sig)) * out.grad)
        out._backward = _bw
        return out

    def __repr__(self):
        return f"Tensor(shape={self.data.shape}, requires_grad={self.requires_grad})"


def embedding_lookup(weight, indices):
    """Gather rows of weight by integer indices. Grad scatters back with add.at."""
    idx = np.asarray(indices, dtype=np.int64)
    out = Tensor(weight.data[idx], (weight,))
    def _bw():
        if weight.requires_grad:
            g = np.zeros_like(weight.data)
            np.add.at(g, idx, out.grad)
            weight._accum(g)
    out._backward = _bw
    return out


def cross_entropy(logits, targets):
    """Mean negative log-likelihood. logits (N,C), targets (N,) int."""
    x = logits.data
    t = np.asarray(targets, dtype=np.int64)
    x_shift = x - x.max(axis=-1, keepdims=True)
    logsumexp = np.log(np.exp(x_shift).sum(axis=-1, keepdims=True))
    log_probs = x_shift - logsumexp
    nll = -log_probs[np.arange(len(t)), t].mean()
    out = Tensor(np.array(nll), (logits,))
    def _bw():
        probs = np.exp(log_probs)
        grad = probs.copy()
        grad[np.arange(len(t)), t] -= 1.0
        grad /= max(len(t), 1)
        logits._accum(grad * float(out.grad))
    out._backward = _bw
    return out
