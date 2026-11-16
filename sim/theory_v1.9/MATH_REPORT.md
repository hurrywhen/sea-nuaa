# v1.9 mathematical reproduction report

All population threshold values and Pareto sums are deterministic. Finite-top-m means use quadrature; Monte Carlo intervals quantify only simulation error, not empirical uncertainty.

## Population Gaussian model

- Filtering arithmetic: 0.998875000 (99.8875%).
- Required separation: 4.389337888; AUC 0.999044514.
- Population recall at d'=1.5 / 2.5: 0.209639680 / 0.523766570.
- With fixed CDF-quantile notation, a critical recall R uses Q1(1-R), hence Q1(0.05) at R=0.95. Boundary cases are recorded in summary.json.

## Finite top-m selection (M=800, K=8, m=10)

| d' | Population recall | Exact-formula E[finite recall] (converged quadrature) | Finite−population | MC mean [MC 95% CI] | Realized 2.5%, 50%, 97.5% quantiles |
|---:|---:|---:|---:|---:|---:|
| 1.5000000 | 0.209639680 | 0.208660712 | -0.000978969 | 0.207418750 [0.205547452, 0.209290048] | 0.000, 0.250, 0.500 |
| 2.5000000 | 0.523766570 | 0.524234386 | +0.000467815 | 0.523000000 [0.520811789, 0.525188211] | 0.250, 0.500, 0.875 |
| 4.3893379 | 0.950000000 | 0.952626284 | +0.002626284 | 0.952825000 [0.951824563, 0.953825437] | 0.750, 1.000, 1.000 |

The finite expected recall is not obtained by plugging the empirical top-m threshold into the population identity. Predictive quantiles describe between-realization variability; the MC CI describes only numerical error in the estimated expectation.

## Pareto leakage

| K,m | Exact | Integral approximation at actual m/K | Approx−exact (pp) |
|---|---:|---:|---:|
| 52,26 | 20.799886% | 20.629947% | -0.169939 |
| 52,42 | 6.919112% | 6.871634% | -0.047478 |

## Counterexamples and design calculations

- Weighted-miss example: exact 0.410000; invalid pooled-product 0.250000. A pooled class mean cannot be inserted into a proposition-wise product.
- Unified-update binary example: W=-0.240000, correct-model VOI=0.240000, regret=0.480000. The same assumed mixture likelihood is used for every observed signal.
- RCT normal approximation with one declared primary comparison: ceil before attrition 129/arm; after 25% attrition 171/arm (total 513).
- Two co-primary Bonferroni sensitivity: 207/arm (total 621). These are future-design calculations only.
