# Naming Conventions

Names must be **sortable, searchable, unambiguous, portable** (Windows/macOS/Linux, SPSS,
Stata, R, Python) and must **say what version** a file is — never `final`, `latest` or `new`.

## 1. General rules (all files and folders)

1. Lowercase, `snake_case`, ASCII letters/digits/underscore/hyphen/dot only.
2. **No spaces, no Arabic characters, no special characters** in file names
   (Arabic content inside files is fine; see [LANGUAGE_POLICY.md](LANGUAGE_POLICY.md)).
3. Dates are ISO 8601: `YYYY-MM-DD` in documents, `YYYYMMDD` inside data file names.
4. Versions are explicit: `v<MAJOR>.<MINOR>` (e.g. `v1.2`). Zero-pad sequence numbers (`01`, `02`).
5. Maximum ~60 characters. Put the most important element first.
6. Exceptions: conventional upper-case docs (`README.md`, `CONTRIBUTING.md`, `DATA_DICTIONARY.md`, …).

## 2. Forbidden names (rejected by CI)

`final`, `final2`, `final_final`, `latest`, `new`, `new2`, `copy`, `copy_of_…`, `old`, `temp`,
`untitled`, `test123`, `v2_final`, `(1)`, names with spaces or non-ASCII characters.

Why: they carry no information, and "final" is never final. Git already keeps history,
and versions/tags say which file is authoritative.

## 3. Patterns by file type

| Type | Pattern | Example |
| --- | --- | --- |
| Raw data (secure storage) | `<short>_raw_<source>_<YYYYMMDD>.<ext>` | `[short]_raw_platform_20260115.csv` |
| Stage data (secure storage) | `<short>_<stage>[_<desc>]_v<MAJOR.MINOR>.<ext>` | `[short]_cleaned_v1.0.csv`, `[short]_processed_weighted_v1.2.csv`, `[short]_analysis_ready_v1.3.csv` |
| Pipeline scripts | `<NN>_<verb>_<object>.<ext>` in `03_scripts/<NN>_<stage>/` | `02_clean.py`, `07_crosstabs.R` |
| Helper modules | `<noun>_utils.<ext>` in `03_scripts/_lib/` | `stats_utils.py` |
| Rule files | `<purpose>.csv` next to their script | `cleaning_rules.csv`, `recode_map.csv` |
| Analysis tables | `tab_<type>_<vars>.csv` | `tab_desc_region.csv`, `tab_xtab_trust_by_sex.csv` |
| Figures | `fig_<type>_<vars>.<svg/png>` | `fig_desc_region.svg` |
| QC reports | `<NN>_<check>_v<ver>.csv` | `02_cleaning_log_v1.0.csv` |
| Meeting minutes | `YYYY-MM-DD_meeting_<topic>.md` | `2026-03-04_meeting_weighting.md` |
| Decision records | `DR-<NNN>_<short-title>.md` | `DR-007_exclude_short_interviews.md` |
| Questionnaire | `questionnaire_<lang>_v<MAJOR.MINOR>.<ext>` | `questionnaire_ar_v1.0.docx` |
| Report drafts | `<short>_report_<part>_v<MAJOR.MINOR>.<ext>` | `[short]_report_full_v0.3.docx` |
| Final report | `<short>_report_<lang>_v<MAJOR.MINOR.PATCH>.pdf` = release tag | `[short]_report_en_v1.0.0.pdf` |
| Branches | `<type>/<issue>-<kebab-desc>` | `data/12-recode-education` |
| Tags | `vMAJOR.MINOR.PATCH`; approved docs `protocol-vX.Y`, `sap-vX.Y` | `v1.0.0`, `sap-v1.0` |

`<short>` = `[PROJECT_SHORT_NAME]` (e.g. study acronym + year, lowercase).

## 4. Replacing the "final_final" habit

| Instead of … | Use … |
| --- | --- |
| `final.xlsx`, `final2.xlsx` | `[short]_analysis_ready_v1.0.csv`, then `…_v1.1.csv` |
| `latest.xlsx` | the version referenced in `config/project.yml` + `DATA_MANIFEST.csv` |
| `report new.docx` | `[short]_report_full_v0.4.docx` |
| `questionnaire (1).docx` | `questionnaire_en_v0.3.docx` |

## 5. Variables

See [DATA_DICTIONARY.md §1](../../02_data/data_dictionary/DATA_DICTIONARY.md#1-conventions):
English `snake_case`, ≤ 32 chars, starting with a letter; question-based prefix `q12_…` where useful;
derived variables descriptive (`age_group`, `idx_trust`); weights `weight_*`; flags `flag_*`.
