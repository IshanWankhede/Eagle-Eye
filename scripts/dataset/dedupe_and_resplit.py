"""Remove exact-duplicate images and re-split a Roboflow-layout YOLO dataset WITHOUT leakage.

Groups images by original file name (the part before '.rf.') or identical bytes, keeps one copy per
distinct content, then assigns whole groups to train/valid/test (class-aware by default).
Usage:
  python scripts/dataset/dedupe_and_resplit.py --src data/raw/electrical-devices --dst data/processed/electrical-devices-v2
"""
from __future__ import annotations

import argparse
import hashlib
import random
import shutil
from collections import defaultdict
from pathlib import Path

IMG_EXT = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
SRC_SPLITS = ("train", "valid", "test")


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def base_name(p: Path) -> str:
    return p.name.split(".rf.")[0] if ".rf." in p.name else p.stem


def label_lines(lbl: Path) -> list[str]:
    return [ln.strip() for ln in lbl.read_text().splitlines() if ln.strip()] if lbl.is_file() else []


class DSU:
    def __init__(self) -> None:
        self.p: dict[str, str] = {}

    def find(self, x: str) -> str:
        self.p.setdefault(x, x)
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a: str, b: str) -> None:
        self.p[self.find(a)] = self.find(b)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, type=Path)
    ap.add_argument("--dst", required=True, type=Path)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--no-stratify", action="store_true", help="balance image counts only (old behaviour)")
    ap.add_argument("--ratios", type=float, nargs=3, default=(0.7, 0.2, 0.1), metavar=("TRAIN", "VALID", "TEST"))
    a = ap.parse_args()
    if a.dst.exists() and any(a.dst.iterdir()):
        raise SystemExit(f"destination {a.dst} is not empty; choose a new folder")

    items = []  # (img_path, lbl_path, sha, base, orig_split)
    for sp in SRC_SPLITS:
        img_dir, lbl_dir = a.src / sp / "images", a.src / sp / "labels"
        if not img_dir.is_dir():
            continue
        for img in sorted(p for p in img_dir.iterdir() if p.suffix.lower() in IMG_EXT):
            items.append((img, lbl_dir / (img.stem + ".txt"), sha256(img), base_name(img), sp))
    if not items:
        raise SystemExit("no images found (expected Roboflow layout <src>/<split>/images)")

    dsu = DSU()
    for img, _, sha, base, _ in items:
        dsu.union("b:" + base, "h:" + sha)
    groups: dict[str, list] = defaultdict(list)
    for it in items:
        groups[dsu.find("b:" + it[3])].append(it)

    kept_groups: list[list] = []
    dropped = conflicts = 0
    conflict_notes: list[str] = []
    for members in groups.values():
        by_hash: dict[str, list] = defaultdict(list)
        for it in members:
            by_hash[it[2]].append(it)
        kept = []
        for copies in by_hash.values():
            best = max(copies, key=lambda c: (len(label_lines(c[1])), -len(c[0].name)))
            kept.append(best)
            dropped += len(copies) - 1
            if len({tuple(sorted(ln.split()[0] for ln in label_lines(c[1]))) for c in copies}) > 1:
                conflicts += 1
                conflict_notes.append(f"{best[3]}: {len(copies)} identical copies, different labels; kept {best[0].name}")
        kept_groups.append(kept)

    rng = random.Random(a.seed)
    rng.shuffle(kept_groups)
    total = sum(len(g) for g in kept_groups)
    names = ("train", "valid", "test")
    ratio = dict(zip(names, a.ratios))
    target = {n: ratio[n] * total for n in names}
    count = dict.fromkeys(names, 0)
    assign: dict[str, list] = {n: [] for n in names}

    def group_cls(g: list) -> dict[int, int]:
        d: dict[int, int] = defaultdict(int)
        for it in g:
            for ln in label_lines(it[1]):
                d[int(ln.split()[0])] += 1
        return d

    gcc = [group_cls(g) for g in kept_groups]
    class_total: dict[int, int] = defaultdict(int)
    for d in gcc:
        for c, k in d.items():
            class_total[c] += k
    cur: dict[str, dict[int, int]] = {n: defaultdict(int) for n in names}
    order = sorted(range(len(kept_groups)),
                   key=lambda i: (min((class_total[c] for c in gcc[i]), default=10**9), -len(kept_groups[i])))
    for i in order:
        g = kept_groups[i]
        if a.no_stratify:
            n = max(names, key=lambda k: target[k] - count[k])
        else:
            def score(k: str) -> float:
                s_img = 0.5 * (target[k] - count[k]) / max(target[k], 1) * len(g)
                s_cls = sum(v * (ratio[k] * class_total[c] - cur[k][c]) / max(ratio[k] * class_total[c], 1)
                            for c, v in gcc[i].items())
                return s_img + s_cls
            n = max(names, key=score)
        assign[n].extend(g)
        count[n] += len(g)
        for c, v in gcc[i].items():
            cur[n][c] += v

    cls_counts: dict[str, dict[int, int]] = {n: defaultdict(int) for n in names}
    for n in names:
        (a.dst / n / "images").mkdir(parents=True, exist_ok=True)
        (a.dst / n / "labels").mkdir(parents=True, exist_ok=True)
        for img, lbl, _, _, _ in assign[n]:
            shutil.copy2(img, a.dst / n / "images" / img.name)
            lines = label_lines(lbl)
            (a.dst / n / "labels" / (img.stem + ".txt")).write_text("\n".join(lines) + ("\n" if lines else ""))
            for ln in lines:
                cls_counts[n][int(ln.split()[0])] += 1
    if (a.src / "data.yaml").is_file():
        shutil.copy2(a.src / "data.yaml", a.dst / "data.yaml")

    if conflict_notes:
        (a.dst / "dedupe_report.txt").write_text("\n".join(conflict_notes) + "\n")
    print(f"images before: {len(items)} | groups (distinct source pictures): {len(groups)}")
    print(f"exact duplicate copies removed: {dropped} | groups with conflicting labels among copies: {conflicts}")
    print(f"images after: {total} -> " + ", ".join(f"{n}={count[n]}" for n in names))
    all_ids = sorted({c for n in names for c in cls_counts[n]})
    print("instances per class id (train / valid / test):")
    for c in all_ids:
        row = [cls_counts[n].get(c, 0) for n in names]
        flag = "   <-- WEAK: too few in valid/test" if row[1] < 5 or row[2] < 3 else ""
        print(f"  class {c}: {row[0]} / {row[1]} / {row[2]}{flag}")
    print("Next: run validate_yolo_dataset.py on the new folder (expect 0 errors).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())