#!/usr/bin/env python3
"""Read-only upstream-opportunity audit for the four-family academic replay.

All Channel-II digests are reconstructed from the frozen citation-correlated
proxy.  The script counts distinct critical proxy papers that reach the judgment
layer and hashes each run's complete 30-day digest to expose shared upstream
configurations.  No LLM is called and no source shard is modified.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
from typing import Any

try:
    from . import corpus as cp
    from .run_llm_replay import build_days
except ImportError:
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from sea_pilot import corpus as cp
    from sea_pilot.run_llm_replay import build_days

ROOT = Path(__file__).resolve().parents[2]
OUTDIR = ROOT / "sim" / "pilot" / "results" / "v19_upstream_digest_audit"
SEEDS = {"O": list(range(1, 31)), "C": list(range(201, 231)),
         "Q": list(range(101, 111)), "G": list(range(1, 11))}
STATUS = "POST_HOC_UPSTREAM_OPPORTUNITY_AUDIT__SEMI_ORACLE_WITHIN_CORPUS"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    os.environ["SEA_FORCE_LITE"] = "1"
    universe, critical, watchlists, _ = cp.build_all()
    critical = set(critical)
    rows = []
    digest_groups: dict[str, list[str]] = {}
    for family, seeds in SEEDS.items():
        for seed in seeds:
            run = seed - (200 if family == "C" else 100 if family == "Q" else 0)
            days = build_days(universe, critical, watchlists["inst"], proxy_seed=99 + seed)[:30]
            daily_ids = []
            reached = set()
            for dd in days:
                ids = [universe[i]["arxiv_id"] for i in dd["digest"]]
                daily_ids.append(ids)
                reached.update(universe[i]["arxiv_id"] for i in dd["critical"])
            digest_hash = hashlib.sha256(json.dumps(
                daily_ids, ensure_ascii=False, separators=(",", ":")).encode("utf-8")).hexdigest()
            run_id = f"{family}{run:02d}"
            digest_groups.setdefault(digest_hash, []).append(run_id)
            rows.append({
                "family": family, "run": run, "run_seed": seed, "proxy_seed": 99 + seed,
                "critical_targets_total": len(critical),
                "critical_targets_reaching_digest": len(reached),
                "upstream_opportunity_share": len(reached) / len(critical),
                "digest_positions": sum(len(x) for x in daily_ids),
                "digest_sha256": digest_hash,
            })
    families = {}
    for family in SEEDS:
        rr = [r for r in rows if r["family"] == family]
        counts = [r["critical_targets_reaching_digest"] for r in rr]
        families[family] = {
            "runs": len(rr), "min_targets": min(counts), "max_targets": max(counts),
            "mean_targets": sum(counts) / len(counts),
            "mean_upstream_opportunity_share": sum(r["upstream_opportunity_share"] for r in rr) / len(rr),
        }
    shared = [v for v in digest_groups.values() if len(v) > 1]
    summary = {
        "schema": "sea.v19.upstream-digest-audit/v1",
        "status": STATUS,
        "new_llm_calls": 0,
        "proxy_construction": "Channel-II candidate construction uses 0.4*z(log1p(2026 citation))+noise",
        "target_count": len(critical),
        "model_seed_configurations": len(rows),
        "distinct_complete_digest_configurations": len(digest_groups),
        "shared_digest_groups": shared,
        "input_provenance": {
            "corpus_lite_json_sha256": _sha256(ROOT / "sim/pilot/data/corpus_lite.json"),
            "run_llm_replay_py_sha256": _sha256(ROOT / "sim/sea_pilot/run_llm_replay.py"),
            "seed_mapping": "proxy_seed = 99 + run_seed",
            "forced_lite_input": True,
        },
        "families": families,
        "interpretation": (
            "Reported judgment recall is conditional on targets reaching the fixed digest. "
            "It is not whole-corpus end-to-end recall. Do not multiply or divide by the "
            "upstream share without freezing a new estimand and its joint denominator rules."),
    }
    return summary, rows


def render(s: dict[str, Any]) -> str:
    lines = [
        "# Upstream digest opportunity audit",
        "",
        f"**Status: `{STATUS}`.** No LLM calls.",
        "",
        "All reconstructed Channel-II digests depend on citation counts captured in "
        "2026. The experiment is therefore semi-oracle by construction, in addition "
        "to any unmeasured model-memory channel.",
        "",
        "| Family | Runs | Targets reaching digest (min–max) | Mean targets / 52 | Mean upstream share |",
        "|---|---:|---:|---:|---:|",
    ]
    for fam, x in s["families"].items():
        lines.append(f"| {fam} | {x['runs']} | {x['min_targets']}–{x['max_targets']} | "
                     f"{x['mean_targets']:.4f} | {100*x['mean_upstream_opportunity_share']:.2f}% |")
    lines += [
        "",
        f"There are {s['model_seed_configurations']} model–seed configurations but only "
        f"{s['distinct_complete_digest_configurations']} distinct complete digest configurations. "
        "O and G share seeds 1–10, hence ten identical upstream digest pairs.",
        "",
        "The recall endpoint in the main replay is conditional on these upstream "
        "opportunities. The upstream share is not a multiplicative correction factor "
        "for end-to-end recall without a separately frozen estimand.",
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
    targets = [OUTDIR / "summary.json", OUTDIR / "REPORT.md", OUTDIR / "run_upstream_coverage.csv"]
    if any(p.exists() for p in targets) and not args.force:
        raise SystemExit("Artifacts exist; use --force to replace them")
    (OUTDIR / "summary.json").write_text(text + "\n", encoding="utf-8")
    (OUTDIR / "REPORT.md").write_text(render(summary), encoding="utf-8")
    with (OUTDIR / "run_upstream_coverage.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(targets)} artifacts to {OUTDIR}")


if __name__ == "__main__":
    main()
