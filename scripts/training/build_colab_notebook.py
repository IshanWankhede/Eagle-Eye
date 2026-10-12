"""Generate notebooks/eagle_eye_yolo_training.ipynb from the python code blocks in MODEL_TRAINING.md.

Usage (from repo root): python scripts/training/build_colab_notebook.py
Only fenced blocks directly under '### Cell N' headings are converted (one code cell each).
"""
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parents[2]
text = (root / "MODEL_TRAINING.md").read_text(encoding="utf-8")
sections = re.split(r"^### (Cell \d+[^\n]*)\n", text, flags=re.M)
cells = [{"cell_type": "markdown", "metadata": {}, "source": [
    "# Eagle Eye YOLO training (generated from MODEL_TRAINING.md)\n",
    "Template only: edit marked variables. Do not paste credentials; use Colab Secrets."]}]
for i in range(1, len(sections), 2):
    title, body = sections[i], sections[i + 1]
    m = re.search(r"```python\n(.*?)```", body, flags=re.S)
    if not m:
        continue
    cells.append({"cell_type": "markdown", "metadata": {}, "source": [f"## {title}"]})
    cells.append({"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [],
                  "source": m.group(1).rstrip("\n").splitlines(keepends=True)})
nb = {"cells": cells, "metadata": {"accelerator": "GPU", "colab": {"provenance": []},
      "kernelspec": {"name": "python3", "display_name": "Python 3"}}, "nbformat": 4, "nbformat_minor": 5}
out = root / "notebooks" / "eagle_eye_yolo_training.ipynb"
out.write_text(json.dumps(nb, indent=1), encoding="utf-8")
print(f"wrote {out} with {sum(c['cell_type'] == 'code' for c in cells)} code cells")
