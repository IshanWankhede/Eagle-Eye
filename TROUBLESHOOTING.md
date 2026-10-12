# Troubleshooting

| Area | Symptom | Likely cause / fix |
|---|---|---|
| Python | `python` not found | Reinstall with "Add to PATH" or use `py -3` |
| venv | `Activate.ps1` blocked | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| venv | Wrong packages imported | Confirm `(.venv)` prompt; `where python` |
| pip | Build errors / incompatible versions | Upgrade pip; use Python 3.10–3.12; install `[ml]` in a fresh venv; pin after success |
| Node | `npm install` fails | Use Node 20 LTS; delete `node_modules` and retry |
| FastAPI | `ModuleNotFoundError: app` | Run `uvicorn app.main:app --app-dir backend` from repo root |
| FastAPI | Port in use | `--port 8001` and update the Vite proxy |
| CORS | Browser blocks requests | Add the UI origin to `CORS_ALLOWED_ORIGINS`; use the Vite `/api` proxy |
| Uploads | 413 / 415 | Check `MAX_UPLOAD_MB`, extension allow-list |
| Uploads | `python-multipart` error | `pip install python-multipart` |
| PDF | No text extracted | Scanned PDF: unsupported in MVP; supply CSV/XLSX |
| CUDA | `torch.cuda.is_available()` False | CPU torch installed; use matching PyTorch CUDA build; Colab: select GPU runtime |
| Colab | Disconnected | Save runs to Drive; resume with `resume=True` ([MODEL_TRAINING.md](MODEL_TRAINING.md)) |
| YOLO | `best.pt` not found | Look under your `project/name/weights/`; check the training log for the save dir |
| YOLO | Class names differ from manifest | Regenerate manifest from the same run; do not edit names by hand |
| YOLO | Pickle / weights load error | Ultralytics version mismatch; install the version used to train (in manifest) |
| Git | `.env` or weights staged | `git rm --cached <file>`; check `.gitignore` |
| Git | Large file rejected | Remove it from history *before* pushing (ask for help; do not rewrite shared history); keep weights/datasets out of Git |
| Git | `PROMPT.md` already tracked | See [CONTRIBUTING.md](CONTRIBUTING.md#untracking-promptmd) |
| Data | Validator reports LEAKAGE errors | Run `scripts/dataset/dedupe_and_resplit.py`, re-validate, train on the output |
