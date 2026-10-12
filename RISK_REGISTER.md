# Risk Register

Likelihood/Impact: L/M/H (judgement, not measured).

| ID | Risk | L | I | Mitigation | Fallback |
|---|---|---|---|---|---|
| R-01 | Public datasets are small/inconsistent and own data will not be collected ([DATASET.md](DATASET.md)) | H | H | Start from one verified-license dataset; limit demo to its classes; state limits | Next dataset in DATASET.md; mark weak classes unsupported |
| R-02 | Detector underperforms | M | H | Fine-tune, measure, tune thresholds | Mark weak classes unsupported → REVIEW |
| R-03 | Overfitting / leakage inflates metrics | M | H | Split by cabinet; one-time test | Report honestly |
| R-04 | PDF/Excel variability breaks parsing | H | M | Strict CSV/XLSX schema; PDF best-effort | Require CSV |
| R-05 | Time overrun | H | H | Phase order, P0 first | Cut P1/P2 |
| R-06 | Confidential data exposure | M | H | Local-only, authorisation, no third-party upload | Synthetic data |
| R-07 | Licensing (Ultralytics AGPL, dataset licenses) | M | M | Track in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md); decide license | Use alternative detector/enterprise license |
| R-08 | Unlabelled false PASS misleads users | L | H | Unsupported/insufficient → REVIEW; tests | Human sign-off required |
| R-09 | Colab disconnects / quota | M | M | Save to Drive; resume | Local/other GPU |
| R-10 | Dependency install problems on Windows | M | M | Pin after first success; Python 3.11 | Use WSL or Colab for ML |
| R-11 | Demo machine too slow | M | M | Measure early; small model; resize images | Pre-computed demo results |
