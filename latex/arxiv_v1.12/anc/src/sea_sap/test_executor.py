"""Tests for the v1.12 minimal longitudinal SAP executor and measurement rules."""
from __future__ import annotations

import copy
import unittest

from sea_sap import (
    SAPExecutor,
    failure_composite_contrast_bounds,
    load_fixture,
    machine_ingestion_and_task_reference,
    run_longitudinal_fixture,
    run_matched_implementation_demo,
)
from sea_sap.executor import OperationalAttendanceInstrument, validate_target_registry


class LongitudinalExecutorTest(unittest.TestCase):
    def test_fixture_and_reference_corpus_are_valid(self):
        fixture = load_fixture()
        validate_target_registry(fixture["target_registry"])
        self.assertEqual(fixture["evidence_scope"], "SYNTHETIC_FIXTURE__NOT_HUMAN_OR_DEPLOYMENT_DATA")

    def test_longitudinal_run_exercises_guard_budgets_and_audit(self):
        result = run_longitudinal_fixture()
        self.assertTrue(all(result["guard_trace"].values()))
        self.assertTrue(result["audit"]["verification"]["valid"])
        self.assertEqual(len(result["periods"]), 2)
        self.assertTrue(all(value > 0 for value in result["budget"]["spent"].values()))
        self.assertEqual(result["new_real_model_calls"], 0)
        self.assertFalse(result["latent_actual_consumption_observed"])

    def test_target_ledger_partitions_omission_and_keeps_latent_unobserved(self):
        result = run_longitudinal_fixture()
        first, second = result["periods"]
        self.assertAlmostEqual(first["outcome_summary"]["weighted_fc_omission"], 5 / 6)
        self.assertAlmostEqual(second["outcome_summary"]["weighted_fc_omission"], 1.0)
        self.assertAlmostEqual(second["outcome_summary"]["weighted_unknown_terminal"], 1 / 6)
        for period in (first, second):
            stages = [row["first_failed_stage"] for row in period["target_ledger"]]
            omitted = [row for row in period["target_ledger"] if row["failure_composite_omission"]]
            self.assertEqual(len(omitted), sum(stage is not None for stage in stages))
            self.assertTrue(all(row["latent_actual_consumption"] is None for row in period["target_ledger"]))

    def test_operational_attendance_and_machine_reference_are_distinct(self):
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
        self.assertAlmostEqual(result["periods"][0]["outcome_summary"]["weighted_fc_omission"], 5 / 6)

    def test_contrast_bounds_use_arm_specific_unknown_extremes(self):
        bounds = failure_composite_contrast_bounds(
            {"sea": 0.5, "control": 0.4}, {"sea": 0.2, "control": 0.1})
        self.assertAlmostEqual(bounds["sea_minus_control_fc"], 0.1)
        self.assertAlmostEqual(bounds["lower_sea_unknown_success_control_unknown_failure"], -0.1)
        self.assertAlmostEqual(bounds["upper_sea_unknown_failure_control_unknown_success"], 0.2)
        with self.assertRaises(ValueError):
            failure_composite_contrast_bounds({"sea": 0.1, "control": 0.1}, {"sea": 0.2, "control": 0.0})

    def test_target_version_change_creates_new_sap_instance(self):
        fixture = load_fixture()
        executor = SAPExecutor(fixture)
        registry = copy.deepcopy(fixture["target_registry"])
        registry["version"] = "targets-v2"
        registry["targets"][0]["canonical_text"] = "Revised synthetic proposition e1."
        forked = executor.fork_for_target_registry(registry)
        self.assertNotEqual(executor.instance_id, forked.instance_id)
        self.assertEqual(executor.registry["version"], "targets-v1")
        self.assertEqual(forked.registry["version"], "targets-v2")
        self.assertEqual(executor.period_results, [])

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

    def test_unvalidated_real_instrument_is_rejected(self):
        fixture = load_fixture()
        registry = copy.deepcopy(fixture["attendance_instrument"])
        registry["validation_status"] = "not_validated"
        with self.assertRaises(ValueError):
            OperationalAttendanceInstrument(registry)

    def test_executor_audit_contains_resource_and_terminal_events(self):
        result = run_longitudinal_fixture()
        events = {record["event"] for record in result["audit"]["records"]}
        self.assertLessEqual({"observation", "update", "resource_use", "ranking", "selection",
                              "period_outcome", "override", "rollback"}, events)


if __name__ == "__main__":
    unittest.main()
