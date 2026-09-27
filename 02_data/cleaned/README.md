# cleaned — pseudonymised and corrected data (C2)

- **Location:** `$DATA_ROOT/cleaned/`. Not committed.
- **Produced by:** `03_scripts/02_cleaning/02_clean.py` only.
- **Contains:** all raw variables **minus direct identifiers**, plus `resp_id`, after the active
  rules in `03_scripts/02_cleaning/cleaning_rules.csv` (whitespace, invalid codes → missing,
  documented corrections, exclusion of invalid records).
- **File name:** `<short>_cleaned_v<MAJOR.MINOR>.<ext>`.
- **Audit:** `04_analysis/qc_reports/02_cleaning_log_v*.csv` gives the count affected by each rule.
