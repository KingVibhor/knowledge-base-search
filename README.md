# knowledge-base-search

## Full setup (Windows) — enable Chromadb backend

This project includes an in-memory fallback for development, but to get full functionality (Chromadb with HNSW indexing) on Windows you should use a Conda environment with Python 3.10 or 3.11 to avoid native build failures.

Steps (recommended):

1. Install Miniconda or Anaconda: https://docs.conda.io/en/latest/miniconda.html
2. Create and activate a conda environment with Python 3.10:

```powershell
conda create -n kb-full python=3.10 -y
conda activate kb-full
```

3. Install a binary `numpy` and `pip` from conda-forge to avoid building from source:

```powershell
conda install -c conda-forge numpy pip -y
```

4. Install Python requirements (this will install `chromadb` and other packages):

```powershell
pip install -r requirements.txt
```

5. Start the server:

```powershell
uvicorn backend.app:app --reload
```

Notes:
- If you prefer not to use conda, you can still run the app locally with the in-memory fallback (already added) — this avoids `chromadb` and HNSW native builds.
- If you want, run the provided helper script `scripts/setup_conda_env.ps1` (requires conda installed) to automate the steps.