# 02_data — data stages

**Data files are NOT stored here.** They live in the secure storage
`$DATA_ROOT` = **[SECURE_STORAGE_LOCATION]** with the same sub-folders.
This folder documents each stage and holds the metadata that makes the data traceable.

```text
$DATA_ROOT/                       (secure storage — outside Git)
├── raw/             C3  original exports, read-only, never edited
├── restricted/      C3  linking key + direct identifiers (Data Manager only)
├── cleaned/         C2  pseudonymised, errors corrected by documented rules
├── processed/       C2  recoded, derived variables, merged, weighted
└── analysis_ready/  C2  final analysis file (only in_analysis variables)

02_data/                          (this repository)
├── raw/ cleaned/ processed/ analysis_ready/   README per stage (what, who, how)
├── analysis_ready/approved_deid/  the ONLY place a data file may be committed (Git LFS, §4 DATA_SECURITY.md)
├── metadata/DATA_MANIFEST.csv     every data file: version, SHA-256, rows, script, commit
└── data_dictionary/               DATA_DICTIONARY.md + data_dictionary.csv (official)
```

## Stage transitions

| From → To | Script | Rules file | Log / QC report | Approver |
| --- | --- | --- | --- | --- |
| raw → (validated) | `03_scripts/01_validation/01_validate_raw.py` | data dictionary | `04_analysis/qc_reports/01_validation_report_v*.csv` | Data Manager |
| raw → cleaned | `03_scripts/02_cleaning/02_clean.py` | `cleaning_rules.csv` | `02_cleaning_log_v*.csv` | Data Manager |
| cleaned → processed | `03_scripts/03_recoding/03_recode.py` | `recode_map.csv` | `03_recode_log_v*.csv` | Data Manager + Analysis Lead |
| processed → processed (weighted) | `03_scripts/04_weighting/04_weight.py` | `weighting_targets.csv` | `04_weighting_qc_v*.csv` | Methodology Lead |
| processed → analysis_ready | `03_scripts/05_analysis_dataset/05_build_analysis_dataset.py` | dictionary `in_analysis` | `05_analysis_dataset_qc_v*.csv` | Data Manager |

No manual step exists between stages. If something cannot be scripted, it is written
as a rule, reviewed in a PR and logged in `06_documentation/analysis_documentation/CLEANING_LOG.md`.
