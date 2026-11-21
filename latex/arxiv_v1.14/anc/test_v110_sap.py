"""Regression tests for the v1.10 worked SAP arithmetic (not validation)."""
from __future__ import annotations

import unittest

from tools.reproduce_v110_sap import compute


class V110SapExampleTests(unittest.TestCase):
    def setUp(self):
        self.result = compute()

    def test_stage_recalls_and_omission_decomposition(self):
        p = self.result["pipeline"]
        self.assertAlmostEqual(p["selected_proxy_recall"], 3 / 6)
        self.assertAlmostEqual(p["delivered_proxy_recall"], 2 / 6)
        self.assertAlmostEqual(p["opened_proxy_recall"], 2 / 6)
        self.assertAlmostEqual(p["actual_consumption_recall"], 1 / 6)
        self.assertAlmostEqual(p["availability_omission"], 1 / 6)
        self.assertAlmostEqual(p["post_availability_omission"], 4 / 6)
        self.assertAlmostEqual(p["total_weighted_omission"], 5 / 6)

    def test_every_omission_has_one_first_failed_stage(self):
        expected = {
            "e1": None, "e2": "attendance", "e3": "delivery",
            "e4": "quota", "e5": "linkage", "e6": "availability",
        }
        self.assertEqual({r["target"]: r["first_omission_stage"]
                          for r in self.result["rows"]}, expected)

    def test_symmetric_channel_and_attendance_measurement(self):
        signal = self.result["signal_model"]
        self.assertAlmostEqual(signal["posterior_relevance_given_positive"], 0.8)
        statuses = {row["target"]: row["attendance_status"] for row in self.result["rows"]}
        self.assertEqual(statuses["e1"], "attended")
        self.assertEqual(statuses["e2"], "not_attended")
        self.assertEqual(statuses["e3"], "unobserved")

    def test_noncomposition_counterexample(self):
        c = self.result["non_composition"]
        self.assertEqual(c["greedy_pair_tie_realization"], ["A", "D"])
        self.assertEqual(c["greedy_value"], 17)
        self.assertEqual(c["optimal_pair"], ["B", "C"])
        self.assertEqual(c["optimal_value"], 22)
        self.assertAlmostEqual(c["ratio"], 17 / 22)
        self.assertAlmostEqual(c["two_step_greedy_lower_bound"], 0.75)


if __name__ == "__main__":
    unittest.main()
