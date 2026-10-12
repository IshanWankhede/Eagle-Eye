# Model Training on Google Colab (beginner guide)

Goal: fine-tune a pretrained YOLO detector on **your** annotated cabinet images, pick a checkpoint, and bring `best.pt` into Eagle Eye. **Nothing in this guide has been executed by the author of this scaffold**; commands follow Ultralytics' documented API (https://docs.ultralytics.com/) and must be verified in your Colab runtime. The same cells are in [notebooks/eagle_eye_yolo_training.ipynb](notebooks/eagle_eye_yolo_training.ipynb) (generated from this file by `scripts/training/build_colab_notebook.py`). Read [DATASET.md](DATASET.md) and [MODEL.md](MODEL.md) first.

## Concepts in one minute
- **Training** adjusts weights using the *train* split. **Validation** (the *val* split) is checked every epoch to pick the best checkpoint and detect overfitting. **Test** is used **once at the end** for an honest score; never tune against it.
- More epochs do not automatically mean better results: training scores can keep rising while real-world performance falls (**overfitting**). Early stopping (`patience`) helps.
- Training from scratch is unnecessary for a hackathon; fine-tune pretrained weights.

## Steps 1–4: Colab, GPU, data, licensing
1. Open https://colab.research.google.com → New notebook (or upload the generated `.ipynb`).
2. Runtime → Change runtime type → **GPU** (availability and type vary; free tier can disconnect).
3. Review the dataset license ([DATASET.md](DATASET.md)). **Do not upload confidential photos to Colab/Drive without authorisation.**
4. Put your dataset as a zip on Google Drive, or use a download snippet. **No credentials in notebooks**: store keys in Colab *Secrets* (key icon in the sidebar) and read with `google.colab.userdata`.

## Expected directory layout (YOLO format)
Two layouts work with this guide: the Ultralytics style below, and the **Roboflow export style** (`train/images`, `train/labels`, `valid/images`, `valid/labels`, optional `test/...`, plus `data.yaml`). Cell 5 builds a clean YAML for either, so you do not have to edit Roboflow's `data.yaml` paths (they are often wrong in Colab).

```text
/content/dataset/
├── images/{train,val,test}/*.jpg
├── labels/{train,val,test}/*.txt     # one .txt per image, same stem
└── data.yaml
```
Each label line: `class_id x_center y_center width height`, all normalised to 0–1. Images with no objects have an empty (or missing) label file.

## Illustrative dataset YAML (class names are EXAMPLES ONLY)
```yaml
path: /content/dataset
train: images/train
val: images/val
test: images/test

names:
  0: breaker
  1: relay
  2: terminal_block
```
The final YAML must use the real class names and IDs of your annotations. Never list classes that do not exist in the labels.

## Split without leakage
**Public Roboflow downloads can already be leaky** (identical copies of one picture in several splits). Run `scripts/dataset/dedupe_and_resplit.py` first and zip the **output** folder for Colab. See [DATASET.md](DATASET.md).

Split **by cabinet** (or by photo session), not by random image: several photos of the same cabinet in train and val make validation scores look better than reality (**data leakage**). Keep all images of a cabinet in one split. Check for exact duplicates with `scripts/dataset/validate_yolo_dataset.py` (it flags cross-split duplicates; it cannot detect near-duplicates).

## Colab cells
Run in order. Edit the marked variables.

### Cell 1 — check GPU
```python
!nvidia-smi
```

### Cell 2 — install and print versions
```python
!pip install -q ultralytics
import sys, torch, ultralytics
print("python", sys.version.split()[0], "| torch", torch.__version__, "| ultralytics", ultralytics.__version__)
print("CUDA available:", torch.cuda.is_available())
```

### Cell 3 — mount Drive (optional, protects against disconnects)
```python
from google.colab import drive
drive.mount('/content/drive')
DRIVE_OUT = '/content/drive/MyDrive/eagle-eye-training'   # EDIT
import os; os.makedirs(DRIVE_OUT, exist_ok=True)
```

