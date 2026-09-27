# [PROJECT_NAME]

> Collaborative, reproducible and secure research repository for **[PROJECT_NAME]** — [ORGANIZATION_NAME].
>
> النسخة العربية: [README.ar.md](README.ar.md)

| Item | Value |
| --- | --- |
| Project short name | `[PROJECT_SHORT_NAME]` |
| Organization | [ORGANIZATION_NAME] |
| Project lead | [PROJECT_LEAD] |
| Funder (if any) | [FUNDER] |
| Ethics approval | [ETHICS_COMMITTEE] — ref. [ETHICS_APPROVAL_REF] |
| Current version | see [CHANGELOG.md](CHANGELOG.md) and GitHub Releases |
| Status | `Planning` / `Fieldwork` / `Cleaning` / `Analysis` / `Reporting` / `Closed` — **[CURRENT_STATUS]** |

---

## 1. Project description

[SHORT_DESCRIPTION — 3–5 sentences: what is studied, where, with whom, and why.
Do not include any participant-level information here.]

## 2. Research objectives

1. [OBJECTIVE_1]
2. [OBJECTIVE_2]
3. [OBJECTIVE_3]

Research questions and hypotheses are defined in the
[Research Protocol](01_protocol/RESEARCH_PROTOCOL.md).

## 3. Research team

Roles, responsibilities and GitHub permissions are defined in
[ROLES_AND_PERMISSIONS.md](00_project_management/team/ROLES_AND_PERMISSIONS.md).

| Role | Person | GitHub handle |
| --- | --- | --- |
| Project Lead | [PROJECT_LEAD] | @[PROJECT_LEAD_HANDLE] |
| Data Manager | [DATA_MANAGER] | @[DATA_MANAGER_HANDLE] |
| Methodology Lead | [METHODOLOGY_LEAD] | @[METHODOLOGY_LEAD_HANDLE] |
| Statistical Analyst / Analysis Lead | [ANALYSIS_LEAD] | @[ANALYSIS_LEAD_HANDLE] |
| Fieldwork Coordinator | [FIELDWORK_COORDINATOR] | @[FIELDWORK_COORDINATOR_HANDLE] |
| Report Lead | [REPORT_LEAD] | @[REPORT_LEAD_HANDLE] |
| Research Assistants | [RESEARCH_ASSISTANTS] | — |
| Reviewer(s) | [REVIEWERS] | — |

## 4. Methodology (summary)

| Element | Summary (full detail in the protocol) |
| --- | --- |
| Design | [STUDY_DESIGN] |
| Population | [TARGET_POPULATION] |
| Sampling | [SAMPLING_DESIGN] — see [01_protocol/sampling/](01_protocol/sampling/) |
| Sample size | [SAMPLE_SIZE] |
| Data collection | [DATA_COLLECTION_MODE] |
| Instrument | [INSTRUMENT] — see [01_protocol/questionnaire/](01_protocol/questionnaire/) |
| Fieldwork period | [FIELDWORK_START] – [FIELDWORK_END] |
| Weighting | [WEIGHTING_APPROACH] |

Analysis is pre-specified in the [Analysis Plan](01_protocol/ANALYSIS_PLAN.md).

## 5. Project status

Track live progress on the GitHub Project board (**[PROJECT_BOARD_URL]**).
The board columns and labels are described in
[PROJECT_BOARD.md](06_documentation/governance/PROJECT_BOARD.md).

## 6. Repository structure

```text
.
├── README.md / README.ar.md       Entry point (EN / AR)
├── CONTRIBUTING.md                How to work: branches, commits, PRs, reviews
├── SECURITY.md                    Reporting & handling security / data incidents
├── DATA_SECURITY.md               What data may and may not enter GitHub
├── CHANGELOG.md                   Human-readable history of every release
├── CODE_OF_CONDUCT.md · LICENSE · CITATION.cff
├── config/                        Pipeline configuration (no secrets)
├── tools/                         Repository checks + GitHub setup script
├── .github/                       CODEOWNERS, issue/PR templates, workflows
├── 00_project_management/         Plan, minutes, tasks, decisions, team roles
├── 01_protocol/                   Protocol, analysis plan, questionnaire, sampling, fieldwork, ethics
├── 02_data/                       Data STAGES (files live in secure storage; Git holds README,
│   │                              manifest, metadata and the data dictionary only)
│   ├── raw/  cleaned/  processed/  analysis_ready/
│   ├── metadata/                  DATA_MANIFEST.csv (version + SHA-256 of every data file)
│   └── data_dictionary/           DATA_DICTIONARY.md + data_dictionary.csv (official reference)
├── 03_scripts/                    Numbered pipeline: 01_validation → 08_visualization
├── 04_analysis/                   Generated tables, figures, statistical outputs, QC reports
├── 05_reports/                    drafts/ → reviewed/ → final/
├── 06_documentation/              DMP, methodology notes, pipeline docs, QC, governance, onboarding
├── 07_outputs/                    Approved, disclosure-checked outputs for publication
└── 99_archive/                    Superseded material (read-only)
```

Every folder contains a `README.md` explaining what belongs there.

## 7. Data handling rules (summary)

