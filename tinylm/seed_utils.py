"""Deterministic seeding helpers (Cycle 28)."""

from __future__ import annotations

import os
import random


def seed_everything(seed: int = 0) -> None:
    """Seed python, numpy, and torch RNGs."""
    seed = int(seed)
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    try:
        import numpy as np
        np.random.seed(seed)
    except Exception:
        pass
    try:
        import torch
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
    except Exception:
        pass
