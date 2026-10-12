# Model

How Eagle Eye uses object detection. Training is in [MODEL_TRAINING.md](MODEL_TRAINING.md); measurement in [MODEL_EVALUATION.md](MODEL_EVALUATION.md); terms in [GLOSSARY.md](GLOSSARY.md). No custom model exists yet.

## Why object detection
The first question of cabinet inspection is "which components are visible, and where?" Detection answers exactly that: it outputs a box, a class and a confidence per object. Classification (one label per image) is too coarse; segmentation is more than the MVP needs.

## What YOLO predicts
For each image: a list of `(class_id, confidence, bounding box)`.
- **Bounding box:** rectangle around the object (x, y, w, h).
- **Confidence score:** the model's own 0–1 score. It is *not* a calibrated probability of being correct.
- **IoU:** overlap of two boxes (intersection / union); used in training, NMS and evaluation.
- **NMS (non-maximum suppression):** removes duplicate overlapping boxes for the same object.
- **Precision:** of predicted boxes, the share that is correct. **Recall:** of real objects, the share found.
- **mAP50 / mAP50-95:** average precision across classes at IoU 0.5 / averaged over IoU 0.5–0.95.

## Baseline choice
Ultralytics' documentation shows both `yolo11n.pt` and the newer `yolo26n.pt` in its Python API (https://docs.ultralytics.com/compare/yolo11-vs-yolo26/, verified in search results). **Recommendation:** start with `yolo11n.pt` (nano, small, widely documented) and, if time allows, run one comparison with `yolo26n.pt`; choose by measured results, not by novelty. Do not promise any accuracy before evaluation. Ultralytics is licensed AGPL-3.0 with a separate enterprise license (see PyPI page https://pypi.org/project/ultralytics/); see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Pretrained vs custom weights
`yolo11n.pt` is pretrained on a general dataset (COCO) and recognises everyday objects, **not** specialised cabinet components. Custom weights are produced by **fine-tuning** the pretrained checkpoint on your annotated cabinet images. A generic model will not reliably detect relays or terminal blocks.

## Backend integration
`backend/app/vision/detector.py` (planned) exposes:
```python
class Detector(Protocol):
    def load(self) -> None: ...
    def detect(self, image: "np.ndarray", conf: float) -> list["Detection"]: ...
    @property
    def info(self) -> "ModelInfo": ...   # name, version, sha256, class map
```
Loading: read `MODEL_PATH` and `MODEL_MANIFEST_PATH` at startup (or lazily on first use). Failures: missing file → `MODEL_NOT_AVAILABLE` for detection endpoints only; class IDs in the weights that disagree with the manifest → refuse to load and report the mismatch.

## Preprocessing and inference configuration
Decode (OpenCV/Pillow), apply EXIF rotation, convert to RGB; let Ultralytics letterbox-resize to `DETECTION_IMGSZ` (default 640). Quality gate (resolution, blur via Laplacian variance, brightness) runs first; thresholds are configuration and need tuning on real photos.

## Confidence thresholds (initial assumptions, to be tuned)
- `DETECTION_CONF_THRESHOLD=0.25`: below this, discard.
- `DETECTION_ACCEPT_THRESHOLD=0.50`: at or above → accepted; between → `LOW` band → leads to `REVIEW`.
- `DETECTION_IOU_THRESHOLD=0.70`: NMS IoU.
Choose final values from per-class precision/recall curves ([MODEL_EVALUATION.md](MODEL_EVALUATION.md)).

## Class-name mapping and versioning
Always map by **name from the manifest**, never hard-code IDs in rules. Version = manifest `version` + checkpoint SHA-256, stored on every processing job. Template: [models/custom/model_manifest.example.json](models/custom/model_manifest.example.json).

## Inference response format (internal)
```json
{"file_id":"…","model":{"name":"…","version":"…"},
 "detections":[{"class_name":"breaker","class_id":0,"confidence":0.91,"bbox":[120,80,60,110],"band":"ACCEPTED"}]}
```
(`bbox` = x, y, w, h in original-image pixels. Illustrative values.)

## Hardware constraints
Nano models are intended to be usable on CPU for a handful of images, but speed on your machine is **unmeasured**; measure in Phase 7/11. GPU only needed for training.

## Replacing the model
Copy new `best.pt` and `model_manifest.json` into `models/custom/`; restart. If class names changed, update rule/alias configuration (not code). Keep old manifests for traceability.

## How OCR and rules complement detection
Detection says "something that looks like a relay is here". OCR reads its tag. Matching relates it to an expected row. Rules decide. Detection alone cannot establish correct part number, position or wiring.

## Limitations
Occlusion, glare, camera angle, small objects, look-alike parts, unseen cabinet layouts, and class imbalance all reduce reliability. A missed detection is not proof of absence.