### Cell 4 — get the dataset (template: choose ONE option and edit)
```python
# Option A: unzip a dataset zip stored on Drive (the zip must contain data.yaml, train/, valid/ ... directly, not inside an extra folder)
!mkdir -p /content/dataset
!unzip -q "/content/drive/MyDrive/cabinet_dataset.zip" -d /content/dataset   # EDIT path

# Option B: Roboflow export (public data). Store the key in Colab Secrets as ROBOFLOW_API_KEY.
# !pip install -q roboflow
# from google.colab import userdata
# from roboflow import Roboflow
# rf = Roboflow(api_key=userdata.get('ROBOFLOW_API_KEY'))
# project = rf.workspace("WORKSPACE").project("PROJECT")      # EDIT from the dataset page
# dataset = project.version(1).download("yolov8")             # pick an Ultralytics-compatible format
```

### Cell 5 — build a clean data YAML and validate labels
```python
import yaml, os
DATA_ROOT = '/content/dataset'                 # EDIT: folder that holds data.yaml and train/ valid/ (Roboflow) or images/ labels/
orig = yaml.safe_load(open(f'{DATA_ROOT}/data.yaml'))
raw = orig['names']
names = dict(enumerate(raw)) if isinstance(raw, list) else {int(k): v for k, v in raw.items()}
NC = len(names)
print("classes:", NC, names)

if os.path.isdir(f'{DATA_ROOT}/images/train'):          # Ultralytics-style layout
    cfg = {'path': DATA_ROOT, 'train': 'images/train', 'val': 'images/val', 'names': names}
    if os.path.isdir(f'{DATA_ROOT}/images/test'): cfg['test'] = 'images/test'
else:                                                    # Roboflow export layout
    val_dir = 'valid' if os.path.isdir(f'{DATA_ROOT}/valid/images') else 'val'
    cfg = {'path': DATA_ROOT, 'train': 'train/images', 'val': f'{val_dir}/images', 'names': names}
    if os.path.isdir(f'{DATA_ROOT}/test/images'): cfg['test'] = 'test/images'
DATA_YAML = f'{DATA_ROOT}/eagle_eye_data.yaml'
yaml.safe_dump(cfg, open(DATA_YAML, 'w'))
print(open(DATA_YAML).read())
HAS_TEST = 'test' in cfg
# Upload scripts/dataset/validate_yolo_dataset.py to /content (or clone your repo), then:
!python /content/validate_yolo_dataset.py --root {DATA_ROOT} --nc {NC}
```
Fix every `ERROR` before training. Open a few labelled images to confirm boxes look right. If the dataset has no `test` split, evaluate on `val` only and say so in your model card.

### Cell 6 — smoke test (1 epoch, tiny): proves the pipeline works
```python
from ultralytics import YOLO
MODEL = 'yolo11n.pt'      # pretrained baseline; yolo26n.pt is an option to compare later
m = YOLO(MODEL)
m.train(data=DATA_YAML, epochs=1, imgsz=320, batch=8, fraction=0.1, project='/content/runs', name='smoke', exist_ok=True)
```

### Cell 7 — real training (TEMPLATE: adjust to your dataset)
```python
from ultralytics import YOLO
model = YOLO(MODEL)
results = model.train(
    data=DATA_YAML,
    epochs=100,          # upper bound; early stopping decides
    patience=20,         # stop if val metrics do not improve for 20 epochs
    imgsz=640,           # reduce to 512/416 if GPU memory runs out
    batch=16,            # reduce to 8/4 on CUDA out-of-memory; -1 requests auto batch
    seed=0,
    project=DRIVE_OUT,   # runs saved to Drive so a disconnect does not lose them
    name='eagle_eye_v1',
    exist_ok=True,
)
```
Batch/image size: larger is not automatically better. Small components in big photos may need `imgsz` 800–1024 (slower, more memory). If Colab disconnects, re-run Cell 2–5 and resume with `YOLO(f'{DRIVE_OUT}/eagle_eye_v1/weights/last.pt').train(resume=True)`.

