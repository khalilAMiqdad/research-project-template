#!/usr/bin/env python3
"""Block sensitive files, personal-data patterns, microdata and oversized files.

  python tools/check_sensitive.py                  # all tracked files (CI)
  python tools/check_sensitive.py --files a b c    # given files (pre-commit)

Checks
  1. Secret / credential file names (.env, *.pem, *.key, id_rsa, credentials...).
  2. Microdata, media and geodata formats outside the approved folders.
  3. Anything inside 02_data/ that is not documentation/metadata or approved_deid/.
  4. Files larger than MAX_MB that are not stored with Git LFS.
  5. CSV headers that look like direct identifiers (name, phone, email, national_id, gps...).
  6. Text content with e-mail addresses, phone numbers or precise GPS coordinates.

False positives: add a justified line to .sensitive-allowlist (glob path patterns) — this file
is owned by the Project Lead and Data Manager (CODEOWNERS). Standard library only.
"""
from __future__ import annotations

import argparse
import csv
import fnmatch
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAX_MB = 5
ALLOWLIST_FILE = ROOT / ".sensitive-allowlist"
SELF = "tools/check_sensitive.py"

SECRET_NAME_PATTERNS = [
    ".env", ".env.*", "*.pem", "*.key", "*.p12", "*.pfx", "*.jks", "*.keystore", "*.kdbx",
    "*.secret", "*.secrets", "id_rsa*", "id_ed25519*", "*.ppk", "*credential*", "*password*",
    "*passwd*", "*secret*.json", "*secret*.y*ml", "service-account*.json", "client_secret*.json",
    "token.json", ".netrc", ".pgpass", ".Renviron", "*.token",
]
SECRET_NAME_EXCEPTIONS = {".env.example"}

MICRODATA_EXT = {".sav", ".zsav", ".por", ".dta", ".sas7bdat", ".xpt", ".rds", ".rdata", ".rda",
                 ".parquet", ".feather", ".h5", ".hdf5", ".db", ".sqlite", ".sqlite3", ".mdb",
                 ".accdb", ".zip", ".7z", ".rar", ".tar", ".gz"}
MEDIA_GEO_EXT = {".m4a", ".mp3", ".wav", ".amr", ".3gp", ".mp4", ".mov", ".kml", ".kmz", ".gpx",
                 ".shp", ".geojson"}
DATA_ALLOWED_DIRS = ("02_data/analysis_ready/approved_deid/", "07_outputs/datasets/")
DATA_DIR_ALLOWED = [
    "02_data/*README.md", "02_data/*.gitkeep", "02_data/metadata/DATA_MANIFEST.csv",
    "02_data/metadata/*.md", "02_data/data_dictionary/DATA_DICTIONARY.md",
    "02_data/data_dictionary/data_dictionary.csv", "02_data/analysis_ready/approved_deid/*",
]

PII_HEADER = re.compile(
    r"^(full_?name|first_?name|last_?name|family_?name|name|respondent_?name|father_?name|"
    r"phone|phone_?number|mobile|mobile_?number|tel|telephone|whatsapp|e_?mail|email_?address|"
    r"national_?id|id_?number|id_?no|passport|passport_?no|identity_?number|ssn|"
    r"address|home_?address|street|house_?number|gps|gps_?lat|gps_?lon|latitude|longitude|lat|lon|lng|"
    r"coordinates|geolocation|ip_?address|date_?of_?birth|dob|signature)$",
    re.IGNORECASE,
)
TEXT_EXT = {".csv", ".tsv", ".txt", ".md", ".py", ".r", ".rmd", ".qmd", ".do", ".sps", ".yml",
            ".yaml", ".json", ".ipynb", ".html", ".tex", ".sql", ".cff"}
