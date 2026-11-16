# Replay integrity audit — LEGACY_EXPLORATORY_NOT_DEDUPLICATED

> Independent read-only audit. No first/last-row or other post-hoc deduplication rule is applied.
> These are **not new frozen primary results**. Any unique-key disposition must be pre-specified before reanalysis.

## Reproduce

From `~/sea`:

```bash
# Default: read-only, print report to stdout; writes nothing
PYTHONDONTWRITEBYTECODE=1 python3 sim/sea_pilot/audit_replay_integrity.py

# Emit only the two dedicated result artifacts (never modifies replay JSONL)
PYTHONDONTWRITEBYTECODE=1 python3 sim/sea_pilot/audit_replay_integrity.py --write
```

Dependencies: Python >= 3.10 and NumPy. The script uses only immutable replay JSONL inputs.
Existing output files require `--force` for replacement.

## Totals

- Shards: **292**; runs: **80**; raw rows: **73704**
- Nonempty `picked`: **73547**; empty selections: **157**
- Unique `(family, run, agent, sim_day)` keys: **71914**
- Duplicate excess: **1633**; unique deficit vs nominal 72000: **86**
- Arithmetic check: 73704 − 73547 = 157; 73547 − 1633 = 71914; 72000 − 71914 = 86
- Therefore 73,547 is a pipeline-valid row count, not a verified count of unique agent-days. The 1,547 row excess over 72,000 is not evidence of additional independent agent-days.

| Family | Raw | Empty | Valid | Unique | Duplicate excess | Unique shortfall vs nominal | Runs below 900 unique |
|---|---:|---:|---:|---:|---:|---:|---:|
| O | 27415 | 30 | 27385 | 26985 | 400 | 15 | 4 |
| C | 27497 | 38 | 27459 | 26979 | 480 | 21 | 8 |
| Q | 9365 | 44 | 9321 | 8978 | 343 | 22 | 6 |
| G | 9427 | 45 | 9382 | 8972 | 410 | 28 | 7 |

## Duplicate outcomes

- Repeated keys: **1608**; same outcome keys: **219**; different outcome keys: **1389**
- Same-outcome excess records: **220**; different-outcome excess records: **1413**
- Outcome comparison fields: `picked, hits_llm, hits_param, n_crit, value_llm, value_param` (order preserved).

De-identified file/line examples (numeric outcome only; no rationale text):

- agent=0, sim_day=20: **different** — llm_replay_c_r01a.jsonl:21; llm_replay_c_r01a.jsonl:143
- agent=0, sim_day=25: **different** — llm_replay_c_r01a.jsonl:25; llm_replay_c_r01a.jsonl:144
- agent=0, sim_day=4: **same** — llm_replay_qc_r06.jsonl:831; llm_replay_qc_r06.jsonl:898
- agent=0, sim_day=5: **same** — llm_replay_ga_r06a.jsonl:418; llm_replay_ga_r06a.jsonl:450

## Legacy exploratory contrasts (not deduplicated)

Family means use unweighted run estimates. Intervals are percentile run-bootstrap 95% CIs, seed=42, 10,000 resamples.
These values reproduce the legacy non-deduplicated pipeline and must not be represented as new frozen primary results.

| Family | Judgment−parametric recall contrast [95% CI] | Δvalue [95% CI] |
|---|---|---|
| O | +0.029954 [-0.004266, +0.064719] | -0.174953 [-0.292388, -0.054597] |
| C | +0.130914 [+0.100330, +0.160221] | +0.676372 [+0.552233, +0.809795] |
| Q | +0.109360 [+0.080931, +0.141390] | +0.431757 [+0.291113, +0.561243] |
| G | +0.087009 [+0.022198, +0.144005] | -0.223145 [-0.426896, -0.030564] |

## Required next step (not performed here)

The unique key is already defined. Pre-specify its duplicate-disposition/outcome-arbitration rule and treatment of the 86-key nominal deficit **before** looking at outcome-sensitive results, then rerun the complete analysis.
This audit deliberately does not choose first/last records or infer the historical cause of any duplicate.

Script version: 1.0.0 · status: **LEGACY_EXPLORATORY_NOT_DEDUPLICATED** · disposition: **UNRESOLVED_PREREGISTRATION_REQUIRED_THEN_RECOMPUTE**.
