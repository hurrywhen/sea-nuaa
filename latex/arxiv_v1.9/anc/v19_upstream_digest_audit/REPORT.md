# Upstream digest opportunity audit

**Status: `POST_HOC_UPSTREAM_OPPORTUNITY_AUDIT__SEMI_ORACLE_WITHIN_CORPUS`.** No LLM calls.

All reconstructed Channel-II digests depend on citation counts captured in 2026. The experiment is therefore semi-oracle by construction, in addition to any unmeasured model-memory channel.

| Family | Runs | Targets reaching digest (min–max) | Mean targets / 52 | Mean upstream share |
|---|---:|---:|---:|---:|
| O | 30 | 25–32 | 28.3667 | 54.55% |
| C | 30 | 25–33 | 28.4000 | 54.62% |
| Q | 10 | 24–31 | 27.7000 | 53.27% |
| G | 10 | 27–32 | 28.7000 | 55.19% |

There are 80 model–seed configurations but only 70 distinct complete digest configurations. O and G share seeds 1–10, hence ten identical upstream digest pairs.

The recall endpoint in the main replay is conditional on these upstream opportunities. The upstream share is not a multiplicative correction factor for end-to-end recall without a separately frozen estimand.
