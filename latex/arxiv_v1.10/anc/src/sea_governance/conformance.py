"""Run the offline governance conformance suite and emit deterministic JSON.

From ``sim``::

    PYTHONDONTWRITEBYTECODE=1 python3 -m sea_governance.conformance
    PYTHONDONTWRITEBYTECODE=1 python3 -m sea_governance.conformance --output /tmp/sea-s1-s4.json

The output intentionally has no wall-clock timestamp or host-specific paths.
"""
from __future__ import annotations

import argparse
import io
import json
from pathlib import Path
import sys
import unittest
from typing import Any, Optional, Sequence

from .reference import INTERFACE_VERSION, LIMITATIONS, SPECIFICATION


def _test_ids(suite: unittest.TestSuite) -> list[str]:
    result = []
    for test in suite:
        if isinstance(test, unittest.TestSuite):
            result.extend(_test_ids(test))
        else:
            result.append(test.id())
    return sorted(result)


def run_conformance() -> dict[str, Any]:
    """Execute the synthetic unit tests and return a machine-readable report."""
    from . import test_reference

    suite = unittest.defaultTestLoader.loadTestsFromModule(test_reference)
    test_ids = _test_ids(suite)
    detail = io.StringIO()
    result = unittest.TextTestRunner(stream=detail, verbosity=2).run(suite)
    failures = sorted(test.id() for test, _ in result.failures)
    errors = sorted(test.id() for test, _ in result.errors)
    skipped = sorted(test.id() for test, _ in result.skipped)
    passed = not failures and not errors
    return {
        "schema": "sea-governance-conformance/1",
        "specification": SPECIFICATION,
        "interface_version": INTERFACE_VERSION,
        "status": "PASS" if passed else "FAIL",
        "properties": ["S1", "S2", "S3", "S4", "negative-and-tamper"],
        "tests_run": result.testsRun,
        "failures": failures,
        "errors": errors,
        "skipped": skipped,
        "test_ids": test_ids,
        "limitations": list(LIMITATIONS),
    }


def report_json(report: dict[str, Any]) -> str:
    return json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n"


def write_report(report: dict[str, Any], path: str) -> None:
    """Write UTF-8 JSON without modifying repository source files."""
    Path(path).write_text(report_json(report), encoding="utf-8")


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", help="optional path for the same JSON written to stdout")
    args = parser.parse_args(argv)
    report = run_conformance()
    text = report_json(report)
    if args.output:
        write_report(report, args.output)
    sys.stdout.write(text)
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
