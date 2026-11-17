#!/usr/bin/env python3
"""Post-hoc recall/citation-return decomposition on strict-singleton replay keys.

The previous 'value' endpoint is a retrospective sum of log1p(citation) values,
not decision utility or welfare.  This audit decomposes its arm difference into
critical and noncritical items to describe how recall and citation-weighted return
can move in opposite directions.  It does not identify SEA's structural effect,
human value, or a causal mechanism.  No LLM is called and no input is modified.
"""
from __future__ import annotations

import argparse
import collections
import csv
import hashlib
import json
import math
import os
from pathlib import Path
from typing import Any

import numpy as np

try:
    from . import corpus as cp
    from .audit_replay_integrity import EXPECTED_RUNS, FAMILY_ORDER, is_valid, load_runs
    from .run_llm_replay import build_days
except ImportError:
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from sea_pilot import corpus as cp
    from sea_pilot.audit_replay_integrity import EXPECTED_RUNS, FAMILY_ORDER, is_valid, load_runs
    from sea_pilot.run_llm_replay import build_days

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "sim" / "pilot" / "results"
OUTDIR = RESULTS / "v19_recall_value_tradeoff"
STATUS = "POST_HOC_STRICT_SINGLETON_DECOMPOSITION__WITHIN_CORPUS_EXPLORATORY"
SEED_BASE = {"O": 0, "G": 0, "Q": 100, "C": 200}


def _seed(family: str, run: int) -> int:
    return SEED_BASE[family] + run


def _logcite(record: dict[str, Any]) -> float:
    return math.log1p(float(record["cit"]))


def _bootstrap(values: list[float], seed: int = 42, B: int = 10000) -> list[float]:
    x = np.asarray(values, dtype=float)
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(x), size=(B, len(x)))
    means = x[idx].mean(axis=1)
    return [float(v) for v in np.quantile(means, [0.025, 0.975])]


