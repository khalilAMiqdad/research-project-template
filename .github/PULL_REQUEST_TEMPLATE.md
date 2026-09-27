<!--
Title format:  <type>(<scope>): <summary>      e.g.  data(cleaning): exclude interviews under threshold
Fill EVERY section. Write "N/A" where not applicable — do not delete sections.
NEVER paste participant-level data, names, contacts or secrets in this PR.
-->

## 1. Description / الوصف

<!-- What does this PR change? -->

Closes #<!-- issue number -->

## 2. Reason for change / سبب التعديل

<!-- Why is it needed? Link to protocol/analysis-plan section or decision record (DR-NNN). -->

## 3. Type of change

- [ ] Data processing (validation / cleaning / recoding / weighting)
- [ ] Analysis (tables, figures, models)
- [ ] Methodology (protocol, questionnaire, sampling, analysis plan)
- [ ] Report / outputs
- [ ] Documentation only
- [ ] Infrastructure (CI, tools, config)
- [ ] Correction of an error already on `main`

## 4. Files affected / الملفات المتأثرة

<!-- Main files or folders; the "Files changed" tab has the full list. -->

## 5. Data changes / هل تم تغيير البيانات؟

- [ ] No
- [ ] Yes → dataset version: from `v…` to `v…` · records before/after: … / …
  - [ ] Rules added/changed in `cleaning_rules.csv` / `recode_map.csv` with IDs: …
  - [ ] `DATA_MANIFEST.csv` updated by the pipeline and committed
  - [ ] Data dictionary (MD **and** CSV) updated

## 6. Methodology changes / هل تم تغيير المنهجية؟

- [ ] No
- [ ] Yes → protocol / analysis-plan section: … · Decision record: DR-…
  - [ ] Change made **before** seeing final results, or clearly labelled post hoc

## 7. Results changed? / هل تغيرت النتائج؟

- [ ] No outputs changed
- [ ] New outputs only (nothing previously reported changes)
- [ ] Previously reported numbers changed → list old → new values and where they were reported:

## 8. Testing & validation / الاختبار والتحقق

- [ ] I ran the affected stage(s): `python 03_scripts/run_pipeline.py --from NN`
- [ ] QC reports in `04_analysis/qc_reports/` reviewed — no unexpected counts
- [ ] Outputs are reproducible (re-run gives identical files)
- [ ] CI checks pass

## 9. Documentation updated / تحديث التوثيق

- [ ] Yes — `CHANGELOG.md` (`[Unreleased]`) and relevant docs
- [ ] Not needed (label `no-changelog`) — reason:

## 10. Review needed / المراجعة المطلوبة

- [ ] Data review (Data Manager) — label `review:data`
- [ ] Methodological review (Methodology Lead) — label `review:methodology`
- [ ] Statistical review (Analysis Lead) — label `review:statistics`
- [ ] Report review (Report Lead)
- [ ] Project Lead approval (final outputs, security, infrastructure)

## 11. Sensitive data check / فحص البيانات الحساسة  (mandatory)

- [ ] This PR contains **no** personal data, identifiers, raw or participant-level data
- [ ] This PR contains **no** passwords, tokens, keys or `.env` files
- [ ] Tables/figures respect the minimum cell size; notebooks have no microdata outputs
- [ ] ⚠️ This PR touches the handling of sensitive data (label `sensitive`) — explained above without including any such data

## 12. Reviewer notes / ملاحظات للمراجع

<!-- What should the reviewer focus on? How to reproduce? Known limitations? -->
