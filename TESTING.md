# Testing Strategy

Commands below refer to files that exist now (`backend/tests/test_health.py`, config files). Other test files are **planned** (see [REQUIREMENTS_TRACEABILITY.md](REQUIREMENTS_TRACEABILITY.md)). No tests were executed while generating this scaffold (dependencies could not be installed offline); see [FINAL_REVIEW.md](FINAL_REVIEW.md).

## Commands
```powershell
pytest                                   # all Python tests (config in pyproject.toml)
ruff check backend scripts               # lint
ruff format --check backend scripts      # formatting
cd frontend; npm run typecheck; npm run build
python scripts/utilities/check_docs.py   # doc links + Mermaid first-line check
python scripts/dataset/validate_yolo_dataset.py --root <dataset> --nc <N>
```

## Test types
| Type | What | Tooling | Notes |
|---|---|---|---|
| Unit: rules/matching | R-001…R-006, normalisation, matching edge cases | pytest, plain data fixtures | No model, DB or HTTP needed (NFR-006) |
| Unit: parsers | CSV/XLSX schema errors, row errors; PDF text extraction | pytest + small fixture files | Include malformed and empty files |
| API | status codes, validation, error envelope | FastAPI `TestClient` (httpx) | Temp DB + temp upload dir |
| File upload / security | traversal names, wrong ext, spoofed content, oversize, empty | pytest | Required before demo |
| Model inference | detector wrapper with a **fake detector** for logic; a tiny real-weights test marked `@pytest.mark.model` skipped if weights absent | pytest markers | Never require weights in CI |
| Integration | upload → process → results with fake detector | pytest | |
| Failure/timeout | missing model, parser exception, job timeout, duplicate process request, restart recovery | pytest | |
| Frontend | type-check + build (CI); component tests with Vitest + Testing Library added in Phase 3 | npm | Choose tools in Phase 3 |
| End-to-end MVP | demo script on authorised sample data (manual first; Playwright optional) | manual / Playwright | Phase 12 |
| Security checks | `pip audit`, `npm audit`, secret scan (e.g., gitleaks) | CLI | |
| Performance | latency per image, memory, total job time vs timeout | script in `scripts/evaluation/` | Report hardware |

## Acceptance criteria (examples)
- Unsupported check never returns `PASS` (test asserts on R-006 for any input).
- Upload of `../../x.png` is stored under a generated name; no file is written outside `UPLOAD_DIR`.
- Second `process` call while a job is active returns 409.
- With no model file, `process` returns 503 `MODEL_NOT_AVAILABLE` and health reports `model_file_found: false`.
- Every `qc_check` has ≥1 evidence row or `reason_code` explaining absence.

## Principles
Test pure logic heavily, I/O lightly; use fixtures not real confidential data; keep tests deterministic; do not claim a check passed unless it was run.
