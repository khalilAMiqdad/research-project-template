"""Stage 05 — ANALYSIS DATASET: processed (weighted) -> analysis_ready.

Keeps only variables flagged in_analysis = yes in the data dictionary (+ id + weight),
refuses to write if any direct identifier would be included, and checks the result
against the dictionary.
Output: $DATA_ROOT/analysis_ready/<short>_analysis_ready_v<ver>.<ext>
        04_analysis/qc_reports/05_analysis_dataset_qc_v<ver>.csv
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _lib import pipeline_utils as pu  # noqa: E402

SCRIPT = "03_scripts/05_analysis_dataset/05_build_analysis_dataset.py"


def main() -> int:
    pu.setup_logging("05-analysis-ds")
    cfg = pu.load_config()
    dd = pu.load_dictionary(cfg)
    src = pu.latest_stage_file(cfg, "processed", "weighted")
    df = pu.read_data(src)
    id_var = cfg["data"]["id_variable"]
    weight = cfg["analysis"]["weight_variable"]

    keep = [id_var, weight] + [v for v in dd.loc[dd["in_analysis"].str.lower() == "yes", "variable"]
                               if v not in (id_var, weight)]
    missing = [v for v in keep if v not in df.columns]
    if missing:
        raise KeyError(f"Variables flagged in_analysis=yes but absent from data: {missing}")
    direct = set(dd.loc[dd["pii"].str.lower() == "direct", "variable"])
    leaked = direct.intersection(keep)
    if leaked:
        raise RuntimeError(f"Direct identifiers must never reach analysis_ready: {sorted(leaked)}")

    out_df = df[keep]
    out = pu.stage_dir(cfg, "analysis_ready") / pu.versioned_name(cfg, "analysis_ready")
    pu.write_data(out_df, out)
    pu.register_output(cfg, out, "analysis_ready", SCRIPT, inputs=[src], df=out_df)
    pu.write_qc_report(cfg, "05_analysis_dataset_qc", [
        {"check": "n_records", "value": len(out_df)},
        {"check": "n_variables", "value": out_df.shape[1]},
        {"check": "id_unique", "value": bool(out_df[id_var].is_unique)},
        {"check": "weight_missing", "value": int(out_df[weight].isna().sum())},
        {"check": "direct_identifiers_present", "value": False},
    ])
    return 0


if __name__ == "__main__":
    sys.exit(main())
