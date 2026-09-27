<div dir="rtl">

# دليل التنفيذ — إنشاء المستودع البحثي وتشغيله

هذا الدليل موجّه لمسؤول المشروع (Project Lead) لتنفيذ الحزمة كاملة على GitHub، ثم لتشغيلها يوميًا مع الفريق.

## أ. الاسم والوصف المقترحان

| البند | المقترح |
| --- | --- |
| اسم المستودع | `research-project-template` كقالب عام، ولكل دراسة: `<org>-<study>-<year>` بحروف صغيرة، مثل `[org]-[study]-2026` |
| الوصف | Reproducible, secure and auditable repository for collaborative survey and quantitative research: data pipeline from raw to analysis-ready, reviewed workflow, data-protection guardrails. |
| الرؤية | **Private** (خاص) — ويُفتح للعامة فقط بعد قرار رسمي وفحص إفصاح |

## ب. قرارات التصميم الرئيسية

1. **GitHub ليس مخزن البيانات.** البيانات تبقى في تخزين آمن (`DATA_ROOT`)، والمستودع يحفظ الكود والقواعد والتوثيق وسجل البصمات `DATA_MANIFEST.csv` الذي يربط كل إصدار بالبيانات المستخدمة بايتًا ببايت.
2. **GitHub Flow بدل Git Flow:** فرع `main` محمي + فروع قصيرة بالبادئات `data/`, `analysis/`, `method/`, `report/`, `docs/`, `fix/`, `chore/`. لا يوجد `develop` لأنه يضيف تعقيدًا دون فائدة لفريق صغير/متوسط.
3. **القرارات كبيانات:** قواعد التنظيف وإعادة الترميز وأهداف الترجيح ملفات CSV تُراجَع في Pull Request، ثم تطبقها السكربتات — فيبقى كل تعديل على البيانات موثقًا ومعروف الصاحب.
4. **خط معالجة مرقّم وحتمي:** 01 تحقق ← 02 تنظيف وإخفاء الهوية ← 03 إعادة ترميز ← 04 أوزان ← 05 ملف التحليل ← 06 وصفي ← 07 مقارن ← 08 رسوم. تشغيله مرتين يعطي ملفات متطابقة تمامًا (تم اختباره).
5. **حواجز آلية على ثلاث طبقات:** `.gitignore` ← `pre-commit` على جهاز الباحث ← GitHub Actions على كل PR.
6. **لم تُفترض أي منهجية أو أرقام:** مستوى الثقة، أثر التصميم، الحد الأدنى للخلية، طريقة الترجيح — كلها REQUIRED في `config/project.yml`، والسكربتات تتوقف برسالة واضحة إن لم تُحدَّد.

## ج. ما يُرفع وما لا يُرفع

| يُرفع إلى Git | Git LFS | لا يُرفع إطلاقًا (تخزين آمن فقط) |
| --- | --- | --- |
| الكود، التوثيق، قاموس البيانات، سجل البصمات، قواعد التنظيف، الجداول المجمّعة، SVG | PDF, DOCX, XLSX, PPTX, PNG/JPG، ملف تحليل مُزال الهوية بعد الموافقة، البيانات العامة المعتمدة | البيانات الخام بأي صيغة (CSV/XLSX/SAV/DTA/RData/ZIP)، المعرّفات، مفتاح الربط، الصوت والصور والإحداثيات، استمارات الموافقة، `.env` وكلمات المرور والمفاتيح |

البدائل للبيانات الحساسة أو الكبيرة: خادم أبحاث مؤسسي، SharePoint/OneDrive أو Google Workspace بصلاحيات مقيّدة، حاويات مشفرة (VeraCrypt/Cryptomator) لمفتاح الربط، أو DVC مع مخزن آمن لمن يريد إصدارات بيانات مرتبطة بـ Git.

## د. خطوات الإنشاء (مرة واحدة)

### 1. المتطلبات

