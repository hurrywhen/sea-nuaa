"""Tests for the v1.17 minimal longitudinal SAP executor and measurement rules."""
from __future__ import annotations

import copy
import hashlib
import json
import unittest

from sea_governance import canonical_json
from sea_sap import (
    SAPExecutor,
    completed_measurement_transport,
    completed_measurement_transport_delta_method,
    completed_measurement_transport_joint_bootstrap,
    completed_measurement_transport_sensitivity_grid,
    load_fixture,
    machine_ingestion_and_task_reference,
    operational_attendance_contrast_bounds,
    run_longitudinal_fixture,
    run_matched_implementation_demo,
    run_protocol_registry_switch_demo,
    transportability_stratified_diagnostics,
)
from sea_sap.executor import OperationalAttendanceInstrument, validate_target_registry


def _refresh_registry_hash(registry):
    registry["reference_corpus"]["sha256"] = hashlib.sha256(
        canonical_json(registry["reference_corpus"]["documents"]).encode("utf-8")
    ).hexdigest()


def _refresh_protocol_declaration(fixture):
    """Re-declare the frozen family after a test-local registry modification.

    Modifying a frozen registry invalidates its ex-ante content-hash
    declaration; a test that changes registry content must re-declare the
    family exactly as a protocol amendment would, not silently bypass it.
    """
    family = fixture["registry_family"]
    family[fixture["target_registry"]["version"]] = hashlib.sha256(
        canonical_json(fixture["target_registry"]).encode("utf-8")).hexdigest()
    for version, registry in fixture.get("protocol_registries", {}).items():
        family[version] = hashlib.sha256(canonical_json(registry).encode("utf-8")).hexdigest()


def _validated_instrument_registry(base):
    """A structurally complete preregistered instrument registration (synthetic values)."""
    registry = copy.deepcopy(base)
    registry["validation_status"] = "validated"
    registry["registry_scope"] = "preregistered_instrument"
    registry["assessor_blinding"] = "arm_and_model_blind"
    registry.update({
        "raw_event_schema": {"required_fields": [
            "focused_visible", "engaged_ms", "coverage_fraction",
            "content_linked_confirmation", "evidence_pointer"]},
        "validation_data_sha256": "a" * 64,
        "measurement_code_sha256": "b" * 64,
        "measurement_error": {
            "sensitivity": 0.9, "sensitivity_interval": [0.8, 0.95],
            "specificity": 0.95, "specificity_interval": [0.9, 0.98],
            "validation_set_pointer": "synthetic-validation:set-1",
            "transportability_assumption": "error rates conditionally stable across validation and deployment populations",
        },
        "blinded_reference_set": {
            "construction_rule": "independent time-outside units, arm-and-model-blind human reference annotation",
            "reference_data_sha256": "c" * 64,
            "unlock_timestamp": "logical:00000001",
            "overlap_with_tuning_or_main_corpus": False,
        },
        "completion_subset_representativeness": "completed-measurement subset compared with all assigned units by arm and stage",
        "alternative_instruments": ["reading_only", "confirmation_only"],
    })
    return registry


