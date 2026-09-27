# metadata

| File | Purpose |
| --- | --- |
| `DATA_MANIFEST.csv` | One row per data file ever produced: stage, dataset version, **SHA-256**, rows, columns, producing script, input files, Git commit, timestamp. Written automatically by the pipeline; commit it in the same PR as the code that produced the data. |

Verify a local copy of the data against the manifest:

```bash
python tools/data_manifest.py verify                # all stages
python tools/data_manifest.py verify --stage analysis_ready
python tools/data_manifest.py add path/to/file.csv --stage raw   # manual registration
```

The manifest contains **no data values** — only file-level metadata — so it is safe for Git.
Other metadata files allowed here: `*.md` (e.g. platform export settings, codebook notes).
