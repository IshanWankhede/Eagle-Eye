# License

**Decision pending: no license has been selected for Eagle Eye.** Until one is added, the default legal position is "all rights reserved" by the author(s): others may not legally reuse the code. No copyright holder name is asserted here (to be filled by the project owner).

## Options (not legal advice)
| Option | Effect | Consider when |
|---|---|---|
| MIT / Apache-2.0 | Permissive reuse | You want wide adoption. **But** dependencies matter (below) |
| GPL-3.0 / AGPL-3.0 | Copyleft; derivative works must share source (AGPL covers network use) | You want reciprocity; compatible with AGPL dependencies |
| Proprietary / none | You keep control | Competition IP rules or employer rules apply |

## Interactions to check before choosing
- **Ultralytics** is AGPL-3.0 with a paid enterprise alternative (see https://pypi.org/project/ultralytics/). Distributing or offering the app as a network service with Ultralytics code/weights may trigger AGPL obligations unless an enterprise license is obtained.
- **PyMuPDF** is AGPL/commercial dual-licensed (verify); `pdfplumber` is an alternative.
- Datasets and weights keep **their own** licenses; the project license does not apply to them ([THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)).
- Competition or institution rules may claim rights over submissions; check them.

When decided, replace this file with the license text and update README, CONTRIBUTING and THIRD_PARTY_NOTICES.
