# Quality-Control Checklists

Copy the relevant section into the Pull Request (or the Review Request issue) and tick it.
The reviewer is never the author.

## 1. Data QC — raw data received (Data Manager)

- [ ] File placed in `$DATA_ROOT/raw/` with the naming convention; set read-only
- [ ] Receipt logged in `02_data/raw/README.md` (no personal data)
- [ ] Stage 01 run; `01_validation_report_v*.csv` reviewed; critical issues = 0 or explained in an Issue
- [ ] Record count matches fieldwork report; IDs unique
- [ ] All variables present in the data dictionary (or dictionary updated)
- [ ] Manifest updated with raw SHA-256

## 2. Cleaning / recoding PR (reviewer: Data Manager)

- [ ] Every new rule has ID, rationale, linked issue and approver in the rule file
- [ ] Rules apply to the intended records only (reviewer checked counts in the cleaning log)
- [ ] Exclusions match ANALYSIS_PLAN §11; counts before/after reported
- [ ] Direct identifiers absent from cleaned output (`pii=direct` variables removed)
- [ ] Data dictionary updated (new/derived variables, codes, missing codes)
- [ ] `dataset_version` bumped when required; manifest committed
- [ ] `CLEANING_LOG.md` updated for non-trivial decisions

## 3. Weighting PR (reviewer: Methodology Lead)

- [ ] Method matches ANALYSIS_PLAN §8 and `config/project.yml`
- [ ] Population targets sourced and dated in `weighting_targets.csv`
- [ ] Weighted margins reproduce targets (tolerance stated)
- [ ] Min/max weight, ratio, Kish deff and effective n reviewed (`04_weighting_qc`)
- [ ] Trimming justified if applied

## 4. Analysis PR (reviewer: Analysis Lead / statistician)

- [ ] Analysis is in the approved plan — or labelled exploratory
- [ ] Correct base (denominator) and missing-data handling
- [ ] Weights applied; unweighted n reported with every estimate
- [ ] MOE / CI computed with the configured confidence level and design effect
- [ ] Small cells suppressed (n < `min_cell_size`)
- [ ] Reviewer re-ran the stage and obtained identical outputs
- [ ] At least [x] key figures cross-checked in a second tool
- [ ] Tables/figures named per convention; figures built from tables
- [ ] Interpretation avoids causal claims and over-reading non-significant differences

## 5. Report / release QC (Report Lead + Project Lead)

- [ ] Every number in the text traces to a file in `04_analysis/tables/` or `statistical_outputs/`
- [ ] Table–text–figure consistency checked (values, rounding, labels, bases)
- [ ] Methodological note complete: sample, response rate, weighting, MOE, limitations
- [ ] Deviations from protocol/analysis plan disclosed
- [ ] Arabic and English versions consistent (numbers identical)
- [ ] Disclosure control applied to all published tables and datasets
- [ ] Fresh-clone reproduction by a reviewer: `run_pipeline.py` → no diff in `04_analysis/`
- [ ] `python tools/check_docs.py --strict` passes
- [ ] CHANGELOG entry states data version; CITATION.cff updated
- [ ] Approvals: Project Lead + owners of changed areas

## 6. Security check (every PR — author and reviewer)

- [ ] No names, phone numbers, e-mails, ID numbers, addresses, GPS, free-text that identifies people
- [ ] No data files outside `approved_deid/` / `07_outputs/datasets/`
- [ ] No secrets, tokens, `.env`, keys
- [ ] Notebook outputs cleared
- [ ] CI sensitive-data and secret scans green
