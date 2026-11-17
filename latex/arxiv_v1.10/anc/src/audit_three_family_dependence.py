#!/usr/bin/env python3
"""Dependence sensitivity for the separate three-family replay.

This is a post-hoc, within-corpus sensitivity analysis, not a new confirmatory
analysis. It preserves every input JSONL and never changes the frozen legacy
three-family outputs. The default is stdout only; dedicated artifacts require
--write, and replacement requires --force.

Run from the repository root:

    PYTHONDONTWRITEBYTECODE=1 python3 sim/sea_pilot/audit_three_family_dependence.py

The day-cluster bootstrap resamples all valid agent records within a simulated
day together. The circular moving-block bootstrap additionally retains runs of
five consecutive simulated days. These procedures address within-day/upstream
sharing and short-range serial dependence descriptively; they do not eliminate
shared-corpus, model-memory, label, or upstream-digest dependence.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Iterable

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SIM = ROOT / "sim"
if str(SIM) not in sys.path:
    sys.path.insert(0, str(SIM))

from sea_pilot.analyze_families import build_honest_arm  # noqa: E402

VERSION = "1.0.0"
STATUS = "POST_HOC_WITHIN_CORPUS_DEPENDENCE_SENSITIVITY"
FAMILIES = {
    "ornith30": ("llm_replay_ornith30.jsonl",),
    "gemma26na": ("llm_replay_gemma26na.jsonl",),
    "qwen38na": ("llm_replay_qwen38na.jsonl",),
    "qwen38b": ("llm_replay_qwen38b.jsonl",),
    "qwen38all": ("llm_replay_qwen38na.jsonl", "llm_replay_qwen38b.jsonl"),
}
BOOTSTRAP_B = 10000
BOOTSTRAP_SEED = 20261103
BLOCK_LENGTH = 5


def load_records(results_dir: Path, filenames: Iterable[str]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for filename in filenames:
        path = results_dir / filename
        with path.open(encoding="utf-8") as handle:
            for line_no, line in enumerate(handle, start=1):
                if not line.strip():
                    continue
                record = json.loads(line)
                record["_source_file"] = filename
                record["_source_line"] = line_no
                records.append(record)
    return records


def contrast(records: list[dict[str, Any]], honest_hits: dict[int, int], arm: str) -> float:
    """Match the legacy caliber for each comparison.

    The recall-level contrast against the parametric arm uses all recorded rows,
    including empty selections, exactly as analyze_family does for recall_llm and
    recall_param. The honest-feature comparison uses nonempty selections, matching
    its paired-day analysis and honest-on-valid-days denominator.
    """
    if arm == "honest":
        records = [record for record in records if record.get("picked")]
    critical = sum(int(record.get("n_crit", 0)) for record in records)
    if critical <= 0:
        return float("nan")
    llm = sum(int(record.get("hits_llm", 0)) for record in records)
    if arm == "parametric":
        other = sum(int(record.get("hits_param", 0)) for record in records)
    elif arm == "honest":
        other = sum(int(honest_hits.get(int(record.get("sim_day", -1)), 0))
                    for record in records)
    else:
        raise ValueError(arm)
    return (llm - other) / critical


def cluster_sample(days: list[int], rng: np.random.Generator) -> list[int]:
    return list(rng.choice(days, size=len(days), replace=True))


def moving_block_sample(days: list[int], rng: np.random.Generator,
                        block_length: int = BLOCK_LENGTH) -> list[int]:
    """Circular moving-block sample with the same number of day clusters."""
    ordered = sorted(days)
    n = len(ordered)
    if n == 0:
        return []
    starts = rng.integers(0, n, size=(n + block_length - 1) // block_length)
    sample: list[int] = []
    for start in starts:
        sample.extend(ordered[(int(start) + offset) % n] for offset in range(block_length))
    return sample[:n]


def expand_sample(by_day: dict[int, list[dict[str, Any]]], sample: list[int]) -> list[dict[str, Any]]:
    return [record for day in sample for record in by_day.get(day, [])]


def intervals(records: list[dict[str, Any]], honest_hits: dict[int, int]) -> dict[str, Any]:
    by_day: dict[int, list[dict[str, Any]]] = {}
    for record in records:
        by_day.setdefault(int(record["sim_day"]), []).append(record)
    days = sorted(by_day)
    output: dict[str, Any] = {
        "recorded_agent_days": len(records),
        "valid_agent_days": sum(bool(record.get("picked")) for record in records),
        "day_clusters": len(days),
        "agents": len({record.get("agent") for record in records}),
        "point_estimates": {},
        "bootstrap": {},
    }
    for arm in ("parametric", "honest"):
        output["point_estimates"][f"judgment_minus_{arm}"] = contrast(records, honest_hits, arm)
    for method in ("day_cluster", "moving_block_5"):
        rng = np.random.default_rng(BOOTSTRAP_SEED)
        values = {"parametric": [], "honest": []}
        for _ in range(BOOTSTRAP_B):
            if method == "day_cluster":
                sample = cluster_sample(days, rng)
            else:
                sample = moving_block_sample(days, rng)
            selected = expand_sample(by_day, sample)
            for arm in values:
                estimate = contrast(selected, honest_hits, arm)
                if np.isfinite(estimate):
                    values[arm].append(estimate)
        output["bootstrap"][method] = {}
        for arm, samples in values.items():
            array = np.asarray(samples, dtype=float)
            output["bootstrap"][method][f"judgment_minus_{arm}_ci95"] = (
                [float(x) for x in np.percentile(array, [2.5, 97.5])]
                if len(array) else [float("nan"), float("nan")]
            )
    return output


def build_summary(results_dir: Path) -> dict[str, Any]:
    honest_hits, _ = build_honest_arm()
    families = {}
    for tag, filenames in FAMILIES.items():
        records = load_records(results_dir, filenames)
        if records:
            families[tag] = intervals(records, honest_hits)
            families[tag]["source_files"] = list(filenames)
    return {
        "schema": "sea.three_family_dependence_sensitivity/v1",
        "script_version": VERSION,
        "status": STATUS,
        "read_only_inputs": True,
        "default_behavior": "stdout only; writes only with --write; no overwrite without --force",
        "interpretation": (
            "Post-hoc within-corpus sensitivity only. No confirmatory or cross-corpus claim. "
            "Day clustering preserves within-day/upstream sharing; circular length-five moving "
            "blocks additionally retain short-range serial structure. Neither removes shared "
            "corpus, labels, memory, or upstream-digest dependence."
        ),
        "comparison_calibers": {
            "parametric": "all recorded rows for recall-level hits and n_crit, matching legacy recall_llm/recall_param",
            "honest": "nonempty picked rows only, matching legacy paired-day honest comparison",
        },
        "honest_arm": "Rebuilt offline by sea_pilot.analyze_families.build_honest_arm; no LLM calls",
        "bootstrap": {
            "resamples_per_method_family_arm": BOOTSTRAP_B,
            "seed_per_method_family": BOOTSTRAP_SEED,
            "interval": "percentile 95%",
            "moving_block_length_days": BLOCK_LENGTH,
            "moving_block_boundary": "circular",
        },
        "families": families,
    }


def fmt_point(value: float) -> str:
    return f"{value:+.6f}"


def fmt_ci(interval: list[float]) -> str:
    return f"[{interval[0]:+.6f}, {interval[1]:+.6f}]"


def markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# Three-family replay — dependence sensitivity",
        "",
        f"> Status: **{STATUS}**. This is a post-hoc, within-corpus sensitivity analysis,",
        "> not a new confirmatory analysis and not evidence of transportability to other corpora or people.",
        "",
        "## Reproduce",
        "",
        "```bash",
        "PYTHONDONTWRITEBYTECODE=1 python3 sim/sea_pilot/audit_three_family_dependence.py",
        "",
        "# Write the two dedicated artifacts; existing files additionally require --force",
        "PYTHONDONTWRITEBYTECODE=1 python3 sim/sea_pilot/audit_three_family_dependence.py --write",
        "```",
        "",
        "The script makes no LLM calls and does not alter replay JSONL or the frozen legacy outputs.",
        f"Each reported interval uses {BOOTSTRAP_B:,} percentile-bootstrap resamples, seed={BOOTSTRAP_SEED}.",
        "The honest arm is rebuilt offline by the original deterministic feature pipeline.",
        "",
        "## Judgment minus semi-oracle parametric recall",
        "",
        "| Family | Point estimate | Day-cluster 95% CI | Circular moving-block (5 days) 95% CI |",
        "|---|---:|---:|---:|",
    ]
    for tag, item in summary["families"].items():
        lines.append(
            f"| {tag} | {fmt_point(item['point_estimates']['judgment_minus_parametric'])} | "
            f"{fmt_ci(item['bootstrap']['day_cluster']['judgment_minus_parametric_ci95'])} | "
            f"{fmt_ci(item['bootstrap']['moving_block_5']['judgment_minus_parametric_ci95'])} |"
        )
    lines += [
        "",
        "## Judgment minus honest-feature recall",
        "",
        "| Family | Point estimate | Day-cluster 95% CI | Circular moving-block (5 days) 95% CI |",
        "|---|---:|---:|---:|",
    ]
    for tag, item in summary["families"].items():
        lines.append(
            f"| {tag} | {fmt_point(item['point_estimates']['judgment_minus_honest'])} | "
            f"{fmt_ci(item['bootstrap']['day_cluster']['judgment_minus_honest_ci95'])} | "
            f"{fmt_ci(item['bootstrap']['moving_block_5']['judgment_minus_honest_ci95'])} |"
        )
    lines += [
        "",
        "## Scope",
        "",
        "- Day clusters keep every recorded agent row from the same simulated day together, preserving within-day and shared-digest dependence in each resample. The parametric recall contrast uses all recorded rows; the honest-feature paired contrast retains the legacy nonempty-`picked` caliber.",
        "- Circular length-five moving blocks additionally retain short-range serial dependence across simulated days.",
        "- These are sensitivity intervals, not independent-run intervals: each family has only 30 shared day clusters, and `qwen38all` pools two agent cohorts on those same days.",
        "- Shared corpus, post-hoc labels, upstream digest construction, potential model memory, and cross-family dependence remain outside the resampling model.",
        "- Legacy CMH/McNemar p-values must therefore be read as nominal within-corpus results under their stated stratification and dependence approximation, not as calibrated population error rates.",
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
    parser.add_argument("--results-dir", type=Path, default=ROOT / "sim" / "pilot" / "results")
    parser.add_argument("--output-json", type=Path,
                        default=ROOT / "sim" / "pilot" / "results" / "THREE_FAMILY_DEPENDENCE_SENSITIVITY.json")
    parser.add_argument("--output-md", type=Path,
                        default=ROOT / "sim" / "pilot" / "results" / "THREE_FAMILY_DEPENDENCE_SENSITIVITY.md")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    summary = build_summary(args.results_dir)
    report = markdown(summary)
    if args.write:
        emit(summary, args.output_json, args.output_md, args.force)
        print(f"Wrote {args.output_json}\nWrote {args.output_md}")
    else:
        print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
