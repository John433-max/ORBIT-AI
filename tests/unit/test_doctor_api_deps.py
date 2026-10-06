"""Doctor and serve must point API installs at requirements-api.txt."""

from pathlib import Path


def test_api_install_hint_uses_requirements_api():
    text = Path("run_orbit.py").read_text(encoding="utf-8")
    assert "fastapi/uvicorn not installed (pip install -r requirements-api.txt)" in text
    assert "fastapi/uvicorn not installed (pip install -r requirements.txt)" not in text
    assert "uvicorn is required: pip install -r requirements-api.txt" in text


def test_ci_installs_requirements_api():
    for name in (".github/workflows/tests.yml", ".github/workflows/ci.yml"):
        text = Path(name).read_text(encoding="utf-8")
        assert "requirements-api.txt" in text
        assert "import fastapi, uvicorn" in text
