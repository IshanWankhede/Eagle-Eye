# Local development workflow
1. `git pull`; create a branch ([github-workflow.md](github-workflow.md)).
2. Activate venv; `pip install -r requirements-dev.txt`; copy `.env.example` to `.env`.
3. Run backend (`uvicorn app.main:app --reload --app-dir backend`) and frontend (`cd frontend; npm run dev`).
4. Implement one phase task; add tests next to it.
5. Before committing: `pytest`, `ruff check backend scripts`, `npm run typecheck`, `python scripts/utilities/check_docs.py`.
6. Commit with a Conventional Commit message. Setup details: [INSTALLATION.md](../../INSTALLATION.md).
