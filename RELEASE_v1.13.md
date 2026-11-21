# SEA v1.13.0 — Operational Bounds, Ledger Separation, and Executor Semantics

**Release status: candidate / prerelease.** This sanitized public snapshot responds to the v1.12 comprehensive review. It corrects the overreaching latent-omission bound, separates theoretical and executable ledgers, synchronizes supplements and notation, and fixes longitudinal executor semantics. It is not independent human mathematical sign-off, a validated deployed system, a public experimental preregistration, or human-validation evidence.

## Four distinct status categories

- **Code tests passed:** synthetic governance, executor, target-construction, mathematical, replay, financial, and caliber regressions.
- **Historical data recomputable:** frozen selected-proxy and financial artifacts can be rerun on pinned inputs; this is not structural-effect evidence.
- **Theory independently reviewed:** pending.
- **System effectiveness validated:** not established.

## Paper and review artifacts

- English manuscript: `input/sovereign_epistemic_acquisition_EN_v1.13.md`
- Review PDF: `latex/SEA_EN_v1.13_draft.pdf`
- arXiv candidate source package: `latex/SEA_v1.13_arxiv_source.tar.gz`
- Chinese point-by-point response: `docs/审稿回复与修改说明_v1.13.md`
- Reproduction guide: `docs/REPRODUCIBILITY_v1.13.md`
- Unexecuted matched protocol: `docs/MINIMAL_VALID_EXPERIMENT_v1.13.md`
- Formal/technical supplement: `docs/SUPPLEMENT_FORMAL_AND_SECONDARY_v1.13.md`
- Retrospective audit supplement: `docs/SUPPLEMENT_RETROSPECTIVE_AUDITS_v1.13.md`
- Evidence status: `sim/pilot/results/evidence_status_v1.13.json`
- Final target-aware artifact hashes on main: `docs/工件清单_v1.13.{md,json}`

## Substantive changes

1. **Formula (6) corrected.** The sharp unknown-extreme bounds now concern **operational attendance omission** $\mathcal M_\nu^Z$, not latent actual-consumption omission $\mathcal M_\nu$. The manuscript and protocol give a no-unknown false-positive/false-negative counterexample showing why latent bounds require measurement-consistency assumptions. The executor bound function, docstring, and tests are updated.
2. **Three ledgers separated.** The theoretical ledger terminates in latent $D_S$; the executable operational/FC ledger terminates in valid positive operational attendance and preserves unknowns. The executor no longer claims to implement the latent partition.
3. **Notation unified.** Source coverage is $G_i(e)$; operational attendance is $Z_i(e)$; latent consumption is $\Gamma_i/D$; coverage probability is $c_e(S)$; KKT shadow price is $\lambda_B$. The five scoring coordinates are `relevance/novelty/credibility/durability/harm_avoidance`. Supplements are synchronized: independent SD result numbering (SD.1–SD.10), S-prefix equation tags, SD-prefixed supplementary tables, N1–N5 normative sections, and an explicit two-ledger decomposition in SD.3.4 with a measurement-consistency note for the Clopper–Pearson statement.
4. **Unified references.** The main reference list now has 52 entries covering main-text and supplement citations, including Resnick, Karush, Kuhn–Tucker, Charnov, Savage, and statistical references; an automated check verifies every entry is actually cited in the manuscript or a supplement.
5. **Executor semantics fixed.** `first_available_period` is persistent and filters longitudinal availability. SEA selection uses `staged_link_pass`; evaluation uses arm-independent `reference_link_truth`. A whole-period resource precheck and structural terminal-plan validation run before mutation. Control continuity and evaluation cohorts are separated; full reset is an optional protocol choice. The machine predicate is explicitly a synthetic placeholder. Hash body uses `sequence`, and operation is the guard scope. Misclassification counterexample tests cover both false-positive and false-negative directions.
6. **Future schema updated.** The prospective schema is `/v4` with `ALL_ASSIGNED_FAILURE_COMPOSITE_OPERATIONAL_ATTENDANCE_OMISSION_V1`, explicit AND attendance, and separate machine-event terminology.
7. **Editorial.** Title now reflects a conditional framework and synthetic audit artifacts; abstract shortened; Part II added; separate TOC page removed; Algorithm 1 kept together; Table 1 negative cells narrowed to NC/NI reviewed-source claims.

## Reproduction and validation

See `docs/REPRODUCIBILITY_v1.13.md`. Exact final counts and hashes are recorded in `tools/audit_v113_report.json`, `tools/clean_verification_v1.13.json`, and the target-aware manifest. All core audits are offline, make no LLM calls, and create no human data. Author-run verification is not third-party reproduction.

The package retains 292 main replay shards and 5 quarantined non-main JSONL files. The financial historical input remains the same 1,260-row CSV with SHA-256 `80e953d19efb44787d4fb8b03e37ee6cbfbfc325488769df8a0e89281b495024`; runtime Git is not required.

## Public repositories and identifier boundary

- GitHub: https://github.com/hurrywhen/sea-nuaa
- Gitee: https://gitee.com/jiangsu-yunhefeng-intelligent_0/sea-nuaa
- Candidate tag: `v1.13.0`

The v1.7 Zenodo DOI does not cover v1.9–v1.13. No v1.13-specific DOI is asserted without a separate persistent record.

## Outstanding work

Independent human mathematical review; independent human target and attendance-instrument validation; third-party reproduction; real matched S2d/S4/S5 experiments; independent temporal/post-cutoff/private corpora; point-in-time and memory audits; new operational-consumption and efficiency observations; public preregistration; human data; and a v1.13 DOI. Code is MIT licensed; paper text and data are CC BY 4.0.
