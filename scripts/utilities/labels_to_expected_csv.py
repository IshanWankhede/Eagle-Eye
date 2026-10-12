"""Create an expected-components CSV for the app from a YOLO label file (ground truth of ONE image).

Why: public datasets have no engineering documents. For a demo you take one dataset test image as the
"cabinet photo" and generate the matching "expected list" from its human-made labels, then edit the
CSV on purpose (remove/add rows) to demonstrate PASS / FAIL / REVIEW.

Usage:
  python scripts/utilities/labels_to_expected_csv.py --data-yaml PATH/data.yaml --label PATH/image.txt --out expected.csv
Output columns: item_id,component_class,tag,quantity,zone,notes   (tag/zone left empty: public data has no tags)
"""
from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path


def load_names(yaml_path: Path) -> dict[int, str]:
    """Minimal parser for the 'names' entry (list or id: name map) without needing PyYAML."""
    try:
        import yaml  # type: ignore

        names = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))["names"]
        return dict(enumerate(names)) if isinstance(names, list) else {int(k): v for k, v in names.items()}
    except ImportError:
        pass
    text = yaml_path.read_text(encoding="utf-8")
    line = next(ln for ln in text.splitlines() if ln.strip().startswith("names:"))
    inline = line.split(":", 1)[1].strip()
    if inline.startswith("["):
        items = [x.strip().strip("'\"") for x in inline.strip("[]").split(",") if x.strip()]
        return dict(enumerate(items))
    names: dict[int, str] = {}
    lines = text.splitlines()
    for ln in lines[lines.index(line) + 1:]:
        if not ln.startswith((" ", "\t", "-")):
            break
        key, _, val = ln.strip().partition(":")
        if _ and key.strip().isdigit():
            names[int(key)] = val.strip().strip("'\"")
        elif ln.strip().startswith("-"):
            names[len(names)] = ln.strip()[1:].strip().strip("'\"")
    return names


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-yaml", required=True, type=Path)
    ap.add_argument("--label", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args()
    names = load_names(a.data_yaml)
    counts: Counter[str] = Counter()
    for ln in a.label.read_text().splitlines():
        if ln.strip():
            counts[names[int(ln.split()[0])]] += 1
    with a.out.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["item_id", "component_class", "tag", "quantity", "zone", "notes"])
        for i, (cls, n) in enumerate(sorted(counts.items()), 1):
            w.writerow([f"E-{i:03d}", cls, "", n, "", "generated from dataset labels"])
    print(f"wrote {a.out}: {dict(counts)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
