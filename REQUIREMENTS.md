# Requirements

These are **internally defined project requirements** derived from the working problem definition in [PRD.md](PRD.md). They are *not* citations of an official competition document. Priority: **P0** = required for the MVP, **P1** = should have if time permits, **P2** = optional enhancement.

## Functional requirements
| ID | Pri | Requirement | Acceptance criteria |
|---|---|---|---|
| FR-001 | P0 | Create an inspection with cabinet ID, project ref, date, notes | `POST /api/inspections` returns 201 with an ID; missing cabinet ID returns 422 |
| FR-002 | P0 | List and view inspections (history) | List returns newest first; detail returns status, files, summary counts |
| FR-003 | P0 | Upload cabinet photos (JPEG, PNG) | Valid image stored; wrong type or oversize rejected with 415/413 |
| FR-004 | P0 | Upload expected-configuration table (CSV, XLSX) following the documented column schema | Rows parsed to `ExpectedItem`; bad schema returns a row-level error list |
| FR-005 | P1 | Best-effort text/table extraction from text-based PDFs | Selectable-text PDF yields text with page refs; scanned PDF is flagged "unsupported", not guessed |
| FR-006 | P0 | Validate files (extension, MIME sniffing, size, safe names) | Tests cover traversal names, wrong extension, empty file, oversize |
| FR-007 | P0 | Start asynchronous processing and poll job status | `POST .../process` returns 202 + job; duplicate request while active returns 409; status endpoint shows state |
| FR-008 | P0 | Detect components with class, confidence, bounding box | Each detection stored with model version; missing model yields a clear `MODEL_NOT_AVAILABLE` error |
| FR-009 | P1 | OCR on images for label/tag text | OCR observations stored with text, confidence, box |
| FR-010 | P0 | Normalize expected and observed data to shared class vocabulary | Class alias map is configuration, unit-tested |
| FR-011 | P0 | Match expected items to observations | Matching output lists matched, missing-candidate, unexpected-candidate items |
| FR-012 | P0 | Evaluate deterministic rules producing PASS / FAIL / REVIEW with reason codes | Rule tests cover each outcome per rule |
| FR-013 | P0 | Unsupported or insufficient-evidence checks (e.g., terminal-level wiring) return REVIEW | Wiring rule never returns PASS from photo evidence alone |
| FR-014 | P0 | Store and display evidence (source image, box, rule, confidence) per check | Evidence endpoint returns image with overlay or box metadata |
| FR-015 | P1 | Inspector can confirm/override REVIEW and FAIL items with a comment | Review record stores user, time, decision, comment; original machine result unchanged |
| FR-016 | P0 | Persist inspections so history survives restart | Restart test retrieves prior inspection |
| FR-017 | P1 | Generate downloadable PDF report | Report lists checks, statuses, evidence, model version, review decisions |
| FR-018 | P2 | Reinspection creating a new run linked to the previous one | Prior run preserved; diff view optional |
| FR-019 | P1 | Show model status/version in UI and health | `GET /api/model/status` returns name, version, classes, loaded flag |
| FR-020 | P2 | Optional checklist upload | Out of MVP |

## Rules (implemented by `backend/app/checks/`, referenced by FR-012/FR-013)
| Rule | Name | Outcome logic (summary) |
|---|---|---|
| R-001 | Component presence | Expected class has ≥1 accepted detection → PASS; none and image quality good and class supported → REVIEW (non-detection is not proof) unless policy sets FAIL; low-confidence only → REVIEW |
| R-002 | Component count | Accepted count equals expected quantity → PASS; accepted count greater → FAIL candidate flagged for review; fewer → REVIEW |
| R-003 | Label text match | Expected `tag` empty → rule **not applicable** (no check created); OCR text matches expected tag (after normalization) → PASS; clear different text → FAIL; unreadable/absent → REVIEW |
| R-004 | Unexpected component | High-confidence detection of class not in expected list → REVIEW (or FAIL by policy) |
| R-005 | Image quality gate | Blur/brightness/resolution below threshold → REVIEW for dependent rules |
| R-006 | Wiring connectivity | **Unsupported in MVP** → always REVIEW |
Exact FAIL-vs-REVIEW policy is an assumption: see [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md) (Q-004).

## Non-functional requirements
| ID | Pri | Requirement | Acceptance |
|---|---|---|---|
| NFR-001 | P0 | Every output traceable to source file, stage, rule and model version | Evidence records populated for all checks |
| NFR-002 | P0 | Safe file handling per [SECURITY.md](SECURITY.md) | Security tests pass |
| NFR-003 | P0 | Config via environment variables | No hard-coded paths/secrets; `.env.example` complete |
| NFR-004 | P0 | Model replaceable without code changes | Swap `best.pt` + manifest only |
| NFR-005 | P1 | Proposed target: process a small inspection (≤10 images) within the configured timeout on demo hardware | **Unmeasured target**; measure in Phase 11 |
| NFR-006 | P0 | Business rules testable without model or HTTP | Rules unit-tested with fixtures |
| NFR-007 | P0 | Local-first data handling; no third-party upload of confidential data | Documented; no external API calls in MVP |
| NFR-008 | P1 | Accessible, responsive UI baseline (labels, keyboard focus, contrast) | Manual checklist |
| NFR-009 | P0 | Reproducible training with manifest | Manifest complete for the shipped model |
| NFR-010 | P0 | Docs consistent with implementation | `check_docs.py` passes; status labels honest |

## Expected-configuration CSV schema (MVP)
Columns: `item_id, component_class, tag, quantity, zone, notes` (`zone`/`notes` optional). Example: [data/samples/expected_components.example.csv](data/samples/expected_components.example.csv) (fictional).
