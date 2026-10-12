# Changelog
Format follows Keep a Changelog; versions are pre-release.

## [Unreleased]
### Added
- Documentation package, repository scaffold, Mermaid diagrams.
- FastAPI scaffold with `GET /api/health`; minimal React/Vite page.
- Dataset validator, doc checker, Colab notebook generator and training template.
### Changed (public-dataset plan)
- DATASET.md rewritten around public Roboflow datasets with download links and folder placement; DEMO_INPUTS.md added.
- Validator supports Roboflow layout; `labels_to_expected_csv.py` added; Colab Cell 5 builds a clean YAML.
- Phase 5 reworked (public dataset selection and preparation); R-003 not applicable when tag is empty.
### Fixed
- Removed `hi-wxre3` as the recommended dataset (thermal images); added image-check step and new candidates.
- Recorded Electrical Devices (FieldSnap Pro) as the chosen dataset candidate with group-box caveats.
- Added `scripts/dataset/dedupe_and_resplit.py` after the real Electrical Devices export showed cross-split leakage (23 errors).
### Not yet implemented
- Uploads, parsing, detection, OCR, matching, rules, review, reports, trained model.
