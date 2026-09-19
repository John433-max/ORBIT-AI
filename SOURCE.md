# Full source

**GitHub:** https://github.com/John433-max/ORBIT-AI

## Complete archive

Project workspace: `artifacts/ORBIT-AI-source.zip` (~352 KB)

Includes the full ORBIT tree **except** large `.npz` weight files (gitignored).

## Cycles 70–79 (local, 2026-09-19)

| Cycle | Change |
|-------|--------|
| 70 | Unit conversion (km/m, °C/°F, kg/g) |
| 71 | Thinking routes science/units |
| 72 | OrbitAI.status: thinking + persona ckpt |
| 73 | Persona chat lines |
| 74 | Calculator natural voice |
| 75 | test_science_math_units |
| 76–79 | Tests green (118), GitHub docs + launcher |

## Smoke

```text
100 km to m          → 100 km = 100000 m
0 celsius to fahrenheit → 0 °C = 32 °F
```

## Upload full tree

1. Download `ORBIT-AI-source.zip` from the Grok project folder
2. Unzip over a clone of this repo
3. `git add -A && git commit -m "Full ORBIT source" && git push`

Or drag-and-drop the unzipped files on GitHub → Add file → Upload files.