def audit() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    os.environ["SEA_FORCE_LITE"] = "1"
    runs, shards, skipped = load_runs(RESULTS)
    universe, critical, watchlists, _ = cp.build_all()
    by_id = {r["arxiv_id"]: r for r in universe}
    frozen_path = RESULTS / "frozen_reanalysis_v1" / "run_metrics.csv"
    with frozen_path.open(encoding="utf-8", newline="") as f:
        frozen_c = {(r["family"], int(r["run"])): r
                    for r in csv.DictReader(f) if r["scenario"] == "C"}
    if len(frozen_c) != 80:
        raise AssertionError(f"Expected 80 frozen scenario-C rows, got {len(frozen_c)}")
    run_rows: list[dict[str, Any]] = []
    for family in FAMILY_ORDER:
        for run in sorted(EXPECTED_RUNS[family]):
            records = runs[(family, run)]
            grouped: dict[tuple[int, int], list[dict[str, Any]]] = collections.defaultdict(list)
            for record in records:
                if is_valid(record):
                    grouped[(record["agent"], record["sim_day"])].append(record)
            days = build_days(universe, critical, watchlists["inst"],
                              proxy_seed=99 + _seed(family, run))[:30]
            cells = []
            for dd in days:
                day = dd["day"]
                critical_ids = {universe[i]["arxiv_id"] for i in dd["critical"]}
                param_ids = [universe[i]["arxiv_id"] for i in dd["proxy_rank"][:3]]
                for agent in range(30):
                    valid = grouped.get((agent, day), [])
                    # Scenario C: exactly one valid record on an existing unique key.
                    if len(valid) != 1:
                        continue
                    rec = valid[0]
                    llm_ids = list(rec["picked"])
                    if len(llm_ids) != len(set(llm_ids)):
                        raise AssertionError("Duplicate ids inside one picked list")
                    def totals(ids: list[str]) -> dict[str, float]:
                        crit_set = set(ids) & critical_ids
                        critical_return = math.fsum(_logcite(by_id[i]) for i in crit_set)
                        total_return = math.fsum(_logcite(by_id[i]) for i in ids)
                        return {
                            "n": len(ids), "hits": len(crit_set),
                            "return": total_return,
                            "critical_return": critical_return,
                            "noncritical_return": total_return - critical_return,
                        }
                    L, P = totals(llm_ids), totals(param_ids)
                    # The recorded total-return endpoint must agree with this
                    # reconstruction before it is decomposed.
                    if not math.isclose(L["return"], float(rec["value_llm"]), abs_tol=1e-10):
                        raise AssertionError(f"value_llm mismatch at {family}/{run}/{agent}/{day}")
                    if not math.isclose(P["return"], float(rec["value_param"]), abs_tol=1e-10):
                        raise AssertionError(f"value_param mismatch at {family}/{run}/{agent}/{day}")
                    if L["hits"] != rec["hits_llm"] or P["hits"] != rec["hits_param"]:
                        raise AssertionError(f"hit mismatch at {family}/{run}/{agent}/{day}")
                    if len(critical_ids) != rec["n_crit"]:
                        raise AssertionError(f"n_crit mismatch at {family}/{run}/{agent}/{day}")
                    cells.append({
                        "delta_hits": L["hits"] - P["hits"],
                        "delta_n": L["n"] - P["n"],
                        "delta_return": L["return"] - P["return"],
                        "delta_critical_return": L["critical_return"] - P["critical_return"],
                        "delta_noncritical_return": L["noncritical_return"] - P["noncritical_return"],
                        "n_crit_opportunities": len(critical_ids),
                    })
            if not cells:
                raise AssertionError(f"No strict-singleton cells for {family}/{run}")
            row = {"family": family, "run": run, "n_cells": len(cells)}
            for field in ("delta_hits", "delta_n", "delta_return",
                          "delta_critical_return", "delta_noncritical_return"):
                row[field] = math.fsum(c[field] for c in cells) / len(cells)
            row["recall_delta"] = (math.fsum(c["delta_hits"] for c in cells)
                                   / math.fsum(c["n_crit_opportunities"] for c in cells))
            # Execute (not merely describe) the scenario-C regression check.
            reference = frozen_c[(family, run)]
            if not math.isclose(row["recall_delta"], float(reference["delta_recall"]),
                                rel_tol=0, abs_tol=1e-10):
                raise AssertionError(f"Scenario-C recall mismatch for {family}/{run}")
            if not math.isclose(row["delta_return"], float(reference["delta_value"]),
                                rel_tol=0, abs_tol=1e-10):
                raise AssertionError(f"Scenario-C return mismatch for {family}/{run}")
            if len(cells) != int(reference["n_resolved_recall"]):
                raise AssertionError(f"Scenario-C cell-count mismatch for {family}/{run}")
            run_rows.append(row)

    families = {}
    for family in FAMILY_ORDER:
        rr = [r for r in run_rows if r["family"] == family]
        item = {"n_runs": len(rr), "n_cells": sum(r["n_cells"] for r in rr)}
        for field in ("recall_delta", "delta_n", "delta_return",
                      "delta_critical_return", "delta_noncritical_return"):
            vals = [r[field] for r in rr]
            item[field] = {"run_equal_mean": math.fsum(vals) / len(vals),
                           "run_bootstrap_95ci": _bootstrap(vals)}
        item["identity_max_abs_error"] = max(
            abs(r["delta_return"] - r["delta_critical_return"] - r["delta_noncritical_return"])
            for r in rr)
        families[family] = item
    summary = {
        "schema": "sea.v19.recall-citation-return-decomposition/v1",
        "status": STATUS,
        "scenario": "C strict singleton: exactly one valid record per existing run/agent/sim_day key",
        "new_experiment": False,
        "new_llm_calls": 0,
        "value_semantics": "sum of log1p(citation) for selected papers; not SEA decision value or welfare",
        "decomposition": "delta_return = delta_critical_return + delta_noncritical_return",
        "validation": {
            "scenario_C_80_of_80_recall_return_cellcount_match": True,
            "all_cell_hit_and_value_fields_reconstructed": True,
            "corpus_lite_json_sha256": hashlib.sha256(
                (ROOT / "sim/pilot/data/corpus_lite.json").read_bytes()).hexdigest(),
            "scenario_C_run_metrics_sha256": hashlib.sha256(frozen_path.read_bytes()).hexdigest(),
            "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        },
        "families": families,
        "interpretation_guardrails": [
            "All 80 configurations share one 30-day corpus and fixed retrospective labels.",
            "The parametric proxy contains log citations and is not an honest ex-ante baseline.",
            "Family, backend, quantization, prompting and reasoning budgets remain confounded.",
            "The decomposition is descriptive; it does not prove why a model made a selection.",
        ],
        "skipped_non_main_tags": skipped,
        "input_shards": sum(len(v) for v in shards.values()),
    }
    return summary, run_rows


def render(s: dict[str, Any]) -> str:
    lines = [
        "# Recall versus citation-weighted return: strict-singleton decomposition",
        "",
        f"**Status: `{STATUS}`.** No new model calls or intervention data.",
        "",
        "The former ‘value’ is the selected papers’ sum of log1p(citation), not "
        "decision utility, SEA value, or human welfare. The identity below is an "
        "accounting decomposition, not a causal explanation:",
        "",
        "$\\Delta$return = $\\Delta$critical-item return + $\\Delta$noncritical-item return.",
        "",
        "| Family | Δrecall | Δtotal citation return [run CI] | Δcritical-item return | Δnoncritical-item return | Δselected count |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for fam, item in s["families"].items():
        def fmt(field: str, ci: bool = False) -> str:
            x = item[field]
            base = f"{x['run_equal_mean']:+.6f}"
            return base + (f" [{x['run_bootstrap_95ci'][0]:+.6f}, {x['run_bootstrap_95ci'][1]:+.6f}]" if ci else "")
        lines.append(f"| {fam} | {fmt('recall_delta')} | {fmt('delta_return', True)} | "
                     f"{fmt('delta_critical_return')} | {fmt('delta_noncritical_return')} | {fmt('delta_n')} |")
    lines += [
        "",
        "A positive recall difference does not imply a positive citation-return difference. "
        "The critical/noncritical columns are consistent with both substitution and changed "
        "selected counts; the decomposition does not separate those mechanisms. O's "
        "critical-item interval includes zero, and C/Q's noncritical intervals include zero. "
        "The endpoint remains a retrospective academic-impact proxy; none of these columns "
        "establishes decision value, welfare, or the overall effect of SEA.",
        "",
        "`run_metrics.csv` preserves all 80 run-level estimates. CIs resample runs within "
        "family (10,000 times, seed 42) and do not include shared-corpus or model dependence.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    summary, rows = audit()
    text = json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True)
    if not args.write:
        print(text)
        return
    OUTDIR.mkdir(parents=True, exist_ok=True)
    targets = [OUTDIR / "summary.json", OUTDIR / "REPORT.md", OUTDIR / "run_metrics.csv"]
    if any(p.exists() for p in targets) and not args.force:
        raise SystemExit("Artifacts exist; use --force to replace them")
    (OUTDIR / "summary.json").write_text(text + "\n", encoding="utf-8")
    (OUTDIR / "REPORT.md").write_text(render(summary), encoding="utf-8")
    fields = ["family", "run", "n_cells", "recall_delta", "delta_hits", "delta_n",
              "delta_return", "delta_critical_return", "delta_noncritical_return"]
    with (OUTDIR / "run_metrics.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(targets)} artifacts to {OUTDIR}")


if __name__ == "__main__":
    main()
