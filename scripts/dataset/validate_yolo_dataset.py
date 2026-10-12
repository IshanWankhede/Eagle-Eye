"""Validate a YOLO-format detection dataset (images/<split>, labels/<split>).

Supports two layouts (auto-detected):
  A) Ultralytics style : <root>/images/<split>/*.jpg  and <root>/labels/<split>/*.txt   (train, val, test)
  B) Roboflow export   : <root>/<split>/images/*.jpg  and <root>/<split>/labels/*.txt   (train, valid, test)
Usage: python scripts/dataset/validate_yolo_dataset.py --root PATH --nc 3
Checks: missing labels/images, class-ID range, normalized coordinates, malformed lines,
exact-duplicate images (SHA-256) within and ACROSS splits (data leakage), optional corrupt-image check
(requires Pillow). Exit code 1 if errors were found.
"""
from __future__ import annotations

import argparse
import hashlib
import sys
from collections import defaultdict
from pathlib import Path

IMG_EXT = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
SPLITS = ("train", "val", "test")


def split_dirs(root: Path, split: str):
    """Return (image_dir, label_dir) for either supported layout, or (None, None)."""
    a_img, a_lbl = root / "images" / split, root / "labels" / split
    if a_img.is_dir():
        return a_img, a_lbl
    name = "valid" if split == "val" else split
    b_img, b_lbl = root / name / "images", root / name / "labels"
    if b_img.is_dir():
        return b_img, b_lbl
    return None, None


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def check_image(path: Path) -> bool:
    try:
        from PIL import Image
    except ImportError:
        return True
    try:
        with Image.open(path) as im:
            im.verify()
        return True
    except Exception:
        return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, type=Path)
    ap.add_argument("--nc", required=True, type=int, help="number of classes")
    args = ap.parse_args()

    errors: list[str] = []
    warnings: list[str] = []
    hashes: dict[str, list[str]] = defaultdict(list)
    counts: dict[str, int] = {}
    class_counts: dict[int, int] = defaultdict(int)

    for split in SPLITS:
        img_dir, lbl_dir = split_dirs(args.root, split)
        if img_dir is None:
            if split == "test":
                warnings.append("no test split found")
            else:
                errors.append(f"missing image folder for split '{split}' (checked both layouts)")
            continue
        images = sorted(p for p in img_dir.rglob("*") if p.suffix.lower() in IMG_EXT)
        counts[split] = len(images)
        for img in images:
            hashes[sha256(img)].append(f"{split}/{img.name}")
            if not check_image(img):
                errors.append(f"corrupt image: {split}/{img.name}")
            lbl = lbl_dir / (img.stem + ".txt")
            if not lbl.is_file():
                warnings.append(f"no label file (treated as background): {split}/{img.name}")
                continue
            for n, line in enumerate(lbl.read_text().splitlines(), 1):
                if not line.strip():
                    continue
                parts = line.split()
                if len(parts) != 5:
                    errors.append(f"{lbl.name}:{n} expected 5 values, got {len(parts)}")
                    continue
                try:
                    cls = int(parts[0])
                    x, y, w, h = map(float, parts[1:])
                except ValueError:
                    errors.append(f"{lbl.name}:{n} non-numeric value")
                    continue
                if not 0 <= cls < args.nc:
                    errors.append(f"{lbl.name}:{n} class id {cls} outside 0..{args.nc - 1}")
                if not all(0.0 <= v <= 1.0 for v in (x, y, w, h)) or w <= 0 or h <= 0:
                    errors.append(f"{lbl.name}:{n} coordinates not normalized/positive")
                class_counts[cls] += 1
        label_stems = {p.stem for p in lbl_dir.rglob("*.txt")} if lbl_dir.is_dir() else set()
        image_stems = {p.stem for p in images}
        for stem in sorted(label_stems - image_stems):
            errors.append(f"label without image: {split}/{stem}.txt")

    for digest, files in hashes.items():
        if len(files) > 1:
            splits_involved = {f.split("/")[0] for f in files}
            msg = f"duplicate images ({digest[:8]}): {files}"
            (errors if len(splits_involved) > 1 else warnings).append(
                ("LEAKAGE " if len(splits_involved) > 1 else "") + msg
            )

    print("Images per split:", counts)
    print("Instances per class id:", dict(sorted(class_counts.items())))
    for w in warnings:
        print("WARN :", w)
    for e in errors:
        print("ERROR:", e)
    print(f"{len(errors)} error(s), {len(warnings)} warning(s)")
    print("Note: exact-hash checks do not detect near-duplicates or frames of the same cabinet.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
