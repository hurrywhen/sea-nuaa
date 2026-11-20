"""Regression tests for retrospective caliber names and prospective measurement schema."""
from __future__ import annotations

import csv
import gzip
import json
import unittest

from sea_pilot import audit_v110_consumption_caliber as audit


class ConsumptionCaliberTest(unittest.TestCase):
    def _state(self) -> audit.KeyState:
        record = audit.PolicyRecord(
            agent=0, sim_day=0, picked=("x",), hits_llm=1, hits_param=0, n_crit=1,
            value_llm=1.0, value_param=0.0, source_file="fixture", source_line=1,
            reason_class="OTHER", raw_consume_class="NOT_APPLICABLE",
        )
        return audit.KeyState(
            family="O", run=1, agent=0, sim_day=0, records=[record],
            canonical=audit.CanonicalDay(hits_param=0, n_crit=1, value_param=0.0),
            full_hits_llm=1.0, full_delta_return=1.0,
            resolved_recall=(1.0, 0.0, 1.0), resolved_delta_return=1.0, resolved_sign=1,
            recall_conflict=False, return_conflict=False, sign_conflict=False,
            any_six_field_conflict=False,
        )

    def test_canonical_names_and_legacy_input_aliases(self) -> None:
        self.assertEqual(audit.NEW_CALIBERS, (
            "ALL_EXISTING_RECORD_MEAN_ZERO_EMPTY", "METRIC_RESOLVED_ZERO_EMPTY",
            "ALL_EXPECTED_RECORD_MEAN_ZERO_EMPTY_NO_ROW"))
        for legacy, canonical in audit.LEGACY_CALIBER_ALIASES.items():
            with self.subTest(legacy=legacy):
                self.assertEqual(audit.canonical_caliber(legacy), canonical)
                row = audit._new_run_row(legacy, [self._state()] * audit.NOMINAL_PER_RUN, "O", 1)
                self.assertEqual(row["caliber"], canonical)
        with self.assertRaises(ValueError):
            audit.canonical_caliber("UNKNOWN_CALIBER")

    def test_generated_summary_uses_only_canonical_calibers(self) -> None:
        summary = json.loads((audit.OUTDIR / "summary.json").read_text(encoding="utf-8"))
        self.assertEqual(set(summary["new_calibers"]), set(audit.NEW_CALIBERS))
        self.assertEqual(summary["schema"], "sea.v110.selected-proxy-consumption-caliber/v3")
        self.assertNotIn("POST_HOC_SELECTED_PROXY_ITT", summary["status"])
        self.assertIn("Designated retrospective descriptive caliber",
                      summary["new_calibers"]["ALL_EXISTING_RECORD_MEAN_ZERO_EMPTY"]["analysis_role"])

    def test_csv_and_ledger_do_not_emit_legacy_names(self) -> None:
        with (audit.OUTDIR / "run_metrics.csv").open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 400)
        self.assertEqual({row["caliber"] for row in rows[:240]}, set(audit.NEW_CALIBERS))
        with gzip.open(audit.OUTDIR / "key_ledger.jsonl.gz", "rt", encoding="utf-8") as handle:
            first = json.loads(handle.readline())
        self.assertIn("ALL_EXISTING_RECORD_MEAN_ZERO_EMPTY", first)
        self.assertIn("METRIC_RESOLVED_ZERO_EMPTY", first)
        self.assertIn("ALL_EXPECTED_RECORD_MEAN_ZERO_EMPTY_NO_ROW", first)
        self.assertNotIn("ITT_ALL_RECORD_MEAN", first)
        self.assertNotIn("ITT_METRIC_RESOLVED", first)

    def test_future_schema_closes_attendance_and_primary_missing_rule(self) -> None:
        schema = json.loads((audit.OUTDIR / "future_logging_schema.json").read_text(encoding="utf-8"))
        self.assertIn("outcome_protocol", schema["required"])
        protocol = schema["properties"]["outcome_protocol"]["properties"]
        self.assertEqual(protocol["primary_rule"]["const"],
                         "ALL_ASSIGNED_FAILURE_COMPOSITE_CONFIRMED_CONSUMPTION_OMISSION_V1")
        self.assertEqual(protocol["attendance_decision_rule"]["const"],
                         "VALID_READING_AND_CONTENT_LINKED_CONFIRMATION")
        self.assertEqual(protocol["machine_event_term"]["const"],
                         "machine_ingestion_and_task_reference_not_human_attention")
        item = schema["properties"]["items"]["items"]
        self.assertEqual(set(item["required"]), {"item_id", "selected", "delivered", "opened", "attended"})
        required = set(item["properties"]["attended"]["required"])
        self.assertLessEqual({"instrument", "instrument_version", "threshold_id", "validation_status",
                              "assessor_blinding", "measurement_status"}, required)

    def test_rename_preserves_designated_numeric_result(self) -> None:
        summary = json.loads((audit.OUTDIR / "summary.json").read_text(encoding="utf-8"))
        families = summary["new_calibers"]["ALL_EXISTING_RECORD_MEAN_ZERO_EMPTY"]["families"]
        self.assertEqual(sum(item["n_recall"] for item in families.values()), 71970)
        self.assertAlmostEqual(families["O"]["equal_run"]["delta_recall"]["estimate"],
                               0.0297197743, places=9)
        self.assertAlmostEqual(families["G"]["equal_run"]["delta_return"]["estimate"],
                               -0.251347, places=6)


    def test_conservative_no_row_caliber_covers_all_expected_keys(self) -> None:
        summary = json.loads((audit.OUTDIR / "summary.json").read_text(encoding="utf-8"))
        families = summary["new_calibers"]["ALL_EXPECTED_RECORD_MEAN_ZERO_EMPTY_NO_ROW"]["families"]
        self.assertEqual(sum(item["n_recall"] for item in families.values()), 72000)
        self.assertEqual(sum(item["n_return"] for item in families.values()), 72000)
        existing = summary["new_calibers"]["ALL_EXISTING_RECORD_MEAN_ZERO_EMPTY"]["families"]
        self.assertEqual(sum(item["n_recall"] for item in existing.values()), 71970)


if __name__ == "__main__":
    unittest.main()
