#!/usr/bin/env python3
"""Read-only integrity audit for the 292 four-family replay JSONL shards.

Default behavior is strictly read-only: the report is printed to stdout and no
files are created or modified. Use --write to emit the two dedicated result
artifacts (JSON + Markdown). Existing output files are never overwritten unless
--force is also supplied.

Run from the repository root:

    PYTHONDONTWRITEBYTECODE=1 python3 sim/sea_pilot/audit_replay_integrity.py
    PYTHONDONTWRITEBYTECODE=1 python3 sim/sea_pilot/audit_replay_integrity.py --write

Dependencies: Python >= 3.10 and NumPy. All replay JSONL files are treated as
immutable inputs. No first/last-row deduplication or other outcome arbitration
is performed. Legacy contrasts are explicitly marked as
LEGACY_EXPLORATORY_NOT_DEDUPLICATED and are not frozen primary results.
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Iterable

import numpy as np

VERSION = "1.0.0"
STATUS = "LEGACY_EXPLORATORY_NOT_DEDUPLICATED"
DISPOSITION = "UNRESOLVED_PREREGISTRATION_REQUIRED_THEN_RECOMPUTE"
TAG_RE = re.compile(r"^(oa|od|qc|ga|o|c|q|g)_r(\d{2})([a-f])?$")
FAMILY_OF = {"o": "O", "oa": "O", "od": "O", "c": "C", "q": "Q", "qc": "Q", "g": "G", "ga": "G"}
EXPECTED_RUNS = {"O": set(range(1, 31)), "C": set(range(1, 31)),
                 "Q": set(range(1, 11)), "G": set(range(1, 11))}
FAMILY_ORDER = ("O", "C", "Q", "G")
NOMINAL_PER_RUN = 900
NOMINAL_TOTAL = 72000
EXPECTED_SHARDS = 292
BOOTSTRAP_B = 10000
BOOTSTRAP_SEED = 42
OUTCOME_FIELDS = ("picked", "hits_llm", "hits_param", "n_crit",
                  "value_llm", "value_param")


def is_valid(record: dict[str, Any]) -> bool:
    """Protocol V-3, matching the legacy pipeline: nonempty picked only."""
    return bool(record.get("picked"))


def outcome(record: dict[str, Any]) -> tuple[Any, ...]:
    """Fields compared for same/different duplicate outcomes (order preserved)."""
    return tuple(record.get(field) for field in OUTCOME_FIELDS)


def load_runs(results_dir: Path) -> tuple[dict[tuple[str, int], list[dict[str, Any]]],
                                           dict[tuple[str, int], list[str]], list[str]]:
    """Read immutable shards, retaining file/line provenance without editing them."""
    runs: dict[tuple[str, int], list[dict[str, Any]]] = collections.defaultdict(list)
    shards: dict[tuple[str, int], list[str]] = collections.defaultdict(list)
    skipped: list[str] = []
    for path in sorted(results_dir.glob("llm_replay_*.jsonl")):
        tag = path.name[len("llm_replay_"):-len(".jsonl")]
        match = TAG_RE.match(tag)
        if not match:
            skipped.append(tag)
            continue
        family = FAMILY_OF[match.group(1)]
        run_no = int(match.group(2))
        key = (family, run_no)
        shards[key].append(path.name)
        with path.open(encoding="utf-8") as handle:
            for line_no, line in enumerate(handle, start=1):
                if not line.strip():
                    continue
                record = json.loads(line)
                record["_source_file"] = path.name
                record["_source_line"] = line_no
                runs[key].append(record)
    got = {family: {run for (fam, run) in runs if fam == family}
           for family in EXPECTED_RUNS}
    missing = {family: sorted(EXPECTED_RUNS[family] - got[family])
               for family in EXPECTED_RUNS}
    missing = {family: runs for family, runs in missing.items() if runs}
    if missing:
        raise ValueError(f"Missing expected runs: {missing}")
    n_shards = sum(len(files) for files in shards.values())
    if n_shards != EXPECTED_SHARDS:
        raise ValueError(f"Expected {EXPECTED_SHARDS} replay shards, found {n_shards}")
    return runs, shards, skipped


def run_metrics(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Compute row accounting and unique run/agent/sim_day key accounting."""
    valid_records = [record for record in records if is_valid(record)]
    grouped: dict[tuple[Any, Any], list[dict[str, Any]]] = collections.defaultdict(list)
    for record in valid_records:
        grouped[(record.get("agent"), record.get("sim_day"))].append(record)

    same_keys = different_keys = 0
    same_excess = different_excess = 0
    examples: list[dict[str, Any]] = []
    for key, group in grouped.items():
        if len(group) < 2:
            continue
        outcomes = [json.dumps(outcome(record), ensure_ascii=False) for record in group]
        if len(set(outcomes)) == 1:
            same_keys += 1
            same_excess += len(group) - 1
            comparison = "same"
        else:
            different_keys += 1
            different_excess += len(group) - 1
            comparison = "different"
        examples.append({"agent": key[0], "sim_day": key[1],
                         "comparison": comparison, "records": group})
    unique = len(grouped)
    valid = len(valid_records)
    return {
        "raw": len(records),
        "empty": len(records) - valid,
        "valid": valid,
        "unique": unique,
        "duplicate_excess": valid - unique,
        "duplicate_groups": same_keys + different_keys,
        "same_outcome_keys": same_keys,
        "different_outcome_keys": different_keys,
        "same_outcome_excess": same_excess,
        "different_outcome_excess": different_excess,
        "unique_shortfall_vs_900": max(0, NOMINAL_PER_RUN - unique),
        "below_nominal_900": unique < NOMINAL_PER_RUN,
        "_valid_records": valid_records,
        "_duplicate_examples": examples,
    }


