#!/usr/bin/env python3
"""Reproduce the v1.10 worked SAP pipeline and non-composition arithmetic.

This is a deterministic illustration, not an experiment or an SAP optimizer.
Default: print JSON. ``--write`` creates sim/theory_v1.10/sap_example.json;
replacement requires ``--force``. No model calls, downloads, or human data.
"""
from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "sim" / "theory_v1.10" / "sap_example.json"


def compute() -> dict:
    values = [6, 5, 4, 3, 2, 1]
    prior = 0.5
    signal_accuracy = 0.8  # symmetric: P(Y=1|w=1)=P(Y=0|w=0)
    posterior = (signal_accuracy * prior) / (
        signal_accuracy * prior + (1 - signal_accuracy) * (1 - prior))
    assert abs(posterior - 0.8) < 1e-15
    authentic = [True, True, True, True, True, False]
    linked = [True, True, True, True, False, False]
    eligible = [i for i in range(6) if authentic[i] and linked[i]]
    ranked = sorted(eligible, key=lambda i: (-posterior * values[i], i))
    selected_set = set(ranked[:3])
    delivered_set = {0, 1}
    opened_set = {0, 1}
    consumed_set = {0}
    rows = []
    for i, value in enumerate(values):
        selected = i in selected_set
        delivered = selected and i in delivered_set
        opened = delivered and i in opened_set
        consumed = opened and i in consumed_set
        attendance_status = ("attended" if consumed else
                             "not_attended" if opened else "unobserved")
        if consumed:
            first_omission = None
        elif not authentic[i]:
            first_omission = "availability"
        elif not linked[i]:
            first_omission = "linkage"
        elif not selected:
            first_omission = "quota"
        elif not delivered:
            first_omission = "delivery"
        elif not opened:
            first_omission = "opening"
        else:
            first_omission = "attendance"
        rows.append({
            "target": f"e{i + 1}", "declared_ranking_value": value,
            "posterior": posterior, "score": posterior * value,
            "authentic": authentic[i], "linked": linked[i], "selected": selected,
            "delivered": delivered, "opened": opened, "consumed": consumed,
            "attendance_status": attendance_status,
            "first_omission_stage": first_omission,
        })
    for row in rows:
        assert row["selected"] <= row["linked"] <= row["authentic"]
        assert row["consumed"] <= row["opened"] <= row["delivered"] <= row["selected"]
    n = len(rows)
    pipeline = {
        "selected_proxy_recall": sum(r["selected"] for r in rows) / n,
        "delivered_proxy_recall": sum(r["delivered"] for r in rows) / n,
        "opened_proxy_recall": sum(r["opened"] for r in rows) / n,
        "actual_consumption_recall": sum(r["consumed"] for r in rows) / n,
        "availability_omission": sum(not r["authentic"] for r in rows) / n,
        "post_availability_omission": sum(r["authentic"] and not r["consumed"] for r in rows) / n,
        "total_weighted_omission": sum(not r["consumed"] for r in rows) / n,
        "target_weight": 1 / n,
    }
    assert abs(pipeline["availability_omission"]
               + pipeline["post_availability_omission"]
               - pipeline["total_weighted_omission"]) < 1e-15

    weights = {item: (3 if item in "abcd" else 2.5) for item in "abcdghij"}
    sets = {
        "A": set("abcd"), "D": set("cdgh"),
        "B": set("abgh"), "C": set("cdij"),
    }
    value = lambda s: sum(weights[item] for item in s)
    # Fixed tie order A,D,B,C after the first step selects D; every second
    # addition is 5. This realizes the manuscript's tie-permitted counterexample.
    first = max(sets, key=lambda name: (value(sets[name]), -list(sets).index(name)))
    assert first == "A"
    second = "D"
    greedy_value = value(sets[first] | sets[second])
    best_name = max(itertools.combinations(sets, 2),
                    key=lambda pair: value(sets[pair[0]] | sets[pair[1]]))
    optimal_value = value(sets[best_name[0]] | sets[best_name[1]])
    composition = {
        "item_weights": weights,
        "sets": {key: sorted(value_set) for key, value_set in sets.items()},
        "single_values": {key: value(value_set) for key, value_set in sets.items()},
        "greedy_pair_tie_realization": [first, second],
        "greedy_value": greedy_value,
        "optimal_pair": list(best_name),
        "optimal_value": optimal_value,
        "ratio": greedy_value / optimal_value,
        "two_step_greedy_lower_bound": 1 - (1 - 1 / 2) ** 2,
        "later_optimal_delivery_repairs_monitoring": False,
    }
    assert greedy_value == 17 and optimal_value == 22 and best_name == ("B", "C")
    assert composition["ratio"] >= composition["two_step_greedy_lower_bound"]
    return {
        "schema": "sea.v110.sap-worked-example/v1",
        "status": "DETERMINISTIC_ILLUSTRATION__NOT_AN_EXPERIMENT",
        "signal_model": {
            "type": "symmetric_binary_channel", "prior_relevance": prior,
            "P(Y=1|omega=1)": signal_accuracy, "P(Y=0|omega=0)": signal_accuracy,
            "posterior_relevance_given_positive": posterior,
            "attendance_measurement": "Both opened items measured: e1 attended, e2 not_attended; later stages unobserved.",
        },
        "pipeline": pipeline,
        "rows": rows,
        "non_composition": composition,
        "new_llm_calls": 0,
        "human_data": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    result = compute()
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if not args.write:
        print(text, end="")
        return
    if OUT.exists() and not args.force:
        raise SystemExit(f"{OUT} exists; use --force to replace it")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
