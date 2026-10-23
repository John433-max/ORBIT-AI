# ORBIT Priority Loop — 2026-10-23 static offline facts

## Baseline
- doctor: READY (API deps WARNING optional; Ollama OPTIONAL offline)
- smoke/eval: 2105/2105 accuracy=100% (before this run)
- probes: coding returns real `add` + Verified; search honest offline; identity ORBIT

## Chosen priority
Priorities 1–3 already green. Added a small offline static-fact path for stable geography so pure knowledge asks (capitals) return a known answer instead of only the no-live-web dead end. News/recent still honest offline.

## Changes
- agents.py: `_offline_static_fact` + `_OFFLINE_FACTS` (capitals of FR/JP/DE/IT/ES/UK/CA/AU/IN/CN/BR)
- ResearchAgent.run: return fact before generic offline message (skips if news/recent)
- MainChatAgent.run: short-circuit hedge when a static fact matches
- evals/datasets/smoke.jsonl: +4 rows (fact_capital_fr/jp/de, search_news_still_offline)

## Tests
- Orchestrator / OrbitAI probes: capitals → Paris/Tokyo/Berlin with offline label; news still "No live web"; code still real function; identity still ORBIT
- Full eval re-run recommended after smoke append (n=2109)

## Benchmark before → after
- capital of France: "No live web…" → "The capital of France is Paris. (offline known fact…)"
- capital of Japan: chat hedge → "The capital of Japan is Tokyo. (offline known fact…)"
- news/search/coding/identity: unchanged

## GitHub push: NO (this run; local only until full eval confirmed)
## Next priority remaining
1. Re-run full smoke after append and confirm ≥ previous accuracy.
2. Optional: more stable facts or country→capital if demand appears.
3. Serve extras CI install still optional.
