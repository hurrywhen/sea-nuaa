"""Synthetic tests for the controlled unique-key frozen reanalysis.

Run from ``sim``::

    PYTHONDONTWRITEBYTECODE=1 python3 -m unittest sea_pilot.test_replay_frozen

These tests never read or write the 292 formal replay outputs.
"""
from __future__ import annotations

import math
import unittest

import numpy as np

from sea_pilot import recompute_replay_frozen as rr


def record(line=1, *, picked=("paper",), hits_llm=1, hits_param=0, n_crit=2,
           value_llm=3.0, value_param=2.0, agent=0, sim_day=0):
    return {
        "agent": agent,
        "sim_day": sim_day,
        "picked": list(picked),
        "hits_llm": hits_llm,
        "hits_param": hits_param,
        "n_crit": n_crit,
        "value_llm": value_llm,
        "value_param": value_param,
        "reason": "diagnostic only; never an arbitration field",
        "raw_consume": list(picked),
        "_source_file": "synthetic.jsonl",
        "_source_line": line,
    }


def make_state(rows, *, family="O", run=1, agent=0, day=0,
               hits_param=0, n_crit=2, value_param=2.0, upper=10.0):
    """Construct one key through the same sufficient-statistic helpers as production."""
    valid = [item for item in rows if rr.is_valid(item)]
    for item in valid:
        rr._validate_valid_record(item, f"synthetic:{item['_source_line']}")
    canonical = rr.CanonicalDay(hits_param, n_crit, value_param)
    pair = rr._consistent(valid, lambda r: (r["hits_llm"], r["n_crit"])) if valid else None
    recall = ((float(pair[0]), float(hits_param), float(n_crit))
              if pair is not None else None)
    dv = rr._consistent(valid, lambda r: float(r["value_llm"]) - float(r["value_param"])) if valid else None
    sign = rr._consistent(valid, lambda r: ((r["hits_llm"] > r["hits_param"])
                                             - (r["hits_llm"] < r["hits_param"]))) if valid else None
    common = rr._build_common_cell(valid, canonical, rr.FIVE_FIELDS, "COMMON_COHORT")
    audit = rr._build_common_cell(valid, canonical, rr.SIX_FIELDS, "AUDIT_SIX_CONSISTENT")
    attempt = rr._attempt_mean_cell(valid, canonical)
    return rr.KeyState(
        family=family, run=run, agent=agent, sim_day=day,
        n_rows=len(rows), n_empty=len(rows) - len(valid), records=valid,
        provenance=[(r["_source_file"], r["_source_line"], rr.is_valid(r)) for r in rows],
        canonical=canonical, value_upper=upper, recall=recall, delta_value=dv, sign=sign,
        common=common, audit_six=audit, attempt_mean=attempt,
        hash_cells={}, hash_meta={},
    )


