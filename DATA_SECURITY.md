# Data Security Policy — what may enter GitHub

**GitHub is a collaboration and version-control platform for code and documentation.
It is not the project's data store.** Research data live in the secure storage
**[SECURE_STORAGE_LOCATION]**, managed by the Data Manager. GitHub holds everything
needed to *reproduce* the data processing, plus a manifest that proves which data version
was used — but not the sensitive data themselves.

## 1. Data classification

| Class | Definition | Examples | Allowed in GitHub? | Storage |
| --- | --- | --- | --- | --- |
| **C0 – Public** | Aggregated, disclosure-checked, approved for release | published tables, charts, reports | ✅ Yes (Git; LFS if large binary) | GitHub + archive |
| **C1 – Internal** | Project documents, code, metadata, no participant-level data | scripts, protocol, dictionary, manifest, aggregate QC reports | ✅ Yes | GitHub |
| **C2 – Confidential** | Participant-level data **without** direct identifiers (pseudonymised), still containing quasi-identifiers | cleaned/processed/analysis-ready microdata | ❌ **No** by default. Exception in §4 | Secure storage |
| **C3 – Restricted** | Direct identifiers or anything that links a record to a person | raw exports, names, phones, e-mails, ID numbers, addresses, exact GPS, photos/audio, signed consent forms, **ID-linking key** | ❌ **Never** | Encrypted secure storage, Data Manager only |

When in doubt, treat data as the **higher** class and ask the Data Manager.

## 2. Sensitive information (C3) — never in GitHub

- Participant names, signatures, photos, voice recordings
- Phone numbers, e-mail addresses, social-media handles
- National ID, passport, refugee/registration numbers, any official identifier
- Home or work addresses, exact GPS coordinates, household/dwelling identifiers from the frame
- Interviewer notes that mention identifiable people
- The key that maps `resp_id` to real identities
- Any combination of quasi-identifiers that makes re-identification likely
  (e.g. small locality + exact age + occupation + household size)

Also **never**: `.env`, passwords, API keys, tokens, SSH/PGP keys (`*.pem`, `*.key`, `*.p12`,
`*.pfx`, `id_rsa*`), `credentials*`, `secrets*`, survey-platform exports, database dumps.

## 3. What goes where

| Artefact | Git | Git LFS | Secure storage only |
| --- | :---: | :---: | :---: |
| Code (`.py`, `.R`, `.do`, `.sps`), notebooks **without outputs of microdata** | ✅ | | |
| Documentation (`.md`), protocol, analysis plan | ✅ | | |
| Data dictionary (`.md`, `.csv`), codebooks, `DATA_MANIFEST.csv` | ✅ | | |
| Cleaning / recoding rules (`.csv`), weighting targets (population margins) | ✅ | | |
| Aggregate tables (`.csv`) with small-cell suppression | ✅ | | |
| Questionnaire (`.docx`/`.pdf`/XLSForm `.xlsx`), final reports (`.pdf`, `.docx`) | | ✅ | |
| Figures (`.png`, `.svg`) | ✅ (`.svg`) | ✅ (`.png`, `.jpg`) | |
| Approved **de-identified** analysis dataset (see §4) | | ✅ | ✅ (master copy) |
| Raw data (any format: `.csv`, `.xlsx`, `.sav`, `.dta`, `.RData`, `.zip`) | | | ✅ |
| Cleaned / processed / analysis-ready microdata | | | ✅ |
| Audio, photos, GPS tracks, paper-scan images, consent forms | | | ✅ |
| ID-linking key, contact lists, sampling-frame with addresses | | | ✅ (restricted) |

`.gitignore` enforces this: every data format inside `02_data/` is ignored except the
README, the manifest, the metadata and the dictionary.

## 4. Exception: sharing a de-identified analysis dataset through Git LFS

Allowed **only** if all of the following are true and recorded in a Decision Record:

1. The repository is **private**, or the dataset is approved for public release.
2. Direct identifiers are removed and quasi-identifiers are generalised
   (e.g. age bands, region instead of locality), and a disclosure-risk check was done
   (e.g. k-anonymity ≥ [K_THRESHOLD] on key quasi-identifiers).
3. The Data Manager **and** Project Lead approved the PR.
4. The consent form and ethics approval allow it.
5. The file is placed in `02_data/analysis_ready/approved_deid/` (the only data folder not ignored)
   and is tracked by Git LFS.

## 5. Why not simply use Git LFS for all data?

- Git LFS **does not encrypt** data and does not change who can read them: every collaborator
  with read access can download every version, forever.
- Removing a file from LFS history is difficult and requires GitHub Support.
- LFS storage and bandwidth quotas are limited and billed.
- Access to data must follow the *need-to-know* principle, which is finer than repository access.

Git LFS is therefore used for **large non-sensitive binaries** (reports, questionnaires,
images, approved de-identified datasets), not as a data warehouse.

## 6. Recommended secure storage options

Choose one per the institution's policy and record it in the DMP:

| Option | Suitable for | Notes |
| --- | --- | --- |
| Institutional research data storage / secure file server | C2, C3 | Preferred where available; backups and access logs managed by IT |
| Institutional cloud (SharePoint/OneDrive, Google Workspace) **with** restricted sharing | C2 | Folder-level permissions; disable public links |
| Encrypted containers (VeraCrypt / Cryptomator) inside the storage | C3 | For the ID-linking key and raw exports |
| Survey platform (e.g. the platform used for collection) | C3 | Delete from platform after secure export per DMP |
| Trusted research environment / data enclave | C2, C3 | For highly sensitive studies |
| DVC or `git-annex` with a secure remote | C2 | Optional, for teams wanting data versioning linked to Git without putting data in GitHub |

## 7. Linking the data version to the code version

Every data file produced by the pipeline is registered in
[02_data/metadata/DATA_MANIFEST.csv](02_data/metadata/DATA_MANIFEST.csv) with its
`dataset_version`, row/column counts, **SHA-256 checksum**, producing script and Git commit.
Because the manifest is versioned in Git, a release tag (e.g. `v1.0.0`) fixes **exactly**
which data files — byte for byte — produced the results. `python tools/data_manifest.py verify`
confirms a local copy is identical.

## 8. Handling rules for every team member

1. Work on data only on institution-approved, encrypted devices.
2. Do not copy data to personal cloud drives, USB sticks, e-mail or messaging apps.
3. Do not paste participant-level rows into Issues, PRs, chat, AI tools or screenshots.
4. Notebooks: clear outputs that show microdata before committing (`nbstripout` recommended).
5. Refer to records only by pseudonymous `resp_id`.
6. Report any suspected exposure immediately — see [SECURITY.md](SECURITY.md).

## 9. Automated guardrails

| Guardrail | What it blocks |
| --- | --- |
| `.gitignore` | data formats in data folders, secrets, `.env`, keys |
| `pre-commit` hooks | secrets (Gitleaks), files > 5 MB, sensitive file names, PII patterns |
| CI `validation.yml` | same checks on every PR + forbidden names + folder structure |
| Branch protection + CODEOWNERS | changes to data rules merged without the Data Manager |

Guardrails reduce risk; they do not replace judgement. **You** remain responsible for what you commit.
