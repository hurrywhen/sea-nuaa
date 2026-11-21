"""Tests for the v1.14 minimal longitudinal SAP executor and measurement rules."""
from __future__ import annotations

import copy
import hashlib
import json
import unittest

from sea_governance import canonical_json
from sea_sap import (
    SAPExecutor,
    load_fixture,
    machine_ingestion_and_task_reference,
    operational_attendance_contrast_bounds,
    run_longitudinal_fixture,
    run_matched_implementation_demo,
)
from sea_sap.executor import OperationalAttendanceInstrument, validate_target_registry


def _refresh_registry_hash(registry):
    registry["reference_corpus"]["sha256"] = hashlib.sha256(
        canonical_json(registry["reference_corpus"]["documents"]).encode("utf-8")
    ).hexdigest()


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
        registry.update({
            "raw_event_schema": {"required_fields": [
                "focused_visible", "engaged_ms", "coverage_fraction",
                "content_linked_confirmation", "evidence_pointer"]},
            "validation_data_sha256": "a" * 64,
            "measurement_code_sha256": "b" * 64,
            "measurement_error": {"sensitivity": 0.9, "specificity": 0.95,
                                   "validation_set_pointer": "synthetic-validation:set-1"},
            "alternative_instruments": ["reading_only", "confirmation_only"],
        })
        instrument = OperationalAttendanceInstrument(registry)
        positive = fixture["period_plans"]["0"]["attendance_events"]["c1"]
        self.assertEqual(instrument.measure(positive).status, "positive")
        bad = copy.deepcopy(registry)
        bad["measurement_error"] = {"sensitivity": 0.9}
        with self.assertRaises(ValueError):
            OperationalAttendanceInstrument(bad)
        bad = copy.deepcopy(registry)
        bad["measurement_error"] = {"sensitivity": float("nan"), "specificity": 0.95,
                                    "validation_set_pointer": "synthetic-validation:set-1"}
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
        registry = copy.deepcopy(fixture["target_registry"])
        registry["version"] = "targets-v2"
        registry["targets"][0]["canonical_text"] = "Revised synthetic proposition e1."
        continued = executor.continue_with_target_registry(registry)
        self.assertEqual(continued.control_instance_id, executor.control_instance_id)
        self.assertNotEqual(continued.evaluation_cohort_id, executor.evaluation_cohort_id)
        self.assertIs(continued.governance, executor.governance)
        self.assertEqual(continued.budget_remaining, executor.budget_remaining)
        self.assertEqual(continued.registry["version"], "targets-v2")
        forked = executor.fork_for_target_registry(registry)
        self.assertNotEqual(forked.control_instance_id, executor.control_instance_id)
        self.assertEqual(forked.budget_spent, {name: 0 for name in forked.budget_spent})

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
