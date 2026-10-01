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

ORBIT is pure Python + NumPy with no compiled extensions and no GPU
requirement, so setup is the same shape on every platform: get Python 3.10+,
create a virtual environment, install `requirements.txt`, run.

Tested during development against **Python 3.12** on Linux. Python 3.10 or
newer should work; anything older is untested and not recommended (the code
uses modern type hints and dict/set literal features).

---

## macOS

1. **Install Python 3.10+** if you don't already have it.
   - Easiest: [python.org](https://www.python.org/downloads/macos/) installer, or
   - Via Homebrew: `brew install python@3.12`
   - Check what you have: `python3 --version`

2. **Clone/unzip the project**, then from a Terminal in the project folder:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Run the tests** (optional, confirms everything works):
   ```bash
   python3 -m pytest -q
   ```

4. **Train the default small model** (fast, a few seconds — produces
   `bpe_tokenizer.json` + `checkpoint_base.npz`):
   ```bash
   python3 train.py
   ```

5. **Start the API**:
   ```bash
   uvicorn api:app --reload --port 8000
   ```
   Then in another terminal:
   ```bash
   curl -N -X POST localhost:8000/v1/chat/completions \
     -H "Content-Type: application/json" \
     -d '{"model":"orbit-toy","messages":[{"role":"user","content":"what is your name"}],"stream":true}'
   ```

macOS's built-in `sqlite3` (used for persistent memory/document/conversation
storage) is already sufficient — no extra install needed.

---

## Ubuntu / Linux (including WSL2 on Windows — see below)

1. **Install Python 3.10+ and venv support:**
   ```bash
   sudo apt update
   sudo apt install python3 python3-venv python3-pip -y
   python3 --version
   ```

2. **From the project folder:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Test, train, run** — identical to the macOS steps above:
   ```bash
   python3 -m pytest -q
   python3 train.py
   uvicorn api:app --reload --port 8000
   ```

If `pip install` fails building anything from source (rare — everything
here has prebuilt wheels for standard Linux), run
`sudo apt install build-essential python3-dev` first and retry.

---

## Windows

Two supported paths. **WSL2 is recommended** — it's the same Linux
environment this project was actually developed and tested against, so
it's the lowest-risk option. Native Windows (PowerShell/CMD) also works;
Python itself has no Linux-only dependencies here, just minor command
differences below.

### Option A — WSL2 (recommended)

1. Install WSL2 if you don't have it (from an elevated PowerShell):
   ```powershell
   wsl --install
   ```
   Reboot if prompted, then open the "Ubuntu" app from the Start Menu and
   finish the one-time Linux user setup.

2. Inside the Ubuntu/WSL terminal, follow the **Ubuntu/Linux** instructions
   above exactly (`sudo apt install python3 python3-venv python3-pip`, then
   venv + `pip install -r requirements.txt`).

3. Copy or clone the project into your WSL filesystem (e.g. `~/orbit`)
   rather than accessing it via `/mnt/c/...` — it'll run noticeably faster,
   since cross-filesystem access between Windows and WSL has overhead.

4. `uvicorn api:app --reload --port 8000` inside WSL is reachable from
   Windows at `http://localhost:8000` — WSL2 forwards localhost
   automatically.

### Option B — Native Windows (PowerShell)

1. **Install Python 3.10+** from [python.org](https://www.python.org/downloads/windows/).
   During install, check **"Add python.exe to PATH"**.

2. **From PowerShell, in the project folder:**
   ```powershell
   python -m venv venv
   venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
   If `Activate.ps1` is blocked by execution policy, either run PowerShell
   as Administrator once and allow it:
   ```powershell
   Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
   ```
   or use `venv\Scripts\activate.bat` from Command Prompt (`cmd.exe`)
   instead of PowerShell.

3. **Test, train, run:**
   ```powershell
   python -m pytest -q
   python train.py
   uvicorn api:app --reload --port 8000
   ```

4. `curl` ships with modern Windows 10/11; if yours doesn't have it, use
   PowerShell's `Invoke-RestMethod` instead, or just open
   `http://localhost:8000/health` in a browser for a quick check (that
   endpoint is a simple GET).

---

## Optional: PyTorch backend for faster large-corpus training

`train.py` and `train_large.py` use this project's own from-scratch NumPy
autograd engine (`autograd.py`/`model.py`) -- that engine is the actual
educational point of this project, not an implementation detail to route
around. But it's also genuinely slow at scale: training on even a few MB
of text takes minutes of pure-Python computation. `model_torch.py` /
`train_torch.py` are a PyTorch port of the identical architecture (same
RMSNorm/RoPE/GQA/SwiGLU/tied-embedding design, config-compatible
checkpoints) for when you actually want to train on more of the bundled
corpus (`data/gitenberg_books/`) than the NumPy path can practically get
through — measured directly in this project's own dev environment, roughly
a 13-15x speedup per training step, CPU only (no GPU involved).

```bash
pip install -r requirements-torch.txt   # separate from requirements.txt -- see that file for why
python3 train_torch.py                  # same CLI shape as train_large.py
```

Not installed by default: `torch` is a large dependency most of this
project doesn't need (the API, agents, RAG, memory all work without it).

## Common to all platforms

- **`data/gitenberg_books/`** (the larger public-domain text corpus) is
  included in the project as-is — no download step needed.
- **`train.py`** is fast (a few seconds) and produces the small default
  model. **`train_large.py`** trains on much more of the bundled corpus and
  takes meaningfully longer (see its own docstring for realistic timing);
  run it when you actually want the bigger model, not as part of routine
  setup.
- The API auto-detects whichever trained checkpoint(s) are present
  (`checkpoint_large.npz` preferred, falling back to `checkpoint_base.npz`,
  falling back further to an untrained model) — see `api.py`'s startup
  logic. Check what actually loaded via `GET /health`.
- **Optional PDF/DOCX document support**: already included in
  `requirements.txt` (`pypdf`, `python-docx`). If you deliberately skip
  installing those two, `.txt`/`.md`/`.csv`/`.json` document upload still
  works fine — only PDF/DOCX become unavailable, and the API reports this
  honestly rather than pretending to support them.
- **No GPU, no CUDA, no platform-specific binary dependencies anywhere in
  this project** — it's plain NumPy on CPU, which is also why training runs
  are small-scale (see DESIGN.md / README.md for the honest scope of what
  this prototype can and can't do).
