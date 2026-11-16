#!/usr/bin/env python3
"""Focused consistency audit for the SEA v1.9 working manuscript and artifacts."""
from __future__ import annotations

import csv
import json
import math
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "input" / "sovereign_epistemic_acquisition_EN_v1.9.md"
REPORT = ROOT / "tools" / "audit_v19_report.json"


def main() -> int:
    checks = []

    def check(name: str, condition: bool, detail: str = "") -> None:
        checks.append({"name": name, "passed": bool(condition), "detail": detail})

    text = SRC.read_text(encoding="utf-8")
    body, tail = text.split("## References", 1)
    refs, _ = tail.split("## Appendix A", 1)
    abstract = text.split("## Abstract", 1)[1].split("**Keywords**", 1)[0]
    check("abstract_at_most_300_words", len(abstract.split()) <= 300, str(len(abstract.split())))
    check("substantially_shorter_than_v18", len(text.split()) < 15000, str(len(text.split())))
    check("no_continue_marker", "[[CONTINUE]]" not in text)
    check("balanced_display_math", text.count("$$") % 2 == 0)
    for phrase in ("added in v1.", "transcription error", "quota-feasible",
                   "becomes measurable on real data", "archived alternative route"):
        check(f"no_version_or_legacy_phrase:{phrase}", phrase not in text)
    for required in ("m_e(S):=P(\\operatorname{miss}_S(e))=1-\\kappa_e(S)\\delta_e(S)",
                     "Q_1(0.05)", "120/126", "121/133", "114/126",
                     "no existing family is certified for human transfer",
                     "independent human mathematical review remains pending"):
        check(f"required_text:{required[:48]}", required.lower() in text.lower())
    check("no_single_item_subset_inclusion_formula", "P(i \\in A) \\propto" not in text)
    check("no_mutual_information_noncapture_definition", "Idealized statement" not in text)

    # Every reference's first author should be visible in the body; this is a
    # deliberately simple guard, not a replacement for publisher-level citation checks.
    for para in refs.strip().split("\n\n"):
        first = para.split(",", 1)[0].strip()
        if first:
            check(f"reference_cited:{first}", first in body)

    math_results = json.loads((ROOT / "sim/theory_v1.9/math_results.json").read_text())
    check("math_dprime", math.isclose(
        math_results["gaussian_population"]["required_dprime"], 4.389337888, abs_tol=1e-8))
    pareto = math_results["pareto_alpha_1.5_K_52"]
    check("pareto_exact_m26", math.isclose(
        pareto["m_26"]["exact_leakage_share"], 0.20799886, abs_tol=1e-7))
    check("pareto_exact_m42", math.isclose(
        pareto["m_42"]["exact_leakage_share"], 0.06919112, abs_tol=1e-7))
    check("rct_one_primary_171", math_results["rct_sample_size"]
          ["one_declared_primary_comparison"]["ceiling_after_25_percent_attrition"] == 171)
    high = math_results["gaussian_population"]["high_budget_regression"]
    check("gaussian_high_budget_zero_separation", high["required_dprime_beta_0.9999"] == 0
          and high["required_dprime_beta_1"] == 0)
    check("gaussian_consume_all_recall", high["population_recall_beta_1"] == 1.0)
    check("online_boundary_delta_1_1", math_results["online_threshold_constant_reward"]["delta_1_1"] == 1.0)
    check("finite_grid_tail_metadata_nonzero", math_results["finite_topm_examples"][0]
          ["finite_topm"]["normal_tail_mass_outside_grid"] > 0)
    check("subset_choice_uses_KL_reference", "D_{\\mathrm{KL}}(p\\|\\pi^0)" in text)
    check("proper_independent_subset_is_upper_bound", "For a proper certified independent subset" in text)
    check("observable_history_not_latent_policy_input", "Latent states enter only transition and reward kernels" in text)

    fin = json.loads((ROOT / "sim/pilot/results/v19_financial_caliber_audit/summary.json").read_text())
    comp = fin["semi_oracle_configuration_comparison"]
    check("financial_old_120_of_126", comp["historical_m5"]["agent_target_hits"] == 120
          and comp["historical_m5"]["agent_target_opportunities"] == 126)
    check("financial_new_121_of_133", comp["expanded_m5"]["agent_target_hits"] == 121
          and comp["expanded_m5"]["agent_target_opportunities"] == 133)
    check("financial_company_day_114_of_126",
          fin["m5_pooled_across_runs"]["company_day"]["hits"] == 114
          and fin["m5_pooled_across_runs"]["company_day"]["opportunities"] == 126)
    check("financial_all_alarm", comp["historical_m5"]["budget_conflict_alarms"] == 7
          and comp["expanded_m5"]["budget_conflict_alarms"] == 7)
    check("financial_matrix_has_175_rows", sum(
        1 for _ in (ROOT / "sim/pilot/results/v19_financial_caliber_audit/critical_coverage_matrix.csv").open()) == 176)

    up = json.loads((ROOT / "sim/pilot/results/v19_upstream_digest_audit/summary.json").read_text())
    check("upstream_80_model_seed_70_digest", up["model_seed_configurations"] == 80
          and up["distinct_complete_digest_configurations"] == 70)
    check("upstream_52_targets", up["target_count"] == 52)
    with (ROOT / "sim/pilot/results/v19_upstream_digest_audit/run_upstream_coverage.csv").open(
            encoding="utf-8", newline="") as f:
        first_upstream = next(csv.DictReader(f))
    check("upstream_seed_mapping", first_upstream["run_seed"] == "1"
          and first_upstream["proxy_seed"] == "100")
    check("upstream_forced_lite", up["input_provenance"]["forced_lite_input"] is True)

    trade = json.loads((ROOT / "sim/pilot/results/v19_recall_value_tradeoff/summary.json").read_text())
    check("tradeoff_O_total_negative", trade["families"]["O"]["delta_return"]["run_equal_mean"] < 0)
    check("tradeoff_G_total_negative", trade["families"]["G"]["delta_return"]["run_equal_mean"] < 0)
    check("tradeoff_O_decomposition", math.isclose(
        trade["families"]["O"]["delta_critical_return"]["run_equal_mean"], 0.124007, abs_tol=1e-6))
    check("tradeoff_identity", all(v["identity_max_abs_error"] < 1e-9 for v in trade["families"].values()))
    check("tradeoff_scenario_C_regression", trade["validation"]
          ["scenario_C_80_of_80_recall_return_cellcount_match"] is True)
    check("financial_18_to_19_not_called_unit_mix", "mixes" not in fin["legacy_18_to_19_note"])

    evidence = json.loads((ROOT / "sim/pilot/results/evidence_status_v1.9.json").read_text())
    check("evidence_no_human_data", evidence["global_scope"]["human_subjects_data"] == "none")
    check("evidence_no_overall_effect", evidence["global_scope"]["overall_SEA_structural_effect_identified"] is False)
    check("evidence_math_review_pending", evidence["global_scope"]["independent_human_mathematical_review"] == "pending")
    check("evidence_public_candidate_release", evidence["global_scope"]["immutable_v1.9_public_release"]
          == "PUBLIC_CANDIDATE_TAG_v1.9.0__DOI_PENDING"
          and evidence["global_scope"]["public_tag"] == "v1.9.0")
    h8 = next(c for c in evidence["claims"] if c["id"] == "TRANSFER-H8-H9")["H8"]
    check("H8_direction_and_interval_correct", "negative across the three named families" in h8
          and "outside the target effect interval" in h8)
    check("no_H8_only_discrimination_description_overclaim", "only discrimination materials are useful" not in h8)

    pdf = ROOT / "latex/SEA_EN_v1.9_draft.pdf"
    if pdf.exists():
        info = subprocess.check_output(["pdfinfo", str(pdf)], text=True)
        pages = int(re.search(r"^Pages:\s+(\d+)", info, re.M).group(1))
        check("pdf_page_count_at_most_40", pages <= 40, str(pages))
        layer = subprocess.run(["python3", str(ROOT / "tools/check_pdf_textlayer.py"),
                                str(pdf), str(SRC)], capture_output=True, text=True)
        check("pdf_textlayer", layer.returncode == 0, layer.stdout.strip().splitlines()[-1])
    else:
        check("pdf_exists", False, str(pdf))

    failed = [c for c in checks if not c["passed"]]
    report = {"schema": "sea.v19.consistency-audit/v1", "checks": checks,
              "n_checks": len(checks), "n_failed": len(failed)}
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"v1.9 audit: {len(checks)-len(failed)}/{len(checks)} passed; failures={len(failed)}")
    for item in failed:
        print("FAIL", item)
    print(f"report: {REPORT}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
