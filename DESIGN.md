# Historical design notes — large-model research vision (NOT current product identity)

> **Status:** HISTORICAL / RESEARCH. This document captures early design thinking
> about large-scale training. **ORBIT AI today is a modular local AI agent runtime**
> (agents, tools, RAG, memory, ModelProvider backends). It is **not** a 100B model
> and does not claim those capabilities. Parameter counts below are design targets
> for a possible future training run, not shipping software.

**Historical project label:** ORBIT-100B (obsolete — do not use in product docs)

## 0. What this document is and isn't

This is a design document plus a real, tested, small prototype (see
`autograd.py`, `model.py`, `tokenizer.py`, `train.py`, `generate.py`,
`test_autograd.py` in this folder — every gradient in the autograd engine is
checked numerically, and the training loop is run end-to-end and shown to
reduce loss and checkpoint/reload correctly).

It is **not**: a completed 100B model, a verified cost estimate backed by
current GPU market prices, a peer-reviewed research paper, or a claim that
the recursive-reasoning idea in Part 7 is proven to help at scale. Where a
number below is arithmetic (parameter counts, memory, FLOPs) it is exact —
you can re-derive it from the stated shapes. Where it's a design
recommendation, it's marked **established** (widely used in shipped
open-weight models, e.g. Llama/Mistral/DeepSeek/Qwen-style architectures),
**experimental** (published, smaller-scale evidence, not proven at 100B),
or **proposed** (this document's synthesis, unvalidated).

---

## 1. Architecture research summary

| Technique | What it does | Established practice | Decision |
|---|---|---|---|
| Decoder-only Transformer | Causal self-attention + MLP stack | Universal choice for general-purpose chat/reasoning/code models | **Adopt** |
| GQA (grouped-query attention) | Multiple Q heads share a smaller set of K/V heads | Shrinks KV-cache memory ~4-8x vs full MHA for small quality cost; used in Llama 2 70B onward, Mistral, most current open models | **Adopt** over full MHA (memory-bound at long context) and over MQA (1 KV head — quality loss is larger, GQA is the accepted middle ground) |
| RoPE (rotary position embeddings) | Encodes relative position via rotation of Q/K in each pair of dims | Standard since GPT-NeoX/Llama; extrapolates better than learned absolute positions, no extra params | **Adopt**, with a documented context-extension method (see below) rather than assuming raw extrapolation past training length |
| RMSNorm | Normalizes by root-mean-square, no mean-centering/bias | Standard in Llama/Mistral/Qwen-family models; cheaper than LayerNorm, comparable quality | **Adopt** |
| SwiGLU MLP | Gated SiLU MLP: `(SiLU(xW1) * xW2) W3` | Outperforms plain GELU MLP at matched compute in the original GLU-variants paper's ablations, replicated across many later model reports | **Adopt** |
| KV cache | Reuse cached K/V per generated token instead of recomputing | Standard for autoregressive decoding; dominant inference memory cost at long context | **Required infrastructure**, sized explicitly in Part 3 |
| FlashAttention-style fused kernels | Fuses attention into a single memory-efficient kernel | Standard in production training/inference stacks; not an architecture choice, an implementation choice | **Adopt at implementation time** (this repo's toy prototype uses plain NumPy matmuls — fine at 100k params, would need a real fused kernel library like the FlashAttention CUDA kernels or a framework that ships them at real scale) |
| Speculative decoding | Small draft model proposes tokens, large model verifies in parallel | Real inference-speed win (roughly 2-3x in published reports), no accuracy cost when done correctly | **Adopt at serving time**, orthogonal to training |
| MoE (mixture-of-experts) | Route each token to a subset of expert MLPs | Total-params-vs-active-params decoupling; used in Mixtral, DeepSeek-MoE, Qwen-MoE, and others at production scale | **Adopt as the primary ~100B candidate** — see Part 3 for why |
| Tensor / pipeline / sequence / data parallelism, FSDP, DeepSpeed, Megatron-style sharding | Ways to split model+data across many GPUs | Established, necessary at this scale; no single one suffices alone above roughly 7-13B dense | **Required**, combined (see Part 6) |

**Rejected / not adopted for this design:** absolute learned positional embeddings (worse extrapolation than RoPE, no offsetting benefit); ALiBi (reasonable alternative to RoPE, but RoPE has broader current tooling/ecosystem support so it's the safer default); full multi-head attention without GQA (memory cost not justified at 100B+context targets in Part 3).

---

## 2. Recursive latent reasoning (x/y/z) — analysis

The diagram you provided is a compressed description of the pattern used in
recent **small-model** recursive-reasoning work (a shared-weight network
iterated over a latent state, trained with deep supervision across outer
steps — the "Tiny Recursion Model" line of work you referenced). Answering
your 13 questions directly, as design decisions rather than claims of
proven results:

1. **z's representation space:** hidden-state space (width = `d_model`), not
   token space and not a separate exotic latent. Token space would force a
   detour through the vocabulary projection every recursive step, which is
   expensive and throws away continuous information between steps.
2. **What y represents:** the transformer's own residual-stream hidden
   state (post-attention/MLP), not a separate embedding table. This lets the
   recursion module reuse everything the base transformer already computed
   instead of re-deriving it.
3. **Combining x + y + z:** the prototype concatenates and passes through a
   shared linear+SwiGLU-ish update (`concat3` in `model.py`). Cross-attention
   between x/y/z is a plausible alternative worth an ablation (Part 24) but
   adds real compute for an unproven gain — concatenation is the cheaper
   default and was the toy-scale choice made here.
4. **Shared weights:** yes, unambiguously. An unshared per-step network is
   just extra depth with a misleading name — it loses the property (a fixed
   computational unit refining a state) that makes "recursion" meaningfully
   different from "more layers." `ReasoningBlock` in `model.py` reuses one
   `Wz`/`Wy` across every step.
5. **Recursion granularity:** at the reasoning-module level, applied once
   per forward pass over the whole sequence's pooled/positional hidden
   state — not per token, not per layer. Per-token recursion multiplies
   compute by `N_sup` for every position, which is prohibitive at 100B
   scale without evidence it's needed; per-layer recursion conflates
   "more layers" with "iterative refinement" and reintroduces problem 4.
6. **Is `N_sup = 16` right:** no fixed number is "right" without an
   ablation on your actual task mix. 16 is a reasonable starting search
   point (matches published small-model recursive-reasoning setups), but it
   trades wall-clock/compute linearly, and Part 24 requires measuring it,
   not assuming it.
7. **Adaptive computation instead of fixed steps:** yes, recommended as
   Architecture C's addition — a learned halting head is strictly more
   flexible than a fixed `N_sup`, at the cost of extra training complexity
   (the halting loss needs its own tuning, see item 9 below) and non-uniform
   latency, which matters for a chat product.
8. **Preventing instability:** RMSNorm inside the recursive update (not just
   at the transformer's own layers — see `norm_z`/`norm_y` in
   `ReasoningBlock`), a residual/gated update for `y` rather than full
   replacement each step, and gradient clipping across the whole unrolled
   recursion during training.
9. **Gradient flow:** full backpropagation-through-time across all `N_sup`
   steps if `N_sup` is small (this prototype does this — `backward()` walks
   the entire unrolled graph). At real `N_sup` and 100B width this is memory-
   prohibitive; the TRM-style literature's answer is a form of truncated /
   one-step gradient approximation (only backprop through the last
   recursion step, or a fixed small window) — this is an **experimental**,
   not established, technique at this scale and needs to be validated on a
   held-out reasoning benchmark before being trusted in the 100B run.
10. **Memory blow-up:** bounded by (a) not persisting per-step activations
    beyond what's needed for the truncated backward window, and (b) not
    scaling `N_sup` per-token (item 5).
11. **Interaction with KV cache:** the recursion in this design operates on
    the pooled/positional hidden state *after* the base transformer's
    self-attention has already used the KV cache normally — recursion does
    not need its own KV cache, but it does add sequential (non-attention)
    compute on the critical path of every forward pass, which shows up as
    added latency per generated token, not added cache memory.
12. **Persisting z between turns:** no. Treat it as private scratch
    computation, discarded at the end of each generation, same as not
    exposing hidden reasoning tokens (see item 13). Persisting it would
    entangle unrelated turns' reasoning state and has no established benefit.
13. **Exposing z to the user:** no — matches your own instruction and
    current practice (concise reasoning summaries, not raw hidden state or
    raw chain-of-thought dumped to the user).

### Three candidate architectures (as requested)

- **Architecture A — standard decoder-only.** Lowest risk, most tooling
  support (this is what makes Ollama/LM Studio/GGUF compatibility easy —
  see Part 16-17). Baseline for every comparison in Part 24.
- **Architecture B — A + recursive latent reasoning module** (this
  document's Part 2, implemented in toy form in `model.py`'s
  `ReasoningBlock`). Adds sequential compute and training complexity for a
  reasoning-quality hypothesis that is **experimental at 100B scale** —
  published recursive-reasoning results are at far smaller scale and on
  narrower task distributions than "general-purpose chat/code/agent model."
- **Architecture C — B + adaptive computation + tool/agent system.** This
  is really "B, plus everything in Parts 9-13 wired through an
  orchestrator" (Part 10) — the recursion module is one component inside a
  larger agent loop, not a replacement for it. Most capability in your
  25-point requirement list (web search, tool use, RAG, memory, coding
  agent, trading research) comes from the **agent/orchestrator layer**,
  not from the base LLM's architecture — a correctly-engineered
  Architecture A model with a good agent harness will cover most of items
  1-20 in your goal list; B/C's value proposition is specifically
  reasoning-quality-per-parameter, which is the part that needs Part 24's
  controlled experiments before committing 100B-scale compute to it.

**Recommendation:** build and validate Architecture A first (Part 20's
progressive roadmap), add Architecture B as an ablation at the 1B-7B scale
where a full `N_sup`-step backprop is actually affordable, and only carry
the recursion module into the 30B+ runs if it wins on held-out reasoning
benchmarks at smaller scale with real numbers, not the toy-scale sanity
check this repo's `train.py` produces (which proves wiring, not benefit —
see its own printed disclaimer).

---

## 3. ~100B parameter budget — worked calculations

### Dense candidate

| Hyperparameter | Value |
|---|---|
| Layers | 92 |
| `d_model` | 10,240 |
| Attention heads | 80 (`d_head` = 128) |
| KV heads (GQA) | 10 (group size 8) |
| `d_ff` (SwiGLU) | 27,392 |
| Vocab size | 128,000 |
| Context length (trained) | 32,768, extended via RoPE scaling (Part 1) |
| Embedding | tied input/output |

Per-layer attention params:
`Wq = d_model² = 10240² = 104,857,600`
`Wk = Wv = d_model × (kv_heads × d_head) = 10240 × 1280 = 13,107,200` each
`Wo = 10240² = 104,857,600`
→ attention/layer = 104,857,600 + 13,107,200 + 13,107,200 + 104,857,600 = **235,929,600**

Per-layer SwiGLU MLP:
`W1 = W2 = d_model × d_ff = 10240 × 27392 = 280,494,080` each
`W3 = d_ff × d_model = 280,494,080`
→ MLP/layer = **841,482,240**

Per layer total = 235,929,600 + 841,482,240 = **1,077,411,840**
× 92 layers = **99,121,889,280**

Tied embedding: `128,000 × 10,240 = 1,310,720,000`

**Total ≈ 100.43B parameters** (all active every token — dense).

### MoE candidate (total ~100B, only a fraction active per token)

| Hyperparameter | Value |
|---|---|
| Layers | 40 |
| `d_model` | 6,144 |
| Attention heads | 48 (`d_head` = 128), KV heads 8 (GQA) — dense, every token |
| Experts per MoE-MLP layer | 16, **top-2 activated** |
| `d_ff` per expert | 8,192 |
| Vocab | 128,000, tied |

Per-layer attention (dense, all active): `88,080,384` (same formula as above with `d_model=6144`)
Per-expert MLP: `3 × (6144 × 8192) = 150,994,944`
All 16 experts (stored, not all active): `16 × 150,994,944 = 2,415,919,104`
Layer total (stored) = 88,080,384 + 2,415,919,104 = **2,503,999,488**
× 40 layers = **100,159,979,520**
+ tied embedding `128,000 × 6144 = 786,432,000`

**Total stored ≈ 100.95B parameters.**

Active per token: attention (always active) + 2/16 experts:
`88,080,384 + (2 × 150,994,944) = 390,070,272` per layer × 40 = **15,602,810,880**
+ embedding (always active, tied) `786,432,000`
**≈ 16.4B active parameters per token** (~16% of total — comparable sparsity ratio to shipped 8-expert/top-2 MoE models scaled up in expert count).

**Why MoE over dense here:** the FLOPs/token (and therefore training and
inference compute cost) scale with *active* params, while quality scales
more closely with *total* params in the published MoE scaling literature.
At fixed inference compute budget, MoE gives access to ~6x the total
parameters of the dense design at the same active-compute cost — this is
the standard argument for MoE at this scale and is why current
frontier-adjacent open-weight releases in the 100B+ range are
overwhelmingly MoE rather than dense. The cost: ~2x the *storage/memory*
footprint of the active-equivalent dense model (all experts must be
resident even if unused per-token, unless expert-offloading is used — Part
18), and materially more complex distributed training (expert parallelism
on top of tensor/pipeline/data parallelism).

### Memory at each precision (dense candidate, 100.43B params; MoE is ~100.95B, essentially identical)

| Precision | Bytes/param | Total |
|---|---|---|
| FP32 | 4 | 401.7 GB |
| BF16 / FP16 | 2 | 200.9 GB |
| INT8 | 1 | 100.4 GB |
| INT4 | 0.5 | 50.2 GB |

### KV cache (dense candidate)

Elements/token = `n_layers × 2 (K,V) × kv_heads × d_head = 92 × 2 × 10 × 128 = 235,520`
At BF16: `235,520 × 2 bytes = 471,040 bytes ≈ 0.45 MB/token`
At 32,768-token context, batch size 1: `0.45 MB × 32,768 ≈ 14.4 GB` — **per sequence**, on top of the ~200 GB (BF16) of weights. This is why GQA (shrinking `kv_heads` from 80 to 10) matters: full MHA here would be **8x** that KV-cache figure.

---

## 4. Tokenizer

**Established approach:** byte-level BPE (GPT-2/GPT-4 style) or SentencePiece
Unigram, trained on a representative multilingual + code corpus, ~100-128k
merges. Byte-level fallback guarantees lossless round-tripping for any input
(no `<unk>` on unseen text), which matters for code, uncommon scripts, and
mixed-language text (relevant given your English/Filipino/Tagalog/Ilocano
requirement — these need real corpus representation in the *training data*
for the merges to be useful, not just byte-level fallback; byte-level alone
means every Ilocano word not seen at training time costs ~1 token/byte,
which is correct but inefficient).

**Recommended vocab size: 128,000.** Rationale: large enough to give
efficient multi-byte merges for English, code, JSON/XML/Markdown structure
tokens, and the specified languages without the embedding table becoming a
disproportionate share of total params (at `d_model=10,240`, 128k vocab is
~1.3B params — about 1.3% of the dense 100B design, in line with typical
current open-model ratios). Reserve explicit special tokens: `<bos>`,
`<eos>`, `<pad>`, tool-call open/close, structured-output (JSON) open/close,
system/user/assistant role tokens, and a small set of code-language tags —
this is standard practice (see Llama 3/Qwen tokenizer special-token designs)
and avoids the model needing to *learn* delimiter tokens from BPE merges
that could also appear in natural text.

**This repo's prototype now has both.** `tokenizer.py` is the original
byte-level stand-in, kept for reference. `bpe_tokenizer.py` is a real,
trained BPE tokenizer (GPT-2-style byte-level base alphabet, so it still
round-trips losslessly on unseen bytes/scripts) — trained on this repo's own
`dataset.py` corpus, 700-token vocab, and it actually compresses: the toy
training text runs ~49% of its byte-level token length under this
tokenizer. This is still nowhere near the 128k-merge, representative-corpus
tokenizer a real 100B run needs — 700 merges on ~5KB of hand-authored text
learns almost nothing about the "specified languages need real corpus
representation" point above — but the *algorithm* (pretokenize, count
adjacent-pair frequency, merge, repeat, save/load merge rules) is the real
one, not a placeholder.

---

## 5-13. Dataset, training pipeline, coding/research/finance/design agents, memory, multimodal, chatbot — condensed

These sections are architecture/process specifications, not calculations,
so they're summarized here rather than repeated at Part-25's full length;
ask for any one expanded to its own document if useful.

- **Dataset (Part 5):** separate curated pools per category as specified;
  the two non-negotiable process steps regardless of category are (a)
  document-level and near-duplicate deduplication (MinHash/LSH, standard),
  and (b) benchmark-contamination screening against your eval suite (Part
  23) before any pretraining run, not after. **Do not scrape indiscriminately
  under a "training on public data" theory** — use datasets with clear
  licensing (public-domain, permissively licensed, or properly licensed
  text), matching your own instruction not to recommend indiscriminate
  copyrighted scraping.
- **Training pipeline (Part 6):** the 13-stage structure you specified is
  the right shape and matches established multi-stage post-training
  practice (pretrain → SFT → domain specialization → tool-use → agent
  trajectories → preference optimization → long-context extension →
  eval → quantize → deploy). Concrete hyperparameters (LR, batch size,
  optimizer schedule) are scale- and dataset-dependent and would be
  **invented** if given generic numbers here — they get tuned per stage
  against real validation loss, not fixed in advance.
- **Coding agent (Part 8):** the sandbox requirements you listed (containers,
  resource limits, filesystem isolation, network restrictions, timeouts,
  audit logs) are the correct minimum bar and match this conversation's own
  execution environment's model (an isolated container with an explicit
  network allowlist, read-only mounts for skills/uploads, a separate
  outputs directory) — a reasonable reference implementation to study.
