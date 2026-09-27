"""Stage 04 — WEIGHTING: processed (recoded) -> processed (weighted).

Method is a methodological decision (config weighting.method, ANALYSIS_PLAN.md §8):
  none    weight_final = 1
  design  weight_final = 1 / inclusion probability (or an existing base weight)
  raking  iterative proportional fitting of the base weight to population margins in
          weighting_targets.csv (variable, category, target_proportion, source)
Optional trimming (weighting.trim_min / trim_max) followed by re-normalisation.
Output: $DATA_ROOT/processed/<short>_processed_weighted_v<ver>.<ext>
        04_analysis/qc_reports/04_weighting_qc_v<ver>.csv
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _lib import pipeline_utils as pu  # noqa: E402
from _lib.stats_utils import kish_deff_weighting  # noqa: E402

SCRIPT = "03_scripts/04_weighting/04_weight.py"


def rake(df, base, targets, variables, max_iter, tol):
    for var in variables:
        t = targets[targets["variable"] == var]
        if t.empty:
            raise ValueError(f"Raking: no targets for '{var}' in weighting_targets.csv")
        total_p = t["target_proportion"].astype(float).sum()
        if abs(total_p - 1) > 1e-3:
            raise ValueError(f"Raking: targets for '{var}' sum to {total_p:.4f}, expected 1")
        uncovered = set(df[var].dropna().astype(str)) - set(t["category"].astype(str))
        if uncovered:
            raise ValueError(f"Raking: categories of '{var}' without target: {sorted(uncovered)}")
    w = base.astype(float).copy()
    for it in range(1, max_iter + 1):
        max_change = 0.0
        for var in variables:
            t = targets[targets["variable"] == var]
            total = w.sum()
            for _, row in t.iterrows():
                mask = df[var].astype(str) == str(row["category"])
                current = w[mask].sum()
                if current == 0:
                    raise ValueError(f"Raking: no respondents in {var}={row['category']}")
                factor = float(row["target_proportion"]) * total / current
                w[mask] *= factor
                max_change = max(max_change, abs(factor - 1))
        if max_change < tol:
            pu.log.info("Raking converged after %d iterations", it)
            return w
    raise RuntimeError(f"Raking did not converge in {max_iter} iterations (max change {max_change:.2e})")


def main() -> int:
    pu.setup_logging("04-weight")
    cfg = pu.load_config()
    wc = cfg["weighting"]
    src = pu.latest_stage_file(cfg, "processed", "recoded")
    df = pu.read_data(src)
    method = pu.require(wc.get("method"), "weighting.method")

    if method == "none":
        w = pd.Series(1.0, index=df.index)
    elif method in ("design", "raking"):
        if wc.get("base_weight_variable"):
            w = pd.to_numeric(df[wc["base_weight_variable"]], errors="raise")
        elif wc.get("inclusion_probability_variable"):
            w = 1.0 / pd.to_numeric(df[wc["inclusion_probability_variable"]], errors="raise")
        elif method == "raking":
            w = pd.Series(1.0, index=df.index)
        else:
            raise pu.ConfigError("weighting.method=design needs base_weight_variable or inclusion_probability_variable")
        if method == "raking":
            targets = pd.read_csv(pu.REPO_ROOT / wc["targets_file"], dtype=str, keep_default_na=False)
            targets = targets[~targets["variable"].str.startswith("[")]
            variables = pu.require(wc.get("raking_variables") or None, "weighting.raking_variables")
            w = rake(df, w, targets, variables, int(wc["max_iterations"]), float(wc["tolerance"]))
    else:
        raise pu.ConfigError(f"Unknown weighting.method '{method}'")

    if wc.get("trim_min") is not None or wc.get("trim_max") is not None:
        scaled = w / w.mean()
        scaled = scaled.clip(lower=wc.get("trim_min"), upper=wc.get("trim_max"))
        w = scaled * (w.sum() / scaled.sum())

    df["weight_final"] = (w * len(df) / w.sum()).round(6)   # normalised to sample size
    out = pu.stage_dir(cfg, "processed") / pu.versioned_name(cfg, "processed", "weighted")
    pu.write_data(df, out)
    pu.register_output(cfg, out, "processed", SCRIPT, inputs=[src], df=df, notes=f"weighting method: {method}")
    wf = df["weight_final"]
    pu.write_qc_report(cfg, "04_weighting_qc", [
        {"statistic": "method", "value": method},
        {"statistic": "n", "value": len(wf)},
        {"statistic": "sum_weights", "value": round(wf.sum(), 3)},
        {"statistic": "min_weight", "value": round(wf.min(), 4)},
        {"statistic": "max_weight", "value": round(wf.max(), 4)},
        {"statistic": "ratio_max_min", "value": round(wf.max() / wf.min(), 3) if wf.min() > 0 else np.nan},
        {"statistic": "kish_deff_weighting", "value": round(kish_deff_weighting(wf), 3)},
        {"statistic": "effective_sample_size", "value": round(len(wf) / kish_deff_weighting(wf), 1)},
    ])
    return 0


if __name__ == "__main__":
    sys.exit(main())
