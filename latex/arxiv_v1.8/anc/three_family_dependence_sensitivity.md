# Three-family replay — dependence sensitivity

> Status: **POST_HOC_WITHIN_CORPUS_DEPENDENCE_SENSITIVITY**. This is a post-hoc, within-corpus sensitivity analysis,
> not a new confirmatory analysis and not evidence of transportability to other corpora or people.

## Reproduce

```bash
PYTHONDONTWRITEBYTECODE=1 python3 sim/sea_pilot/audit_three_family_dependence.py

# Write the two dedicated artifacts; existing files additionally require --force
PYTHONDONTWRITEBYTECODE=1 python3 sim/sea_pilot/audit_three_family_dependence.py --write
```

The script makes no LLM calls and does not alter replay JSONL or the frozen legacy outputs.
Each reported interval uses 10,000 percentile-bootstrap resamples, seed=20261103.
The honest arm is rebuilt offline by the original deterministic feature pipeline.

## Judgment minus semi-oracle parametric recall

| Family | Point estimate | Day-cluster 95% CI | Circular moving-block (5 days) 95% CI |
|---|---:|---:|---:|
| ornith30 | -0.047414 | [-0.250000, +0.168274] | [-0.196429, +0.113281] |
| gemma26na | +0.008621 | [-0.217596, +0.262511] | [-0.175785, +0.220021] |
| qwen38na | +0.064655 | [-0.164068, +0.302902] | [-0.088710, +0.236111] |
| qwen38b | +0.068966 | [-0.155427, +0.317571] | [-0.099138, +0.255220] |
| qwen38all | +0.066810 | [-0.159095, +0.309783] | [-0.090533, +0.244565] |

## Judgment minus honest-feature recall

| Family | Point estimate | Day-cluster 95% CI | Circular moving-block (5 days) 95% CI |
|---|---:|---:|---:|
| ornith30 | +0.215000 | [-0.004954, +0.432584] | [+0.039770, +0.364166] |
| gemma26na | +0.272727 | [+0.060224, +0.513891] | [+0.121208, +0.403143] |
| qwen38na | +0.271552 | [+0.049102, +0.489583] | [+0.102273, +0.410004] |
| qwen38b | +0.275862 | [+0.050000, +0.500000] | [+0.110577, +0.401054] |
| qwen38all | +0.273707 | [+0.052875, +0.491950] | [+0.107500, +0.402784] |

## Scope

- Day clusters keep every recorded agent row from the same simulated day together, preserving within-day and shared-digest dependence in each resample. The parametric recall contrast uses all recorded rows; the honest-feature paired contrast retains the legacy nonempty-`picked` caliber.
- Circular length-five moving blocks additionally retain short-range serial dependence across simulated days.
- These are sensitivity intervals, not independent-run intervals: each family has only 30 shared day clusters, and `qwen38all` pools two agent cohorts on those same days.
- Shared corpus, post-hoc labels, upstream digest construction, potential model memory, and cross-family dependence remain outside the resampling model.
- Legacy CMH/McNemar p-values must therefore be read as nominal within-corpus results under their stated stratification and dependence approximation, not as calibrated population error rates.
