# Contributing to [PROJECT_NAME]

This guide is binding for every team member. It exists so that every change is
**reviewed, traceable, reversible and reproducible**.

> ملخص عربي سريع في نهاية الملف — [Arabic quick guide](#arabic-quick-guide--دليل-سريع-بالعربية).

---

## 0. Golden rules

1. **Never push to `main`.** All work goes `Branch → Pull Request → Review → Merge`.
2. **Never commit personal or identifiable data, raw data, or secrets.** See [DATA_SECURITY.md](DATA_SECURITY.md).
3. **Never edit data by hand.** Data change only through scripts in `03_scripts/` and documented rules.
4. **Every change starts from an Issue.** No issue, no branch.
5. **Every result must be reproducible** from `main` + the data version recorded in the manifest.
6. **Document as you go.** A PR that changes data or analysis without updating docs is not complete.

---

## 1. First-time setup

```bash
git clone https://github.com/[ORG_OR_USER]/[REPO_NAME].git
cd [REPO_NAME]

# Identity used in the audit trail — use your real name and GitHub no-reply e-mail
git config user.name  "Your Name"
git config user.email "ID+username@users.noreply.github.com"

# Large-file support (needed only for approved LFS files)
git lfs install

# Python environment
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Local safety net: blocks secrets, large files and sensitive files before they are committed
pip install pre-commit && pre-commit install

# Secure data location (outside the repository)
cp config/.env.example .env     # edit DATA_ROOT
```

Read, in this order: [README.md](README.md) → [DATA_SECURITY.md](DATA_SECURITY.md) →
this file → [ONBOARDING.md](06_documentation/onboarding/ONBOARDING.md).

---

## 2. Branching strategy

We use **GitHub Flow with typed branch prefixes and release tags**.

```text
main  ●────●────●────●────●────●──── (protected; tags v0.1.0, v0.2.0, v1.0.0 …)
        \      /  \      /
         data/12-clean-age   analysis/15-crosstabs
```

### Why no `develop` branch?

A `develop` branch (Git Flow) is designed for software with parallel release trains.
A small/medium research team gains nothing from it and pays a real cost: two long-lived
branches drift apart, reviewers do not know which one is "true", and results produced on
`develop` are not the ones on `main`. With GitHub Flow:

- `main` is the **single source of truth**: always reviewed, always reproducible.
- Short-lived branches (hours to a few days) keep reviews small.
- A **release** is simply a tag on `main` (e.g. `v1.0.0` = results of the final report).

> If the project grows to several parallel studies or waves that must be frozen while
> work continues, add a temporary `release/vX.Y` branch for the frozen report only.

### Branch naming

`<type>/<issue-number>-<short-kebab-description>` — lowercase, ASCII, no spaces.

| Prefix | Use for | Example |
| --- | --- | --- |
| `data/` | validation, cleaning, recoding, weighting, cleaning rules | `data/12-recode-education` |
| `analysis/` | statistical analysis, tables, figures | `analysis/15-crosstabs-region` |
| `method/` | protocol, questionnaire, sampling, analysis plan | `method/8-update-sampling-frame` |
| `report/` | report drafts and revisions | `report/30-chapter-3-draft` |
| `docs/` | documentation only | `docs/21-update-dictionary` |
| `fix/` | correction of an error already on `main` | `fix/40-weight-calculation` |
| `chore/` | tooling, CI, repository settings | `chore/5-add-link-check` |

---

## 3. Daily workflow (step by step)

```bash
# 1. Pull latest changes
git switch main
git pull --ff-only

# 2. Create a branch for your assigned issue (#42)
git switch -c analysis/42-crosstabs-by-region

# 3. Work on the task … run the relevant pipeline stage locally
python 03_scripts/run_pipeline.py --only 07

# 4. Commit changes (small, meaningful commits)
git add 03_scripts/07_comparative_analysis/ 04_analysis/tables/
git commit -m "analysis(crosstabs): add weighted tables by region (refs #42)"

# 5. Push the branch
git push -u origin analysis/42-crosstabs-by-region

# 6. Open a Pull Request (web UI or GitHub CLI)
gh pr create --fill --base main --label analysis --label review-required

# 7–8. Reviewer comments → you fix on the same branch
git commit -am "analysis(crosstabs): apply suppression rule n<[MIN_CELL_SIZE] (refs #42)"
git push

# 9–10. After approval + green checks, a maintainer clicks "Squash and merge"
# 11. The issue closes automatically if the PR body contains "Closes #42"

# Clean up locally
git switch main && git pull --ff-only && git branch -d analysis/42-crosstabs-by-region
```

**Keep your branch up to date** if `main` moved: `git fetch origin && git rebase origin/main`
(then `git push --force-with-lease` — allowed on *your own* branch only, never on `main`).

---

## 4. Commit messages

Format: `<type>(<scope>): <imperative summary> (refs #<issue>)`

| Type | Meaning |
| --- | --- |
| `data` | data-processing scripts, cleaning/recoding rules, manifest updates |
| `analysis` | analysis code or generated analysis outputs |
| `method` | protocol, questionnaire, sampling, analysis plan |
| `report` | report text |
| `docs` | documentation |
| `fix` | correction of an error |
| `chore` | tooling, CI, configuration |
| `release` | version bump + changelog for a release |

Examples:

```text
data(cleaning): set age>110 to missing per rule CLN-004 (refs #12)
method(questionnaire): add Q17 translation v1.2 (refs #8)
fix(weighting): correct raking target for region 3 (closes #40)
release: v1.0.0 final report results
```

Rules: English, ≤ 72 characters in the summary line, explain *why* in the body when not obvious.

---

## 5. Pull Requests

- Open the PR **early as Draft** if you want feedback; mark *Ready for review* when done.
- Fill in **every** section of the PR template. "N/A" is acceptable; blank is not.
- Link the issue with `Closes #<n>` (or `Refs #<n>` if the issue stays open).
- Keep PRs focused: do not mix data-cleaning changes with report editing.
- The author **never** merges their own PR without the required approvals.
- Merge method: **Squash and merge** (one clean, reviewed commit per change on `main`).
- Resolve all review conversations before merging.

### Review requirements

| What changed | Required approval |
| --- | --- |
| `02_data/`, `03_scripts/01–05`, cleaning/recoding rules, `DATA_MANIFEST.csv` | Data Manager |
| `01_protocol/`, `ANALYSIS_PLAN.md`, weighting method | Methodology Lead |
| `03_scripts/06–08`, `04_analysis/` | Analysis Lead (statistical review) |
| `05_reports/`, `07_outputs/` | Report Lead **and** Project Lead for `final/` and `07_outputs/` |
| `.github/`, `tools/`, `config/`, security docs | Project Lead |

These are enforced by [CODEOWNERS](.github/CODEOWNERS) + branch protection.

### What reviewers check

Use the checklist in [QC_CHECKLIST.md](06_documentation/quality_control/QC_CHECKLIST.md):

- **Correctness** — does the code do what the issue/analysis plan says?
- **Reproducibility** — can the reviewer re-run the stage and get the same output?
- **Traceability** — are decisions logged, rules documented, manifest updated?
- **Data protection** — no identifiers, small cells suppressed, no secrets.
- **Documentation** — dictionary, pipeline docs and CHANGELOG updated.

---

## 6. Issues

Use the templates (they appear when you click *New issue*):

| Template | Use it for |
| --- | --- |
| Research Task | any planned piece of work |
| Data Issue | a problem found in the data (inconsistency, outlier, coding error) |
| Analysis Issue | a problem or question about an analysis or result |
| Review Request | asking for methodological / statistical / data / report review |
| Technical Issue | Git, scripts, environment, CI problems |

Every issue gets: an **assignee**, at least one **label**, and is added to the **Project board**.
Do **not** paste participant-level data into issues — reference record IDs only
(pseudonymous `resp_id`), never names or contact details.

---

## 7. Working with data (short version)

1. Raw data arrive **only** in the secure storage (`$DATA_ROOT/raw/`), placed by the Data Manager.
2. You never open raw data in Excel and save it — that silently changes types and dates.
3. Cleaning/recoding decisions are written as **rules** in
   `03_scripts/02_cleaning/cleaning_rules.csv` and `03_scripts/03_recoding/recode_map.csv`,
   reviewed through a PR, then applied by the scripts.
4. Scripts write outputs to `$DATA_ROOT/<stage>/` and register them in
   `02_data/metadata/DATA_MANIFEST.csv` automatically.
5. Commit the **scripts, rules, manifest and aggregate QC reports** — never the data files.

Full workflow: [PIPELINE.md](06_documentation/analysis_documentation/PIPELINE.md).

---

## 8. File naming

See [NAMING_CONVENTIONS.md](06_documentation/governance/NAMING_CONVENTIONS.md). In short:
lowercase, `snake_case`, ASCII, no spaces, ISO dates, explicit versions —
**never** `final.xlsx`, `final2.xlsx`, `latest.xlsx`, `new.xlsx`. CI rejects these names.

---

## 9. Documentation duties

| If you change… | Also update… |
| --- | --- |
| a variable or its coding | `02_data/data_dictionary/` (MD + CSV) |
| a cleaning/recoding rule | the rule file + `06_documentation/analysis_documentation/CLEANING_LOG.md` |
| methodology or analysis plan | the protocol/plan + a decision record in `00_project_management/decisions/` |
| anything user-visible | `CHANGELOG.md` → `## [Unreleased]` |

---

## Arabic quick guide — دليل سريع بالعربية

<div dir="rtl">

- لا يُسمح بالعمل مباشرة على الفرع `main` إطلاقًا.
- كل عمل يبدأ من **Issue**، ثم فرع باسم مثل `analysis/42-crosstabs-by-region`.
- المسار الإلزامي: **فرع ← طلب دمج (Pull Request) ← مراجعة ← دمج**.
- لا تُرفع أي بيانات شخصية أو خام أو كلمات مرور إلى GitHub. البيانات تبقى في التخزين الآمن.
- لا تُعدّل البيانات يدويًا؛ كل تعديل عبر سكربت وقاعدة موثقة.
- أسماء الملفات والفروع والمتغيرات والكود بالإنجليزية، بحروف صغيرة وبدون مسافات.
- حدّث قاموس البيانات وسجل التغييرات (CHANGELOG) مع كل تعديل مؤثر.
- إذا اشتبهت برفع بيانات حساسة: توقّف فورًا وأبلغ وفق [SECURITY.md](SECURITY.md).

</div>
