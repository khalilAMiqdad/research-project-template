"""Stage 01 — Validate RAW data (read-only).

Input : $DATA_ROOT/raw/<files listed in config data.raw_files>
Output: 04_analysis/qc_reports/01_validation_report_v<ver>.csv   (aggregate counts only)
        manifest rows for every raw file (freezes their SHA-256)
Never modifies raw data. Exit code 1 if a CRITICAL check fails.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _lib import pipeline_utils as pu  # noqa: E402

SCRIPT = "03_scripts/01_validation/01_validate_raw.py"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--allow-errors", action="store_true", help="report critical errors but exit 0")
    args = ap.parse_args()
    pu.setup_logging("01-validate")
    cfg = pu.load_config()
    dd = pu.load_dictionary(cfg)
    raw_dir = pu.stage_dir(cfg, "raw")
    id_var = cfg["data"]["id_variable"]
    source_id = cfg["data"].get("source_id_variable")

    frames, qc = [], []
    for name in pu.require(cfg["data"]["raw_files"], "data.raw_files"):
        path = raw_dir / pu.require(name, "data.raw_files[]")
        df = pu.read_data(path)
        pu.register_output(cfg, path, "raw", SCRIPT, df=df, notes="raw input frozen at validation")
        df["_source_file"] = path.name
        frames.append(df)
    df = pd.concat(frames, ignore_index=True)
    pu.log.info("Loaded %d records, %d columns", *df.shape)

    def add(check, variable, n, severity, detail=""):
        qc.append({"check": check, "variable": variable, "n_issues": int(n),
                   "severity": severity if n else "ok", "detail": detail})

    raw_vars = dd[dd["stage_created"].str.lower() == "raw"]
    # 1. structure
    missing_vars = sorted(set(raw_vars["variable"]) - set(df.columns))
    for v in missing_vars:
        add("variable_missing_from_data", v, 1, "critical")
    extra = sorted(set(df.columns) - set(dd["variable"]) - {"_source_file"})
    for v in extra:
        add("variable_not_in_dictionary", v, 1, "warning", "document it in the data dictionary")

    # 2. identifier
    key = source_id or id_var
    if key in df.columns:
        add("id_missing", key, df[key].isna().sum(), "critical")
        add("id_duplicated", key, df[key].duplicated(keep=False).sum(), "critical")
    else:
        add("id_variable_absent", key, 1, "critical")
    add("duplicate_records_all_columns", "*", df.drop(columns="_source_file").duplicated().sum(), "warning")

    # 3. values per variable
    for _, spec in raw_vars.iterrows():
        v = spec["variable"]
        if v not in df.columns:
            continue
        col = df[v]
        missing_codes = pu.parse_list(spec.get("missing_codes", ""))
        add("missing_or_blank", v, (col.isna() | (col.astype(str).str.strip() == "")).sum(), "info")
        present = col.dropna().astype(str).str.strip()
        present = present[(present != "") & (~present.isin(missing_codes))]
        codes = pu.parse_codes(spec.get("values", ""))
        if spec["type"].lower() in ("categorical", "ordinal", "binary") and codes:
            add("invalid_code", v, (~present.isin(codes.keys())).sum(), "error",
                f"allowed: {'|'.join(codes)}")
        if spec["type"].lower() in ("numeric", "integer", "continuous"):
            num = pd.to_numeric(present, errors="coerce")
            add("non_numeric_value", v, num.isna().sum(), "error")
            lo, hi = spec.get("valid_min", ""), spec.get("valid_max", "")
            if lo != "":
                add("below_valid_min", v, (num < float(lo)).sum(), "error", f"min={lo}")
            if hi != "":
                add("above_valid_max", v, (num > float(hi)).sum(), "error", f"max={hi}")

    report = pu.write_qc_report(cfg, "01_validation_report", qc)
    critical = [r for r in qc if r["severity"] == "critical"]
    errors = [r for r in qc if r["severity"] == "error"]
    pu.log.info("Validation finished: %d critical, %d error checks with issues -> %s",
                len(critical), len(errors), report.name)
    if critical and not args.allow_errors:
        pu.log.error("CRITICAL validation failures — fix with the Data Manager before cleaning.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