- **Research agent (Part 9):** the planner → search → fetch → extract →
  evidence-store → cite pipeline you diagrammed is standard current agent
  design. The hard requirement worth flagging explicitly: the evidence store
  needs per-claim source attribution *before* the reasoning model writes the
  final answer, not reconstructed after — otherwise citation becomes
  post-hoc rationalization rather than grounding.
- **Finance/trading (Part 12):** your requirement (research + paper trading
  first, no live execution, out-of-sample backtest validation, explicit
  authorization/kill-switch gating before any live-execution phase) is the
  correct ordering and should not be relaxed. Look-ahead bias prevention
  (strict point-in-time data joins) is the single most common correctness
  bug in backtesting systems and deserves its own test suite (Part 23).
- **Design/layout agent (Part 13):** separating design reasoning / code
  generation / visual validation into distinct stages (rather than one
  model call doing all three) is the right structure — it lets a vision
  model validate the *rendered* output against the *intended* design
  independently of whether the generated code is syntactically "nice."
- **Memory (Part 11):** the layered structure (short-term/working/
  long-term-semantic/episodic/procedural/knowledge-base) matches current
  agent-memory practice; the operational requirement worth over-indexing on
  is user inspect/edit/export/delete — build this before scaling data
  volume, not after.
- **Multimodal (Part 14):** **modular** (B) over fully-multimodal-in-one-100B
  (A) — recommended. A separately-trained vision encoder + projector bolted
  onto the frozen or lightly-adapted text model (LLaVA-style architecture)
  lets you iterate on vision quality without retraining the 100B backbone,
  matches your own "modular so components can be replaced" requirement
  (goal #30), and is the dominant pattern in current open multimodal
  releases. A multimodal-MoE (C) is a reasonable later optimization, not a
  starting point.
- **Chatbot (Part 15):** FastAPI + SSE/WebSocket streaming + OpenAI-compatible
  `/v1/chat/completions` surface is the standard, low-risk choice — it gets
  you compatibility with the large existing ecosystem of OpenAI-API clients
  for free.

---

## 14. Ollama / LM Studio / AirLLM compatibility (verified against current docs)

**Ollama:** imports GGUF-format weights via a `Modelfile` and runs them
through a pinned internal `llama.cpp` build — Ollama does **not**
automatically support an arbitrary custom architecture. A new architecture
(including this document's recursive-reasoning module) needs to actually be
implemented in the `llama.cpp`/Ollama codebase before a GGUF export of it
will load; a GGUF with an architecture string the pinned build doesn't
recognize fails with an "unknown model architecture" error, independent of
Ollama's version number matching your intuition. This is a real,
documented, currently-occurring failure mode (recent examples: brand-new
architectures like DiffusionGemma sitting as an open feature request for
weeks after weights shipped). **Practical implication for Architecture B/C:**
plan on a standard Architecture-A-shaped export path (dense or
already-llama.cpp-supported MoE structure) for Ollama/GGUF compatibility;
the recursive-reasoning module, if kept, would need either (a) upstream
`llama.cpp` support work, or (b) being stripped/distilled into a
standard-architecture checkpoint for that deployment target. Example
Modelfile for a compatible export:

```
FROM ./orbit-100b-q4_k_m.gguf
PARAMETER num_ctx 32768
PARAMETER temperature 0.7
SYSTEM "You are ORBIT, a general-purpose assistant."
```

**LM Studio:** also runs on a `llama.cpp`-derived backend and exposes an
OpenAI-compatible local server; same GGUF-and-supported-architecture
constraint as Ollama. No additional compatibility surface beyond that.

**AirLLM (layer-by-layer disk-offload inference):** technically viable for
serving a 100B model on very limited VRAM (loads one layer's weights at a
time from disk/CPU RAM into GPU memory), but **do not read low VRAM as fast
inference** — layer-by-layer loading is bound by disk/PCIe bandwidth, not
compute, and at 92 layers × ~1.1-2.2 GB/layer (BF16/INT8) per forward pass,
per-token latency is dominated by repeated weight streaming rather than
matrix-multiply time. It's a "can run at all on modest hardware" tool, not a
"runs fast on modest hardware" tool — appropriate for offline/batch use,
not interactive chat latency targets.

---

## 15. Hardware scenarios (order-of-magnitude, not vendor pricing — pricing changes too fast to state reliably here)

| Scenario | Realistic scope |
|---|---|
| A. Dev workstation (1 consumer GPU, 24 GB VRAM) | Prototype at this repo's toy scale (<10M params) comfortably; a quantized 7-8B model for inference testing (INT4, ~4-5 GB) |
| B. Small research cluster (4-8× 80GB-class GPUs) | Train/fine-tune up to roughly 7B-13B dense with standard FSDP/DeepSpeed; inference-serve a quantized 30-70B |
| C-E. 8/16/32-GPU servers (80GB-class) | Fine-tune 30-70B with tensor+pipeline parallelism; inference-serve the 100B dense or MoE design at BF16 with enough headroom for KV cache and batching |
| F. 64-GPU cluster | Pretraining runs in the 30-70B range become feasible in reasonable wall-clock time |
| G. Cloud training cluster (hundreds of GPUs, weeks-months) | Required scale for a from-scratch ~100B pretraining run — **this is genuinely expensive** (hundreds of GPU-node-weeks); do not let anyone tell you otherwise, and do not commit to this stage before the smaller-scale roadmap (Part 16) has validated the architecture |

**Why training memory vastly exceeds inference memory:** inference needs
weights + KV cache + activations for one forward pass. Training needs
weights + gradients (same size as weights) + optimizer state (Adam: 2x
weights, for the first/second moment estimates) + activations retained for
backward (not discarded after each layer, unlike inference) + communication
buffers for whichever parallelism strategy is in use. Rule of thumb before
any framework-specific overhead: **training memory ≈ 4x weight memory just
from weights+gradients+Adam-state**, before activations — which is why the
BF16 dense design's ~201 GB of weights implies roughly 800 GB+ of
combined weight/gradient/optimizer-state memory *before* activations and
KV-cache-equivalents during training, spread across the cluster via
sharding (FSDP/ZeRO/Megatron-style).

---

## 16. Realistic development roadmap

Matches your Part 20 structure — each stage should genuinely gate the next
(train, benchmark, debug, compare, only then scale):

0. **Tokenizer** — train the real BPE/Unigram tokenizer on a representative
   corpus sample (not the byte-level toy stand-in in this repo).
1. **~10M toy transformer** — this repo's prototype is one order of
   magnitude below even this rung (~100k params); the next real step is a
   proper small dense Architecture-A model at this size, trained with a real
   framework (PyTorch/JAX) once GPU access is available, to get real
   throughput/quality numbers this NumPy prototype can't produce.
2. **100M** — first point where held-out perplexity and small benchmark
   subsets become meaningful.
3. **1B** — first reasonable point to run the Architecture A vs B ablation
   from Part 24 (small enough to backprop through full `N_sup` recursion,
   large enough that results say something about scaling).
4. **3B, 5. 7-8B** — instruction-tuning and tool-use pipeline validated
   end-to-end at a scale cheap enough to iterate on quickly.
6. **30B** — first point where MoE-vs-dense tradeoffs (Part 3) become worth
   re-measuring empirically rather than assumed from the calculation.
7. **70B** — validate distributed-training strategy (tensor+pipeline+FSDP
   combination) at a scale close enough to 100B that the same recipe should
   transfer.
8. **100B/MoE** — only after 0-7 have each independently validated their
   piece of the design.

---

## 17. Repository structure

Matches your Part 21 layout as specified — it's a sound modular structure
(model/training/agents/tools/inference/api/frontend separated cleanly) and
doesn't need modification. This repo (the prototype delivered with this
document) corresponds to a minimal slice of `model/transformer/`,
`model/attention/`, `model/embeddings/`, `model/tokenizer/`,
`model/recursive_reasoning/`, and `training/pretraining/`.

---

## 18. What's implemented vs proposed in this deliverable

**Actually implemented, run, and tested in this session** (see files in this
folder): a from-scratch NumPy reverse-mode autograd engine with numerically
gradient-checked ops; a decoder-only transformer with RMSNorm, RoPE
(hand-derived backward), GQA, SwiGLU, tied embeddings; an optional recursive
x/y/z reasoning module with shared weights and full backprop-through-
recursion; a real trained BPE tokenizer (`bpe_tokenizer.py` — GPT-2-style
byte-level base alphabet, lossless round-trip on unseen text, ~49%
compression vs. the byte-level fallback kept in `tokenizer.py`); nucleus
(top-p) + repetition-penalty sampling (`sampling.py`) replacing plain
multinomial sampling; an Adam optimizer; a real dataset construction
pipeline (`dataset.py`) — 9 hand-authored raw-data categories (English
prose, Python, JavaScript, JSON, Markdown, math, Filipino/Ilocano, Q&A,
persona-chat), exact + near-duplicate dedup via shingle/Jaccard matching
(verified to catch both a planted exact duplicate and a planted
near-duplicate), a quality filter, a character-frequency language-ID
heuristic, and a train/val split with an explicit, honestly-reported
contamination check (shared 8-grams between splits, not assumed to be
zero); a training loop with that pipeline's real output tokenized through
the real BPE tokenizer, a held-out validation split, and real perplexity
evaluation, run across two model sizes (tiny/small) and both architectures;
checkpoint save/reload verified to reproduce the same validation loss; a
generation script run against a trained checkpoint using the improved
sampler; a feature-hashed vector store (add/query/delete/TTL-expiry, cosine
similarity) used both for RAG/long-term memory AND as ORBIT's persona
knowledge base — a retrieval-first chat agent that matches user questions
against a 25-row hand-authored persona dataset and returns the matched
answer verbatim, falling back to an honest hedge (not raw model noise)
below the similarity threshold, tuned and verified against both true
positives and a deliberate false-positive case; a sandboxed Python tool
(subprocess isolation, static import blocklist, CPU/memory rlimits,
wall-clock timeout, audit log) plus a file-read tool confined to a sandbox
root and an honestly-labeled web-search stub; a paper-trading engine
(buy/sell bookkeeping, transaction costs, insufficient-funds/position
guardrails) with an SMA-crossover backtest reporting P&L, drawdown, and a
buy-and-hold baseline; a rule-based agent orchestrator routing across seven
specialized agents (code/research/data/finance/design/file/memory+chat)
plus a verifier pass; and an OpenAI-wire-compatible FastAPI server
(`/v1/chat/completions` with both streaming SSE and non-streaming,
`/v1/models`, `/v1/memory` inspect/delete, `/healthz`) integration-tested
end to end — persona retrieval, hedge fallback, and tool-agent routing all
confirmed working through the actual HTTP contract. A real, Soup-validated
persona dataset (`soup_data/`) and a runnable `soup.yaml` config for anyone
with real GPU hardware to actually fine-tune a real base model on it.

**Proposed, not implemented:** everything at 100B scale (obviously);
real licensed/public-domain raw data at production volume (this session's
`dataset.py` is hand-authored/synthetic, explicitly not scraped, per the
spec's own instruction — see that file's docstring); a production-scale BPE
tokenizer (700 merges on ~5KB of text learns almost nothing — the algorithm
is real, the scale isn't); a real language-ID model (the heuristic in
`dataset.py` is a stand-in, documented as such); the full 13-stage training
pipeline; model-driven (rather than keyword-rule-based) agent routing and
real tool-calling from the model itself; a trained semantic embedding model
for retrieval (the vector store's hashing-trick embeddings are a real
mechanism, tuned and threshold-verified for the persona-matching use case
specifically, but not a general-purpose semantic encoder); a true
container/gVisor sandbox boundary (the current one is subprocess + rlimits +
a static blocklist, explicitly flagged in `tools.py` as insufficient for
production); live market data and broker connectivity for finance (paper
trading only, on synthetic price
series); a real search API behind the research agent; the design agent's
visual-validation pass; the multimodal encoders; the production chatbot
frontend; Ollama/LM Studio export tooling; any actual benchmark numbers, GPU
pricing, or training cost figures (Part 24's controlled experiments and Part
27's cost estimates specifically require infrastructure this session
doesn't have access to, and inventing numbers for them would violate your
own "do not hallucinate" instruction more than declining to would).

## 19. Soup integration (real fine-tuning tool, honestly scoped)

[MakazhanAlpamys/Soup](https://github.com/MakazhanAlpamys/Soup) (`soup-cli`)
is a real, actively-maintained LoRA/QLoRA fine-tuning CLI with layer
streaming for low-VRAM training of real base models (e.g. Llama-3.1-8B,
Qwen2.5) — not a dataset. Giving ORBIT an actual trained-in personality via
Soup needs two things this sandbox doesn't have: a GPU (Soup's own training
path is torch/CUDA-based) and access to a base model download (Hugging Face
Hub isn't in this sandbox's network allowlist). So here's exactly what was
and wasn't done:

**Actually done:** authored a 15-row persona dataset
(`soup_data/persona_chat.jsonl`, Alpaca instruction/output format) giving
ORBIT a name and a consistent voice (direct, a little dry, upfront about
being a small prototype). Ran Soup's own **light-mode** tooling on it for
real — `soup data validate` (15/15 valid), `soup data stats` (length/token
distribution), `soup data dedup` (MinHash, 0 duplicates found — correctly,
since these 15 rows are genuinely distinct), and `soup data split`
(12 train / 3 val). Wrote `soup.yaml`, a real config anyone with a GPU can
run via `soup train -c soup.yaml` against a small base model
(Qwen2.5-0.5B-Instruct — chosen deliberately small, since 15 rows can't
meaningfully move an 8B model's behavior). Also flattened the same persona
data into a `persona_chat` category in `dataset.py`'s own pipeline and
retrained this session's toy `TinyLM` on it, and gave the orchestrator's
chat fallback (`MainChatAgent` in `agents.py`) a real persona-preamble
prompt and wired it into `api.py`.

**Honestly, what that last part proves and doesn't:** the wiring is real —
`MainChatAgent` actually generates from the trained checkpoint with the
persona preamble prepended, and the orchestrator actually routes plain chat
through it now instead of a placeholder string. What it does *not* do is
give the toy model a working personality — see `generate.py`'s sample
output. A ~100k-parameter model trained on a few KB of text total (15
persona rows mixed into ~40 other documents) cannot hold a persona in any
meaningful sense; the persona preamble is there, but the model's raw
byte-level output remains close to noise. Real personality-via-fine-tuning
needs the actual `soup train` run this document's `soup.yaml` sets up —
that's the honest state of this integration: the dataset is real and
Soup-validated, the config is real and runnable, the toy-model wiring is
real, and the actual trained personality is the piece that needs hardware
this session doesn't have.

## 20. Known limitations and open questions

- The Architecture A-vs-B question (does recursive reasoning help a
  general-purpose model, net of its added training/inference complexity) is
  genuinely open and this document takes no position beyond "test it at
  1B-scale before committing 100B compute to it."
- The truncated-backprop-through-recursion approximation needed to make
  Architecture B/C affordable at 100B scale (Part 2, item 9) is itself an
  active research question, not a solved one — this document flags it
  rather than picking an unvalidated answer.
- No cost estimates are given for the from-scratch 100B pretraining run
  (Part 27) — current GPU pricing and required token counts are both moving
  targets, and any number stated here without a live pricing check would be
  exactly the kind of hallucinated figure your instructions warn against.
- MoE routing stability (expert collapse, load balancing) is a well-known
  practical failure mode in the published MoE literature and needs its own
  auxiliary load-balancing loss — noted here as a requirement, not designed
  in detail in this pass.
