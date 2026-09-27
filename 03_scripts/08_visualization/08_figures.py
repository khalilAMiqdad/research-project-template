"""Stage 08 — FIGURES built from the tables of stage 06 (never directly from microdata),
so every figure matches a reviewed table exactly.
Output: 04_analysis/figures/fig_desc_<variable>.svg and .png
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
matplotlib.rcParams["svg.hashsalt"] = "[PROJECT_SHORT_NAME]"  # deterministic SVG ids
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _lib import pipeline_utils as pu  # noqa: E402


def main() -> int:
    pu.setup_logging("08-figures")
    cfg = pu.load_config()
    tables = pu.REPO_ROOT / cfg["paths"]["tables"]
    out_dir = pu.REPO_ROOT / cfg["paths"]["figures"]
    out_dir.mkdir(parents=True, exist_ok=True)

    for var in cfg["analysis"].get("figure_variables") or []:
        tab = pd.read_csv(tables / f"tab_desc_{var}.csv", keep_default_na=False)
        tab = tab[tab["suppressed"].astype(str) != "True"]
        names = [lbl or code for code, lbl in zip(tab["code"].astype(str), tab["label"].astype(str))]
        values = tab["pct_weighted"].astype(float)
        fig, ax = plt.subplots(figsize=(7, 0.5 * len(tab) + 1.5))
        ax.barh(names, values, xerr=tab["moe_pct_points"].astype(float), color="#3b6ea8", capsize=3)
        ax.invert_yaxis()
        ax.set_xlabel("Weighted % (bars show margin of error)")
        ax.set_title(var)
        ax.spines[["top", "right"]].set_visible(False)
        fig.tight_layout()
        # metadata without timestamps -> byte-identical files on re-run (reproducibility check)
        fig.savefig(out_dir / f"fig_desc_{var}.svg", metadata={"Date": None})
        fig.savefig(out_dir / f"fig_desc_{var}.png", dpi=200, metadata={"Software": None})
        plt.close(fig)
        pu.log.info("fig_desc_%s written", var)
    return 0


if __name__ == "__main__":
    sys.exit(main())
