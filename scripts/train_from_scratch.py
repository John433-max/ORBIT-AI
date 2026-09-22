#!/usr/bin/env python3
"""From-scratch TinyLM training CLI.

Examples:
  python scripts/train_from_scratch.py --preset 1m --steps 40
  python scripts/train_from_scratch.py --preset 10m --steps 20
  python scripts/train_from_scratch.py --preset 100m --steps 5   # needs GPU/large RAM
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def main() -> int:
    p = argparse.ArgumentParser(description="ORBIT TinyLM from-scratch train")
    p.add_argument("--preset", default="1m", choices=["1m", "10m", "100m", "rope", "modern"])
    p.add_argument("--steps", type=int, default=40)
    p.add_argument("--batch", type=int, default=4)
    p.add_argument("--seq", type=int, default=64)
    p.add_argument("--lr", type=float, default=3e-3)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--ckpt", default=None)
    args = p.parse_args()

    from tinylm.train import train_from_scratch

    result = train_from_scratch(
        preset=args.preset,
        steps=args.steps,
        batch=args.batch,
        seq=args.seq,
        lr=args.lr,
        seed=args.seed,
        ckpt_path=args.ckpt,
    )
    out = {k: v for k, v in result.items() if k not in ("cfg", "model_np", "losses")}
    out["loss_curve_tail"] = (result.get("losses") or [])[-5:]
    print(json.dumps(out, indent=2, default=str))
    return 0 if result.get("ok", True) else 1


if __name__ == "__main__":
    raise SystemExit(main())
