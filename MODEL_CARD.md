# Model Card — Eagle Eye component detector (baseline v1)

| Field | Value |
|---|---|
| Model name | Eagle Eye component detector |
| Version | v1 (baseline) |
| Architecture / base checkpoint | Ultralytics YOLO11n (`yolo11n.pt`), fine-tuned; 2,599,238 parameters (fused) |
| Checkpoint | `models/custom/best.pt` (about 5.5 MB), not committed to Git |
| Checkpoint SHA-256 | <copy from model_manifest.json> |
| Training date | <copy from model_manifest.json> |
| Software | Ultralytics 8.4.175, torch 2.11.0+cu130, Python 3.13.15 (Google Colab, Tesla T4) |
| Maintainer / contact | <your name or team> |

## Intended use
Detect visible electrical-panel components in photographs as **one input** to Eagle Eye's QC checks. A detection is evidence for a rule; it is not an inspection decision. A human inspector makes the final decision.

## Out-of-scope use
Sole basis for pass/fail; wiring or terminal-level verification; safety-critical release decisions; classes not listed below; thermal or infrared images; engineering drawings or schematics; counting individual parts inside grouped boxes.

## Classes (class id: name)
0 Active-Harmonic-Filters, 1 Air-Circuit-Breakers, 2 Bus-Bar, 3 Capacitors, 4 Contactors, 5 Fuses, 6 MCB, 7 Panel-Fans, 8 Phase-Reactor, 9 Power-Cable.

## Training data
- **Source:** Electrical Devices by VIT, Roboflow Universe (https://universe.roboflow.com/fieldsnap-pro). **License: CC BY 4.0** (attribution required: VIT, Roboflow Universe).
- **Preparation:** forked as version "v-clean" (Auto-Orient only, no augmentation). Exact duplicate images were removed and the data re-split by picture group with `scripts/dataset/dedupe_and_resplit.py` (seed 0, class-aware, ratios 0.7/0.2/0.1) after the original export showed cross-split leakage.
- **Size after cleaning:** 1,163 images -> 288 distinct source pictures -> 760 images kept (variants included). Split: train 531, valid 152, test 77.
- **Instances per class (train / valid / test):** 72/22/11, 35/12/5, 105/32/15, 101/31/15, 113/32/31, 120/39/23, 61/19/11, 52/15/11, 44/14/9, 91/27/14 (class ids 0 to 9).
- **Nature of the data:** mostly public internet-style images, many product close-ups; many boxes cover a group of parts (fuse rows, capacitor banks).

## Training configuration
Fine-tuned from `yolo11n.pt`; up to 100 epochs, patience 20, image size 640, batch 16, seed 0. Early stopping ended training at epoch 90; best epoch 70. Training time about 0.31 hours on a Tesla T4.

## Evaluation (held-out test split, evaluated once)
Test set: 77 images, 145 boxes. Metrics from Ultralytics `model.val(split="test")`, rounded to 3 decimals.

| Class | Test boxes | Precision | Recall | mAP50 | mAP50-95 |
|---|---|---|---|---|---|
| **All** | 145 | 0.716 | 0.519 | 0.608 | 0.411 |
| Active-Harmonic-Filters | 11 | 0.452 | 0.545 | 0.646 | 0.500 |
| Air-Circuit-Breakers | 5 | 0.942 | 1.000 | 0.995 | 0.799 |
| Bus-Bar | 15 | 0.562 | 0.267 | 0.250 | 0.155 |
| Capacitors | 15 | 0.632 | 0.600 | 0.594 | 0.303 |
| Contactors | 31 | 0.996 | 0.419 | 0.710 | 0.491 |
| Fuses | 23 | 0.643 | 0.522 | 0.615 | 0.384 |
| MCB | 11 | 0.818 | 0.818 | 0.856 | 0.595 |
| Panel-Fans | 11 | 0.721 | 0.472 | 0.732 | 0.432 |
| Phase-Reactor | 9 | 0.533 | 0.259 | 0.373 | 0.244 |
| Power-Cable | 14 | 0.861 | 0.286 | 0.307 | 0.204 |

Validation split (152 images, 243 boxes), used to choose the checkpoint, so slightly optimistic: precision 0.781, recall 0.586, mAP50 0.679, mAP50-95 0.469.

**Speed (Colab Tesla T4):** about 6.6 to 20.7 ms per image inference across runs. This does not represent the demo machine; measure there (Phase 7).

These are **object-detection** metrics. They are not end-to-end inspection accuracy (see MODEL_EVALUATION.md).

## Known limitations
- Trained on about 288 distinct public pictures; **not validated on real cabinet photographs**.
- The test set is small (5 to 31 boxes per class), so per-class scores are noisy. Air-Circuit-Breakers' 0.995 mAP50 rests on 5 boxes.
- Overall test recall is 0.519: the model misses about half of the objects. A missed detection must never be read as absence; the application returns `REVIEW`.
- **Low-reliability classes** (test recall below 0.3): Bus-Bar (0.267), Phase-Reactor (0.259), Power-Cable (0.286). The application should treat them as unsupported (checks return `REVIEW`).
- Grouped boxes make counting individual parts unreliable.
- 31 groups of identical image copies had differing labels; the copy with the most boxes was kept. Near-duplicates with different bytes may remain.
- Confidence thresholds are untuned defaults (conf 0.25, accept 0.50).

## Safety considerations
Human review is required. When evidence is missing, low-confidence or unsupported, the system returns `REVIEW`, never a guessed pass or fail.

## Licenses and attribution
- Dataset: Electrical Devices by VIT, Roboflow Universe, CC BY 4.0.
- Weights are derived from Ultralytics YOLO11, which is licensed AGPL-3.0 (with a separate enterprise license). Review the obligations before distributing the weights or offering the app as a service. See THIRD_PARTY_NOTICES.md.