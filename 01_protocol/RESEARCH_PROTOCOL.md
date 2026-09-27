# Research Protocol — [PROJECT_NAME]

| Field | Value |
| --- | --- |
| Protocol version | [v1.0] — date [YYYY-MM-DD] |
| Status | Draft / Under review / **Approved** / Amended |
| Principal investigator / Project Lead | [PROJECT_LEAD] |
| Methodology Lead | [METHODOLOGY_LEAD] |
| Institution | [ORGANIZATION_NAME] |
| Ethics approval | [ETHICS_COMMITTEE], ref. [ETHICS_APPROVAL_REF], date [YYYY-MM-DD] |
| Pre-registration (if any) | [REGISTRY_AND_ID or "not pre-registered"] |

> **Change control.** After approval, any change is an *amendment*: open a `method/` branch,
> update this file, add a Decision Record in `00_project_management/decisions/`, obtain the
> Methodology Lead's and Project Lead's approval, and — where required — ethics approval.
> Record amendments in §17.

---

## 1. Study title

- English: [FULL_TITLE_EN]
- العربية: [FULL_TITLE_AR]
- Short name: `[PROJECT_SHORT_NAME]`

## 2. Background

[Context, existing evidence and gaps. Cite sources. 1–2 pages.]

## 3. Problem statement

[What exactly is unknown or problematic, for whom, and why it matters.]

## 4. Objectives

- **General objective:** [GENERAL_OBJECTIVE]
- **Specific objectives:**
  1. [SPECIFIC_OBJECTIVE_1]
  2. [SPECIFIC_OBJECTIVE_2]

## 5. Research questions and hypotheses

| ID | Research question | Hypothesis (if confirmatory) | Linked indicators (Analysis Plan §3) |
| --- | --- | --- | --- |
| RQ1 | [question] | [H1 or "exploratory"] | [IND-01] |
| RQ2 | [question] | [H2 or "exploratory"] | [IND-02] |

## 6. Study population

| Element | Definition |
| --- | --- |
| Target population | [who, where, when] |
| Survey population | [target population minus exclusions such as institutions, inaccessible areas] |
| Unit of analysis | [individual / household / organisation] |
| Eligibility criteria | [inclusion criteria] |
| Exclusion criteria | [exclusion criteria] |
| Respondent selection within unit | [e.g. method used — if applicable] |

## 7. Sampling design

Full detail: [sampling/SAMPLING_PLAN.md](sampling/SAMPLING_PLAN.md).

| Element | Description |
| --- | --- |
| Sampling frame | [frame, source, date, known coverage issues] |
| Design | [e.g. simple random / stratified / multi-stage cluster / quota / non-probability] |
| Stratification | [variables] |
| Stages and units | [PSU → SSU → …] |
| Selection method at each stage | [method] |
| Replacement / substitution rules | [rules or "none"] |

## 8. Sample size

| Element | Value | Justification / source |
| --- | --- | --- |
| Target precision (margin of error) | [value] | [reason] |
| Confidence level | [value] | [reason] |
| Expected proportion | [value] | [source / conservative assumption] |
| Design effect | [value] | [source: previous survey / pilot] |
| Expected response rate | [value] | [source] |
| Sub-groups requiring minimum n | [list] | [reason] |
| **Final target sample** | **[n]** | calculation reproducible in `sampling/` |

## 9. Data collection method

| Element | Description |
| --- | --- |
| Mode | [CAPI / CATI / CAWI / PAPI / mixed] |
| Platform / tool | [platform name and version] |
| Fieldwork period | [start] – [end] |
| Interviewers | [number, recruitment, training — see fieldwork/] |
| Languages | [Arabic / English / other] |
| Contact protocol | [number of attempts, call-backs, times] |

## 10. Research instrument

- Questionnaire: [questionnaire/](questionnaire/) — current version [vX.Y], languages [ar, en].
- Development: [sources of items, adaptation, translation & back-translation, cognitive testing].
- Pilot: [date, n, main changes — decision records].
- Scales/indices and their validation: [list; reliability to be reported per Analysis Plan].

## 11. Quality-control procedures

| Phase | Procedure | Responsible | Evidence |
| --- | --- | --- | --- |
| Before fieldwork | Instrument review, translation check, pilot, interviewer training & test | Methodology Lead / Fieldwork Coordinator | `fieldwork/`, decision records |
| During fieldwork | Daily data checks (completeness, duration, straight-lining, GPS/time plausibility), back-checks on [x]% of interviews, supervisor accompaniment | Fieldwork Coordinator / Data Manager | aggregate QC reports |
| After fieldwork | Validation (stage 01), rule-based cleaning (stage 02), second-person review of every rule | Data Manager | `04_analysis/qc_reports/`, PRs |
| Analysis | Independent re-run of the pipeline, statistical review, table–text consistency check | Analysis Lead / Reviewer | `06_documentation/quality_control/QC_CHECKLIST.md` |

## 12. Data processing

Processing follows the scripted pipeline documented in
[PIPELINE.md](../06_documentation/analysis_documentation/PIPELINE.md) and the
[Data Management Plan](../06_documentation/data_management/DATA_MANAGEMENT_PLAN.md):
raw → validation → cleaning (pseudonymisation) → recoding → weighting → analysis-ready.

## 13. Analysis plan (summary)

Pre-specified in [ANALYSIS_PLAN.md](ANALYSIS_PLAN.md), approved before analysis of the
final data begins. Deviations are reported as such in the report.

## 14. Ethical considerations

| Topic | Approach |
| --- | --- |
| Approval | [committee, reference, conditions] |
| Informed consent | [oral / written; how recorded; stored in secure storage only] |
| Voluntariness & right to withdraw | [procedure; how withdrawals are removed from data] |
| Confidentiality | Pseudonymisation at stage 02; identifiers only in restricted storage; see [DATA_SECURITY.md](../DATA_SECURITY.md) |
| Vulnerable groups / minors | [special procedures or "not applicable"] |
| Risks and mitigation | [e.g. sensitive questions, interviewer safety, distress protocol, referral] |
| Compensation | [if any] |
| Data sharing & publication | [what may be shared, with whom, conditions] |
| Conflict of interest | [declaration] |

## 15. Methodological limitations

| Limitation | Expected effect | Mitigation |
| --- | --- | --- |
| [e.g. frame coverage] | [bias direction if known] | [weighting / sensitivity analysis / disclosure in report] |
| [e.g. non-response] | | |
| [e.g. social desirability] | | |
| [e.g. mode effects] | | |

## 16. Timeline and deliverables

See [00_project_management/project_plan/PROJECT_PLAN.md](../00_project_management/project_plan/PROJECT_PLAN.md).

## 17. Amendments

| Version | Date | Section(s) | Change | Reason | Decision record | Ethics notified |
| --- | --- | --- | --- | --- | --- | --- |
| v1.0 | [YYYY-MM-DD] | — | Initial approved protocol | — | — | — |