1. **No personal or identifiable data in GitHub. Ever.** Raw data, direct identifiers,
   contact lists, GPS coordinates, consent forms and the ID-linking key live only in the
   secure storage: **[SECURE_STORAGE_LOCATION]**.
2. `02_data/raw/` is **read-only**. Nobody edits raw files; all changes are made by scripts.
3. Data move **only forward** through `raw → cleaned → processed → analysis_ready`, and only
   through scripts in `03_scripts/`.
4. Every data file produced is registered in
   [02_data/metadata/DATA_MANIFEST.csv](02_data/metadata/DATA_MANIFEST.csv) with its version and SHA-256.
5. Every variable is documented in the
   [Data Dictionary](02_data/data_dictionary/DATA_DICTIONARY.md).

Full rules: [DATA_SECURITY.md](DATA_SECURITY.md) and the
[Data Management Plan](06_documentation/data_management/DATA_MANAGEMENT_PLAN.md).

## 8. How to contribute — the daily workflow

```text
 1. Pull latest changes        git switch main && git pull
 2. Create branch              git switch -c analysis/42-crosstabs-by-region
 3. Work on assigned task      (the task is a GitHub Issue, e.g. #42)
 4. Commit changes             git commit -m "analysis(crosstabs): add region tables (refs #42)"
 5. Push branch                git push -u origin analysis/42-crosstabs-by-region
 6. Open Pull Request          fill in the PR template; link "Closes #42"
 7. Reviewer checks work       CODEOWNERS are requested automatically; CI runs checks
 8. Corrections if needed      push new commits to the same branch
 9. Approval                   required approvals + all checks green
10. Merge                      "Squash and merge" by a maintainer
11. Close Issue                automatic via "Closes #42"; branch deleted automatically
```

Details: [CONTRIBUTING.md](CONTRIBUTING.md).

## 9. Branching model

| Branch | Purpose | Who merges |
| --- | --- | --- |
| `main` | Always-reviewed, reproducible state. **Protected — no direct pushes.** | Maintainers via PR |
| `data/<issue>-<desc>` | Validation, cleaning, recoding, weighting scripts & rules | Data Manager review |
| `analysis/<issue>-<desc>` | Statistical analysis, tables, figures | Analysis Lead review |
| `method/<issue>-<desc>` | Protocol, questionnaire, sampling, analysis-plan changes | Methodology Lead review |
| `docs/<issue>-<desc>` | Documentation only | Any maintainer |
| `report/<issue>-<desc>` | Report drafts and revisions | Report Lead review |
| `fix/<issue>-<desc>` | Corrections of errors already merged | Owner of the affected area |

There is deliberately **no `develop` branch** — see the rationale in
[CONTRIBUTING.md](CONTRIBUTING.md#2-branching-strategy).

## 10. Submitting a Pull Request

- One PR = one issue = one logical change. Keep it small enough to review in < 30 minutes.
- Fill in every section of the [PR template](.github/PULL_REQUEST_TEMPLATE.md), especially
  *Data changes*, *Methodology changes*, *Results changed?* and *Sensitive data check*.
- CI must pass: structure check, sensitive-data scan, secret scan, Markdown and link checks.
- Changes to data rules or analysis code need the relevant CODEOWNER approval.

## 11. Sensitive data policy

See [DATA_SECURITY.md](DATA_SECURITY.md). If you think sensitive data or a secret was
committed, **stop, do not try to fix it quietly**, and follow the incident procedure in
[SECURITY.md](SECURITY.md) immediately.

## 12. Reproducing the analysis

```bash
# 1. Clone and set up the environment
git clone https://github.com/[ORG_OR_USER]/[REPO_NAME].git && cd [REPO_NAME]
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 2. Point the pipeline at the secure data location (never inside the repo)
cp config/.env.example .env        # then set DATA_ROOT=/path/to/secure/storage/[PROJECT_SHORT_NAME]

# 3. Check you have the exact data version used for the release you reproduce
git checkout v1.0.0
python tools/data_manifest.py verify          # compares SHA-256 with 02_data/metadata/DATA_MANIFEST.csv

# 4. Run the full pipeline
python 03_scripts/run_pipeline.py             # or: python 03_scripts/run_pipeline.py --from 06
```

Pipeline stages and their inputs/outputs are documented in
[PIPELINE.md](06_documentation/analysis_documentation/PIPELINE.md).

## 13. Versions and change history

- Semantic versioning adapted to research: see [VERSIONING.md](06_documentation/governance/VERSIONING.md).
- Every release is a Git tag (`vMAJOR.MINOR.PATCH`) plus a GitHub Release and a
  [CHANGELOG.md](CHANGELOG.md) entry that states which data version it used.

## 14. Citation and licence

Cite this work using [CITATION.cff](CITATION.cff). Licence: [LICENSE](LICENSE).

## 15. Contact

| Purpose | Contact |
| --- | --- |
| General questions | [CONTACT_EMAIL] |
| Data access requests | [DATA_MANAGER] — [DATA_MANAGER_EMAIL] |
| Security or data incidents | [SECURITY_CONTACT_EMAIL] (see [SECURITY.md](SECURITY.md)) |

New to the project? Start with the
[Onboarding guide](06_documentation/onboarding/ONBOARDING.md).