class LongitudinalExecutorTest(unittest.TestCase):
    def test_fixture_and_reference_corpus_are_valid(self):
        fixture = load_fixture()
        validate_target_registry(fixture["target_registry"])
        self.assertEqual(fixture["evidence_scope"], "SYNTHETIC_FIXTURE__NOT_HUMAN_OR_DEPLOYMENT_DATA")
        self.assertIn("reference_link_truth", fixture)
        self.assertIn("staged_link_pass", fixture)

    def test_longitudinal_run_exercises_guard_budgets_and_audit(self):
        result = run_longitudinal_fixture()
        self.assertTrue(all(result["guard_trace"].values()))
        self.assertTrue(result["audit"]["verification"]["valid"])
        self.assertEqual(len(result["periods"]), 2)
        self.assertTrue(all(value > 0 for value in result["budget"]["spent"].values()))
        self.assertEqual(result["new_real_model_calls"], 0)
        self.assertFalse(result["latent_actual_consumption_observed"])
        self.assertIn("NOT_LATENT", result["ledger_scope"])

    def test_operational_ledger_partitions_omission_and_keeps_latent_unobserved(self):
        result = run_longitudinal_fixture()
        first, second = result["periods"]
        self.assertAlmostEqual(first["outcome_summary"]["weighted_fc_omission"], 5 / 6)
        self.assertAlmostEqual(second["outcome_summary"]["weighted_fc_omission"], 1.0)
        self.assertAlmostEqual(second["outcome_summary"]["weighted_unknown_terminal"], 1 / 6)
        for period in (first, second):
            ledger = period["operational_target_ledger"]
            stages = [row["first_failed_stage"] for row in ledger]
            omitted = [row for row in ledger if row["failure_composite_omission"]]
            self.assertEqual(len(omitted), sum(stage is not None for stage in stages))
            self.assertTrue(all(row["latent_actual_consumption"] is None for row in ledger))
            self.assertIn("OPERATIONAL", period["outcome_summary"]["ledger_scope"])

    def test_operational_attendance_and_machine_placeholder_are_distinct(self):
        fixture = load_fixture()
        instrument = OperationalAttendanceInstrument(fixture["attendance_instrument"])
        positive = instrument.measure(fixture["period_plans"]["0"]["attendance_events"]["c1"])
        negative = instrument.measure(fixture["period_plans"]["0"]["attendance_events"]["c2"])
        unknown = instrument.measure(fixture["period_plans"]["1"]["attendance_events"]["c2"])
        self.assertEqual(positive.status, "positive")
        self.assertEqual(negative.status, "negative")
        self.assertEqual(unknown.status, "unknown")
        machine = fixture["period_plans"]["0"]["machine_events"]["c1"]
        self.assertTrue(machine_ingestion_and_task_reference(machine))
        bad = dict(machine, task_reference_sha256="0" * 64)
        self.assertFalse(machine_ingestion_and_task_reference(bad))
        result = run_longitudinal_fixture()
        self.assertTrue(result["periods"][0]["outcome_summary"]["machine_ingestion_and_task_reference"]["c1"])
        self.assertIn("synthetic placeholder", result["periods"][0]["outcome_summary"]["machine_event_interpretation"])

    def test_bounds_are_operational_not_latent_and_misclassification_counterexample(self):
        bounds = operational_attendance_contrast_bounds(
            {"sea": 0.5, "control": 0.4}, {"sea": 0.2, "control": 0.1})
        self.assertEqual(bounds["estimand"],
                         "operational_attendance_omission_contrast_not_latent_actual_consumption")
        self.assertAlmostEqual(bounds["sea_minus_control_fc"], 0.1)
        self.assertAlmostEqual(bounds["lower_sea_unknown_operational_success_control_unknown_failure"], -0.1)
        self.assertAlmostEqual(bounds["upper_sea_unknown_operational_failure_control_unknown_success"], 0.2)
        self.assertTrue(bounds["latent_bounds_require_measurement_error_assumptions"])
        # No unknowns AND zero FC contrast: operational bounds collapse to [0,0]
        # (in general they collapse to [Delta^FC, Delta^FC]).  A false positive in
        # SEA (Z=1, D=0) and true positive in control (Z=1, D=1) gives latent
        # omission contrast 1, outside the operational bounds.  A false negative
        # in control gives the reverse violation.  Hence the bounds are not latent.
        no_unknown = operational_attendance_contrast_bounds(
            {"sea": 0.0, "control": 0.0}, {"sea": 0.0, "control": 0.0})
        self.assertAlmostEqual(no_unknown["lower_sea_unknown_operational_success_control_unknown_failure"], 0.0)
        self.assertAlmostEqual(no_unknown["upper_sea_unknown_operational_failure_control_unknown_success"], 0.0)
        latent_false_positive_contrast = 1.0
        self.assertFalse(no_unknown["lower_sea_unknown_operational_success_control_unknown_failure"]
                         <= latent_false_positive_contrast
                         <= no_unknown["upper_sea_unknown_operational_failure_control_unknown_success"])
        # False-negative counterexample (no unknowns): control has a complete
        # negative measurement Z=0 while latent D=1, sea has Z=1, D=1.  Then
        # FC omission is sea=0, control=1, so the operational bounds are [-1,-1],
        # but both arms actually consumed: latent omission contrast is 0, outside.
        false_negative = operational_attendance_contrast_bounds(
            {"sea": 0.0, "control": 1.0}, {"sea": 0.0, "control": 0.0})
        self.assertAlmostEqual(false_negative["lower_sea_unknown_operational_success_control_unknown_failure"], -1.0)
        self.assertAlmostEqual(false_negative["upper_sea_unknown_operational_failure_control_unknown_success"], -1.0)
        latent_false_negative_contrast = 0.0
        self.assertFalse(false_negative["lower_sea_unknown_operational_success_control_unknown_failure"]
                         <= latent_false_negative_contrast
                         <= false_negative["upper_sea_unknown_operational_failure_control_unknown_success"])
        with self.assertRaises(ValueError):
            operational_attendance_contrast_bounds({"sea": 0.1, "control": 0.1}, {"sea": 0.2, "control": 0.0})

    def test_delayed_first_available_period_changes_longitudinal_availability(self):
        fixture = load_fixture()
        registry = fixture["target_registry"]
        for doc in registry["reference_corpus"]["documents"]:
            if doc["document_id"] == "doc2":
                doc["first_available_period"] = 2
        _refresh_registry_hash(registry)
        _refresh_protocol_declaration(fixture)
        executor = SAPExecutor(fixture, arm="sea")
        positive = fixture["period_plans"]["0"]["attendance_events"]["c1"]
        plan = {"delivered": ["c1"], "opened": ["c1"],
                "attendance_events": {"c1": positive}, "machine_events": {}}
        period0 = executor.run_period(0, plan)
        e2 = next(row for row in period0["operational_target_ledger"] if row["target_id"] == "e2")
        self.assertEqual(e2["first_failed_stage"], "availability")
        self.assertEqual(e2["available_candidate_ids"], [])
        period1 = executor.run_period(1, plan)
        e2_1 = next(row for row in period1["operational_target_ledger"] if row["target_id"] == "e2")
        self.assertEqual(e2_1["first_failed_stage"], "availability")
        self.assertAlmostEqual(period1["outcome_summary"]["weighted_unknown_terminal"], 0.0)

    def test_first_available_period_expiry_restores_availability(self):
        fixture = load_fixture()
        registry = fixture["target_registry"]
        for doc in registry["reference_corpus"]["documents"]:
            if doc["document_id"] == "doc2":
                doc["first_available_period"] = 1
        _refresh_registry_hash(registry)
        _refresh_protocol_declaration(fixture)
        executor = SAPExecutor(fixture, arm="sea")
        positive_c1 = fixture["period_plans"]["0"]["attendance_events"]["c1"]
        positive_c2 = dict(positive_c1, evidence_pointer="synthetic-attendance:c2-positive-period1")
        plan0 = {"delivered": ["c1"], "opened": ["c1"],
                 "attendance_events": {"c1": positive_c1}, "machine_events": {}}
        period0 = executor.run_period(0, plan0)
        e2 = next(row for row in period0["operational_target_ledger"] if row["target_id"] == "e2")
        self.assertEqual(e2["first_failed_stage"], "availability")
        self.assertEqual(e2["available_candidate_ids"], [])
        plan1 = {"delivered": ["c1", "c2"], "opened": ["c1", "c2"],
                 "attendance_events": {"c1": positive_c1, "c2": positive_c2},
                 "machine_events": {}}
        period1 = executor.run_period(1, plan1)
        e2_1 = next(row for row in period1["operational_target_ledger"] if row["target_id"] == "e2")
        self.assertIn("c2", e2_1["available_candidate_ids"])
        self.assertIsNone(e2_1["first_failed_stage"])
        self.assertEqual(e2_1["operational_attendance"], "positive")
        self.assertAlmostEqual(period1["outcome_summary"]["weighted_unknown_terminal"], 0.0)

    def test_invalid_telemetry_is_unknown_not_negative_or_positive(self):
        fixture = load_fixture()
        instrument = OperationalAttendanceInstrument(fixture["attendance_instrument"])
        base = fixture["period_plans"]["0"]["attendance_events"]["c1"]
        cases = [
            dict(base, coverage_fraction=float("nan")),
            dict(base, coverage_fraction=float("inf")),
            dict(base, coverage_fraction=float("-inf")),
            dict(base, coverage_fraction=1.5),
            dict(base, coverage_fraction=-0.1),
            dict(base, engaged_ms=float("nan")),
            dict(base, engaged_ms=float("inf")),
            dict(base, engaged_ms=-1),
            dict(base, engaged_ms="45000"),
            dict(base, coverage_fraction=True),
            dict(base, evidence_pointer=""),
            dict(base, evidence_pointer="   "),
            dict(base, evidence_pointer=None),
            dict(base, focused_visible="yes"),
            dict(base, content_linked_confirmation="true"),
        ]
        for event in cases:
            decision = instrument.measure(event)
            self.assertEqual(decision.status, "unknown", str(event))
            self.assertEqual(decision.reason, "invalid_telemetry_values")
        # A complete valid measurement below threshold remains negative, not unknown.
        negative = fixture["period_plans"]["0"]["attendance_events"]["c2"]
        self.assertEqual(instrument.measure(negative).status, "negative")

    def test_invalid_thresholds_rejected_at_registration(self):
        fixture = load_fixture()
        for thresholds in (
            {"min_engaged_ms": float("nan"), "min_coverage_fraction": 0.6},
            {"min_engaged_ms": 30000, "min_coverage_fraction": float("inf")},
            {"min_engaged_ms": -1, "min_coverage_fraction": 0.6},
            {"min_engaged_ms": 30000, "min_coverage_fraction": 1.5},
            {"min_engaged_ms": 30000, "min_coverage_fraction": -0.2},
            {"min_engaged_ms": 30000},
        ):
            registry = copy.deepcopy(fixture["attendance_instrument"])
            registry["thresholds"] = thresholds
            with self.assertRaises(ValueError):
                OperationalAttendanceInstrument(registry)

    def test_instrument_registry_scope_and_full_preregistration_enforcement(self):
        fixture = load_fixture()
        base = fixture["attendance_instrument"]
        self.assertEqual(base["registry_scope"], "synthetic_instrument_fixture")
        registry = copy.deepcopy(base)
        registry["registry_scope"] = "preregistered_instrument"
        with self.assertRaises(ValueError):
            OperationalAttendanceInstrument(registry)
        registry = copy.deepcopy(base)
        registry["validation_status"] = "validated"
        registry["registry_scope"] = "preregistered_instrument"
        registry["assessor_blinding"] = "arm_and_model_blind"
        with self.assertRaises(ValueError):
            OperationalAttendanceInstrument(registry)
        registry = _validated_instrument_registry(base)
        instrument = OperationalAttendanceInstrument(registry)
        positive = fixture["period_plans"]["0"]["attendance_events"]["c1"]
        self.assertEqual(instrument.measure(positive).status, "positive")
        bad = copy.deepcopy(registry)
        bad["measurement_error"] = {"sensitivity": 0.9}
        with self.assertRaises(ValueError):
            OperationalAttendanceInstrument(bad)
        bad = copy.deepcopy(registry)
        bad["measurement_error"]["sensitivity"] = float("nan")
        with self.assertRaises(ValueError):
            OperationalAttendanceInstrument(bad)

    def test_validated_instrument_hashes_must_be_true_hex(self):
        fixture = load_fixture()
        registry = _validated_instrument_registry(fixture["attendance_instrument"])
        for field in ("validation_data_sha256", "measurement_code_sha256"):
            for bad_value in ("g" * 64, "A" * 64, "a" * 63, "a" * 65, "a" * 62 + "zz", 123):
                bad = copy.deepcopy(registry)
                bad[field] = bad_value
                with self.assertRaises(ValueError):
                    OperationalAttendanceInstrument(bad)
        bad = copy.deepcopy(registry)
        bad["blinded_reference_set"]["reference_data_sha256"] = "z" * 64
        with self.assertRaises(ValueError):
            OperationalAttendanceInstrument(bad)

    def test_validated_instrument_requires_uncertainty_and_transportability(self):
        fixture = load_fixture()
        registry = _validated_instrument_registry(fixture["attendance_instrument"])
        for key in ("sensitivity_interval", "specificity_interval"):
            bad = copy.deepcopy(registry)
            del bad["measurement_error"][key]
            with self.assertRaises(ValueError):
                OperationalAttendanceInstrument(bad)
        for bad_interval in ([0.95, 0.8], [0.85, 0.88], [-0.1, 0.95], [0.8, 1.2],
                             [0.8, float("nan")], [0.8], [True, 0.95]):
            bad = copy.deepcopy(registry)
            bad["measurement_error"]["sensitivity_interval"] = bad_interval
            with self.assertRaises(ValueError):
                OperationalAttendanceInstrument(bad)
        bad = copy.deepcopy(registry)
        del bad["measurement_error"]["transportability_assumption"]
        with self.assertRaises(ValueError):
            OperationalAttendanceInstrument(bad)
        bad = copy.deepcopy(registry)
        bad["measurement_error"]["transportability_assumption"] = "   "
        with self.assertRaises(ValueError):
            OperationalAttendanceInstrument(bad)

    def test_validated_instrument_requires_blinded_reference_set_and_representativeness(self):
        fixture = load_fixture()
        registry = _validated_instrument_registry(fixture["attendance_instrument"])
        bad = copy.deepcopy(registry)
        del bad["blinded_reference_set"]
        with self.assertRaises(ValueError):
            OperationalAttendanceInstrument(bad)
        for field in ("construction_rule", "reference_data_sha256", "unlock_timestamp"):
            bad = copy.deepcopy(registry)
            del bad["blinded_reference_set"][field]
            with self.assertRaises(ValueError):
                OperationalAttendanceInstrument(bad)
        bad = copy.deepcopy(registry)
        bad["blinded_reference_set"]["overlap_with_tuning_or_main_corpus"] = True
        with self.assertRaises(ValueError):
            OperationalAttendanceInstrument(bad)
        bad = copy.deepcopy(registry)
        del bad["completion_subset_representativeness"]
        with self.assertRaises(ValueError):
            OperationalAttendanceInstrument(bad)
        bad = copy.deepcopy(registry)
        bad["completion_subset_representativeness"] = ""
        with self.assertRaises(ValueError):
            OperationalAttendanceInstrument(bad)

    def test_delivered_but_not_selected_fails_before_mutation(self):
        fixture = load_fixture()
        executor = SAPExecutor(fixture)  # SEA: c3 fails staged linkage, is never selected
        before_records = executor.governance.audit_records()
        positive = fixture["period_plans"]["0"]["attendance_events"]["c1"]
        plan = {"delivered": ["c1", "c3"], "opened": ["c1", "c3"],
                "attendance_events": {"c1": positive, "c3": positive}, "machine_events": {}}
        with self.assertRaises(ValueError):
            executor.run_period(0, plan)
        self.assertEqual(executor.governance.audit_records(), before_records)
        self.assertEqual(executor.budget_spent, {name: 0 for name in executor.budget_spent})
        self.assertEqual(executor.updated_candidates, {})
        self.assertEqual(executor.period_results, [])
        # An eligible candidate beyond the selection limit is also rejected pre-mutation.
        fixture2 = load_fixture()
        fixture2["selection_limit"] = 1
        executor2 = SAPExecutor(fixture2)
        plan2 = {"delivered": ["c1", "c2"], "opened": ["c1"],
                 "attendance_events": {"c1": positive}, "machine_events": {}}
        with self.assertRaises(ValueError):
            executor2.run_period(0, plan2)
        self.assertEqual(executor2.governance.audit_records(), [])
        self.assertEqual(executor2.budget_spent, {name: 0 for name in executor2.budget_spent})
        self.assertEqual(executor2.updated_candidates, {})
        # The same plan with only selected candidates executes normally.
        period = executor2.run_period(0, {"delivered": ["c1"], "opened": ["c1"],
                                          "attendance_events": {"c1": positive},
                                          "machine_events": {}})
        self.assertEqual(period["selected_candidate_ids"], ["c1"])

    def test_all_audit_events_carry_cohort_attribution(self):
        fixture = load_fixture()
        executor = SAPExecutor(fixture)
        executor.run_period(0, fixture["period_plans"]["0"])
        executor.write_after_period({"weights": {"novelty": 10}},
                                    authorization_id="cohort-write", timestamp="logical:00000010")
        registry = copy.deepcopy(fixture["target_registry"])
        registry["version"] = "targets-v2"
        registry["targets"][0]["canonical_text"] = "Revised synthetic proposition e1."
        continued = executor.continue_with_target_registry(registry)
        continued.run_period(1, fixture["period_plans"]["0"])
        records = continued.governance.audit_records()
        keys = {"control_instance_id", "evaluation_cohort_id",
                "target_registry_version", "target_registry_sha256"}
        switch_index = next(i for i, record in enumerate(records)
                            if record["event"] == "evaluation_cohort_change")
        for index, record in enumerate(records):
            payload = record["payload"]
            if record["event"] == "evaluation_cohort_change":
                self.assertEqual(payload["control_instance_id"], executor.control_instance_id)
                self.assertEqual(payload["old_evaluation_cohort_id"], executor.evaluation_cohort_id)
                self.assertEqual(payload["new_evaluation_cohort_id"], continued.evaluation_cohort_id)
                self.assertEqual(payload["old_target_registry_version"], "targets-v1")
                self.assertEqual(payload["new_target_registry_version"], "targets-v2")
                continue
            self.assertTrue(keys <= set(payload), record["event"])
            self.assertEqual(payload["control_instance_id"], executor.control_instance_id)
            expected_cohort = (executor.evaluation_cohort_id if index < switch_index
                               else continued.evaluation_cohort_id)
            self.assertEqual(payload["evaluation_cohort_id"], expected_cohort, record["event"])
            expected_version = "targets-v1" if index < switch_index else "targets-v2"
            self.assertEqual(payload["target_registry_version"], expected_version)
        self.assertTrue(continued.governance.verify_audit(
            anchor=continued.governance.audit_anchor())["valid"])

    def test_s2d_can_select_staged_link_failure_but_evaluation_uses_reference_truth(self):
        fixture = load_fixture()
        fixture["staged_link_pass"]["c3"] = {"e3": False, "e4": False}
        fixture["reference_link_truth"]["c3"] = {"e3": True, "e4": True}
        fixture["run_id"] = "s2d-link-truth-test"
        executor = SAPExecutor(fixture, arm="s2d")
        positive = fixture["period_plans"]["0"]["attendance_events"]["c1"]
        plan = {
            "delivered": ["c1", "c3"], "opened": ["c1", "c3"],
            "attendance_events": {"c1": positive, "c3": positive},
            "machine_events": {},
        }
        period = executor.run_period(0, plan)
        self.assertIn("c3", period["selected_candidate_ids"])
        e3 = next(row for row in period["operational_target_ledger"] if row["target_id"] == "e3")
        self.assertIn("c3", e3["linked_candidate_ids"])
        self.assertIsNone(e3["first_failed_stage"])
        sea_fixture = copy.deepcopy(fixture)
        sea_fixture["run_id"] = "sea-link-truth-test"
        sea = SAPExecutor(sea_fixture, arm="sea")
        sea_period = sea.run_period(0, {"delivered": ["c1"], "opened": ["c1"],
                                        "attendance_events": {"c1": positive}, "machine_events": {}})
        self.assertNotIn("c3", sea_period["selected_candidate_ids"])

    def test_whole_period_resource_precheck_fails_before_mutation(self):
        fixture = load_fixture()
        fixture["initial_budget"]["time"] = 0
        executor = SAPExecutor(fixture)
        before_records = executor.governance.audit_records()
        with self.assertRaises(RuntimeError):
            executor.run_period(0, fixture["period_plans"]["0"])
        self.assertEqual(executor.governance.audit_records(), before_records)
        self.assertEqual(executor.budget_spent, {name: 0 for name in executor.budget_spent})

    def test_invalid_terminal_plan_fails_before_mutation(self):
        fixture = load_fixture()
        executor = SAPExecutor(fixture)
        before_records = executor.governance.audit_records()
        unknown_candidate = {"delivered": ["c1", "no-such-candidate"], "opened": ["c1"],
                             "attendance_events": {}, "machine_events": {}}
        with self.assertRaises(ValueError):
            executor.run_period(0, unknown_candidate)
        opened_not_delivered = {"delivered": ["c1"], "opened": ["c1", "c2"],
                                "attendance_events": {}, "machine_events": {}}
        with self.assertRaises(ValueError):
            executor.run_period(0, opened_not_delivered)
        self.assertEqual(executor.governance.audit_records(), before_records)
        self.assertEqual(executor.budget_spent, {name: 0 for name in executor.budget_spent})

    def test_control_continuity_and_evaluation_cohort_are_separate(self):
        fixture = load_fixture()
        executor = SAPExecutor(fixture)
        executor.run_period(0, fixture["period_plans"]["0"])
        registry = fixture["protocol_registries"]["targets-v2"]
        continued = executor.continue_with_target_registry(registry)
        self.assertEqual(continued.control_instance_id, executor.control_instance_id)
        self.assertNotEqual(continued.evaluation_cohort_id, executor.evaluation_cohort_id)
        self.assertIs(continued.governance, executor.governance)
        # Single-line control: unique shared budget/history state, not copies.
        self.assertIs(continued.budget_remaining, executor.budget_remaining)
        self.assertIs(continued.budget_spent, executor.budget_spent)
        self.assertIs(continued.history, executor.history)
        self.assertEqual(continued.budget_remaining, executor.budget_remaining)
        self.assertEqual(continued.registry["version"], "targets-v2")
        # The predecessor is sealed; the successor is the only active path.
        with self.assertRaises(RuntimeError):
            executor.run_period(1, fixture["period_plans"]["1"])
        forked = continued.fork_for_target_registry(registry)
        self.assertNotEqual(forked.control_instance_id, continued.control_instance_id)
        self.assertEqual(forked.budget_spent, {name: 0 for name in forked.budget_spent})
        with self.assertRaises(RuntimeError):
            continued.run_period(1, fixture["period_plans"]["1"])
        forked.run_period(0, fixture["period_plans"]["0"])

    def test_non_family_registry_switch_is_rejected_with_record(self):
        fixture = load_fixture()
        executor = SAPExecutor(fixture)
        arbitrary = copy.deepcopy(fixture["target_registry"])
        arbitrary["version"] = "unregistered-arbitrary-v999"
        before_records = executor.governance.audit_records()
        before_budget = dict(executor.budget_remaining)
        with self.assertRaises(ValueError) as caught:
            executor.continue_with_target_registry(arbitrary)
        self.assertIn("version_not_in_registry_family", str(caught.exception))
        records = executor.governance.audit_records()
        self.assertEqual(len(records), len(before_records) + 1)
        self.assertEqual(records[-1]["event"], "registry_switch_rejected")
        payload = records[-1]["payload"]
        self.assertEqual(payload["attempted_target_registry_version"], "unregistered-arbitrary-v999")
        self.assertFalse(payload["policy_action"])
        self.assertFalse(payload["registry_objective_budget_mutated"])
        self.assertFalse(payload["active_path_mutated"])
        self.assertTrue(payload["rejection_audit_record_appended"])
        self.assertEqual(payload["resources_spent"], 0)
        self.assertEqual(payload["control_instance_id"], executor.control_instance_id)
        self.assertEqual(executor.budget_remaining, before_budget)
        self.assertEqual(executor.budget_spent, {name: 0 for name in executor.budget_spent})
        self.assertFalse(executor._sealed)
        self.assertEqual(executor.registry["version"], "targets-v1")
        # The same attempt via fork is rejected identically.
        with self.assertRaises(ValueError):
            executor.fork_for_target_registry(arbitrary)

    def test_tampered_family_registry_hash_mismatch_is_rejected(self):
        fixture = load_fixture()
        executor = SAPExecutor(fixture)
        tampered = copy.deepcopy(fixture["protocol_registries"]["targets-v2"])
        tampered["targets"][0]["canonical_text"] = "Tampered proposition text."
        with self.assertRaises(ValueError) as caught:
            executor.continue_with_target_registry(tampered)
        self.assertIn("registry_content_hash_mismatch", str(caught.exception))
        records = executor.governance.audit_records()
        self.assertEqual(records[-1]["event"], "registry_switch_rejected")
        self.assertEqual(records[-1]["payload"]["reason"], "registry_content_hash_mismatch")
        self.assertFalse(executor._sealed)
        self.assertEqual(executor.budget_spent, {name: 0 for name in executor.budget_spent})

    def test_out_of_schedule_switch_is_rejected(self):
        fixture = load_fixture()
        executor = SAPExecutor(fixture)
        executor.run_period(0, fixture["period_plans"]["0"])
        registry_v2 = fixture["protocol_registries"]["targets-v2"]
        continued = executor.continue_with_target_registry(registry_v2)
        # Backward switch to the previous scheduled version is not append-only forward.
        with self.assertRaises(ValueError) as caught:
            continued.continue_with_target_registry(fixture["target_registry"])
        self.assertIn("version_not_next_in_protocol_schedule", str(caught.exception))
        # No further scheduled version exists after the last one.
        with self.assertRaises(ValueError) as caught:
            continued.continue_with_target_registry(registry_v2)
        self.assertIn("version_not_next_in_protocol_schedule", str(caught.exception))
        self.assertEqual(continued.registry["version"], "targets-v2")
        self.assertFalse(continued._sealed)

    def test_sealed_predecessor_cannot_run_write_rollback_or_switch(self):
        fixture = load_fixture()
        executor = SAPExecutor(fixture)
        executor.run_period(0, fixture["period_plans"]["0"])
        continued = executor.continue_with_target_registry(fixture["protocol_registries"]["targets-v2"])
        for call in (
            lambda: executor.run_period(1, fixture["period_plans"]["1"]),
            lambda: executor.write_after_period({"weights": {"novelty": 9}},
                                                authorization_id="sealed-write",
                                                timestamp="logical:00000030"),
            lambda: executor.rollback_after_period(0, authorization_id="sealed-rollback",
                                                   timestamp="logical:00000031"),
        ):
            with self.assertRaises(RuntimeError):
                call()
        with self.assertRaises(ValueError) as caught:
            executor.continue_with_target_registry(fixture["protocol_registries"]["targets-v2"])
        self.assertIn("sealed_control_path", str(caught.exception))
        seal_records = [record for record in continued.governance.audit_records()
                        if record["event"] == "control_path_sealed"]
        self.assertEqual(len(seal_records), 1)
        self.assertEqual(seal_records[0]["payload"]["reason"], "protocol_registry_switch")
        self.assertEqual(seal_records[0]["payload"]["evaluation_cohort_id"], executor.evaluation_cohort_id)
        self.assertEqual(seal_records[0]["payload"]["successor_evaluation_cohort_id"],
                         continued.evaluation_cohort_id)
        # The successor keeps running on the unique shared budget.
        continued.run_period(1, fixture["period_plans"]["1"])
        self.assertTrue(all(value > 0 for value in executor.budget_spent.values()))

    def test_objective_rollback_does_not_restore_registry_version(self):
        fixture = load_fixture()
        executor = SAPExecutor(fixture)
        executor.run_period(0, fixture["period_plans"]["0"])
        executor.write_after_period({"weights": {"novelty": 10}},
                                    authorization_id="rollback-independence-write",
                                    timestamp="logical:00000010")
        continued = executor.continue_with_target_registry(fixture["protocol_registries"]["targets-v2"])
        restored = continued.rollback_after_period(
            0, authorization_id="rollback-independence-rollback", timestamp="logical:00000020")
        self.assertTrue(restored["accepted"])
        self.assertEqual(continued.registry["version"], "targets-v2")
        self.assertEqual(continued.registry_sha256,
                         fixture["registry_family"]["targets-v2"])
        self.assertEqual(continued.governance.inspect_objective()["version"], restored["version"])
        self.assertEqual(continued.governance.inspect_objective()["objective"]["weights"]["novelty"], 2)

    def test_switch_without_family_declaration_is_rejected(self):
        fixture = load_fixture()
        del fixture["registry_family"]
        del fixture["protocol_registry_schedule"]
        del fixture["protocol_registries"]
        del fixture["protocol_switch_timing"]
        del fixture["protocol_reset_targets"]
        executor = SAPExecutor(fixture)
        self.assertEqual(executor.protocol_registry_schedule, ["targets-v1"])
        registry_v2 = copy.deepcopy(fixture["target_registry"])
        registry_v2["version"] = "targets-v2"
        registry_v2["targets"][0]["canonical_text"] = "Revised synthetic proposition e1."
        with self.assertRaises(ValueError) as caught:
            executor.continue_with_target_registry(registry_v2)
        self.assertIn("version_not_in_registry_family", str(caught.exception))

    def test_frozen_family_declaration_is_verified_at_load(self):
        fixture = load_fixture()
        self.assertEqual(fixture["protocol_registry_schedule"], ["targets-v1", "targets-v2"])
        bad = copy.deepcopy(fixture)
        bad["registry_family"]["targets-v1"] = "0" * 64
        with self.assertRaises(ValueError):
            SAPExecutor(bad)
        bad = copy.deepcopy(fixture)
        bad["protocol_registry_schedule"] = ["targets-v2"]
        with self.assertRaises(ValueError):
            SAPExecutor(bad)  # active version must appear in the schedule
        bad = copy.deepcopy(fixture)
        bad["protocol_registry_schedule"] = ["targets-v1", "targets-v9"]
        with self.assertRaises(ValueError):
            SAPExecutor(bad)  # scheduled version outside the family
        bad = copy.deepcopy(fixture)
        bad["protocol_registries"]["targets-v2"]["targets"][0]["canonical_text"] = "Drifted content."
        with self.assertRaises(ValueError):
            SAPExecutor(bad)  # frozen content no longer matches the family hash

    def _assert_period_sequence_rejected_before_mutation(self, executor, period, plan):
        before = (executor.next_period, copy.deepcopy(executor.period_results),
                  copy.deepcopy(executor.history), executor.governance.audit_records(),
                  copy.deepcopy(executor.budget_remaining), copy.deepcopy(executor.budget_spent))
        with self.assertRaises(ValueError) as caught:
            executor.run_period(period, plan)
        self.assertIn("period sequence rejected", str(caught.exception))
        after = (executor.next_period, executor.period_results, executor.history,
                 executor.governance.audit_records(), executor.budget_remaining, executor.budget_spent)
        self.assertEqual(after, before)

    def test_duplicate_period_cannot_advance_frozen_switch_boundary(self):
        fixture = load_fixture()
        fixture["protocol_switch_timing"]["targets-v2"] = 1
        registry_v2 = fixture["protocol_registries"]["targets-v2"]
        executor = SAPExecutor(fixture)
        executor.run_period(0, fixture["period_plans"]["0"])
        self._assert_period_sequence_rejected_before_mutation(
            executor, 0, fixture["period_plans"]["0"])
        self.assertEqual(executor.next_period, 1)
        self.assertEqual(len(executor.period_results), 1)
        # The old counterexample stopped here: two period-0 result rows used to
        # satisfy switch_after_period=1.  Now the switch is still early.
        with self.assertRaises(ValueError) as caught:
            executor.continue_with_target_registry(registry_v2)
        self.assertIn("switch_timing_mismatch", str(caught.exception))
        payload = executor.governance.audit_records()[-1]["payload"]
        self.assertEqual(payload["completed_periods"], 1)
        self.assertEqual(payload["declared_switch_after_period"], 1)
        executor.run_period(1, fixture["period_plans"]["1"])
        continued = executor.continue_with_target_registry(registry_v2)
        self.assertEqual(continued.next_period, 2)
        self.assertEqual([row["period"] for row in continued.period_results], [0, 1])

    def test_regressed_period_is_rejected_before_mutation(self):
        fixture = load_fixture()
        executor = SAPExecutor(fixture)
        executor.run_period(0, fixture["period_plans"]["0"])
        executor.run_period(1, fixture["period_plans"]["1"])
        self._assert_period_sequence_rejected_before_mutation(
            executor, 0, fixture["period_plans"]["0"])
        self.assertEqual(executor.next_period, 2)

    def test_skipped_period_is_rejected_before_mutation(self):
        fixture = load_fixture()
        executor = SAPExecutor(fixture)
        for invalid in (-1, 1, True, 0.0, "0"):
            self._assert_period_sequence_rejected_before_mutation(
                executor, invalid, fixture["period_plans"]["0"])
        executor.run_period(0, fixture["period_plans"]["0"])
        for invalid in (2, 1.0, "1"):
            self._assert_period_sequence_rejected_before_mutation(
                executor, invalid, fixture["period_plans"]["1"])
        self.assertEqual(executor.next_period, 1)

    def test_old_period_after_switch_is_rejected_before_mutation(self):
        fixture = load_fixture()
        executor = SAPExecutor(fixture)
        executor.run_period(0, fixture["period_plans"]["0"])
        continued = executor.continue_with_target_registry(
            fixture["protocol_registries"]["targets-v2"])
        self._assert_period_sequence_rejected_before_mutation(
            continued, 0, fixture["period_plans"]["0"])
        self.assertEqual(continued.next_period, 1)
        continued.run_period(1, fixture["period_plans"]["1"])
        self.assertEqual(continued.next_period, 2)

    def test_period_clock_is_read_only_and_shared_history_cannot_drift(self):
        fixture = load_fixture()
        executor = SAPExecutor(fixture)
        # A caller cannot manufacture a completed period by assigning a clock.
        with self.assertRaises(AttributeError):
            setattr(executor, "next_period", 1)
        with self.assertRaises(ValueError):
            executor.continue_with_target_registry(fixture["protocol_registries"]["targets-v2"])
        executor.run_period(0, fixture["period_plans"]["0"])
        continued = executor.continue_with_target_registry(
            fixture["protocol_registries"]["targets-v2"])
        continued.run_period(1, fixture["period_plans"]["1"])
        self.assertEqual(continued.next_period, 2)
        self.assertEqual(executor.next_period, 2)  # sealed predecessor shares history
        self.assertEqual(len(executor.period_results), 2)
        # Directly corrupted duplicate rows are not a valid substitute for a clock.
        corrupt = SAPExecutor(fixture)
        corrupt.run_period(0, fixture["period_plans"]["0"])
        corrupt.period_results.append(copy.deepcopy(corrupt.period_results[0]))
        with self.assertRaisesRegex(RuntimeError, "period history integrity violation"):
            _ = corrupt.next_period
        with self.assertRaisesRegex(RuntimeError, "period history integrity violation"):
            corrupt.continue_with_target_registry(fixture["protocol_registries"]["targets-v2"])

    def test_switch_timing_is_frozen_and_enforced(self):
        fixture = load_fixture()
        registry_v2 = fixture["protocol_registries"]["targets-v2"]
        # Early attempt: no period completed yet, declared boundary is after period 0.
        early = SAPExecutor(fixture)
        with self.assertRaises(ValueError) as caught:
            early.continue_with_target_registry(registry_v2)
        self.assertIn("switch_timing_mismatch", str(caught.exception))
        payload = early.governance.audit_records()[-1]["payload"]
        self.assertEqual(payload["declared_switch_after_period"], 0)
        self.assertEqual(payload["completed_periods"], 0)
        self.assertFalse(payload["registry_objective_budget_mutated"])
        self.assertFalse(payload["active_path_mutated"])
        self.assertTrue(payload["rejection_audit_record_appended"])
        self.assertEqual(payload["resources_spent"], 0)
        self.assertEqual(early.budget_spent, {name: 0 for name in early.budget_spent})
        self.assertFalse(early._sealed)
        # Late attempt: the declared boundary was missed; timing cannot be renegotiated.
        late = SAPExecutor(fixture)
        late.run_period(0, fixture["period_plans"]["0"])
        late.run_period(1, fixture["period_plans"]["1"])
        with self.assertRaises(ValueError) as caught:
            late.continue_with_target_registry(registry_v2)
        self.assertIn("switch_timing_mismatch", str(caught.exception))
        self.assertEqual(late.governance.audit_records()[-1]["payload"]["completed_periods"], 2)
        # Accepted exactly at the frozen boundary.
        at_boundary = SAPExecutor(fixture)
        at_boundary.run_period(0, fixture["period_plans"]["0"])
        continued = at_boundary.continue_with_target_registry(registry_v2)
        self.assertEqual(continued.registry["version"], "targets-v2")

    def test_declaration_tampering_after_results_is_rejected(self):
        fixture = load_fixture()
        registry_v2 = fixture["protocol_registries"]["targets-v2"]
        control = SAPExecutor(fixture)
        control.run_period(0, fixture["period_plans"]["0"])
        mutations = (
            lambda ex: ex.protocol_switch_timing.__setitem__("targets-v2", 1),
            lambda ex: ex.protocol_registry_schedule.append("targets-v9"),
            lambda ex: ex.registry_family.__setitem__("targets-v9", "0" * 64),
            lambda ex: ex.protocol_reset_targets.remove("targets-v1"),
            lambda ex: ex._frozen_protocol_registries.clear(),
        )
        for mutate in mutations:
            executor = SAPExecutor(fixture)
            executor.run_period(0, fixture["period_plans"]["0"])
            mutate(executor)  # outcome-motivated edit after reading period-0 results
            with self.assertRaises(ValueError) as caught:
                executor.continue_with_target_registry(registry_v2)
            self.assertIn("protocol_declaration_tampered", str(caught.exception))
            with self.assertRaises(ValueError) as caught:
                executor.fork_for_target_registry(registry_v2)
            self.assertIn("protocol_declaration_tampered", str(caught.exception))
            self.assertFalse(executor._sealed)
            self.assertEqual(executor.registry["version"], "targets-v1")
            self.assertEqual(executor.budget_remaining, control.budget_remaining)
            self.assertEqual(executor.budget_spent, control.budget_spent)

    def test_full_reset_requires_declared_reset_target(self):
        fixture = load_fixture()
        fixture["protocol_reset_targets"] = ["targets-v2"]
        executor = SAPExecutor(fixture)
        with self.assertRaises(ValueError) as caught:
            executor.fork_for_target_registry(fixture["target_registry"])
        self.assertIn("reset_target_not_declared", str(caught.exception))
        payload = executor.governance.audit_records()[-1]["payload"]
        self.assertFalse(payload["registry_objective_budget_mutated"])
        self.assertTrue(payload["rejection_audit_record_appended"])
        self.assertFalse(executor._sealed)
        forked = executor.fork_for_target_registry(fixture["protocol_registries"]["targets-v2"])
        self.assertEqual(forked.protocol_registry_schedule, ["targets-v2"])
        # Absent declaration defaults to the whole family (documented default).
        default = load_fixture()
        del default["protocol_reset_targets"]
        self.assertEqual(SAPExecutor(default).protocol_reset_targets, ["targets-v1", "targets-v2"])

    def test_backward_full_reset_is_new_instance_with_single_version_schedule(self):
        fixture = load_fixture()
        executor = SAPExecutor(fixture)
        executor.run_period(0, fixture["period_plans"]["0"])
        continued = executor.continue_with_target_registry(fixture["protocol_registries"]["targets-v2"])
        reset = continued.fork_for_target_registry(fixture["target_registry"])
        self.assertEqual(reset.registry["version"], "targets-v1")
        self.assertEqual(reset.protocol_registry_schedule, ["targets-v1"])
        self.assertEqual(reset.protocol_switch_timing, {})
        self.assertEqual(reset.next_period, 0)
        self.assertNotEqual(reset.control_instance_id, continued.control_instance_id)
        self.assertIsNot(reset.governance, continued.governance)
        self.assertEqual(reset.budget_spent, {name: 0 for name in reset.budget_spent})
        self.assertTrue(continued._sealed)
        self.assertFalse(reset._sealed)
        # The sealed parent keeps its registry version: a reset is not a rollback.
        self.assertEqual(continued.registry["version"], "targets-v2")
        # The reset instance has no scheduled successor: continuity is impossible.
        with self.assertRaises(ValueError) as caught:
            reset.continue_with_target_registry(fixture["protocol_registries"]["targets-v2"])
        self.assertIn("version_not_next_in_protocol_schedule", str(caught.exception))
        reset.run_period(0, fixture["period_plans"]["0"])

    def test_protocol_timing_and_reset_declaration_validation(self):
        fixture = load_fixture()
        for mutate in (
            lambda bad: bad.pop("protocol_switch_timing"),
            lambda bad: bad.__setitem__("protocol_switch_timing", {}),
            lambda bad: bad.__setitem__("protocol_switch_timing", {"targets-v1": 0}),
            lambda bad: bad.__setitem__("protocol_switch_timing", {"targets-v2": -1}),
            lambda bad: bad.__setitem__("protocol_switch_timing", {"targets-v2": True}),
            lambda bad: bad.__setitem__("protocol_reset_targets", ["targets-v9"]),
            lambda bad: bad.__setitem__("protocol_reset_targets", []),
            lambda bad: bad.__setitem__("protocol_reset_targets", ["targets-v1", "targets-v1"]),
        ):
            bad = copy.deepcopy(fixture)
            mutate(bad)
            with self.assertRaises(ValueError):
                SAPExecutor(bad)
        # A three-version schedule must have strictly increasing switch periods.
        bad = copy.deepcopy(fixture)
        v3 = copy.deepcopy(fixture["protocol_registries"]["targets-v2"])
        v3["version"] = "targets-v3"
        v3["targets"][0]["canonical_text"] = "Third synthetic proposition e1."
        bad["protocol_registries"]["targets-v3"] = v3
        bad["registry_family"]["targets-v3"] = hashlib.sha256(
            canonical_json(v3).encode("utf-8")).hexdigest()
        bad["protocol_registry_schedule"] = ["targets-v1", "targets-v2", "targets-v3"]
        bad["protocol_switch_timing"] = {"targets-v2": 1, "targets-v3": 1}
        with self.assertRaises(ValueError):
            SAPExecutor(bad)
        bad["protocol_switch_timing"] = {"targets-v2": 0, "targets-v3": 2}
        ok = SAPExecutor(bad)
        self.assertEqual(ok.protocol_switch_timing, {"targets-v2": 0, "targets-v3": 2})
        # Timing/reset declarations without a family are rejected.
        bad = copy.deepcopy(fixture)
        del bad["registry_family"]
        del bad["protocol_registry_schedule"]
        del bad["protocol_registries"]
        with self.assertRaises(ValueError):
            SAPExecutor(bad)

    def test_protocol_registry_switch_demo_passes_all_checks(self):
        result = run_protocol_registry_switch_demo()
        self.assertEqual(result["schema"], "sea.protocol-registry-switch-demo/v3")
        self.assertEqual(result["status"], "SYNTHETIC_PROTOCOL_TRANSITION_DEMO__NOT_EFFECTIVENESS_EVIDENCE")
        self.assertTrue(all(result["checks"].values()))
        self.assertTrue(result["audit"]["verification"]["valid"])
        self.assertEqual(len(result["rejection_events"]), 5)
        self.assertEqual(len(result["timing_and_declaration_rejection_events"]), 3)
        self.assertEqual(len(result["duplicate_period_switch_rejection_events"]), 1)
        self.assertEqual(result["duplicate_period_switch_rejection_events"][0]["completed_periods"], 1)
        self.assertIn("period == next_period", result["semantics"]["period_sequence"])
        self.assertEqual(len(result["seal_events"]), 2)
        self.assertEqual(len(result["full_reset_seal_events"]), 1)
        self.assertEqual(result["full_reset_seal_events"][0]["reason"],
                         "protocol_full_reset_new_control_instance")
        self.assertEqual(len(result["cohort_change_events"]), 1)
        change = result["cohort_change_events"][0]
        self.assertEqual(change["event_kind"], "exogenous_evaluation_protocol_event")
        self.assertFalse(change["policy_action"])
        self.assertFalse(change["authorization_required"])
        self.assertTrue(change["old_control_path_sealed"])
        self.assertEqual(change["declared_switch_after_period"], 0)
        self.assertEqual(change["completed_periods_before_switch"], 1)
        self.assertTrue(change["switch_timing_frozen_before_results"])
        self.assertEqual(result["protocol_switch_timing"], {"targets-v2": 0})
        self.assertEqual(result["protocol_reset_targets"], ["targets-v1", "targets-v2"])
        self.assertEqual(result["new_real_model_calls"], 0)
        self.assertFalse(result["human_data"])

    def test_s12_transport_identity_precision_warning_and_delta_method(self):
        # Perfect measurement transports identically.
        perfect = completed_measurement_transport(0.2, 1.0, 1.0)
        self.assertAlmostEqual(perfect["m_D"], 0.2)
        self.assertFalse(perfect["precision_warning"])
        # False negatives alone: operational omission 0.2, latent omission 0.
        fn_only = completed_measurement_transport(0.2, 0.8, 1.0)
        self.assertAlmostEqual(fn_only["m_D"], 0.0)
        # Worked example: se=0.9, sp=0.95, m^Z=0.13 -> (0.13-0.1)/0.85.
        worked = completed_measurement_transport(0.13, 0.9, 0.95)
        self.assertAlmostEqual(worked["m_D"], 0.03 / 0.85)
        self.assertAlmostEqual(worked["youden_denominator"], 0.85)
        self.assertAlmostEqual(worked["variance_amplification_factor"], 1 / 0.85 ** 2)
        self.assertFalse(worked["precision_warning"])
        # Near-zero Youden denominator fires the precision warning.
        unstable = completed_measurement_transport(0.4, 0.55, 0.5)
        self.assertTrue(unstable["precision_warning"])
        self.assertAlmostEqual(unstable["variance_amplification_factor"], 1 / 0.05 ** 2)
        with self.assertRaises(ValueError):
            completed_measurement_transport(0.2, 0.5, 0.5)  # se+sp=1 not >1
        with self.assertRaises(ValueError):
            completed_measurement_transport(float("nan"), 0.9, 0.95)
        # Delta-method propagation, hand-checked at the worked example.
        propagated = completed_measurement_transport_delta_method(
            0.13, 0.9, 0.95, var_m_z=0.001, var_se=0.002, var_sp=0.001)
        j, n = 0.85, 0.13 - 1 + 0.9
        d_se, d_sp, d_mz = (j - n) / j ** 2, -n / j ** 2, 1 / j
        expected_var = d_se ** 2 * 0.002 + d_sp ** 2 * 0.001 + d_mz ** 2 * 0.001
        self.assertAlmostEqual(propagated["delta_method_variance"], expected_var)
        low, high = propagated["approx_95_interval"]
        self.assertLess(low, propagated["m_D"])
        self.assertGreater(high, propagated["m_D"])
        self.assertTrue(propagated["input_independence_assumed"])

    def test_s12_delta_method_covariance_terms(self):
        kwargs = dict(var_m_z=0.001, var_se=0.002, var_sp=0.001)
        independent = completed_measurement_transport_delta_method(0.13, 0.9, 0.95, **kwargs)
        self.assertTrue(independent["input_independence_assumed"])
        dependent = completed_measurement_transport_delta_method(
            0.13, 0.9, 0.95, cov_se_sp=0.0005, cov_mz_se=0.0002, cov_mz_sp=-0.0001, **kwargs)
        j, n = 0.85, 0.13 - 1 + 0.9
        d_se, d_sp, d_mz = (j - n) / j ** 2, -n / j ** 2, 1 / j
        expected = (d_se ** 2 * 0.002 + d_sp ** 2 * 0.001 + d_mz ** 2 * 0.001
                    + 2 * d_se * d_sp * 0.0005 + 2 * d_mz * d_se * 0.0002
                    + 2 * d_mz * d_sp * (-0.0001))
        self.assertAlmostEqual(dependent["delta_method_variance"], expected)
        self.assertFalse(dependent["input_independence_assumed"])
        self.assertTrue(dependent["covariance_matrix_positive_semidefinite"])
        self.assertEqual(dependent["covariance_matrix_order"],
                         ["sensitivity", "specificity", "operational_omission"])
        self.assertNotAlmostEqual(dependent["delta_method_variance"],
                                  independent["delta_method_variance"])
        # Invalid covariance inputs are rejected, never silently corrected.
        with self.assertRaises(ValueError):
            completed_measurement_transport_delta_method(0.13, 0.9, 0.95, cov_se_sp=1.0, **kwargs)
        with self.assertRaises(ValueError):
            completed_measurement_transport_delta_method(0.13, 0.9, 0.95,
                                                         cov_se_sp=float("nan"), **kwargs)
        # Every pairwise 2x2 minor is nonnegative here, but det(Sigma)<0.
        # The S12 directional variance is positive, so the old scalar-only
        # check would incorrectly accept this jointly impossible matrix.
        with self.assertRaisesRegex(ValueError, "positive semidefinite"):
            completed_measurement_transport_delta_method(
                0.13, 0.9, 0.95, var_m_z=1.0, var_se=1.0, var_sp=1.0,
                cov_se_sp=0.9, cov_mz_se=0.9, cov_mz_sp=-0.9)
        # A large unrelated variance must not hide an illegal small subblock,
        # and a zero-variance coordinate cannot carry nonzero covariance.
        with self.assertRaisesRegex(ValueError, "positive semidefinite"):
            completed_measurement_transport_delta_method(
                0.13, 0.9, 0.95, var_m_z=1.0, var_se=1e-8, var_sp=1e-8,
                cov_se_sp=2e-8)
        with self.assertRaisesRegex(ValueError, "zero-variance"):
            completed_measurement_transport_delta_method(
                0.13, 0.9, 0.95, var_m_z=1.0, var_se=0.0, var_sp=0.0,
                cov_se_sp=1e-7)
        all_zero = completed_measurement_transport_delta_method(
            0.13, 0.9, 0.95, var_m_z=0.0, var_se=0.0, var_sp=0.0)
        self.assertEqual(all_zero["delta_method_variance"], 0.0)
        # Normalization, not raw products, preserves this extreme-scale valid
        # singular correlation (sqrt(1e-200 * 1e200) = 1).
        extreme = completed_measurement_transport_delta_method(
            0.13, 0.9, 0.95, var_m_z=0.0, var_se=1e-200, var_sp=1e200,
            cov_se_sp=1.0)
        self.assertTrue(extreme["covariance_matrix_positive_semidefinite"])
        # A singular but valid PSD boundary remains admissible.
        singular = completed_measurement_transport_delta_method(
            0.13, 0.9, 0.95, var_m_z=0.0, var_se=0.002, var_sp=0.002,
            cov_se_sp=0.002)
        self.assertTrue(singular["covariance_matrix_positive_semidefinite"])

    def test_s12_joint_bootstrap_preserves_dependence_and_is_deterministic(self):
        records = ([{"test_positive": True, "truth_positive": True}] * 90
                   + [{"test_positive": False, "truth_positive": True}] * 10
                   + [{"test_positive": False, "truth_positive": False}] * 95
                   + [{"test_positive": True, "truth_positive": False}] * 5)
        result = completed_measurement_transport_joint_bootstrap(
            0.13, records, n_bootstrap=2000, seed=42)
        self.assertAlmostEqual(result["sensitivity"], 0.9)
        self.assertAlmostEqual(result["specificity"], 0.95)
        self.assertAlmostEqual(result["m_D"], 0.03 / 0.85)
        low, high = result["bootstrap_95_interval"]
        self.assertLess(low, result["m_D"])
        self.assertGreater(high, result["m_D"])
        again = completed_measurement_transport_joint_bootstrap(
            0.13, records, n_bootstrap=2000, seed=42)
        self.assertEqual(result["bootstrap_95_interval"], again["bootstrap_95_interval"])
        self.assertEqual(result["degenerate_replicates"], 0)
        self.assertTrue(result["m_z_held_fixed"])
        self.assertEqual(result["method"], "joint_bootstrap")
        clustered = [dict(record, cluster_id=index // 10)
                     for index, record in enumerate(records)]
        cluster_result = completed_measurement_transport_joint_bootstrap(
            0.13, clustered, n_bootstrap=1000, seed=42, cluster_key="cluster_id")
        self.assertEqual(cluster_result["method"], "joint_cluster_bootstrap")
        self.assertEqual(cluster_result["n_clusters"], 20)
        # Near-zero denominator: degenerate replicates are reported, not hidden.
        unstable = ([{"test_positive": True, "truth_positive": True}] * 20
                    + [{"test_positive": False, "truth_positive": True}] * 20
                    + [{"test_positive": False, "truth_positive": False}] * 22
                    + [{"test_positive": True, "truth_positive": False}] * 18)
        warning = completed_measurement_transport_joint_bootstrap(
            0.4, unstable, n_bootstrap=1000, seed=7)
        self.assertTrue(warning["precision_warning"])
        self.assertGreater(warning["degenerate_replicates"], 0)
        self.assertAlmostEqual(warning["degenerate_replicate_fraction"],
                               warning["degenerate_replicates"] / 1000)
        with self.assertRaises(ValueError):
            completed_measurement_transport_joint_bootstrap(
                0.13, [{"test_positive": True, "truth_positive": True}])
        with self.assertRaises(ValueError):
            completed_measurement_transport_joint_bootstrap(0.13, records, n_bootstrap=10)

    def test_s12_sensitivity_grid_reports_inadmissible_and_range(self):
        grid = completed_measurement_transport_sensitivity_grid(0.13, [0.5, 0.9], [0.5, 0.95])
        self.assertEqual(grid["grid_size"], 4)
        self.assertEqual(grid["inadmissible_cells"], 1)
        self.assertAlmostEqual(grid["m_D_min"], (0.13 - 0.5) / 0.45)
        self.assertAlmostEqual(grid["m_D_max"], (0.13 - 0.1) / 0.4)
        self.assertAlmostEqual(grid["outside_unit_interval_fraction"], 1 / 3)
        with self.assertRaises(ValueError):
            completed_measurement_transport_sensitivity_grid(0.13, [0.5], [0.5])

    def test_transportability_stratified_diagnostics(self):
        def block(n_tp, n_fn, n_tn, n_fp, stratum):
            return ([{"test_positive": True, "truth_positive": True,
                      "stratum": stratum, "measurement_status": "complete"}] * n_tp
                    + [{"test_positive": False, "truth_positive": True,
                        "stratum": stratum, "measurement_status": "complete"}] * n_fn
                    + [{"test_positive": False, "truth_positive": False,
                        "stratum": stratum, "measurement_status": "complete"}] * n_tn
                    + [{"test_positive": True, "truth_positive": False,
                        "stratum": stratum, "measurement_status": "complete"}] * n_fp)

        validation = (block(36, 4, 38, 2, "a") + block(24, 16, 28, 12, "b")
                      + [{"test_positive": True, "truth_positive": True,
                          "stratum": "c", "measurement_status": "complete"}] * 10
                      + [{"test_positive": True, "truth_positive": True,
                          "stratum": "a", "measurement_status": "unknown"}] * 2)
        deployment = ([{"stratum": "a", "measurement_status": "complete"}] * 90
                      + [{"stratum": "a", "measurement_status": "unknown"}] * 10
                      + [{"stratum": "b", "measurement_status": "complete"}] * 50
                      + [{"stratum": "b", "measurement_status": "unknown"}] * 50)
        diag = transportability_stratified_diagnostics(validation, deployment)
        self.assertTrue(diag["validation"]["heterogeneity_warning"])
        # Sensitivity is estimable in all three strata (including c, which
        # lacks truth-negative units); specificity is estimable in a and b.
        self.assertAlmostEqual(diag["validation"]["heterogeneity_max_abs_deviation"], 2 / 9)
        by_metric = diag["validation"]["heterogeneity_by_metric"]
        self.assertEqual(by_metric["sensitivity"]["n_estimable_strata"], 3)
        self.assertAlmostEqual(by_metric["sensitivity"]["max_abs_deviation"], 2 / 9)
        self.assertEqual(by_metric["specificity"]["n_estimable_strata"], 2)
        self.assertAlmostEqual(by_metric["specificity"]["max_abs_deviation"], 0.125)
        self.assertIn("not_estimable", diag["validation"]["strata"]["c"])
        self.assertEqual(diag["validation"]["strata"]["c"]["not_estimable_reason"],
                         "no_truth_negative_units")
        self.assertEqual(diag["validation"]["n_unknown_excluded_from_error_estimation"], 2)
        pooled = diag["validation"]["pooled"]
        self.assertTrue(pooled["error_rates_estimable"])
        self.assertEqual(pooled["sensitivity_n"], 90)
        self.assertEqual(pooled["specificity_n"], 80)
        for metric in ("sensitivity", "specificity"):
            low, high = pooled[f"{metric}_wilson_95_interval"]
            self.assertLess(low, pooled[metric])
            self.assertGreater(high, pooled[metric])
        stratum_a = diag["validation"]["strata"]["a"]
        self.assertEqual(stratum_a["n_completed"], 80)
        self.assertEqual(stratum_a["n_assigned"], 82)
        self.assertEqual(stratum_a["n_unknown"], 2)
        self.assertEqual(stratum_a["sensitivity_n"], 40)
        self.assertIn("not cluster-adjusted", diag["interval_method"])
        completion = diag["validation"]["completion"]
        self.assertTrue(completion["complete_subset_share_shift_estimable"])
        low, high = completion["overall_completion_rate_wilson_95_interval"]
        self.assertLessEqual(low, completion["overall_completion_rate"])
        self.assertGreaterEqual(high, completion["overall_completion_rate"])
        representativeness = diag["completion_representativeness"]
        self.assertTrue(representativeness["warning"])
        self.assertAlmostEqual(representativeness["max_completion_rate_gap"], 0.5)
        self.assertEqual(representativeness["strata_missing_in_deployment"], ["c"])
        self.assertFalse(diag["transportability_proven"])
        self.assertTrue(diag["sensitivity_grid_required"])
        solo = transportability_stratified_diagnostics(validation)
        self.assertIsNone(solo["deployment"])
        self.assertNotIn("completion_representativeness", solo)
        with self.assertRaises(ValueError):
            transportability_stratified_diagnostics([])
        with self.assertRaises(ValueError):
            transportability_stratified_diagnostics([{"test_positive": True, "truth_positive": True}])

    def test_stratified_zero_completion_returns_structured_not_estimable(self):
        # Unknown-only records need not contain paired test/truth fields: no
        # pooled estimator should run and suppress the completion diagnostics.
        records = [
            {"stratum": "a", "measurement_status": "unknown"},
            {"stratum": "a", "measurement_status": "unknown"},
            {"stratum": "b", "measurement_status": "unknown"},
        ]
        diag = transportability_stratified_diagnostics(records)
        self.assertEqual(diag["completion_rate"], 0.0)
        self.assertEqual(diag["completion_subset_share_shift"], "not_estimable")
        self.assertFalse(diag["completion_subset_share_shift_estimable"])
        self.assertFalse(diag["sensitivity_specificity_estimable"])
        self.assertFalse(diag["error_rates_estimable"])
        self.assertTrue(diag["completion_warning"])
        self.assertTrue(diag["representativeness_warning"])
        self.assertEqual(diag["reason"], "no_completed_measurements")
        completion = diag["validation"]["completion"]
        self.assertEqual(completion["assigned"], {"a": 2, "b": 1})
        self.assertEqual(completion["unknown"], {"a": 2, "b": 1})
        self.assertEqual(completion["completed"], {"a": 0, "b": 0})
        self.assertEqual(completion["n_completed"], 0)
        self.assertIsNone(completion["max_share_shift"])
        self.assertEqual(completion["complete_subset_share_shift_by_stratum"],
                         {"a": None, "b": None})
        low, high = completion["overall_completion_rate_wilson_95_interval"]
        self.assertEqual(low, 0.0)
        self.assertGreater(high, 0.0)
        pooled = diag["validation"]["pooled"]
        self.assertEqual(pooled["n"], 0)
        self.assertIsNone(pooled["sensitivity"])
        self.assertIsNone(pooled["specificity"])
        self.assertEqual(pooled["not_estimable_reason"], "no_completed_measurements")
        self.assertIsNone(diag["validation"]["heterogeneity_max_abs_deviation"])
        self.assertFalse(diag["validation"]["heterogeneity_estimable"])
        for stratum in ("a", "b"):
            self.assertEqual(diag["validation"]["strata"][stratum]["not_estimable_reason"],
                             "no_completed_measurements")
        # A zero-completion deployment table likewise cannot block diagnostics.
        both = transportability_stratified_diagnostics(records, records)
        self.assertTrue(both["completion_representativeness"]["warning"])
        self.assertFalse(both["completion_representativeness"]["complete_subset_share_shift_estimable"])
        self.assertIsNone(both["completion_representativeness"]
                          ["max_complete_subset_share_shift_validation"])
        self.assertEqual(both["reason"], "no_completed_measurements")
        self.assertEqual(both["completion_representativeness"]["reason"],
                         "validation:no_completed_measurements;deployment:no_completed_measurements")
        single = transportability_stratified_diagnostics(
            [{"stratum": "solo", "measurement_status": "unknown"}])
        low, high = single["validation"]["completion"]["overall_completion_rate_wilson_95_interval"]
        z = 1.959963984540054
        self.assertEqual(low, 0.0)
        self.assertAlmostEqual(high, z * z / (1 + z * z))

    def test_stratified_single_truth_class_is_not_estimable_not_exception(self):
        records = [{"stratum": "only", "measurement_status": "complete",
                    "test_positive": True, "truth_positive": True}] * 4
        diag = transportability_stratified_diagnostics(records)
        pooled = diag["validation"]["pooled"]
        self.assertFalse(diag["error_rates_estimable"])
        self.assertEqual(diag["reason"], "no_truth_negative_units")
        self.assertEqual(pooled["sensitivity"], 1.0)
        self.assertIsNone(pooled["specificity"])
        self.assertIsNone(pooled["specificity_wilson_95_interval"])
        self.assertEqual(pooled["sensitivity_n"], 4)
        self.assertEqual(pooled["specificity_n"], 0)
        self.assertTrue(pooled["sensitivity_estimable"])
        self.assertFalse(pooled["specificity_estimable"])
        self.assertEqual(pooled["specificity_not_estimable_reason"], "no_truth_negative_units")
        self.assertIsNone(diag["validation"]["heterogeneity_max_abs_deviation"])
        negative_only = transportability_stratified_diagnostics([
            {"stratum": "only", "measurement_status": "complete",
             "test_positive": False, "truth_positive": False}] * 4)
        negative_pooled = negative_only["validation"]["pooled"]
        self.assertIsNone(negative_pooled["sensitivity"])
        self.assertEqual(negative_pooled["specificity"], 1.0)
        self.assertFalse(negative_pooled["sensitivity_estimable"])
        self.assertTrue(negative_pooled["specificity_estimable"])
        self.assertEqual(negative_pooled["sensitivity_not_estimable_reason"], "no_truth_positive_units")

    def test_stratified_single_completed_stratum_and_missing_stratum_remain_visible(self):
        validation = [
            {"stratum": "a", "measurement_status": "complete",
             "test_positive": True, "truth_positive": True},
            {"stratum": "a", "measurement_status": "complete",
             "test_positive": False, "truth_positive": False},
            {"stratum": "b", "measurement_status": "unknown",
             "test_positive": True, "truth_positive": True},
        ]
        deployment = [{"stratum": "a", "measurement_status": "unknown"}]
        diag = transportability_stratified_diagnostics(validation, deployment)
        self.assertTrue(diag["validation"]["pooled"]["error_rates_estimable"])
        self.assertEqual(diag["validation"]["strata"]["b"]["n_completed"], 0)
        self.assertEqual(diag["validation"]["strata"]["b"]["n_unknown"], 1)
        self.assertEqual(diag["validation"]["strata"]["b"]["not_estimable_reason"],
                         "no_completed_measurements")
        self.assertIsNone(diag["validation"]["heterogeneity_max_abs_deviation"])
        representativeness = diag["completion_representativeness"]
        self.assertEqual(representativeness["strata_missing_in_deployment"], ["b"])
        self.assertTrue(representativeness["warning"])
        self.assertTrue(diag["representativeness_warning"])

    def test_open_world_absence_cannot_be_asserted_from_closed_snapshot(self):
        fixture = load_fixture()
        registry = copy.deepcopy(fixture["target_registry"])
        registry["reference_corpus"]["availability_universe"] = "open_world"
        with self.assertRaises(ValueError):
            validate_target_registry(registry)

    def test_matched_fixture_matches_input_and_budget_without_effect_claim(self):
        result = run_matched_implementation_demo()
        self.assertEqual(result["status"], "MECHANISTIC_MATCHED_FIXTURE__NOT_A_MODEL_OR_DEPLOYMENT_EXPERIMENT")
        self.assertEqual(result["matching"]["external_model_calls"], 0)
        self.assertTrue(result["arms"]["sea"]["audit_valid"])
        self.assertTrue(result["arms"]["s2d"]["audit_valid"])
        self.assertNotEqual(result["arms"]["sea"]["selected_candidate_ids"],
                            result["arms"]["s2d"]["selected_candidate_ids"])
        self.assertEqual(result["arms"]["s2d"]["evaluation_link_rule"], "reference_link_truth_arm_independent")

    def test_unvalidated_real_instrument_is_rejected(self):
        fixture = load_fixture()
        registry = copy.deepcopy(fixture["attendance_instrument"])
        registry["validation_status"] = "not_validated"
        with self.assertRaises(ValueError):
            OperationalAttendanceInstrument(registry)

    def test_executor_audit_contains_resource_and_terminal_events(self):
        result = run_longitudinal_fixture()
        events = {record["event"] for record in result["audit"]["records"]}
        self.assertLessEqual({"resource_precheck", "selection_dry_run", "observation", "update",
                              "resource_use", "ranking", "selection", "period_outcome",
                              "override", "rollback"}, events)


if __name__ == "__main__":
    unittest.main()
