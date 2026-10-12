# GitHub workflow
- `main` is always runnable. Work on short-lived branches; open PRs; CI ([.github/workflows/ci.yml](../../.github/workflows/ci.yml)) runs lint, tests, frontend typecheck/build (CI has not been run yet).
- First push: `git init`, `git add .`, review `git status` (no `.env`, weights, datasets, `PROMPT.md`), commit, create the GitHub repo, `git remote add origin <url>`, `git push -u origin main`.
- Never force-push shared branches or rewrite history without agreement. Large files: keep out of Git.
- `PROMPT.md` stays local (git-ignored); `PHASE.md` is committed.
