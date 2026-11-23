# SEA v1.17.0 — Strict Actual Periods and Structured Zero-Completion Diagnostics

**Release status: candidate / prerelease.** This sanitized public snapshot responds to the v1.16.0 comprehensive review ("minor revision then re-review"). It fixes the two executor boundary counterexamples identified by that review—duplicate periods could satisfy a frozen switch boundary, and zero completed measurements could suppress stratified diagnostics—and completes the codeable P1 statistical improvements. It is not independent human mathematical sign-off, a validated deployed system, a public experimental preregistration, or human-validation evidence.

## Four distinct status categories

- **Code tests passed:** synthetic governance, executor, target-construction, mathematical, replay, financial, and caliber regressions.
- **Historical data recomputable:** frozen selected-proxy and financial artifacts can be rerun on pinned inputs; this is not structural-effect evidence.
- **Theory independently reviewed:** pending.
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
- Evidence status: `sim/pilot/results/evidence_status_v1.17.json`
- Final target-aware artifact hashes on main: `docs/工件清单_v1.17.{md,json}`

## Substantive changes

1. **Strict contiguous actual periods (P0-1/P0-2).** `next_period` is a read-only value derived from the exact committed sequence $0,\ldots,N-1$, not an independently writable clock or an unchecked `len(period_results)`. `run_period` accepts only integer `period == next_period`; duplicate, regressed, skipped, Boolean, and noninteger periods are rejected before any state mutation. Continuity transitions share the sequence, while a full-reset instance starts at 0. Switch acceptance requires `next_period == switch_after_period + 1`. Repeating period 0 therefore cannot satisfy a period-1 boundary, and post-switch old periods remain invalid.
2. **Structured zero-completion diagnostics (P0-3/P0-4).** Completion reporting no longer depends on pooled error-rate estimability. With zero completions, overall completion is 0 and its interval remains available, assigned/completed/unknown counts are retained, completed-subset share shifts are `None/not_estimable`, sensitivity/specificity joint estimability is false, and completion/representativeness warnings carry `no_completed_measurements`. Undefined shifts and unavailable heterogeneity are never filled with zero. Single-truth-class, single-completed-stratum, fully unknown-stratum, and missing-stratum cases return explicit reasons.
3. **Joint covariance validity (P1-1).** Manual S12 covariance inputs now require a positive-semidefinite 3×3 matrix in addition to a finite nonnegative transported scalar variance. Checks use zero-variance row constraints and normalized pairwise/determinant conditions, preventing a large unrelated variance from hiding an illegal small subblock. Joint/cluster bootstrap remains the preferred alternative when manual covariance estimation is inappropriate.
4. **Small-sample uncertainty and per-rate heterogeneity (P1-2).** Sensitivity, specificity, and completion rates include counts, denominators, separate estimability flags, and unit-level Wilson 95% intervals. These intervals are not exact, cluster-adjusted, simultaneous, or joint S12 regions. Heterogeneity is computed separately for each rate only when at least two strata and the pooled rate are estimable; a one-stratum zero deviation is not cross-stratum evidence. Wilson (1927) was added as the sole new reference, verified through Crossref.
5. **Executable adversarial coverage and schemas.** The source suite currently contains 49 executor tests, including the duplicate-period attack, regression/skip/old-period rejection, clock/history integrity, zero completion, single truth class, missing strata, PSD joint counterexamples, and Wilson boundaries. The protocol demonstration includes the duplicate-period switch probe. Executor and matched outputs use schema `/v6`, and the protocol demonstration uses `/v3`; governance interface and audit schema versions are unchanged.
6. **Editorial scope (P2).** Title, abstract, claim matrix, and retrospective evidence positioning are unchanged. No new effectiveness, human-measurement, or deployment claim is introduced. Tagged PDF and a v1.17-specific DOI remain pending.

## Reproduction and validation

See `docs/REPRODUCIBILITY_v1.17.md`. Final checks recorded 13/13 math/SAP tests, 100/100 sim tests (49 executor), a 157/157 release audit, a 22-page review/arXiv PDF with zero missing glyphs, 733/733 arXiv ancillary hashes, and 19/19 author-run clean-public-copy verification groups. Machine records are `tools/audit_v117_report.json`, `tools/pdf_layout_v1.17.json`, and `tools/clean_verification_v1.17.json`; the target-aware manifest records final file and tag hashes. All core audits are offline, make no LLM calls, and create no human data. Author-run verification is not third-party reproduction.

The package retains 292 main replay shards and 5 quarantined non-main JSONL files. The financial historical input remains the same 1,260-row CSV with SHA-256 `80e953d19efb44787d4fb8b03e37ee6cbfbfc325488769df8a0e89281b495024`; runtime Git is not required.

## Public repositories and identifier boundary

- GitHub: https://github.com/hurrywhen/sea-nuaa
- Gitee: https://gitee.com/jiangsu-yunhefeng-intelligent_0/sea-nuaa
- Candidate tag: `v1.17.0`

The v1.7 Zenodo DOI does not cover v1.9–v1.17. No v1.17-specific DOI is asserted without a separate persistent record.

## Outstanding work

Independent human mathematical review (including strict actual-period semantics, frozen switching/reset lifecycle, formula (6), S12 covariance/PSD propagation, and zero-completion/Wilson diagnostics); independent human target and attendance-instrument validation (protocol §1.4.1); third-party reproduction; real matched S2d/S4/S5 experiments; independent temporal/post-cutoff/private corpora; point-in-time and memory audits; new operational-consumption and efficiency observations; public preregistration; human data; tagged PDF accessibility; and a v1.17 DOI. Code is MIT licensed; paper text and data are CC BY 4.0.
