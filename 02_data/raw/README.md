# raw — original data (C3, read-only)

- **Location:** `$DATA_ROOT/raw/` in secure storage. Nothing from this stage is committed.
- **Who writes:** only the Data Manager, who places each export exactly as received.
- **File name:** `<short>_raw_<source>_<YYYYMMDD>.<ext>` — e.g. `[PROJECT_SHORT_NAME]_raw_platform_20260115.csv`.
- **Never edited.** Set the folder/file to read-only after upload. Corrections happen in stage 02 via rules.
- **Registered** in `02_data/metadata/DATA_MANIFEST.csv` (SHA-256) when stage 01 runs — this
  freezes the raw version; any later change to a raw file is detectable.
- A new delivery (e.g. a late batch) is a **new file** with a new date, never an overwrite.

Receipt log (fill for each delivery — no personal data):

| Date received | File name | Source | Records | Received by | Manifest updated (PR) |
| --- | --- | --- | --- | --- | --- |
| [YYYY-MM-DD] | [file] | [platform / partner] | [n] | [DATA_MANAGER] | #[PR] |
