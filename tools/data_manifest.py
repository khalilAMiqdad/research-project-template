#!/usr/bin/env python3
"""Register and verify data files against 02_data/metadata/DATA_MANIFEST.csv.

  python tools/data_manifest.py verify [--stage analysis_ready]
        Recompute SHA-256 of every manifest file found under $DATA_ROOT/<stage>/ and compare.
  python tools/data_manifest.py add <file> --stage raw [--version 1.0] [--notes "..."]
        Register a file produced outside the pipeline (e.g. a raw delivery).

The manifest holds only file-level metadata (never data values), so it is safe for Git.
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "03_scripts"))
from _lib import pipeline_utils as pu  # noqa: E402


def verify(cfg: dict, stage: str | None) -> int:
    manifest = pu.REPO_ROOT / cfg["paths"]["manifest_csv"]
    with open(manifest, encoding="utf-8") as fh:
        rows = [r for r in csv.DictReader(fh) if not stage or r["stage"] == stage]
    if not rows:
        print("Manifest has no entries to verify.")
        return 0
    root = pu.data_root(cfg)
    ok = bad = missing = 0
    for r in rows:
        path = root / r["stage"] / r["file_name"]
        if not path.exists():
            print(f"  ? missing locally : {r['stage']}/{r['file_name']}")
            missing += 1
        elif pu.sha256(path) != r["sha256"]:
            print(f"  ✗ CHECKSUM DIFFERS: {r['stage']}/{r['file_name']}  (file changed after registration)")
            bad += 1
        else:
            ok += 1
    print(f"\nverified: {ok} identical, {bad} different, {missing} not available locally")
    return 1 if bad else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    v = sub.add_parser("verify")
    v.add_argument("--stage")
    a = sub.add_parser("add")
    a.add_argument("file")
    a.add_argument("--stage", required=True, choices=pu.STAGES)
    a.add_argument("--version")
    a.add_argument("--notes", default="")
    args = ap.parse_args()
    cfg = pu.load_config()
    if args.cmd == "verify":
        return verify(cfg, args.stage)
    if args.version:
        cfg["data"]["dataset_version"] = args.version
    row = pu.register_output(cfg, Path(args.file).resolve(), args.stage, "manual (tools/data_manifest.py)",
                             notes=args.notes)
    print(f"registered {row['file_name']}  sha256={row['sha256'][:12]}…")
    return 0


if __name__ == "__main__":
    sys.exit(main())
