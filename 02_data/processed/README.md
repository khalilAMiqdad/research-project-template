# processed — recoded, derived, merged and weighted data (C2)

- **Location:** `$DATA_ROOT/processed/`. Not committed.
- **Produced by:** `03_scripts/03_recoding/03_recode.py` → `<short>_processed_recoded_v*.ext`
  then `03_scripts/04_weighting/04_weight.py` → `<short>_processed_weighted_v*.ext`.
- **Contains:** recodes from `recode_map.csv`, derived variables (documented in the data
  dictionary, stage `processed`), merges with auxiliary files, and `weight_final`.
