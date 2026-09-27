"""Stage 06 — DESCRIPTIVE ANALYSIS on analysis_ready data.

For each variable in config analysis.descriptive_variables: unweighted n, weighted %,
margin of error and small-cell suppression (ANALYSIS_PLAN.md §5, §9, §12).
Output: 04_analysis/tables/tab_desc_<variable>.csv
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _lib import pipeline_utils as pu  # noqa: E402
from _lib.stats_utils import weighted_frequency  # noqa: E402


def main() -> int:
    pu.setup_logging("06-descriptives")
    cfg = pu.load_config()
    ac = cfg["analysis"]
    cl = float(pu.require(ac.get("confidence_level"), "analysis.confidence_level"))
    deff = float(pu.require(ac.get("design_effect"), "analysis.design_effect"))
    min_cell = int(pu.require(ac.get("min_cell_size"), "analysis.min_cell_size"))
    dd = pu.load_dictionary(cfg).set_index("variable")
    df = pu.read_data(pu.latest_stage_file(cfg, "analysis_ready"))
    out_dir = pu.REPO_ROOT / cfg["paths"]["tables"]
    out_dir.mkdir(parents=True, exist_ok=True)

    for var in ac.get("descriptive_variables") or []:
        spec = dd.loc[var] if var in dd.index else None
        labels = pu.parse_codes(spec["values"]) if spec is not None else {}
        missing = pu.parse_list(spec["missing_codes"]) if spec is not None else []
        tab = weighted_frequency(df, var, ac["weight_variable"], labels, cl, deff, min_cell, missing)
        path = out_dir / f"tab_desc_{var}.csv"
        tab.to_csv(path, index=False, encoding="utf-8")
        pu.log.info("%s (base n=%s)", path.name, tab.attrs.get("base_n"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
