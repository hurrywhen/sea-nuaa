#!/usr/bin/env python3
"""Release-oriented consistency audit for the SEA v1.13 candidate snapshot.

Checks the conditional framework/artifact claims, synthetic executor, governance
fixes, measurement protocol, retrospective caliber boundaries, and PDF layout.
Passing this audit is not independent proof, third-party reproduction, or
end-to-end effectiveness evidence.
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
MANUSCRIPT = ROOT / "input/sovereign_epistemic_acquisition_EN_v1.13.md"
EVIDENCE_PATH = ROOT / "sim/pilot/results/evidence_status_v1.13.json"
CONSUMPTION_PATH = ROOT / "sim/pilot/results/v110_consumption_caliber/summary.json"
FINANCIAL_PATH = ROOT / "sim/pilot/results/v19_financial_caliber_audit/summary.json"
GOVERNANCE_PATH = ROOT / "sim/pilot/results/governance_conformance_v1.13.json"
SAP_PATH = ROOT / "sim/theory_v1.10/sap_example.json"
LONGITUDINAL_PATH = ROOT / "sim/pilot/results/sap_v1.13/longitudinal.json"
TARGET_PATH = ROOT / "sim/pilot/results/sap_v1.13/target_construction_audit.json"
MATCHED_PATH = ROOT / "sim/pilot/results/sap_v1.13/matched_implementation_demo.json"
REPORT = ROOT / "tools/audit_v113_report.json"
HISTORICAL_SHA256 = "80e953d19efb44787d4fb8b03e37ee6cbfbfc325488769df8a0e89281b495024"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skip-pdf", action="store_true", help="development only; release audits must not use it")
    args = parser.parse_args()
    checks: list[dict] = []

    def check(name: str, condition: bool, detail: str = "") -> None:
        checks.append({"name": name, "passed": bool(condition), "detail": detail})

    required = [
        MANUSCRIPT, EVIDENCE_PATH, CONSUMPTION_PATH, FINANCIAL_PATH, GOVERNANCE_PATH, SAP_PATH,
        LONGITUDINAL_PATH, TARGET_PATH, MATCHED_PATH,
        ROOT / "RELEASE_v1.13.md",
        ROOT / "docs/REPRODUCIBILITY_v1.13.md",
        ROOT / "docs/MINIMAL_VALID_EXPERIMENT_v1.13.md",
        ROOT / "docs/LITERATURE_SEARCH_v1.13.md",
        ROOT / "docs/SUPPLEMENT_NORMATIVE_AND_TRANSFER_v1.13.md",
        ROOT / "docs/SUPPLEMENT_FORMAL_AND_SECONDARY_v1.13.md",
        ROOT / "docs/SUPPLEMENT_RETROSPECTIVE_AUDITS_v1.13.md",
        ROOT / "sim/pilot/results/v110_consumption_caliber/future_logging_schema.json",
        ROOT / "sim/pilot/results/v110_consumption_caliber/key_ledger.jsonl.gz",
        ROOT / "sim/pilot/results/v110_consumption_caliber/scenario_effects.csv",
        ROOT / "sim/sea_governance/reference.py",
        ROOT / "sim/sea_governance/test_reference.py",
        ROOT / "sim/sea_sap/executor.py",
        ROOT / "sim/sea_sap/test_executor.py",
        ROOT / "sim/sea_sap/target_construction.py",
        ROOT / "sim/sea_sap/test_target_construction.py",
        ROOT / "sim/sea_sap/fixtures/longitudinal.json",
        ROOT / "sim/sea_sap/fixtures/target_construction.json",
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
    protocol = (ROOT / "docs/MINIMAL_VALID_EXPERIMENT_v1.13.md").read_text(encoding="utf-8")
    supplement = (ROOT / "docs/SUPPLEMENT_RETROSPECTIVE_AUDITS_v1.13.md").read_text(encoding="utf-8")
    formal = (ROOT / "docs/SUPPLEMENT_FORMAL_AND_SECONDARY_v1.13.md").read_text(encoding="utf-8")
    normative = (ROOT / "docs/SUPPLEMENT_NORMATIVE_AND_TRANSFER_v1.13.md").read_text(encoding="utf-8")
    literature = (ROOT / "docs/LITERATURE_SEARCH_v1.13.md").read_text(encoding="utf-8")
    reproducibility = (ROOT / "docs/REPRODUCIBILITY_v1.13.md").read_text(encoding="utf-8")
    evidence = json.loads(EVIDENCE_PATH.read_text(encoding="utf-8"))
    consumption = json.loads(CONSUMPTION_PATH.read_text(encoding="utf-8"))
    financial = json.loads(FINANCIAL_PATH.read_text(encoding="utf-8"))
    governance = json.loads(GOVERNANCE_PATH.read_text(encoding="utf-8"))
    sap = json.loads(SAP_PATH.read_text(encoding="utf-8"))
    longitudinal = json.loads(LONGITUDINAL_PATH.read_text(encoding="utf-8"))
    target = json.loads(TARGET_PATH.read_text(encoding="utf-8"))
    matched = json.loads(MATCHED_PATH.read_text(encoding="utf-8"))

    check("release:route", evidence["release_route"] == "CONDITIONAL_COMPONENTS_GOVERNANCE_AND_EVIDENCE_AUDIT")
    scope = evidence["global_scope"]
    check("release:tag_and_doi_boundary", scope["public_tag"] == "v1.13.0"
          and scope["v1.13_specific_doi"] is None
          and scope["historical_v1.7_version_doi_not_covering_this_release"] == "10.5281/zenodo.23620920")
    check("release:no_effect_or_human_claim", not scope["overall_SEA_structural_effect_identified"]
          and not scope["prospective_cross_corpus_confirmation"]
          and scope["human_subjects_data"] == "none"
          and scope["synthetic_executor_is_effectiveness_evidence"] is False)
    check("release:manuscript_version", "current public candidate snapshot is **`v1.13.0`**" in text)
    check("release:historical_doi_not_mislabeled", "do not cover v1.9, v1.10, v1.11, or v1.13" in text)
    check("release:three_contributions", "one conditional framework and two checkable artifacts" in text
          and "The paper makes three bounded contributions" in text)

    check("governance:18_pass", governance["status"] == "PASS"
          and governance["tests_run"] == 18 and not governance["failures"] and not governance["errors"])
    check("governance:manuscript_result", "18/18 conformance and negative tests pass" in text)
    check("governance:actor_principal", "actor–principal consistency" in text
          and "actor_principal_mismatch" in (ROOT / "sim/sea_governance/reference.py").read_text())
    check("governance:hash_spec", "sea-governance-record/2" in text
          and "domain-separated canonical JSON" in text
          and "recursive embedding" in text)
    check("governance:feature_alignment", "harm_avoidance" in text
          and "actionability" not in text.split("## 4 Consumption")[0])
    check("governance:scope_limit", "malicious-host security" in text and "meaningful human control" in text)

    check("executor:guard_trace", all(longitudinal["guard_trace"].values()))
    check("executor:five_resources", all(v > 0 for v in longitudinal["budget"]["spent"].values()))
    check("executor:audit_valid", longitudinal["audit"]["verification"]["valid"])
    check("executor:no_latent_consumption", longitudinal["latent_actual_consumption_observed"] is False
          and all(row["latent_actual_consumption"] is None
                  for period in longitudinal["periods"] for row in period["operational_target_ledger"]))
    check("executor:ledger_scope", "NOT_LATENT" in longitudinal["ledger_scope"]
          and all("OPERATIONAL" in p["outcome_summary"]["ledger_scope"] for p in longitudinal["periods"]))
    check("executor:availability_and_link_rules", "first_available_period" in text
          and "reference_link_truth" in (ROOT / "sim/sea_sap/executor.py").read_text()
          and "staged_link_pass" in (ROOT / "sim/sea_sap/executor.py").read_text())
    check("executor:resource_precheck", "resource_precheck" in {r["event"] for r in longitudinal["audit"]["records"]}
          and "Whole-period resource precheck" in text)
    check("executor:control_continuity", "control continuity" in text.lower()
          and "evaluation cohort" in text.lower()
          and "continue_with_target_registry" in (ROOT / "sim/sea_sap/executor.py").read_text())
    check("executor:fc_and_unknown", math.isclose(longitudinal["periods"][0]["outcome_summary"]["weighted_fc_omission"], 5 / 6)
          and math.isclose(longitudinal["periods"][1]["outcome_summary"]["weighted_fc_omission"], 1.0)
          and math.isclose(longitudinal["periods"][1]["outcome_summary"]["weighted_unknown_terminal"], 1 / 6))
    check("executor:machine_separate", "machine_ingestion_and_task_reference" in text
          and longitudinal["periods"][0]["outcome_summary"]["machine_ingestion_and_task_reference"]["c1"] is True)
    check("executor:matched_not_effect", matched["status"] == "MECHANISTIC_MATCHED_FIXTURE__NOT_A_MODEL_OR_DEPLOYMENT_EXPERIMENT"
          and matched["matching"]["external_model_calls"] == 0)
    check("target:human_pending", target["human_annotations_created"] is False
          and "HUMAN_VALIDATION_PENDING" in target["status"])
    check("target:granularity", math.isclose(target["granularity_sensitivity"]["fine_weighted_omission"], 0.5)
          and math.isclose(target["granularity_sensitivity"]["coarse_weighted_omission"], 1 / 6))
    check("target:dynamic_rule", "NEW_EVALUATION_COHORT__NO_CROSS_VERSION_POOLING" in text
          and target["dynamic_target_rule"] == "NEW_EVALUATION_COHORT__NO_CROSS_VERSION_POOLING")

    p = sap["pipeline"]
    check("sap:noncomposition", sap["non_composition"]["greedy_value"] == 17
          and sap["non_composition"]["optimal_value"] == 22
          and math.isclose(sap["non_composition"]["ratio"], 17 / 22))
    check("sap:manuscript_noncomposition", "17/22\\approx77.27\\%" in text
          and "guarantee is not violated" in text and "does not exceed" not in text)
    check("sap:zero_probability_histories", "full-support behavioral reference policy" in text
          and "zero probability under $\\beta$" in text and "any fixed feasible action" in text)
    check("sap:action_sets", "resource-feasible" in text and "guard-admissible" in text
          and "loggable attempts" in text)
    check("algorithm:decomposed_complexity", "L_{\\mathcal T}" in text
          and "B_{audit}" in text and "T_{select}" in text
          and "not a universal running-time theorem" in text)

    historical = ROOT / "sim/pilot/results/v19_financial_caliber_audit/historical_p2_rows_8ffc7f5.csv"
    check("financial:hash", sha256(historical) == HISTORICAL_SHA256)
    check("financial:bytes", historical.stat().st_size == 382663)
    with historical.open(encoding="utf-8", newline="") as handle:
        check("financial:1260_rows", sum(1 for _ in csv.DictReader(handle)) == 1260)
    financial_script = (ROOT / "sim/sea_pilot/audit_v19_financial_caliber.py").read_text(encoding="utf-8")
    check("financial:no_git_subprocess", "git\", \"show" not in financial_script
          and "subprocess.check_output" not in financial_script)
    check("financial:manuscript_no_git_dependency",
          "default reproduction verifies its bytes and row count without reading git history" in text.lower())
    check("financial:falsification_example", "120/126=0.952381" in text and "7/7 budget alarms" in text)

    population = consumption["population_accounting"]
    check("consumption:key_identities", population["expected_keys"] == 72000
          and population["existing_keys"] == 71970 and population["nonempty_keys"] == 71914
          and population["empty_only_keys"] == 56 and population["missing_keys"] == 30)
    check("consumption:three_calibers", set(consumption["new_calibers"]) == {
        "ALL_EXISTING_RECORD_MEAN_ZERO_EMPTY", "METRIC_RESOLVED_ZERO_EMPTY",
        "ALL_EXPECTED_RECORD_MEAN_ZERO_EMPTY_NO_ROW"})
    check("consumption:conservative_support", sum(
        item["n_recall"] for item in consumption["new_calibers"]["ALL_EXPECTED_RECORD_MEAN_ZERO_EMPTY_NO_ROW"]["families"].values()) == 72000)
    check("consumption:no_consumption_observation",
          all(v == 0 for v in consumption["observability"]["delivery_open_attendance_actual_consumption_field_counts"].values()))
    check("consumption:main_no_family_estimates", "+0.029720" not in text and "+0.129060" not in text
          and "p=0.160128" not in text and "exploratory run-level descriptive intervals" not in text)
    check("consumption:retrospective_title", "## 6 Frozen Retrospective Sensitivity Audits" in text)
    schema = json.loads((ROOT / "sim/pilot/results/v110_consumption_caliber/future_logging_schema.json").read_text(encoding="utf-8"))
    protocol_props = schema["properties"]["outcome_protocol"]["properties"]
    check("consumption:schema_and_rule", schema["properties"]["schema_version"]["const"].endswith("/v4")
          and protocol_props["primary_rule"]["const"] == "ALL_ASSIGNED_FAILURE_COMPOSITE_OPERATIONAL_ATTENDANCE_OMISSION_V1"
          and protocol_props["attendance_decision_rule"]["const"] == "VALID_READING_AND_CONTENT_LINKED_CONFIRMATION"
          and protocol_props["machine_event_term"]["const"] == "machine_ingestion_and_task_reference_not_human_attention")
    check("consumption:main_and_rule", "VALID_READING_AND_CONTENT_LINKED_CONFIRMATION" in text
          and "\\mathbf{AND}" in text)

    captions = [int(x) for x in re.findall(r"^\*\*Table (\d+)\.", text, re.M)]
    check("structure:7_tables", captions == list(range(1, 8)), str(captions))
    check("structure:two_figures", text.count("\\begin{figure}") == 2)
    tags = [int(x) for x in re.findall(r"\\tag\{(\d+)\}", text)]
    check("structure:7_equation_tags", tags == list(range(1, 8)), str(tags))
    reference_block = text.split("## References", 1)[1].split("## Appendix A", 1)[0].strip()
    references = [part for part in reference_block.split("\n\n") if part.strip()]
    check("structure:52_references", len(references) == 52, str(len(references)))
    check("references:savage_unified", "Savage, L. J. (1951)" in reference_block)
    body_text = text.split("## References", 1)[0]
    uncited = []
    for entry in references:
        surname = entry.split(",")[0].strip()
        if not any(surname in document for document in (body_text, formal, supplement, normative, literature)):
            uncited.append(surname)
    check("references:unified_list_all_cited", not uncited, str(uncited))
    check("structure:compression", len(text.split()) < 9000, str(len(text.split())))
    check("structure:standard_foundations_demoted", "## 5 Conditional Technical Foundations" in text
          and "not presented as multiple new theorems" in text)

    check("protocol:one_primary", "one primary comparison" in text and "one primary outcome" in text
          and "唯一主要结局" in protocol and "多个主要结局采用" not in protocol)
    check("protocol:fc_symbol", "\\mathcal M^{FC}" in text and "\\mathcal M_\\nu" in text
          and "M_{\\nu,a}^{FC}" in protocol)
    check("protocol:contrast_bounds", "\\Delta^{FC}-u_{sea}" in text and "\\Delta^{FC}+u_{control}" in text
          and "\\mathcal M_{\\nu,sea}^{Z}" in text
          and "\\Delta^{FC}-u_{sea}" in protocol and "\\mathcal M_{\\nu,sea}^{Z}" in protocol)
    check("protocol:bounds_not_latent", "operational** bounds, not latent" in text
          and "不是潜在真实消费遗漏边界" in protocol
          and "false positive" in text and "假阳性" in protocol)
    check("protocol:attendance_and", "instrument registry" in text and "blind" in text
          and "AND" in protocol and "machine_ingestion_and_task_reference" in protocol)
    check("protocol:target_version", "新的评价队列" in protocol and "参考语料快照" in protocol
          and "first_available_period" in protocol)
    check("protocol:power", "最低覆盖要求" in protocol and "功效模拟" in protocol)
    check("supplement:retrospective_moved", "ALL_EXPECTED_RECORD_MEAN_ZERO_EMPTY_NO_ROW" in supplement
          and "Demoted exploratory run-level bootstrap intervals" in supplement
          and "R3 Run-level dispersion" in supplement)
    check("supplement:formal_foundations", "### SA.0 Finite observable-history existence proof" in formal
          and "SD Standard technical foundations" in formal)
    check("supplement:notation_sync", "actionability" not in formal and "\\kappa_e" not in formal
          and "c_e(S)" in formal and "\\lambda_B" in formal
          and "attended / consumed" not in formal and "G_i(e)" in formal)
    check("supplement:ledger_separation", "**Theoretical ledger.**" in formal
          and "**Executable operational/FC ledger.**" in formal
          and "(attendance/actual consumption)" not in formal
          and "not executable from operational telemetry alone" in formal)
    check("supplement:coverage_symbol_not_Z", "Z_i(e,\\omega)" not in formal
          and "G_i(e,\\omega)" in formal)
    check("supplement:SD_numbering", "Proposition SD.5" in formal and "Proposition SD.6" in formal
          and "Proposition SD.10" in formal
          and not re.search(r"(Proposition|Definition|Corollary) [4-7]\.\d", formal))
    check("supplement:table_numbering", "**Table 5." not in formal
          and "Supplementary Table SD1" in formal)
    check("supplement:cp_measurement_note", "theoretical-ledger" in formal
          and "perfectly classify $D$" in formal)
    check("normative:N_numbering", "## N1 Measurement" in normative
          and "## S1 " not in normative and "Savage, 1951" in normative)
    check("main:coverage_symbol", "G_i(e)" in text and "c_e(S)" in text
          and "Z_i(e)$ be authentic reference coverage" not in text)
    check("main:cohort_not_instance", "New version creates new evaluation cohort" in text
          and "New version creates new SAP instance" not in text)
    check("reproducibility:schema_v4_sync", "升级为 `/v4`" in reproducibility
          and "升级为 `/v3`" not in reproducibility
          and "新评价队列" in reproducibility and "创建新 SAP 实例" not in reproducibility)
    executor_source = (ROOT / "sim/sea_sap/executor.py").read_text(encoding="utf-8")
    executor_tests = (ROOT / "sim/sea_sap/test_executor.py").read_text(encoding="utf-8")
    check("executor:plan_validation_before_mutation",
          "invalid terminal plan: delivered/opened must be known candidates" in executor_source
          and "test_invalid_terminal_plan_fails_before_mutation" in executor_tests)
    check("executor:misclassification_both_directions",
          "latent_false_positive_contrast" in executor_tests
          and "latent_false_negative_contrast" in executor_tests)

    pdf = ROOT / "latex/SEA_EN_v1.13_draft.pdf"
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
        "schema": "sea.v113.release-audit/v1", "n_checks": len(checks),
        "n_passed": len(checks) - len(failed), "n_failed": len(failed),
        "status": "PASS" if not failed else "FAIL", "failures": failed,
        "scope": "Internal consistency only; not independent proof, reproduction, or effectiveness validation.",
        "checks": checks,
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"v1.13 audit: {report['n_passed']}/{report['n_checks']} passed; failures={len(failed)}")
    for failure in failed:
        print("FAIL", failure["name"], failure["detail"])
    print(f"report: {REPORT}")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
