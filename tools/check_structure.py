#!/usr/bin/env python3
"""Check repository structure and file-naming conventions.

  python tools/check_structure.py                  # full check (CI)
  python tools/check_structure.py --names-only --files a b c   # naming only (pre-commit)

Exit code 1 on any error. Standard library only.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md", "README.ar.md", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "SECURITY.md",
    "DATA_SECURITY.md", "CHANGELOG.md", "LICENSE", "CITATION.cff",
    ".gitignore", ".gitattributes", ".editorconfig",
    ".github/CODEOWNERS", ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/workflows/validation.yml", ".github/workflows/documentation-check.yml",
    "config/project.yml", "config/.env.example", "requirements.txt",
    "01_protocol/RESEARCH_PROTOCOL.md", "01_protocol/ANALYSIS_PLAN.md",
    "02_data/data_dictionary/DATA_DICTIONARY.md", "02_data/data_dictionary/data_dictionary.csv",
    "02_data/metadata/DATA_MANIFEST.csv",
    "03_scripts/run_pipeline.py",
    "06_documentation/data_management/DATA_MANAGEMENT_PLAN.md",
    "06_documentation/analysis_documentation/PIPELINE.md",
    "06_documentation/quality_control/QC_CHECKLIST.md",
    "00_project_management/team/ROLES_AND_PERMISSIONS.md",
]

REQUIRED_DIRS = [
    "00_project_management", "01_protocol", "02_data/raw", "02_data/cleaned", "02_data/processed",
    "02_data/analysis_ready", "02_data/metadata", "02_data/data_dictionary", "03_scripts",
    "04_analysis/tables", "04_analysis/figures", "04_analysis/qc_reports", "05_reports/drafts",
    "05_reports/reviewed", "05_reports/final", "06_documentation", "07_outputs", "99_archive",
    ".github/ISSUE_TEMPLATE",
]

TOP_LEVEL_ALLOWED = {
    "00_project_management", "01_protocol", "02_data", "03_scripts", "04_analysis", "05_reports",
    "06_documentation", "07_outputs", "99_archive", "config", "tools", ".github", ".vscode",
}

FORBIDDEN_STEM = re.compile(
    r"(^|[_\-. ])(final\d*|final[_\- ]?final|latest|new\d*|copy|copy[_\- ]?of|old|temp|untitled)([_\-. ]|$)"
    r"|\(\d+\)$",
    re.IGNORECASE,
)
ALLOWED_CHARS = re.compile(r"^[A-Za-z0-9_.\-]+$")
EXEMPT_NAMES = {".gitkeep", "Makefile", "LICENSE"}
EXEMPT_DIRS = ("99_archive/",)


def tracked_files() -> list[str]:
    try:
        out = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT, text=True)
        return [line for line in out.split("\0") if line]
    except Exception:  # not a git repo: walk the tree
        return [str(p.relative_to(ROOT)) for p in ROOT.rglob("*")
                if p.is_file() and ".git" not in p.parts and ".venv" not in p.parts]


def naming_errors(paths: list[str]) -> list[str]:
    errors = []
    for rel in paths:
        rel = rel.replace("\\", "/")
        if rel.startswith(EXEMPT_DIRS):
            continue
        parts = rel.split("/")
        bad_part = next((p for p in parts if p not in EXEMPT_NAMES and not ALLOWED_CHARS.match(p)), None)
        if bad_part:
            errors.append(f"{rel}: '{bad_part}' contains spaces, non-ASCII (e.g. Arabic) or special characters")
            continue
        name = parts[-1]  # vague-name rule applies to file names (folders such as 05_reports/final are fine)
        stem = name.split(".")[0] if not name.startswith(".") else name
        if name not in EXEMPT_NAMES and FORBIDDEN_STEM.search(stem):
            errors.append(f"{rel}: forbidden vague name '{name}' (final/latest/new/copy/old...). "
                          "Use an explicit version, e.g. name_v1.2.ext")
    return errors


def structure_errors() -> list[str]:
    errors = [f"missing required file: {f}" for f in REQUIRED_FILES if not (ROOT / f).is_file()]
    errors += [f"missing required folder: {d}" for d in REQUIRED_DIRS if not (ROOT / d).is_dir()]
    for top in sorted({p.split("/")[0] for p in tracked_files() if "/" in p}):
        if top not in TOP_LEVEL_ALLOWED:
            errors.append(f"unexpected top-level folder '{top}/' — agree new folders via a Decision Record "
                          "and add them to tools/check_structure.py")
    for numbered in sorted(p for p in ROOT.iterdir() if p.is_dir() and re.match(r"^\d\d_", p.name)):
        if not (numbered / "README.md").is_file():
            errors.append(f"{numbered.name}/ has no README.md")
    return errors


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--names-only", action="store_true")
    ap.add_argument("--files", nargs="*", help="check only these files")
    args = ap.parse_args()

    files = args.files if args.files else tracked_files()
    errors = naming_errors(files)
    if not args.names_only:
        errors += structure_errors()

    if errors:
        print("✗ Structure / naming check failed:\n")
        for e in errors:
            print(f"  - {e}")
        print("\nSee 06_documentation/governance/NAMING_CONVENTIONS.md")
        return 1
    print(f"✓ Structure and naming OK ({len(files)} files checked)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
