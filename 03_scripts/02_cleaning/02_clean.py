"""Stage 02 — CLEAN: raw -> cleaned.

Applies, in order:
  1. pseudonymisation: builds/reuses resp_id and moves direct identifiers to $DATA_ROOT/restricted/
  2. documented, reviewed rules from 03_scripts/02_cleaning/cleaning_rules.csv
Input : $DATA_ROOT/raw/<raw files>
Output: $DATA_ROOT/cleaned/<short>_cleaned_v<ver>.<ext>
        $DATA_ROOT/restricted/<short>_restricted_identifiers_v<ver>.csv   (NEVER in Git)
        04_analysis/qc_reports/02_cleaning_log_v<ver>.csv   (rule-by-rule counts)
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _lib import pipeline_utils as pu  # noqa: E402

SCRIPT = "03_scripts/02_cleaning/02_clean.py"
RULES = Path(__file__).with_name("cleaning_rules.csv")
ACTIONS = {"trim_whitespace", "set_missing", "replace", "to_numeric", "drop_record"}


def pseudonymise(cfg, df, dd, log_rows):
    id_var = cfg["data"]["id_variable"]
    source_id = cfg["data"].get("source_id_variable")
    restricted = pu.stage_dir(cfg, "restricted")
    key_path = restricted / f"{cfg['project']['short_name']}_restricted_linking_key.csv"
    if source_id:
        key = pd.read_csv(key_path, dtype=str) if key_path.exists() else pd.DataFrame(columns=[source_id, id_var])
        known = dict(zip(key[source_id], key[id_var]))
        start = len(known)
        new_ids = [s for s in df[source_id].astype(str).unique() if s not in known]
        for i, s in enumerate(sorted(new_ids), start=start + 1):
            known[s] = f"R{i:06d}"
        pd.DataFrame({source_id: list(known), id_var: list(known.values())}).to_csv(key_path, index=False)
        df[id_var] = df[source_id].astype(str).map(known)
        log_rows.append({"rule_id": "PSEUDO-01", "variable": id_var, "action": "assign_resp_id",
                         "n_affected": len(new_ids), "rationale": "pseudonymous ID; key stored in restricted area"})
    direct = [v for v in dd.loc[dd["pii"].str.lower() == "direct", "variable"] if v in df.columns]
    if source_id and source_id not in direct:
        direct.append(source_id)
    if direct:
        ident = df[[id_var] + direct]
        ident_path = restricted / pu.versioned_name(cfg, "restricted", "identifiers", "csv")
        ident.to_csv(ident_path, index=False)
        pu.register_output(cfg, ident_path, "restricted", SCRIPT, df=ident, notes="RESTRICTED - direct identifiers")
        df = df.drop(columns=direct)
        log_rows.append({"rule_id": "PSEUDO-02", "variable": "|".join(direct), "action": "remove_direct_identifiers",
                         "n_affected": len(direct), "rationale": "DATA_SECURITY.md C3 - moved to restricted storage"})
    return df


def apply_rules(df, rules, log_rows):
    for _, r in rules.iterrows():
        action, var, cond = r["action"].strip(), r["variable"].strip(), r.get("condition", "").strip()
        if action not in ACTIONS:
            raise ValueError(f"Rule {r['rule_id']}: unknown action '{action}'")
        if var != "*" and var not in df.columns:
            raise KeyError(f"Rule {r['rule_id']}: variable '{var}' not in data")
        mask = df.eval(cond, engine="python").astype(bool) if cond else pd.Series(True, index=df.index)
        n = int(mask.sum())
        if action == "drop_record":
            df = df.loc[~mask]
        elif action == "trim_whitespace":
            cols = df.select_dtypes(include=["object", "string"]).columns if var == "*" else [var]
            for c in cols:
                df.loc[mask, c] = df.loc[mask, c].astype("string").str.strip()
        elif action == "set_missing":
            df.loc[mask, var] = np.nan
        elif action == "replace":
            df.loc[mask, var] = r["value"]
        elif action == "to_numeric":
            df[var] = pd.to_numeric(df[var], errors="coerce")
        log_rows.append({"rule_id": r["rule_id"], "variable": var, "action": action, "n_affected": n,
                         "rationale": r.get("rationale", "")})
    return df


def main() -> int:
    pu.setup_logging("02-clean")
    cfg = pu.load_config()
    dd = pu.load_dictionary(cfg)
    raw_dir = pu.stage_dir(cfg, "raw")
    inputs = [raw_dir / f for f in cfg["data"]["raw_files"]]
    df = pd.concat([pu.read_data(p) for p in inputs], ignore_index=True)
    log_rows = [{"rule_id": "START", "variable": "*", "action": "records_in", "n_affected": len(df), "rationale": ""}]

    df = pseudonymise(cfg, df, dd, log_rows)
    rules = pd.read_csv(RULES, dtype=str, keep_default_na=False)
    rules = rules[(rules["active"].str.lower() == "yes") & ~rules["rule_id"].str.startswith("[")]
    df = apply_rules(df, rules, log_rows)
    log_rows.append({"rule_id": "END", "variable": "*", "action": "records_out", "n_affected": len(df), "rationale": ""})

    out = pu.stage_dir(cfg, "cleaned") / pu.versioned_name(cfg, "cleaned")
    pu.write_data(df, out)
    pu.register_output(cfg, out, "cleaned", SCRIPT, inputs=inputs, df=df)
    pu.write_qc_report(cfg, "02_cleaning_log", log_rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
