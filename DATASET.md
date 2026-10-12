# Dataset Research and Selection

Research date: **2026-10-11**, via web search of public pages. **Verification level used here:** "page seen" means the dataset page or its mirror was seen in search results and the stated facts were read there. **No dataset was downloaded, opened, inspected for label quality, or trained on.** Every license must be re-read on the original page before use. Related: [DATASET_CARD.md](DATASET_CARD.md), [DATA_ANNOTATION.md](DATA_ANNOTATION.md), [MODEL_TRAINING.md](MODEL_TRAINING.md).

## Chosen plan: public datasets only (no own data collection)
The project owner decided **not to collect or annotate their own data** and to use public datasets from Roboflow Universe (and Kaggle if available). Consequences, stated plainly:
- Training is possible with a suitable colour-photo dataset, and the full pipeline (Colab -> `best.pt` -> FastAPI) can be completed.
- The model will only know the classes inside the chosen public datasets. The demo must be limited to those classes.
- Results are a **proof of concept**; accuracy on real cabinets is unmeasured and likely lower. Say so in the viva.
- **Kaggle:** a search on 2026-10-11 found no relevant Kaggle dataset. Search Kaggle yourself ("electrical panel", "switchgear", "DIN rail"); apply the same checks.

### CORRECTION (2026-10-11): `hi-wxre3` is NOT suitable
The owner opened `hi-wxre3` and found its images are **thermal (infrared) images** (false-colour heat pictures, file names ending `_ir`, boxes around hot cables/components). That is a different image domain from normal colour cabinet photos; a model trained on it will not work on RGB photos. The earlier recommendation was made from page text only, without seeing images. **Do not use it for this project** (do not mix it with colour datasets either). Lesson: always look at the images before downloading.

### Step 0 for EVERY dataset: look at the images first (2 minutes)
On the dataset page click **Images** (or Dataset) and scan the thumbnails with "Show Annotations" on. Accept only if:
- Normal **colour photos** (not thermal, not schematics/drawings, not isolated product shots on white background).
- Show **open panels/cabinets with components** (breakers, contactors, terminal blocks) similar to what you will demo.
- Boxes look tight and consistent; class names are clear (no duplicates like two spellings of the same part).
- Enough instances per class (aim for 100+ per class; fewer works only as a proof of concept).
Then record license and class list in [DATASET_CARD.md](DATASET_CARD.md).

