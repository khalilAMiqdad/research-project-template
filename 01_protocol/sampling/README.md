# sampling

- [SAMPLING_PLAN.md](SAMPLING_PLAN.md) — design, frame, allocation, selection, sample-size calculation.
- Scripts that compute sample size or select units may live here (`sample_size_calculation.py|R`),
  with fixed random seeds recorded in the plan.
- **Never commit** a sampling frame that contains names, addresses, phone numbers or exact
  coordinates. Frames stay in `$DATA_ROOT/restricted/`; only aggregate allocation tables are committed.
