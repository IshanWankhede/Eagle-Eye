"""TEMPLATE training script (not executed during scaffold creation).

Adjust DATA_YAML, MODEL and hyperparameters to the real dataset. Prefer the Colab notebook
(notebooks/eagle_eye_yolo_training.ipynb) because a GPU is needed for practical training.
"""
from __future__ import annotations

import argparse

from ultralytics import YOLO


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True, help="path to dataset YAML")
    ap.add_argument("--model", default="yolo11n.pt", help="pretrained checkpoint")
    ap.add_argument("--epochs", type=int, default=50)
    ap.add_argument("--imgsz", type=int, default=640)
    ap.add_argument("--batch", type=int, default=16)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--project", default="runs")
    ap.add_argument("--name", default="eagle_eye_baseline")
    args = ap.parse_args()

    model = YOLO(args.model)
    model.train(
        data=args.data, epochs=args.epochs, imgsz=args.imgsz, batch=args.batch,
        seed=args.seed, patience=20, project=args.project, name=args.name,
    )
    model.val(data=args.data, split="test")  # final held-out evaluation, run once


if __name__ == "__main__":
    main()