### Cell 8 — evaluate on validation and test (test only once, at the end)
```python
best_path = f'{DRIVE_OUT}/eagle_eye_v1/weights/best.pt'
best = YOLO(best_path)
for split in (['val', 'test'] if HAS_TEST else ['val']):
    m_ = best.val(data=DATA_YAML, split=split, project=DRIVE_OUT, name=f'eval_{split}', exist_ok=True)
    print(split, 'precision', m_.box.mp, 'recall', m_.box.mr, 'mAP50', m_.box.map50, 'mAP50-95', m_.box.map)
    print('per-class mAP50-95:', dict(zip(m_.names.values(), m_.box.maps)))
```
Ultralytics also saves a confusion matrix and PR curves in the evaluation run folder; open them. Record the numbers **as measured**; do not round up or cherry-pick.

### Cell 9 — qualitative check on sample images
```python
import glob
IMG_GLOB = f'{DATA_ROOT}/test/images/*' if os.path.isdir(f'{DATA_ROOT}/test/images') else f'{DATA_ROOT}/valid/images/*'
samples = glob.glob(IMG_GLOB)[:12]   # EDIT if you use the Ultralytics-style layout (images/test)
pred = best.predict(source=samples, conf=0.25, save=True, project=DRIVE_OUT, name='samples', exist_ok=True)
```
Look at the saved images. Note false positives, missed objects, and failures under glare or angle.

### Cell 10 — write the model manifest and download the checkpoint
```python
import hashlib, json, sys, datetime, torch, ultralytics
sha = hashlib.sha256(open(best_path, 'rb').read()).hexdigest()
manifest = {
  "model_family": "ultralytics-yolo",
  "base_checkpoint": MODEL,
  "checkpoint_path": "models/custom/best.pt",
  "checkpoint_sha256": sha,
  "class_names": {str(k): v for k, v in dict(names).items()} if isinstance(names, dict) else {str(i): n for i, n in enumerate(names)},
  "dataset": {"name": "FILL", "source_url": "FILL", "version": "FILL", "license": "FILL"},
  "training": {"epochs_max": 100, "patience": 20, "imgsz": 640, "batch": 16, "seed": 0, "date": datetime.date.today().isoformat()},
  "software": {"ultralytics": ultralytics.__version__, "torch": torch.__version__, "python": sys.version.split()[0]},
  "evaluation": {"split": "test", "precision": None, "recall": None, "map50": None, "map50_95": None, "status": "FILL FROM CELL 8"},
  "known_limitations": ["FILL"]
}
json.dump(manifest, open('/content/model_manifest.json', 'w'), indent=2)
from google.colab import files
files.download(best_path)
files.download('/content/model_manifest.json')
```
Then edit the `FILL` values by hand with real numbers and dataset details.

## Checkpoint selection
`best.pt` is the checkpoint with the best validation fitness during training; `last.pt` is the final epoch. Use `best.pt` unless evaluation shows a problem. Compare candidate runs only on the **validation** split; confirm the winner once on **test**.

## Transfer to the repository and connect to FastAPI
1. Copy `best.pt` → `eagle-eye/models/custom/best.pt` and `model_manifest.json` → `eagle-eye/models/custom/model_manifest.json` (both are git-ignored except the example; weights are never committed).
2. Ensure `.env` has `MODEL_PATH=./models/custom/best.pt`.
3. Start the backend; `GET /api/health` shows `model_file_found: true` (and `model_loaded: true` once Phase 7 is implemented).
4. Verify class names in the manifest equal those in the weights.

## Improving results responsibly
Better and more representative annotations; consistent class definitions; more varied cabinets, lighting and angles; enough examples per class (watch class imbalance); better image quality; sensible augmentation (do not add unrealistic ones); hyperparameter experiments *one change at a time*; and **error analysis** (look at failures, then collect data to fix them). A credible model comes from measurement and iteration, not from a promised number.

## Troubleshooting
| Symptom | Fix |
|---|---|
| `CUDA out of memory` | Lower `batch`, then `imgsz`; restart runtime |
| No GPU | Runtime → Change runtime type; free quota may be exhausted |
| "No labels found" | Check folder names `images/` and `labels/`, matching stems, YAML `path` |
| Class IDs out of range | Fix labels or YAML; re-run validator |
| mAP near zero | Wrong class mapping, empty labels, or too little data; inspect overlays |
| Colab disconnected | Resume from `last.pt` on Drive |
More: [TROUBLESHOOTING.md](TROUBLESHOOTING.md).
