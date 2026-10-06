# Improvement Cycle 461

Date: 2026-10-06

## Problem
Phrase-gated asks still fell through after Cycle 460: METAR parse, dew point, initial bearing, next prime, and metaphone. "converts an integer to a roman numeral" matched `roman_to_int` because a later pack treats any "roman numeral" phrase as the reverse conversion.

## Research
- SOURCE: FAA METAR group order (station, time, wind `dddffKT` / gust `G`, temp/dew `TT/DD` with `M` for minus, altimeter `Axxxx`). Specimen groups: `18015G20KT`, `22/M01`, `A2992` = 29.92 inHg.
- DATE: 2026-10-06
- TECHNIQUE: regex extract of those groups; remarks ignored.
- TRADE-OFFS: not a full FMH-1 decoder (no RVR, sky, weather phenomena).
- SOURCE: August–Roche–Magnus dew point, a=17.27, b=237.7 °C. RH 100% inverts to the dry-bulb temperature.
- SOURCE: initial great-circle bearing `atan2(sin Δλ cos φ2, cos φ1 sin φ2 − sin φ1 cos φ2 cos Δλ)`.
- SOURCE: Lawrence Philips, Metaphone (Computer Language, 1990). Implemented a reduced primary encoder (TH→0, PH→F, drop non-initial vowels), not Metaphone 3 and not Double Metaphone alternate codes. Smith→SM0, Robert→RBRT, phone→FN on this reducer.
- SOURCE: standard subtractive Roman numerals (III, LVIII, MCMXCIV).

## Implementation
- `code_synth_p179.py` loaded first.
- Direction gate: integer→Roman requires an integer-to-Roman phrase and rejects "roman numeral to" / "from roman".
- METAR, dew point, bearing, next prime, reduced metaphone.
- Smoke `code_1319`–`code_1324`.
- Unit `test_p179_metar_dew_bearing_roman_direction`.

## Tests
- p179 examples: 6/6 verify ok after fixing in-function `import re` and mapping `M`.
- Direct test_p179 + test_p177 PASS.
- Sibling probes: roman→int stays `roman_to_int`; soundex, haversine, unix iso-8601 unchanged.

## Benchmark

| Metric | Before | After | Difference |
|---|---:|---:|---:|
| unique templates | 1282 (pre-pack load of p179) | 1287 | +5 names (integer_to_roman already existed) |
| smoke rows appended | 1356 catalogued | +6 (`code_1319`–`code_1324`) | new verified asks |
| integer→roman route | `roman_to_int` | `integer_to_roman` verified | fixed |
| METAR / dew / bearing / next prime / metaphone | stub | verified | new |

Full smoke re-eval not re-run. Targeted asks this cycle changes pass.

## Result
Kept. Metaphone is a reduced primary encoder, not Philips Metaphone 3.

## Next
Non-template bottleneck (TinyLM decode / INT4 without full FP32 W) or remaining phrase misses (heat index, wind chill, celsius to kelvin).
