# Data Management Plan (DMP) — [PROJECT_NAME]

| Field | Value |
| --- | --- |
| DMP version | [v1.0] — [YYYY-MM-DD] |
| Owner | Data Manager — [DATA_MANAGER] |
| Approved by | Project Lead — [PROJECT_LEAD] |
| Institutional / funder DMP requirements | [FUNDER_OR_INSTITUTION_REQUIREMENTS] |
| Applicable data-protection law | [APPLICABLE_DATA_PROTECTION_LAW] |
| Review frequency | At each phase change and at least every [6] months |

Related: [DATA_SECURITY.md](../../DATA_SECURITY.md) · [SECURITY.md](../../SECURITY.md) ·
[PIPELINE.md](../analysis_documentation/PIPELINE.md) · [DATA_DICTIONARY.md](../../02_data/data_dictionary/DATA_DICTIONARY.md)

---

## 1. Data sources

| ID | Source | Type | Format | Expected volume | Owner / provider | Classification |
| --- | --- | --- | --- | --- | --- | --- |
| DS-1 | Primary survey | Respondent-level responses | [csv/xlsx/sav] | [n records × k variables] | [ORGANIZATION_NAME] | C3 (raw) |
| DS-2 | Sampling frame | Unit list | [format] | [n] | [provider] | C3 |
| DS-3 | Population margins for weighting | Aggregate | csv | small | [official source] | C0 |
| DS-4 | [Secondary data] | [type] | [format] | | [provider + licence/DUA] | [class] |

## 2. Data collection

