# Improvement Cycle 474

## Problem
Natural-language coding asks for hours to minutes, days to hours, weeks to days, rectangle perimeter, and trapezoid area returned the generic NotImplemented draft.

## Research
SI time units used in teaching and NIST practice are exact: 1 h = 60 min, 1 day = 24 h, 1 week = 7 days. Trapezoid area is (a+b)/2 * h, distinct from the triangle base/height template. Rectangle perimeter is 2(w+h), distinct from rectangle area.

## Sources
- NIST SP 330-2019 SI brochure (second is the base unit; minute/hour/day are accepted non-SI units with exact factors 60 / 3600 / 86400)
- Local unmatched probes on 2026-10-06

## Finding
Phrase gates loaded before the seconds converters avoid stealing hour/minute asks. Perimeter must exclude area so rectangle-area templates stay in place.

## Implementation
- code_synth_p191.py: hours_to_minutes, minutes_to_hours, days_to_hours, weeks_to_days, rectangle_perimeter, trapezoid_area
- Loader lists p191 first locally
- Closed a truncated synthesize_and_verify return that dropped the error key
- Smoke code_1391-code_1396 and test_p191_time_geometry

## Result
Local smoke 1428/1428 to 1434/1434 (100%). Coding 1383 to 1389.

## Risks
Week-to-hours and day-to-seconds still miss. GitHub loader still needs p191 registered; missing packs are skipped until the loader lists them.