### Owner review: Electrical Devices (user FieldSnap Pro) — passes the image check, with caveats
Source: https://universe.roboflow.com/fieldsnap-pro (open the **Electrical Devices** project). From a screenshot of its images (owner-provided, 2026-10-11): normal colour photos of real panels; capacitor banks, fuses, MCB rows, panel fans, cables are visible.
Caveats seen in the screenshot:
- **Many boxes cover a group** (a row of fuses or MCBs, a whole capacitor bank), so per-item counting is unreliable. In the demo, prefer presence checks (R-001); treat count checks (R-002) as indicative only and expect `REVIEW`.
- Mixed image sources: catalogue shots on white backgrounds (fans), dark/blurry images, internet-style photos.
- Class list per search listing: about 17 classes (e.g., Active-Harmonic-Filters, Air-Circuit-Breakers, Bus-Bar, Capacitors, Contactors, Fuses, MCB, Panel-Fans, Phase-Reactor, Power-Cable); the full list and per-class counts are **unverified**. Open the project's class/health-check view, then **train on the 4-6 classes with the most instances** (drop or relabel the rest) and say this in the model card.
- **License: CC BY 4.0** (seen in an owner-provided screenshot of the project page: author "VIT", 1,163 images, 6 dataset versions, 2 models). CC BY 4.0 requires **attribution**: credit the author and Roboflow Universe and link the source (see THIRD_PARTY_NOTICES.md). Not legal advice.
- The page also shows a Roboflow-trained model with mAP@50 79.5%, precision 82.8%, recall 71.4%. These are **the dataset author's numbers on their own validation data**, not results of this project, and they say nothing about performance on your cabinets. Do not quote them as Eagle Eye's accuracy.
- **Class list (owner screenshot of Classes & Tags, whole dataset, 10 classes, box counts):** Bus-Bar 447, Contactors 371, Fuses 331, Capacitors 307, Power-Cable 182, Phase-Reactor 181, Air-Circuit-Breakers 175, Panel-Fans 161, MCB 120, Active-Harmonic-Filters 105. **Decision: keep all 10** (every class has at least 105 boxes); no class remapping. Counts are before the train/valid/test split, so per-split counts are lower. Expect MCB and Active-Harmonic-Filters to be weakest; report per-class metrics. Class IDs: always read them from the export's `data.yaml`, never assume.
- **Validator finding on the real download (owner-run, v-clean export, 949/122/92 train/valid/test images):** 23 cross-split LEAKAGE errors and 71 duplicate warnings. The same source picture exists as several identical copies (different `.rf.<hash>` names) and some copies sit in train while others sit in valid or test. Training on this split would inflate validation and test scores. **Fix before training:** run `python scripts/dataset/dedupe_and_resplit.py --src data/raw/electrical-devices --dst data/processed/electrical-devices-dedup`, then validate the new folder (expect 0 errors) and use it for Colab. The unique image count and per-class counts after de-duplication are **unknown until the script is run**; classes that end up with too few valid/test instances should be dropped or reported as weak. The script was tested on synthetic data only.
- **Version choice (owner screenshot of the Dataset tab):** v6 has 2,870 images (train 2,656 / valid 122 / test 92), Auto-Orient, resize stretch to 640x640, **Grayscale applied**, and Roboflow augmentation (3 outputs per training image, horizontal flip, bounding-box flips horizontal+vertical). **Reject v6**: grayscale does not match colour photos, and vertical flips are unrealistic; Ultralytics adds its own augmentation during training. Other versions listed: v5 2,872 images, v4 1,710, v3 1,514, v2 1,503, v1 960 (their preprocessing was not visible). **Preferred route:** *Fork Dataset* into your own Roboflow workspace and generate a new version with Auto-Orient only (or resize "fit within 640x640"), **no Grayscale, no augmentation**, unwanted classes removed via Modify Classes, then export as **YOLOv11** (Ultralytics label format; check the export has train/valid/test folders and `data.yaml`).