EMAIL = re.compile(r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b")
EMAIL_OK = re.compile(r"@(example\.(com|org|net)|users\.noreply\.github\.com|anthropic\.com)$|^noreply@", re.I)
PHONE = re.compile(r"(?<![\w.])(\+\d{1,3}[\s\-]?\(?\d{1,4}\)?[\s\-]?\d{3}[\s\-]?\d{3,4}|0[5-9]\d{8})(?![\w.])")
GPS_PAIR = re.compile(r"-?\d{1,3}\.\d{5,}\s*[,;]\s*-?\d{1,3}\.\d{5,}")


def git_files() -> list[str]:
    try:
        out = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT, text=True)
        return [f for f in out.split("\0") if f]
    except Exception:
        return [str(p.relative_to(ROOT)) for p in ROOT.rglob("*")
                if p.is_file() and ".git" not in p.parts and ".venv" not in p.parts]


def is_lfs(rel: str) -> bool:
    path = ROOT / rel
    try:
        with open(path, "rb") as fh:
            if fh.read(40).startswith(b"version https://git-lfs"):
                return True
        out = subprocess.check_output(["git", "check-attr", "filter", "--", rel], cwd=ROOT, text=True)
        return out.strip().endswith(": lfs")
    except Exception:
        return False


def load_allowlist() -> list[str]:
    if not ALLOWLIST_FILE.exists():
        return []
    return [line.split("#")[0].strip() for line in ALLOWLIST_FILE.read_text(encoding="utf-8").splitlines()
            if line.split("#")[0].strip()]


def match_any(name: str, patterns) -> bool:
    return any(fnmatch.fnmatch(name, p) for p in patterns)


def check_file(rel: str) -> list[str]:
    rel = rel.replace("\\", "/")
    path = ROOT / rel
    name = path.name
    lower_name = name.lower()
    ext = path.suffix.lower()
    problems = []

    if name not in SECRET_NAME_EXCEPTIONS and match_any(lower_name, SECRET_NAME_PATTERNS):
        problems.append("secret/credential file name — never commit secrets (SECURITY.md §4)")
    if ext in MEDIA_GEO_EXT:
        problems.append(f"audio/video/geodata file ({ext}) — C3 data, keep in secure storage")
    if ext in MICRODATA_EXT and not rel.startswith(DATA_ALLOWED_DIRS):
        problems.append(f"microdata/archive format ({ext}) outside approved folders (DATA_SECURITY.md §3)")
    if rel.startswith("02_data/") and not match_any(rel, DATA_DIR_ALLOWED):
        problems.append("data file inside 02_data/ — data belong in $DATA_ROOT secure storage")
    if not path.exists():
        return problems

    size_mb = path.stat().st_size / 1_048_576
    if size_mb > MAX_MB and not is_lfs(rel):
        problems.append(f"file is {size_mb:.1f} MB (> {MAX_MB} MB) and not tracked by Git LFS")

    if ext in TEXT_EXT and rel != SELF and size_mb <= 20:
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            text = ""
        if ext in (".csv", ".tsv") and text:
            header = next(csv.reader([text.splitlines()[0]], delimiter="\t" if ext == ".tsv" else ","), [])
            bad = [h for h in header if PII_HEADER.match(h.strip())]
            if bad:
                problems.append(f"column(s) look like direct identifiers: {', '.join(bad)}")
        emails = [e for e in EMAIL.findall(text) if not EMAIL_OK.search(e)]
        if emails:
            problems.append(f"{len(emails)} e-mail address(es) found (e.g. {emails[0][:3]}***)")
        phones = PHONE.findall(text)
        if phones:
            problems.append(f"{len(phones)} phone-number-like value(s) found")
        if GPS_PAIR.search(text):
            problems.append("precise GPS coordinate pair(s) found")
    return problems


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--files", nargs="*")
    args = ap.parse_args()
    files = args.files if args.files else git_files()
    allow = load_allowlist()

    failures = {}
    for rel in files:
        rel_norm = str(Path(rel)).replace("\\", "/")
        if match_any(rel_norm, allow):
            continue
        problems = check_file(rel_norm)
        if problems:
            failures[rel_norm] = problems

    if failures:
        print("✗ Sensitive-data check FAILED\n")
        for rel, problems in failures.items():
            print(f"  {rel}")
            for p in problems:
                print(f"     - {p}")
        print("\nWhat to do: remove the file from the commit (git rm --cached <file>), move data to secure "
              "storage, and if anything sensitive was already pushed follow SECURITY.md immediately.")
        return 1
    print(f"✓ Sensitive-data check passed ({len(files)} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
