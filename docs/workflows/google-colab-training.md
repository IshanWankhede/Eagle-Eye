# Google Colab training workflow (summary)
Full guide: [MODEL_TRAINING.md](../../MODEL_TRAINING.md).
1. Prepare/validate dataset locally (`scripts/dataset/validate_yolo_dataset.py`).
2. Upload dataset zip to Drive (authorised data only).
3. Open `notebooks/eagle_eye_yolo_training.ipynb` in Colab, GPU runtime.
4. Run smoke test, then real training, then val/test evaluation, then export manifest.
5. Download `best.pt` + manifest → `models/custom/`.
6. Record metrics in [MODEL_CARD.md](../../MODEL_CARD.md).
