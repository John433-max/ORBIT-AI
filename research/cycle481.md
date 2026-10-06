# Cycle 481

## Problem
GitHub Tests run 37545375783 (commit a2c7d90) failed on 3.11 and 3.12:

`test_p179_metar_dew_bearing_roman_direction`
`match_template("write a function that computes haversine distance between two lat lon points")` returned `point_distance` instead of `haversine_km`.

## Cause
Packs load newest-first. `code_synth_p194.point_distance` matches any prompt containing both "distance" and "point", so it wins before p164 `haversine_km` ("haversine" or "great circle").

## Change
Exclude haversine, great circle, lat, and lon from the point_distance matcher. Euclidean two-point asks still match.

## Check
- haversine lat/lon prompt -> haversine_km
- "distance between two points" -> point_distance (verified, 3 examples)
- great circle + points -> haversine_km
