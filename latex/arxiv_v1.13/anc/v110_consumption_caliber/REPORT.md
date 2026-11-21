# Frozen replay selected-proxy consumption-caliber audit

**Status: `POST_HOC_SELECTED_PROXY_RETROSPECTIVE_DESCRIPTIVE__WITHIN_CORPUS_EXPLORATORY`.** No model calls, interventions, or new delivery/open/consumption observations.

`picked` identifies a **selected proxy only**. Neither selected recall nor selected citation-weighted return is actual consumption, decision utility, welfare, or an end-to-end effect.

## 1. Observable records and identification boundary

- 292 hash-verified shards; 73704 nonblank JSONL rows; 73704 structurally parseable policy records; 157 have `picked=[]`.
- Current-file transport failures: **0**; JSONL decode/parse failures: **0**; invalid policy records: **0**. Separately, **154** stored rows say `reason='parse-error'`; **3** empty rows have other reason text.
- Historical API transport failures are not observable from these JSONL fields and are not inferred from dispatch logs. Current successful file reads do not establish historical delivery or execution success.
- The records contain no delivered/opened/attended or item-level actual-consumption fields. `raw_consume` is a raw-output diagnostic and `impulse_consumed` concerns injected impulses; neither repairs the missing chain.
- **Historical logs cannot distinguish valid abstention from silent empty-selection execution failure.** This audit therefore labels zero only as a selected-proxy sensitivity assignment, never as observed actual non-consumption.

## 2. Existing-key accounting and unresolved duplicates

An existing key has at least one structurally parseable policy record. There are **71970 = 71914 nonempty-key + 56 empty-only** existing keys. **30** no-row keys remain missing in the existing-key and resolved calibers; only the explicitly named conservative all-expected-key caliber assigns them selected-proxy zero. The 101 empty records sharing nonempty keys are counted in the all-record-mean caliber and reported separately in the resolved caliber; they are not extra independent keys.

| Family | Expected | Nonempty keys | Empty-only | Existing frame | Missing | Empty rows on nonempty keys | Stored parse-error rows |
|---|---:|---:|---:|---:|---:|---:|---:|
| O | 27000 | 26985 | 11 | 26996 | 4 | 19 | 29 |
| C | 27000 | 26979 | 8 | 26987 | 13 | 30 | 36 |
| Q | 9000 | 8978 | 20 | 8998 | 2 | 24 | 44 |
| G | 9000 | 8972 | 17 | 8989 | 11 | 28 | 45 |
| **Total** | **72000** | **71914** | **56** | **71970** | **30** | **101** | **154** |

Nonempty duplicate groups: **1608**; excess nonempty records: **1633**. Metric conflicts are recall **341**, citation return **1238**, paired sign **296**, and any six-field conflict **1389**. No conflict is silently assigned zero.

Key flow: 72,000 expected keys = 71,970 existing keys + 30 no-row keys; 71,970 existing keys = 71,914 nonempty-selection keys + 56 empty-only keys. The 73,704 raw records include 157 empty records, of which 101 share nonempty keys. The three calibers differ only in no-row and conflict disposition, not in the frozen raw inputs.

## 3. Complete all-existing-key zero-empty sensitivity (`ALL_EXISTING_RECORD_MEAN_ZERO_EMPTY`)

Every existing key contributes once to recall and return. Within a key, every raw policy record has equal weight, including each `picked=[]` record as zero selected hits/return. If `h̄_k` is the record-averaged selected hits for key k, run recall is `sum_k h̄_k / sum_k n_crit,k` (a ratio of sums), **not** `mean_k(h̄_k/n_crit,k)`; keys with more critical opportunities therefore have greater weight. Citation return is the equal-key mean of within-key attempt-mean contrasts. This gives complete existing-key support but estimates a recorded-attempt mean; it does not identify the historically correct attempt. Paired sign is not applicable to fractional means.

| Family | n recall / return / sign | sum n_crit | Selected recall | Parametric recall | Δrecall [95% run CI] | Δcitation return [95% run CI] |
|---|---:|---:|---:|---:|---:|---:|
| O | 26996 / 26996 / NA | 25527 | 0.443161 [0.432892, 0.453681] | 0.413441 [0.381007, 0.445307] | +0.029720 [-0.004409, +0.064360] | -0.181292 [-0.297932, -0.062012] |
| C | 26987 / 26987 / NA | 25556 | 0.532275 [0.525647, 0.539166] | 0.403215 [0.372917, 0.434296] | +0.129060 [+0.098475, +0.158255] | +0.662236 [+0.534883, +0.796727] |
| Q | 8998 / 8998 / NA | 8310 | 0.513909 [0.502175, 0.525385] | 0.403200 [0.369002, 0.433873] | +0.110709 [+0.080555, +0.144612] | +0.396418 [+0.258508, +0.521986] |
| G | 8989 / 8989 / NA | 8597 | 0.517008 [0.494626, 0.536723] | 0.430937 [0.374858, 0.485212] | +0.086071 [+0.019272, +0.144873] | -0.251347 [-0.457599, -0.062888] |