def legacy_metrics(records: list[dict[str, Any]]) -> dict[str, float]:
    """Legacy, non-deduplicated run metrics used only for exploratory contrasts."""
    valid = [record for record in records if is_valid(record)]
    critical = sum(record.get("n_crit", 0) for record in valid)
    llm_hits = sum(record.get("hits_llm", 0) for record in valid)
    param_hits = sum(record.get("hits_param", 0) for record in valid)
    differences = [record.get("value_llm", 0.0) - record.get("value_param", 0.0)
                   for record in valid]
    return {
        "recall_contrast": (llm_hits - param_hits) / critical if critical else float("nan"),
        "dvalue": float(np.mean(differences)) if differences else float("nan"),
    }


def bootstrap_ci(values: Iterable[float]) -> tuple[float, list[float]]:
    """Unweighted family mean of run estimates; percentile bootstrap over runs."""
    array = np.asarray(list(values), dtype=float)
    array = array[np.isfinite(array)]
    if not len(array):
        return float("nan"), [float("nan"), float("nan")]
    rng = np.random.default_rng(BOOTSTRAP_SEED)
    indices = rng.integers(0, len(array), size=(BOOTSTRAP_B, len(array)))
    means = array[indices].mean(axis=1)
    return float(array.mean()), [float(x) for x in np.percentile(means, [2.5, 97.5])]


def compact_run_metrics(metrics: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in metrics.items() if not key.startswith("_")}


def example_record(record: dict[str, Any]) -> dict[str, Any]:
    """De-identified file/line and numeric outcome provenance; no rationale text."""
    return {
        "file": record["_source_file"],
        "line": record["_source_line"],
        "outcome": outcome(record),
    }


