#!/usr/bin/env python3
"""Release-oriented consistency audit for the SEA v1.11 candidate snapshot.

Checks numerical identities, estimand labels, public-input provenance, governance
artifacts, manuscript structure, and PDF coordinates. Passing this audit is not
independent proof, third-party reproduction, or end-to-end effectiveness evidence.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "input/sovereign_epistemic_acquisition_EN_v1.11.md"
EVIDENCE_PATH = ROOT / "sim/pilot/results/evidence_status_v1.11.json"
CONSUMPTION_PATH = ROOT / "sim/pilot/results/v110_consumption_caliber/summary.json"
FINANCIAL_PATH = ROOT / "sim/pilot/results/v19_financial_caliber_audit/summary.json"
GOVERNANCE_PATH = ROOT / "sim/pilot/results/governance_conformance_v1.10.json"
SAP_PATH = ROOT / "sim/theory_v1.10/sap_example.json"
REPORT = ROOT / "tools/audit_v111_report.json"
HISTORICAL_SHA256 = "80e953d19efb44787d4fb8b03e37ee6cbfbfc325488769df8a0e89281b495024"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def close_text(value: float, digits: int = 6) -> str:
    return f"{value:.{digits}f}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skip-pdf", action="store_true", help="development only; release audits must not use it")
    args = parser.parse_args()
    checks: list[dict] = []

    def check(name: str, condition: bool, detail: str = "") -> None:
        checks.append({"name": name, "passed": bool(condition), "detail": detail})

    required = [
        MANUSCRIPT, EVIDENCE_PATH, CONSUMPTION_PATH, FINANCIAL_PATH, GOVERNANCE_PATH, SAP_PATH,
        ROOT / "RELEASE_v1.11.md",
        ROOT / "docs/REPRODUCIBILITY_v1.11.md",
        ROOT / "docs/MINIMAL_VALID_EXPERIMENT_v1.11.md",
        ROOT / "docs/LITERATURE_SEARCH_v1.11.md",
        ROOT / "docs/SUPPLEMENT_NORMATIVE_AND_TRANSFER_v1.11.md",
        ROOT / "docs/SUPPLEMENT_FORMAL_AND_SECONDARY_v1.11.md",
        ROOT / "sim/pilot/results/v110_consumption_caliber/future_logging_schema.json",
        ROOT / "sim/pilot/results/v110_consumption_caliber/key_ledger.jsonl.gz",
        ROOT / "sim/pilot/results/v110_consumption_caliber/scenario_effects.csv",
        ROOT / "sim/sea_governance/reference.py",
        ROOT / "sim/sea_governance/test_reference.py",
        ROOT / "sim/sea_pilot/audit_v110_consumption_caliber.py",
        ROOT / "sim/sea_pilot/test_audit_v110_consumption_caliber.py",
        ROOT / "sim/sea_pilot/audit_v19_financial_caliber.py",
        ROOT / "sim/pilot/results/v19_financial_caliber_audit/historical_p2_rows_8ffc7f5.csv",
        ROOT / "tools/reproduce_v110_sap.py",
        ROOT / "tools/test_v110_sap.py",
        ROOT / "tools/check_pdf_layout.py",
    ]
    for path in required:
        check(f"exists:{path.relative_to(ROOT)}", path.is_file())
    missing = [c["name"] for c in checks if not c["passed"]]
    if missing:
        print("Missing required artifacts:", *missing, sep="\n  ")
    text = MANUSCRIPT.read_text(encoding="utf-8")
    evidence = json.loads(EVIDENCE_PATH.read_text(encoding="utf-8"))
    consumption = json.loads(CONSUMPTION_PATH.read_text(encoding="utf-8"))
    financial = json.loads(FINANCIAL_PATH.read_text(encoding="utf-8"))
    governance = json.loads(GOVERNANCE_PATH.read_text(encoding="utf-8"))
    sap = json.loads(SAP_PATH.read_text(encoding="utf-8"))

    check("release:route", evidence["release_route"] == "CONDITIONAL_COMPONENTS_GOVERNANCE_AND_EVIDENCE_AUDIT")
    scope = evidence["global_scope"]
    check("release:tag_and_doi_boundary", scope["public_tag"] == "v1.11.0"
          and scope["v1.11_specific_doi"] is None
          and scope["historical_v1.7_version_doi_not_covering_this_release"] == "10.5281/zenodo.23620920")
    check("release:no_effect_or_human_claim", not scope["overall_SEA_structural_effect_identified"]
          and not scope["prospective_cross_corpus_confirmation"]
          and scope["human_subjects_data"] == "none")
    check("release:manuscript_version", "current public candidate snapshot is **`v1.11.0`**" in text)
    check("release:historical_doi_not_mislabeled", "do not cover v1.9, v1.10, or v1.11" in text)

    check("governance:14_pass", governance["status"] == "PASS"
          and governance["tests_run"] == 14 and not governance["failures"] and not governance["errors"])
    check("governance:four_properties", set(governance["properties"]) >= {"S1", "S2", "S3", "S4"})
    check("governance:manuscript_result", "14/14 conformance and negative tests pass" in text)
    check("governance:scope_limit", "malicious host" in text and "meaningful human control" in text)
    old_algo = "\n".join(p.read_text(encoding="utf-8") for p in (ROOT / "sim/sea_algo").glob("*.py"))
    for stale in ("定理 6.1 分工", "定理 8.2：", "引理 12.1 修正", "§15.3", "定理 11.1", "定理 7.3"):
        check(f"legacy:no_stale_reference:{stale}", stale not in old_algo)
    check("legacy:version_boundary", (ROOT / "sim/sea_algo/README.md").is_file()
          and "historical A1–A10" in (ROOT / "sim/sea_algo/README.md").read_text(encoding="utf-8"))

    p = sap["pipeline"]
    check("sap:pipeline_recalls", p["selected_proxy_recall"] == 0.5
          and math.isclose(p["delivered_proxy_recall"], 1 / 3)
          and math.isclose(p["opened_proxy_recall"], 1 / 3)
          and math.isclose(p["actual_consumption_recall"], 1 / 6))
    check("sap:omission_decomposition", math.isclose(p["total_weighted_omission"], 5 / 6)
          and math.isclose(p["availability_omission"], 1 / 6)
          and math.isclose(p["post_availability_omission"], 4 / 6))
    check("sap:noncomposition", sap["non_composition"]["greedy_value"] == 17
          and sap["non_composition"]["optimal_value"] == 22
          and math.isclose(sap["non_composition"]["ratio"], 17 / 22))
    check("sap:manuscript_example", "selected-proxy recall is $3/6$" in text
          and "actual-consumption recall is $1/6$" in text
          and "17/22\\approx77.27\\%" in text and "guarantee is not violated" in text
          and "does not exceed" not in text)
    check("sap:initial_joint_and_write_timing", "$\\rho_0(x_0,y_0)$" in text
          and "Period-$t$ ranking, delivery, and reward use the pre-write" in text
          and "newly appended current version" in text
          and "every conditional history law is defined" not in text)
    check("sap:zero_probability_histories", "positive-probability support" in text
          and "full-support behavioral reference policy" in text
          and "zero probability under $\\beta$" in text
          and "any fixed feasible action" in text)
    check("algorithm:decomposed_complexity", "L_\\kappa=\\sum_{i=1}^n|\\kappa(x_i)|" in text
          and "B_{\\mathrm{audit}}" in text and "T_{\\mathrm{select}}" in text
          and "Exact $m$-subset enumeration" in text
          and "not a universal running-time theorem" in text)
    check("sap:symmetric_channel_and_measured_absence",
          sap["signal_model"]["type"] == "symmetric_binary_channel"
          and math.isclose(sap["signal_model"]["posterior_relevance_given_positive"], 0.8)
          and sap["rows"][1]["attendance_status"] == "not_attended"
          and "Attendance is instrumented for both opened items" in text)
    check("sap:multi_item_target_partition", "an arbitrary item's first failure does **not** partition" in text
          and "$\\widetilde O\\cap D_S^c$" in text)

    historical = ROOT / "sim/pilot/results/v19_financial_caliber_audit/historical_p2_rows_8ffc7f5.csv"
    check("financial:hash", sha256(historical) == HISTORICAL_SHA256)
    check("financial:bytes", historical.stat().st_size == 382663)
    with historical.open(encoding="utf-8", newline="") as handle:
        check("financial:1260_rows", sum(1 for _ in csv.DictReader(handle)) == 1260)
    financial_script = (ROOT / "sim/sea_pilot/audit_v19_financial_caliber.py").read_text(encoding="utf-8")
    check("financial:no_git_subprocess", "git\", \"show" not in financial_script
          and "subprocess.check_output" not in financial_script)
    provenance = financial["inputs"]["sim/pilot/results/v19_financial_caliber_audit/historical_p2_rows_8ffc7f5.csv"]
    check("financial:provenance", provenance["sha256"] == HISTORICAL_SHA256
          and provenance["source_commit"] == "8ffc7f5"
          and "verified" in provenance["integrity_check"]
          and provenance["rows"] == 1260)
    comparison = financial["semi_oracle_configuration_comparison"]
    check("financial:historical_values", comparison["historical_m5"]["agent_target_hits"] == 120
          and comparison["historical_m5"]["agent_target_opportunities"] == 126
          and math.isclose(comparison["historical_m5"]["feature_scorer_mean_recall"], 13 / 18))
    check("financial:expanded_values", comparison["expanded_m5"]["agent_target_hits"] == 121
          and comparison["expanded_m5"]["agent_target_opportunities"] == 133
          and financial["m5_pooled_across_runs"]["company_day"]["hits"] == 114
          and financial["m5_pooled_across_runs"]["company_day"]["opportunities"] == 126)
    check("financial:budget_caliber", comparison["historical_m5"]["budget_conflict_alarms"] == 7
          and comparison["expanded_m5"]["budget_conflict_alarms"] == 7
          and comparison["expanded_m5"]["slots_per_run"] == 150)
    check("financial:manuscript_no_git_dependency",
          "default reproduction verifies its bytes and row count without reading git history" in text.lower())
    check("financial:feature_and_supply_provenance",
          comparison["expanded_feature_scorer_selection_independently_rebuilt"] is False
          and "not verified from the pinned" in comparison["channel1_supply_per_day"]["historical_evidence_basis"]
          and "S2p-feat values remain frozen-row aggregates" in text)

    population = consumption["population_accounting"]
    check("consumption:key_identities", population["expected_keys"] == 72000
          and population["existing_keys"] == 71970 and population["nonempty_keys"] == 71914
          and population["empty_only_keys"] == 56 and population["missing_keys"] == 30
          and population["existing_keys"] + population["missing_keys"] == 72000)
    check("consumption:record_accounting", population["raw_records"] == 73704
          and population["empty_records"] == 157
          and population["empty_records_on_nonempty_keys"] == 101)
    check("consumption:no_consumption_observation",
          all(v == 0 for v in consumption["observability"]["delivery_open_attendance_actual_consumption_field_counts"].values()))
    check("consumption:no_efficiency_backfill",
          all(v == 0 for v in consumption["observability"]["historical_efficiency_field_counts"].values()))
    resolved = consumption["secondary_existing_calibers"]["RULE_A_NONEMPTY"]["families"]
    totals = {metric: sum(resolved[f][f"n_{metric}"] for f in resolved)
              for metric in ("recall", "return", "sign")}
    check("consumption:rule_A_denominators", totals == {"recall": 71573, "return": 70676, "sign": 71618}, str(totals))
    check("consumption:strict_singleton",
          sum(consumption["secondary_existing_calibers"]["STRICT_SINGLETON_NONEMPTY"]["families"][f]["n_recall"]
              for f in ("O", "C", "Q", "G")) == 70306)
    check("consumption:G_denominators", population["resolved_zero_empty_recall"] == 71629
          and population["resolved_zero_empty_return"] == 70732
          and population["resolved_zero_empty_sign"] == 71674)
    primary = consumption["new_calibers"]["ALL_EXISTING_RECORD_MEAN_ZERO_EMPTY"]["families"]
    replay_evidence = next(c for c in evidence["claims"] if c["id"] == "REPLAY-FOUR-FAMILY")
    check("consumption:accurate_retrospective_names",
          set(consumption["new_calibers"]) == {
              "ALL_EXISTING_RECORD_MEAN_ZERO_EMPTY", "METRIC_RESOLVED_ZERO_EMPTY"}
          and replay_evidence["designated_retrospective_descriptive_caliber"]["id"]
          == "ALL_EXISTING_RECORD_MEAN_ZERO_EMPTY"
          and "Designated retrospective descriptive caliber" in text
          and "ITT_ALL_RECORD_MEAN" not in text and "ITT_METRIC_RESOLVED" not in text
          and "selected-proxy ITT" not in text and "actual-consumption ITT" not in text
          and "primary_historical_sensitivity" not in EVIDENCE_PATH.read_text(encoding="utf-8"))
    for family in ("O", "C", "Q", "G"):
        estimate = primary[family]["equal_run"]["delta_recall"]["estimate"]
        check(f"consumption:primary_delta:{family}", f"{estimate:+.6f}" in text)
        check(f"consumption:primary_keys:{family}", f"{primary[family]['n_recall']:,}" in text)
    ranges = consumption["frozen_17_scenario_ranges"]
    for family in ("O", "C", "Q", "G"):
        item = ranges[family]
        check(f"consumption:17_sign_stability:{family}", not item["delta_recall"]["sign_changed_across_scenarios"]
              and not item["delta_return"]["sign_changed_across_scenarios"])
    check("consumption:interval_label", "exploratory run-level descriptive intervals" in text)
    check("consumption:selected_not_consumed", "never actual-consumption recall" in text
          and "No delivered/opened/attended fields exist" in text)
    schema = json.loads((ROOT / "sim/pilot/results/v110_consumption_caliber/future_logging_schema.json").read_text(encoding="utf-8"))
    required_item = set(schema["properties"]["items"]["items"]["required"])
    check("consumption:future_stages", {"selected", "delivered", "opened", "attended"} <= required_item
          and "consumed" not in required_item)
    attended_required = set(schema["properties"]["items"]["items"]["properties"]["attended"]["required"])
    check("consumption:attendance_instrument", {
        "measurement_status", "instrument", "instrument_version", "threshold_id",
        "validation_status", "assessor_blinding", "evidence_pointer"} <= attended_required)
    outcome_protocol = schema["properties"]["outcome_protocol"]["properties"]
    check("consumption:primary_missing_rule",
          outcome_protocol["primary_rule"]["const"]
          == "ALL_ASSIGNED_FAILURE_COMPOSITE_CONFIRMED_CONSUMPTION_OMISSION_V1"
          and "instrument_registry_sha256" in outcome_protocol
          and "all-assigned failure-composite weighted omission" in text
          and "need not be conservative for a between-arm contrast" in text)
    efficiency_required = set(schema["properties"]["efficiency"]["required"])
    check("consumption:future_efficiency", {"calls", "input_tokens", "output_tokens", "cost", "latency_ms", "retries"} <= efficiency_required)

    captions = [int(x) for x in re.findall(r"^\*\*Table (\d+)\.", text, re.M)]
    check("structure:11_tables", captions == list(range(1, 12)), str(captions))
    check("structure:three_figures", text.count("\\begin{figure}") == 3
          and len(re.findall(r"\\label\{fig:[^}]+\}", text)) == 3)
    tags = [int(x) for x in re.findall(r"\\tag\{(\d+)\}", text)]
    check("structure:11_equation_tags", tags == list(range(1, 12)), str(tags))
    check("structure:no_theorem_mix", "**Theorem " not in text)
    reference_block = text.split("## References", 1)[1].split("## Appendix A", 1)[0].strip()
    references = [part for part in reference_block.split("\n\n") if part.strip()]
    check("structure:51_references", len(references) == 51, str(len(references)))
    check("structure:oracle_relaxation", "clairvoyant/oracle relaxation" in text
          and "normalized expected leaked value" in text
          and "expectation $\\mathbb E[" in text)
    check("structure:explicit_monotone_quantifiers", "for every** $i\\in\\mathcal C_M$ and **every** $A\\subseteq" in text)
    check("structure:narrative_review", "structured narrative positioning" in text
          and "targeted scoping search" not in text)
    for token in ("Lewis et al. (2020)", "Peng et al. (2025)", "Lin et al. (2026)",
                  "Clopper & Pearson, 1934", "Kuhn & Tucker, 1951", "McNemar, 1947",
                  "Cochran, 1954", "Mantel & Haenszel, 1959", "Efron, 1979"):
        check(f"literature:{token}", token in text)
    protocol = (ROOT / "docs/MINIMAL_VALID_EXPERIMENT_v1.11.md").read_text(encoding="utf-8")
    check("protocol:one_primary", "one primary comparison" in text and "one primary outcome" in text
          and "failure-composite weighted omission" in text
          and "唯一主要结局" in protocol and "多个主要结局采用" not in protocol)
    check("protocol:attendance_registration",
          "instrument_registry" in protocol and "有效阅读事件" in protocol
          and "主动确认" in protocol and "任务相关操作" in protocol
          and "测量缺失" in protocol and "盲法" in protocol
          and "instrument registry" in text and "assessor" in text)
    check("protocol:closed_primary_missing_rule",
          "全分配失败复合规则" in protocol and "逆概率加权" in protocol
          and "多重插补" in protocol and "不保证两臂差值方向保守" in protocol
          and "不得在查看结果后选择缺失规则" in protocol)
    supplement = (ROOT / "docs/SUPPLEMENT_FORMAL_AND_SECONDARY_v1.11.md").read_text(encoding="utf-8")
    check("structure:deferred_proofs_and_secondary_tables",
          "SA.1 Online threshold" in supplement and "SA.2 Conditional EIG" in supplement
          and "SA.3 Fixed-capacity" in supplement and "Supplementary Table SB1" in supplement
          and "Supplementary Table SB2" in supplement and "Supplementary Table SB3" in supplement
          and "Supplementary Table SC1" in supplement
          and "Secondary Rule A: nonempty selections" not in text
          and "Strict-singleton C: 70,306 common keys" not in text
          and "Core commands are manually wrapped" not in text)
    check("protocol:efficiency", "per-run and per-successfully-consumed-target efficiency outcomes" in text)
    bash_lines = []
    in_bash = False
    for line in text.splitlines():
        if line.strip() == "```bash":
            in_bash = True
        elif in_bash and line.strip() == "```":
            in_bash = False
        elif in_bash and len(line) > 100:
            bash_lines.append(line)
    check("layout:no_long_bash_source_lines", not bash_lines, str(bash_lines[:2]))

    pdf = ROOT / "latex/SEA_EN_v1.11_draft.pdf"
    if not args.skip_pdf:
        check("layout:pdf_exists", pdf.is_file())
        if pdf.is_file():
            sys.path.insert(0, str(ROOT / "tools"))
            from check_pdf_layout import inspect
            layout = inspect(pdf, 20.0)
            check("layout:no_edge_overflow", layout["status"] == "PASS", str(layout["findings"][:2]))
            info = subprocess.run(["pdfinfo", str(pdf)], check=True, capture_output=True, text=True).stdout
            check("layout:a4", "595.276 x 841.89 pts (A4)" in info)
            check("layout:author_metadata", "Wen Hu" in info and "Xutong Wang" in info and "Ya Yu" in info)

    failed = [c for c in checks if not c["passed"]]
    report = {
        "schema": "sea.v111.release-audit/v1", "n_checks": len(checks),
        "n_passed": len(checks) - len(failed), "n_failed": len(failed),
        "status": "PASS" if not failed else "FAIL", "failures": failed,
        "scope": "Internal consistency only; not independent proof, reproduction, or effectiveness validation.",
        "checks": checks,
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"v1.11 audit: {report['n_passed']}/{report['n_checks']} passed; failures={len(failed)}")
    for failure in failed:
        print("FAIL", failure["name"], failure["detail"])
    print(f"report: {REPORT}")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