### Candidates to inspect now (search these names on https://universe.roboflow.com; image type NOT verified for any of them)
| Candidate (search name) | Seen in Roboflow search listings | License | Notes |
|---|---|---|---|
| **Control Panels** (by "Control Panel Azure") | 320 images; classes include circuit breaker 1-pole/2-pole/3-pole, contactor, RCBO, NH-fuse, electric meter, CEE socket | Not seen | German-style distribution boards; promising class set. Exact project URL not captured: search the name |
| **Electrical Devices** (FieldSnap Pro, https://universe.roboflow.com/fieldsnap-pro) | 1.16k images; classes include air circuit breakers, bus bar, capacitors, contactors, fuses, MCB, panel fans, power cable | Not seen | Industrial equipment; may be many classes with few examples each |
| **breaker phase 2** (user braker-p7qyl, https://universe.roboflow.com/braker-p7qyl) | 210 images; 1/2/3/4-pole circuit breaker | Not seen | Breaker types only |
| **panel 3** (https://universe.roboflow.com/yolov8-ggh2w/panel-3) | classes breaker, SD-T50, Terminal Block | Not seen | The page URL returned 404 when fetched; search the name |
| **Audit Panel** | 597 images; classes include breaker, wires L1/L2/L3, panel ampere rating | Not seen | Wire-related labels, possibly useful for later |
| **Circuit Breakers** (Enconnex, https://universe.roboflow.com/enconnex/circuit-breakers) | 40 images | CC BY 4.0 (seen) | Too small except as a supplement |
| Terminal strips (Zenodo via https://www.th-owl.de/elsa/record/13824.yaml) | 30,000 synthetic + 300 real images, 36 terminal-block types | Not seen | Targets DIN-rail terminal strips; synthetic images |

**Recommendation:** pick **one** dataset that passes Step 0 (the owner chose *Electrical Devices*, which passed the image check; *Control Panels* is the fallback), train a baseline on it alone, and add others only later by class name. These are guesses from listing text, not verified choices.

### How to download from Roboflow (beginner steps)
1. Create a free account at https://roboflow.com and open the dataset link.
2. Read the **License** and the **class list** on the page. Write them in [DATASET_CARD.md](DATASET_CARD.md).
3. Click **Dataset** (or **Download Dataset**) -> choose an Ultralytics YOLO format (e.g., "YOLOv8" or a newer YOLO option) -> **Download zip to computer**.
4. If a version has no train/valid/test split, use the version that has one.

### Where to put the files
```text
eagle-eye/data/raw/<dataset-name>/    <- unzip the Roboflow zip HERE
    data.yaml
    train/images  train/labels
    valid/images  valid/labels
    test/images   test/labels          (only if the export contains a test split)
    README.dataset.txt  README.roboflow.txt   (read the license here too)
```
`data/raw/*` is git-ignored, so the dataset is never committed. Check it:
```powershell
python scripts/dataset/validate_yolo_dataset.py --root data/raw/<dataset-name> --nc <number of classes in data.yaml>
```
For Colab: zip the **contents** of `data/raw/<dataset-name>` (so `data.yaml` sits at the top of the zip), upload it to Google Drive, and follow [MODEL_TRAINING.md](MODEL_TRAINING.md) (Option A in Cell 4). Do not use real confidential images this way; these are public datasets.

### Extra candidates found on 2026-10-11 (page seen, not downloaded; licenses and classes unconfirmed)
| Source | URL | Seen on page |
|---|---|---|
| Switch-gear-cabinet-parts (user g-ndd4b) | https://universe.roboflow.com/g-ndd4b | 118 images, YOLO11 models listed |
| SWITCH GEAR (winsheild) | https://universe.roboflow.com/winsheild/switch-gear-vqhoc | sample classes: label, a high-voltage measurement and control unit, a push-button |
| FieldSnap Pro projects (Electrical Devices 1.16k, Main Breaker 520) | https://universe.roboflow.com/fieldsnap-pro | image counts only |

## Bottom line
1. **No comprehensive public cabinet-QC dataset was verified.** Public Roboflow Universe projects are small, community-made, with inconsistent class names. None is shown here to cover a full cabinet with consistent QC classes.
2. A **custom, authorised, consistently annotated cabinet dataset** would be better for a credible product, but the owner chose public data only; see the chosen plan above.
3. Public sets are useful for a **pipeline smoke test** and, with care, as **supplementary data**.
4. Three data domains must not be mixed: **cabinet photographs**, **isolated component photographs**, and **electrical drawings/schematics**. They look completely different to a model.

## Candidates (all "page seen", none downloaded)
| # | Dataset | Source URL | License (as seen) | Size (as seen) | Classes (as seen) | Domain / suitability |
|---|---|---|---|---|---|---|
| 1 | hi (project `hi-wxre3`) | https://universe.roboflow.com/ssar/hi-wxre3 | CC BY 4.0 | 184 images | Classes: Circuit Breaker, Contactor, Electrical Cabinet, Electrical Cable | **NOT SUITABLE: thermal (infrared) images**, confirmed by the owner viewing the images |
| 2 | panel 3 | https://universe.roboflow.com/yolov8-ggh2w/panel-3 | **Not seen on page snippet — check** | Not seen | breaker, SD-T50, Terminal Block | Likely panel/DIN-rail style. Promising supplementary data **after license check**. "SD-T50" is a product-specific label |
| 3 | Terminal block (user `braker-p7qyl`) | https://universe.roboflow.com/braker-p7qyl | Not seen — check each project | 90 images (terminal block); 210 (breaker phase 2); 230 (braker3); 18 (high voltage) | Not seen | Supplementary candidates; individual project pages need review |
| 4 | circuit breaker | https://universe.roboflow.com/mytest-xesat/circuit-breaker | Not seen | 18 images | Not seen | Too small except for a trivial smoke test |
| 5 | Circuit Breakers | https://universe.roboflow.com/chirine/circuit-breakers-crbki | CC BY 4.0 | Not seen | Page lists sample classes: Product, 2P, Ambient-Rating | Breaker-focused; possibly product images (isolated domain). Unverified |
| 6 | Electrical Components | https://universe.roboflow.com/khaledrakhisis-workspace/electrical-components-8v8ak | Not seen | 211 images (version 6) | Not seen | Unknown domain; inspect before use |
| 7 | meter-cabin | https://universe.roboflow.com/viny/meter-cabin | Not seen | Not seen | 14 listed, incl. fuse, terminal block variants, Main supply relay, overvoltage protection, Cabin box; **duplicate/near-duplicate names** (e.g., "fuse" twice, two "terminal block" spellings) | Telecom/meter cabin context; class cleanup required; domain differs from control cabinets |
| 8 | Electrical Panels Detection Dataset (Hugging Face) | https://huggingface.co/datasets/sriom1/electrical-panels-dataset | Not seen | Not seen | YOLO-format `.txt` labels with numeric IDs up to at least 106 (observed in preview); **names not seen** | Possibly the broadest, but class names unknown and viewer errored. Investigate manually |
| 9 | Electrical equipments | https://universe.roboflow.com/electricaltest01-yiuvf/electrical-equipments-umhl8 | CC BY 4.0 | Not seen | Sample classes: speaker, 120V receptacles (building electrical plans) | **Not suitable** (building drawings domain) |
| 10 | circuitObjectsDetection | https://universe.roboflow.com/proyetos/circuitobjectsdetection-pa4wi | CC BY 4.0 | Not seen | Switch, Resistor, Capacitor (sample) | Circuit components/schematics. **Not suitable** for cabinets |
| 11 | bmo | https://universe.roboflow.com/bom-mvv0o/bmo | CC BY 4.0 | Not seen | 31 classes of schematic symbols (breakers, relays, transformers…) | **Drawing domain** — do not mix with photos |
| 12 | RF100 circuit-elements | https://universe.roboflow.com/roboflow-100/circuit-elements (mirror: https://huggingface.co/datasets/Francesco/circuit-elements) | CC BY 4.0 | Not seen | Single class "circuit" | PCB-style; **not suitable** |
| 13 | AITEE Electrical Circuit Dataset | https://github.com/CKnievel/aitee-dataset | Not seen | 831 circuit diagrams (per a third-party index page) | Components/connection points in diagrams | **Drawing domain**; possible later use for GA/drawing parsing research, not for photo detection |

Facts labelled "as seen" were read from search-result page content; license strings on Roboflow pages can change by version.

## Recommended strategy
- **Fastest baseline:** the first candidate that passes Step 0 above (not `hi-wxre3`, which is thermal). Treat metrics as proof of concept only.
- **Possible supplements:** #2, #3 (and #8 if its names and license are confirmed). Only add after (a) license is confirmed permissive for your use, (b) visual inspection of 50+ images, (c) class mapping is written down.
- **Better option if ever possible (not the chosen plan):** photograph authorised cabinets (or lab mock-ups), define a **small** class list matching the checks you will actually demo, annotate consistently ([DATA_ANNOTATION.md](DATA_ANNOTATION.md)), split **by cabinet**, fine-tune, evaluate on held-out cabinets.
- **Which classes are actually supported?** Only those you verify in the downloaded `data.yaml` and label files. The classes in the `MODEL_TRAINING.md` YAML (breaker, relay, terminal_block) are **illustrative**. Verified-supported classes today: none, because nothing was downloaded.

## Avoiding incompatible class definitions
1. Write a `class_map.csv` (`source_dataset, source_name, target_name`) for every source.
2. Never merge by class ID; always remap via names.
3. Drop or relabel unmapped classes; do not leave them as background silently.
4. Re-run `scripts/dataset/validate_yolo_dataset.py` after merging.
5. Review a sample overlay per source to catch label-semantics mismatches (e.g., "breaker" meaning MCB vs MCCB vs symbol).

## Licensing notes
- CC BY 4.0 (seen on several pages) generally permits reuse **with attribution**; confirm on the original page and keep the citation. This is not legal advice.
- Datasets with no license seen: treat as **not cleared**; exploratory use only until confirmed, or contact the author.
- A public download is not automatically approved for commercial use.
- Roboflow Universe exports usually need a free account and API key. Keep keys in Colab Secrets, never in notebooks.
- **Do not upload confidential cabinet photos or engineering documents to Roboflow, Colab, or any third-party service without authorisation.** If your photos are confidential, annotate locally (e.g., CVAT/Label Studio self-hosted) and use a private Drive or a local GPU.

## How to download (template)
Roboflow: open the project page → Dataset → Download → choose an Ultralytics-compatible YOLO format → "show download code" for Colab (use a Colab secret for the key). Hugging Face: `huggingface_hub` or `git lfs`. Verify the result with the validator script and inspect `data.yaml`.
