# `sea_algo` version and evidence boundary

This directory contains the **historical A1–A10 algorithm experiments** developed for the v1.0/v1.7 manuscript lineage. It is not an end-to-end implementation of the v1.10 SAP tuple and does not establish joint optimality, actual consumption, human effectiveness, or S1–S4 governance conformance.

## Stable identifiers

Cross-version code references use `A1`–`A10` only. Manuscript theorem numbers changed between versions and are not code contracts.

| ID | Historical module | Current evidence boundary |
|---|---|---|
| A1 | `prop_graph.py` | Proposition/document aggregation checks |
| A2, A9 | `selector.py` | Historical dual-channel and salience-firewall experiments |
| A3 | `planner.py` | Heuristic `p_hat * value - kappa * cost` query scoring; not a full conditional-EIG theorem |
| A4 | `scheduler.py` | Restricted Pandora/threshold calculations |
| A5 | `allocator.py` | Historical marginal-score allocation; not joint SAP optimality |
| A6, A7 | `watchlist.py` | Standard coverage/greedy and rolling-list experiments |
| A8 | `certify.py` | Descriptive scarcity weighting; no pointwise independence or recall floor |
| A10 | `calib.py` | AI-task calibration material; no human transfer certificate |

The historical `validate.py` and `validate_p3.py` reports retain their original dates and calibers. The README phrase **9/9 algorithm validation** refers only to the nine historical tests in that 2026-09-30 suite. It is separate from the v1.10 governance suite (`sim/sea_governance`, 14 synthetic conformance tests) and from mathematical or replay regression tests.

For the current guarded objective store, rollback, fixed-supply/supply-ecology counterfactuals, hash-chain tamper tests, and recourse interface, use `sim/sea_governance/` instead.
