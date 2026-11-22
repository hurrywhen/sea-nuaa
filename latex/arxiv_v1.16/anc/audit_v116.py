#!/usr/bin/env python3
"""Release-oriented consistency audit for the SEA v1.16 candidate snapshot.

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
MANUSCRIPT = ROOT / "input/sovereign_epistemic_acquisition_EN_v1.16.md"
EVIDENCE_PATH = ROOT / "sim/pilot/results/evidence_status_v1.16.json"
CONSUMPTION_PATH = ROOT / "sim/pilot/results/v110_consumption_caliber/summary.json"
FINANCIAL_PATH = ROOT / "sim/pilot/results/v19_financial_caliber_audit/summary.json"
GOVERNANCE_PATH = ROOT / "sim/pilot/results/governance_conformance_v1.16.json"
SAP_PATH = ROOT / "sim/theory_v1.10/sap_example.json"
LONGITUDINAL_PATH = ROOT / "sim/pilot/results/sap_v1.16/longitudinal.json"
TARGET_PATH = ROOT / "sim/pilot/results/sap_v1.16/target_construction_audit.json"
MATCHED_PATH = ROOT / "sim/pilot/results/sap_v1.16/matched_implementation_demo.json"
PROTOCOL_DEMO_PATH = ROOT / "sim/pilot/results/sap_v1.16/protocol_registry_switch_demo.json"
REPORT = ROOT / "tools/audit_v116_report.json"
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
        LONGITUDINAL_PATH, TARGET_PATH, MATCHED_PATH, PROTOCOL_DEMO_PATH,
        ROOT / "RELEASE_v1.16.md",
        ROOT / "docs/REPRODUCIBILITY_v1.16.md",
        ROOT / "docs/MINIMAL_VALID_EXPERIMENT_v1.16.md",
        ROOT / "docs/LITERATURE_SEARCH_v1.16.md",
        ROOT / "docs/SUPPLEMENT_NORMATIVE_AND_TRANSFER_v1.16.md",
        ROOT / "docs/SUPPLEMENT_FORMAL_AND_SECONDARY_v1.16.md",
        ROOT / "docs/SUPPLEMENT_RETROSPECTIVE_AUDITS_v1.16.md",
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
        ROOT / "tools/make_retrospective_tables.py",
    ]
    for path in required:
        check(f"exists:{path.relative_to(ROOT)}", path.is_file())
    missing = [c["name"] for c in checks if not c["passed"]]
    if missing:
        print("Missing required artifacts:", *missing, sep="\n  ")
    text = MANUSCRIPT.read_text(encoding="utf-8")
    protocol = (ROOT / "docs/MINIMAL_VALID_EXPERIMENT_v1.16.md").read_text(encoding="utf-8")
    supplement = (ROOT / "docs/SUPPLEMENT_RETROSPECTIVE_AUDITS_v1.16.md").read_text(encoding="utf-8")
    formal = (ROOT / "docs/SUPPLEMENT_FORMAL_AND_SECONDARY_v1.16.md").read_text(encoding="utf-8")
    normative = (ROOT / "docs/SUPPLEMENT_NORMATIVE_AND_TRANSFER_v1.16.md").read_text(encoding="utf-8")
    literature = (ROOT / "docs/LITERATURE_SEARCH_v1.16.md").read_text(encoding="utf-8")
    reproducibility = (ROOT / "docs/REPRODUCIBILITY_v1.16.md").read_text(encoding="utf-8")
    evidence = json.loads(EVIDENCE_PATH.read_text(encoding="utf-8"))
    consumption = json.loads(CONSUMPTION_PATH.read_text(encoding="utf-8"))
    financial = json.loads(FINANCIAL_PATH.read_text(encoding="utf-8"))
    governance = json.loads(GOVERNANCE_PATH.read_text(encoding="utf-8"))
    sap = json.loads(SAP_PATH.read_text(encoding="utf-8"))
    longitudinal = json.loads(LONGITUDINAL_PATH.read_text(encoding="utf-8"))
    target = json.loads(TARGET_PATH.read_text(encoding="utf-8"))
    matched = json.loads(MATCHED_PATH.read_text(encoding="utf-8"))
    protocol_demo = json.loads(PROTOCOL_DEMO_PATH.read_text(encoding="utf-8"))

    check("release:route", evidence["release_route"] == "CONDITIONAL_COMPONENTS_GOVERNANCE_AND_EVIDENCE_AUDIT")
    scope = evidence["global_scope"]
    check("release:tag_and_doi_boundary", scope["public_tag"] == "v1.16.0"
          and scope["v1.16_specific_doi"] is None
          and scope["historical_v1.7_version_doi_not_covering_this_release"] == "10.5281/zenodo.23620920")
    check("release:no_effect_or_human_claim", not scope["overall_SEA_structural_effect_identified"]
          and not scope["prospective_cross_corpus_confirmation"]
          and scope["human_subjects_data"] == "none"
          and scope["synthetic_executor_is_effectiveness_evidence"] is False)
    check("release:manuscript_version", "current public candidate snapshot is **`v1.16.0`**" in text)
    check("release:historical_doi_not_mislabeled", "do not cover v1.9, v1.10, v1.11, v1.13, v1.14, v1.15, or v1.16" in text)
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
    references = [part for part in reference_block.split("\n\n")
                  if part.strip() and not part.strip().startswith("\\")]
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

    # ---- v1.16 revision checks: exogenous protocol registry governance ----
    check("sap:registry_in_state_exogenous_protocol",
          "\\rho_t=(v_t,E_{v_t},\\mathcal T_{v_t},A^{ref}_{v_t})" in text
          and "\\{\\nu^{(v)}\\}_{\\rho^{(v)}\\in\\mathfrak R}" in text
          and "exogenous evaluation-protocol events" in text
          and "maximal interval of constant $v_t$" in text
          and longitudinal.get("sap_tuple_scope")
          == "control_instance_registry_in_state__exogenous_protocol_single_line__cohort_separated")
    check("sap:switch_not_policy_action",
          "registry-version switch" not in text
          and "not policy actions" in text
          and "no objective-write authorization is required or meaningful" in text
          and "the policy cannot switch registries" in text.lower())
    check("sap:single_line_lifecycle",
          "single-line" in text and "sealed" in text
          and "unique active path" in text
          and "never copied into parallel branches" in text
          and "no registry rollback" in text
          and "objective rollback restores an objective version only, never a registry version" in text)
    check("sap:symbols_deduplicated",
          "\\mathfrak R" in text and "\\mu_0(x_0,y_0)" in text
          and "\\rho_0" not in text and "R_t" not in text
          and "v\\in\\mathcal V" not in text
          and "Reflective principal $R$" in text)
    check("sap:existence_preserved", "Registry-version extension" in formal
          and "frozen ex ante" in formal and "finite and frozen ex ante" in text
          and "exogenous evaluation-protocol events following a fixed ex-ante schedule and frozen switch timing, not policy actions" in formal)
    check("executor:protocol_declaration_code",
          all(token in executor_source for token in (
              "registry_family", "protocol_registry_schedule", "_parse_protocol_declaration",
              "control_path_sealed", "registry_switch_rejected",
              "version_not_in_registry_family", "registry_content_hash_mismatch",
              "version_not_next_in_protocol_schedule", "sealed_control_path",
              "protocol_declaration_sha256",
              "protocol_switch_timing", "protocol_reset_targets",
              "switch_timing_mismatch", "protocol_declaration_tampered",
              "reset_target_not_declared", "_assert_declaration_intact",
              "registry_objective_budget_mutated", "active_path_mutated",
              "rejection_audit_record_appended")))
    check("executor:protocol_governance_tests",
          all(name in executor_tests for name in (
              "test_non_family_registry_switch_is_rejected_with_record",
              "test_tampered_family_registry_hash_mismatch_is_rejected",
              "test_out_of_schedule_switch_is_rejected",
              "test_sealed_predecessor_cannot_run_write_rollback_or_switch",
              "test_objective_rollback_does_not_restore_registry_version",
              "test_switch_without_family_declaration_is_rejected",
              "test_frozen_family_declaration_is_verified_at_load",
              "test_protocol_registry_switch_demo_passes_all_checks",
              "test_switch_timing_is_frozen_and_enforced",
              "test_declaration_tampering_after_results_is_rejected",
              "test_full_reset_requires_declared_reset_target",
              "test_backward_full_reset_is_new_instance_with_single_version_schedule",
              "test_protocol_timing_and_reset_declaration_validation")))
    check("executor:protocol_demo_artifact",
          protocol_demo["status"] == "SYNTHETIC_PROTOCOL_TRANSITION_DEMO__NOT_EFFECTIVENESS_EVIDENCE"
          and all(protocol_demo["checks"].values())
          and protocol_demo["audit"]["verification"]["valid"]
          and len(protocol_demo["rejection_events"]) == 5
          and len(protocol_demo["timing_and_declaration_rejection_events"]) == 3
          and len(protocol_demo["seal_events"]) == 2
          and len(protocol_demo["full_reset_seal_events"]) == 1
          and len(protocol_demo["cohort_change_events"]) == 1
          and protocol_demo["cohort_change_events"][0]["event_kind"] == "exogenous_evaluation_protocol_event"
          and protocol_demo["cohort_change_events"][0]["policy_action"] is False
          and protocol_demo["cohort_change_events"][0]["authorization_required"] is False
          and protocol_demo["cohort_change_events"][0]["declared_switch_after_period"] == 0
          and protocol_demo["cohort_change_events"][0]["completed_periods_before_switch"] == 1
          and protocol_demo["protocol_switch_timing"] == {"targets-v2": 0}
          and protocol_demo["protocol_reset_targets"] == ["targets-v1", "targets-v2"]
          and all(event["registry_objective_budget_mutated"] is False
                  and event["active_path_mutated"] is False
                  and event["rejection_audit_record_appended"] is True
                  and event["resources_spent"] == 0
                  for event in protocol_demo["rejection_events"]
                  + protocol_demo["timing_and_declaration_rejection_events"])
          and protocol_demo["new_real_model_calls"] == 0)
    check("executor:fixture_frozen_timing_and_reset_declaration",
          json.loads((ROOT / "sim/sea_sap/fixtures/longitudinal.json").read_text(encoding="utf-8"))
          ["protocol_switch_timing"] == {"targets-v2": 0}
          and json.loads((ROOT / "sim/sea_sap/fixtures/longitudinal.json").read_text(encoding="utf-8"))
          ["protocol_reset_targets"] == ["targets-v1", "targets-v2"])
    check("main:rejection_state_effect_precise",
          "zero state mutation" not in text
          and "only state change is one appended rejection audit record" in text
          and "switch_after_period" in text
          and "switch_timing_mismatch" in text and "protocol_declaration_tampered" in text
          and "pre-declared allowed reset target" in text
          and "fresh independent single-version schedule" in text)
    check("supplement:rejection_and_timing_reset",
          "only one rejection audit record is appended" in formal
          and "frozen switch timing" in formal
          and "declared protocol exception" in formal
          and "not that the whole state is unmutated" in formal)
    check("protocol:timing_reset_preregistration",
          "switch_after_period" in protocol and "protocol_reset_targets" in protocol
          and "读取任何处理臂结果之前冻结" in protocol
          and "全新独立单版本日程" in protocol
          and "仅向账本追加一条拒绝审计记录" in protocol)
    check("executor:s12_dependent_input_helpers",
          all(token in executor_source for token in (
              "cov_se_sp", "cov_mz_se", "cov_mz_sp",
              "completed_measurement_transport_joint_bootstrap",
              "completed_measurement_transport_sensitivity_grid",
              "transportability_stratified_diagnostics",
              "degenerate_replicates", "input_independence_assumed"))
          and all(name in executor_tests for name in (
              "test_s12_delta_method_covariance_terms",
              "test_s12_joint_bootstrap_preserves_dependence_and_is_deterministic",
              "test_s12_sensitivity_grid_reports_inadmissible_and_range",
              "test_transportability_stratified_diagnostics")))
    check("supplement:s12_dependent_inputs_and_diagnostics",
          "Dependent inputs: covariance terms or joint bootstrap" in formal
          and "transportability_stratified_diagnostics" in formal
          and "completed_measurement_transport_joint_bootstrap" in formal
          and "completed_measurement_transport_sensitivity_grid" in formal
          and "never prove" in formal)
    check("protocol:s12_covariance_bootstrap_stratified_plan",
          "completed_measurement_transport_joint_bootstrap" in protocol
          and "transportability_stratified_diagnostics" in protocol
          and "不得默认独立" in protocol
          and "分层诊断" in protocol)
    check("executor:instrument_hardening_code",
          all(token in executor_source for token in (
              "_is_sha256_hex", 'f"{key}_interval"',
              "transportability_assumption", "blinded_reference_set",
              "completion_subset_representativeness", "overlap_with_tuning_or_main_corpus"))
          and all(name in executor_tests for name in (
              "test_validated_instrument_hashes_must_be_true_hex",
              "test_validated_instrument_requires_uncertainty_and_transportability",
              "test_validated_instrument_requires_blinded_reference_set_and_representativeness"))
          and "sensitivity_interval" in executor_tests and "specificity_interval" in executor_tests)
    check("executor:s12_transport_helper",
          "completed_measurement_transport" in executor_source
          and "variance_amplification_factor" in executor_source
          and "precision_warning" in executor_source
          and "completed_measurement_transport_delta_method" in executor_source
          and "test_s12_transport_identity_precision_warning_and_delta_method" in executor_tests)
    check("main:s12_transportability_and_precision",
          "conditionally stable between the validation and deployment populations" in text
          and "Youden denominator $se_a+sp_a-1$ approaches zero" in text
          and "precision warning" in text and "sensitivity grid" in text)
    check("supplement:s12_transportability_conditions",
          "P_{\\mathrm{validation}}(Z=1\\mid D=1,a)=P_{\\mathrm{deployment}}(Z=1\\mid D=1,a)" in formal
          and "P_{\\mathrm{validation}}(Z=0\\mid D=0,a)=P_{\\mathrm{deployment}}(Z=0\\mid D=0,a)" in formal
          and "Validation-to-deployment transportability" in formal
          and "Precision warning near a zero denominator" in formal
          and "1/J_a^2" in formal and "covariate standardization or stratified estimation" in formal)
    check("protocol:transportability_and_precision_plan",
          "可迁移性条件与完成子集代表性" in protocol
          and "P_{\\mathrm{validation}}(Z=1\\mid D=1,a)" in protocol
          and "近零分母精度预警与敏感性网格" in protocol
          and "completion_subset_representativeness" in protocol
          and "transportability_assumption" in protocol
          and "blinded_reference_set" in protocol)
    check("main:counterexample_condition",
          "collapse to $[\\Delta^{FC},\\Delta^{FC}]$, and to $[0,0]$ when additionally $\\Delta^{FC}=0$" in text
          and "with no unknowns the operational bounds collapse to $[0,0]$" not in text)
    context_keys = {"control_instance_id", "evaluation_cohort_id",
                    "target_registry_version", "target_registry_sha256"}
    check("executor:cohort_attribution_all_events",
          all(context_keys <= set(record["payload"])
              for record in longitudinal["audit"]["records"])
          and all(record["payload"]["evaluation_cohort_id"] == longitudinal["evaluation_cohort_id"]
                  for record in longitudinal["audit"]["records"]))
    check("executor:dry_run_before_mutation",
          "selection_dry_run" in {r["event"] for r in longitudinal["audit"]["records"]}
          and "_dry_run_selection" in executor_source
          and "record=False" in executor_source
          and "test_delivered_but_not_selected_fails_before_mutation" in executor_tests)
    check("executor:instrument_validation_code",
          "math.isfinite" in executor_source
          and "registry_scope" in executor_source
          and "FULL_REGISTRATION_FIELDS" in executor_source
          and "test_invalid_telemetry_is_unknown_not_negative_or_positive" in executor_tests
          and "test_invalid_thresholds_rejected_at_registration" in executor_tests
          and "test_instrument_registry_scope_and_full_preregistration_enforcement" in executor_tests)
    check("executor:availability_expiry_positive_test",
          "test_first_available_period_expiry_restores_availability" in executor_tests)
    check("executor:fixture_is_synthetic_instrument_fixture",
          json.loads((ROOT / "sim/sea_sap/fixtures/longitudinal.json").read_text(encoding="utf-8"))
          ["attendance_instrument"]["registry_scope"] == "synthetic_instrument_fixture"
          and longitudinal.get("instrument_registry_scope") == "synthetic_instrument_fixture")
    # Functional re-check of the review's counterexamples (semantic, not string):
    # v1.13 review: invalid telemetry -> unknown; delivered-not-selected -> no mutation.
    # v1.14 review: unregistered-arbitrary-v999 switch without authorization;
    #               parallel control paths after a continuity switch.
    sys.path.insert(0, str(ROOT / "sim"))
    try:
        import copy as _copy
        from sea_sap import SAPExecutor, load_fixture, completed_measurement_transport
        from sea_sap.executor import OperationalAttendanceInstrument
        fixture = load_fixture()
        instrument = OperationalAttendanceInstrument(fixture["attendance_instrument"])
        base_event = fixture["period_plans"]["0"]["attendance_events"]["c1"]
        statuses = [instrument.measure(dict(base_event, coverage_fraction=value)).status
                    for value in (float("nan"), float("inf"), 1.5)]
        probe = SAPExecutor(fixture)
        rejected = False
        try:
            probe.run_period(0, {"delivered": ["c1", "c3"], "opened": ["c1", "c3"],
                                 "attendance_events": {"c1": base_event, "c3": base_event},
                                 "machine_events": {}})
        except ValueError:
            rejected = True
        check("executor:review_counterexamples_functional",
              statuses == ["unknown", "unknown", "unknown"] and rejected
              and probe.governance.audit_records() == []
              and all(value == 0 for value in probe.budget_spent.values()),
              str(statuses))
        # Counterexample 1: caller-defined non-family registry without actor/authorization.
        probe2 = SAPExecutor(fixture)
        arbitrary = _copy.deepcopy(fixture["protocol_registries"]["targets-v2"])
        arbitrary["version"] = "unregistered-arbitrary-v999"
        arbitrary_rejected = False
        try:
            probe2.continue_with_target_registry(arbitrary)
        except ValueError:
            arbitrary_rejected = True
        records2 = probe2.governance.audit_records()
        # Counterexample 2: after a legal protocol switch the predecessor must be sealed
        # and the budget unique; no parallel active control path may exist.
        probe3 = SAPExecutor(fixture)
        probe3.run_period(0, fixture["period_plans"]["0"])
        continued3 = probe3.continue_with_target_registry(fixture["protocol_registries"]["targets-v2"])
        sealed_reuse_rejected = False
        try:
            probe3.run_period(1, fixture["period_plans"]["1"])
        except RuntimeError:
            sealed_reuse_rejected = True
        transport_ok = math.isclose(
            completed_measurement_transport(0.13, 0.9, 0.95)["m_D"], 0.03 / 0.85)
        warning_ok = completed_measurement_transport(0.4, 0.55, 0.5)["precision_warning"]
        check("executor:v114_review_counterexamples_functional",
              arbitrary_rejected
              and len(records2) == 1 and records2[0]["event"] == "registry_switch_rejected"
              and records2[0]["payload"]["reason"] == "version_not_in_registry_family"
              and all(value == 0 for value in probe2.budget_spent.values())
              and probe2.registry["version"] == "targets-v1"
              and sealed_reuse_rejected and probe3._sealed and not continued3._sealed
              and continued3.budget_remaining is probe3.budget_remaining
              and continued3.control_instance_id == probe3.control_instance_id
              and transport_ok and warning_ok)
    except Exception as exc:  # noqa: BLE001 - audit must report, not crash
        check("executor:review_counterexamples_functional", False, repr(exc))
        check("executor:v114_review_counterexamples_functional", False, repr(exc))
    # Functional re-check of the v1.15 review's three precise concerns (semantic):
    # (1) a rejection appends exactly one ledger record with precise state-effect
    #     fields (not "whole state unmutated"); (2) switch timing is frozen and
    #     enforced (early/late/tampered rejected); (3) full reset is a declared
    #     exception (undeclared target rejected; backward reset = new instance).
    try:
        from sea_sap import SAPExecutor as _SAP, load_fixture as _load
        fx = _load()
        v2 = fx["protocol_registries"]["targets-v2"]
        v1 = fx["target_registry"]
        # (1) rejection ledger growth + precise payload, zero spend, path unchanged.
        rj = _SAP(fx)
        n_before = len(rj.governance.audit_records())
        try:
            rj.continue_with_target_registry(v2)  # early: no period completed
            early_rejected = False
        except ValueError:
            early_rejected = True
        rj_records = rj.governance.audit_records()
        rj_payload = rj_records[-1]["payload"]
        rejection_precise = (
            early_rejected and len(rj_records) == n_before + 1
            and rj_records[-1]["event"] == "registry_switch_rejected"
            and rj_payload["reason"] == "switch_timing_mismatch"
            and rj_payload["registry_objective_budget_mutated"] is False
            and rj_payload["active_path_mutated"] is False
            and rj_payload["rejection_audit_record_appended"] is True
            and rj_payload["resources_spent"] == 0
            and "state_mutated" not in rj_payload
            and all(v == 0 for v in rj.budget_spent.values())
            and not rj._sealed and rj.registry["version"] == "targets-v1")
        # (2) late attempt and outcome-motivated timing edit both rejected.
        late = _SAP(fx)
        late.run_period(0, fx["period_plans"]["0"])
        late.run_period(1, fx["period_plans"]["1"])
        try:
            late.continue_with_target_registry(v2)
            late_rejected = False
        except ValueError as exc:
            late_rejected = "switch_timing_mismatch" in str(exc)
        tamper = _SAP(fx)
        tamper.run_period(0, fx["period_plans"]["0"])
        tamper.protocol_switch_timing["targets-v2"] = 1
        try:
            tamper.continue_with_target_registry(v2)
            tamper_rejected = False
        except ValueError as exc:
            tamper_rejected = "protocol_declaration_tampered" in str(exc)
        # (3) undeclared reset target rejected; declared backward reset = new instance.
        narrow = _load()
        narrow["protocol_reset_targets"] = ["targets-v2"]
        nr = _SAP(narrow)
        try:
            nr.fork_for_target_registry(v1)
            undeclared_reset_rejected = False
        except ValueError as exc:
            undeclared_reset_rejected = "reset_target_not_declared" in str(exc)
        ok = _SAP(fx)
        ok.run_period(0, fx["period_plans"]["0"])
        cont = ok.continue_with_target_registry(v2)
        back = cont.fork_for_target_registry(v1)
        backward_reset_ok = (
            back.registry["version"] == "targets-v1"
            and back.protocol_registry_schedule == ["targets-v1"]
            and back.protocol_switch_timing == {}
            and back.control_instance_id != cont.control_instance_id
            and back.governance is not cont.governance
            and cont._sealed and not back._sealed
            and cont.registry["version"] == "targets-v2")
        check("executor:v115_review_counterexamples_functional",
              rejection_precise and late_rejected and tamper_rejected
              and undeclared_reset_rejected and backward_reset_ok)
    except Exception as exc:  # noqa: BLE001
        check("executor:v115_review_counterexamples_functional", False, repr(exc))
    check("supplement:single_source_retrospective",
          "Supplementary Table SB1" not in formal and "26,908" not in formal
          and "Supplementary Table SB1" in supplement and "26,908" in supplement
          and "single-source pointer" in formal)
    generator = subprocess.run([sys.executable, str(ROOT / "tools/make_retrospective_tables.py")],
                               capture_output=True, text=True, cwd=ROOT)
    check("supplement:r5_generator_no_drift", generator.returncode == 0,
          generator.stdout.strip() or generator.stderr.strip())
    check("supplement:transport_identity_S12", "\\tag{S12}" in formal
          and "se_a+sp_a>1" in formal and "explicit-error-model transport" in formal)
    check("protocol:misclassification_validation_plan",
          "### 1.4.1 误分类验证与臂间误差比较" in protocol
          and "敏感度" in protocol and "特异度" in protocol and "臂间误差差异" in protocol
          and "(S12)" in protocol and "synthetic_instrument_fixture" in protocol)
    check("reproducibility:executor_count_and_generator",
          "41 项纵向执行器回归" in reproducibility
          and "make_retrospective_tables.py" in reproducibility
          and "audit_v116.py" in reproducibility
          and "make_v116_manifest.py" in reproducibility
          and "make_v114_manifest.py" not in reproducibility)

    pdf = ROOT / "latex/SEA_EN_v1.16_draft.pdf"
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
        "schema": "sea.v116.release-audit/v1", "n_checks": len(checks),
        "n_passed": len(checks) - len(failed), "n_failed": len(failed),
        "status": "PASS" if not failed else "FAIL", "failures": failed,
        "scope": "Internal consistency only; not independent proof, reproduction, or effectiveness validation.",
        "checks": checks,
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"v1.16 audit: {report['n_passed']}/{report['n_checks']} passed; failures={len(failed)}")
    for failure in failed:
        print("FAIL", failure["name"], failure["detail"])
    print(f"report: {REPORT}")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
