# Uploading the full ORBIT tree

The GitHub API path used by the assistant uploads files in small batches.
For a **complete** sync from your project machine:

```bash
# 1. Clone the repo
git clone https://github.com/John433-max/ORBIT-AI.git
cd ORBIT-AI

# 2. Copy the full local tree (exclude weights / caches)
# From the Grok project folder:
rsync -av --exclude '.pytest_cache' --exclude '__pycache__' \
  --exclude '*.npz' --exclude '.orbit_data' --exclude '*.db' \
  /path/to/artifacts/orbit/ ./

# 3. Commit and push
git add -A
git commit -m "Full ORBIT source tree"
git push origin main
```

Or unzip `artifacts/ORBIT-AI-source.zip` over the clone and push.

Large `.npz` checkpoints are intentionally gitignored.