def build_summary(runs: dict[tuple[str, int], list[dict[str, Any]]],
                  shards: dict[tuple[str, int], list[str]], skipped: list[str]) -> dict[str, Any]:
    per_run: dict[tuple[str, int], dict[str, Any]] = {}
    all_examples: list[dict[str, Any]] = []
    for key, records in runs.items():
        per_run[key] = run_metrics(records)
        all_examples.extend(per_run[key]["_duplicate_examples"])

    manifest = []
    for family, run_no in sorted(per_run, key=lambda key: (FAMILY_ORDER.index(key[0]), key[1])):
        entry = {"family": family, "run": run_no,
                 "shards": sorted(shards[(family, run_no)])}
        entry.update(compact_run_metrics(per_run[(family, run_no)]))
        manifest.append(entry)

    family_summaries: dict[str, dict[str, Any]] = {}
    for family in FAMILY_ORDER:
        selected = [metrics for (fam, _), metrics in per_run.items() if fam == family]
        totals: dict[str, Any] = {}
        for field in ("raw", "empty", "valid", "unique", "duplicate_excess",
                      "duplicate_groups", "same_outcome_keys", "different_outcome_keys",
                      "same_outcome_excess", "different_outcome_excess",
                      "unique_shortfall_vs_900"):
            totals[field] = sum(metrics[field] for metrics in selected)
        totals["below_nominal_900"] = sum(metrics["below_nominal_900"] for metrics in selected)
        totals["runs"] = len(selected)
        totals["nominal_agent_days"] = totals["runs"] * NOMINAL_PER_RUN
        totals["unique_deficit_vs_nominal"] = totals["nominal_agent_days"] - totals["unique"]
        family_summaries[family] = totals

    totals: dict[str, Any] = {}
    for field in ("raw", "empty", "valid", "unique", "duplicate_excess",
                  "duplicate_groups", "same_outcome_keys", "different_outcome_keys",
                  "same_outcome_excess", "different_outcome_excess",
                  "unique_shortfall_vs_900"):
        totals[field] = sum(family_summaries[family][field] for family in FAMILY_ORDER)
    totals["below_nominal_900"] = sum(family_summaries[family]["below_nominal_900"]
                                      for family in FAMILY_ORDER)
    totals["runs"] = len(manifest)
    totals["shards"] = sum(len(files) for files in shards.values())
    totals["nominal_agent_days"] = NOMINAL_TOTAL
    totals["unique_deficit_vs_nominal"] = NOMINAL_TOTAL - totals["unique"]

    legacy: dict[str, dict[str, Any]] = {}
    for family in FAMILY_ORDER:
        run_estimates = [legacy_metrics(records) for (fam, _), records in runs.items() if fam == family]
        recall_mean, recall_ci = bootstrap_ci([item["recall_contrast"] for item in run_estimates])
        dvalue_mean, dvalue_ci = bootstrap_ci([item["dvalue"] for item in run_estimates])
        legacy[family] = {
            "recall_contrast_mean": recall_mean,
            "recall_contrast_ci95": recall_ci,
            "dvalue_mean": dvalue_mean,
            "dvalue_ci95": dvalue_ci,
        }

    # Prefer the documented c_r01a examples; then add the first same-outcome pair.
    different = sorted((item for item in all_examples if item["comparison"] == "different"),
                       key=lambda item: (item["agent"], item["sim_day"]))
    preferred = sorted((item for item in different
                        if item["agent"] == 0 and item["sim_day"] in {20, 25}
                        and item["records"][0]["_source_file"] == "llm_replay_c_r01a.jsonl"),
                       key=lambda item: item["sim_day"])
    same = sorted((item for item in all_examples if item["comparison"] == "same"),
                  key=lambda item: (item["agent"], item["sim_day"]))
    examples = []
    for item in ((preferred or different[:2]) + same[:2]):
        examples.append({"agent": item["agent"], "sim_day": item["sim_day"],
                         "comparison": item["comparison"],
                         "records": [example_record(record) for record in item["records"]]})

    return {
        "schema": "sea.replay_integrity_audit/v1",
        "script_version": VERSION,
        "status": STATUS,
        "disposition": DISPOSITION,
        "read_only_inputs": True,
        "default_behavior": "stdout only; writes only with --write; no overwrite without --force",
        "source_shards": totals["shards"],
        "skipped_non_main_tags": skipped,
        "unique_key": "(family, run, agent, sim_day)",
        "validity_rule": "bool(record.picked), matching protocol V-3; no deduplication arbitration",
        "duplicate_outcome_fields": list(OUTCOME_FIELDS),
        "run_manifest": manifest,
        "family_totals": family_summaries,
        "totals": totals,
        "duplicate_examples": examples,
        "legacy_exploratory_analysis": {
            "status": STATUS,
            "bootstrap": {"method": "percentile", "resamples": BOOTSTRAP_B,
                          "seed": BOOTSTRAP_SEED, "unit": "run"},
            "recall_contrast_formula": "(sum(hits_llm) - sum(hits_param)) / sum(n_crit)",
            "dvalue_formula": "mean(value_llm - value_param) per run, then unweighted family mean over runs",
            "families": legacy,
        },
    }


