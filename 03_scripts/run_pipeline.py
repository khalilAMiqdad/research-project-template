"""Run the full reproducible pipeline, in order, stopping at the first failure.

  python 03_scripts/run_pipeline.py              # all stages
  python 03_scripts/run_pipeline.py --from 03    # stage 03 onwards
  python 03_scripts/run_pipeline.py --only 06    # a single stage
  python 03_scripts/run_pipeline.py --list       # show stages

Raw Data -> 01 Validation -> 02 Cleaning -> 03 Recoding -> 04 Weighting
         -> 05 Analysis dataset -> 06 Descriptives -> 07 Cross-tabs -> 08 Figures -> Report
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
STAGES = [
    ("01", "Validate raw data", "01_validation/01_validate_raw.py"),
    ("02", "Clean", "02_cleaning/02_clean.py"),
    ("03", "Recode & derive", "03_recoding/03_recode.py"),
    ("04", "Weight", "04_weighting/04_weight.py"),
    ("05", "Build analysis dataset", "05_analysis_dataset/05_build_analysis_dataset.py"),
    ("06", "Descriptive tables", "06_descriptive_analysis/06_descriptives.py"),
    ("07", "Cross-tabulations", "07_comparative_analysis/07_crosstabs.py"),
    ("08", "Figures", "08_visualization/08_figures.py"),
]


def main() -> int:
    ap = argparse.ArgumentParser(description="Run the [PROJECT_NAME] pipeline")
    ap.add_argument("--from", dest="start", default="01")
    ap.add_argument("--to", dest="end", default="08")
    ap.add_argument("--only")
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()
    if args.list:
        for sid, name, path in STAGES:
            print(f"{sid}  {name:<24} 03_scripts/{path}")
        return 0
    selected = [s for s in STAGES if (s[0] == args.only if args.only else args.start <= s[0] <= args.end)]
    for sid, name, path in selected:
        print(f"\n=== Stage {sid}: {name} ===", flush=True)
        t0 = time.time()
        code = subprocess.call([sys.executable, str(HERE / path)])
        if code != 0:
            print(f"Stage {sid} FAILED (exit {code}). Pipeline stopped.", file=sys.stderr)
            return code
        print(f"Stage {sid} done in {time.time() - t0:.1f}s")
    print("\nPipeline complete. Review 04_analysis/qc_reports/ and commit the manifest + outputs via a PR.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
