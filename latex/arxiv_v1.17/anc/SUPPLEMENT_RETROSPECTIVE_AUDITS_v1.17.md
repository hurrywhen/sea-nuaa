# SEA v1.17 Supplementary Retrospective Sensitivity Audits

> **References:** all citations use the unified reference list in the v1.17 main manuscript.
>
> **Status: frozen post-hoc selected-proxy descriptions on one shared corpus.** These tables are moved out of the main text because they do not identify a structural SEA effect. They contain no delivered/opened/attended observations, no independent environments, and no prospective primary analysis. Bootstrap intervals and nominal tests below are exploratory artifacts only; they are not deployment confidence statements or calibrated cross-corpus error rates.
>
> **Single source:** section R5 is the only authoritative location of the secondary Rule A, strict-singleton, and 17-scenario tables. It is regenerated from the frozen data files by `tools/make_retrospective_tables.py` and verified against them by the release audit; the formal supplement keeps pointers only.

## R1 Key flow and caliber definitions

72,000 expected keys = 71,970 existing keys + 30 no-row keys. Existing keys = 71,914 nonempty-selection keys + 56 empty-only keys. Raw records = 73,704, including 157 empty records; 101 empty records share nonempty keys. The three calibers differ only in no-row and conflict disposition.

| Caliber | No-row keys | Conflicts | Interpretation |
|---|---|---|---|
| `ALL_EXISTING_RECORD_MEAN_ZERO_EMPTY` | Missing | Attempt means | Designated retrospective descriptive convention |
| `ALL_EXPECTED_RECORD_MEAN_ZERO_EMPTY_NO_ROW` | Selected-proxy zero | Attempt means | Conservative selection-failure sensitivity |
| `METRIC_RESOLVED_ZERO_EMPTY` | Missing | Metric-specific refusal | Conflict-refusing sensitivity |

## R2 Family point estimates and denominators

### ALL_EXISTING_RECORD_MEAN_ZERO_EMPTY

| Family | n recall / return | sum n_crit | Selected recall | Parametric recall | Δrecall | Δcitation return |
|---|---:|---:|---:|---:|---:|---:|
| O | 26996 / 26996 | 25527 | 0.443161 | 0.413441 | +0.029720 | -0.181292 |
| C | 26987 / 26987 | 25556 | 0.532275 | 0.403215 | +0.129060 | +0.662236 |
| Q | 8998 / 8998 | 8310 | 0.513909 | 0.403200 | +0.110709 | +0.396418 |
| G | 8989 / 8989 | 8597 | 0.517008 | 0.430937 | +0.086071 | -0.251347 |

### ALL_EXPECTED_RECORD_MEAN_ZERO_EMPTY_NO_ROW

| Family | n recall / return | sum n_crit | Selected recall | Parametric recall | Δrecall | Δcitation return |
|---|---:|---:|---:|---:|---:|---:|
| O | 27000 / 27000 | 25530 | 0.443105 | 0.413405 | +0.029700 | -0.182199 |
| C | 27000 / 27000 | 25560 | 0.532182 | 0.403169 | +0.129014 | +0.657917 |
| Q | 9000 / 9000 | 8310 | 0.513909 | 0.403200 | +0.110709 | +0.395332 |
| G | 9000 / 9000 | 8610 | 0.516255 | 0.430856 | +0.085398 | -0.260004 |

### METRIC_RESOLVED_ZERO_EMPTY

| Family | n recall / return | sum n_crit | Selected recall | Parametric recall | Δrecall | Δcitation return |
|---|---:|---:|---:|---:|---:|---:|
| O | 26919 / 26679 | 25391 | 0.443505 | 0.413516 | +0.029989 | -0.178179 |
| C | 26859 / 26585 | 25342 | 0.532409 | 0.403328 | +0.129080 | +0.664627 |
| Q | 8936 / 8753 | 8199 | 0.514790 | 0.402854 | +0.111936 | +0.409018 |
| G | 8915 / 8715 | 8469 | 0.518654 | 0.430575 | +0.088079 | -0.237198 |

## R3 Run-level dispersion and sign counts (descriptive, not inferential)

