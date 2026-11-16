#!/usr/bin/env python3
"""Post-hoc caliber audit for the financial retrospective proxy replay.

This script runs no model and downloads no data.  It reconstructs the deterministic
S2p selection from the frozen lightweight environment, verifies the proposition-
level recalls already stored in ``p2_rows.csv``, and reports company-day and
proposition denominators separately.  It also exports the observed source-class
by critical-proposition coverage matrix.  The binary matrix is a descriptive
cross-tabulation, not an estimate of a proposition-conditional probability floor
or of independence between source classes.

Default: print the JSON summary only.  ``--write`` creates a dedicated artifact
set; existing files require ``--force``.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import subprocess
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

try:
    from . import config
    from .p2_environment import build_all
    from .strategies import select
except ImportError:  # direct script execution
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from sea_pilot import config
    from sea_pilot.p2_environment import build_all
    from sea_pilot.strategies import select

ROOT = Path(__file__).resolve().parents[2]
OUTDIR = ROOT / "sim" / "pilot" / "results" / "v19_financial_caliber_audit"
CLASSES = ("regulator", "wire", "fin_media", "tech_media", "aggregator", "general", "other")
STATUS = "POST_HOC_CALIBER_AUDIT__SAME_CORPUS_DESCRIPTIVE"


def _z(x: np.ndarray) -> np.ndarray:
    return (x - x.mean()) / (x.std() + 1e-9)


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def _ratio(hits: int, total: int) -> dict[str, Any]:
    return {
        "hits": hits,
        "opportunities": total,
        "ratio": hits / total if total else None,
        "fraction": str(Fraction(hits, total)) if total else None,
    }


def audit() -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    os.environ["SEA_FORCE_LITE"] = "1"
    env = build_all(verbose=False)
    props = env["props"]
    n = len(props)
    day = np.array([int(p["date"][8:10]) - 1 for p in props], dtype=int)
    crit_legal = np.array([p["legal_critical"] for p in props], dtype=bool)
    crit_market = np.array([p["market_critical"] for p in props], dtype=bool)
    port_mask = np.array([p["in_portfolio"] for p in props], dtype=bool)
    imp = 2.0 * crit_legal + 2.0 * crit_market + 0.5 * _z(
        np.array([p["n_docs"] for p in props], dtype=float))
    order = np.lexsort((np.array([p["pid"] for p in props]), day))
    rows_path = ROOT / "sim" / "pilot" / "results" / "p2_rows.csv"
    with rows_path.open(encoding="utf-8", newline="") as f:
        frozen = list(csv.DictReader(f))

    comparisons: list[dict[str, Any]] = []
    # rho=0.4 is ri=1 in the frozen run_p2 loop.  Reconstruct every S2p agent
    # and check its proposition recall against the legacy row before adding the
    # company-day caliber.
    for ai in range(config.N_AGENTS):
        m = config.BUDGETS_PER_DAY_P2[ai % len(config.BUDGETS_PER_DAY_P2)]
        rng = np.random.default_rng(config.SEED + 7000 + ai)
        proxy = 0.4 * _z(imp) + math.sqrt(1 - 0.4 ** 2) * rng.standard_normal(n)
        selected, info = select(
            "S2", m * config.SIM_DAYS_P2, order=order,
            hype=np.zeros(n), proxy=proxy, wl_mask=port_mask,
        )
        selected_set = set(int(i) for i in selected)
        target_idx = [i for i, p in enumerate(props)
                      if p["market_critical"] and p["in_portfolio"]]
        target_days = {(props[i]["ticker"], props[i]["date"]) for i in target_idx}
        hit_days = {(props[i]["ticker"], props[i]["date"])
                    for i in selected_set
                    if props[i]["market_critical"] and props[i]["in_portfolio"]}
        hit_props = sum(i in selected_set for i in target_idx)
        legacy = [r for r in frozen
                  if r["arm"] == "S2p" and r["rho"] == "0.4"
                  and r["truth"] == "market" and int(r["agent"]) == ai]
        if len(legacy) != 1:
            raise AssertionError(f"Expected one frozen S2p row for agent {ai}")
        old = float(legacy[0]["recall_mkt_port"])
        new = hit_props / len(target_idx)
        if not math.isclose(old, new, rel_tol=0, abs_tol=1e-12):
            raise AssertionError(f"Proposition recall mismatch at agent {ai}: {old} != {new}")
        comparisons.append({
            "agent": ai,
            "budget_per_day": m,
            "proposition": _ratio(hit_props, len(target_idx)),
            "company_day": _ratio(len(hit_days), len(target_days)),
            "legacy_proposition_ratio_verified": old,
            "budget_conflict_alarm": bool(info["alarm_budget_conflict"]),
            "budget_window": "month",
            "slots": m * config.SIM_DAYS_P2,
            "strict_daily_cap_enforced": False,
        })

    m5 = [r for r in comparisons if r["budget_per_day"] == 5]
    pooled_prop_hits = sum(r["proposition"]["hits"] for r in m5)
    pooled_prop_opps = sum(r["proposition"]["opportunities"] for r in m5)
    pooled_day_hits = sum(r["company_day"]["hits"] for r in m5)
    pooled_day_opps = sum(r["company_day"]["opportunities"] for r in m5)

    # Read the earlier frozen configuration from git history without changing the
    # worktree. The earlier headline is 120/(7x18), not a 21-target corpus.
    old_text = subprocess.check_output(
        ["git", "show", "8ffc7f5:sim/pilot/results/p2_rows.csv"],
        cwd=ROOT, text=True)
    old_rows = list(csv.DictReader(old_text.splitlines()))
    old_m5 = [r for r in old_rows if r["arm"] == "S2p" and r["rho"] == "0.4"
              and r["truth"] == "market" and r["budget_per_day"] == "5"]
    old_recall = sum(float(r["recall_mkt_port"]) for r in old_m5) / len(old_m5)
    # Recover the common per-run target denominator from non-degenerate recalls,
    # not from the reduced pooled mean (120/126 reduces to 20/21).
    old_target_count = max(
        (Fraction(float(r["recall_mkt_port"])).limit_denominator(10000).denominator
         for r in old_m5 if 0 < float(r["recall_mkt_port"]) < 1),
        default=0)
    if old_target_count != 18:
        raise AssertionError(f"Unexpected historical target denominator: {old_target_count}")
    old_hits = round(old_recall * old_target_count * len(old_m5))
    old_feat = [r for r in old_rows if r["arm"] == "S2p-feat" and r["rho"] == "0.4"
                and r["truth"] == "market" and r["budget_per_day"] == "5"]
    new_feat = [r for r in frozen if r["arm"] == "S2p-feat" and r["rho"] == "0.4"
                and r["truth"] == "market" and r["budget_per_day"] == "5"]
    semi_oracle_comparison = {
        "historical_git_commit": "8ffc7f5",
        "historical_m5": {
            "agent_proxy_configurations": len(old_m5),
            "proposition_targets_per_run": old_target_count,
            "agent_target_hits": old_hits,
            "agent_target_opportunities": old_target_count * len(old_m5),
            "mean_recall": old_recall,
            "budget_conflict_alarms": sum(r["alarm_budget_conflict"] == "True" for r in old_m5),
            "feature_scorer_mean_recall": sum(float(r["recall_mkt_port"]) for r in old_feat) / len(old_feat),
            "slots_per_run": 5 * config.SIM_DAYS_P2,
            "strict_daily_cap_enforced": False,
        },
        "expanded_m5": {
            "agent_proxy_configurations": len(m5),
            "proposition_targets_per_run": 19,
            "agent_target_hits": pooled_prop_hits,
            "agent_target_opportunities": pooled_prop_opps,
            "mean_recall": pooled_prop_hits / pooled_prop_opps,
            "budget_conflict_alarms": sum(r["budget_conflict_alarm"] for r in m5),
            "feature_scorer_mean_recall": sum(float(r["recall_mkt_port"]) for r in new_feat) / len(new_feat),
            "slots_per_run": 5 * config.SIM_DAYS_P2,
            "strict_daily_cap_enforced": False,
        },
        "channel1_supply_per_day": {
            "historical": 4.6,
            "expanded": env["supply"]["portfolio_props_per_day"],
            "channel1_cap_at_m5": 3,
        },
        "comparison_status": "non-paired descriptive configurations; not a news-expansion causal effect",
        "r4_compliant_95_percent_guarantee_established": False,
    }

    coverage: list[dict[str, Any]] = []
    for p in props:
        if not p["market_critical"]:
            continue
        row: dict[str, Any] = {
            "pid": p["pid"], "ticker": p["ticker"], "date": p["date"],
            "family": p["family"], "in_portfolio": int(p["in_portfolio"]),
        }
        row.update({c: int(c in p["classes"]) for c in CLASSES})
        coverage.append(row)

    port_targets = [p for p in props if p["market_critical"] and p["in_portfolio"]]
    class_counts = {
        scope: {
            c: {
                "covered": sum(c in p["classes"] for p in subset),
                "targets": len(subset),
                "share": sum(c in p["classes"] for p in subset) / len(subset),
            }
            for c in CLASSES
        }
        for scope, subset in (("all_market_proxy", [p for p in props if p["market_critical"]]),
                              ("portfolio_market_proxy", port_targets))
    }
    acceptance = {}
    for scope, subset in (("all_market_proxy", [p for p in props if p["market_critical"]]),
                          ("portfolio_market_proxy", port_targets)):
        acceptance[scope] = {
            "acceptance_hour_ge_13": sum(p["acceptance_hour"] >= 13 for p in subset),
            "acceptance_hour_lt_13": sum(0 <= p["acceptance_hour"] < 13 for p in subset),
            "acceptance_hour_unknown_news": sum(p["acceptance_hour"] < 0 for p in subset),
            "targets": len(subset),
        }
    summary = {
        "schema": "sea.v19.financial-caliber-audit/v1",
        "status": STATUS,
        "new_experiment": False,
        "new_llm_calls": 0,
        "selection_reconstruction_verified_against_p2_rows": True,
        "target_definitions": {
            "proposition": "pid=(ticker,date,family), market_critical and in_portfolio",
            "company_day": "unique (ticker,date) among those propositions",
            "distinct_ticker": "reported for provenance only; not a recall denominator",
        },
        "portfolio_market_proxy": {
            "proposition_targets": len(port_targets),
            "company_day_targets": len({(p["ticker"], p["date"]) for p in port_targets}),
            "distinct_tickers": len({p["ticker"] for p in port_targets}),
            "family_counts": {
                family: sum(p["family"] == family for p in port_targets)
                for family in sorted({p["family"] for p in port_targets})
            },
        },
        "m5_run_level": m5,
        "m5_pooled_across_runs": {
            "n_runs": len(m5),
            "proposition": _ratio(pooled_prop_hits, pooled_prop_opps),
            "company_day": _ratio(pooled_day_hits, pooled_day_opps),
            "note": ("121/133 pools 121 proposition hits over 7 runs x 19 targets; "
                     "it is not a single-corpus denominator. The 0.909774 value is "
                     "also the unweighted mean of the seven run recalls because every "
                     "run has the same 19-target denominator."),
        },
        "semi_oracle_configuration_comparison": semi_oracle_comparison,
        "timestamp_audit": acceptance,
        "selection_proxy_warning": (
            "The parametric selection score uses realized legal and market labels; "
            "headline S2p recall is semi-oracle. Feature-only comparisons are reported "
            "separately and still have timestamp limitations."),
        "class_coverage_descriptive": class_counts,
        "independence_warning": (
            "Conditional recovery and disjoint class indicators are not evidence of "
            "mutual independence. Because pid includes family, regulatory and news "
            "items can be distinct targets for the same company-day; class coverage "
            "is therefore confounded with target construction."),
        "legacy_18_to_19_note": (
            "The target count increases from 18 to 19 propositions, which is valid "
            "at proposition level. The expanded 19 propositions represent 18 "
            "company-days (10 tickers), not a company-day increase from 18 to 19. "
            "The configurations and target sets are non-paired; the historical "
            "company-day denominator was not independently reconstructed."),
        "inputs": {},
    }
    for rel in ("sim/pilot/data/p2_env_lite.json", "sim/pilot/results/p2_rows.csv"):
        path = ROOT / rel
        summary["inputs"][rel] = {"sha256": _sha256(path), "bytes": path.stat().st_size}
    return summary, coverage, comparisons


def render(summary: dict[str, Any]) -> str:
    p = summary["portfolio_market_proxy"]
    pooled = summary["m5_pooled_across_runs"]
    semi_oracle_comparison = summary["semi_oracle_configuration_comparison"]
    acceptance = summary["timestamp_audit"]
    lines = [
        "# Financial replay caliber audit (v1.9)",
        "",
        f"**Status: `{STATUS}`.** No LLM calls, downloads, or new intervention data.",
        "",
        "## Denominators",
        "",
        f"The expanded configuration has **{p['proposition_targets']} critical propositions**, "
        f"**{p['company_day_targets']} critical company-days**, and "
        f"{p['distinct_tickers']} distinct tickers. A proposition is keyed by "
        "`(ticker,date,family)`; these units must not be interchanged.",
        "",
        "| Unit | Hits / opportunities (pooled over seven m=5 runs) | Ratio |",
        "|---|---:|---:|",
    ]
    for key, label in (("proposition", "Agent–proposition evaluation"),
                       ("company_day", "Agent–company-day evaluation")):
        r = pooled[key]
        lines.append(f"| {label} | {r['hits']} / {r['opportunities']} | {r['ratio']:.9f} |")
    lines += [
        "",
        "The proposition value 121/133 = 0.9097744361 pools seven runs with 19 "
        "targets each. It is not one independent 133-target corpus. The increase "
        "18→19 is valid in proposition units, but not in company-day units: the "
        "expanded 19 propositions represent 18 company-days. The configurations "
        "are non-paired, and the historical company-day denominator was not reconstructed.",
        "",
        "## Semi-oracle configurations, budget alarms, and supervised feature-scorer comparisons",
        "",
        "| Configuration | Parametric S2p agent–target recall | Supervised feature-scorer mean recall | Budget-conflict alarms |",
        "|---|---:|---:|---:|",
        f"| Historical | 120/(7×18) = {semi_oracle_comparison['historical_m5']['mean_recall']:.9f} | "
        f"{semi_oracle_comparison['historical_m5']['feature_scorer_mean_recall']:.9f} | "
        f"{semi_oracle_comparison['historical_m5']['budget_conflict_alarms']}/7 |",
        f"| Expanded | 121/(7×19) = {semi_oracle_comparison['expanded_m5']['mean_recall']:.9f} | "
        f"{semi_oracle_comparison['expanded_m5']['feature_scorer_mean_recall']:.9f} | "
        f"{semi_oracle_comparison['expanded_m5']['budget_conflict_alarms']}/7 |",
        "",
        "The parametric score uses realized legal/market labels and is semi-oracle. "
        "Both m=5 configurations use 150 monthly slots rather than a strict daily cap. "
        "Supply (4.6/4.733 propositions per day) exceeds the Channel-I cap (3/day), "
        "and every m=5 run alarms. Neither configuration establishes an R4-compliant "
        "95% delivery guarantee. The supervised feature scorer is trained on day<15 "
        "realized labels and evaluated descriptively over the full month. Its identical "
        "deterministic selection is repeated across seven agent rows, not seven "
        "independent feature experiments; it is neither label-free nor held-out evidence.",
        "",
        "## Per-run reconstruction",
        "",
        "| Agent | Proposition recall | Company-day recall |",
        "|---:|---:|---:|",
    ]
    for r in summary["m5_run_level"]:
        lines.append(f"| {r['agent']} | {r['proposition']['hits']}/{r['proposition']['opportunities']} = "
                     f"{r['proposition']['ratio']:.9f} | {r['company_day']['hits']}/{r['company_day']['opportunities']} = "
                     f"{r['company_day']['ratio']:.9f} |")
    lines += [
        "",
        "Every reconstructed proposition recall equals the frozen `p2_rows.csv` value "
        "to 1e-12. The company-day column is a post-hoc unit-sensitivity description, "
        "not a new confirmatory result.",
        "",
        "## Coverage matrix interpretation",
        "",
        "`critical_coverage_matrix.csv` contains one binary row per market-proxy "
        "proposition and one column per source class. These are observed indicators, "
        "not repeated Bernoulli samples for each proposition. They estimate neither "
        "a uniform proposition-conditional `p_min` nor `k_eff`. Conditional recovery "
        "does not establish independence; target construction by `family` also "
        "confounds source class and target type.",
        "",
        "## Timestamp availability",
        "",
        f"Among the 19 portfolio targets, {acceptance['portfolio_market_proxy']['acceptance_hour_ge_13']} "
        f"have acceptance_hour>=13, {acceptance['portfolio_market_proxy']['acceptance_hour_unknown_news']} "
        f"are news items without that timestamp, and only "
        f"{acceptance['portfolio_market_proxy']['acceptance_hour_lt_13']} satisfy the code's <13 marker. "
        "The marker is a feature, not a pre-availability filter.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    summary, coverage, comparisons = audit()
    text = json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True)
    if not args.write:
        print(text)
        return
    OUTDIR.mkdir(parents=True, exist_ok=True)
    targets = [OUTDIR / "summary.json", OUTDIR / "REPORT.md",
               OUTDIR / "critical_coverage_matrix.csv", OUTDIR / "run_recall_by_unit.csv"]
    if any(p.exists() for p in targets) and not args.force:
        raise SystemExit("Artifacts exist; use --force to replace the dedicated v1.9 audit set")
    (OUTDIR / "summary.json").write_text(text + "\n", encoding="utf-8")
    (OUTDIR / "REPORT.md").write_text(render(summary), encoding="utf-8")
    with (OUTDIR / "critical_coverage_matrix.csv").open("w", encoding="utf-8", newline="") as f:
        fields = ["pid", "ticker", "date", "family", "in_portfolio", *CLASSES]
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(coverage)
    with (OUTDIR / "run_recall_by_unit.csv").open("w", encoding="utf-8", newline="") as f:
        fields = ["agent", "budget_per_day", "unit", "hits", "opportunities", "ratio"]
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for r in comparisons:
            for unit in ("proposition", "company_day"):
                writer.writerow({"agent": r["agent"], "budget_per_day": r["budget_per_day"],
                                 "unit": unit, "hits": r[unit]["hits"],
                                 "opportunities": r[unit]["opportunities"],
                                 "ratio": r[unit]["ratio"]})
    print(f"Wrote {len(targets)} artifacts to {OUTDIR}")


if __name__ == "__main__":
    main()
