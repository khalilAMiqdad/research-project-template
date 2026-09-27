#!/usr/bin/env python3
"""Documentation completeness check.

  python tools/check_docs.py            # CI on every PR: structure of key docs; placeholders = warnings
  python tools/check_docs.py --strict   # releases: unfilled [PLACEHOLDERS] in core docs = errors

Standard library only.
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLACEHOLDER = re.compile(r"\[(?:[A-Z][A-Z0-9_]{2,})\]")

# file -> headings (substrings) that must be present
REQUIRED_SECTIONS = {
    "README.md": ["Project description", "Research objectives", "Research team", "Methodology",
                  "Repository structure", "Data handling rules", "Reproducing the analysis", "Contact"],
    "CONTRIBUTING.md": ["Branching strategy", "Daily workflow", "Commit messages", "Pull Requests"],
    "SECURITY.md": ["Reporting", "Incident response procedure"],
    "DATA_SECURITY.md": ["Data classification", "What goes where"],
    "01_protocol/RESEARCH_PROTOCOL.md": ["Objectives", "Research questions", "Sampling design", "Sample size",
                                         "Ethical considerations", "Methodological limitations"],
    "01_protocol/ANALYSIS_PLAN.md": ["Indicators", "Statistical tests", "Weighting", "Missing data",
                                     "Exclusion rules", "Interpretation"],
    "06_documentation/data_management/DATA_MANAGEMENT_PLAN.md": ["Storage", "Backup", "Access", "Retention"],
    "02_data/data_dictionary/DATA_DICTIONARY.md": ["| Variable | Label | Type | Values | Missing | Source | Notes |"],
    "CHANGELOG.md": ["## [Unreleased]"],
}
# docs that must be free of placeholders at release time (--strict)
STRICT_FILES = ["README.md", "01_protocol/RESEARCH_PROTOCOL.md", "01_protocol/ANALYSIS_PLAN.md",
                "06_documentation/data_management/DATA_MANAGEMENT_PLAN.md",
                "02_data/data_dictionary/DATA_DICTIONARY.md", "CITATION.cff"]
DICT_COLUMNS = ["variable", "label_en", "label_ar", "type", "values", "valid_min", "valid_max",
                "missing_codes", "source", "stage_created", "pii", "in_analysis", "notes"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()
    errors, warnings = [], []

    for rel, sections in REQUIRED_SECTIONS.items():
        path = ROOT / rel
        if not path.exists():
            errors.append(f"{rel}: missing")
            continue
        text = path.read_text(encoding="utf-8")
        for s in sections:
            if s.lower() not in text.lower():
                errors.append(f"{rel}: required section/heading not found: '{s}'")

    # Data dictionary CSV structure and consistency with the Markdown version
    dict_csv = ROOT / "02_data/data_dictionary/data_dictionary.csv"
    if dict_csv.exists():
        with open(dict_csv, encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            if reader.fieldnames != DICT_COLUMNS:
                errors.append(f"data_dictionary.csv: columns must be exactly {DICT_COLUMNS}")
            rows = [r for r in reader if not r["variable"].startswith("[")]
        md = (ROOT / "02_data/data_dictionary/DATA_DICTIONARY.md").read_text(encoding="utf-8")
        for r in rows:
            if f"`{r['variable']}`" not in md:
                errors.append(f"variable '{r['variable']}' is in data_dictionary.csv but not in DATA_DICTIONARY.md")
            if r["pii"] not in ("none", "quasi", "direct"):
                errors.append(f"data_dictionary.csv: '{r['variable']}' has invalid pii value '{r['pii']}'")
            if r["pii"] == "direct" and r["in_analysis"] == "yes":
                errors.append(f"data_dictionary.csv: direct identifier '{r['variable']}' flagged in_analysis=yes")

    # Every numbered folder and every sub-folder of 02_data documented
    for d in sorted(ROOT.glob("[0-9][0-9]_*")):
        if d.is_dir() and not (d / "README.md").exists():
            errors.append(f"{d.name}/README.md missing")

    # Placeholders
    for rel in STRICT_FILES:
        path = ROOT / rel
        if path.exists():
            found = sorted(set(PLACEHOLDER.findall(path.read_text(encoding="utf-8"))))
            if found:
                msg = f"{rel}: {len(found)} unfilled placeholder(s), e.g. {', '.join(found[:5])}"
                (errors if args.strict else warnings).append(msg)

    for w in warnings:
        print(f"  ! {w}")
    if errors:
        print("✗ Documentation check failed:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"✓ Documentation check passed ({len(warnings)} warning(s)){' [strict]' if args.strict else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
