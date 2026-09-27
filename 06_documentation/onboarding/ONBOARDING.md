# Onboarding & Offboarding

Goal: a new researcher understands the project and makes a first reviewed contribution
within **two days**.

## Day 1 — understand

1. Read, in order (≈ 2 hours):
   [README](../../README.md) → [DATA_SECURITY](../../DATA_SECURITY.md) →
   [CONTRIBUTING](../../CONTRIBUTING.md) → [RESEARCH_PROTOCOL](../../01_protocol/RESEARCH_PROTOCOL.md) →
   [ANALYSIS_PLAN](../../01_protocol/ANALYSIS_PLAN.md) → [PIPELINE](../analysis_documentation/PIPELINE.md) →
   [DATA_DICTIONARY](../../02_data/data_dictionary/DATA_DICTIONARY.md).
2. Browse the last 10 merged Pull Requests and the [Decision Log](../../00_project_management/decisions/DECISION_LOG.md).
3. Open the Project board and read the issues assigned to you.

## Day 1 — set up

- [ ] GitHub account with **two-factor authentication** enabled
- [ ] Accepted repository / organization invitation
- [ ] Git configured (`user.name`, no-reply `user.email`), Git LFS installed
- [ ] Repository cloned; Python/R environment installed; `pre-commit install` done
- [ ] Signed confidentiality agreement / data-use terms ([AGREEMENT_REF]) — **before** any data access
- [ ] Completed data-protection / research-ethics training ([TRAINING_REF])
- [ ] Data access requested via Issue and granted by the Data Manager (only the stages you need)
- [ ] `.env` created with `DATA_ROOT`; `python tools/data_manifest.py verify` succeeds

## Day 2 — first contribution

Pick an issue labelled `good-first-task`, follow the workflow in CONTRIBUTING §3,
open a PR and go through review. Ask questions in the issue — not in private chat — so
the answers stay documented.

## Buddy

Each newcomer is assigned a buddy: [BUDDY_ROLE]. The buddy reviews the first PR.

## Offboarding checklist (same day the person leaves)

- [ ] Open work re-assigned; branches merged or closed
- [ ] Repository / organization access removed (GitHub → Settings → Collaborators / Teams)
- [ ] Secure-storage access removed; shared credentials rotated if they were known to the person
- [ ] Local copies of data deleted — written confirmation stored by the Data Manager
- [ ] Devices returned / wiped as per institutional policy
- [ ] Roles table in [ROLES_AND_PERMISSIONS.md](../../00_project_management/team/ROLES_AND_PERMISSIONS.md) and CODEOWNERS updated
