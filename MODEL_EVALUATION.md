# Model Evaluation

How to measure the detector reproducibly. **No evaluation has been run.** All numbers must come from real runs and be recorded in [MODEL_CARD.md](MODEL_CARD.md) and the model manifest.

## Two different questions
1. **Detector performance:** how well does YOLO find and classify components in images (precision, recall, mAP)?
2. **End-to-end inspection accuracy:** how often does Eagle Eye's final PASS/FAIL/REVIEW agree with a human expert's ground truth for whole cabinets? This depends on OCR, parsing, matching and rules too. A good mAP does **not** imply good inspection accuracy.

## Split policy
Train/val/test split **by cabinet** (no cabinet appears in two splits). Test set is touched once per model version for the final report. Keep split lists (`splits.csv`: image, cabinet_id, split) under version control (not the images).

## Baselines
(a) Pretrained generic weights without fine-tuning (expected to fail on specialised classes; documents the need for training). (b) First fine-tuned model. (c) Any later version. Compare on the same val/test sets.

## Detection metrics
Precision, recall, mAP50, mAP50-95 overall **and per class** (Ultralytics `model.val`). Also read the confusion matrix and PR/F1 curves. Report the number of validation/test images and instances per class; metrics on a handful of instances are unreliable.

## False positives / false negatives
Review saved prediction images; tag each error: missed object (FN), wrong class, duplicate box, hallucinated object (FP), cause (occlusion, glare, small, unseen type). The matching and rules stage treats FN and FP differently (non-detection ≠ absence), so error types matter.

## Confidence-threshold selection
Plot precision and recall vs confidence per class. Choose `DETECTION_ACCEPT_THRESHOLD` for high precision (avoid false PASS) and `DETECTION_CONF_THRESHOLD` low enough that uncertain objects surface as `REVIEW` instead of vanishing. Record the chosen values and the reasoning.

## Speed and resources
On the target demo machine, measure per-image latency (warm, excluding first call), peak RAM/VRAM, model file size. Report hardware and software versions. Unmeasured today.

## End-to-end evaluation (Phase 11)
Build a small ground-truth set: for each held-out cabinet, a human-labelled expected result per check. Compute agreement per rule, the rate of unsafe errors (false PASS), and the REVIEW rate. A high REVIEW rate is acceptable early; a false PASS is the worst outcome.

## Acceptance criteria (proposals, set after the first baseline)
- No class used in a demo rule has zero test instances.
- Per-class recall and precision on test are reported and documented; classes below an agreed floor are marked **unsupported** in the UI and rules (return `REVIEW`).
- No false PASS in the demo set (end-to-end).

## Model version comparison table (template)
| Version | Base | Data | mAP50 | mAP50-95 | Precision | Recall | Latency | Notes |
|---|---|---|---|---|---|---|---|---|
| v0 | yolo11n.pt (no fine-tune) | — | PENDING | PENDING | PENDING | PENDING | PENDING | |

## Limitations
Small test sets give noisy metrics; synthetic or mock-up cabinets may not represent real ones; mAP does not capture the cost asymmetry between missed defects and false alarms.
