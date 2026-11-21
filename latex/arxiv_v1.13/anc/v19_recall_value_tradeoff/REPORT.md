# Recall versus citation-weighted return: strict-singleton decomposition

**Status: `POST_HOC_STRICT_SINGLETON_DECOMPOSITION__WITHIN_CORPUS_EXPLORATORY`.** No new model calls or intervention data.

The former ‘value’ is the selected papers’ sum of log1p(citation), not decision utility, SEA value, or human welfare. The identity below is an accounting decomposition, not a causal explanation:

$\Delta$return = $\Delta$critical-item return + $\Delta$noncritical-item return.

| Family | Δrecall | Δtotal citation return [run CI] | Δcritical-item return | Δnoncritical-item return | Δselected count |
|---|---:|---:|---:|---:|---:|
| O | +0.030230 | -0.175557 [-0.293701, -0.054364] | +0.124007 | -0.299564 | -0.044889 |
| C | +0.128146 | +0.663589 [+0.535146, +0.799188] | +0.606797 | +0.056792 | -0.009278 |
| Q | +0.115622 | +0.420392 [+0.285632, +0.543034] | +0.510555 | -0.090163 | -0.000936 |
| G | +0.089547 | -0.219101 [-0.425724, -0.026358] | +0.410169 | -0.629270 | -0.182926 |

A positive recall difference does not imply a positive citation-return difference. The critical/noncritical columns are consistent with both substitution and changed selected counts; the decomposition does not separate those mechanisms. O's critical-item interval includes zero, and C/Q's noncritical intervals include zero. The endpoint remains a retrospective academic-impact proxy; none of these columns establishes decision value, welfare, or the overall effect of SEA.

`run_metrics.csv` preserves all 80 run-level estimates. CIs resample runs within family (10,000 times, seed 42) and do not include shared-corpus or model dependence.
