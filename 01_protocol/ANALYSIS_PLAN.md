# Statistical Analysis Plan — [PROJECT_NAME]

| Field | Value |
| --- | --- |
| Plan version | [v1.0] — [YYYY-MM-DD] |
| Status | Draft / **Approved (frozen)** / Amended |
| Author | [ANALYSIS_LEAD] |
| Methodology approval | [METHODOLOGY_LEAD] — [YYYY-MM-DD] |
| Linked protocol version | [RESEARCH_PROTOCOL vX.Y](RESEARCH_PROTOCOL.md) |

> **Freeze rule.** This plan is approved and tagged (e.g. `sap-v1.0`) **before** the final
> analysis-ready data are analysed. Any later change is an amendment (§14) and every analysis
> not in the approved plan is labelled *exploratory / post hoc* in all outputs.

Pipeline settings that implement this plan live in [config/project.yml](../config/project.yml)
(`weighting`, `analysis`). Keep both consistent — reviewers check it.

---

## 1. Analysis software and environment

| Item | Choice |
| --- | --- |
| Primary language | [Python ≥ 3.11 / R ≥ 4.3 / Stata / SPSS] |
| Design-based estimation | [e.g. R `survey`, Stata `svy`, Python `samplics`] |
| Environment capture | `requirements.txt` (+ `requirements.lock.txt`) / `renv.lock` |
| Random seed (if any resampling) | [SEED] |

## 2. Key variables (outcomes)

| ID | Variable(s) | Definition | Type | Source item(s) |
| --- | --- | --- | --- | --- |
| Y1 | `[var]` | [definition] | [binary/ordinal/…] | [Qxx] |
| Y2 | `[var]` | | | |

## 3. Indicators

| ID | Indicator | Numerator | Denominator (base) | Disaggregation | RQ |
| --- | --- | --- | --- | --- | --- |
| IND-01 | [name] | [definition] | [who is included] | [by region, sex, …] | RQ1 |
| IND-02 | | | | | |

Composite indices: [construction, item scoring, reverse-coded items, handling of partial
missingness, reliability statistic to report (e.g. Cronbach's alpha / omega)].

## 4. Demographic and background variables

| Variable | Categories used in analysis | Derived from | Notes |
| --- | --- | --- | --- |
| `[sex]` | [categories] | [Qxx] | |
| `[age_group]` | [bands — define here] | `age` | derived in stage 03 |
| `[region]` | [categories] | [frame / Qxx] | |
| `[education]` | [categories] | [Qxx] | |

## 5. Descriptive analysis

- Frequencies: weighted % + unweighted n + margin of error for every indicator.
- Continuous variables: weighted mean, median, SD, min–max, n.
- Implemented by `03_scripts/06_descriptive_analysis/` (config `analysis.descriptive_variables`).

## 6. Statistical tests and models

| Analysis | Variables | Test / model | Assumptions checked | Software function |
| --- | --- | --- | --- | --- |
| Group differences (categorical) | [Y × X] | [e.g. design-adjusted chi-square (Rao-Scott)] | [cell sizes] | [function] |
| Group differences (continuous) | | [e.g. design-based t-test / regression] | | |
| Multivariable | [Y ~ X1 + X2 …] | [e.g. survey-weighted logistic regression] | [collinearity, fit] | |

- Significance level: [α] (two-sided unless stated).
- Multiple comparisons: [approach or "none — interpret as exploratory"].
- Effect sizes and confidence intervals are reported with every test.

## 7. Required tables

| Table ID | Content | Rows × columns | Base | Script / output file |
| --- | --- | --- | --- | --- |
| T1 | Sample characteristics (unweighted n, weighted %) | demographics | all respondents | `tab_desc_*.csv` |
| T2 | [indicator] by [group] | | | `tab_xtab_*_by_*.csv` |

## 8. Weighting

| Element | Specification |
| --- | --- |
| Base (design) weight | [1/probability of selection at each stage, or "not applicable"] |
| Non-response adjustment | [method, cells] |
| Calibration / raking | [variables, population source and year → `03_scripts/04_weighting/weighting_targets.csv`] |
| Trimming | [bounds and rule, or "none"] |
| Final weight variable | `weight_final` (normalised to sample size) |
| Reporting | Kish design effect due to weighting and effective n (stage 04 QC report) |

## 9. Margins of error and precision

- Confidence level: [value] → `analysis.confidence_level`.
- Design effect used for approximate MOE: [value and source] → `analysis.design_effect`.
- MOE formula for proportions: `z × sqrt(deff × p(1−p)/n)`; design-based standard errors
  are used instead where [strata/cluster variables] are available.
- Estimates with [MOE > threshold or n < threshold] are flagged "interpret with caution".

## 10. Missing data

| Situation | Handling |
| --- | --- |
| Item non-response codes ([97/98/99]) | Treated as missing in % bases unless the category is substantively reported (e.g. "Don't know" shown in tables) — specify per indicator |
| Missingness < [x]% | Complete-case analysis |
| Missingness ≥ [x]% on key variables | [e.g. report pattern; multiple imputation / sensitivity analysis] |
| Reporting | Base n reported for every estimate |

## 11. Exclusion rules

Applied only in stage 02 (`cleaning_rules.csv`, action `drop_record`) and counted in the cleaning log:

| Rule | Criterion | Rationale |
| --- | --- | --- |
| EX-1 | [no consent] | ethics |
| EX-2 | [ineligible respondent] | protocol §6 |
| EX-3 | [e.g. interview duration below threshold defined here] | data quality |
| EX-4 | [failed back-check] | data quality |

## 12. Interpretation and reporting rules

- Report weighted % with unweighted base n and MOE; round % to [0/1] decimals.
- Do not report cells with unweighted n < [MIN_CELL_SIZE] (`analysis.min_cell_size`) — show "–" and footnote.
- Differences are described as "higher/lower" only when [the test / non-overlapping CI rule] supports it.
- Exploratory findings are labelled as such.
- Causal language is not used for cross-sectional associations.
- Every number in the report must trace to a table file in `04_analysis/tables/` or `statistical_outputs/`.

## 13. Quality control of the analysis

- Independent re-run of `run_pipeline.py` by a second analyst from a clean clone → identical outputs (checksums).
- Spot-check of [x] key estimates recomputed in a second tool (e.g. SPSS/Stata vs Python/R).
- Table–text consistency check before each report version.
- Checklist: [QC_CHECKLIST.md](../06_documentation/quality_control/QC_CHECKLIST.md).

## 14. Amendments

| Version | Date | Change | Reason | Before/after seeing final data? | Decision record |
| --- | --- | --- | --- | --- | --- |
| v1.0 | [YYYY-MM-DD] | Approved plan | — | before | — |
