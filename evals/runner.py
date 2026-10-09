"""Minimal evaluation runner — measure tool/agent behavior, not LLM hype."""

from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


def load_dataset(path: str) -> List[dict]:
    rows = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        rows.append(json.loads(line))
    return rows


def score_row(row: dict, answer: str) -> Dict[str, Any]:
    ans = answer or ""
    low = ans.lower()
    ok = True
    reasons = []
    for needle in row.get("expect_contains") or []:
        if needle.lower() not in low and needle not in ans:
            ok = False
            reasons.append(f"missing:{needle}")
    any_needles = list(row.get("expect_any") or [])
    if any_needles and not any(
        (n.lower() in low) or (n in ans) for n in any_needles
    ):
        ok = False
        reasons.append("missing_any:" + "|".join(any_needles))
    for needle in row.get("expect_not_contains") or []:
        if needle.lower() in low:
            ok = False
            reasons.append(f"forbidden:{needle}")
    return {"ok": ok, "reasons": reasons}


def run_eval(dataset_path: str = "evals/datasets/smoke.jsonl", out_dir: str = "evals/results") -> dict:
    from orbit_ai import OrbitAI

    rows = load_dataset(dataset_path)
    ai = OrbitAI(persist=False, load_model=False)
    results = []
    t0 = time.perf_counter()
    for row in rows:
        t1 = time.perf_counter()
        try:
            text = ai.ask(row["input"])
            err = None
        except Exception as e:
            text, err = "", str(e)
        scored = score_row(row, text)
        results.append(
            {
                "id": row.get("id"),
                "category": row.get("category"),
                "input": row["input"],
                "answer": (text or "")[:500],
                "error": err,
                "ok": scored["ok"] and not err,
                "reasons": scored["reasons"],
                "latency_ms": round((time.perf_counter() - t1) * 1000, 1),
            }
        )
    elapsed = time.perf_counter() - t0
    n_ok = sum(1 for r in results if r["ok"])
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "dataset": dataset_path,
        "n": len(results),
        "n_ok": n_ok,
        "accuracy": (n_ok / len(results)) if results else 0.0,
        "total_s": round(elapsed, 3),
        "by_category": {},
        "results": results,
    }
    by: Dict[str, List[bool]] = {}
    for r in results:
        by.setdefault(r.get("category") or "other", []).append(bool(r["ok"]))
    report["by_category"] = {
        k: {"n": len(v), "ok": sum(v), "accuracy": (sum(v) / len(v) if v else 0.0)} for k, v in by.items()
    }
    outp = Path(out_dir)
    outp.mkdir(parents=True, exist_ok=True)
    name = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M%S_eval.json")
    path = outp / name
    path.write_text(json.dumps(report, indent=2))
    # also write/update baseline pointer
    (outp / "latest.json").write_text(json.dumps(report, indent=2))
    report["path"] = str(path)
    return report


if __name__ == "__main__":
    print(json.dumps(run_eval(), indent=2))