- حساب GitHub مع **المصادقة الثنائية (2FA)**.
- يُفضّل إنشاء **GitHub Organization** للمؤسسة (من الموقع: <https://github.com/organizations/plan>) — لا يمكن إنشاؤها عبر API أو CLI.
- حماية الفروع للمستودعات **الخاصة** تتطلب خطة GitHub Team للمنظمات أو Pro للحسابات الشخصية؛ على الخطة المجانية تعمل فقط للمستودعات العامة.
- ثبّت: Git، Git LFS، GitHub CLI (`gh`)، Python 3.11+.

</div>

```bash
gh auth login
gh auth refresh -s project,admin:org      # للوحة المشروع وفرق المنظمة
```

<div dir="rtl">

### 2. تجهيز الملفات

1. فكّ ضغط الحزمة، وادخل إلى المجلد.
2. املأ القيم الأساسية: `README.md`، `CITATION.cff`، `config/project.yml` (على الأقل `short_name`)، وجدول الفريق.
3. عدّل كتلة **CONFIGURATION** في `tools/setup_github.sh`: `OWNER`، `REPO`، أسماء المستخدمين لأصحاب الأدوار، والفرق أو المتعاونين.

### 3. التشغيل الآلي

</div>

```bash
DRY_RUN=1 bash tools/setup_github.sh    # معاينة الأوامر دون تنفيذ
bash tools/setup_github.sh              # التنفيذ الفعلي
```

<div dir="rtl">

ينفّذ السكربت: استبدال الـ placeholders في الروابط وCODEOWNERS ← `git init` وLFS وأول commit ← إنشاء المستودع ورفعه ← إعدادات الدمج (Squash فقط، حذف الفروع تلقائيًا) ← 20 وسمًا ← 5 مراحل Milestones ← حماية `main` ← ميزات الأمان ← الفرق/المتعاونين ← لوحة Project بحقولها.

### 4. أوامر GitHub CLI اليدوية (بديل للسكربت أو لخطوات منفردة)

</div>

```bash
OWNER=your-org; REPO=your-repo

# إنشاء المستودع ورفع الملفات
git init -b main && git lfs install --local && git add -A
git commit -m "chore: initialise research repository structure (v0.1.0)"
gh repo create "$OWNER/$REPO" --private --source . --remote origin --push \
  --description "Reproducible, secure and auditable research repository"

# إعدادات الدمج
gh repo edit "$OWNER/$REPO" --enable-squash-merge --enable-merge-commit=false \
  --enable-rebase-merge=false --delete-branch-on-merge --enable-wiki=false

# وسم (كرر لكل وسم في PROJECT_BOARD.md)
gh label create "review:statistics" --repo "$OWNER/$REPO" --color fbca04 \
  --description "Needs statistical review" --force

# مرحلة
gh api "repos/$OWNER/$REPO/milestones" -f title="M1 Protocol"

# حماية الفرع main
gh api -X PUT "repos/$OWNER/$REPO/branches/main/protection" --input - <<'JSON'
{"required_status_checks":{"strict":true,"contexts":["structure-and-security","docs-check"]},
 "enforce_admins":true,
 "required_pull_request_reviews":{"required_approving_review_count":1,"require_code_owner_reviews":true,
   "dismiss_stale_reviews":true,"require_last_push_approval":true},
 "restrictions":null,"required_linear_history":true,"allow_force_pushes":false,
 "allow_deletions":false,"required_conversation_resolution":true}
JSON

# فحص الأسرار (حسب الخطة والرؤية)
gh api -X PATCH "repos/$OWNER/$REPO" \
  -f "security_and_analysis[secret_scanning][status]=enabled" \
  -f "security_and_analysis[secret_scanning_push_protection][status]=enabled"

# فرق المنظمة وصلاحياتها
gh api "orgs/$OWNER/teams" -f name="data-team" -f privacy=closed
gh api -X PUT "orgs/$OWNER/teams/data-team/repos/$OWNER/$REPO" -f permission=maintain
gh api -X PUT "orgs/$OWNER/teams/data-team/memberships/GITHUB_HANDLE" -f role=member

# دعوة متعاون فردي (pull | triage | push | maintain | admin)
gh api -X PUT "repos/$OWNER/$REPO/collaborators/GITHUB_HANDLE" -f permission=push

# لوحة المشروع
gh project create --owner "$OWNER" --title "Research Board"
gh project field-create <NUMBER> --owner "$OWNER" --name "Research Stage" --data-type SINGLE_SELECT \
  --single-select-options "Backlog,To Do,In Progress,Internal Review,Methodology Review,Statistical Review,Approved,Completed,Archived"
gh project link <NUMBER> --owner "$OWNER" --repo "$OWNER/$REPO"

# أول إصدار
git tag -a v0.1.0 -m "v0.1.0 repository set up" && git push origin v0.1.0
```

<div dir="rtl">

### 5. خطوات يدوية في واجهة GitHub

- المنظمة: Settings ← Authentication security ← **Require two-factor authentication**.
- اللوحة: New view ← Board ← Group by **Research Stage**؛ وفي Workflows فعّل: Item added ← Backlog، PR merged ← Completed، Auto-archive.
- تأكد من ظهور قاعدة الحماية في Settings ← Branches، وأن فحصَي `structure-and-security` و`docs-check` ظهرا بعد أول PR.
- ملاحظة: الحماية مع `enforce_admins` تحتاج **شخصين على الأقل** بصلاحية Write، لأن صاحب الـ PR لا يستطيع الموافقة على عمله.

## هـ. دعوة أعضاء الفريق

1. أضف كل عضو إلى الفريق المناسب (أو كمتعاون) بالصلاحية المحددة في `ROLES_AND_PERMISSIONS.md`.
2. حدّث CODEOWNERS إن تغيّر الأشخاص (أو استخدم الفرق `@org/data-team` لتجنب ذلك).
3. يتبع العضو الجديد `ONBOARDING.md`: توقيع اتفاقية السرية والتدريب **قبل** أي وصول للبيانات، ثم أول PR.
4. الوصول للتخزين الآمن يُمنح من مسؤول البيانات بطلب عبر Issue، وبالمراحل اللازمة فقط.

## و. العمل اليومي للباحث

</div>

```bash
git switch main && git pull --ff-only                    # 1 سحب آخر التحديثات
git switch -c analysis/42-crosstabs-by-region            # 2 فرع للمهمة #42
# 3 العمل على المهمة
git add <files> && git commit -m "analysis(crosstabs): add region tables (refs #42)"   # 4
git push -u origin analysis/42-crosstabs-by-region       # 5
gh pr create --fill --base main --label analysis         # 6 ثم تعبئة النموذج
# 7-9 المراجعة والتصحيح والموافقة ← 10 Squash and merge ← 11 تُغلق المهمة تلقائيًا بـ Closes #42
```

<div dir="rtl">

## ز. خطوات رفع البيانات (مسؤول البيانات فقط)

1. ضع الملف كما وصل في `$DATA_ROOT/raw/` باسم `<short>_raw_<source>_<YYYYMMDD>.<ext>`، واجعله للقراءة فقط.
2. سجّل الاستلام في `02_data/raw/README.md` (دون بيانات شخصية).
3. أضف اسم الملف إلى `data.raw_files` في `config/project.yml`، وحدّث قاموس البيانات بالمتغيرات وتصنيف `pii`.
4. شغّل `python 03_scripts/run_pipeline.py --only 01` وراجع تقرير التحقق.
5. افتح PR يحتوي **فقط**: الإعدادات، القاموس، `DATA_MANIFEST.csv`، تقرير الجودة المجمّع.

## ح. خطوات إجراء التحليل

1. اعتمد `ANALYSIS_PLAN.md` ووسمه (`sap-v1.0`) قبل تحليل البيانات النهائية.
2. أدخل القيم المطلوبة في `config/project.yml` (مستوى الثقة، أثر التصميم، الحد الأدنى للخلية، الترجيح، المتغيرات).
3. اكتب قواعد التنظيف وإعادة الترميز في ملفات CSV عبر PRs منفصلة ومراجَعة.
4. شغّل `python 03_scripts/run_pipeline.py`، راجع `04_analysis/qc_reports/`، ثم ارفع الجداول والرسوم والسجل في PR.
5. التحليلات بتصميم معقّد (طبقات/عناقيد) تُنفّذ بـ R `survey` أو Stata `svy` بنفس الترقيم، وتُحفظ في `statistical_outputs/`.

## ط. خطوات مراجعة النتائج

1. يعيد مراجعٌ مستقل تشغيل الخط من نسخة نظيفة ويتأكد أن `git status` لا يُظهر أي فرق في `04_analysis/`.
2. تطبيق القسم المناسب من `QC_CHECKLIST.md` داخل الـ PR.
3. مطابقة كل رقم في التقرير مع ملف جدول، ومطابقة النسختين العربية والإنجليزية.
4. أي تعديل على رقم منشور = إصدار MINOR على الأقل + تصويب في CHANGELOG.

## ي. إصدار نسخة نهائية

1. Issue بعنوان "Release v1.0.0" ← فرع `chore/<n>-release-v1.0.0`.
2. نقل البنود من `[Unreleased]` في CHANGELOG وذكر نسخة البيانات، وتحديث `CITATION.cff`.
3. `python tools/check_docs.py --strict` يجب أن ينجح (لا placeholders في الوثائق الأساسية).
4. موافقة مسؤول المشروع ثم الدمج، ثم:

</div>

```bash
git switch main && git pull --ff-only
git tag -a v1.0.0 -m "v1.0.0 — final report results (data v1.3)"
git push origin v1.0.0          # يُنشئ GitHub Release تلقائيًا من CHANGELOG
```

<div dir="rtl">

## ك. قائمة التحقق قبل بدء العمل

- [ ] المنظمة/الحساب مع 2FA إلزامي، والمستودع **خاص**
- [ ] كل الـ placeholders الأساسية مملوءة (المشروع، الفريق، التخزين الآمن، جهات الاتصال)
- [ ] CODEOWNERS يحتوي أسماء/فرقًا حقيقية لها صلاحية Write
- [ ] حماية `main` مفعّلة: PR إلزامي، موافقة CODEOWNER، فحصان إلزاميان، لا دفع قسري، تشمل المدراء
- [ ] الفحوص الآلية نجحت على أول PR تجريبي
- [ ] فحص الأسرار مفعّل (إن توفر في الخطة) + `pre-commit install` لدى كل عضو
- [ ] التخزين الآمن جاهز بمجلداته: raw, restricted, cleaned, processed, analysis_ready — مع صلاحيات ونسخ احتياطي
- [ ] خطة إدارة البيانات والبروتوكول معتمدان، والموافقة الأخلاقية موثقة
- [ ] الوسوم والمراحل ولوحة المشروع جاهزة
- [ ] كل عضو قرأ README وDATA_SECURITY وCONTRIBUTING ووقّع اتفاقية السرية
- [ ] اختبار تجريبي: رفع ملف باسم `final.xlsx` أو يحتوي بريدًا إلكترونيًا يجب أن **يفشل** في الفحص
- [ ] الإصدار `v0.1.0` موسوم

## ل. خريطة المطلوب ← الملف

| المطلوب | الملف |
| --- | --- |
| README (EN/AR) | `README.md`, `README.ar.md` |
| CONTRIBUTING + نظام الفروع + الـ commits + سير العمل اليومي | `CONTRIBUTING.md` |
| SECURITY + التعامل مع التسريب | `SECURITY.md` |
| سياسة البيانات الحساسة + Git LFS + ربط نسخة البيانات | `DATA_SECURITY.md` |
| خطة إدارة البيانات | `06_documentation/data_management/DATA_MANAGEMENT_PLAN.md` |
| بروتوكول البحث | `01_protocol/RESEARCH_PROTOCOL.md` |
| خطة التحليل | `01_protocol/ANALYSIS_PLAN.md` |
| قاموس البيانات | `02_data/data_dictionary/DATA_DICTIONARY.md` + `data_dictionary.csv` |
| CODEOWNERS / قوالب Issues / قالب PR | `.github/CODEOWNERS`, `.github/ISSUE_TEMPLATE/*.yml`, `.github/PULL_REQUEST_TEMPLATE.md` |
| GitHub Actions | `.github/workflows/validation.yml`, `documentation-check.yml`, `release.yml` |
| `.gitignore` / `.gitattributes` / `.editorconfig` / pre-commit | ملفات الجذر |
| الإصدارات + الإصدار النهائي | `06_documentation/governance/VERSIONING.md`, `RELEASE_PROCESS.md`, `CHANGELOG.md` |
| تسمية الملفات / اللغة | `06_documentation/governance/NAMING_CONVENTIONS.md`, `LANGUAGE_POLICY.md` |
| الأدوار والصلاحيات | `00_project_management/team/ROLES_AND_PERMISSIONS.md` |
| Projects + Labels + Issues | `06_documentation/governance/PROJECT_BOARD.md` |
| مراجعة الجودة | `06_documentation/quality_control/QC_CHECKLIST.md` |
| إعادة الإنتاج وخط المعالجة | `06_documentation/analysis_documentation/PIPELINE.md`, `03_scripts/` |
| الاستطلاعات: العينة، العمل الميداني، الاستبيان، الأخلاقيات | `01_protocol/sampling/`, `fieldwork/`, `questionnaire/`, `ethics/` |
| الانضمام والمغادرة | `06_documentation/onboarding/ONBOARDING.md` |
| إنشاء المستودع آليًا | `tools/setup_github.sh` |

</div>

<div dir="rtl">

## م. شجرة الملفات النهائية

</div>

```text
research-project-template/
├── .editorconfig
├── .gitattributes
├── .github/
│   ├── CODEOWNERS
│   ├── ISSUE_TEMPLATE/
│   │   ├── 01_research_task.yml
│   │   ├── 02_data_issue.yml
│   │   ├── 03_analysis_issue.yml
│   │   ├── 04_review_request.yml
│   │   ├── 05_technical_issue.yml
│   │   └── config.yml
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── workflows/
│       ├── documentation-check.yml
│       ├── release.yml
│       └── validation.yml
├── .gitignore
├── .lychee.toml
├── .markdownlint-cli2.yaml
├── .pre-commit-config.yaml
├── .sensitive-allowlist
├── 00_project_management/
│   ├── README.md
│   ├── decisions/
│   │   ├── DECISION_LOG.md
│   │   └── DR-000_template.md
│   ├── meeting_minutes/
│   │   └── _TEMPLATE_meeting_minutes.md
│   ├── project_plan/
│   │   └── PROJECT_PLAN.md
│   ├── tasks/
│   │   └── README.md
│   └── team/
│       └── ROLES_AND_PERMISSIONS.md
├── 01_protocol/
│   ├── ANALYSIS_PLAN.md
│   ├── README.md
│   ├── RESEARCH_PROTOCOL.md
│   ├── ethics/
│   │   └── README.md
│   ├── fieldwork/
│   │   ├── FIELDWORK_MANUAL.md
│   │   └── README.md
│   ├── methodology/
│   │   └── README.md
│   ├── questionnaire/
│   │   ├── README.md
│   │   ├── ar/
│   │   │   └── README.md
│   │   ├── en/
│   │   │   └── README.md
│   │   └── versions/
│   │       └── README.md
│   └── sampling/
│       ├── README.md
│       └── SAMPLING_PLAN.md
├── 02_data/
│   ├── README.md
│   ├── analysis_ready/
│   │   ├── README.md
│   │   └── approved_deid/
│   │       └── README.md
│   ├── cleaned/
│   │   └── README.md
│   ├── data_dictionary/
│   │   ├── DATA_DICTIONARY.md
│   │   ├── README.md
│   │   └── data_dictionary.csv
│   ├── metadata/
│   │   ├── DATA_MANIFEST.csv
│   │   └── README.md
│   ├── processed/
│   │   └── README.md
│   └── raw/
│       └── README.md
├── 03_scripts/
│   ├── 01_validation/
│   │   └── 01_validate_raw.py
│   ├── 02_cleaning/
│   │   ├── 02_clean.py
│   │   └── cleaning_rules.csv
│   ├── 03_recoding/
│   │   ├── 03_recode.py
│   │   └── recode_map.csv
│   ├── 04_weighting/
│   │   ├── 04_weight.py
│   │   └── weighting_targets.csv
│   ├── 05_analysis_dataset/
│   │   └── 05_build_analysis_dataset.py
│   ├── 06_descriptive_analysis/
│   │   └── 06_descriptives.py
│   ├── 07_comparative_analysis/
│   │   └── 07_crosstabs.py
│   ├── 08_visualization/
│   │   └── 08_figures.py
│   ├── README.md
│   ├── _lib/
│   │   ├── __init__.py
│   │   ├── pipeline_utils.py
│   │   └── stats_utils.py
│   └── run_pipeline.py
├── 04_analysis/
│   ├── README.md
│   ├── analysis_reports/
│   ├── figures/
│   ├── qc_reports/
│   ├── statistical_outputs/
│   └── tables/
├── 05_reports/
│   ├── README.md
│   ├── drafts/
│   ├── final/
│   └── reviewed/
├── 06_documentation/
│   ├── README.md
│   ├── analysis_documentation/
│   │   ├── CLEANING_LOG.md
│   │   └── PIPELINE.md
│   ├── data_management/
│   │   └── DATA_MANAGEMENT_PLAN.md
│   ├── governance/
│   │   ├── IMPLEMENTATION_GUIDE.ar.md
│   │   ├── LANGUAGE_POLICY.md
│   │   ├── NAMING_CONVENTIONS.md
│   │   ├── PROJECT_BOARD.md
│   │   ├── RELEASE_PROCESS.md
│   │   └── VERSIONING.md
│   ├── methodology/
│   │   ├── METHODOLOGICAL_NOTES.md
│   │   └── README.md
│   ├── onboarding/
│   │   └── ONBOARDING.md
│   └── quality_control/
│       └── QC_CHECKLIST.md
├── 07_outputs/
│   ├── README.md
│   ├── charts/
│   ├── datasets/
│   ├── publications/
│   └── tables/
├── 99_archive/
│   ├── README.md
│   └── previous_versions/
├── CHANGELOG.md
├── CITATION.cff
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── DATA_SECURITY.md
├── LICENSE
├── README.ar.md
├── README.md
├── SECURITY.md
├── config/
│   ├── .env.example
│   ├── README.md
│   └── project.yml
├── requirements.txt
└── tools/
    ├── README.md
    ├── check_docs.py
    ├── check_sensitive.py
    ├── check_structure.py
    ├── data_manifest.py
    └── setup_github.sh
```
