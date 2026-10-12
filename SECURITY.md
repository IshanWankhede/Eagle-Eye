# Security

Status of controls: **all items below are proposed** unless marked implemented; **no authentication or authorisation exists**. The MVP is for local/demo use on a trusted machine. Related: [ARCHITECTURE.md](ARCHITECTURE.md#9-security-boundaries).

## File uploads (untrusted input)
- Allow-list extensions (`.jpg .jpeg .png .pdf .csv .xlsx`), **and** verify content (magic bytes / successful decode), not just the extension or client MIME type.
- Size cap `MAX_UPLOAD_MB` (default 25), enforced while streaming; reject empty files.
- Limit images per inspection and image pixel count (decompression-bomb protection; set Pillow/OpenCV limits).
- Store with **server-generated names** (`<file_id>.<ext>`); keep original name as metadata only, sanitised for display.
- **Path traversal:** never join user-supplied strings into paths; resolve and assert the final path is inside `UPLOAD_DIR`. Evidence/report endpoints take IDs, not paths.
- Parsing risks: PDFs and XLSX can be malformed or malicious. Parse in the backend process with bounded size/time; disable macros (openpyxl does not run them); treat parser exceptions as `422`. Consider running parsing in a subprocess later.
- Uploaded files are never executed or served back from a static directory.

## Secrets and configuration
Environment variables / `.env` (git-ignored). `.env.example` has no real values. Never put Roboflow or other keys in notebooks or Git; use Colab Secrets.

## API behaviour
Consistent error envelope; no stack traces or file-system paths in responses; CORS restricted to configured origins; request-size limits at the server. Add rate limiting if ever exposed beyond localhost.

## Access control
None in the MVP. If deployed beyond a single trusted user, add authentication, per-user ownership of inspections, and audit of reviews. Do not expose the MVP to the internet.

## Sensitive engineering documents
Cabinet photos and engineering documents may be confidential. Use only with authorisation; keep on local/approved storage; avoid third-party upload (Colab/Drive/Roboflow) unless explicitly approved.

## Retention and deletion
No automatic retention in MVP. Provide a documented manual procedure that deletes DB rows and associated files together; future `DELETE /api/inspections/{id}`. Do not keep real data in the repository.

## Dependencies and model artifacts
Run `pip audit` / `npm audit` periodically and before the demo; pin versions after first install. Treat `.pt` files as **code-equivalent** (PyTorch checkpoints can execute code when unpickled): load only checkpoints you trained or obtained from a trusted source, record SHA-256 and provenance in the manifest, never load weights from user uploads.

## Reporting a vulnerability
Open a private issue or contact the maintainer (PENDING: define contact in [CONTRIBUTING.md](CONTRIBUTING.md)).
