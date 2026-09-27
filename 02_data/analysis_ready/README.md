# analysis_ready — final analysis file (C2)

- **Location:** `$DATA_ROOT/analysis_ready/`. Not committed (except `approved_deid/`, see below).
- **Produced by:** `03_scripts/05_analysis_dataset/05_build_analysis_dataset.py`.
- **Contains:** `resp_id`, `weight_final` and variables with `in_analysis = yes` in the dictionary.
  The script refuses to run if a direct identifier would be included.
- **This is the only input** for stages 06–08 and for any ad-hoc analysis.
- **File name:** `<short>_analysis_ready_v<MAJOR.MINOR>.<ext>`.

## approved_deid/

The only data folder tracked by Git (via Git LFS). A file may be added only under the
conditions of `DATA_SECURITY.md` §4 and with a Decision Record reference in the PR.