- Mode, platform and period: see [RESEARCH_PROTOCOL.md §9](../../01_protocol/RESEARCH_PROTOCOL.md#9-data-collection-method).
- Platform account owner: Data Manager. Access for interviewers limited to submission.
- Devices: encrypted, PIN-protected, remote-wipe enabled; no local copies after sync.
- Paper forms (if any): locked storage, digitised by [procedure], then [retained/destroyed per §12].

## 3. Storage

| Stage | Location | Encryption | Access |
| --- | --- | --- | --- |
| Raw, restricted (C3) | [SECURE_STORAGE_LOCATION]/[PROJECT_SHORT_NAME]/raw, /restricted | at rest [method] + encrypted container for `restricted/` | Data Manager (+ Project Lead in emergency) |
| Cleaned → analysis-ready (C2) | [SECURE_STORAGE_LOCATION]/[PROJECT_SHORT_NAME]/cleaned … /analysis_ready | at rest | Data Manager, Statistical Analysts, Methodology Lead |
| Code, docs, metadata (C1) | GitHub private repository | GitHub-managed | Team per ROLES_AND_PERMISSIONS.md |
| Approved outputs (C0) | GitHub `07_outputs/` + institutional repository | — | Team; public after release |

## 4. Data security

Measures: least-privilege access, two-factor authentication on GitHub and storage, encryption at
rest and in transit, no personal devices/cloud, pseudonymisation at stage 02, automated
repository guardrails. Full policy: [DATA_SECURITY.md](../../DATA_SECURITY.md). Incidents:
[SECURITY.md](../../SECURITY.md).

## 5. Backup

| What | Method | Frequency | Retention | Location | Restore test |
| --- | --- | --- | --- | --- | --- |
| Secure data storage | [institutional backup / snapshot] | [daily] | [30 days rolling + monthly] | [separate site] | every [3] months, logged |
| Git repository | GitHub + [mirror clone / institutional Git backup] | [weekly] | [ ] | [location] | at each release |
| Raw data | Immutable copy at receipt (read-only) + checksum in manifest | at receipt | project lifetime + §12 | [location] | checksum verify |

"3-2-1" principle: 3 copies, 2 media/locations, 1 off-site.

## 6. Data cleaning

- Scripted in `03_scripts/02_cleaning/02_clean.py`; decisions as rules in
  `cleaning_rules.csv` (ID, condition, action, rationale, issue, approver).
- Every rule reviewed via Pull Request by the Data Manager; counts logged per rule.
- Narrative log: [CLEANING_LOG.md](../analysis_documentation/CLEANING_LOG.md).
- Raw data are never modified.

## 7. Data processing

Recoding, derived variables, merging and weighting are scripted (stages 03–05) and
documented in the data dictionary (derived variables) and the Analysis Plan (weights).

## 8. Documentation and metadata

| Document | Content |
| --- | --- |
| Data dictionary (MD + CSV) | All variables, codes, missing codes, sources, PII class |
| DATA_MANIFEST.csv | Every data file: version, SHA-256, rows, script, commit |
| QC reports | Aggregate results of each stage |
| Protocol, Analysis Plan, Methodological notes | Context needed to reuse the data |
| CHANGELOG.md | Data version used by each release |

## 9. Access and permissions

| Role | Raw / restricted | Cleaned → analysis-ready | Repository |
| --- | --- | --- | --- |
| Project Lead | emergency only | read | Admin |
| Data Manager | read/write | read/write | Maintain |
| Methodology Lead | — | read | Maintain |
| Statistical Analyst | — | read | Write |
| Fieldwork Coordinator | platform monitoring (aggregate) | — | Write |
| Research Assistant | — | read if assigned | Write |
| Reviewer | — | read if needed for review | Write / Triage |

Access is granted by the Data Manager on request (Issue), reviewed every [3] months and
revoked on the day a member leaves (checklist in [ONBOARDING.md](../onboarding/ONBOARDING.md)).

## 10. Data sharing

| Audience | What | Conditions |
| --- | --- | --- |
| Team | analysis-ready (C2) | need-to-know, DMP compliance |
| Partners | [de-identified subset] | Data-sharing agreement [DSA_REF] |
| Public | aggregate outputs; [de-identified PUF if consent allows] | disclosure control, licence, Project Lead approval |

Disclosure control before any sharing: remove direct identifiers, generalise
quasi-identifiers, check k-anonymity ≥ [K_THRESHOLD], suppress cells n < [MIN_CELL_SIZE].

## 11. Archiving

At project close: final analysis-ready dataset (and public-use file if any), data dictionary,
questionnaire, protocol, analysis plan, code at the final release tag, and manifest are deposited in
[ARCHIVE_REPOSITORY e.g. institutional repository / data archive] with a persistent identifier.

## 12. Retention and deletion

| Data | Retention | Deletion method | Responsible | Evidence |
| --- | --- | --- | --- | --- |
| Direct identifiers & linking key | until [event, e.g. end of back-checks / follow-up] | secure deletion ([method]) | Data Manager | deletion log |
| Raw data | [n] years after project end | secure deletion | Data Manager | deletion log |
| Consent records | per ethics requirement ([n] years) | | | |
| Audio/photos (if any) | [n] days after QC | | | |
| Pseudonymised data | [n] years | | | |
| Survey-platform copies | after verified export | platform deletion + confirmation | Data Manager | screenshot/log |

Participant withdrawal: remove the participant's records from raw-derived stages by adding
an exclusion rule referencing the pseudonymous ID (no names), rerun the pipeline, bump version.

## 13. Version management of data

- Dataset versions `v<MAJOR>.<MINOR>` (config `data.dataset_version`):
  MAJOR = new data delivery/wave or change to cleaning rules that alters records;
  MINOR = recodes/derived variables/weights change.
- Every file name includes its version; no file is overwritten with a different content
  under the same name — the manifest checksum would reveal it.
- Each code release (Git tag) records the dataset version in CHANGELOG.md.

## 14. Responsibilities and resources

| Task | Responsible |
| --- | --- |
| Maintaining this DMP | Data Manager |
| Storage & backups | Data Manager with [IT_CONTACT] |
| Access reviews | Data Manager + Project Lead |
| Resources (storage, licences) | [budget line] |

## 15. DMP change history

| Version | Date | Change | Approved by |
| --- | --- | --- | --- |
| v1.0 | [YYYY-MM-DD] | Initial DMP | [PROJECT_LEAD] |
