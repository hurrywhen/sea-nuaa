# Financial replay caliber audit (v1.9)

**Status: `POST_HOC_CALIBER_AUDIT__SAME_CORPUS_DESCRIPTIVE`.** No LLM calls, downloads, or new intervention data.

## Denominators

The expanded configuration has **19 critical propositions**, **18 critical company-days**, and 10 distinct tickers. A proposition is keyed by `(ticker,date,family)`; these units must not be interchanged.

| Unit | Hits / opportunities (pooled over seven m=5 runs) | Ratio |
|---|---:|---:|
| Agent–proposition evaluation | 121 / 133 | 0.909774436 |
| Agent–company-day evaluation | 114 / 126 | 0.904761905 |

The proposition value 121/133 = 0.9097744361 pools seven runs with 19 targets each. It is not one independent 133-target corpus. The increase 18→19 is valid in proposition units, but not in company-day units: the expanded 19 propositions represent 18 company-days. The configurations are non-paired, and the historical company-day denominator was not reconstructed.

## Semi-oracle configurations, budget alarms, and supervised feature-scorer comparisons

| Configuration | Parametric S2p agent–target recall | Supervised feature-scorer mean recall | Budget-conflict alarms |
|---|---:|---:|---:|
| Historical | 120/(7×18) = 0.952380952 | 0.722222222 | 7/7 |
| Expanded | 121/(7×19) = 0.909774436 | 0.789473684 | 7/7 |

The parametric score uses realized legal/market labels and is semi-oracle. Both m=5 configurations use 150 monthly slots rather than a strict daily cap. Supply (4.6/4.733 propositions per day) exceeds the Channel-I cap (3/day), and every m=5 run alarms. Neither configuration establishes an R4-compliant 95% delivery guarantee. The supervised feature scorer is trained on day<15 realized labels and evaluated descriptively over the full month. Its identical deterministic selection is repeated across seven agent rows, not seven independent feature experiments; it is neither label-free nor held-out evidence.

## Per-run reconstruction

| Agent | Proposition recall | Company-day recall |
|---:|---:|---:|
| 3 | 18/19 = 0.947368421 | 17/18 = 0.944444444 |
| 7 | 15/19 = 0.789473684 | 14/18 = 0.777777778 |
| 11 | 18/19 = 0.947368421 | 17/18 = 0.944444444 |
| 15 | 18/19 = 0.947368421 | 17/18 = 0.944444444 |
| 19 | 18/19 = 0.947368421 | 17/18 = 0.944444444 |
| 23 | 17/19 = 0.894736842 | 16/18 = 0.888888889 |
| 27 | 17/19 = 0.894736842 | 16/18 = 0.888888889 |

Every reconstructed proposition recall equals the frozen `p2_rows.csv` value to 1e-12. The company-day column is a post-hoc unit-sensitivity description, not a new confirmatory result.

## Coverage matrix interpretation

`critical_coverage_matrix.csv` contains one binary row per market-proxy proposition and one column per source class. These are observed indicators, not repeated Bernoulli samples for each proposition. They estimate neither a uniform proposition-conditional `p_min` nor `k_eff`. Conditional recovery does not establish independence; target construction by `family` also confounds source class and target type.

## Timestamp availability

Among the 19 portfolio targets, 7 have acceptance_hour>=13, 8 are news items without that timestamp, and only 4 satisfy the code's <13 marker. The marker is a feature, not a pre-availability filter.