def markdown(summary: dict[str, Any]) -> str:
    totals = summary["totals"]
    lines = [
        "# Replay integrity audit — LEGACY_EXPLORATORY_NOT_DEDUPLICATED",
        "",
        "> Independent read-only audit. No first/last-row or other post-hoc deduplication rule is applied.",
        "> These are **not new frozen primary results**. Any unique-key disposition must be pre-specified before reanalysis.",
        "",
        "## Reproduce",
        "",
        "From `~/sea`:",
        "",
        "```bash",
        "# Default: read-only, print report to stdout; writes nothing",
        "PYTHONDONTWRITEBYTECODE=1 python3 sim/sea_pilot/audit_replay_integrity.py",
        "",
        "# Emit only the two dedicated result artifacts (never modifies replay JSONL)",
        "PYTHONDONTWRITEBYTECODE=1 python3 sim/sea_pilot/audit_replay_integrity.py --write",
        "```",
        "",
        "Dependencies: Python >= 3.10 and NumPy. The script uses only immutable replay JSONL inputs.",
        "Existing output files require `--force` for replacement.",
        "",
        "## Totals",
        "",
        f"- Shards: **{totals['shards']}**; runs: **{totals['runs']}**; raw rows: **{totals['raw']}**",
        f"- Nonempty `picked`: **{totals['valid']}**; empty selections: **{totals['empty']}**",
        f"- Unique `(family, run, agent, sim_day)` keys: **{totals['unique']}**",
        f"- Duplicate excess: **{totals['duplicate_excess']}**; unique deficit vs nominal {totals['nominal_agent_days']}: **{totals['unique_deficit_vs_nominal']}**",
        f"- Arithmetic check: {totals['raw']} − {totals['valid']} = {totals['empty']}; {totals['valid']} − {totals['duplicate_excess']} = {totals['unique']}; {totals['nominal_agent_days']} − {totals['unique']} = {totals['unique_deficit_vs_nominal']}",
        f"- Therefore 73,547 is a pipeline-valid row count, not a verified count of unique agent-days. The 1,547 row excess over 72,000 is not evidence of additional independent agent-days.",
        "",
        "| Family | Raw | Empty | Valid | Unique | Duplicate excess | Unique shortfall vs nominal | Runs below 900 unique |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for family in FAMILY_ORDER:
        item = summary["family_totals"][family]
        nominal = item["nominal_agent_days"]
        lines.append(f"| {family} | {item['raw']} | {item['empty']} | {item['valid']} | {item['unique']} | "
                     f"{item['duplicate_excess']} | {nominal - item['unique']} | {item['below_nominal_900']} |")
    lines += [
        "",
        "## Duplicate outcomes",
        "",
        f"- Repeated keys: **{totals['duplicate_groups']}**; same outcome keys: **{totals['same_outcome_keys']}**; different outcome keys: **{totals['different_outcome_keys']}**",
        f"- Same-outcome excess records: **{totals['same_outcome_excess']}**; different-outcome excess records: **{totals['different_outcome_excess']}**",
        f"- Outcome comparison fields: `{', '.join(summary['duplicate_outcome_fields'])}` (order preserved).",
        "",
        "De-identified file/line examples (numeric outcome only; no rationale text):",
        "",
    ]
    for example in summary["duplicate_examples"]:
        locations = "; ".join(f"{record['file']}:{record['line']}" for record in example["records"])
        lines.append(f"- agent={example['agent']}, sim_day={example['sim_day']}: **{example['comparison']}** — {locations}")
    lines += [
        "",
        "## Legacy exploratory contrasts (not deduplicated)",
        "",
        "Family means use unweighted run estimates. Intervals are percentile run-bootstrap 95% CIs, seed=42, 10,000 resamples.",
        "These values reproduce the legacy non-deduplicated pipeline and must not be represented as new frozen primary results.",
        "",
        "| Family | Judgment−parametric recall contrast [95% CI] | Δvalue [95% CI] |",
        "|---|---|---|",
    ]
    for family, item in summary["legacy_exploratory_analysis"]["families"].items():
        lines.append(f"| {family} | {item['recall_contrast_mean']:+.6f} [{item['recall_contrast_ci95'][0]:+.6f}, {item['recall_contrast_ci95'][1]:+.6f}] | "
                     f"{item['dvalue_mean']:+.6f} [{item['dvalue_ci95'][0]:+.6f}, {item['dvalue_ci95'][1]:+.6f}] |")
    lines += [
        "",
        "## Required next step (not performed here)",
        "",
        "The unique key is already defined. Pre-specify its duplicate-disposition/outcome-arbitration rule and treatment of the 86-key nominal deficit **before** looking at outcome-sensitive results, then rerun the complete analysis.",
        "This audit deliberately does not choose first/last records or infer the historical cause of any duplicate.",
        "",
        f"Script version: {summary['script_version']} · status: **{STATUS}** · disposition: **{DISPOSITION}**.",
        "",
    ]
    return "\n".join(lines)


def emit(summary: dict[str, Any], json_path: Path, md_path: Path, force: bool) -> None:
    for path in (json_path, md_path):
        if path.exists() and not force:
            raise FileExistsError(f"Refusing to overwrite {path}; use --force to replace it")
    json_path.write_text(json.dumps(summary, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    md_path.write_text(markdown(summary), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results-dir", type=Path, default=Path("sim/pilot/results"),
                        help="Directory containing immutable replay JSONL shards")
    parser.add_argument("--output-json", type=Path,
                        default=Path("sim/pilot/results/REPLAY_INTEGRITY_AUDIT.json"))
    parser.add_argument("--output-md", type=Path,
                        default=Path("sim/pilot/results/REPLAY_INTEGRITY_AUDIT.md"))
    parser.add_argument("--write", action="store_true",
                        help="Write dedicated JSON and Markdown artifacts; default is stdout only")
    parser.add_argument("--force", action="store_true",
                        help="Allow replacement of the two dedicated output artifacts, never replay inputs")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    runs, shards, skipped = load_runs(args.results_dir)
    summary = build_summary(runs, shards, skipped)
    report = markdown(summary)
    if args.write:
        emit(summary, args.output_json, args.output_md, args.force)
        print(f"Wrote {args.output_json}\nWrote {args.output_md}")
    else:
        print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