Family estimates are unweighted run means. Intervals are exploratory 10,000-draw whole-run percentile bootstrap intervals (seed 42); Q/G have only 10 runs. They omit corpus, duplicate-arbitration, missingness, and model-dependence uncertainty.

## 4. Conservative all-expected-key zero-empty/no-row sensitivity (`ALL_EXPECTED_RECORD_MEAN_ZERO_EMPTY_NO_ROW`)

This post-hoc descriptive convention extends the recorded-attempt mean to all 72,000 expected keys by assigning selected-proxy zero to the 30 no-row keys. It answers a different data-quality question from the existing-key caliber: what if absence of a record is treated as selection failure? It is not a recovered historical all-assigned analysis, not actual consumption, and not a prospective primary endpoint. Conflict records remain attempt means, as in the existing-key caliber; the conflict-refusing caliber below answers a separate question.

| Family | n recall / return / sign | sum n_crit | Selected recall | Parametric recall | Δrecall [95% run CI] | Δcitation return [95% run CI] |
|---|---:|---:|---:|---:|---:|---:|
| O | 27000 / 27000 / NA | 25530 | 0.443105 [0.432829, 0.453589] | 0.413405 [0.380933, 0.445290] | +0.029700 [-0.004409, +0.064344] | -0.182199 [-0.298424, -0.063222] |
| C | 27000 / 27000 / NA | 25560 | 0.532182 [0.525533, 0.539015] | 0.403169 [0.372829, 0.434271] | +0.129014 [+0.098454, +0.158164] | +0.657917 [+0.531025, +0.792166] |
| Q | 9000 / 9000 / NA | 8310 | 0.513909 [0.502175, 0.525385] | 0.403200 [0.369002, 0.433873] | +0.110709 [+0.080555, +0.144612] | +0.395332 [+0.257951, +0.520688] |
| G | 9000 / 9000 / NA | 8610 | 0.516255 [0.493673, 0.536152] | 0.430856 [0.374713, 0.485166] | +0.085398 [+0.018970, +0.144181] | -0.260004 [-0.462863, -0.072922] |

## 5. Conflict-refusing zero-empty sensitivity (`METRIC_RESOLVED_ZERO_EMPTY` = frozen G)

Empty-only keys are zero-filled. Nonempty duplicates enter a metric only when that metric's sufficient statistic is consistent; empty rows sharing a nonempty key do not create a new key or overwrite the nonempty Rule-A value. Exact recall/return/sign denominators are **71629 / 70732 / 71674**. The 30 no-row keys and each affected conflict remain excluded, not zero-filled.

| Family | n recall / return / sign | sum n_crit | Selected recall | Parametric recall | Δrecall [95% run CI] | Δcitation return [95% run CI] |
|---|---:|---:|---:|---:|---:|---:|
| O | 26919 / 26679 / 26929 | 25391 | 0.443505 [0.433152, 0.454117] | 0.413516 [0.381040, 0.445384] | +0.029989 [-0.004113, +0.064420] | -0.178179 [-0.295210, -0.058389] |
| C | 26859 / 26585 / 26877 | 25342 | 0.532409 [0.525719, 0.539301] | 0.403328 [0.372867, 0.434637] | +0.129080 [+0.098259, +0.158527] | +0.664627 [+0.535973, +0.800840] |
| Q | 8936 / 8753 / 8946 | 8199 | 0.514790 [0.502578, 0.526572] | 0.402854 [0.368220, 0.434133] | +0.111936 [+0.080700, +0.146579] | +0.409018 [+0.282964, +0.525141] |
| G | 8915 / 8715 / 8922 | 8469 | 0.518654 [0.496182, 0.538124] | 0.430575 [0.374569, 0.484674] | +0.088079 [+0.020790, +0.147295] | -0.237198 [-0.445377, -0.047897] |

Raw recomputation matches frozen scenario G for **80/80 runs** across denominators, sufficient sums, recall, and return (maximum absolute numeric error 9.71e-17).

## 6. Secondary existing calibers: nonempty Rule A versus strict singleton

These are existing frozen outputs, not replacements for the designated retrospective descriptive caliber. Rule A uses different resolved cohorts by metric: **71,573 recall, 70,676 return, 71,618 sign**. Strict singleton uses exactly one nonempty record per key and therefore a common **70,306-key** cohort. Their population difference prevents interpreting numerical changes as an isolated duplicate effect.

