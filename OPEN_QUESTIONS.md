# Open Questions and Assumptions

No answers were requested; each item has the assumption used so far.

| ID | Question | Assumption used |
|---|---|---|
| Q-001 | Official problem statement requirements? | Not supplied; working definition only ([PRD.md](PRD.md)) |
| Q-002 | Which components/classes must be checked? | **Decided:** whatever classes the chosen public dataset contains (chosen: Roboflow *Electrical Devices* by FieldSnap Pro, subject to license check; `hi-wxre3` rejected: thermal images); demo limited to them |
| Q-003 | Format of expected configuration? | CSV/XLSX with columns `item_id, component_class, tag, quantity, zone, notes`; PDF best-effort |
| Q-004 | Should "not detected" be FAIL or REVIEW? | REVIEW by default (non-detection is not proof); configurable policy later |
| Q-005 | Can cabinet photos be used for training and shown in a demo? | **Decided:** public datasets only, no own data collection; dataset licenses must still be checked (attribution for CC BY) |
| Q-006 | Project license? | Undecided ([LICENSE.md](LICENSE.md)) |
| Q-007 | Is Ultralytics AGPL acceptable for the competition/product plan? | Unknown; acceptable for a local prototype, review before distribution |
| Q-008 | Required report format/content? | Simple PDF with checks, evidence, model version, reviews |
| Q-009 | Number of photos per cabinet and camera angles? | 1–10 mostly frontal photos |
| Q-010 | OCR engine choice? | EasyOCR baseline; confirm by a Phase 7 spike |
| Q-011 | Multi-user/authentication needed? | No (single local user) |
| Q-012 | Inspection time target? | Proposed only; measure |
