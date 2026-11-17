#!/usr/bin/env python3
"""Regression tests for tools/reproduce_v19_math.py (stdlib unittest)."""
from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import reproduce_v19_math as r


class V19MathTests(unittest.TestCase):
    def test_reviewer_numerics(self) -> None:
        self.assertAlmostEqual(r.required_dprime(0.0125, 0.01, 0.95), 4.389337888, places=8)
        self.assertAlmostEqual(r.population_recall(0.0125, 0.01, 1.5), 0.209639680, places=8)
        self.assertAlmostEqual(r.population_recall(0.0125, 0.01, 2.5), 0.523766570, places=8)
        self.assertAlmostEqual(r.pareto_leakage(52, 26, 1.5)["exact_leakage_share"],
                               0.20799886, places=7)
        self.assertAlmostEqual(r.pareto_leakage(52, 42, 1.5)["exact_leakage_share"],
                               0.06919112, places=7)
        self.assertAlmostEqual(
            r.pareto_leakage(52, 42, 1.5)["quantile_integral_approximation_using_actual_m_over_K"],
            0.06871634, places=7)

    def test_finite_topm_quadrature(self) -> None:
        d = r.required_dprime(0.0125, 0.01, 0.95)
        a = r.finite_topm_expected_recall(800, 8, 10, d, nodes=192)["expected_recall"]
        b = r.finite_topm_expected_recall(800, 8, 10, d, nodes=384)["expected_recall"]
        self.assertAlmostEqual(a, b, places=11)
        self.assertAlmostEqual(b, 0.952626284, places=8)

    def test_feasibility_boundaries(self) -> None:
        self.assertTrue(math.isinf(r.required_dprime(0.009, 0.01, 0.95)))
        self.assertTrue(math.isinf(r.required_dprime(0.0095, 0.01, 0.95)))
        self.assertTrue(math.isfinite(r.required_dprime(0.0125, 0.01, 0.95)))
        # b>=1 is the high-budget region: identical scores already meet the target.
        self.assertEqual(r.required_dprime(0.9999, 0.01, 0.95), 0.0)
        self.assertEqual(r.required_dprime(1.0, 0.01, 0.95), 0.0)
        self.assertEqual(r.population_recall(1.0, 0.01, 0.0), 1.0)

    def test_survival_function_and_grid_tail_metadata(self) -> None:
        self.assertGreater(r.sf(9.0), 0.0)
        tail = r.finite_topm_expected_recall(800, 8, 10, 1.5, nodes=96)[
            "normal_tail_mass_outside_grid"]
        self.assertGreater(tail, 0.0)
        self.assertLess(tail, 1e-15)

    def test_online_threshold_boundary_recursion(self) -> None:
        # Constant unit reward: W_1(1)=1, so Delta_1(1)=1, while Delta_1(2)=0.
        self.assertEqual(r.online_delta_constant_reward(1, 1), 1.0)
        self.assertEqual(r.online_delta_constant_reward(1, 2), 0.0)
        self.assertEqual(r.online_delta_constant_reward(2, 1), 1.0)
        self.assertEqual(r.online_delta_constant_reward(2, 2), 1.0)

    def test_subset_choice_reference_and_zero_temperature_limit(self) -> None:
        utilities = [3.0, 2.0, 1.0]
        subsets = [(0, 1), (0, 2), (1, 2)]
        p = r.subset_choice_distribution(utilities, 2, 1.0, reference=[1.0, 2.0, 3.0])
        self.assertAlmostEqual(sum(p.values()), 1.0)
        self.assertTrue(all(p[s] > 0 for s in subsets))
        inclusion_0 = p[(0, 1)] + p[(0, 2)]
        self.assertGreater(inclusion_0, 0.0)
        sharp = r.subset_choice_distribution(utilities, 2, 1e-6, reference=[1.0, 2.0, 3.0])
        self.assertAlmostEqual(sharp[(0, 1)], 1.0)

    def test_weighted_average_is_not_product_of_average(self) -> None:
        w = r.weighted_coverage_counterexample()
        self.assertAlmostEqual(w["weighted_expected_miss"], 0.41)
        self.assertAlmostEqual(w["invalid_product_of_pooled_mean_coverages"], 0.25)
        self.assertGreater(w["weighted_expected_miss"],
                           w["invalid_product_of_pooled_mean_coverages"])

    def test_one_behaviorally_implementable_update_rule(self) -> None:
        b = r.misspecified_binary_example()
        self.assertAlmostEqual(b["expected_realized_value_W"], -0.24)
        self.assertAlmostEqual(b["correct_model_VOI"], 0.24)
        self.assertAlmostEqual(b["misspecification_regret"], 0.48)

    def test_rct_rounding_and_multiplicity(self) -> None:
        s = r.rct_sizes()
        self.assertEqual(s["one_declared_primary_comparison"]["ceiling_before_attrition"], 129)
        self.assertEqual(s["one_declared_primary_comparison"]["ceiling_after_25_percent_attrition"], 171)
        self.assertEqual(s["one_declared_primary_comparison"]["three_arm_total"], 513)
        self.assertEqual(s["two_coprimary_bonferroni_sensitivity"]["ceiling_after_25_percent_attrition"], 207)


if __name__ == "__main__":
    unittest.main()
