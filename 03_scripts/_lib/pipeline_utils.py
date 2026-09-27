"""Shared helpers for the [PROJECT_NAME] pipeline.

Every stage script imports this module to:
  * load the configuration (config/project.yml) and the data dictionary;
  * resolve paths inside the SECURE data storage ($DATA_ROOT) — never inside the repo;
  * read / write data files in csv, xlsx, sav, dta or parquet;
  * register every output in 02_data/metadata/DATA_MANIFEST.csv (version + SHA-256);
  * write aggregate QC reports (never row-level data) into the repository.
"""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import logging
import os
import subprocess
import sys
from pathlib import Path

import pandas as pd
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = REPO_ROOT / "config" / "project.yml"
STAGES = ("raw", "cleaned", "processed", "analysis_ready", "restricted")
MANIFEST_FIELDS = [
    "file_name", "stage", "dataset_version", "sha256", "n_rows", "n_cols",
    "storage_location", "produced_by_script", "input_files", "git_commit",
    "created_utc", "notes",
]

log = logging.getLogger("pipeline")


class ConfigError(RuntimeError):
    """Raised when a REQUIRED configuration value is missing."""


# --------------------------------------------------------------------------- config
def load_config() -> dict:
    with open(CONFIG_PATH, encoding="utf-8") as fh:
        cfg = yaml.safe_load(fh)
    _load_dotenv()
    return cfg


def _load_dotenv() -> None:
    env_file = REPO_ROOT / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def require(value, name: str):
    """Stop the pipeline if a REQUIRED setting has not been decided yet."""
    if value is None or value == "" or (isinstance(value, str) and value.startswith("[")):
        raise ConfigError(
            f"Configuration value '{name}' is REQUIRED but not set in config/project.yml. "
            "Set it according to the Research Protocol / Analysis Plan."
        )
    return value


# --------------------------------------------------------------------------- paths
def data_root(cfg: dict) -> Path:
    var = cfg["data"]["root_env_var"]
    root = os.environ.get(var)
    if not root:
        raise ConfigError(f"Environment variable {var} is not set (see config/.env.example).")
    root_path = Path(root).expanduser().resolve()
    if REPO_ROOT in root_path.parents or root_path == REPO_ROOT:
        raise ConfigError(f"{var} points inside the repository. Data must live in secure storage.")
    if not root_path.is_dir():
        raise ConfigError(f"{var}={root_path} does not exist or is not a directory.")
    return root_path


def stage_dir(cfg: dict, stage: str) -> Path:
    if stage not in STAGES:
        raise ValueError(f"Unknown stage '{stage}'. Expected one of {STAGES}.")
    path = data_root(cfg) / stage
    path.mkdir(parents=True, exist_ok=True)
    return path


def versioned_name(cfg: dict, stage: str, description: str | None = None, ext: str | None = None) -> str:
    """<short_name>_<stage>[_<description>]_v<dataset_version>.<ext>  (see NAMING_CONVENTIONS.md)."""
    short = require(cfg["project"]["short_name"], "project.short_name")
    ext = ext or cfg["data"].get("output_format", "csv")
    parts = [short, stage] + ([description] if description else [])
    return f"{'_'.join(parts)}_v{cfg['data']['dataset_version']}.{ext}"


