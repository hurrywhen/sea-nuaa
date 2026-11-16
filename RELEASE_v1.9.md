# SEA v1.9.0 — Conditional Design for Pull, Push, and Weighted Recall

**Release status: candidate / prerelease.** This is a sanitized public source-and-data snapshot for independent reading and computational checking. It is not a claim of independent human mathematical sign-off, end-to-end structural identification, or human effectiveness.

## Paper and source artifacts

- English manuscript: `input/sovereign_epistemic_acquisition_EN_v1.9.md`
- 32-page review PDF: `latex/SEA_EN_v1.9_draft.pdf`
- arXiv candidate source package: `latex/SEA_v1.9_arxiv_source.tar.gz`
- Chinese point-by-point response: `docs/审稿回复与修改说明_v1.9.md`
- Reproduction guide: `docs/REPRODUCIBILITY_v1.9.md`
- Proposed matched evaluation protocol: `docs/MINIMAL_VALID_EXPERIMENT_v1.9.md`
- Evidence status: `sim/pilot/results/evidence_status_v1.9.json`
- Working-artifact hashes: `docs/工件清单_v1.9.md` and `.json`

## Main revisions

1. Replaces the pooled pointwise recall narrative with weighted expected omission and an exact coverage–delivery identity, $m_e=1-\kappa_e\delta_e$.
2. Uses one misspecified update kernel for every signal, with $W(c,\hat c)=\mathrm{VOI}_c-\operatorname{Regret}_c(\hat c)$.
3. Separates population thresholds from finite top-$m$ order statistics, adds exact-formula finite-pool calculations and complete feasibility boundaries.
4. Corrects Pareto approximation, online-threshold boundaries, independent-subset bounds, KL-regularized fixed-capacity subset choice, EIG conditioning, and observable-history policy existence.
5. Reclassifies existing experiments as semi-oracle, retrospective, within-corpus mechanism checks. No 95% deployment guarantee or superiority to end-to-end LLM, RAG, or welfare-recommender baselines is claimed.

## New offline audits

- Financial caliber: historical 120/126 and expanded 121/133 agent–target evaluations; expanded 19 propositions on 18 company–days; company-day sensitivity 114/126; 7/7 budget alarms and 150 monthly slots in both $m=5$ configurations.
- Upstream digest: 80 model–seed configurations but 70 distinct complete digests; mean upstream opportunity shares 53.27%–55.19%.
- Citation-return decomposition: O/G critical-item point estimates rise but noncritical-item losses are larger; total citation-weighted return remains negative, and O's critical-item interval crosses zero.
- H8/H9: no model family is certified for human transfer.

## Validation at packaging

- 9 mathematical unit tests passed.
- 100/100 manuscript and artifact consistency checks passed.
- 32-page PDF text-layer check: no broken second-level headings.
- arXiv XeLaTeX check: 32 pages, zero missing-character warnings.
- 292 main replay shards plus 5 quarantined non-main JSONL files; `anc/SHA256SUMS` verifies.

## Public repositories

- GitHub: https://github.com/hurrywhen/sea-nuaa
- Gitee: https://gitee.com/jiangsu-yunhefeng-intelligent_0/sea-nuaa
- Tag: `v1.9.0`

The tag identifies the final public snapshot. The v1.7 Zenodo DOI (10.5281/zenodo.23620920) is historical and does not include v1.9. A v1.9 DOI is not asserted unless a separate persistent record is actually created.

## Outstanding work

Independent human mathematical review; S2d/S4/S5 and full matched ablations; independent temporal and post-cutoff/private corpora; anonymized memory and strict point-in-time audits; human data; and any subsequent persistent DOI registration. Code is MIT licensed; paper text and data are CC BY 4.0.
