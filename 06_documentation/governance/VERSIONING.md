# Versioning

Two related version numbers are used:

| What | Format | Where | Example |
| --- | --- | --- | --- |
| **Project release** (code + docs + outputs) | `vMAJOR.MINOR.PATCH` | Git tag, GitHub Release, CHANGELOG | `v1.2.0` |
| **Dataset version** | `vMAJOR.MINOR` | `config/project.yml` → file names → `DATA_MANIFEST.csv` | `…_analysis_ready_v1.3.csv` |

Each project release states in CHANGELOG which dataset version it used — that is the link
between code and data.

## 1. Project releases (Semantic Versioning adapted to research)

| Increment | When | Examples |
| --- | --- | --- |
| **MAJOR** `X.0.0` | A change that makes previously released results **not comparable** or a major deliverable is published | `v1.0.0` final report results; new data wave; change of weighting method; protocol amendment affecting estimates; change of indicator definitions |
| **MINOR** `1.X.0` | New content that **adds** without invalidating released results | new analysis chapter, new tables/figures, new derived variables, a policy brief, a de-identified public dataset |
| **PATCH** `1.0.X` | Corrections that **do not change substantive conclusions** | typo/label fixes, documentation, rounding display, a coding error affecting < [threshold] with no change in conclusions (documented) |

- `0.y.z` = work in progress before the first approved deliverable. Suggested milestones:
  `v0.1.0` repository set up · `v0.2.0` protocol & questionnaire approved · `v0.3.0` fieldwork completed, raw data received ·
  `v0.4.0` cleaned & weighted data · `v0.5.0` analysis complete · `v0.9.0` report draft for review · `v1.0.0` final.
- Any correction that changes a published number is **at least MINOR** and must be listed
  under *Results* in CHANGELOG with the old and new value (erratum).

## 2. Dataset versions

| Increment | When |
| --- | --- |
| MAJOR `X.0` | new raw delivery or wave; cleaning/exclusion rule changing which records are kept |
| MINOR `1.X` | recodes, derived variables, weights, corrections that keep the same records |

Set `data.dataset_version` in `config/project.yml` in the same PR that changes the rules,
re-run the pipeline, commit the updated `DATA_MANIFEST.csv`.

## 3. Documents

Protocol, analysis plan, questionnaire, DMP: `vMAJOR.MINOR` in the document header;
approved versions are also tagged: `protocol-v1.0`, `sap-v1.0`, `questionnaire-v1.0`.

## 4. How to release

See [RELEASE_PROCESS.md](RELEASE_PROCESS.md).
