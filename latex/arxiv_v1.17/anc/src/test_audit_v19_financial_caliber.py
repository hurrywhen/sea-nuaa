"""Regression tests for the public v1.9 financial-caliber audit input.

Run from ``sim``::

    PYTHONDONTWRITEBYTECODE=1 python3 -m unittest sea_pilot.test_audit_v19_financial_caliber
"""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest import mock

from sea_pilot import audit_v19_financial_caliber as audit


class TestFrozenHistoricalInput(unittest.TestCase):
    def test_independent_csv_matches_pinned_provenance(self):
        rows, provenance = audit._read_historical_rows()

        self.assertEqual(len(rows), 1260)
        self.assertEqual(provenance["sha256"], audit.HISTORICAL_SHA256)
        self.assertEqual(provenance["bytes"], 382663)
        self.assertEqual(provenance["rows"], 1260)
        self.assertEqual(provenance["source_commit"], "8ffc7f5")
        self.assertEqual(provenance["source_path"], "sim/pilot/results/p2_rows.csv")
        self.assertIn("Byte-for-byte copy", provenance["generation_rule"])

    def test_same_size_modification_is_rejected(self):
        raw = bytearray(audit.HISTORICAL_ROWS_PATH.read_bytes())
        raw[-1] ^= 1
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "tampered.csv"
            path.write_bytes(raw)
            with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
                audit._read_historical_rows(path)

    def test_audit_preserves_results_without_git_history(self):
        with mock.patch(
            "subprocess.check_output",
            side_effect=AssertionError("Git history is not a runtime input"),
        ):
            summary, _, _ = audit.audit()

        comparison = summary["semi_oracle_configuration_comparison"]
        historical = comparison["historical_m5"]
        expanded = comparison["expanded_m5"]
        pooled = summary["m5_pooled_across_runs"]
        self.assertEqual(
            (historical["agent_target_hits"], historical["agent_target_opportunities"]),
            (120, 126),
        )
        self.assertEqual(historical["feature_scorer_mean_recall"], 13 / 18)
        self.assertEqual(
            (expanded["agent_target_hits"], expanded["agent_target_opportunities"]),
            (121, 133),
        )
        self.assertEqual(
            (pooled["company_day"]["hits"], pooled["company_day"]["opportunities"]),
            (114, 126),
        )
        self.assertEqual(
            (expanded["budget_conflict_alarms"], expanded["agent_proxy_configurations"]),
            (7, 7),
        )
        self.assertEqual(expanded["slots_per_run"], 150)
        self.assertFalse(comparison["historical_selection_independently_rebuilt"])
        self.assertTrue(comparison["expanded_selection_independently_rebuilt"])


if __name__ == "__main__":
    unittest.main()
