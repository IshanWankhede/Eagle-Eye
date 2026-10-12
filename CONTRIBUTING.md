# Contributing

## Workflow
1. Read [README.md](README.md), [ARCHITECTURE.md](ARCHITECTURE.md), [PHASE.md](PHASE.md).
2. Branch from `main`: `feat/<short-name>`, `fix/<short-name>`, `docs/<short-name>`.
3. Keep changes within one phase/topic. Do not commit secrets, datasets, model weights, `.env`.
4. Run checks ([TESTING.md](TESTING.md)): `pytest`, `ruff check backend scripts`, `npm run typecheck` in `frontend/`.
5. Use Conventional Commits (`feat(api): ...`, `fix(vision): ...`, `docs: ...`).
6. Open a pull request describing what changed, what was tested, and what was not.

## Style
Python: Ruff (line length 100). TypeScript: strict mode. Architecture rule: `checks/` and `matching/` stay free of I/O, model and web imports.

## Documentation honesty
Mark features as planned/implemented/verified. Never state that something ran if it did not. Never invent dataset facts, licenses or metrics.

## Untracking PROMPT.md
`/PROMPT.md` is in `.gitignore`, but ignoring does not untrack a file Git already tracks. If `PROMPT.md` was committed earlier, run **yourself** (not automated), after committing or stashing other work:
```bash
git rm --cached PROMPT.md
git commit -m "chore: stop tracking local PROMPT.md"
```
`--cached` keeps your local file. It remains in older history; rewriting history is not recommended on shared branches. `PHASE.md` is **not** ignored.

## Security contact
PENDING: add a maintainer contact for vulnerability reports.