| Caliber | Family | Metric | Runs | Mean | SD | Min | Max | Positive / zero / negative |
|---|---|---|---:|---:|---:|---:|---:|---:|
| ALL_EXISTING_RECORD_MEAN_ZERO_EMPTY | O | Δrecall | 30 | +0.029720 | 0.097289 | -0.155729 | +0.191954 | 19 / 0 / 11 |
| ALL_EXISTING_RECORD_MEAN_ZERO_EMPTY | O | Δcitation return | 30 | -0.181292 | 0.336810 | -0.975474 | +0.504095 | 8 / 0 / 22 |
| ALL_EXISTING_RECORD_MEAN_ZERO_EMPTY | C | Δrecall | 30 | +0.129060 | 0.085272 | -0.093103 | +0.321979 | 28 / 0 / 2 |
| ALL_EXISTING_RECORD_MEAN_ZERO_EMPTY | C | Δcitation return | 30 | +0.662236 | 0.372575 | -0.007818 | +1.583801 | 29 / 0 / 1 |
| ALL_EXISTING_RECORD_MEAN_ZERO_EMPTY | Q | Δrecall | 10 | +0.110709 | 0.054846 | +0.046552 | +0.206667 | 10 / 0 / 0 |
| ALL_EXISTING_RECORD_MEAN_ZERO_EMPTY | Q | Δcitation return | 10 | +0.396418 | 0.224574 | +0.031431 | +0.703414 | 10 / 0 / 0 |
| ALL_EXISTING_RECORD_MEAN_ZERO_EMPTY | G | Δrecall | 10 | +0.086071 | 0.108724 | -0.156771 | +0.231034 | 9 / 0 / 1 |
| ALL_EXISTING_RECORD_MEAN_ZERO_EMPTY | G | Δcitation return | 10 | -0.251347 | 0.344034 | -0.961415 | +0.150117 | 3 / 0 / 7 |
| ALL_EXPECTED_RECORD_MEAN_ZERO_EMPTY_NO_ROW | O | Δrecall | 30 | +0.029700 | 0.097259 | -0.155729 | +0.191954 | 19 / 0 / 11 |
| ALL_EXPECTED_RECORD_MEAN_ZERO_EMPTY_NO_ROW | O | Δcitation return | 30 | -0.182199 | 0.335928 | -0.975474 | +0.504095 | 8 / 0 / 22 |
| ALL_EXPECTED_RECORD_MEAN_ZERO_EMPTY_NO_ROW | C | Δrecall | 30 | +0.129014 | 0.085185 | -0.093103 | +0.321154 | 28 / 0 / 2 |
| ALL_EXPECTED_RECORD_MEAN_ZERO_EMPTY_NO_ROW | C | Δcitation return | 30 | +0.657917 | 0.370117 | -0.007818 | +1.583801 | 29 / 0 / 1 |
| ALL_EXPECTED_RECORD_MEAN_ZERO_EMPTY_NO_ROW | Q | Δrecall | 10 | +0.110709 | 0.054846 | +0.046552 | +0.206667 | 10 / 0 / 0 |
| ALL_EXPECTED_RECORD_MEAN_ZERO_EMPTY_NO_ROW | Q | Δcitation return | 10 | +0.395332 | 0.224063 | +0.031431 | +0.703414 | 10 / 0 / 0 |
| ALL_EXPECTED_RECORD_MEAN_ZERO_EMPTY_NO_ROW | G | Δrecall | 10 | +0.085398 | 0.108420 | -0.156771 | +0.231034 | 9 / 0 / 1 |
| ALL_EXPECTED_RECORD_MEAN_ZERO_EMPTY_NO_ROW | G | Δcitation return | 10 | -0.260004 | 0.340265 | -0.961415 | +0.150117 | 2 / 0 / 8 |
| METRIC_RESOLVED_ZERO_EMPTY | O | Δrecall | 30 | +0.029989 | 0.097199 | -0.156184 | +0.191954 | 19 / 0 / 11 |
| METRIC_RESOLVED_ZERO_EMPTY | O | Δcitation return | 30 | -0.178179 | 0.339113 | -0.976121 | +0.502842 | 8 / 0 / 22 |
| METRIC_RESOLVED_ZERO_EMPTY | C | Δrecall | 30 | +0.129080 | 0.085741 | -0.096400 | +0.324538 | 28 / 0 / 2 |
| METRIC_RESOLVED_ZERO_EMPTY | C | Δcitation return | 30 | +0.664627 | 0.376890 | -0.003995 | +1.580779 | 29 / 0 / 1 |
| METRIC_RESOLVED_ZERO_EMPTY | Q | Δrecall | 10 | +0.111936 | 0.056335 | +0.046674 | +0.207219 | 10 / 0 / 0 |
| METRIC_RESOLVED_ZERO_EMPTY | Q | Δcitation return | 10 | +0.409018 | 0.207228 | +0.064368 | +0.701168 | 10 / 0 / 0 |
| METRIC_RESOLVED_ZERO_EMPTY | G | Δrecall | 10 | +0.088079 | 0.109210 | -0.155154 | +0.237427 | 9 / 0 / 1 |
| METRIC_RESOLVED_ZERO_EMPTY | G | Δcitation return | 10 | -0.237198 | 0.345176 | -0.956393 | +0.172455 | 3 / 0 / 7 |

