# Data Annotation Guide

For annotating cabinet photos for YOLO detection. Tools: any that exports YOLO format (e.g., CVAT, Label Studio, Roboflow). Use a **self-hosted/local** tool for confidential images. Related: [DATASET.md](DATASET.md), [MODEL_TRAINING.md](MODEL_TRAINING.md).

## 1. Define classes first
Write one sentence plus 2–3 example descriptions per class, and a "do not label" list. Keep the list **small and tied to the checks you will demo**. Use lowercase `snake_case` names. Do not change a class's meaning mid-project; if you must, version the guideline and relabel.

## 2. Bounding-box rules
- Tight box around the **visible** part of the object, including its housing/body but not neighbouring parts.
- One box per physical object; do not merge a row of breakers into one box.
- Keep boxes inside the image.
- Be consistent: same convention for every annotator.

## 3. Hard cases
| Case | Rule (proposal) |
|---|---|
| Partial occlusion | Label the visible part if you can still identify the class; skip if <~30% visible (state your threshold and keep it) |
| Tiny objects | Label if identifiable at full resolution; otherwise skip and note image as "small objects" |
| Blurry | Label if class is clear to a human; mark very blurry images for removal from the test set |
| Ambiguous class | Do not guess; flag for second review; use an `unsure` list outside the dataset |
| Reflections/glare | Label only the real object |

## 4. Image-level quality checks
Reject or flag: corrupt files, extreme blur, severe over/under-exposure, duplicates, photos of screens, images containing people/personal data (privacy), unauthorised content.

## 5. Label ID consistency
The class list order defines IDs (0..N−1). Export with the same order every time; verify with `validate_yolo_dataset.py`. Never merge datasets by ID — use names ([DATASET.md](DATASET.md)).

## 6. Splits
Split by cabinet/session **before** augmentation. Keep the test set frozen and untouched during labelling-rule changes.

## 7. Inter-annotator consistency
Double-annotate ~10% of images; compare boxes (IoU ≥ 0.5 agreement and class agreement); discuss disagreements; update the guideline. Record the agreement rate you measure.

## 8. Review and versioning
Second-pass review of all boxes of rare classes; keep guideline version, dataset version and export date in [DATASET_CARD.md](DATASET_CARD.md). Store labels in a versioned archive (not in Git if large or confidential).

## Illustrative example (not real training data)
Image `cab01_front.jpg`, 1000×800 px, with one object of class 0 occupying pixels x=100–300, y=200–400:
`x_center=(100+300)/2/1000=0.20`, `y_center=(200+400)/2/800=0.375`, `width=200/1000=0.20`, `height=200/800=0.25`
Label file `cab01_front.txt`: `0 0.200000 0.375000 0.200000 0.250000`