class TestSufficientStatisticsAndScenarios(unittest.TestCase):
    def test_consistent_attempts_resolve_once(self):
        state = make_state([record(1), record(2)])
        cell = rr.scenario_cell(state, "A")
        self.assertEqual(cell.recall, (1.0, 0.0, 2.0))
        self.assertEqual(cell.delta_value, 1.0)
        self.assertEqual(cell.sign, 1)
        self.assertEqual(cell.recall_status, "RESOLVED")
        # Duplicates contribute one key, but C intentionally excludes them.
        self.assertIsNone(rr.scenario_cell(state, "C").recall)
        self.assertEqual(rr.scenario_cell(state, "E").recall, (1.0, 0.0, 2.0))

    def test_conflicts_are_metric_specific_not_first_or_last_row(self):
        rows = [
            record(1, hits_llm=0, hits_param=2, value_llm=3.0, value_param=2.0),
            record(2, hits_llm=1, hits_param=2, value_llm=3.0, value_param=2.0),
        ]
        state = make_state(rows, hits_param=2)
        cell = rr.scenario_cell(state, "A")
        self.assertIsNone(cell.recall)                 # (hits_llm,n_crit) conflict
        self.assertEqual(cell.delta_value, 1.0)       # equal differences still resolve
        self.assertEqual(cell.sign, -1)                # equal signs still resolve
        self.assertEqual(cell.recall_status, "UNRESOLVED_CONFLICT")
        self.assertIsNone(rr.scenario_cell(state, "B").recall)

    def test_value_conflict_does_not_imply_recall_conflict(self):
        rows = [record(1, value_llm=3.0), record(2, value_llm=4.0)]
        state = make_state(rows)
        cell = rr.scenario_cell(state, "A")
        self.assertEqual(cell.recall, (1.0, 0.0, 2.0))
        self.assertIsNone(cell.delta_value)
        self.assertEqual(cell.sign, 1)

    def test_audit_six_requires_picked_consistency(self):
        rows = [record(1, picked=("a",)), record(2, picked=("b",))]
        state = make_state(rows)
        self.assertIsNotNone(rr.scenario_cell(state, "B").recall)
        self.assertIsNone(rr.scenario_cell(state, "D").recall)

    def test_empty_only_and_no_surviving_row_are_distinct(self):
        empty = make_state([record(1, picked=(), hits_llm=0)], hits_param=1)
        no_row = make_state([], hits_param=1)
        self.assertEqual(empty.gap, "EMPTY_ONLY")
        self.assertEqual(no_row.gap, "NO_SURVIVING_ROW")
        self.assertEqual(rr.scenario_cell(empty, "A").recall_status, "EMPTY_ONLY")
        self.assertEqual(rr.scenario_cell(no_row, "A").recall_status, "NO_SURVIVING_ROW")
        # G fills only the observed empty-only failure; H fills both.
        self.assertEqual(rr.scenario_cell(empty, "G").recall, (0.0, 1.0, 2.0))
        self.assertIsNone(rr.scenario_cell(no_row, "G").recall)
        self.assertEqual(rr.scenario_cell(no_row, "H").recall, (0.0, 1.0, 2.0))
        self.assertEqual(rr.scenario_cell(no_row, "H").delta_value, -2.0)

    def test_empty_record_sharing_valid_key_is_not_a_gap(self):
        state = make_state([record(1), record(2, picked=(), hits_llm=0)])
        self.assertIsNone(state.gap)
        self.assertEqual(state.n_empty, 1)
        self.assertEqual(rr.scenario_cell(state, "A").recall_status, "RESOLVED")

    def test_attempt_mean_is_equal_attempt_mean_without_mcnemar(self):
        state = make_state([
            record(1, hits_llm=0, value_llm=1.0),
            record(2, hits_llm=2, value_llm=3.0),
        ])
        cell = rr.scenario_cell(state, "E")
        self.assertEqual(cell.recall, (1.0, 0.0, 2.0))
        self.assertEqual(cell.delta_value, 0.0)  # mean(-1,+1)
        self.assertIsNone(cell.sign)
        self.assertEqual(cell.sign_status, "NOT_APPLICABLE_FRACTIONAL")

    def test_directional_and_partial_identification_bounds(self):
        rows = [
            record(1, hits_llm=0, hits_param=1, value_llm=1.0, value_param=2.0),
            record(2, hits_llm=2, hits_param=1, value_llm=3.0, value_param=2.0),
        ]
        state = make_state(rows, hits_param=1, value_param=2.0, upper=10.0)
        lower = rr.scenario_cell(state, "J_lower_value")
        upper = rr.scenario_cell(state, "J_upper_value")
        tie = rr.scenario_cell(state, "I_unresolved_tie")
        self.assertEqual(lower.recall, (0.0, 1.0, 2.0))
        self.assertEqual(upper.recall, (2.0, 1.0, 2.0))
        self.assertEqual(lower.delta_value, -2.0)
        self.assertEqual(upper.delta_value, 8.0)
        self.assertLess(lower.recall[0], upper.recall[0])
        self.assertLess(lower.delta_value, upper.delta_value)
        self.assertEqual(tie.recall, (1.0, 1.0, 2.0))
        self.assertEqual(tie.delta_value, 0.0)
        self.assertEqual(tie.sign, 0)
        # I's two directional scenarios and J's endpoints intentionally have
        # the same numeric assignments, while retaining distinct ledger labels.
        favor_param = rr.scenario_cell(state, "I_favor_param")
        favor_llm = rr.scenario_cell(state, "I_favor_llm")
        self.assertEqual((favor_param.recall, favor_param.delta_value, favor_param.sign),
                         (lower.recall, lower.delta_value, lower.sign))
        self.assertEqual((favor_llm.recall, favor_llm.delta_value, favor_llm.sign),
                         (upper.recall, upper.delta_value, upper.sign))
        self.assertNotEqual(favor_param.recall_status, lower.recall_status)


class TestInputGuardsAndHashes(unittest.TestCase):
    def test_daily_parameter_conflict_fails_instead_of_arbitrating(self):
        rows = [record(1, sim_day=day) for day in range(30)]
        rows.append(record(31, sim_day=0, agent=1, hits_param=1))
        with self.assertRaisesRegex(ValueError, "Non-unique daily parameter hits_param"):
            rr.canonical_daily_parameters({("O", 1): rows})

    def test_daily_parameters_can_be_recovered_from_all_rows(self):
        rows = [record(day + 1, sim_day=day) for day in range(30)]
        rows.append(record(31, sim_day=0, agent=1, picked=(), hits_llm=0))
        canonical = rr.canonical_daily_parameters({("O", 1): rows})
        self.assertEqual(canonical[("O", 1, 0)], rr.CanonicalDay(0, 2, 2.0))

    def test_hash_is_blind_to_all_result_and_reason_fields(self):
        first = record(1, hits_llm=0, value_llm=1.0, picked=("a",))
        second = record(1, hits_llm=2, value_llm=999.0, picked=("z",))
        second["reason"] = "completely different"
        second["raw_consume"] = ["not", "the", "same"]
        args = ("salt00", "O", 1, 0, 0, "synthetic.jsonl", 1)
        self.assertEqual(rr.selection_hash(*args), rr.selection_hash(*args))
        # Changing results on the record cannot enter the hash: only explicit
        # provenance arguments are accepted by the function.
        digest_before = rr.selection_hash("salt00", "O", 1,
                                          first["agent"], first["sim_day"],
                                          first["_source_file"], first["_source_line"])
        first.update(second)
        digest_after = rr.selection_hash("salt00", "O", 1,
                                         first["agent"], first["sim_day"],
                                         first["_source_file"], first["_source_line"])
        self.assertEqual(digest_before, digest_after)

    def test_hash_changes_with_salt_and_provenance(self):
        base = ("salt00", "O", 1, 0, 0, "synthetic.jsonl", 1)
        self.assertNotEqual(rr.selection_hash(*base),
                            rr.selection_hash("salt01", *base[1:]))
        self.assertNotEqual(rr.selection_hash(*base),
                            rr.selection_hash(*base[:-1], 2))

    def test_default_cli_is_stdout_without_force(self):
        args = rr.parse_args([])
        self.assertFalse(args.write)
        self.assertFalse(args.force)
        self.assertEqual(len(rr.SCENARIOS), 17)


