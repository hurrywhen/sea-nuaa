#!/usr/bin/env python3
"""Detect PDF text bounding boxes that approach/cross the physical page edge.

Unlike a text-layer existence check, this catches long verbatim commands clipped
at the right boundary. Requires Poppler's ``pdftotext``. The default safety band
is 20 PDF points; a finding is a layout failure even if glyphs remain extractable.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import subprocess
import tempfile
from pathlib import Path

PAGE_RE = re.compile(r'<page width="([\d.]+)" height="([\d.]+)">(.*?)</page>', re.S)
WORD_RE = re.compile(
    r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>',
    re.S,
)


def inspect(pdf: Path, band: float) -> dict:
    with tempfile.TemporaryDirectory(prefix="sea-pdf-layout-") as tmp:
        target = Path(tmp) / "bbox.html"
        subprocess.run(["pdftotext", "-bbox", str(pdf), str(target)], check=True)
        source = target.read_text(encoding="utf-8")
    findings = []
    pages = 0
    max_ratio = 0.0
    for pages, match in enumerate(PAGE_RE.finditer(source), start=1):
        width, height = float(match.group(1)), float(match.group(2))
        for word in WORD_RE.finditer(match.group(3)):
            xmin, ymin, xmax, ymax = map(float, word.groups()[:4])
            text = html.unescape(re.sub(r"<[^>]+>", "", word.group(5)))
            max_ratio = max(max_ratio, xmax / width, xmin / width)
            reasons = []
            if xmin < band:
                reasons.append("left-safety-band")
            if xmax > width - band:
                reasons.append("right-safety-band")
            if ymin < 0 or ymax > height:
                reasons.append("vertical-page-boundary")
            if reasons:
                findings.append({
                    "page": pages, "text": text, "xMin": xmin, "xMax": xmax,
                    "page_width": width, "reasons": reasons,
                })
    return {
        "schema": "sea.pdf-layout-check/v1", "pdf": str(pdf), "pages": pages,
        "safety_band_points": band, "status": "PASS" if not findings else "FAIL",
        "findings": findings, "max_word_xmax_to_page_width": max_ratio,
        "note": "Coordinate checks do not replace full-page visual inspection.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--band", type=float, default=20.0)
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()
    result = inspect(args.pdf, args.band)
    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.json:
        args.json.write_text(text, encoding="utf-8")
    if result["status"] == "PASS":
        print(f"PDF layout PASS: {result['pages']} pages; no word within {args.band:g} pt of left/right edge")
    else:
        print(f"PDF layout FAIL: {len(result['findings'])} finding(s)")
        for finding in result["findings"][:20]:
            print(f"  p{finding['page']}: xMax={finding['xMax']:.2f}/{finding['page_width']:.2f} {finding['text']!r}")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
