# 03_scripts — the reproducible pipeline

```text
03_scripts/
├── run_pipeline.py                  runs stages in order; --from / --only / --list
├── _lib/                            shared helpers (paths, IO, manifest, statistics)
├── 01_validation/                   01_validate_raw.py
├── 02_cleaning/                     02_clean.py + cleaning_rules.csv
├── 03_recoding/                     03_recode.py + recode_map.csv
├── 04_weighting/                    04_weight.py + weighting_targets.csv
├── 05_analysis_dataset/             05_build_analysis_dataset.py
├── 06_descriptive_analysis/         06_descriptives.py
├── 07_comparative_analysis/         07_crosstabs.py
└── 08_visualization/                08_figures.py
```

Rules:

1. Scripts never write inside `02_data/` except the manifest; data go to `$DATA_ROOT`.
2. Scripts read **only** from the previous stage and from reviewed rule files.
3. No manual steps. If something cannot be automated, write it as a rule and log it.
4. No hard-coded paths, passwords or thresholds — use `config/project.yml` and `.env`.
5. Every script starts with a docstring: purpose, input, output.
6. Scripts stop with a clear error if a REQUIRED setting (e.g. confidence level) is not decided.
7. R / Stata / SPSS equivalents follow the same numbering — see
   [PIPELINE.md §3](../06_documentation/analysis_documentation/PIPELINE.md#3-organising-analysis-code-by-language).

Rule files (`*.csv`) contain placeholder rows starting with `[` and `active = no`; they are ignored
until replaced by real, reviewed rules.
