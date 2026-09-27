# config

| File | Purpose | In Git? |
| --- | --- | --- |
| `project.yml` | Pipeline settings: dataset version, raw files, weighting, analysis parameters | yes |
| `.env.example` | Names of local environment variables (`DATA_ROOT`, API tokens) | yes (no values) |
| `../.env` | Your local values | **never** (git-ignored) |

Settings marked REQUIRED come from the Research Protocol / Analysis Plan; a change to them is
a methodological change and needs the Methodology Lead's review.
