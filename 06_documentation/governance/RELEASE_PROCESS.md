# Release Process

A release freezes **code + documentation + outputs + the data version** so that results can
be reproduced and cited. Releases are tags on `main`; nobody tags an unreviewed commit.

## 1. Before the release (release PR)

1. Open an Issue "Release vX.Y.Z" (template *Research Task*, label `release`).
2. Branch `chore/<issue>-release-vX.Y.Z`.
3. Independent reproduction: a reviewer runs, from a fresh clone,
   `python tools/data_manifest.py verify && python 03_scripts/run_pipeline.py`
   and confirms outputs are identical (`git status` shows no changes to `04_analysis/`).
4. Complete [QC_CHECKLIST.md](../quality_control/QC_CHECKLIST.md) §5 (release) in the PR.
5. Update `CHANGELOG.md`: move items from `[Unreleased]` to `[X.Y.Z] — YYYY-MM-DD`,
   state **Data version: vA.B**, list result changes.
6. Update `CITATION.cff` (`version`, `date-released`).
7. For final reports: copy the approved PDF to `05_reports/final/` with the version in its name,
   and approved outputs to `07_outputs/`.
8. `python tools/check_docs.py --strict` must pass (no unfilled placeholders in core docs).
9. Approvals: Project Lead + owners of changed areas.

## 2. Tag and publish

```bash
git switch main && git pull --ff-only
git tag -a v1.0.0 -m "v1.0.0 — final report results (data v1.3)"
git push origin v1.0.0
```

The `release.yml` workflow runs the strict checks and creates the GitHub Release with the
CHANGELOG section as release notes. Optionally attach the PDF report to the release and
archive the release in [ARCHIVE_REPOSITORY] (e.g. via Zenodo integration) for a DOI.

## 3. After the release

- Close the release milestone; move board items to *Completed* / *Archived*.
- Superseded report drafts → `99_archive/previous_versions/` (only if still needed — Git keeps history).
- Record the release in the Decision Log if it was a formal deliverable.
