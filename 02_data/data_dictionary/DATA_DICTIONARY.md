# Data Dictionary — [PROJECT_NAME]

**Status:** official reference for every variable in every data stage.
**Owner:** Data Manager ([DATA_MANAGER]). **Changes:** only through a Pull Request approved by the Data Manager.
**Dataset version documented:** [DATASET_VERSION] · **Questionnaire version:** [QUESTIONNAIRE_VERSION]

> The machine-readable twin of this file is [data_dictionary.csv](data_dictionary.csv) — the
> pipeline reads it for validation (codes, ranges), identifier removal (`pii`) and
> variable selection (`in_analysis`). **Both files must be updated in the same PR.**

## 1. Conventions

| Item | Rule |
| --- | --- |
| Variable names | English, `snake_case`, ASCII, ≤ 32 characters (SPSS/Stata compatible), start with a letter |
| Question-based names | Keep the questionnaire ID when useful: `q12_trust_gov` |
| Derived variables | Descriptive name + created at `processed` stage: `age_group`, `idx_trust` |
| Labels | English label (official) + Arabic label (for Arabic outputs) |
| Types | `categorical`, `ordinal`, `binary`, `numeric`, `integer`, `string`, `date` (ISO 8601 `YYYY-MM-DD`) |
| Values | `code=label` pairs separated by `\|`, e.g. `1=Yes\|2=No` |
| Missing codes | Standard project codes (define once, use everywhere): [e.g. 97=Refused \| 98=Don't know \| 99=Not applicable] |
| Source | Questionnaire item ID + version (e.g. `Q12 v1.2`), or the script that created it |
| PII | `none`, `quasi` (quasi-identifier — may enable re-identification in combination), `direct` (removed at cleaning) |

## 2. Variables

| Variable | Label | Type | Values | Missing | Source | Notes |
| -------- | ----- | ---- | ------ | ------- | ------ | ----- |
| `resp_id` | Pseudonymous respondent ID / المعرّف المستعار | string | — | none allowed | System — `02_clean.py` | Unique; linking key only in restricted storage |
| `weight_final` | Final analysis weight / الوزن النهائي | numeric | > 0 | none allowed | System — `04_weight.py` | Method: see Analysis Plan §8 |
| `[variable_name]` | [English label] / [التسمية العربية] | [type] | [1=…\|2=…] | [98\|99] | [Q_ID vX.Y] | [notes] |

<!-- Add one row per variable. Group rows by questionnaire section using sub-headings if helpful:
### Section A — Demographics
### Section B — [Topic]
-->

## 3. Derived variables

| Variable | Label | Derived from | Rule / formula | Script | Decision record |
| -------- | ----- | ------------ | -------------- | ------ | --------------- |
| `[derived_var]` | [label] | `[source_vars]` | [exact rule] | `03_scripts/03_recoding/03_recode.py` | `DR-[NNN]` |

## 4. Identifiers and quasi-identifiers

| Variable | PII class | Handling |
| -------- | --------- | -------- |
| `[direct_identifier]` | direct | Removed at stage 02; kept only in `$DATA_ROOT/restricted/` |
| `[quasi_identifier]` | quasi | Kept for analysis; generalised before any data sharing |

## 5. Change log of this dictionary

| Date | Version | Change | PR |
| ---- | ------- | ------ | -- |
| [YYYY-MM-DD] | 0.1 | Template created | #[PR] |
