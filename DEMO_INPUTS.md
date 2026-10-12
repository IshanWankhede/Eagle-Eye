# What do I give the app? (demo inputs)

Status: the upload and processing features are **planned** (Phases 4, 7, 8). This explains what inputs the finished MVP will expect, and how to prepare them from a public dataset.

## The two inputs
1. **A cabinet photo** (JPEG or PNG). For the demo use an image from the dataset's `test/images` (or `valid/images`) folder, because you know the correct answer for it. Optionally also use a few photos you take yourself of a real panel, to see how the model behaves (expect weaker results).
2. **An expected-components file** (CSV or XLSX) listing what *should* be in that cabinet.

Columns: `item_id, component_class, tag, quantity, zone, notes`
- `component_class` **must use a class name your trained model knows** (the names in the dataset's `data.yaml`, e.g. a name from your dataset's `data.yaml` (for example `circuit breaker 3-pole`)). Other names cannot be matched, so the check becomes `REVIEW`.
- `quantity`: how many of that class are expected.
- `tag`, `zone`, `notes`: optional. Public datasets contain no tag text, so leave `tag` empty; text-label checks (R-003) are then not applicable.

## Make the expected file from a dataset image (script included)
Each image in a YOLO dataset has a label file with the same name in `labels/`. The script counts the objects per class in that file:
```powershell
python scripts/utilities/labels_to_expected_csv.py `
  --data-yaml data/raw/<dataset-name>/data.yaml `
  --label data/raw/<dataset-name>/test/labels/<image-name>.txt `
  --out expected_demo.csv
```
Then upload `data/raw/<dataset-name>/test/images/<image-name>.jpg` and `expected_demo.csv` to the app. (Tested on synthetic files only, not yet on a real Roboflow export.)

## Create demo scenarios by editing the CSV
| Edit | Expected app outcome (design intent) |
|---|---|
| Leave the CSV as generated | Mostly `PASS`; low-confidence detections show `REVIEW` |
| Increase a `quantity` by 1 | Count rule flags a shortfall -> `REVIEW` (not-detected is not proof of absence) |
| Add a class that is not in the photo | `REVIEW`, never a guessed `PASS` |
| Remove a row for something that is visible | Unexpected component -> `REVIEW` |
| Use a blurry or dark photo | Image-quality rule -> `REVIEW` |
These are design intentions from [REQUIREMENTS.md](REQUIREMENTS.md); behaviour is not verified until Phase 8 is built and tested.

## Not supported as input (MVP)
CAD files, scanned drawings, arbitrary spreadsheet layouts, video, wiring/terminal-level verification (always `REVIEW`).

## Note for the Electrical Devices dataset (FieldSnap Pro)
Boxes in this dataset often cover a **group** of parts (a row of fuses, a capacitor bank). Therefore:
- Set `quantity` in the CSV to the **number of boxes** the script counts, not the number of physical parts. (`labels_to_expected_csv.py` counts label lines, i.e. boxes.)
- Use presence-style demos ("is there a Fuses box / Capacitors box?"). Count mismatches should end up as `REVIEW`, not `FAIL`.
- Use class names exactly as written in `data.yaml` (e.g., `Fuses`, `Capacitors`, `MCB`).

## Real class names for the chosen dataset (Electrical Devices)
Use these spellings exactly in the CSV `component_class` column: `Active-Harmonic-Filters`, `Air-Circuit-Breakers`, `Bus-Bar`, `Capacitors`, `Contactors`, `Fuses`, `MCB`, `Panel-Fans`, `Phase-Reactor`, `Power-Cable`. (Names seen on the dataset's Classes & Tags page; confirm against your export's `data.yaml`.) A fictional example file using them: [data/samples/expected_components.electrical_devices.example.csv](data/samples/expected_components.electrical_devices.example.csv).
