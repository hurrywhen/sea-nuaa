# SEA v1.10.0 — Conditional Components, Governance Audits, and Weighted Omission

**Release status: candidate / prerelease.** This sanitized public snapshot responds to the v1.9 major-revision review. It is not independent human mathematical sign-off, a globally solved SAP, an end-to-end effectiveness experiment, or human-validation evidence.

## Paper and review artifacts

- English manuscript: `input/sovereign_epistemic_acquisition_EN_v1.10.md`
- Review PDF: `latex/SEA_EN_v1.10_draft.pdf`
- arXiv candidate source package: `latex/SEA_v1.10_arxiv_source.tar.gz`
- Chinese point-by-point response: `docs/审稿回复与修改说明_v1.10.md`
- Reproduction guide: `docs/REPRODUCIBILITY_v1.10.md`
- Unexecuted matched protocol: `docs/MINIMAL_VALID_EXPERIMENT_v1.10.md`
- Narrative literature/search record: `docs/LITERATURE_SEARCH_v1.10.md`
- Demoted normative/transfer supplement: `docs/SUPPLEMENT_NORMATIVE_AND_TRANSFER_v1.10.md`
- Evidence status: `sim/pilot/results/evidence_status_v1.10.json`
- Artifact hashes: `docs/工件清单_v1.10.{md,json}`

## Substantive revisions

1. **Conditional SAP closure.** The full tuple defines state, observations, attempted and feasible actions, transitions, rewards/harms, discount/horizon, five resource budgets, authorized writes, rollback, and observable histories. A component map, worked six-target pipeline, guarded-step algorithm, complexity statement, and 17-versus-22 non-composition example replace the former schematic overview. No joint optimality is claimed.
2. **Executable S1–S4 governance.** `sim/sea_governance/` provides deterministic reference behavior and 14 passing synthetic tests: unauthorized/stale writes rejected, objective bytes and exact ranking restored on rollback, fixed-supply invariance, separate supply-ecology records, hash-chain tamper/reorder/anchored-truncation detection, and contest/recourse linkage. These are not malicious-host security or human-control results.
3. **Consumption-aligned estimands.** Availability, linkage, selection, delivery, opening, and attendance are separate events. Historical `picked` is only a selected proxy; no delivered/opened/attended or efficiency values are backfilled.
4. **New historical robustness calibers.** `ITT_ALL_RECORD_MEAN` covers 71,970 existing keys with selected-proxy zero for empty records and 30 no-row keys left missing. G, Rule A, and strict-singleton use explicit 71,629/70,732/71,674, 71,573/70,676/71,618, and 70,306-key calibers. All 17 scenario ranges and a 72,000-key ledger are public.
5. **Financial public-reproduction fix.** The 1,260-row historical CSV is frozen at `sim/pilot/results/v19_financial_caliber_audit/historical_p2_rows_8ffc7f5.csv`, SHA-256 `80e953d19efb44787d4fb8b03e37ee6cbfbfc325488769df8a0e89281b495024`. Default audit reads and verifies this file without Git. Expanded parametric-S2p selections are reconstructed; historical S2p and both S2p-feat configurations remain frozen-row aggregates. The historical 4.6/day supply is an inherited constant, not a value verified from the pinned CSV.
6. **Theory wording and numbering.** Capacity leakage is a clairvoyant/oracle relaxation; Pareto leakage is normalized expected leaked value (a ratio of expectations); the monotonicity restriction has explicit universal quantifiers and algorithm-specific domains. Key equations are numbered (1)–(11), tables 1–15 have captions, and three figures cover SAP flow, staged omission, and identification.
7. **Literature and code synchronization.** Adds the original RAG paper, EMNLP Findings 2025 agent-recommender survey, a verified 2026 arXiv autonomy roadmap, RAG evaluation, and direct statistical-method sources. `sim/sea_algo` is explicitly a historical A1–A10 experiment suite; stale theorem-number references are removed.

## Principal new numerical sensitivity (selected proxy only)

| Family | Existing keys | Δrecall [exploratory run-level interval] | Δcitation return |
|---|---:|---:|---:|
| O | 26,996 | +0.029720 [−0.004409, +0.064360] | −0.181292 |
| C | 26,987 | +0.129060 [+0.098475, +0.158255] | +0.662236 |
| Q | 8,998 | +0.110709 [+0.080555, +0.144612] | +0.396418 |
| G | 8,989 | +0.086071 [+0.019272, +0.144873] | −0.251347 |

These are post-hoc recorded-attempt means on one shared retrospective corpus. They do not measure actual consumption, independent-environment uncertainty, decision utility, welfare, or SEA's structural effect.

## Reproduction and validation

See `docs/REPRODUCIBILITY_v1.10.md` for wrapped commands and dependency boundaries. The release requires mathematical/SAP regressions, 14 governance tests, replay and financial tests, deterministic audit regeneration, manuscript/artifact consistency, XeLaTeX missing-character checks, PDF text-layer checks, and coordinate-level page-overflow checks. Exact final counts and PDF hashes are recorded in `docs/工件清单_v1.10.json` and `tools/audit_v110_report.json`.

The package retains 292 main replay shards and 5 quarantined non-main JSONL files. A separate sanitized copy with no `.git` completed 17 verification command groups: 13 math/SAP tests, 37 governance/replay/financial tests, all data audits, 100/100 release checks, PDF/arXiv builds, and 714/714 public arXiv attachment hashes. Financial default and forced-write runs also passed with no Git executable in `PATH`; see `tools/clean_verification_v1.10.json`. No audit makes LLM calls or creates human data. Public snapshot verification by the authors is not third-party independent reproduction.

## Public repositories and identifier boundary

- GitHub: https://github.com/hurrywhen/sea-nuaa
- Gitee: https://gitee.com/jiangsu-yunhefeng-intelligent_0/sea-nuaa
- Candidate tag: `v1.10.0`

The v1.7 Zenodo version DOI `10.5281/zenodo.23620920` and concept DOI `10.5281/zenodo.23620919` are historical and do not cover v1.9 or v1.10. No v1.10-specific DOI is asserted unless a separate persistent record is actually created.

## Outstanding work

Independent human mathematical review; S2d/S4/S5 and matched ablations; independent temporal/post-cutoff/private corpora; strict point-in-time and memory audits; actual-consumption and efficiency observations in new matched runs; public experimental preregistration; third-party clean-environment reproduction; human data for any human claim; and any subsequent v1.10 DOI registration. Code is MIT licensed; paper text and data are CC BY 4.0.
