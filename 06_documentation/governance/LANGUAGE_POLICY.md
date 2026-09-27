# Language Policy (Arabic / English)

| Element | Language | Why |
| --- | --- | --- |
| File and folder names | **English**, ASCII only | Portability across OS/tools; no encoding errors in Git, SPSS, Stata |
| Branch names, tags, commit messages | **English** | Tooling, searchability, international reviewers |
| Code, comments, function names | **English** | Standard practice; libraries and help are in English |
| Variable names | **English** `snake_case` | SPSS/Stata/R/Python compatibility |
| Variable / value **labels** | **Both**: `label_en` (official) + `label_ar` | Arabic outputs without re-coding |
| Governance docs (README, CONTRIBUTING, SECURITY, DMP, protocol, analysis plan) | **English** (official) + Arabic summary where useful ([README.ar.md](../../README.ar.md)) | International team, funders, reviewers |
| Questionnaire | **Both**, same version number | Field language + reference language |
| Fieldwork manual & training | Language of the field team (Arabic), with English summary | Usability in the field |
| Issues and PR discussions | English by default; Arabic allowed if everyone involved reads it | Traceability for all members |
| Reports | As required by the deliverable: `…_report_ar_vX.Y.Z.pdf`, `…_report_en_vX.Y.Z.pdf` | — |

Technical notes for Arabic:

- All text files are **UTF-8** (`.editorconfig`). CSV files for Excel users: export with
  UTF-8 BOM (`encoding="utf-8-sig"`) so Arabic displays correctly; the pipeline reads both.
- In Markdown, wrap Arabic sections in `<div dir="rtl"> … </div>` for correct direction.
- In figures, use a font that supports Arabic shaping (e.g. Noto Naskh Arabic) and, in Python,
  `arabic-reshaper` + `python-bidi` for labels.
- SPSS: set Unicode mode (`SET UNICODE=ON`) before reading/writing `.sav` with Arabic labels.
