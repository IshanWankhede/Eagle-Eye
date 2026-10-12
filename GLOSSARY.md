# Glossary (plain English)

| Term | Meaning |
|---|---|
| API | A set of URLs/functions programs use to talk to each other. Here: the backend's HTTP endpoints |
| REST | A style of API using HTTP methods (GET, POST) on resource URLs, usually with JSON |
| Schema | A formal description of data shape (fields and types), e.g., Pydantic models |
| ORM | Object-relational mapper: lets code use Python classes instead of raw SQL (SQLAlchemy) |
| Migration | A versioned change to the database structure (e.g., Alembic) |
| YOLO | "You Only Look Once": a family of fast object-detection neural networks |
| Object detection | Finding objects in an image and giving each a class and a box |
| Bounding box | A rectangle around a detected object |
| Inference | Running a trained model on new data to get predictions |
| Fine-tuning | Continuing training of a pretrained model on your own data |
| Epoch | One full pass over the training images |
| Batch size | Images processed together in one training step |
| Confidence score | The model's 0–1 certainty for a prediction (not a guaranteed probability) |
| IoU | Intersection over Union: how much two boxes overlap (0–1) |
| NMS | Non-maximum suppression: removes duplicate overlapping boxes |
| Precision | Of the things the model flagged, how many were right |
| Recall | Of the real things present, how many the model found |
| mAP | Mean average precision: summary of detection quality; mAP50 uses IoU 0.5, mAP50-95 averages thresholds |
| False positive | The model reports something that is not there |
| False negative | The model misses something that is there |
| OCR | Optical character recognition: reading text from images |
| Data leakage | Information from test/validation data leaking into training, inflating scores (e.g., same cabinet in train and val) |
| Expected configuration | What the engineering documents say should be in the cabinet |
| Observed evidence | What detection/OCR found in the photos |
| PASS / FAIL / REVIEW | Rule outcomes: consistent evidence / inconsistent evidence / not enough or unsupported evidence, needs a human |
| Checkpoint | A saved model weights file (`.pt`) |
| Manifest | A JSON file describing a model: classes, data, training, metrics, hashes |
| GA drawing | General-arrangement drawing showing how components are laid out |
| MVP | Minimum viable product: the smallest credible working version |
