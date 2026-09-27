"""Stage 07 — COMPARATIVE ANALYSIS: weighted cross-tabulations (row %).

Pairs come from config analysis.crosstabs. Significance tests are specified in
ANALYSIS_PLAN.md §6; design-based tests (e.g. Rao-Scott) should be run with R `survey`
or Stata `svy:` and saved to 04_analysis/statistical_outputs/.
Output: 04_analysis/tables/tab_xtab_<row>_by_<col>.csv
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _lib import pipeline_utils as pu  # noqa: E402
from _lib.stats_utils import weighted_crosstab  # noqa: E402


def main() -> int:
    pu.setup_logging("07-crosstabs")
    cfg = pu.load_config()
    ac = cfg["analysis"]
    cl = float(pu.require(ac.get("confidence_level"), "analysis.confidence_level"))
    deff = float(pu.require(ac.get("design_effect"), "analysis.design_effect"))
    min_cell = int(pu.require(ac.get("min_cell_size"), "analysis.min_cell_size"))
    dd = pu.load_dictionary(cfg).set_index("variable")
    df = pu.read_data(pu.latest_stage_file(cfg, "analysis_ready"))
    out_dir = pu.REPO_ROOT / cfg["paths"]["tables"]
    out_dir.mkdir(parents=True, exist_ok=True)

    for row, col in ac.get("crosstabs") or []:
        miss = {v: pu.parse_list(dd.loc[v, "missing_codes"]) if v in dd.index else [] for v in (row, col)}
        tab = weighted_crosstab(df, row, col, ac["weight_variable"], cl, deff, min_cell, miss)
        path = out_dir / f"tab_xtab_{row}_by_{col}.csv"
        tab.to_csv(path, index=False, encoding="utf-8")
        pu.log.info("%s written", path.name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
