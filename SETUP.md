# Running ORBIT on Windows, macOS, and Ubuntu/Linux

ORBIT is pure Python + NumPy with no compiled extensions and no GPU
requirement, so setup is the same shape on every platform: get Python 3.10+,
create a virtual environment, install `requirements.txt`, run.

Tested during development against **Python 3.12** on Linux. Python 3.10 or
newer should work; anything older is untested and not recommended.

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

4. **Train the default small model**:
   ```bash
   python3 train.py
   ```

5. **Start the API**:
   ```bash
   uvicorn api:app --reload --port 8000
   ```

---

## Ubuntu / Linux (including WSL2)

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

3. **Test, train, run:**
   ```bash
   python3 -m pytest -q
   python3 train.py
   uvicorn api:app --reload --port 8000
   ```

---

## Windows

### Option A — WSL2 (recommended)

1. Install WSL2 from elevated PowerShell: `wsl --install`
2. Inside Ubuntu/WSL, follow the Ubuntu/Linux instructions above.
3. Prefer the WSL filesystem (`~/orbit`) over `/mnt/c/...`.
4. API is reachable from Windows at `http://localhost:8000`.

### Option B — Native Windows (PowerShell)

1. Install Python 3.10+ from python.org (check "Add to PATH").
2. From the project folder:
   ```powershell
   python -m venv venv
   venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   python -m pytest -q
   python train.py
   uvicorn api:app --reload --port 8000
   ```

---

## Optional: PyTorch backend

```bash
pip install -r requirements-torch.txt
python3 train_torch.py
```

Not installed by default — API, agents, RAG, and memory work without it.

## Common notes

- Optional PDF/DOCX support via `pypdf` / `python-docx` in requirements.txt.
- No GPU/CUDA required — CPU-first NumPy path.
