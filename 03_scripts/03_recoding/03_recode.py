"""Stage 03 — RECODE & DERIVE: cleaned -> processed (recoded).

  1. value recodes from 03_scripts/03_recoding/recode_map.csv (reviewed via PR)
  2. derived variables in derive_variables() below (each documented in the data dictionary)
Input : $DATA_ROOT/cleaned/<short>_cleaned_v<ver>.<ext>
Output: $DATA_ROOT/processed/<short>_processed_recoded_v<ver>.<ext>
        04_analysis/qc_reports/03_recode_log_v<ver>.csv
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _lib import pipeline_utils as pu  # noqa: E402

SCRIPT = "03_scripts/03_recoding/03_recode.py"
RECODE_MAP = Path(__file__).with_name("recode_map.csv")


def derive_variables(df: pd.DataFrame, log_rows: list) -> pd.DataFrame:
    """Create derived variables. Each one MUST be added to the data dictionary
    (stage_created = processed) and justified in ANALYSIS_PLAN.md.

    Example (disabled — thresholds must come from the Analysis Plan, not from this template):
        bins = [...]; labels = [...]
        df["age_group"] = pd.cut(pd.to_numeric(df["age"], errors="coerce"), bins=bins, labels=labels, right=False)
        log_rows.append({"rule_id": "DRV-001", "variable": "age_group", "action": "derive", "n_affected": df["age_group"].notna().sum()})
    """
    return df


def main() -> int:
    pu.setup_logging("03-recode")
    cfg = pu.load_config()
    src = pu.latest_stage_file(cfg, "cleaned")
    df = pu.read_data(src)
    log_rows = []

    rmap = pd.read_csv(RECODE_MAP, dtype=str, keep_default_na=False)
    rmap = rmap[(rmap["active"].str.lower() == "yes") & ~rmap["rule_id"].str.startswith("[")]
    for (rule_id, var, new_var), grp in rmap.groupby(["rule_id", "variable", "new_variable"], sort=False):
        if var not in df.columns:
            raise KeyError(f"Recode {rule_id}: variable '{var}' not found")
        target = new_var or var
        mapping = dict(zip(grp["from_value"], grp["to_value"]))
        original = df[var].astype("string")
        df[target] = original.map(lambda x: mapping.get(x, x) if pd.notna(x) else x)
        log_rows.append({"rule_id": rule_id, "variable": f"{var}->{target}", "action": "recode",
                         "n_affected": int((original != df[target].astype("string")).fillna(False).sum())})

    df = derive_variables(df, log_rows)
    out = pu.stage_dir(cfg, "processed") / pu.versioned_name(cfg, "processed", "recoded")
    pu.write_data(df, out)
    pu.register_output(cfg, out, "processed", SCRIPT, inputs=[src], df=df)
    pu.write_qc_report(cfg, "03_recode_log", log_rows or [{"rule_id": "-", "variable": "-", "action": "no active recodes", "n_affected": 0}])
    return 0


if __name__ == "__main__":
    sys.exit(main())
