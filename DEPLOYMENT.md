# Deployment

Nothing is deployed. This describes realistic options. See [deployment.mmd](docs/diagrams/deployment.mmd).

## Local development
Vite dev server (5173) + Uvicorn (8000) + SQLite file + local upload folder + weights in `models/custom/`.

## Hackathon demo (recommended)
Run everything on one laptop (ideally the one with the demo data). Build the frontend (`npm run build`) and either serve `frontend/dist` with any static server or keep the dev server. Pre-load a demo inspection; keep a backup screen recording. This avoids uploading confidential data to the internet and removes network risk.
- **Persistence:** SQLite file in `artifacts/`. **Files:** local folder. **Models:** local `best.pt` + manifest.
- **Env vars:** from `.env` ([.env.example](.env.example)). **Logs:** stdout (`LOG_LEVEL`). **Health:** `GET /api/health`.
- **Resource constraints:** CPU inference speed unmeasured; test the demo machine beforehand; keep images moderate (resize on upload if needed).

## Optional cloud demo (unverified, not planned for MVP)
Frontend on a static host; backend in a container on a VM/PaaS with a persistent volume. Requires: authentication, HTTPS, upload limits, retention policy, and explicit approval for any confidential data. Free tiers may lack RAM for PyTorch.

## Production considerations (future)
PostgreSQL; object storage; task queue + worker pool; GPU or ONNX runtime; model registry; structured logging and metrics; authentication/authorisation; backups; dependency scanning; model/rule version audit trail; legal review of Ultralytics AGPL-3.0 vs enterprise license.
