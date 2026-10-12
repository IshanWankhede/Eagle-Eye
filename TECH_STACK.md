# Technology Stack

Version ranges below are minimums from `pyproject.toml` / `frontend/package.json`. **They have not been install-tested in this scaffold** (no network access was available when generating it). Pin exact versions after the first successful install (`pip freeze`, `package-lock.json`).

| Technology | What / why | Alternatives considered |
|---|---|---|
| React + TypeScript + Vite | Fast dev loop, typed UI | Next.js (SSR unnecessary), Vue |
| Tailwind CSS (v4 via `@tailwindcss/vite`) | Utility styling, leaves visual design open | CSS modules |
| shadcn/ui (add in Phase 3) | Accessible components copied into repo | Radix directly, MUI |
| React Router, a typed fetch client, a form-validation library (e.g., Zod + React Hook Form) — chosen in Phase 3 | Routing, typed API, validation | TanStack Router/Query |
| Python 3.10+ (3.11 recommended) | ML ecosystem | — |
| FastAPI + Pydantic + Uvicorn | Typed API, auto docs | Flask, Django |
| SQLAlchemy 2 + SQLite (+ Alembic later) | Zero-setup persistence, migration path | Raw sqlite3, Postgres from day one |
| Ultralytics YOLO | Detection training/inference; docs show `yolo11n.pt` and newer `yolo26n.pt` ([docs](https://docs.ultralytics.com/compare/yolo11-vs-yolo26/)) | RT-DETR, torchvision models |
| OpenCV (headless) | Image quality metrics, drawing overlays | Pillow only |
| EasyOCR (baseline, Phase 7 spike) | pip-installable OCR | PaddleOCR (strong but heavier install on Windows; unverified here), Tesseract |
| PyMuPDF (pymupdf) | PDF text/table extraction | pdfplumber (pure Python; consider if PyMuPDF licensing is a concern — PyMuPDF is AGPL/commercial, verify) |
| pandas + openpyxl | CSV/XLSX parsing | csv module + openpyxl directly |
| ReportLab | PDF reports | WeasyPrint, HTML-to-PDF |
| pytest, httpx, Ruff | Tests, API tests, lint+format | unittest, Black+flake8 |
| Google Colab | Free GPU for training | Kaggle notebooks, local GPU |

## Optional components / install groups
`pip install -e ".[dev]"` tests; `".[docs]"` parsers + reports (Phase 4/10); `".[ml]"` YOLO, OpenCV, EasyOCR (Phase 7). `ml` pulls PyTorch transitively; for GPU builds follow PyTorch's official selector.

## Why two Python manifests?
`pyproject.toml` is the source of truth. `requirements.txt` mirrors core runtime deps for simple `pip install -r`; `requirements-dev.txt` adds test tools. Keep them in sync when editing. The frontend has its own `frontend/package.json`; there is **no** root Node manifest.

## Reproducibility
Commit lock files after first install; record Python/Node versions; record training software versions in the model manifest ([MODEL_TRAINING.md](MODEL_TRAINING.md)).