## R4 Demoted exploratory run-level bootstrap intervals

These 10,000-draw whole-run percentile intervals (seed 42; Efron, 1979) resample runs within one shared corpus. They omit corpus, label, missingness, duplicate-arbitration, backend, and model dependence. They are retained for transparency only and are not used in the main text.

| Caliber | Family | Δrecall interval | Δcitation return interval |
|---|---|---:|---:|
| ALL_EXISTING_RECORD_MEAN_ZERO_EMPTY | O | [-0.004409, +0.064360] | [-0.297932, -0.062012] |
| ALL_EXISTING_RECORD_MEAN_ZERO_EMPTY | C | [+0.098475, +0.158255] | [+0.534883, +0.796727] |
| ALL_EXISTING_RECORD_MEAN_ZERO_EMPTY | Q | [+0.080555, +0.144612] | [+0.258508, +0.521986] |
| ALL_EXISTING_RECORD_MEAN_ZERO_EMPTY | G | [+0.019272, +0.144873] | [-0.457599, -0.062888] |
| ALL_EXPECTED_RECORD_MEAN_ZERO_EMPTY_NO_ROW | O | [-0.004409, +0.064344] | [-0.298424, -0.063222] |
| ALL_EXPECTED_RECORD_MEAN_ZERO_EMPTY_NO_ROW | C | [+0.098454, +0.158164] | [+0.531025, +0.792166] |
| ALL_EXPECTED_RECORD_MEAN_ZERO_EMPTY_NO_ROW | Q | [+0.080555, +0.144612] | [+0.257951, +0.520688] |
| ALL_EXPECTED_RECORD_MEAN_ZERO_EMPTY_NO_ROW | G | [+0.018970, +0.144181] | [-0.462863, -0.072922] |
| METRIC_RESOLVED_ZERO_EMPTY | O | [-0.004113, +0.064420] | [-0.295210, -0.058389] |
| METRIC_RESOLVED_ZERO_EMPTY | C | [+0.098259, +0.158527] | [+0.535973, +0.800840] |
| METRIC_RESOLVED_ZERO_EMPTY | Q | [+0.080700, +0.146579] | [+0.282964, +0.525141] |
| METRIC_RESOLVED_ZERO_EMPTY | G | [+0.020790, +0.147295] | [-0.445377, -0.047897] |

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

## R6 Financial and upstream audit details

The financial historical aggregate is 120 hits over 7×18 recurring agent–target evaluations (120/126=0.952381). The expanded configuration is 121/133 agent–target evaluations (0.909774), concerning 19 propositions on 18 company–days; post-hoc company–day pooling is 114/126 (0.904762). All seven historical and seven expanded configurations trigger budget-conflict alarms. The historical supply constant 4.6 is inherited and not verified from the pinned CSV; reconstructed expanded supply is 4.733, above the Channel-I cap of three propositions per day. The 150 slots are monthly, not strict daily caps. Realized legal/market labels enter the semi-oracle score. Historical selections and the company–day denominator are not independently reconstructed. The public CSV SHA-256 is 80e953d19efb44787d4fb8b03e37ee6cbfbfc325488769df8a0e89281b495024; default reproduction verifies bytes and row count without Git.

Across frozen academic seed sets, 24–33 of 52 proxy targets reach a run digest. Family means are 28.37 (O), 28.40 (C), 27.70 (Q), 28.70 (G), or 53.27%–55.19% upstream opportunity share. O and G share seeds 1–10 and therefore ten identical upstream digest pairs. Judgment recall is conditional on targets reaching the digest; the upstream share is not a legitimate multiplier without a separately frozen joint estimand.

## R7 What these audits cannot support

No table here measures actual delivery, opening, attendance, latent consumption, decision utility, welfare, efficiency, or independent-environment robustness. Positive point estimates and stable signs across 17 missing/conflict scenarios do not convert a retrospective selected-proxy description into a structural effect. Nominal agent-day McNemar (McNemar, 1947) / CMH (Cochran, 1954; Mantel & Haenszel, 1959) or sign-flip calculations, if present in older frozen outputs, are dependence approximations only and are not used as calibrated inference. The main text therefore reports boundaries and a falsification example rather than these estimates as benefits.
