# Project Board, Issues and Labels

The team uses one **GitHub Project** (board view) linked to this repository.
Created by [tools/setup_github.sh](../../tools/setup_github.sh); view layout is set once in the web UI.

## 1. Board columns (field "Research Stage")

| Column | Meaning | Entry criteria | Exit criteria |
| --- | --- | --- | --- |
| **Backlog** | Identified, not yet planned | Issue created with template | Prioritised + assigned |
| **To Do** | Planned for the current cycle | Assignee, labels, due date | Branch created |
| **In Progress** | Being worked on | Branch exists | PR opened |
| **Internal Review** | PR under peer review | PR "Ready for review" | Peer approval |
| **Methodology Review** | Needs Methodology Lead | label `review:methodology` | ML approval |
| **Statistical Review** | Needs Analysis Lead / statistician | label `review:statistics` | AL approval |
| **Approved** | All approvals, checks green | Required approvals | Merged |
| **Completed** | Merged and issue closed | Merge | — |
| **Archived** | Obsolete / won't do / old releases | Decision noted in issue | — |

Built-in automations to enable (Project → Workflows): *Item added → Backlog*,
*Pull request merged → Completed*, *Item closed → Completed*, *Auto-archive items* (closed > 30 days).

## 2. Additional project fields

| Field | Type | Values |
| --- | --- | --- |
| Research Stage | single select | columns above |
| Work Package | single select | Protocol, Fieldwork, Data, Analysis, Reporting, Management |
| Priority | single select | P1-High, P2-Medium, P3-Low |
| Due date | date | — |
| Effort | number | person-days |

Recommended views: **Board** (grouped by Research Stage), **By person** (table grouped by assignee),
**Timeline** (roadmap by due date), **Review queue** (filter `label:review-required`).

## 3. Labels

| Label | Colour | Use |
| --- | --- | --- |
| `data` | `#1d76db` | Anything touching data or data scripts |
| `data-cleaning` | `#5319e7` | Cleaning rules / stage 02 |
| `methodology` | `#0e8a16` | Protocol, sampling, questionnaire, weighting design |
| `analysis` | `#fbca04` | Analysis scripts and outputs |
| `statistics` | `#c5def5` | Statistical method questions |
| `documentation` | `#0075ca` | Docs only |
| `report` | `#d4c5f9` | Report writing |
| `fieldwork` | `#bfd4f2` | Field operations |
| `technical` | `#e4e669` | Git, CI, environment |
| `urgent` | `#b60205` | Must be handled within 48h |
| `review-required` | `#ff9f1c` | Waiting for a reviewer |
| `review:methodology` | `#0e8a16` | Needs methodology review |
| `review:statistics` | `#fbca04` | Needs statistical review |
| `review:data` | `#1d76db` | Needs data-manager review |
| `sensitive` | `#000000` | Involves sensitive data **process** — never put the data itself in the issue |
| `blocked` | `#e11d21` | Cannot progress; say why |
| `decision-needed` | `#f9d0c4` | Requires a decision by the leads |
| `release` | `#0052cc` | Release preparation |
| `no-changelog` | `#eeeeee` | PR intentionally without CHANGELOG entry |
| `good-first-task` | `#7057ff` | Suitable for new team members |

## 4. Issue hygiene

- One issue = one deliverable a single person can finish in ≤ 1 week (split larger tasks).
- Title: imperative + object — "Recode education into 4 categories".
- Always: assignee, labels, project, milestone (phase), acceptance criteria.
- Milestones = project phases: `M1 Protocol`, `M2 Fieldwork`, `M3 Data`, `M4 Analysis`, `M5 Report`.
