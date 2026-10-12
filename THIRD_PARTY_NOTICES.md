# Third-Party Notices

Only facts actually seen during research are stated as verified; everything else is **to verify** before distribution. Date: 2026-10-11. Project license is undecided ([LICENSE.md](LICENSE.md)).

## Software (licenses to confirm from each package's own metadata at install time)
| Component | License | Status |
|---|---|---|
| Ultralytics (YOLO) | AGPL-3.0 and Enterprise License (stated on https://pypi.org/project/ultralytics/) | Verified from PyPI page text; legal implications need review |
| FastAPI, Pydantic, Uvicorn, SQLAlchemy | Not verified here | To verify |
| React, Vite, Tailwind CSS, TypeScript | Not verified here | To verify |
| OpenCV, EasyOCR, PyMuPDF, pandas, openpyxl, ReportLab, PyTorch | Not verified here (PyMuPDF believed AGPL/commercial) | To verify |

After the first install, generate the real list: `pip-licenses` and `npx license-checker` and paste results here.

## Pretrained model weights
`yolo11n.pt` / `yolo26n.pt` are distributed by Ultralytics; licensing follows Ultralytics terms (AGPL-3.0/enterprise). Not bundled in this repo.

## Datasets (none bundled)
**Electrical Devices** (author: VIT, Roboflow Universe workspace page https://universe.roboflow.com/fieldsnap-pro), license **CC BY 4.0** per the project page (seen by the owner). Attribution required in any publication, demo material or model card that uses it. Keep the citation text shown on the dataset page (it offers a BibTeX block).

Others:
See [DATASET.md](DATASET.md) for the per-dataset license as seen on source pages (CC BY 4.0 seen for several; many unseen). Attribution to dataset authors is required where the license demands it. A trained model derived from a dataset may inherit usage obligations; verify.

## Other
No third-party images, drawings or documents are included in this package. `data/samples/expected_components.example.csv` is fictional.
