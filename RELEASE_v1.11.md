# SEA v1.11.0 — Minor Revision: Caliber, Measurement, and Protocol Closure

**Release status: candidate / prerelease.** This sanitized public snapshot responds to the “minor revision before further review” assessment of v1.10.0 (`817de9839d4bcc9446d39e631b14ab1c387ad0bd`). It preserves the conditional-component/governance-audit route. It is not independent human mathematical sign-off, a globally solved SAP, an end-to-end effectiveness experiment, a public experimental preregistration, or human-validation evidence.

## Paper and review artifacts

- English manuscript: `input/sovereign_epistemic_acquisition_EN_v1.11.md`
- Review PDF: `latex/SEA_EN_v1.11_draft.pdf`
- arXiv candidate source package: `latex/SEA_v1.11_arxiv_source.tar.gz`
- Chinese point-by-point response: `docs/审稿回复与修改说明_v1.11.md`
- Reproduction guide: `docs/REPRODUCIBILITY_v1.11.md`
- Unexecuted matched protocol: `docs/MINIMAL_VALID_EXPERIMENT_v1.11.md`
- Deferred proofs and secondary tables: `docs/SUPPLEMENT_FORMAL_AND_SECONDARY_v1.11.md`
- Normative/transfer supplement: `docs/SUPPLEMENT_NORMATIVE_AND_TRANSFER_v1.11.md`
- Narrative literature/search record: `docs/LITERATURE_SEARCH_v1.11.md`
- Evidence status: `sim/pilot/results/evidence_status_v1.11.json`
- Final target-aware artifact hashes on main: `docs/工件清单_v1.11.{md,json}`

## Minor-revision changes

1. **Mathematical wording corrected.** The non-composition example now states that \(17/22\approx77.27\%\) exceeds the 75% worst-case two-step greedy guarantee but remains below the optimum 22. The guarantee is not violated; joint optimality still fails. Proposition 3.1 now restricts conditional rewards and observation kernels to positive-probability support and assigns arbitrary feasible actions at zero-probability histories.
2. **Retrospective “ITT” names removed.** `ALL_EXISTING_RECORD_MEAN_ZERO_EMPTY` is the designated retrospective descriptive caliber; `METRIC_RESOLVED_ZERO_EMPTY` is the conflict-refusing caliber. Historical outputs no longer emit the old identifiers. Input-only aliases remain in code for compatibility, and 320/320 run-metric rows were verified numerically unchanged after label normalization.
3. **Attendance measurement is operationalized.** Future domains must freeze an instrument registry, raw-event schema, validated thresholds, validation-set hash, alternative instruments, and assessor blinding before outcome unblinding. Digital text uses a validated reading event plus active content-linked confirmation or a task operation; machine consumption is measured and reported separately from human attention. Failed measurement remains `unknown`.
4. **One primary missing-outcome rule.** The sole prospective primary outcome is all-assigned failure-composite weighted omission of confirmed actual consumption. Valid positive attendance is success; explicit abstention, observed non-attendance, and unknown terminal outcomes are omission under the frozen primary rule. Best-case coding, arm-aware inverse-probability weighting, and separately justified preregistered multiple imputation are sensitivity analyses only. Failure coding is not claimed to make between-arm contrasts uniformly conservative.
5. **Algorithm 1 complexity decomposed.** Sorting is only \(O(n\log n)\). Association traversal and target initialization use \(L_\kappa=\sum_i|\kappa(x_i)|\); linking, scoring, subset selection, canonical audit bytes, persistence, and model/tool costs are reported separately. Exact subset enumeration, greedy variants, and knapsack algorithms receive no false shared polynomial bound.
6. **Main line shortened.** The manuscript retains 11 numbered tables, three figures, and 11 numbered equations. Online-threshold, EIG, and KL-choice proofs plus complete Rule A and strict-singleton tables move to the supplementary appendix. Reproduction commands remain only in the reproduction guide. Duplicate Jaccard/agenda appendix entries are removed, and PDF Author metadata is populated.
7. **Provenance made explicit.** The final manifest records `target_tag`, `target_commit`, `target_tag_object`, and local tag-peeling verification. It is generated after the annotated content tag exists and is then added in a separate provenance-only commit on main; the tag is never moved. This avoids treating a previous HEAD plus a dirty tree as the release target.

## Designated retrospective descriptive result (selected proxy only)

`ALL_EXISTING_RECORD_MEAN_ZERO_EMPTY` covers 71,970 existing keys, assigns selected-proxy zero to empty picks, and leaves 30 no-row keys missing. It is a recorded-attempt mean, not an intention-to-treat or actual-consumption analysis.

| Family | Existing keys | Δrecall [exploratory run-level interval] | Δcitation return |
|---|---:|---:|---:|
| O | 26,996 | +0.029720 [−0.004409, +0.064360] | −0.181292 |
| C | 26,987 | +0.129060 [+0.098475, +0.158255] | +0.662236 |
| Q | 8,998 | +0.110709 [+0.080555, +0.144612] | +0.396418 |
| G | 8,989 | +0.086071 [+0.019272, +0.144873] | −0.251347 |

These are post-hoc recorded-attempt means on one shared retrospective corpus. They do not measure actual consumption, independent-environment uncertainty, decision utility, welfare, or SEA's structural effect. `METRIC_RESOLVED_ZERO_EMPTY` retains 71,629/70,732/71,674 recall/citation-return/sign keys; Rule A and strict-singleton use their distinct secondary populations.

## Reproduction and validation

See `docs/REPRODUCIBILITY_v1.11.md` for commands, dependencies, frozen-input hashes, no-Git financial checks, and clean-snapshot verification. The release gate covers 13 mathematical/SAP tests, 42 governance/replay/financial/caliber tests, deterministic data-audit regeneration, manuscript/artifact consistency, JSON Schema validation, PDF text/layout/metadata checks, XeLaTeX missing-character checks, and arXiv attachment hashes. Final author-run clean-public verification completed 17/17 command groups with 112/112 release checks, a 39-page PDF, and 716/716 arXiv attachment hashes. Exact counts and hashes are recorded in `tools/audit_v111_report.json`, `tools/clean_verification_v1.11.json`, and the target-aware manifest. All core audits are offline, make no LLM calls, and create no human data. Author-run verification is not third-party reproduction.

The package retains 292 main replay shards and 5 quarantined non-main JSONL files. The financial historical input remains the same 1,260-row CSV with SHA-256 `80e953d19efb44787d4fb8b03e37ee6cbfbfc325488769df8a0e89281b495024`; runtime Git is not required.

## Public repositories and identifier boundary

- GitHub: https://github.com/hurrywhen/sea-nuaa
- Gitee: https://gitee.com/jiangsu-yunhefeng-intelligent_0/sea-nuaa
- Candidate tag: `v1.11.0`

The v1.7 Zenodo version DOI `10.5281/zenodo.23620920` and concept DOI `10.5281/zenodo.23620919` are historical and do not cover v1.9, v1.10, or v1.11. No v1.11-specific DOI is asserted unless a separate persistent record is actually created.

## Outstanding work

Independent human mathematical review; S2d/S4/S5 and matched ablations; independent temporal/post-cutoff/private corpora; strict point-in-time and memory audits; new actual-consumption and efficiency observations; public experimental preregistration; third-party clean-environment reproduction; and human data for any human claim. None is a hidden completed result of this minor revision. Code is MIT licensed; paper text and data are CC BY 4.0.
