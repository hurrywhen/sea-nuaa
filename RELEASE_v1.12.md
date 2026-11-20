# SEA v1.12.0 — Major Revision: Framework Focus, Executor Alignment, and Measurement Closure

**Release status: candidate / prerelease.** This sanitized public snapshot responds to the “major revision before further review” assessment of v1.11.0. It narrows the paper to a conditional framework plus two checkable artifacts, aligns the formal model with a minimal longitudinal executor, closes measurement and missing-outcome definitions, and moves retrospective effect-like numbers out of the main text. It is not independent human mathematical sign-off, a globally solved SAP, a validated deployed system, a public experimental preregistration, or human-validation evidence.

## Four distinct status categories

- **Code tests passed:** synthetic governance, executor, target-construction, mathematical, replay, financial, and caliber regressions.
- **Historical data recomputable:** frozen selected-proxy and financial artifacts can be rerun on pinned inputs; this is not structural-effect evidence.
- **Theory independently reviewed:** pending. AI-assisted derivation and automated checks are not independent human mathematical review.
- **System effectiveness validated:** not established. No real matched S2d/S4/S5 deployment experiment or human outcome study is reported.

## Paper and review artifacts

- English manuscript: `input/sovereign_epistemic_acquisition_EN_v1.12.md`
- Review PDF: `latex/SEA_EN_v1.12_draft.pdf`
- arXiv candidate source package: `latex/SEA_v1.12_arxiv_source.tar.gz`
- Chinese point-by-point response: `docs/审稿回复与修改说明_v1.12.md`
- Reproduction guide: `docs/REPRODUCIBILITY_v1.12.md`
- Unexecuted matched protocol: `docs/MINIMAL_VALID_EXPERIMENT_v1.12.md`
- Formal/technical supplement: `docs/SUPPLEMENT_FORMAL_AND_SECONDARY_v1.12.md`
- Retrospective audit supplement: `docs/SUPPLEMENT_RETROSPECTIVE_AUDITS_v1.12.md`
- Normative/transfer supplement: `docs/SUPPLEMENT_NORMATIVE_AND_TRANSFER_v1.12.md`
- Evidence status: `sim/pilot/results/evidence_status_v1.12.json`
- Final target-aware artifact hashes on main: `docs/工件清单_v1.12.{md,json}`

## Substantive changes

1. **Contribution narrowed.** The abstract and Section 1.2 now state one conditional SAP framework and two artifacts: governance/executor reference and falsifiable audit/future-evaluation specification. Standard results are demoted to conditional technical foundations.
2. **Minimal longitudinal executor added.** `sim/sea_sap/executor.py` runs a synthetic fixture through target registry, reference availability, one update kernel, linkage, ranking, resource-feasible selection, delivery, opening, operational attendance, five resource budgets, guard write/rollback, target-level omission ledger, and domain-separated hash audit. A matched S2/S2d implementation fixture uses the same mock scorer/input/budget and is explicitly not an effectiveness experiment.
3. **Governance defects fixed.** Authorization now binds actor to principal, operation, exact proposal, current version token, single-use ID, and monotonic structural timestamp. The hash specification matches the code’s domain-separated canonical body and `previous_hash`, not recursive record embedding. The five scoring coordinates are aligned to `relevance`, `novelty`, `credibility`, `durability`, `harm_avoidance`.
4. **Measurement closed.** Latent actual consumption, operational attendance, and failure-composite omission use distinct symbols. Digital-text attendance is an explicit AND of valid reading and content-linked confirmation/task operation. Machine events are `machine_ingestion_and_task_reference`, not human attention or downstream information use. Target construction, reference availability, merge/split sensitivity, and dynamic target-version rules are specified; independent human target validation remains pending.
5. **Contrast bounds added.** The protocol reports both arm-specific unknown extremes: lower $\Delta^{FC}-u_{sea}$ and upper $\Delta^{FC}+u_{control}$ for SEA-minus-control latent omission. Missingness must be published by arm, stage, and reason.
6. **Retrospective numbers moved.** The main text keeps the evidence matrix, key flow, three caliber populations, and one financial falsification example. Family estimates, dispersion, sign counts, bootstrap intervals, Rule A, strict-singleton, 17 scenarios, and citation-return decompositions are in the retrospective supplement. A new conservative `ALL_EXPECTED_RECORD_MEAN_ZERO_EMPTY_NO_ROW` caliber covers all 72,000 expected keys.
7. **Main text compressed.** The v1.12 main manuscript is substantially shorter than v1.11, with 7 tables, 2 figures, 7 numbered equations, and 39 verified references. Standard proofs and numerical tables are moved to supplements.
8. **Version hygiene.** Historical manuscripts and PDFs are marked superseded in `archive/README.md`; the current authoritative entry is v1.12. The historical v1.7 DOI does not cover v1.9–v1.12.

## Reproduction and validation

See `docs/REPRODUCIBILITY_v1.12.md` for commands, dependencies, frozen-input hashes, no-Git financial checks, and clean-snapshot verification. Final author-run clean-public verification completed 18/18 command groups with 93/93 release checks, a 19-page PDF, and 729/729 public arXiv attachment hashes. Exact counts and hashes are recorded in `tools/audit_v112_report.json`, `tools/clean_verification_v1.12.json`, and the target-aware manifest. All core audits are offline, make no LLM calls, and create no human data. Author-run verification is not third-party reproduction.

The package retains 292 main replay shards and 5 quarantined non-main JSONL files. The financial historical input remains the same 1,260-row CSV with SHA-256 `80e953d19efb44787d4fb8b03e37ee6cbfbfc325488769df8a0e89281b495024`; runtime Git is not required.

## Public repositories and identifier boundary

- GitHub: https://github.com/hurrywhen/sea-nuaa
- Gitee: https://gitee.com/jiangsu-yunhefeng-intelligent_0/sea-nuaa
- Candidate tag: `v1.12.0`

The v1.7 Zenodo version DOI `10.5281/zenodo.23620920` and concept DOI `10.5281/zenodo.23620919` are historical and do not cover v1.9, v1.10, v1.11, or v1.12. No v1.12-specific DOI is asserted unless a separate persistent record is actually created.

## Outstanding work

Independent human mathematical review; independent human target validation; third-party clean-environment reproduction; real matched S2d/S4/S5 and ablations; independent temporal/post-cutoff/private corpora; strict point-in-time and memory audits; new operational-consumption and efficiency observations; public experimental preregistration; and human data for any human claim. None is a hidden completed result of this revision. Code is MIT licensed; paper text and data are CC BY 4.0.
