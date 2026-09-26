# Running ORBIT on Windows, macOS, and Ubuntu/Linux

Preferred launcher: `python run_orbit.py` (doctor / serve / chat).  
You can also run `uvicorn api:app --port 8000`.

API / serve is **optional**. Core agent + TinyLM + eval work without FastAPI.
`run_orbit.py doctor` treats missing FastAPI/uvicorn as a non-blocking warning.

```bash
# agent / eval / chat only
pip install -r requirements.txt

# HTTP API + Web UI
pip install -r requirements-api.txt
# or: pip install fastapi uvicorn
python run_orbit.py serve
```

ORBIT is pure Python + NumPy. Python 3.10+ required (developed on 3.12).

```bash
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run_orbit.py doctor
python run_orbit.py eval
```

Optional PyTorch extras: `pip install -r requirements-torch.txt`.
No GPU or compiled extensions are required for the agent runtime.
