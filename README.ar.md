<div dir="rtl">

# [PROJECT_NAME]

> مستودع بحثي تعاوني آمن وقابل لإعادة الإنتاج لمشروع **[PROJECT_NAME]** — [ORGANIZATION_NAME].
>
> English version: [README.md](README.md) (النسخة الإنجليزية هي المرجع الرسمي عند الاختلاف).
>
> دليل التنفيذ خطوة بخطوة: [IMPLEMENTATION_GUIDE.ar.md](06_documentation/governance/IMPLEMENTATION_GUIDE.ar.md)

## ١. وصف المشروع

[وصف مختصر من 3–5 جمل: ماذا يُدرس، وأين، ومع من، ولماذا. لا تضع هنا أي معلومات عن المشاركين.]

## ٢. أهداف البحث

1. [الهدف الأول]
2. [الهدف الثاني]

الأسئلة البحثية والفرضيات مفصّلة في [بروتوكول البحث](01_protocol/RESEARCH_PROTOCOL.md).

## ٣. فريق البحث

الأدوار والصلاحيات في [ROLES_AND_PERMISSIONS.md](00_project_management/team/ROLES_AND_PERMISSIONS.md):
المسؤول العام [PROJECT_LEAD]، مسؤول البيانات [DATA_MANAGER]، مسؤول المنهجية [METHODOLOGY_LEAD]،
مسؤول التحليل الإحصائي [ANALYSIS_LEAD]، منسق العمل الميداني [FIELDWORK_COORDINATOR].

## ٤. المنهجية (ملخص)

التصميم: [STUDY_DESIGN] · المجتمع: [TARGET_POPULATION] · العينة: [SAMPLING_DESIGN] ·
حجم العينة: [SAMPLE_SIZE] · طريقة الجمع: [DATA_COLLECTION_MODE] · الأوزان: [WEIGHTING_APPROACH].
خطة التحليل المسبقة: [ANALYSIS_PLAN.md](01_protocol/ANALYSIS_PLAN.md).

## ٥. حالة المشروع

**[CURRENT_STATUS]** — تابع التقدم على لوحة GitHub Project. شرح الأعمدة والوسوم في
[PROJECT_BOARD.md](06_documentation/governance/PROJECT_BOARD.md).

## ٦. هيكل المستودع

| المجلد | المحتوى |
| --- | --- |
| `00_project_management/` | خطة المشروع، محاضر الاجتماعات، سجل القرارات، الأدوار |
| `01_protocol/` | البروتوكول، خطة التحليل، الاستبيان (عربي/إنجليزي)، العينة، العمل الميداني، الأخلاقيات |
| `02_data/` | توثيق مراحل البيانات + سجل النسخ `DATA_MANIFEST.csv` + قاموس البيانات — **دون ملفات البيانات نفسها** |
| `03_scripts/` | خط المعالجة المرقّم: 01 تحقق ← 02 تنظيف ← 03 إعادة ترميز ← 04 أوزان ← 05 ملف التحليل ← 06–08 تحليل ورسوم |
| `04_analysis/` | الجداول والرسوم والمخرجات الإحصائية وتقارير الجودة (مُنتَجة آليًا) |
| `05_reports/` | مسودات ← مراجَعة ← نهائية |
| `06_documentation/` | خطة إدارة البيانات، الملاحظات المنهجية، توثيق خط المعالجة، الجودة، الحوكمة |
| `07_outputs/` | مخرجات معتمدة للنشر |
| `99_archive/` | مواد مستبدلة للاطلاع فقط |

## ٧. قواعد التعامل مع البيانات

1. **لا تُرفع أي بيانات شخصية أو قابلة للتعريف إلى GitHub إطلاقًا.** البيانات الخام والمعرّفات المباشرة
   ومفتاح الربط تبقى في التخزين الآمن: **[SECURE_STORAGE_LOCATION]**.
