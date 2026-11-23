#!/usr/bin/env python3
"""Unit tests for the read-only three-family dependence sensitivity helpers."""
from __future__ import annotations

import unittest

import numpy as np

from sea_pilot.audit_three_family_dependence import (
    contrast,
    expand_sample,
    moving_block_sample,
)


class ThreeFamilyDependenceTests(unittest.TestCase):
    def test_comparison_specific_calibers(self) -> None:
        records = [
            {"picked": ["paper"], "sim_day": 0, "hits_llm": 1, "hits_param": 1, "n_crit": 2},
            {"picked": [], "sim_day": 0, "hits_llm": 0, "hits_param": 1, "n_crit": 1},
            {"picked": ["other"], "sim_day": 1, "hits_llm": 1, "hits_param": 0, "n_crit": 1},
        ]
        honest = {0: 0, 1: 1}
        # Parametric recall uses all three recorded rows: (2-2)/4 = 0.
        self.assertEqual(contrast(records, honest, "parametric"), 0.0)
        # Honest comparison excludes the empty selection: (2-(0+1))/3 = 1/3.
        self.assertAlmostEqual(contrast(records, honest, "honest"), 1 / 3)

    def test_day_cluster_expansion_preserves_all_rows(self) -> None:
        by_day = {0: [{"picked": []}, {"picked": ["x"]}], 1: [{"picked": ["y"]}]}
        selected = expand_sample(by_day, [0, 0, 1])
        self.assertEqual(len(selected), 5)
        self.assertEqual(sum(not bool(row["picked"]) for row in selected), 2)

    def test_circular_moving_block(self) -> None:
        rng = np.random.default_rng(7)
        days = list(range(30))
        sample = moving_block_sample(days, rng, block_length=5)
        self.assertEqual(len(sample), 30)
        self.assertTrue(set(sample).issubset(days))
        # Force a length-ten block starting at 25, which wraps through zero.
        class FixedRng:
            def integers(self, low, high, size=None):
                return np.array([25] * size)
        wrapped = moving_block_sample(days, FixedRng(), block_length=10)
        self.assertEqual(wrapped[:5], [25, 26, 27, 28, 29])
        self.assertEqual(wrapped[5:10], [0, 1, 2, 3, 4])


if __name__ == "__main__":
    unittest.main()
