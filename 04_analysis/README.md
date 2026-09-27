# 04_analysis — generated analysis outputs

Everything here is **produced by scripts** and must be reproducible by re-running the pipeline.
Do not edit these files by hand.

| Folder | Content | Produced by |
| --- | --- | --- |
| `tables/` | `tab_desc_*.csv`, `tab_xtab_*.csv` — aggregate, small cells suppressed | stages 06–07 |
| `figures/` | `fig_*.svg` / `.png` (PNG via Git LFS) | stage 08 |
| `statistical_outputs/` | model results, test statistics (text/CSV/HTML) | analysis scripts |
| `qc_reports/` | stage QC and cleaning logs — counts only | stages 01–05 |
| `analysis_reports/` | analyst notes interpreting outputs for the report team | analysts |

Allowed: aggregate numbers. **Not allowed:** row-level data, lists of IDs with values, free-text answers.