# --------------------------------------------------------------------------- IO
def read_data(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(path, dtype=str, keep_default_na=False, na_values=[""], encoding="utf-8-sig")
    if suffix in (".xlsx", ".xls"):
        return pd.read_excel(path, dtype=str)
    if suffix == ".parquet":
        return pd.read_parquet(path)
    if suffix in (".sav", ".dta"):
        import pyreadstat
        reader = pyreadstat.read_sav if suffix == ".sav" else pyreadstat.read_dta
        df, _meta = reader(str(path))
        return df
    raise ValueError(f"Unsupported file type: {path}")


def write_data(df: pd.DataFrame, path: Path) -> Path:
    suffix = path.suffix.lower()
    path.parent.mkdir(parents=True, exist_ok=True)
    if suffix == ".csv":
        df.to_csv(path, index=False, encoding="utf-8")
    elif suffix == ".parquet":
        df.to_parquet(path, index=False)
    elif suffix in (".sav", ".dta"):
        import pyreadstat
        (pyreadstat.write_sav if suffix == ".sav" else pyreadstat.write_dta)(df, str(path))
    else:
        raise ValueError(f"Unsupported output type: {path}")
    return path


# --------------------------------------------------------------------------- dictionary
def load_dictionary(cfg: dict) -> pd.DataFrame:
    path = REPO_ROOT / cfg["paths"]["dictionary_csv"]
    dd = pd.read_csv(path, dtype=str, keep_default_na=False)
    dd = dd[~dd["variable"].str.startswith("[")]          # skip template placeholder rows
    return dd


def parse_codes(spec: str) -> dict[str, str]:
    """'1=Male|2=Female' -> {'1': 'Male', '2': 'Female'}."""
    out: dict[str, str] = {}
    for item in filter(None, (s.strip() for s in (spec or "").split("|"))):
        code, _, label = item.partition("=")
        out[code.strip()] = label.strip()
    return out


def parse_list(spec: str) -> list[str]:
    return [s.strip() for s in (spec or "").split("|") if s.strip()]


# --------------------------------------------------------------------------- manifest
def sha256(path: Path, chunk: int = 1 << 20) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(chunk), b""):
            digest.update(block)
    return digest.hexdigest()


def git_commit() -> str:
    try:
        sha = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=REPO_ROOT, text=True).strip()
        dirty = subprocess.call(["git", "diff", "--quiet"], cwd=REPO_ROOT) != 0
        return sha + ("-dirty" if dirty else "")
    except Exception:  # noqa: BLE001 - git not available
        return "unknown"


def register_output(cfg: dict, path: Path, stage: str, script: str, inputs: list[Path] | None = None,
                    df: pd.DataFrame | None = None, notes: str = "") -> dict:
    """Add or replace the manifest row for *path* (keyed on file name)."""
    manifest = REPO_ROOT / cfg["paths"]["manifest_csv"]
    rows = []
    if manifest.exists():
        with open(manifest, encoding="utf-8", newline="") as fh:
            rows = [r for r in csv.DictReader(fh) if r.get("file_name") != path.name]
    row = {
        "file_name": path.name,
        "stage": stage,
        "dataset_version": cfg["data"]["dataset_version"],
        "sha256": sha256(path),
        "n_rows": "" if df is None else len(df),
        "n_cols": "" if df is None else df.shape[1],
        "storage_location": f"$DATA_ROOT/{stage}/",
        "produced_by_script": script,
        "input_files": ";".join(p.name for p in (inputs or [])),
        "git_commit": git_commit(),
        "created_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "notes": notes,
    }
    rows.append(row)
    with open(manifest, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=MANIFEST_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    log.info("Registered %s (%s rows) in manifest", path.name, row["n_rows"])
    return row


# --------------------------------------------------------------------------- QC reports
def write_qc_report(cfg: dict, name: str, records: list[dict]) -> Path:
    """Write an AGGREGATE QC report (counts only — never respondent-level values)."""
    out = REPO_ROOT / cfg["paths"]["qc_reports"] / f"{name}_v{cfg['data']['dataset_version']}.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(records).to_csv(out, index=False, encoding="utf-8")
    log.info("QC report written: %s", out.relative_to(REPO_ROOT))
    return out


def setup_logging(stage_name: str) -> None:
    logging.basicConfig(
        level=logging.INFO,
        format=f"%(asctime)s [{stage_name}] %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
        stream=sys.stdout,
    )


def latest_stage_file(cfg: dict, stage: str, description: str | None = None) -> Path:
    """Return the file for the current dataset_version of a stage (explicit, not 'latest' by date)."""
    path = stage_dir(cfg, stage) / versioned_name(cfg, stage, description)
    if not path.exists():
        raise FileNotFoundError(f"Expected input {path} not found — run the previous stage first.")
    return path
