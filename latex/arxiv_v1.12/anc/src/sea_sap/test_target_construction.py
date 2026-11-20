"""Tests for synthetic target construction, rule agreement and granularity."""
from __future__ import annotations

import csv
import unittest

from sea_sap.target_construction import (
    TEMPLATE_PATH,
    audit_target_construction,
    cohens_kappa,
    granularity_sensitivity,
    load_target_fixture,
)


class TargetConstructionTest(unittest.TestCase):
    def test_audit_reports_rule_agreement_not_human_validation(self):
        audit = audit_target_construction()
        self.assertIn("HUMAN_VALIDATION_PENDING", audit["status"])
        self.assertFalse(audit["human_annotations_created"])
        self.assertIn("deterministic extraction rules", audit["rule_agreement"]["interpretation"])
        self.assertEqual(audit["dynamic_target_rule"], "NEW_SAP_INSTANCE__NO_CROSS_VERSION_POOLING")

    def test_granularity_sensitivity_is_not_invariant(self):
        fixture = load_target_fixture()
        sensitivity = granularity_sensitivity(fixture)
        self.assertAlmostEqual(sensitivity["fine_weighted_omission"], 0.5)
        self.assertAlmostEqual(sensitivity["coarse_weighted_omission"], 1 / 6)
        self.assertNotAlmostEqual(sensitivity["fine_weighted_omission"],
                                  sensitivity["coarse_weighted_omission"])

    def test_kappa_handles_perfect_and_chance_agreement(self):
        perfect = cohens_kappa({"a": True, "b": False}, {"a": True, "b": False})
        self.assertAlmostEqual(perfect["cohens_kappa"], 1.0)
        chance = cohens_kappa({"a": True, "b": True}, {"a": True, "b": True})
        self.assertIsNone(chance["cohens_kappa"])

    def test_human_validation_template_is_blank(self):
        self.assertTrue(TEMPLATE_PATH.is_file())
        with TEMPLATE_PATH.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertTrue(rows)
        self.assertTrue(all(row["annotator_1_label"] == "" and row["annotator_2_label"] == ""
                            for row in rows))


if __name__ == "__main__":
    unittest.main()
