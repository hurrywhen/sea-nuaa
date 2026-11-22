## R5 Secondary Rule A and strict-singleton calibers

Rule A uses nonempty selections with metric-specific cohorts: 71,573 recall, 70,676 citation-return, 71,618 paired-sign keys. Strict singleton uses exactly one nonempty record per key: 70,306 common keys. These populations differ from the all-record calibers and must not be subtracted cell by cell.

### SB.1 Rule A: nonempty selections with metric-specific cohorts

**Supplementary Table SB1. Secondary Rule A: 71,573 recall, 70,676 citation-return, and 71,618 paired-sign resolved keys.**

| Family | R/V/S keys | Selected recall | Parametric recall | $\Delta$recall [interval] | $\Delta$citation return [interval] |
|---|---|---:|---:|---:|---:|---:|
| O | 26,908 / 26,668 / 26,918 | 0.443790 | 0.413620 | +0.030170 [−0.003971, +0.064767] | −0.175016 [−0.293452, −0.053577] |
| C | 26,851 / 26,577 / 26,869 | 0.532600 | 0.403317 | +0.129283 [+0.098441, +0.158663] | +0.667380 [+0.539180, +0.802858] |
| Q | 8,916 / 8,733 / 8,926 | 0.516153 | 0.403265 | +0.112887 [+0.081432, +0.147666] | +0.426727 [+0.295044, +0.548216] |
| G | 8,898 / 8,698 / 8,905 | 0.519783 | 0.430371 | +0.089412 [+0.022924, +0.148522] | −0.219053 [−0.427112, −0.025626] |

### SB.2 Strict-singleton citation-return accounting

**Supplementary Table SB2. Strict-singleton C: 70,306 common keys; selected citation-return accounting decomposition.**

| Family | Keys | $\Delta$critical-item return | $\Delta$noncritical-item return | Total return | $\Delta$selected count |
|---|---:|---:|---:|---:|---:|
| O | 26,592 | +0.124007 | −0.299564 | −0.175557 | −0.044889 |
| C | 26,499 | +0.606797 | +0.056792 | +0.663589 | −0.009278 |
| Q | 8,641 | +0.510555 | −0.090163 | +0.420392 | −0.000936 |
| G | 8,574 | +0.410169 | −0.629270 | −0.219101 | −0.182926 |

For O, the critical-item component's exploratory interval is [−0.054770, +0.304276], crossing zero; G's is [+0.048621, +0.729638]. Noncritical-item intervals are [−0.403201, −0.186791] for O and [−0.781947, −0.459691] for G. C/Q noncritical intervals also cross zero. Positive O/G critical-item point estimates are outweighed by noncritical declines. Under the intentional favor-LLM endpoint, O/G total-return intervals include zero. The identity is accounting, not a causal explanation of substitution or changed counts. Retrospective $\log(1+\text{2026 citations})$ is not ex-ante decision utility or welfare.

### SB.3 All 17 frozen missing/conflict/endpoint scenarios

**Supplementary Table SB3. Run-equal point-estimate ranges across all 17 scenarios.**

| Family | $\Delta$recall min–max | Recall sign changes | $\Delta$citation return min–max | Return sign changes |
|---|---:|---:|---:|---:|
| O | +0.027697 to +0.033656 | 0 | −0.277317 to −0.103091 | 0 |
| C | +0.124652 to +0.133596 | 0 | +0.522966 to +0.749538 | 0 |
| Q | +0.104956 to +0.120525 | 0 | +0.159403 to +0.587765 | 0 |
| G | +0.079407 to +0.097947 | 0 | −0.507806 to −0.027918 | 0 |

Recall point estimates stay positive in all 17 scenarios; citation return stays positive for C/Q and negative for O/G. Zero point-estimate sign changes do not make every interval exclude zero and do not identify a structural effect. Exact per-scenario denominators and intervals remain in `scenario_effects.csv`.
