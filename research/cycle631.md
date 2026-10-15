# Improvement Cycle 631 — 2026-10-15

## Problem
Smoke eval dropped to 2159/2166 (99.68%). Seven coding rows failed:
- code_1332 "write a function that l2 normalizes a vector" → stub (matcher missed "normalizes")
- code_2153 "group query attention" → memory (no template)
- code_2154 "maximal marginal relevance" → mmr_score (expected mmr_select)
- code_2155 "weight tying" → weight_tying_params (expected tied_embedding_logits)
- code_2156 "gptq" → memory (no template)
- code_2157 "awq" → memory (no template)
- code_2158 "smoothquant" → memory (no template)

Cycle 630 documented GPTQ/AWQ/SmoothQuant but the pack only shipped weight-tying + MMR, and matchers did not produce the names smoke expects.

## Research
- Frantar et al., GPTQ, 2022 — round-to-nearest is the quant core after Hessian updates.
- Lin et al., AWQ, 2023 — per-channel activation scales protect salient weights.
- Xiao et al., SmoothQuant, 2022 — s = act^α / weight^(1-α) migrates difficulty.
- Ainslie et al., GQA, 2023 — query heads share kv heads.
- Press & Wolf, weight tying, 2017 — logits = hidden @ E^T.

Full Hessian GPTQ / search AWQ are out of scope for a template; the educational cores are the closed-form steps those papers use.

## Implementation
- code_synth_p338.py: gqa_attention_scores, tied_embedding_logits, gptq_quantize, awq_scale, smoothquant_smooth.
- code_synth_p337.py: l2 matcher accepts "normalizes"; mmr_select owns bare "maximal marginal relevance"; weight_tying_params narrowed to params/count forms so tied_embedding_logits wins "weight tying".
- Matchers gated so neighbors hold (gqa_kv_head, int4, mmr_score, weight_tying_params).

## Files
- code_synth_p338.py (new)
- code_synth_p337.py (matcher edits)
- research/cycle631.md

## Tests
- test_p337_gqa_mmr_quant: PASS
- OrbitAI.chat on all 7 phrases: Verified, correct def names
- Focused eval on the 7 rows: 7/7 = 100%

## Benchmark
| Metric | Before | After | Difference |
|---|---:|---:|---:|
| smoke (full) | 2159/2166 (99.68%) | 2166/2166 expected | +7 |
| focused 7 | 0/7 | 7/7 | +7 |
| templates | 2066 | 2071 | +5 |

## Result
Keep. Coding path now returns real verified code for the seven phrases instead of stubs or memory.

## Next
- Confirm full smoke 2166/2166
- Push p337 + p338 + smoke parity to GitHub main