2. مجلد البيانات الخام للقراءة فقط؛ لا يعدّله أحد يدويًا.
3. تنتقل البيانات في اتجاه واحد: خام ← منظّفة ← معالجة ← جاهزة للتحليل، وعبر السكربتات فقط.
4. كل ملف بيانات يُسجَّل في `DATA_MANIFEST.csv` مع إصداره وبصمته SHA-256.
5. كل متغير موثّق في [قاموس البيانات](02_data/data_dictionary/DATA_DICTIONARY.md).

التفاصيل: [DATA_SECURITY.md](DATA_SECURITY.md) و[خطة إدارة البيانات](06_documentation/data_management/DATA_MANAGEMENT_PLAN.md).

## ٨. طريقة المساهمة — سير العمل اليومي

</div>

```text
 1. سحب آخر التحديثات        git switch main && git pull
 2. إنشاء فرع                 git switch -c analysis/42-crosstabs-by-region
 3. تنفيذ المهمة المسندة       (المهمة = Issue رقم 42)
 4. حفظ التعديلات              git commit -m "analysis(crosstabs): add region tables (refs #42)"
 5. رفع الفرع                  git push -u origin analysis/42-crosstabs-by-region
 6. فتح طلب دمج                Pull Request + تعبئة النموذج + "Closes #42"
 7. المراجِع يفحص العمل         يُطلب أصحاب الملفات (CODEOWNERS) تلقائيًا + الفحوص الآلية
 8. التصحيحات إن لزم            commits جديدة على الفرع نفسه
 9. الموافقة                    الموافقات المطلوبة + نجاح الفحوص
10. الدمج                       Squash and merge
11. إغلاق المهمة                 تلقائيًا عبر "Closes #42"
```

<div dir="rtl">

## ٩. نظام الفروع

الفرع `main` محمي ولا يُسمح بالدفع المباشر إليه. تُنشأ فروع قصيرة العمر بالبادئات:
`data/` للبيانات، `analysis/` للتحليل، `method/` للمنهجية، `report/` للتقارير، `docs/` للتوثيق،
`fix/` للتصحيحات، `chore/` للأدوات. لا يوجد فرع `develop` عمدًا — السبب في [CONTRIBUTING.md](CONTRIBUTING.md).

## ١٠. إرسال طلب دمج (Pull Request)

طلب واحد = مهمة واحدة = تعديل منطقي واحد. عبّئ كل أقسام النموذج، خصوصًا: تغييرات البيانات،
تغييرات المنهجية، هل تغيّرت النتائج، وفحص البيانات الحساسة.

## ١١. سياسة البيانات الحساسة

إذا اشتبهت بأن بيانات حساسة أو كلمة مرور رُفعت: **توقّف فورًا** ولا تحاول إصلاحها بصمت، واتبع
إجراءات [SECURITY.md](SECURITY.md).

## ١٢. إعادة إنتاج التحليل

</div>

```bash
git clone https://github.com/[ORG_OR_USER]/[REPO_NAME].git && cd [REPO_NAME]
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp config/.env.example .env        # ثم حدّد DATA_ROOT = مسار التخزين الآمن
git checkout v1.0.0                 # الإصدار المراد إعادة إنتاجه
python tools/data_manifest.py verify
python 03_scripts/run_pipeline.py
```

<div dir="rtl">

## ١٣. الإصدارات وسجل التغييرات

نظام إصدارات دلالي مكيّف للبحث: [VERSIONING.md](06_documentation/governance/VERSIONING.md) — وسجل التغييرات في
[CHANGELOG.md](CHANGELOG.md) ويذكر كل إصدار نسخة البيانات التي استخدمها.

## ١٤. اللغة

أسماء الملفات والفروع والكود والمتغيرات بالإنجليزية؛ تسميات المتغيرات والاستبيان والتقارير بالعربية والإنجليزية.
التفاصيل في [LANGUAGE_POLICY.md](06_documentation/governance/LANGUAGE_POLICY.md).

## ١٥. التواصل

استفسارات عامة: [CONTACT_EMAIL] · طلبات الوصول للبيانات: [DATA_MANAGER] · الحوادث الأمنية: [SECURITY_CONTACT_EMAIL].

عضو جديد؟ ابدأ بـ [دليل الانضمام](06_documentation/onboarding/ONBOARDING.md).

</div>
