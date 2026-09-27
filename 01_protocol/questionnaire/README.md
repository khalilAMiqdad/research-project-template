# questionnaire

```text
questionnaire/
├── en/          questionnaire_en_v<MAJOR.MINOR>.docx|pdf   (reference language for variable names)
├── ar/          questionnaire_ar_v<MAJOR.MINOR>.docx|pdf
└── versions/    xlsform_v<MAJOR.MINOR>.xlsx (if CAPI/CAWI) + translation/back-translation records
```

Rules:

1. The **same version number** is used for all language versions and the XLSForm.
   `v1.0` = version used in the field. Pilot versions are `v0.x`.
2. Every item has a stable ID (`Q01`, `Q02a` …) that is used as `source` in the data dictionary.
3. Changes after `v1.0` require a Decision Record and are listed below.
4. Binary files (`.docx`, `.pdf`, `.xlsx`) are tracked with Git LFS automatically.
5. Arabic text inside files is fine; **file names are English/ASCII**.

| Version | Date | Change | Decision record | Used in field? |
| --- | --- | --- | --- | --- |
| v0.1 | [YYYY-MM-DD] | First draft | — | no |
