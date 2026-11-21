# SEA v1.14.0 — Dynamic-Target Closure, Measurement Robustness, and Single-Source Materials

**Release status: candidate / prerelease.** This sanitized public snapshot is the minor revision responding to the v1.13.0 comprehensive review. It writes dynamic target versions into the formal SAP tuple, makes invalid attendance telemetry and late terminal-plan errors fail correctly before mutation, and gives every retrospective table exactly one authoritative source. It is not independent human mathematical sign-off, a validated deployed system, a public experimental preregistration, or human-validation evidence.

## Four distinct status categories

- **Code tests passed:** synthetic governance, executor, target-construction, mathematical, replay, financial, and caliber regressions.
- **Historical data recomputable:** frozen selected-proxy and financial artifacts can be rerun on pinned inputs; this is not structural-effect evidence.
- **Theory independently reviewed:** pending.
- **System effectiveness validated:** not established.

## Paper and review artifacts

- English manuscript: `input/sovereign_epistemic_acquisition_EN_v1.14.md`
- Review PDF: `latex/SEA_EN_v1.14_draft.pdf`
- arXiv candidate source package: `latex/SEA_v1.14_arxiv_source.tar.gz`
- Chinese point-by-point response: `docs/审稿回复与修改说明_v1.14.md`
- Reproduction guide: `docs/REPRODUCIBILITY_v1.14.md`
- Unexecuted matched protocol: `docs/MINIMAL_VALID_EXPERIMENT_v1.14.md`
- Formal/technical supplement: `docs/SUPPLEMENT_FORMAL_AND_SECONDARY_v1.14.md`
- Retrospective audit supplement: `docs/SUPPLEMENT_RETROSPECTIVE_AUDITS_v1.14.md`
- Evidence status: `sim/pilot/results/evidence_status_v1.14.json`
- Final target-aware artifact hashes on main: `docs/工件清单_v1.14.{md,json}`

## Substantive changes

1. **SAP tuple closed under dynamic targets (option B).** The tuple is defined per control instance with the active registry $R_t=(v_t,E_{v_t},\mathcal T_{v_t},A^{ref}_{v_t})$ in state, a finite ex-ante registry family, version switches as controlled transitions with cohort-boundary audit records, and a version-indexed evaluation measure $\nu^{(v)}$ chosen per cohort. The finite-history existence argument is unchanged (Supplement SA.0). The executor's continue/fork methods implement the controlled switch and optional full reset.
2. **Attendance measurement robustness.** Non-finite telemetry (NaN/±Inf), negative engaged time, coverage outside [0,1], non-Boolean flags, and empty evidence pointers now yield `unknown`, never positive or negative; thresholds are validated for finiteness and range at registration. The shipped registry object is explicitly a `synthetic_instrument_fixture`; claiming `validated` status requires the full preregistration fields (raw-event schema, validation-data and measurement-code hashes, measurement error, alternative instruments, arm-and-model blinding) and is rejected otherwise.
3. **Pre-mutation terminal-plan feasibility.** A commit-free selection dry run (pure update/ranking/selection preview, no records, no spend) rejects delivered-but-not-selected plans before any state change; the resource precheck record is also appended only after all previews pass. Both failure paths leave zero audit records and zero resource deductions. New tests cover staged-link-failure and over-limit candidates.
4. **Single-source retrospective tables.** The duplicated SB.1–SB.3 tables are removed from the formal supplement; Rule A, strict-singleton, and 17-scenario tables live only in the retrospective supplement §R5, regenerated from frozen data files by `tools/make_retrospective_tables.py` and drift-checked by the release audit.
5. **Counterexample precision.** With no unknowns the operational bounds collapse to $[\Delta^{FC},\Delta^{FC}]$, and to $[0,0]$ only when additionally $\Delta^{FC}=0$; manuscript, protocol, tests, and evidence status are synchronized.
6. **Cohort attribution everywhere.** Every cohort-scoped audit event (precheck, dry run, observation, update, resource use, ranking, selection, period outcome, objective write/rollback) carries control-instance, evaluation-cohort, registry-version, and registry-hash fields; the cohort-change record carries old/new identities. A cross-version-switch test verifies partitioning without inference.
7. **Measurement-error validation plan.** Protocol §1.4.1 preregisters independent blinded reference sets, arm-specific sensitivity/specificity with intervals, AND-rule operational false-negative rates, arm-differential error margins, and the explicit-error-model transport identity (S12) in Supplement SD.3.4 as sensitivity analysis only. None of this is executed; it is a design obligation before outcome unlock.
8. **Availability expiry positive test.** `first_available_period` expiry now has a positive test (delayed document becomes available, linked, selected, delivered, opened, and positively attended) complementing the delayed-unavailability test.

## Reproduction and validation

See `docs/REPRODUCIBILITY_v1.14.md`. Exact final counts and hashes are recorded in `tools/audit_v114_report.json`, `tools/clean_verification_v1.14.json`, and the target-aware manifest. All core audits are offline, make no LLM calls, and create no human data. Author-run verification is not third-party reproduction.

The package retains 292 main replay shards and 5 quarantined non-main JSONL files. The financial historical input remains the same 1,260-row CSV with SHA-256 `80e953d19efb44787d4fb8b03e37ee6cbfbfc325488769df8a0e89281b495024`; runtime Git is not required.

## Public repositories and identifier boundary

- GitHub: https://github.com/hurrywhen/sea-nuaa
- Gitee: https://gitee.com/jiangsu-yunhefeng-intelligent_0/sea-nuaa
- Candidate tag: `v1.14.0`

The v1.7 Zenodo DOI does not cover v1.9–v1.14. No v1.14-specific DOI is asserted without a separate persistent record.

## Outstanding work

Independent human mathematical review (including the dynamic-target closure, formula (6), and CP measurement-consistency statements); independent human target and attendance-instrument validation (protocol §1.4.1); third-party reproduction; real matched S2d/S4/S5 experiments; independent temporal/post-cutoff/private corpora; point-in-time and memory audits; new operational-consumption and efficiency observations; public preregistration; human data; tagged PDF accessibility; and a v1.14 DOI. Code is MIT licensed; paper text and data are CC BY 4.0.