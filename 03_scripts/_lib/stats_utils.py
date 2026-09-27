"""Weighted descriptive statistics with margins of error and small-cell suppression.

Design-based inference (variance estimation with strata/clusters, Rao-Scott tests) is
out of scope for these helpers: when the Analysis Plan requires it, use R `survey` /
`srvyr`, Stata `svy:` or Python `samplics`, and document it in the Analysis Plan.
"""
from __future__ import annotations

import math
from statistics import NormalDist

import pandas as pd


def z_value(confidence_level: float) -> float:
    return NormalDist().inv_cdf((1 + float(confidence_level)) / 2)


def moe_proportion(p: float, n: int, confidence_level: float, design_effect: float) -> float:
    """Margin of error (percentage points) for a proportion p in [0,1] with base n.

    MOE = z * sqrt(deff * p * (1 - p) / n)  — approximate; see ANALYSIS_PLAN.md §8–9.
    """
    if n <= 0:
        return float("nan")
    return 100 * z_value(confidence_level) * math.sqrt(float(design_effect) * p * (1 - p) / n)


def weighted_frequency(df: pd.DataFrame, var: str, weight: str | None, labels: dict[str, str] | None = None,
                       confidence_level: float = 0.95, design_effect: float = 1.0,
                       min_cell_size: int = 0, missing_codes: list[str] | None = None) -> pd.DataFrame:
    data = df[[var] + ([weight] if weight else [])].copy()
    data = data[data[var].notna() & (data[var].astype(str) != "")]
    if missing_codes:
        data = data[~data[var].astype(str).isin(missing_codes)]
    w = data[weight].astype(float) if weight else pd.Series(1.0, index=data.index)
    base_n = len(data)
    total_w = w.sum()
    rows = []
    for code, grp in data.groupby(data[var].astype(str), sort=True):
        n = len(grp)
        p = w.loc[grp.index].sum() / total_w if total_w else float("nan")
        suppressed = n < min_cell_size
        rows.append({
            "variable": var,
            "code": code,
            "label": (labels or {}).get(code, ""),
            "n_unweighted": n,
            "pct_weighted": None if suppressed else round(100 * p, 1),
            "moe_pct_points": None if suppressed else round(moe_proportion(p, base_n, confidence_level, design_effect), 1),
            "suppressed": suppressed,
        })
    out = pd.DataFrame(rows)
    out.attrs["base_n"] = base_n
    return out


def weighted_crosstab(df: pd.DataFrame, row: str, col: str, weight: str | None,
                      confidence_level: float = 0.95, design_effect: float = 1.0,
                      min_cell_size: int = 0, missing_codes: dict[str, list[str]] | None = None) -> pd.DataFrame:
    """Row percentages of *col* within each category of *row*."""
    data = df[[row, col] + ([weight] if weight else [])].copy()
    for v in (row, col):
        data = data[data[v].notna() & (data[v].astype(str) != "")]
        if missing_codes and missing_codes.get(v):
            data = data[~data[v].astype(str).isin(missing_codes[v])]
    data["_w"] = data[weight].astype(float) if weight else 1.0
    rows = []
    for r_code, r_grp in data.groupby(data[row].astype(str), sort=True):
        base_n, base_w = len(r_grp), r_grp["_w"].sum()
        for c_code, cell in r_grp.groupby(r_grp[col].astype(str), sort=True):
            n = len(cell)
            p = cell["_w"].sum() / base_w if base_w else float("nan")
            suppressed = n < min_cell_size or base_n < min_cell_size
            rows.append({
                "row_variable": row, "row_code": r_code,
                "col_variable": col, "col_code": c_code,
                "n_unweighted": n, "row_base_n": base_n,
                "row_pct_weighted": None if suppressed else round(100 * p, 1),
                "moe_pct_points": None if suppressed else round(moe_proportion(p, base_n, confidence_level, design_effect), 1),
                "suppressed": suppressed,
            })
    return pd.DataFrame(rows)


def kish_deff_weighting(weights: pd.Series) -> float:
    """Design effect due to unequal weighting: n * sum(w^2) / (sum w)^2."""
    w = weights.astype(float)
    return float(len(w) * (w ** 2).sum() / (w.sum() ** 2)) if len(w) else float("nan")
