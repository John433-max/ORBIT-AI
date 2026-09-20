"""Cycle 36: minimal CLI — train | generate | bench | card."""

from __future__ import annotations

import argparse
import json
import sys


def cmd_bench(args: argparse.Namespace) -> int:
    from .config import TinyLMConfig
    from .generate import bench_numpy, bench_torch
    from .numpy_model import TinyLMNumPy
    from .torch_model import TinyLMTorch

    cfg = TinyLMConfig.preset(
        args.preset,
        vocab_size=args.vocab,
        n_layer=args.layers,
        n_embd=args.embd,
        n_head=args.heads,
        block_size=args.block,
    )
    np_m = TinyLMNumPy.from_config(cfg, seed=0)
    t_m = TinyLMTorch.from_config(cfg)
    t_m.load_numpy_state(np_m)
    out = {
        "preset": args.preset,
        "numpy_cache_tok_s": bench_numpy(np_m, prompt_len=8, n_new=args.n_new, use_cache=True),
        "torch_cache_tok_s": bench_torch(t_m, prompt_len=8, n_new=args.n_new, use_cache=True),
        "params": sum(p.numel() for p in t_m.parameters()),
        "estimate_params": cfg.estimate_parameters(),
    }
    print(json.dumps(out, indent=2))
    return 0


def cmd_generate(args: argparse.Namespace) -> int:
    from .config import TinyLMConfig
    from .generate import generate_numpy
    from .numpy_model import TinyLMNumPy

    cfg = TinyLMConfig.preset(args.preset, vocab_size=args.vocab, n_layer=args.layers, n_embd=args.embd, n_head=args.heads, block_size=args.block)
    m = TinyLMNumPy.from_config(cfg, seed=args.seed)
    prompt = [int(x) for x in args.prompt.split(",")]
    idx = __import__("numpy").array([prompt], dtype=__import__("numpy").int64)
    out = generate_numpy(
        m,
        idx,
        args.n_new,
        temperature=args.temperature,
        top_k=args.top_k,
        top_p=args.top_p,
        repetition_penalty=args.rep_penalty,
        seed=args.seed,
    )
    print(json.dumps({"tokens": out[0].tolist()}))
    return 0


def cmd_train(args: argparse.Namespace) -> int:
    from .train import train_ablation

    r = train_ablation(
        qk_norm=args.qk_norm,
        steps=args.steps,
        lr=args.lr,
        seed=args.seed,
        grad_accum=args.grad_accum,
        use_cosine=True,
    )
    print(
        json.dumps(
            {
                "final_nll": r.final_nll,
                "final_ppl": r.final_ppl,
                "steps": r.steps,
                "last_loss": r.losses[-1] if r.losses else None,
            },
            indent=2,
        )
    )
    return 0


def cmd_card(args: argparse.Namespace) -> int:
    from .model_card import build_model_card

    card = build_model_card(args.preset, vocab=args.vocab, layers=args.layers, embd=args.embd, heads=args.heads, block=args.block)
    print(json.dumps(card, indent=2))
    if args.out:
        from pathlib import Path

        Path(args.out).write_text(json.dumps(card, indent=2))
    return 0


def cmd_kvreport(args: argparse.Namespace) -> int:
    from .kv_report import kv_cache_bytes_report

    print(json.dumps(kv_cache_bytes_report(args.preset, seq=args.seq, batch=args.batch, embd=args.embd, layers=args.layers, heads=args.heads), indent=2))
    return 0



def cmd_matrix(args):
    from .bench_matrix import run_matrix, write_results
    res = run_matrix(args.file)
    if args.out:
        write_results(res, args.out)
    import json
    print(json.dumps(res, indent=2))
    return 0


def cmd_regression(args):
    from .regression import run_regression
    import json
    r = run_regression()
    print(json.dumps(r, indent=2))
    return 0 if r["ok"] else 1

def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="python -m orbit.cli", description="ORBIT TinyLM CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    def add_model_args(sp):
        sp.add_argument("--preset", default="rope")
        sp.add_argument("--vocab", type=int, default=64)
        sp.add_argument("--layers", type=int, default=4)
        sp.add_argument("--embd", type=int, default=64)
        sp.add_argument("--heads", type=int, default=4)
        sp.add_argument("--block", type=int, default=64)

    b = sub.add_parser("bench")
    add_model_args(b)
    b.add_argument("--n-new", type=int, default=40)
    b.set_defaults(func=cmd_bench)

    g = sub.add_parser("generate")
    add_model_args(g)
    g.add_argument("--prompt", default="1,2,3,4")
    g.add_argument("--n-new", type=int, default=8)
    g.add_argument("--temperature", type=float, default=0.0)
    g.add_argument("--top-k", type=int, default=0)
    g.add_argument("--top-p", type=float, default=1.0)
    g.add_argument("--rep-penalty", type=float, default=1.0)
    g.add_argument("--seed", type=int, default=0)
    g.set_defaults(func=cmd_generate)

    t = sub.add_parser("train")
    t.add_argument("--steps", type=int, default=40)
    t.add_argument("--lr", type=float, default=2e-2)
    t.add_argument("--seed", type=int, default=0)
    t.add_argument("--qk-norm", action="store_true")
    t.add_argument("--grad-accum", type=int, default=1)
    t.set_defaults(func=cmd_train)

    c = sub.add_parser("card")
    add_model_args(c)
    c.add_argument("--out", default="")
    c.set_defaults(func=cmd_card)

    k = sub.add_parser("kv-report")
    add_model_args(k)
    k.add_argument("--seq", type=int, default=128)
    k.add_argument("--batch", type=int, default=1)
    k.set_defaults(func=cmd_kvreport)

    m = sub.add_parser("bench-matrix")
    m.add_argument("--file", default=None)
    m.add_argument("--out", default="")
    m.set_defaults(func=cmd_matrix)

    rg = sub.add_parser("regression")
    rg.set_defaults(func=cmd_regression)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
