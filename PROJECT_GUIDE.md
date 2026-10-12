# Eagle Eye Project Guide (for students)

Read this first. After it you should be able to explain the project in a technical review. Terms are defined in [GLOSSARY.md](GLOSSARY.md). Status: the design is documented; only a health endpoint exists.

## 1. What Eagle Eye does and why
Checking a control cabinet means comparing what is *supposed* to be there (drawings, component lists) with what is *actually* there (photos). People do this by eye, which is slow and inconsistent. Eagle Eye is a tool that does the first pass and shows its evidence, so the inspector can focus on the doubtful items. **It assists; the inspector decides.**

## 2. The workflow in one picture
```text
Photos + expected list ──► detect (YOLO) + read text (OCR) ──► compare with expected ──► rules ──► PASS / FAIL / REVIEW ──► inspector ──► report
```
Detailed steps: [SYSTEM_WORKFLOW.md](SYSTEM_WORKFLOW.md).

## 3. What the user uploads
(Practical demo inputs built from a public dataset: see [DEMO_INPUTS.md](DEMO_INPUTS.md).)
1. **Photos** of the cabinet (JPEG/PNG).
2. **An expected-configuration table** (CSV or Excel), e.g. "one breaker tagged QF1, two relays, twelve terminal blocks". (Fictional example: [data/samples/expected_components.example.csv](data/samples/expected_components.example.csv)).
3. Optionally a **PDF** (text-based only, best effort).
Not supported: CAD files, scanned drawings, arbitrary spreadsheets.

## 4. How YOLO works (simple version)
YOLO is a neural network that looks at a photo once and outputs boxes: "class = breaker, confidence 0.91, here". It learned by seeing many labelled examples. It does **not** understand drawings, prove wiring, or decide quality. Details: [MODEL.md](MODEL.md).

## 5. What OCR does
OCR reads text in an image (e.g., a label "QF1"). Reading the tag lets us check *which* breaker it is, not just *that* it is a breaker.

## 6. Why documents are parsed separately
A drawing and a photo are completely different kinds of images; comparing pixels is meaningless. Instead we extract **structured data** from the documents (a list of expected items) and compare it with structured data from the photos (detections + text).

## 7. Expected vs observed
- **Expected item:** `{class: breaker, tag: QF1, quantity: 1}` from the table.
- **Observed item:** `{class: breaker, confidence: 0.91, box: …, text: "QF1"}` from the image.
- **Matching** pairs them (class first, then tag text).
- **Rules** judge the pair.
- **Human decision** settles doubtful cases.

## 8. PASS, FAIL, REVIEW
- **PASS:** the evidence clearly agrees with the expectation.
- **FAIL:** the evidence clearly disagrees.
- **REVIEW:** not enough or unsupported evidence — a human must look. Example: terminal-level wiring can't be proven from a photo, so that check is always REVIEW.
Why separate them? A tool that bluffs a PASS is dangerous; REVIEW keeps it honest. Also, *not detecting* something is not proof it is missing (it may be hidden or blurry).

## 9. How the parts communicate
Browser (React) ⇄ HTTP/JSON ⇄ FastAPI backend → services → [parsers, YOLO detector, OCR, matching, rules] → SQLite database (records) + upload folder (images/evidence). The model is a file (`best.pt`) loaded by the backend; the frontend never touches it. See [ARCHITECTURE.md](ARCHITECTURE.md).

## 10. Folder tour
`frontend/` UI · `backend/app/api` routes · `schemas` data shapes · `services` orchestration · `parsers` documents · `vision` detector · `ocr` text reading · `matching` pairing · `checks` rules · `database` storage of records · `storage` files · `reporting` reports · `data/` datasets · `models/` weights · `notebooks/` Colab · `scripts/` helper tools · `docs/` diagrams.

## 11. Data flow example
Upload 3 photos + CSV → the CSV becomes 4 expected rows → each photo is checked for quality → YOLO finds objects → OCR reads tags → matching pairs "breaker QF1" → rule R-001 says PASS; relay KA2 was detected at 0.41 confidence → R-001 says REVIEW → inspector confirms → report.

## 12. When the model is uncertain
Detections below the accept threshold become *low-confidence*; checks depending on them become REVIEW with the box and score shown. Poor image quality also triggers REVIEW.

## 13. Colab training and moving the checkpoint
Your laptop likely lacks a GPU, so train in **Google Colab**: upload a labelled dataset, run the notebook, evaluate, download `best.pt` and a manifest, copy them into `models/custom/`, restart the backend. Guide: [MODEL_TRAINING.md](MODEL_TRAINING.md). Data sources and licensing: [DATASET.md](DATASET.md). Never upload confidential photos without permission.

## 14. Development phases and what to understand first
| Phase | Before you start, understand |
|---|---|
| 1 Setup | Git, venv, npm basics |
| 2 Backend | REST, FastAPI routes, Pydantic, SQLAlchemy |
| 3 Frontend | React components, TypeScript types, fetch |
| 4 Uploads/parsing | File safety, CSV/XLSX columns |
| 5 Dataset | YOLO label format, class definitions, data leakage |
| 6 Training | train/val/test, mAP, overfitting |
| 7 Integration | Inference, thresholds, interface boundaries |
| 8 Matching/rules | Expected vs observed, why REVIEW exists |
| 9 Results/review | Evidence traceability |
| 10 Reports | Reading stored results only |
| 11 Hardening | Testing, security checks |
| 12 Demo | Telling the story honestly |
Roadmap: [PHASE.md](PHASE.md).

## 15. Viva cheat-sheet
- *Is YOLO the whole system?* No: parsing, OCR, matching, rules, human review.
- *Can it verify wiring from photos?* No; those checks return REVIEW.
- *What if the object is not detected?* Not proof of absence → REVIEW.
- *How do you avoid inflated accuracy?* Split by cabinet, test once, report per-class metrics.
- *What is not done yet?* Everything except the scaffold; see [FINAL_REVIEW.md](FINAL_REVIEW.md).