| Caliber | Family | n recall / return / sign | Selected recall | Parametric recall | Δrecall [CI] | Δcitation return [CI] |
|---|---|---:|---:|---:|---:|---:|
| RULE_A_NONEMPTY | O | 26908 / 26668 / 26918 | 0.443790 [0.433311, 0.454506] | 0.413620 [0.381320, 0.445497] | +0.030170 [-0.003971, +0.064767] | -0.175016 [-0.293452, -0.053577] |
| RULE_A_NONEMPTY | C | 26851 / 26577 / 26869 | 0.532600 [0.525874, 0.539520] | 0.403317 [0.372882, 0.434602] | +0.129283 [+0.098441, +0.158663] | +0.667380 [+0.539180, +0.802858] |
| RULE_A_NONEMPTY | Q | 8916 / 8733 / 8926 | 0.516153 [0.503543, 0.528210] | 0.403265 [0.368628, 0.434499] | +0.112887 [+0.081432, +0.147666] | +0.426727 [+0.295044, +0.548216] |
| RULE_A_NONEMPTY | G | 8898 / 8698 / 8905 | 0.519783 [0.497670, 0.539156] | 0.430371 [0.374549, 0.484268] | +0.089412 [+0.022924, +0.148522] | -0.219053 [-0.427112, -0.025626] |
| STRICT_SINGLETON_NONEMPTY | O | 26592 / 26592 / 26592 | 0.443873 [0.433436, 0.454659] | 0.413643 [0.381276, 0.445498] | +0.030230 [-0.004110, +0.064992] | -0.175557 [-0.293701, -0.054364] |
| STRICT_SINGLETON_NONEMPTY | C | 26499 / 26499 / 26499 | 0.531595 [0.524951, 0.538477] | 0.403450 [0.372918, 0.434844] | +0.128146 [+0.097421, +0.157488] | +0.663589 [+0.535146, +0.799188] |
| STRICT_SINGLETON_NONEMPTY | Q | 8641 / 8641 / 8641 | 0.517713 [0.504656, 0.529774] | 0.402091 [0.366588, 0.433916] | +0.115622 [+0.082768, +0.152260] | +0.420392 [+0.285632, +0.543034] |
| STRICT_SINGLETON_NONEMPTY | G | 8574 / 8574 / 8574 | 0.518663 [0.496025, 0.538126] | 0.429116 [0.373883, 0.482775] | +0.089547 [+0.021819, +0.149491] | -0.219101 [-0.425724, -0.026358] |

## 7. All 17 frozen scenarios: effect ranges and point-estimate sign changes

Ranges below use run-equal point estimates copied from `frozen_reanalysis_v1/summary.json`; no scenario was rerun or hidden. Sign change means a change in point-estimate sign across scenarios, not whether an interval contains zero.

| Family | Δrecall min–max | Δrecall sign changes | Δcitation return min–max | Return sign changes |
|---|---:|---:|---:|---:|
| O | +0.027697 to +0.033656 | 0 | -0.277317 to -0.103091 | 0 |
| C | +0.124652 to +0.133596 | 0 | +0.522966 to +0.749538 | 0 |
| Q | +0.104956 to +0.120525 | 0 | +0.159403 to +0.587765 | 0 |
| G | +0.079407 to +0.097947 | 0 | -0.507806 to -0.027918 | 0 |

For every family and both contrasts, the minimum occurs at `I_favor_param` and `J_lower_value`, and the maximum at `I_favor_llm` and `J_upper_value`. Recall stays positive in all 17 scenarios for every family. Citation return stays positive for C/Q and negative for O/G in all 17; there are **zero point-estimate sign changes**. This does not make the intervals or the causal interpretation uniformly robust.

All 68 scenario×family estimates, intervals, and exact metric denominators are in `scenario_effects.csv`; min/max scenario IDs and sign vectors are machine-readable in `summary.json`.

## 8. Prospective logging schema (not historical backfill)

`future_logging_schema.json` is a JSON Schema for one policy attempt with explicit attempt identity, parser/execution/transport status, empty-selection reason, and per-item **selected → delivered → opened → operational attendance** event objects. Attended is the single terminal consumption event and carries instrument/version, threshold, validation, blinding, and evidence fields. The registered primary outcome is all-assigned failure-composite omission; unknown raw attendance is not rewritten as observed non-consumption. The schema also requires explicit `calls`, `input_tokens`, `output_tokens`, `cost{amount,currency}`, `latency_ms`, and `retries`; unknown measurements are null, not zero.
The old replay fails the historical information requirement for this chain, so no synthetic old events or efficiency values are emitted.

## 9. Reproduction and files

```bash
PYTHONDONTWRITEBYTECODE=1 python3 sim/sea_pilot/audit_v110_consumption_caliber.py --write
```

Artifacts: `summary.json`, `REPORT.md`, per-run `run_metrics.csv`, all-scenario `scenario_effects.csv`, compressed unique-key `key_ledger.jsonl.gz`, prospective `future_logging_schema.json`, and hash-verified `input_manifest.json`. The ledger gives exact key status, conflict disposition, sources, and both new-caliber values without rationale text.

Interpretation remains post hoc and exploratory: one frozen 30-day corpus, retrospective citation labels, upstream digest conditioning, semi-oracle construction, possible nonrandom missingness, and confounded family/backend/prompt/runtime configurations. No result here measures delivered/opened/attended/actual consumption or human welfare.
