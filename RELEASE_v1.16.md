# SEA v1.16.0 — Frozen Switch Timing, Declared Reset Exception, and Precise Rejection Semantics

**Release status: candidate / prerelease.** This sanitized public snapshot responds to the v1.15.0 comprehensive review ("minor revision then re-review"). It completes three precise corrections—accurately describing the state changed by a rejection log, freezing the switch timing and the full-reset exception, and fixing the reproduction command—and implements the codeable P1 statistical details (covariance-aware / joint-bootstrap S12 uncertainty, stratified transportability and completion-representativeness diagnostics). It is not independent human mathematical sign-off, a validated deployed system, a public experimental preregistration, or human-validation evidence.

## Four distinct status categories

- **Code tests passed:** synthetic governance, executor, target-construction, mathematical, replay, financial, and caliber regressions.
- **Historical data recomputable:** frozen selected-proxy and financial artifacts can be rerun on pinned inputs; this is not structural-effect evidence.
- **Theory independently reviewed:** pending.
- **System effectiveness validated:** not established.

## Paper and review artifacts

- English manuscript: `input/sovereign_epistemic_acquisition_EN_v1.16.md`
- Review PDF: `latex/SEA_EN_v1.16_draft.pdf`
- arXiv candidate source package: `latex/SEA_v1.16_arxiv_source.tar.gz`
- Chinese point-by-point response: `docs/审稿回复与修改说明_v1.16.md`
- Reproduction guide: `docs/REPRODUCIBILITY_v1.16.md`
- Unexecuted matched protocol: `docs/MINIMAL_VALID_EXPERIMENT_v1.16.md`
- Formal/technical supplement: `docs/SUPPLEMENT_FORMAL_AND_SECONDARY_v1.16.md`
- Retrospective audit supplement: `docs/SUPPLEMENT_RETROSPECTIVE_AUDITS_v1.16.md`
- Evidence status: `sim/pilot/results/evidence_status_v1.16.json`
- Final target-aware artifact hashes on main: `docs/工件清单_v1.16.{md,json}`

## Substantive changes

1. **Precise rejection state effect (P0-1).** Because the audit ledger $L_t$ is part of the SAP state, a rejected transition is no longer described as "zero state mutation." The registry, objective store, budget, and active path are unchanged; the only state change is one appended rejection audit record, with zero resource spend. The payload replaces `state_mutated=False` with `registry_objective_budget_mutated=False`, `active_path_mutated=False`, `rejection_audit_record_appended=True`, `resources_spent=0`. Main text, supplement SA.0, protocol, tests, and the demonstration are synchronized.
2. **Frozen switch timing (P0-2).** The protocol declaration adds `protocol_switch_timing` (`switch_after_period` per scheduled successor), fixed before any arm result is read. A continuity transition is accepted only when exactly the declared number of periods has completed; early/late attempts are rejected (`switch_timing_mismatch`). A declaration-integrity hash rejects any post-result edit of the family/schedule/timing/reset allowlist/frozen content (`protocol_declaration_tampered`). New negative tests and demonstration probes cover early, late, and outcome-motivated timing edits. The protocol lists switch timing as a required public-preregistration field.
3. **Declared full-reset exception (P0-3).** Continuity transitions strictly advance along the schedule; a full reset is an independent-control-instance exception that selects a pre-declared allowed reset target (`protocol_reset_targets`, including backward versions or family members outside the parent schedule) and generates a fresh independent single-version schedule, sealing the parent. A backward reset is a new control instance, never a registry rollback of the sealed path. Undeclared reset targets are rejected (`reset_target_not_declared`). Main text, supplement, protocol, code, tests, and a backward-reset demonstration are consistent.
4. **Reproduction command fix (P0-4).** `docs/REPRODUCIBILITY_v1.16.md` §6 uses `tools/make_v116_manifest.py` (the v1.15 guide mistakenly named `make_v114_manifest.py`); environment variables, tag, and target-commit notes all point to v1.16. The release audit adds a regression string check.
5. **Dependent-input S12 uncertainty (P1-1).** The delta-method helper accepts all three covariance terms (zero = independent, flagged; negative implied variance rejected). A new joint/cluster bootstrap resamples paired validation records, re-estimating sensitivity/specificity together to preserve same-validation-set dependence; degenerate replicates are reported, never silently dropped; $m^Z$ from a separate deployment sample is held fixed. Supplement adds the full covariance expansion; protocol §1.4.1 forbids defaulting to independence for shared/clustered samples.
6. **Testable transportability and representativeness (P1-2).** New stratified diagnostics report stratum-specific error rates, pooled-deviation heterogeneity warnings, not-estimable strata, completion rates, completed-subset share shifts, and validation-vs-deployment completion gaps (including one-sided missing strata); a pre-specified sensitivity grid reports inadmissible cells and the transported range without truncation. Both are framed as supporting—but never proving—transportability. Protocol §1.4.1 makes them mandatory reporting.
7. **Editorial (P2).** Title, abstract, and evidence-matrix positioning unchanged; no defensive expansion. Pagination remains 21 pages with the references page filled and Tables 6/7 whole on the final page (no orphan row). Tagged PDF and a v1.16 DOI remain honestly pending.

## Reproduction and validation

See `docs/REPRODUCIBILITY_v1.16.md`. Exact final counts and hashes are recorded in `tools/audit_v116_report.json`, `tools/clean_verification_v1.16.json`, and the target-aware manifest. All core audits are offline, make no LLM calls, and create no human data. Author-run verification is not third-party reproduction.

The package retains 292 main replay shards and 5 quarantined non-main JSONL files. The financial historical input remains the same 1,260-row CSV with SHA-256 `80e953d19efb44787d4fb8b03e37ee6cbfbfc325488769df8a0e89281b495024`; runtime Git is not required.

## Public repositories and identifier boundary

- GitHub: https://github.com/hurrywhen/sea-nuaa
- Gitee: https://gitee.com/jiangsu-yunhefeng-intelligent_0/sea-nuaa
- Candidate tag: `v1.16.0`

The v1.7 Zenodo DOI does not cover v1.9–v1.16. No v1.16-specific DOI is asserted without a separate persistent record.

## Outstanding work

Independent human mathematical review (including the exogenous protocol registry semantics, frozen switch timing, declared reset exception, single-line lifecycle, dynamic-target closure, formula (6), and S12 transportability with the new covariance/bootstrap/stratified diagnostics); independent human target and attendance-instrument validation (protocol §1.4.1); third-party reproduction; real matched S2d/S4/S5 experiments; independent temporal/post-cutoff/private corpora; point-in-time and memory audits; new operational-consumption and efficiency observations; public preregistration; human data; tagged PDF accessibility; and a v1.16 DOI. Code is MIT licensed; paper text and data are CC BY 4.0.
