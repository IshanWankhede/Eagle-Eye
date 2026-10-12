# API (proposed contract)

**Only `GET /api/health` exists today.** Everything else is a *proposed* MVP contract. Base path `/api`. JSON unless stated. IDs are UUID strings. Times are ISO-8601 UTC. FastAPI generates live docs at `/docs` once running. No authentication in the MVP (see [SECURITY.md](SECURITY.md)); if added, all endpoints below except health would require it.

## Error envelope (all non-2xx)
```json
{"error": {"code": "VALIDATION_ERROR", "message": "Human-readable text", "details": {}}}
```
Codes: `VALIDATION_ERROR` (422), `NOT_FOUND` (404), `UNSUPPORTED_FILE_TYPE` (415), `FILE_TOO_LARGE` (413), `JOB_ALREADY_ACTIVE` (409), `MODEL_NOT_AVAILABLE` (503), `PROCESSING_FAILED` (500), `INVALID_STATE` (409).

## Enums
`inspection.status`: `CREATED, FILES_UPLOADED, QUEUED, PROCESSING, AWAITING_REVIEW, COMPLETED, FAILED` ([state machine](docs/diagrams/inspection-state-machine.mmd)).
`check.result`: `PASS, FAIL, REVIEW`. `file.kind`: `IMAGE, EXPECTED_TABLE, DRAWING_PDF`. `review.decision`: `PASS, FAIL`.

## MVP endpoints
### GET /api/health — *implemented (scaffold)*
Purpose: liveness + model file check. Response 200: `{"status":"ok","version":"0.1.0","model_loaded":false,"model_file_found":false}`.

### POST /api/inspections — *proposed, P0 (Phase 2)*
Request: `{"cabinet_id":"CAB-001","project_ref":"PRJ-9","inspection_date":"2026-10-12","notes":"optional"}`.
Validation: `cabinet_id` 1–64 chars, required; `project_ref` ≤64; `notes` ≤2000; date not required (defaults today).
Response 201: `{"id":"…","status":"CREATED","cabinet_id":"CAB-001","created_at":"…"}`. Errors: 422.

### GET /api/inspections — *proposed, P0*
Query: `limit` (1–100, default 20), `offset` (default 0). Response 200: `{"items":[{id,cabinet_id,status,created_at,summary:{pass,fail,review}}],"total":N}`, newest first.

### GET /api/inspections/{inspection_id} — *proposed, P0*
Response 200: inspection fields + `files:[{id,kind,original_name,size_bytes}]` + `latest_job`. 404 if unknown.

### POST /api/inspections/{inspection_id}/files — *proposed, P0 (Phase 4)*
`multipart/form-data`: `file` (one file per request), `kind` (`IMAGE`|`EXPECTED_TABLE`|`DRAWING_PDF`).
Validation: extension and sniffed content must match `kind` (IMAGE: jpg/jpeg/png; EXPECTED_TABLE: csv/xlsx; DRAWING_PDF: pdf); size ≤ `MAX_UPLOAD_MB`; non-empty; inspection state must be `CREATED` or `FILES_UPLOADED`.
Response 201: `{"id":"…","kind":"IMAGE","original_name":"cab1.jpg","size_bytes":123456,"parse_summary":{"expected_items":12,"warnings":[]}}` (parse_summary only for tables/PDFs).
Errors: 404, 413, 415, 422 (e.g., missing required CSV columns, with `details.row_errors`), 409 `INVALID_STATE`.

### POST /api/inspections/{inspection_id}/process — *proposed, P0 (Phases 7–8)*
Request: empty body or `{"conf_threshold":0.25}` (optional override within 0.05–0.95).
Behaviour: validates ≥1 image (and an expected table for matching checks), creates a job, returns immediately.
Response 202: `{"job_id":"…","status":"QUEUED"}`. Errors: 409 `JOB_ALREADY_ACTIVE` (duplicate-request protection: one active job per inspection), 409 `INVALID_STATE`, 422 (no images), 503 `MODEL_NOT_AVAILABLE`.
Job states: `QUEUED → RUNNING → SUCCEEDED | FAILED`. Timeout `PROCESSING_TIMEOUT_SECONDS` marks `FAILED` (`error_code: TIMEOUT`). Retry = call `process` again after `FAILED` (new job). MVP: in-process background task; the client polls.

### GET /api/inspections/{inspection_id}/status — *proposed, P0*
Response 200: `{"inspection_status":"PROCESSING","job":{"id":"…","state":"RUNNING","stage":"detection","progress":0.4,"error_code":null,"error_message":null}}`. Poll every 1–2 s.

### GET /api/inspections/{inspection_id}/results — *proposed, P0 (Phase 8–9)*
Response 200:
```json
{"inspection_id":"…","model":{"name":"yolo11n-eagleeye","version":"TBD"},
 "summary":{"pass":8,"fail":1,"review":3},
 "checks":[{"id":"…","rule":"R-001","expected_item_id":"…","result":"REVIEW",
   "reason_code":"LOW_CONFIDENCE","message":"Relay KA1 detected at 0.41 confidence",
   "evidence":[{"id":"…","type":"DETECTION","file_id":"…","bbox":[x,y,w,h],"confidence":0.41}],
   "review":null}],
 "unexpected":[{"class":"relay","confidence":0.83,"file_id":"…","bbox":[0,0,0,0]}]}
```
Errors: 404; 409 `INVALID_STATE` if not yet processed.

### GET /api/inspections/{inspection_id}/evidence/{evidence_id} — *proposed, P0*
Response 200: `image/jpeg` overlay (or `application/json` metadata with `Accept: application/json`). 404 if evidence is not part of this inspection. Path IDs only; no client-supplied paths.

### POST /api/inspections/{inspection_id}/checks/{check_id}/review — *proposed, P1*
Request: `{"decision":"PASS","comment":"Verified visually on photo 2"}` (comment required, 1–2000 chars). Response 201: review record. Original machine result is never overwritten. When all `REVIEW` checks are reviewed the inspection becomes `COMPLETED`.

### GET /api/inspections/{inspection_id}/report — *proposed, P1 (Phase 10)*
Response 200: `application/pdf` (`Content-Disposition: attachment`). 409 if results absent.

### GET /api/model/status — *proposed, P1*
Response 200: `{"loaded":true,"name":"…","version":"…","classes":{"0":"breaker"},"manifest_found":true}`.

## Future endpoints (not in MVP)
`POST /api/inspections/{id}/reinspect` (FR-018, P2) · `DELETE /api/inspections/{id}` (retention) · checklist upload (FR-020) · auth endpoints.

## Consistency notes
Schemas map one-to-one to [DATABASE.md](DATABASE.md) entities; `check.result` and `file.kind` enums are shared by DB, API and UI types; the frontend consumes only these shapes.
