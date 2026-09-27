# Reproducible Pipeline

```text
 Raw Data ($DATA_ROOT/raw)                                  C3 — secure storage only
    │  01 Validation        01_validate_raw.py      → qc_reports/01_validation_report   (+ raw SHA-256 frozen)
    ▼
 Cleaning                   02_clean.py + cleaning_rules.csv
    │                       → $DATA_ROOT/cleaned/…_cleaned_vX.Y   (pseudonymised; identifiers → restricted/)
    ▼
 Recoding / derivation      03_recode.py + recode_map.csv
    │                       → $DATA_ROOT/processed/…_processed_recoded_vX.Y
    ▼
 Weighting                  04_weight.py + weighting_targets.csv
    │                       → $DATA_ROOT/processed/…_processed_weighted_vX.Y
    ▼
 Analysis dataset           05_build_analysis_dataset.py (dictionary: in_analysis)
    │                       → $DATA_ROOT/analysis_ready/…_analysis_ready_vX.Y
    ▼
 Statistical analysis       06_descriptives.py · 07_crosstabs.py · (models → statistical_outputs/)
    ▼
 Tables                     04_analysis/tables/tab_*.csv            (Git — aggregate, suppressed)
    ▼
 Figures                    08_figures.py → 04_analysis/figures/fig_*.svg|png   (built from tables)
    ▼
 Report                     05_reports/drafts → reviewed → final     (every number traceable to a table)
```

## 1. Stage contract

| # | Stage | Input | Output | Documentation produced | Reviewer |
| --- | --- | --- | --- | --- | --- |
| 01 | Validation | raw files in config | QC report; raw rows in manifest | `01_validation_report_v*.csv` | Data Manager |
| 02 | Cleaning | raw | cleaned + restricted identifiers | `02_cleaning_log_v*.csv`, [CLEANING_LOG.md](CLEANING_LOG.md) | Data Manager |
| 03 | Recoding | cleaned | processed (recoded) | `03_recode_log_v*.csv`, dictionary | Data Manager + Analysis Lead |
| 04 | Weighting | processed (recoded) | processed (weighted) | `04_weighting_qc_v*.csv` | Methodology Lead |
| 05 | Analysis dataset | processed (weighted) | analysis_ready | `05_analysis_dataset_qc_v*.csv` | Data Manager |
| 06 | Descriptives | analysis_ready | `tab_desc_*.csv` | Analysis Plan §5 | Analysis Lead |
| 07 | Comparative | analysis_ready | `tab_xtab_*.csv` | Analysis Plan §6 | Analysis Lead |
| 08 | Figures | tables | `fig_*.svg/png` | — | Report Lead |

Principles:

1. **Deterministic** — same inputs + same code ⇒ byte-identical outputs (fixed seeds, sorted output).
2. **Forward only** — a stage reads only the previous stage; never edits its input.
3. **Rules as data** — decisions live in reviewed CSV rule files, not in ad-hoc code edits.
4. **Explicit versions** — scripts read the file for the configured `dataset_version`, never "the newest file".
5. **Aggregate outputs only in Git** — QC reports and tables contain counts/percentages, not rows.

## 2. Running

```bash
python 03_scripts/run_pipeline.py --list        # stages
python 03_scripts/run_pipeline.py               # everything
python 03_scripts/run_pipeline.py --from 03     # from recoding on
python 03_scripts/run_pipeline.py --only 06     # one stage
```

After a run: review `04_analysis/qc_reports/`, then commit scripts, rule files, the manifest and
aggregate outputs in a PR (`git status` shows exactly what changed).

## 3. Organising analysis code by language

The pipeline skeleton is in Python. Teams using other tools keep **the same numbered
structure and the same rule files**, so the stage contract above does not change:

| Tool | Organisation | Reproducibility tooling |
| --- | --- | --- |
| **Python** | `03_scripts/NN_stage/NN_verb.py`, shared code in `_lib/`, runner `run_pipeline.py` | `requirements.txt` + `pip freeze > requirements.lock.txt`; optional `Makefile`/`snakemake` |
| **R** | `03_scripts/NN_stage/NN_verb.R`; functions in `03_scripts/_lib/R/`; runner `run_pipeline.R` (`source()` in order) or `{targets}` | `renv` (`renv.lock` committed), `here::here()` for paths, `survey`/`srvyr` for design-based estimates |
| **Stata** | `03_scripts/NN_stage/NN_verb.do`; master `run_pipeline.do` with `version 18` and `set seed` | `log using` to `logs/` (git-ignored), `svyset` defined once in stage 05 |
| **SPSS** | `03_scripts/NN_stage/NN_verb.sps` (syntax only — **never** point-and-click without pasting syntax); master `run_pipeline.sps` with `INSERT FILE=` | `SET UNICODE=ON`; save syntax + output tables, not `.spv` with microdata |

Mixed teams: the **data** stages (01–05) should be in one language owned by the Data Manager;
analysis stages (06–08) may be in another, reading the same `analysis_ready` file.

Paths: never hard-code `C:\Users\…`. Read `DATA_ROOT` from the environment (`.env`) and build
paths relative to the repository root.

## 4. Reproducing a released result

```bash
git checkout v1.0.0
pip install -r requirements.lock.txt   # or requirements.txt
python tools/data_manifest.py verify   # confirms local data == data used for v1.0.0
python 03_scripts/run_pipeline.py
git status                             # must show no differences in 04_analysis/
```
