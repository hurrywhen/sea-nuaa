#!/usr/bin/env python3
"""Reproduce v1.13 synthetic SAP executor, matched fixture and target audit.

Default: print a compact summary. ``--write`` emits dedicated JSON artifacts under
``sim/pilot/results/sap_v1.13/``; replacement requires ``--force``. No LLM calls,
network access, or human data are created.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sea_sap import run_longitudinal_fixture, run_matched_implementation_demo
from sea_sap.target_construction import audit_target_construction

ROOT = Path(__file__).resolve().parents[2]
OUTDIR = ROOT / "sim" / "pilot" / "results" / "sap_v1.13"
ARTIFACTS = {
    "longitudinal.json": run_longitudinal_fixture,
    "matched_implementation_demo.json": run_matched_implementation_demo,
    "target_construction_audit.json": audit_target_construction,
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    results = {name: builder() for name, builder in ARTIFACTS.items()}
    if not args.write:
        print(json.dumps({
            "longitudinal_guard_trace": results["longitudinal.json"]["guard_trace"],
            "matched_status": results["matched_implementation_demo.json"]["status"],
            "target_status": results["target_construction_audit.json"]["status"],
        }, ensure_ascii=False, indent=2))
        return 0
    existing = [str(OUTDIR / name) for name in ARTIFACTS if (OUTDIR / name).exists()]
    if existing and not args.force:
        raise SystemExit(f"Refusing to overwrite without --force: {existing}")
    OUTDIR.mkdir(parents=True, exist_ok=True)
    for name, result in results.items():
        (OUTDIR / name).write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                                   encoding="utf-8")
    print(f"Wrote {len(results)} synthetic SAP artifacts to {OUTDIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
