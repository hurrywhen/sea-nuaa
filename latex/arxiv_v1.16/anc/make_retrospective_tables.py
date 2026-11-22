#!/usr/bin/env python3
"""Single-source generator for the retrospective Rule A / strict-singleton tables.

The SB.1–SB.3 tables (Supplementary Tables SB1–SB3) exist in exactly one
authoritative location: section R5 of
``docs/SUPPLEMENT_RETROSPECTIVE_AUDITS_v1.16.md``.  This tool regenerates that
section from the frozen data files instead of hand-copying numbers:

- ``sim/pilot/results/v110_consumption_caliber/scenario_effects.csv``
  (Rule A cohort counts/estimates/intervals; 17-scenario ranges);
- ``sim/pilot/results/v19_recall_value_tradeoff/summary.json``
  (strict-singleton critical/noncritical decomposition and intervals).

Default: read-only verification that the supplement's R5 section equals the
regenerated text (exit 1 on any drift).  ``--write`` additionally emits the
dedicated artifact ``sim/pilot/results/retrospective_tables_v1.16/``;
replacement requires ``--force``.  No LLM calls, network access, or new data.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCENARIO_CSV = ROOT / "sim/pilot/results/v110_consumption_caliber/scenario_effects.csv"
TRADEOFF_JSON = ROOT / "sim/pilot/results/v19_recall_value_tradeoff/summary.json"
SUPPLEMENT = ROOT / "docs/SUPPLEMENT_RETROSPECTIVE_AUDITS_v1.16.md"
OUTDIR = ROOT / "sim/pilot/results/retrospective_tables_v1.16"
FAMILIES = ("O", "C", "Q", "G")
MINUS = "\u2212"  # typographic minus used by the supplement tables


def signed(value: float, digits: int = 6) -> str:
    text = f"{abs(value):.{digits}f}"
    return ("+" if value >= 0 else MINUS) + text


def interval(low: float, high: float) -> str:
    return f"[{signed(low)}, {signed(high)}]"


def crosses_zero(low: float, high: float) -> bool:
    return low <= 0 <= high


def sign_changes(values: list[float]) -> int:
    signs = [(1 if v > 0 else -1 if v < 0 else 0) for v in values]
    return sum(1 for a, b in zip(signs, signs[1:]) if a != b)


def load_inputs() -> tuple[list[dict], dict]:
    with SCENARIO_CSV.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    tradeoff = json.loads(TRADEOFF_JSON.read_text(encoding="utf-8"))
    scenarios = sorted({row["scenario"] for row in rows})
    if len(scenarios) != 17 or len(rows) != 68:
        raise SystemExit("expected 17 scenarios x 4 families in scenario_effects.csv")
    if tradeoff["scenario"] != "C strict singleton: exactly one valid record per existing run/agent/sim_day key":
        raise SystemExit("unexpected tradeoff scenario identity")
    return rows, tradeoff


def generate_r5(rows: list[dict], tradeoff: dict) -> str:
    rule_a = {row["family"]: row for row in rows if row["scenario"] == "A"}
    n_recall = sum(int(rule_a[f]["n_recall"]) for f in FAMILIES)
    n_return = sum(int(rule_a[f]["n_return"]) for f in FAMILIES)
    n_sign = sum(int(rule_a[f]["n_sign"]) for f in FAMILIES)
    families = tradeoff["families"]
    n_cells = sum(families[f]["n_cells"] for f in FAMILIES)

    lines = [
        "## R5 Secondary Rule A and strict-singleton calibers",
        "",
        f"Rule A uses nonempty selections with metric-specific cohorts: {n_recall:,} recall, "
        f"{n_return:,} citation-return, {n_sign:,} paired-sign keys. Strict singleton uses exactly "
        f"one nonempty record per key: {n_cells:,} common keys. These populations differ from the "
        "all-record calibers and must not be subtracted cell by cell.",
        "",
        "### SB.1 Rule A: nonempty selections with metric-specific cohorts",
        "",
        f"**Supplementary Table SB1. Secondary Rule A: {n_recall:,} recall, {n_return:,} "
        f"citation-return, and {n_sign:,} paired-sign resolved keys.**",
        "",
        "| Family | R/V/S keys | Selected recall | Parametric recall | $\\Delta$recall [interval] | $\\Delta$citation return [interval] |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for f in FAMILIES:
        row = rule_a[f]
        keys = f"{int(row['n_recall']):,} / {int(row['n_return']):,} / {int(row['n_sign']):,}"
        dr = (f"{signed(float(row['delta_recall']))} "
              f"{interval(float(row['delta_recall_ci95_low']), float(row['delta_recall_ci95_high']))}")
        dv = (f"{signed(float(row['delta_return']))} "
              f"{interval(float(row['delta_return_ci95_low']), float(row['delta_return_ci95_high']))}")
        lines.append(f"| {f} | {keys} | {float(row['recall_llm']):.6f} | "
                     f"{float(row['recall_param']):.6f} | {dr} | {dv} |")
    lines += [
        "",
        "### SB.2 Strict-singleton citation-return accounting",
        "",
        f"**Supplementary Table SB2. Strict-singleton C: {n_cells:,} common keys; selected "
        "citation-return accounting decomposition.**",
        "",
        "| Family | Keys | $\\Delta$critical-item return | $\\Delta$noncritical-item return | Total return | $\\Delta$selected count |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for f in FAMILIES:
        fam = families[f]
        lines.append(
            f"| {f} | {fam['n_cells']:,} | {signed(fam['delta_critical_return']['run_equal_mean'])} | "
            f"{signed(fam['delta_noncritical_return']['run_equal_mean'])} | "
            f"{signed(fam['delta_return']['run_equal_mean'])} | "
            f"{signed(fam['delta_n']['run_equal_mean'])} |")
    # Prose claims are verified against the frozen data before being emitted.
    o, g = families["O"], families["G"]
    o_crit_ci = o["delta_critical_return"]["run_bootstrap_95ci"]
    g_crit_ci = g["delta_critical_return"]["run_bootstrap_95ci"]
    o_non_ci = o["delta_noncritical_return"]["run_bootstrap_95ci"]
    g_non_ci = g["delta_noncritical_return"]["run_bootstrap_95ci"]
    assert crosses_zero(*o_crit_ci) and not crosses_zero(*g_crit_ci)
    assert crosses_zero(*o_non_ci) is False and crosses_zero(*g_non_ci) is False
    for f in ("C", "Q"):
        assert crosses_zero(*families[f]["delta_noncritical_return"]["run_bootstrap_95ci"])
    for f in ("O", "G"):
        fam = families[f]
        assert fam["delta_critical_return"]["run_equal_mean"] > 0
        assert abs(fam["delta_noncritical_return"]["run_equal_mean"]) > fam["delta_critical_return"]["run_equal_mean"]
        assert fam["delta_noncritical_return"]["run_equal_mean"] < 0
    favor_llm = {row["family"]: row for row in rows if row["scenario"] == "I_favor_llm"}
    for f in ("O", "G"):
        assert crosses_zero(float(favor_llm[f]["delta_return_ci95_low"]),
                            float(favor_llm[f]["delta_return_ci95_high"]))
    lines += [
        "",
        f"For O, the critical-item component's exploratory interval is {interval(*o_crit_ci)}, "
        f"crossing zero; G's is {interval(*g_crit_ci)}. Noncritical-item intervals are "
        f"{interval(*o_non_ci)} for O and {interval(*g_non_ci)} for G. C/Q noncritical intervals "
        "also cross zero. Positive O/G critical-item point estimates are outweighed by noncritical "
        "declines. Under the intentional favor-LLM endpoint, O/G total-return intervals include "
        "zero. The identity is accounting, not a causal explanation of substitution or changed "
        "counts. Retrospective $\\log(1+\\text{2026 citations})$ is not ex-ante decision utility "
        "or welfare.",
        "",
        "### SB.3 All 17 frozen missing/conflict/endpoint scenarios",
        "",
        "**Supplementary Table SB3. Run-equal point-estimate ranges across all 17 scenarios.**",
        "",
        "| Family | $\\Delta$recall min–max | Recall sign changes | $\\Delta$citation return min–max | Return sign changes |",
        "|---|---:|---:|---:|---:|",
    ]
    for f in FAMILIES:
        fam_rows = [row for row in rows if row["family"] == f]
        dr = [float(row["delta_recall"]) for row in fam_rows]
        dv = [float(row["delta_return"]) for row in fam_rows]
        lines.append(f"| {f} | {signed(min(dr))} to {signed(max(dr))} | {sign_changes(dr)} | "
                     f"{signed(min(dv))} to {signed(max(dv))} | {sign_changes(dv)} |")
    recall_positive = all(float(row["delta_recall"]) > 0 for row in rows)
    return_sign = {f: {("pos" if float(row["delta_return"]) > 0 else "neg")
                       for row in rows if row["family"] == f} for f in FAMILIES}
    assert recall_positive
    assert return_sign["C"] == return_sign["Q"] == {"pos"}
    assert return_sign["O"] == return_sign["G"] == {"neg"}
    lines += [
        "",
        "Recall point estimates stay positive in all 17 scenarios; citation return stays positive "
        "for C/Q and negative for O/G. Zero point-estimate sign changes do not make every interval "
        "exclude zero and do not identify a structural effect. Exact per-scenario denominators and "
        "intervals remain in `scenario_effects.csv`.",
    ]
    return "\n".join(lines)


def supplement_r5(text: str) -> str:
    start = text.index("## R5 Secondary Rule A and strict-singleton calibers")
    end = text.index("## R6 Financial and upstream audit details")
    return text[start:end].rstrip("\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="emit the dedicated artifact directory")
    parser.add_argument("--force", action="store_true", help="allow replacing existing artifacts")
    args = parser.parse_args()
    rows, tradeoff = load_inputs()
    generated = generate_r5(rows, tradeoff)
    supplement = SUPPLEMENT.read_text(encoding="utf-8")
    current = supplement_r5(supplement)
    match = current == generated
    print(f"R5 single-source check: {'MATCH' if match else 'DRIFT'} "
          f"({len(generated.splitlines())} generated lines)")
    if args.write:
        if OUTDIR.exists() and not args.force:
            raise SystemExit(f"Refusing to overwrite without --force: {OUTDIR}")
        OUTDIR.mkdir(parents=True, exist_ok=True)
        (OUTDIR / "r5_section.md").write_text(generated + "\n", encoding="utf-8")
        rule_a = {row["family"]: row for row in rows if row["scenario"] == "A"}
        values = {
            "schema": "sea.retrospective-tables-single-source/v1",
            "inputs": {
                "scenario_effects_csv": str(SCENARIO_CSV.relative_to(ROOT)),
                "recall_value_tradeoff_summary": str(TRADEOFF_JSON.relative_to(ROOT)),
            },
            "rule_a_totals": {
                "n_recall": sum(int(rule_a[f]["n_recall"]) for f in FAMILIES),
                "n_return": sum(int(rule_a[f]["n_return"]) for f in FAMILIES),
                "n_sign": sum(int(rule_a[f]["n_sign"]) for f in FAMILIES),
            },
            "strict_singleton_common_keys": sum(tradeoff["families"][f]["n_cells"] for f in FAMILIES),
            "supplement_section_matches_generated": match,
            "status": "FROZEN_RETROSPECTIVE_DESCRIPTION__NOT_EFFECT_EVIDENCE",
        }
        (OUTDIR / "values.json").write_text(json.dumps(values, ensure_ascii=False, indent=2) + "\n",
                                            encoding="utf-8")
        print(f"Wrote {OUTDIR / 'r5_section.md'} and values.json")
    if not match:
        print("Supplement R5 section differs from the frozen-data regeneration; "
              "update the supplement from tools/make_retrospective_tables.py output.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
