# Cycle 348 — doctor stays READY without PyYAML

## Problem
Fresh doctor (PyYAML absent) was NOT READY: `Dependencies [ERROR] PyYAML not installed`. Shipped `configs/*.yaml` already match `model.yaml_lite` (maps, scalars, flow lists). `OrbitConfig.load` had a yaml_lite branch locally, but GitHub `run_orbit.py` still classified any "not installed" line except fastapi as a blocking error. The unit test named `test_config_load_without_pyyaml` never cleared the PyYAML module, so it passed with PyYAML installed.

## Research
SOURCE: YAML 1.2.2 (https://yaml.org/spec/1.2.2/) subset already implemented in model/yaml_lite.py; PyYAML safe_load (https://pyyaml.org/wiki/PyYAMLDocumentation)
DATE: 2026-10-01
TECHNIQUE: severity split + forced fallback test
WHAT IT IMPROVES: doctor readiness on a numpy-only install
REQUIREMENTS: stdlib parser already in tree
TRADE-OFFS: yaml_lite is not a general YAML parser; anchors/tags still rejected
RELEVANCE: doctor critical path uses orbit.core.config (no PyYAML). Educational model configs are the subset parser's target.

## Implementation
- Doctor: PyYAML message that mentions yaml_lite is WARNING, not ERROR.
- `tests/unit/test_yaml_lite.py`: `test_config_load_forces_yaml_lite` sets `model.config.yaml = None` and loads `configs/tiny.yaml`.

## Measurement
- Simulated missing PyYAML: doctor Overall READY (PyYAML WARNING, API deps WARNING, Ollama OPTIONAL). Exit 0.
- Same probe before the severity split (GitHub run_orbit.py): message `PyYAML not installed (pip install PyYAML)` counted in missing_core → Dependencies ERROR → NOT READY.
- unittest tests.unit.test_yaml_lite: 6 passed.
- Smoke eval unchanged this run: 761/761 (100%) before the doctor-only change.
- Probes: add() verified; fusion search returned live sources; identity ORBIT.

## GitHub
Push run_orbit.py, model/config.py, model/yaml_lite.py, tests/unit/test_yaml_lite.py.
