# SEA v1.17.1 — Mandatory Cohort Boundaries and Precise Statistical Scope

**Release status: candidate / prerelease.** This sanitized public snapshot responds to the v1.17.0 comprehensive review while preserving the conditional-framework/synthetic-artifact route. It makes the frozen cohort boundary commit-enforcing, clarifies the operational-bound sharpness and S12 statistical limits, strengthens the unexecuted real-evaluation protocol, and supplies a blank independent-review handoff. It is not independent human mathematical sign-off, validated measurement, a public experimental preregistration, third-party reproduction, or effectiveness evidence. The immutable `v1.17.0` tag is retained.

## Four distinct status categories

- **Code tests passed:** synthetic governance, executor, target-construction, mathematical, replay, financial, and caliber regressions.
- **Historical data recomputable:** frozen selected-proxy and financial artifacts can be rerun on pinned inputs; this is not structural-effect evidence.
- **Theory independently reviewed:** pending; the handoff is blank, not a signature.
- **System effectiveness validated:** not established.

## Paper and review artifacts

- English manuscript: `input/sovereign_epistemic_acquisition_EN_v1.17.md`
- Review PDF: `latex/SEA_EN_v1.17_draft.pdf`
- arXiv candidate source package: `latex/SEA_v1.17_arxiv_source.tar.gz`
- Chinese point-by-point response: `docs/审稿回复与修改说明_v1.17.md`
- Reproduction guide: `docs/REPRODUCIBILITY_v1.17.md`
- Unexecuted matched protocol: `docs/MINIMAL_VALID_EXPERIMENT_v1.17.md`
- Formal/technical supplement: `docs/SUPPLEMENT_FORMAL_AND_SECONDARY_v1.17.md`
- Retrospective audit supplement: `docs/SUPPLEMENT_RETROSPECTIVE_AUDITS_v1.17.md`
- Blank independent-review handoff: `docs/INDEPENDENT_REVIEW_HANDOFF_v1.17.md`
- Evidence status: `sim/pilot/results/evidence_status_v1.17.json`
- Final target-aware artifact hashes on main: `docs/工件清单_v1.17.{md,json}`

## Changes in v1.17.1

