# SEA v1.15.0 — Exogenous Protocol Registry Governance and Single-Line Control

**Release status: candidate / prerelease.** This sanitized public snapshot responds to the v1.14.0 comprehensive review. Registry-version transitions are now explicitly **exogenous frozen evaluation-protocol events, not policy actions**, validated against an ex-ante finite registry family and ordered schedule; the control lifecycle is **single-line** (the predecessor path is sealed at every transition, with one unique shared budget and ledger); objective rollback never restores a registry version. Measurement transport gains validation-to-deployment transportability conditions, completion-subset representativeness, and a near-zero-denominator precision warning with sensitivity grid. It is not independent human mathematical sign-off, a validated deployed system, a public experimental preregistration, or human-validation evidence.

## Four distinct status categories

- **Code tests passed:** synthetic governance, executor, target-construction, mathematical, replay, financial, and caliber regressions.
- **Historical data recomputable:** frozen selected-proxy and financial artifacts can be rerun on pinned inputs; this is not structural-effect evidence.
- **Theory independently reviewed:** pending.
- **System effectiveness validated:** not established.

## Paper and review artifacts

- English manuscript: `input/sovereign_epistemic_acquisition_EN_v1.15.md`
- Review PDF: `latex/SEA_EN_v1.15_draft.pdf`
- arXiv candidate source package: `latex/SEA_v1.15_arxiv_source.tar.gz`
- Chinese point-by-point response: `docs/审稿回复与修改说明_v1.15.md`
- Reproduction guide: `docs/REPRODUCIBILITY_v1.15.md`
- Unexecuted matched protocol: `docs/MINIMAL_VALID_EXPERIMENT_v1.15.md`
- Formal/technical supplement: `docs/SUPPLEMENT_FORMAL_AND_SECONDARY_v1.15.md`
- Retrospective audit supplement: `docs/SUPPLEMENT_RETROSPECTIVE_AUDITS_v1.15.md`
- Evidence status: `sim/pilot/results/evidence_status_v1.15.json`
- Final target-aware artifact hashes on main: `docs/工件清单_v1.15.{md,json}`

## Substantive changes

1. **Registry transitions are exogenous protocol events (review option A).** The policy action set no longer contains a registry-version switch. The evaluation protocol freezes ex ante a finite registry family $\mathfrak R$ (version→content-hash allowlist with frozen registry content) and an ordered version schedule; the executor accepts only the next scheduled member with a matching content hash. No objective-write authorization is required or meaningful for these events because they are outside the policy action space; protocol membership/schedule validation replaces authorization. Non-family (including the review's `unregistered-arbitrary-v999`), tampered-hash, backward/out-of-schedule, and sealed-path attempts are rejected with logged rejection records, zero state mutation, and zero resource spend.
2. **Single-line control lifecycle.** At a continuity transition the predecessor executor is sealed and can no longer run periods, write, roll back, or switch; the successor is the unique active path of the same control instance. Budget, history, period results, and the governance ledger are shared as one unique state, never copied into parallel branches. A full reset (fork) starts a new control instance with its own identity/budget/ledger and also seals its parent. New negative tests cover sealed-path reuse, and a dedicated protocol-transition demonstration artifact records all checks.
3. **Rollback/registry independence.** Objective rollback restores an objective version only; it never restores a registry version. Registry transitions are append-only forward along the schedule (no registry rollback). A post-switch rollback test verifies the registry version and hash are unchanged.
4. **S12 transportability and precision.** The supplement now states the validation-to-deployment conditional-stability assumptions for sensitivity and specificity, comparability and completion-subset representativeness requirements, remedies (covariate standardization, stratified estimation, preregistered error-rate sensitivity grid), and a precision warning when the Youden denominator $J_a=se_a+sp_a-1$ approaches zero (variance amplification $1/J_a^2$). Reference helpers `completed_measurement_transport` and `completed_measurement_transport_delta_method` implement the identity, warning, and independent-input delta-method propagation with numerical tests. Protocol §1.4.1 carries the corresponding preregistration obligations. None of this is executed measurement validation.
5. **Stricter `validated` instrument registration.** True 64-character lowercase hexadecimal hash checks (not length only), sensitivity/specificity intervals covering the point estimates, a declared transportability assumption, an independent blinded reference-set construction/data-hash/unlock record with a no-overlap declaration, and a completion-subset representativeness statement are now mandatory; missing or malformed fields reject registration. The shipped object remains explicitly a `synthetic_instrument_fixture`, never a validated instance.
6. **Symbol de-duplication.** Registry family $\mathfrak R=\{\rho^{(v)}\}$, active registry $\rho_t$, initial law $\mu_0$ (former $\rho_0$); objective version history keeps $\mathcal V_t$; the reflective principal keeps $R$ in Figure 1. The tuple's measure family is indexed by $\rho^{(v)}\in\mathfrak R$.
7. **Editorial.** Reference pagination optimized; the finite-history existence argument (Supplement SA.0) is restated for exogenous schedule-driven transitions (no switch action enters the attempt set). Tagged-PDF accessibility remains honestly pending.

## Reproduction and validation

See `docs/REPRODUCIBILITY_v1.15.md`. Exact final counts and hashes are recorded in `tools/audit_v115_report.json`, `tools/clean_verification_v1.15.json`, and the target-aware manifest. All core audits are offline, make no LLM calls, and create no human data. Author-run verification is not third-party reproduction.

The package retains 292 main replay shards and 5 quarantined non-main JSONL files. The financial historical input remains the same 1,260-row CSV with SHA-256 `80e953d19efb44787d4fb8b03e37ee6cbfbfc325488769df8a0e89281b495024`; runtime Git is not required.

## Public repositories and identifier boundary

- GitHub: https://github.com/hurrywhen/sea-nuaa
- Gitee: https://gitee.com/jiangsu-yunhefeng-intelligent_0/sea-nuaa
- Candidate tag: `v1.15.0`

The v1.7 Zenodo DOI does not cover v1.9–v1.15. No v1.15-specific DOI is asserted without a separate persistent record.

## Outstanding work

Independent human mathematical review (including the exogenous protocol registry semantics, single-line lifecycle, dynamic-target closure, formula (6), S12 transportability, and CP measurement-consistency statements); independent human target and attendance-instrument validation (protocol §1.4.1, including transportability and representativeness checks); third-party reproduction; real matched S2d/S4/S5 experiments; independent temporal/post-cutoff/private corpora; point-in-time and memory audits; new operational-consumption and efficiency observations; public preregistration; human data; tagged PDF accessibility; and a v1.15 DOI. Code is MIT licensed; paper text and data are CC BY 4.0.
