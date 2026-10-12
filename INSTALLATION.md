# Installation (Windows-first)

Status: commands match files in this repo but were **not executed** by the scaffold author (no package network access). Expect to fix minor version issues on first run and then pin versions. No trained checkpoint is assumed.

## 1. Prerequisites
- **Git** (https://git-scm.com), **Python 3.10+** (3.11 recommended; tick "Add python.exe to PATH"), **Node.js 20 LTS** (https://nodejs.org).
Check: `python --version; node --version; npm --version; git --version`.

## 2. Backend (PowerShell)
```powershell
cd eagle-eye
python -m venv .venv
.\.venv\Scripts\Activate.ps1          # if blocked: Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload --app-dir backend
```
Open http://127.0.0.1:8000/api/health and http://127.0.0.1:8000/docs.
Later phases: `pip install -e ".[docs]"` (parsers, reports) and `pip install -e ".[ml]"` (YOLO, OpenCV, EasyOCR; large download).

## 3. Frontend
```powershell
cd frontend
npm install
npm run dev        # http://localhost:5173 (proxies /api to port 8000)
```

## 4. Database initialisation
Not implemented yet. From Phase 2 the app creates the SQLite file at `DATABASE_URL` (default `./artifacts/eagle_eye.sqlite3`) on startup / via Alembic.

## 5. Model checkpoint placement
Place `best.pt` and `model_manifest.json` in `models/custom/` ([MODEL_TRAINING.md](MODEL_TRAINING.md)). **Missing-model behaviour:** the backend starts normally; `/api/health` shows `model_file_found: false`; once implemented, detection requests return `MODEL_NOT_AVAILABLE`.

## 6. macOS / Linux differences
```bash
python3 -m venv .venv && source .venv/bin/activate
cp .env.example .env
uvicorn app.main:app --reload --app-dir backend
```
Paths use `/`. On Linux, installing OpenCV/PyTorch GPU builds may need system libraries; use `opencv-python-headless` (already the choice).

## 7. Troubleshooting
See [TROUBLESHOOTING.md](TROUBLESHOOTING.md).
