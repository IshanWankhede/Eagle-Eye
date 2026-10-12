# Requirements Traceability

Requirements are **internally defined** (see [REQUIREMENTS.md](REQUIREMENTS.md)); there are no official competition-document citations. "Phase" refers to [PHASE.md](PHASE.md). Endpoint names are **proposed** ([API.md](API.md)). Test files are **planned**.

| Req | PRD section | Architecture component | API endpoint | DB entity | Planned test | Phase |
|---|---|---|---|---|---|---|
| FR-001 | 8 Functional | api, services, database | POST /api/inspections | inspections | backend/tests/test_inspections_api.py | 2 |
| FR-002 | 8 | api, database | GET /api/inspections, GET /api/inspections/{id} | inspections | test_inspections_api.py | 2 |
| FR-003 | 8 | api, storage | POST /api/inspections/{id}/files | uploaded_files | test_uploads.py | 4 |
| FR-004 | 8 | parsers | POST .../files | uploaded_files, expected_items | test_parsers_tabular.py | 4 |
| FR-005 | 8 | parsers | POST .../files | expected_items | test_parsers_pdf.py | 4 |
| FR-006 | 8, 9 NFR | storage, api | POST .../files | uploaded_files | test_upload_security.py | 4 |
| FR-007 | 8 | services (job runner) | POST .../process, GET .../status | processing_jobs | test_processing_jobs.py | 7–8 |
| FR-008 | 8 | vision | (internal), GET /api/model/status | detected_objects | test_detector.py | 7 |
| FR-009 | 8 | ocr | (internal) | ocr_observations | test_ocr.py | 7 |
| FR-010 | 8 | matching | (internal) | expected_items | test_normalization.py | 8 |
| FR-011 | 8 | matching | GET .../results | qc_checks | test_matching.py | 8 |
| FR-012 | 8 | checks | GET .../results | qc_checks | test_rules.py | 8 |
| FR-013 | 8 | checks | GET .../results | qc_checks | test_rules_wiring.py | 8 |
| FR-014 | 8 | storage, services | GET .../evidence/{evidence_id} | evidence | test_evidence.py | 9 |
| FR-015 | 8 | api, database | POST .../checks/{check_id}/review | inspector_reviews | test_review.py | 9 |
| FR-016 | 8 | database | GET /api/inspections | inspections | test_persistence.py | 2, 9 |
| FR-017 | 8 | reporting | GET .../report | reports | test_report.py | 10 |
| FR-018 | 8 (future) | services | POST .../reinspect | inspections (parent link) | test_reinspect.py | deferred |
| FR-019 | 8 | vision, api | GET /api/model/status | — | test_model_status.py | 7 |
| NFR-001 | 9 | services, database | all results endpoints | evidence | test_evidence.py | 9 |
| NFR-002 | 9 | storage | files | uploaded_files | test_upload_security.py | 4, 11 |
| NFR-003 | 9 | core | — | — | test_config.py | 1–2 |
| NFR-004 | 9 | vision | GET /api/model/status | — | test_model_loading.py | 7 |
| NFR-006 | 9 | checks, matching | — | — | test_rules.py | 8 |
| NFR-009 | 9 | scripts, models | — | — | manifest review | 6 |
