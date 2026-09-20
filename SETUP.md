# Running ORBIT on Windows, macOS, and Ubuntu/Linux

Preferred launcher: `python run_orbit.py` (`doctor` / `serve` / `chat`).  
You can also run `uvicorn api:app --port 8000`.

ORBIT is pure Python + NumPy with no required GPU, so setup is the same shape on every platform: get Python 3.10+, create a virtual environment, install `requirements.txt`, run.

Tested during development against **Python 3.12** on Linux. Python 3.10 or newer should work.

---

## All platforms (short path)

```bash
git clone https://github.com/John433-max/ORBIT-AI.git
cd ORBIT-AI
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run_orbit.py doctor
python run_orbit.py               # http://127.0.0.1:8000/
```

Optional Torch extras for TinyLM torch backend:

```bash
pip install -r requirements-torch.txt
```

---

## macOS notes

- Install Python 3.10+ from python.org or `brew install python@3.12`
- Use `python3` / `pip` inside the venv after `source venv/bin/activate`

---

## Ubuntu / Debian notes

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip
```

Then the same venv + `pip install -r requirements.txt` steps.

---

## Windows notes

- Install Python 3.10+ from python.org and check **Add to PATH**
- In PowerShell or cmd:

```bat
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python run_orbit.py doctor
python run_orbit.py
```

WSL2 is supported: use the Linux instructions inside WSL.

---

## Configuration

Copy `.env.example` to `.env` and set provider variables as needed (`ORBIT_MODEL_PROVIDER`, Ollama/OpenAI URLs, optional `ORBIT_API_KEY`).

See the main [README.md](README.md) configuration table.

---

## Tests

```bash
PYTHONPATH=. pytest tests/unit -q
```

---

## Honesty

ORBIT is a **modular local AI agent runtime**. It is not a 100-billion-parameter model. Attach larger models through ModelProvider backends (Ollama, OpenAI-compatible, optional GGUF) when you need stronger generation.
