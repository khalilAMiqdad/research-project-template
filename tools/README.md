# tools

| Script | Purpose | Used by |
| --- | --- | --- |
| `check_structure.py` | Required files/folders, allowed top-level folders, file-naming rules | CI, pre-commit |
| `check_sensitive.py` | Secret file names, microdata/media formats, files in `02_data/`, large non-LFS files, PII column headers, e-mails/phones/GPS in text | CI, pre-commit |
| `check_docs.py` | Required sections in key docs, dictionary consistency, placeholders (`--strict` for releases) | CI, release |
| `data_manifest.py` | `verify` local data against `DATA_MANIFEST.csv`; `add` a file manually | Data Manager, reproducers |
| `setup_github.sh` | One-time creation and configuration of the GitHub repository (labels, protection, project, teams) | Project Lead |

All Python tools use the standard library only (except `data_manifest.py`, which uses the pipeline requirements).