1. **Mandatory frozen cohort boundary.** After `switch_after_period=k`, the old cohort cannot skip the scheduled transition and commit period `k+1` (or a later legacy period). The rejection occurs before results, budget, history, or audit mutation. Declaration integrity is rechecked at every period commit, so outcome-motivated timing edits cannot reopen the old path. Late switch rejection remains as defense for legacy/deserialized states. The two-period guard/budget fixture now declares a single-version schedule; the separate two-version protocol demonstration exercises the transition. Executor/matched schemas are `/v7`, protocol-demo schema `/v4`; governance versions are unchanged.
2. **Exact period, cohort, reset, and measure semantics.** `next_period` is read-only and derived only after validating the committed sequence `0…N-1`; it is not an independent counter or an unchecked list length. Period indices are ordinal commits, not wall-clock duration or independent-environment evidence. The old cohort ends at `k`, the new begins at `k+1`, and each version’s `nu^(v)` is frozen before outcome unlock and only looked up at evaluation. A reset-target allowlist alone does not establish exogeneity: confirmatory reset additionally needs frozen trigger/timing and deterministic target selection; otherwise it starts an exploratory new experiment. Proposition 3.1 remains per control instance.
3. **Sharp operational contrast derivation.** Equation (6) now includes the per-arm identity `M_FC-M_Z=sum_unknown nu*1{Z=1}` and a joint endpoint-attainability proof. The bounds are sharp for operational attendance under the stated no-assumption model, not latent actual-consumption bounds.
4. **Precise S12 feasibility and uncertainty limits.** The supplement distinguishes exact population incompatibility (`1-se<=mZ<=sp` for positive Youden `J`), zero-denominator nonidentification (`J=0,N=0`) and no compatible population (`J=0,N!=0`), and finite-sample plug-in instability. The delta gradient is written as `J^-1(1-f,-f,1)`; `J^-2` is only a common scale, not a universal full divergence order when `N/J` varies. Delta variance is explicitly first-order, not exact finite-sample variance.
5. **No independence or calibration overclaim.** Zero covariances are only a zero-covariance approximation. PSD checks now state all normalized second- and third-order principal-minor conditions and their tolerance; PSD establishes algebraic admissibility, not accurate covariance estimation, transportability, or interval calibration. The shipped bootstrap jointly re-estimates only sensitivity/specificity with operational omission fixed; it is not a three-input bootstrap, and its percentile interval is conditional on nondegenerate replicates. Shared three-input estimation requires genuine joint resampling or full covariance.
6. **Cluster/multiplicity and preregistration requirements.** The unexecuted protocol requires an inferential interval family, simultaneous-confidence/multiplicity rules where applicable, design-consistent clustered intervals, small-stratum denominators/reasons, and no joint-map interpretation of marginal Wilson intervals. Public preregistration must include period-window maps, reset trigger/selection rules, corpus/code hashes, instrument validation, cluster/multiplicity plans, and power-simulation code/seeds/assumption grids with Monte Carlo error. Internal freezing remains distinct from public preregistration.
7. **Independent-review handoff, not sign-off.** `docs/INDEPENDENT_REVIEW_HANDOFF_v1.17.md` separates mathematical review, target/attendance validation, and third-party reproduction. It is blank and demands reviewer-generated counterexamples and exact commit/hash identification.
8. **v1.17.0 fixes retained.** Strict contiguous periods, duplicate/regressed/skipped-period rejection, structured zero-completion/single-class/missing-stratum diagnostics, joint covariance PSD checks, per-rate heterogeneity, and unit-level Wilson intervals are retained. The executor still has 49 tests; new assertions were added within existing tests rather than increasing the count. Title, abstract, claim matrix, and retrospective evidence positioning are unchanged.

## Reproduction and validation

Final author-run checks recorded 13/13 math/SAP tests, 100/100 sim tests (49 executor), 162/162 release-audit checks, a 22-page review/arXiv PDF with zero missing glyphs, 734/734 arXiv ancillary hashes, and 19/19 clean-public-copy verification groups. See `docs/REPRODUCIBILITY_v1.17.md` for commands and scope. Machine records are `tools/audit_v117_report.json`, `tools/pdf_layout_v1.17.json`, and `tools/clean_verification_v1.17.json`; the target-aware manifest records final file and tag hashes. All core audits are offline, make no LLM calls, and create no human data. Author-run clean-copy verification is not third-party reproduction, and test counts are not independent mathematical proof.

The package retains 292 main replay shards and 5 quarantined non-main JSONL files. The financial historical input remains the same 1,260-row CSV with SHA-256 `80e953d19efb44787d4fb8b03e37ee6cbfbfc325488769df8a0e89281b495024`; runtime Git is not required. No historical attendance, consumption, or efficiency fields were imputed.

## Public repositories and identifier boundary

- GitHub: https://github.com/hurrywhen/sea-nuaa
- Gitee: https://gitee.com/jiangsu-yunhefeng-intelligent_0/sea-nuaa
- Candidate tag: `v1.17.1`

The v1.7 Zenodo DOI does not cover v1.9–v1.17, including this patch. No v1.17-specific DOI or public experimental preregistration is asserted without a separate persistent record.

## Outstanding work

Independent human mathematical review; independent human target and attendance-instrument validation; third-party reproduction; public timestamped preregistration and power simulation; real matched S2d/S4/S5 experiments; independent temporal/post-cutoff/private corpora; point-in-time and memory audits; operational-consumption and efficiency observations; human data where human claims are intended; tagged PDF accessibility; and a v1.17-specific DOI. Code is MIT licensed; paper text and data are CC BY 4.0.
