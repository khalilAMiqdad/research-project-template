# Roles & Permissions — [PROJECT_NAME]

Principle: **least privilege + four-eyes review.** Nobody approves their own work, and
access to data is independent of access to the repository.

## 1. Roles

| Role | Person (placeholder) | Main responsibilities |
| --- | --- | --- |
| **Project Lead** | [PROJECT_LEAD] | Overall accountability; approves protocol, releases, final reports and public outputs; repository admin; incident lead |
| **Data Manager** | [DATA_MANAGER] | Secure storage and access; receives raw data; owns cleaning rules, manifest, data dictionary, DMP; approves every data change |
| **Methodology Lead** | [METHODOLOGY_LEAD] | Protocol, sampling, questionnaire, weighting design; approves methodological changes and amendments |
| **Statistical Analyst / Analysis Lead** | [ANALYSIS_LEAD] | Analysis Plan, analysis scripts, tables and figures; statistical review of others' analyses |
| **Fieldwork Coordinator** | [FIELDWORK_COORDINATOR] | Fieldwork manual, training, field QC, progress reporting (aggregate) |
| **Report Lead** | [REPORT_LEAD] | Report structure and drafting; table–text consistency (may be the Project Lead) |
| **Research Assistants** | [RESEARCH_ASSISTANTS] | Assigned tasks: scripts, documentation, literature, drafting — always via PR |
| **Reviewer** | [REVIEWERS] | Independent methodological/statistical/report review; re-runs pipeline for QC |

One person may hold several roles in a small team, **except**: the author of a change
cannot be its only approver, and the Data Manager should not be the only person able to
restore data (the Project Lead holds emergency access).

## 2. GitHub permissions

GitHub repository roles: *Read < Triage < Write < Maintain < Admin*.
Only reviews from people with **Write or higher** count as approvals for protected branches.

| Role | GitHub role | Can merge to `main`? | CODEOWNER of |
| --- | --- | --- | --- |
| Project Lead | **Admin** | yes, after required reviews | `.github/`, `tools/`, `config/`, security docs, `05_reports/final/`, `07_outputs/` |
| Data Manager | **Maintain** | yes, after review | `02_data/`, `03_scripts/01–05`, DMP, `DATA_SECURITY.md` |
| Methodology Lead | **Maintain** | yes, after review | `01_protocol/`, `03_scripts/04_weighting/`, `06_documentation/methodology/` |
| Analysis Lead | **Write** (or Maintain) | no (or yes if Maintain) | `03_scripts/06–08`, `04_analysis/`, `ANALYSIS_PLAN.md` (with Methodology Lead) |
| Fieldwork Coordinator | **Write** | no | `01_protocol/fieldwork/`, `01_protocol/questionnaire/` (with Methodology Lead) |
| Report Lead | **Write** | no | `05_reports/` |
| Research Assistants | **Write** | no | — |
| Internal Reviewer | **Write** | no | — (requested as reviewer) |
| External reviewer / observer | **Read** or **Triage** | no | — (comments do not count as approval) |

"Can merge" is controlled by who has Maintain/Admin plus the branch-protection rules; with
the recommended settings **no one, including admins, can bypass review on `main`**.

### Organization teams (recommended when using a GitHub Organization)

| Team | Members | Repository permission |
| --- | --- | --- |
| `[org]/research-leads` | Project Lead | Admin |
| `[org]/data-team` | Data Manager (+ deputy) | Maintain |
| `[org]/methodology` | Methodology Lead | Maintain |
| `[org]/analysis` | Analysts | Write |
| `[org]/field-team` | Fieldwork Coordinator | Write |
| `[org]/research-assistants` | RAs | Write |
| `[org]/reviewers` | Reviewers | Write |

Using teams in CODEOWNERS (e.g. `@[org]/data-team`) avoids editing the file when people change.

## 3. Data-storage permissions (outside GitHub)

| Role | raw/ | restricted/ | cleaned/ processed/ analysis_ready/ |
| --- | --- | --- | --- |
| Project Lead | emergency | emergency | read |
| Data Manager | read/write | read/write | read/write |
| Methodology Lead | — | — | read |
| Analysts | — | — | read (analysis_ready; others if assigned) |
| Fieldwork Coordinator | platform monitoring only | — | — |
| Research Assistants | — | — | read if assigned |
| Reviewers | — | — | read if needed |

## 4. Decision rights (RACI summary)

R = responsible, A = accountable/approves, C = consulted, I = informed

| Decision | PL | DM | ML | AL | FC | RA | Rev |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Protocol / amendments | A | C | R | C | C | I | C |
| Questionnaire changes | A | C | R | C | C | I | C |
| Cleaning / exclusion rules | I | A/R | C | C | C | R | C |
| Weighting method | I | C | A/R | C | I | I | C |
| Analysis plan | A | C | C | R | I | I | C |
| Release a version | A/R | C | C | C | I | I | C |
| Publish outputs / data | A | R | C | C | I | I | C |
| Grant data access | A | R | I | I | I | I | I |

## 5. Joining and leaving

Checklists are in [ONBOARDING.md](../../06_documentation/onboarding/ONBOARDING.md).
