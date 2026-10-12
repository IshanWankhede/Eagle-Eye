# Product Requirements Document — Eagle Eye

Status: draft for review. Requirement IDs refer to [REQUIREMENTS.md](REQUIREMENTS.md). Terms: [GLOSSARY.md](GLOSSARY.md).

> **Scope note.** The original competition problem statement was not supplied. This PRD is built from the *working problem definition* given by the project owner. Items are labelled **Working definition**, **Assumption**, **Proposed requirement** or **Optional enhancement**. Nothing here is claimed to be an official competition requirement.

## 1. Executive summary
Eagle Eye is a proposed software-assisted workflow that helps an inspector compare a control cabinet's *expected* engineering configuration against its *visible* condition in photographs. It organises evidence, flags possible discrepancies, and produces a report. It supports the inspector; it does not replace them. (Working definition)

## 2. Background and problem statement
Cabinet inspection can involve comparing photos with drawings, component lists, wiring information, labels and inspection rules. The work is slow, hard to standardise, and leaves inconsistent evidence. Failures are hard to explain and inspections are hard to compare over time. (Working definition)

## 3. User personas
- **Inspector (primary):** checks cabinets on a shop floor or in an office; wants fast, clear evidence and the final say.
- **QC lead (secondary):** wants consistent results, history and reports.
- **Developer/maintainer (internal):** swaps models, adds rules, extends parsers.

## 4. Existing workflow and pain points
Manual comparison of photos to lists: time-consuming, subjective, evidence scattered, hard to re-check. (Assumption: no existing digital system is available.)

## 5. Proposed solution
Create inspection → upload photos + expected-configuration files → parse expected items → detect and OCR → match → apply rules → review uncertain items → store → report. Full detail: [SYSTEM_WORKFLOW.md](SYSTEM_WORKFLOW.md).
Plain-language idea: *expected* (what the document says) vs *observed* (what the camera model sees) vs *decision* (what a rule and then a human conclude).

## 6. Product objectives
1. Deliver one credible end-to-end inspection flow for a hackathon demo.
2. Make every result explainable with evidence.
3. Be honest about uncertainty (`REVIEW`).
4. Keep the model replaceable.

## 7. Measurable success criteria (proposed targets, not achieved results)
| Metric | Proposed target | How measured |
|---|---|---|
| End-to-end flow works on a demo inspection | Yes/No | Demo script (Phase 12) |
| Every check has at least one evidence reference or an explicit reason code | 100% | Automated test |
| Detector quality on held-out cabinet test set | Set after baseline; see [MODEL_EVALUATION.md](MODEL_EVALUATION.md) | Ultralytics validation on test split |
| Unsupported checks never return PASS | 100% | Rule tests |
| Setup from clean clone | 30 minutes or less | Manual timing |

## 8. Functional requirements
See FR-001 to FR-020 in [REQUIREMENTS.md](REQUIREMENTS.md). Summary: create/list inspections; upload images and CSV/XLSX (PDF best-effort); validate; process asynchronously; detect; OCR; normalise; match; rules; evidence; review; history; report.

## 9. Non-functional requirements
See NFR-001 to NFR-010: traceability, safe files, env config, replaceable model, testable rules, local-first privacy, accessibility baseline, reproducibility, doc consistency.

## 10. MVP scope
In: FR-001–004, 006–008, 010–014, 016 (P0) and, if time permits, FR-005, 009, 015, 017, 019 (P1). Supported inputs: JPEG/PNG; CSV/XLSX with the documented columns; text-based PDF (best effort, P1). Rules R-001 to R-006 (R-006 always `REVIEW`).

## 11. Out of scope (MVP)
Arbitrary CAD files; scanned-drawing interpretation; arbitrary Excel layouts; terminal-level wiring verification; pixel comparison of drawings vs photos; authentication/roles; multi-user collaboration; production certification; mobile app; real-time video.

## 12. User journeys
**Journey A (happy path):** Inspector creates inspection → uploads 4 photos and an expected CSV → clicks Process → sees progress → opens results → checks are PASS or REVIEW → reviews REVIEW items → downloads report.
**Journey B (model uncertain):** Detector returns low confidence for a relay → check = REVIEW with box and score → inspector confirms or rejects.
**Journey C (bad input):** Inspector uploads a `.dwg` → rejected with a clear message listing supported formats.

## 13. User stories
- As an inspector, I want to upload photos and a component list so I do not compare them by hand. (FR-003/004)
- As an inspector, I want each result to show the image evidence so I can trust or challenge it. (FR-014)
- As an inspector, I want uncertain items marked REVIEW so the tool never bluffs. (FR-012/013)
- As a QC lead, I want past inspections so I can compare over time. (FR-016/018)
- As a maintainer, I want to drop in a new `best.pt` so retraining does not require code changes. (NFR-004)

## 14. Acceptance criteria
Per-requirement criteria are in [REQUIREMENTS.md](REQUIREMENTS.md). MVP acceptance: the demo script in Phase 12 runs end to end on authorised sample data, and all P0 tests pass.

## 15. Constraints
Hackathon time; student developer; Colab for training; Windows-first development; no confidential data on third-party services without authorisation.

## 16. Risks
See [RISK_REGISTER.md](RISK_REGISTER.md). Top: no suitable cabinet dataset; model underperforms; PDF variability; time overrun.

## 17. Assumptions
Detailed in [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md). Key: expected configuration is available as a table; target classes are a small set (e.g., breaker, relay, terminal block, illustrative); photos are taken reasonably frontally.

## 18. Dependencies
Authorised cabinet photos and documents; annotation tool; Google Colab GPU; Ultralytics, FastAPI, React ecosystems; verified licenses ([THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)).

## 19. Future enhancements
Reinspection diff; checklist upload; layout/position checks using zones; terminal-level evidence with specialised models; authentication; PostgreSQL; ONNX export; scanned-drawing OCR; multi-photo stitching.
