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