class TestValueCeilingAndStatistics(unittest.TestCase):
    def test_daily_upper_uses_all_corpus_top_three(self):
        universe = []
        for day in range(30):
            citations = [0, 1, 2, 3, 4] if day == 0 else [0]
            for index, cit in enumerate(citations):
                universe.append({"arxiv_id": f"{day}-{index}",
                                 "date": f"2019-09-{day + 1:02d}", "cit": cit})
        upper = rr.daily_value_upper(universe)
        expected = math.log1p(4) + math.log1p(3) + math.log1p(2)
        self.assertAlmostEqual(upper[0], expected)
        self.assertEqual(upper[1], 0.0)

    def test_b_equals_c_corrected_cmh_is_exactly_zero(self):
        result = rr.cmh_formulas([(2, 2), (3, 3)])
        self.assertEqual(result["B"], 5)
        self.assertEqual(result["C"], 5)
        self.assertEqual(result["uncorrected"]["chi2"], 0.0)
        self.assertEqual(result["continuity_corrected"]["chi2"], 0.0)
        self.assertEqual(result["continuity_corrected"]["p_nominal"], 1.0)
        self.assertEqual(result["legacy_unbounded_correction"]["chi2"], 0.1)
        zero = rr.cmh_formulas([(0, 0)])
        self.assertEqual(zero["legacy_unbounded_correction"]["chi2"], 0.0)

    def test_bootstrap_is_deterministic_and_constant_ci_degenerates(self):
        indices1 = rr.bootstrap_indices(3, resamples=200, seed=42)
        indices2 = rr.bootstrap_indices(3, resamples=200, seed=42)
        np.testing.assert_array_equal(indices1, indices2)
        result = rr.run_bootstrap([0.5, 0.5, 0.5], indices1)
        self.assertEqual(result["estimate"], 0.5)
        self.assertEqual(result["ci95"], [0.5, 0.5])
        with self.assertRaisesRegex(ValueError, "may not delete a run"):
            rr.run_bootstrap([0.5, None, 0.5], indices1)

    def test_exact_sign_flip_basic_properties(self):
        # d=(1,1): T=2; flipped |T| values are 2,0,0,2 -> p=0.5.
        result = rr.run_cluster_sign_flip([1, 1], exact=True)
        self.assertEqual(result["enumerations"], 4)
        self.assertEqual(result["extreme"], 2)
        self.assertEqual(result["p"], 0.5)
        # B=C globally implies T=0 and every absolute statistic is extreme.
        tied = rr.run_cluster_sign_flip([1, -1], exact=True)
        self.assertEqual(tied["T_observed"], 0)
        self.assertEqual(tied["p"], 1.0)

    def test_monte_carlo_sign_flip_is_seeded_and_bounded(self):
        first = rr.run_cluster_sign_flip([2, -1, 1, 3], exact=False,
                                         n_draws=1000, seed=42)
        second = rr.run_cluster_sign_flip([2, -1, 1, 3], exact=False,
                                          n_draws=1000, seed=42)
        self.assertEqual(first, second)
        self.assertGreaterEqual(first["p"], 1 / 1001)
        self.assertLessEqual(first["p"], 1.0)

    def test_report_number_format_regression(self):
        self.assertEqual(rr._fmt(0.25, signed=True), "+0.250000")
        self.assertEqual(rr._fmt(-0.25, signed=True), "-0.250000")
        self.assertEqual(rr._fmt(None), "NA")

    def test_bh4_monotone_and_bounded(self):
        raw = [0.01, 0.02, 0.03, 0.04]
        adjusted = rr.bh_adjust(raw)
        self.assertEqual(len(adjusted), 4)
        self.assertTrue(all(0 <= value <= 1 for value in adjusted))
        self.assertAlmostEqual(adjusted[-1], 0.04)
        with self.assertRaises(ValueError):
            rr.bh_adjust([0.05])


if __name__ == "__main__":
    unittest.main()
