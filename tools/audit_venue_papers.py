#!/usr/bin/env python3
"""Consistency and PDF checks for the generic conference/journal SEA papers.

Usage: python3 tools/audit_venue_papers.py [--source-only]
The monograph audit remains tools/audit_paper.py; this checker is deliberately
scoped to the two venue-form v1.0 documents and their distinct page budgets.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPERS = {
    "conference-en": {
        "src": "input/SEA_conference_EN_v1.0.md",
        "pdf": "latex/SEA_conference_v1.0.pdf",
        "kind": "conference",
        "lang": "en",
    },
    "journal-en": {
        "src": "input/SEA_journal_EN_v1.0.md",
        "pdf": "latex/SEA_journal_v1.0.pdf",
        "kind": "journal",
        "lang": "en",
    },
    "conference-zh": {
        "src": "input/主权认知获取_会议版_v1.0.md",
        "pdf": "latex/主权认知获取_会议版_v1.0.pdf",
        "kind": "conference",
        "lang": "zh",
    },
    "journal-zh": {
        "src": "input/主权认知获取_期刊版_v1.0.md",
        "pdf": "latex/主权认知获取_期刊版_v1.0.pdf",
        "kind": "journal",
        "lang": "zh",
    },
}
REQUIRED_BOTH = [
    "73,547",
    "0.443",
    "0.534",
    "0.514",
    "0.519",
    "0.241",
    "0.28",
    "0.952",
    "0.910",
    "https://github.com/hurrywhen/sea-nuaa",
    "10.5281/zenodo.23620920",
]


def norm(text: str) -> str:
    return re.sub(r"\s+", "", text)


def norm_heading(text: str) -> str:
    # PDF line wrapping may turn "architectural" into "architec- tural";
    # ignore whitespace and dash characters when checking heading continuity.
    return re.sub(r"[\s\-–—]+", "", text)


def run(args: list[str]) -> str:
    return subprocess.run(args, cwd=ROOT, capture_output=True, text=True, check=True).stdout


def check_reference_closure(text: str, label: str, issues: list[str]) -> int:
    match = re.search(r"(?m)^#{1,3}\s+(?:References|参考文献)\s*$", text)
    if not match:
        issues.append(f"{label}: missing References/参考文献 heading")
        return 0
    tail = text[match.end() :]
    numbers = [int(x) for x in re.findall(r"(?m)^(\d+)\.\s+", tail)]
    if not numbers:
        numbers = [int(x) for x in re.findall(r"(?m)^\[(\d+)\]\s+", tail)]
    if not numbers:
        issues.append(f"{label}: no manually numbered references found")
        return 0
    expected = list(range(1, max(numbers) + 1))
    if numbers != expected:
        issues.append(
            f"{label}: reference sequence is not closed 1..{max(numbers)}; "
            f"found {numbers[:5]}...{numbers[-5:]}"
        )
    return max(numbers)


def check_frozen_record_values(text: str, cfg: dict[str, str], label: str, issues: list[str]) -> None:
    """Reconcile every printed four-family table cell against the frozen JSON."""
    record = json.loads((ROOT / "sim/pilot/results/main_validation_analysis.json").read_text())
    expected = {f"{record['n_valid_total']:,}"}
    for family, data in record["families"].items():
        expected.add(f"{data['recall_mean']:.3f}")
        for endpoint in data["recall_ci95"]:
            expected.add(f"{endpoint:.3f}")
        expected.add(f"{data['dvalue_mean']:+.3f}".replace("-", "−"))
        if cfg["kind"] == "conference":
            expected.add(str(data["n_runs"]))
            expected.add(f"{data['n_valid']:,}")
    if cfg["kind"] == "conference":
        expected.add(f"{sum(d['mcnemar_b'] for d in record['families'].values()):,}")
        expected.add(f"{sum(d['mcnemar_c'] for d in record['families'].values()):,}")
    for token in sorted(expected):
        if token not in text:
            issues.append(f"{label}: frozen-record value missing/transcribed differently: {token}")
    chi = record["pooled_cmh"][0]
    if f"{chi:.1f}" not in text:
        issues.append(f"{label}: pooled CMH chi-square missing: {chi:.1f}")


def check_citation_closure(text: str, ref_count: int, label: str, issues: list[str]) -> None:
    marker = re.search(r"(?m)^#{1,3}\s+(?:References|参考文献)\s*$", text)
    if not marker or not ref_count:
        return
    body = text[: marker.start()]
    cited: set[int] = set()
    for content in re.findall(r"\[([0-9][0-9,\s\-–]*)\]", body):
        for part in content.split(","):
            part = part.strip()
            interval = re.fullmatch(r"(\d+)\s*[\-–]\s*(\d+)", part)
            if interval:
                cited.update(range(int(interval.group(1)), int(interval.group(2)) + 1))
            elif part.isdigit():
                cited.add(int(part))
    cited.discard(0)  # mathematical interval [0,1], not a citation
    expected = set(range(1, ref_count + 1))
    uncited = sorted(expected - cited)
    undefined = sorted(cited - expected)
    if uncited:
        issues.append(f"{label}: listed but uncited references: {uncited}")
    if undefined:
        issues.append(f"{label}: citations without reference entries: {undefined}")


def check_source(name: str, cfg: dict[str, str], issues: list[str]) -> None:
    path = ROOT / cfg["src"]
    if not path.exists():
        issues.append(f"{name}: missing source {cfg['src']}")
        return
    text = path.read_text(encoding="utf-8")
    for token in REQUIRED_BOTH:
        if token not in text:
            issues.append(f"{name}: required frozen value/link missing: {token}")
    check_frozen_record_values(text, cfg, name, issues)
    for token in ["[TO FILL", "arXiv:[", "PENDING AUTHOR", "<!--"]:
        if token in text:
            issues.append(f"{name}: unresolved placeholder/comment: {token}")
    if cfg["lang"] == "en":
        if not re.search(r"no human(?:-subject| subject) (?:data|experiments|participants)", text, re.I):
            issues.append(f"{name}: explicit no-human-subject-data statement missing")
        if "P1–P12" in text and not re.search(r"P1–P12[^.]{0,100}in progress", text, re.I):
            issues.append(f"{name}: P1–P12 must retain in-progress status")
    else:
        if not re.search(r"(?:未|尚无|零|没有).{0,16}人类被试|人类被试.{0,16}(?:未|尚无|零|没有)", text):
            issues.append(f"{name}: explicit zero-human-data statement missing")
        if "P1–P12" in text and not re.search(r"P1–P12[^。]{0,100}(?:进行中|尚未完成)", text):
            issues.append(f"{name}: P1–P12 未保留进行中状态")
    if "HP-0" in text:
        # The explicit status need not be repeated at every later cross-reference;
        # require at least one clear designed/pending declaration in the manuscript.
        status = re.search(
            r"(?:HP-0.{0,350}(?:designed|pending|awaiting|设计|待|尚未))"
            r"|(?:(?:designed|pending|awaiting|设计|待|尚未).{0,120}HP-0)",
            text,
            re.I | re.S,
        )
        if not status:
            issues.append(f"{name}: HP-0 lacks an explicit designed/pending declaration")
    overclaims = [
        r"human (?:trial|experiment|study) (?:shows|showed|demonstrates|demonstrated|confirms|confirmed)",
        r"participants (?:showed|demonstrated|improved)",
        r"人类(?:实验|试验|研究)(?:表明|证明|证实)",
        r"被试(?:表现出|显示出|提升了)",
    ]
    for pattern in overclaims:
        if re.search(pattern, text, re.I):
            issues.append(f"{name}: possible human-evidence overclaim: /{pattern}/")
    if "erfc" in text and not re.search(r"erfc\}?[^\n]{0,80}(?:χ|chi|\\chi)", text):
        issues.append(f"{name}: erfc expression present without an explicit chi-square argument")
    ref_count = check_reference_closure(text, name, issues)
    check_citation_closure(text, ref_count, name, issues)
    words = len(re.findall(r"\b[\w'-]+\b", text)) if cfg["lang"] == "en" else len(text)
    print(f"{name}: source {cfg['src']}; words/chars={words}; references={ref_count}")


def check_pdf(name: str, cfg: dict[str, str], issues: list[str]) -> None:
    pdf = ROOT / cfg["pdf"]
    src = ROOT / cfg["src"]
    if not pdf.exists() or not src.exists():
        issues.append(f"{name}: missing PDF or source for text-layer check")
        return
    info = run(["pdfinfo", str(pdf)])
    pages = int(re.search(r"(?m)^Pages:\s+(\d+)", info).group(1))
    if cfg["lang"] == "en" and cfg["kind"] == "conference" and pages > 6:
        issues.append(f"{name}: conference PDF has {pages} pages (>6 including references)")
    if cfg["lang"] == "en" and cfg["kind"] == "journal" and not 28 <= pages <= 32:
        issues.append(f"{name}: journal PDF has {pages} pages (target 28–32)")
    # Raw stream order avoids two-column layout extraction interleaving a heading
    # with equations from the opposite column.
    text = run(["pdftotext", "-raw", str(pdf), "-"])
    source = src.read_text(encoding="utf-8")
    ntext, nsource = norm(text), norm(source)
    ratio = len(ntext) / max(1, len(nsource))
    if not 0.45 <= ratio <= 1.35:
        issues.append(f"{name}: suspicious PDF/source normalized text ratio {ratio:.2f}")
    if "??" in text:
        issues.append(f"{name}: unresolved ?? marker in PDF")
    headings = re.findall(r"(?m)^#{1,3}\s+(.+)$", source)
    for heading in headings:
        cleaned = re.sub(r"[*`]", "", heading).strip()
        if norm_heading(cleaned) not in norm_heading(text):
            issues.append(f"{name}: heading missing/broken in PDF: {cleaned}")
    for token in REQUIRED_BOTH[:9]:
        if norm(token) not in ntext:
            issues.append(f"{name}: frozen value absent from PDF text: {token}")
    check_frozen_record_values(text, cfg, f"{name}-pdf", issues)
    print(f"{name}: PDF {cfg['pdf']}; pages={pages}; text/source ratio={ratio:.2f}; headings={len(headings)}")


def _math_inventory(text: str) -> tuple[list[str], list[str]]:
    displays = re.findall(r"\$\$(.*?)\$\$|\\\[(.*?)\\\]", text, re.S)
    display_list = [a or b for a, b in displays]
    stripped = re.sub(r"\$\$(.*?)\$\$|\\\[(.*?)\\\]", "", text, flags=re.S)
    inline = re.findall(r"(?<!\\)\$(?!\$)(.*?)(?<!\\)\$(?!\$)|\\\((.*?)\\\)", stripped, re.S)
    inline_list = [a or b for a, b in inline]
    return display_list, inline_list


def check_mirror_pair(en_path: str, zh_path: str, label: str, issues: list[str]) -> None:
    en_file, zh_file = ROOT / en_path, ROOT / zh_path
    if not en_file.exists() or not zh_file.exists():
        issues.append(f"{label}: EN/ZH mirror source missing")
        return
    en, zh = en_file.read_text(), zh_file.read_text()
    en_math, zh_math = _math_inventory(en), _math_inventory(zh)
    if en_math != zh_math:
        issues.append(
            f"{label}: formula inventory differs "
            f"(EN displays/inlines {len(en_math[0])}/{len(en_math[1])}, "
            f"ZH {len(zh_math[0])}/{len(zh_math[1])})"
        )
    number_pattern = r"\d+(?:,\d{3})*(?:\.\d+)?"
    # Month names are commonly converted between English and 中文数字日期;
    # exclude complete date phrases from the otherwise strict numeric comparison.
    months = r"(?:January|February|March|April|May|June|July|August|September|October|November|December)"
    def strip_dates(s: str) -> str:
        s = re.sub(rf"\b{months}\s+\d{{4}}\b", "", s)
        return re.sub(r"\d{4}\s*年\s*\d{1,2}\s*月", "", s)
    en_numbers = Counter(re.findall(number_pattern, strip_dates(en)))
    zh_numbers = Counter(re.findall(number_pattern, strip_dates(zh)))
    if en_numbers != zh_numbers:
        delta = (en_numbers - zh_numbers) + (zh_numbers - en_numbers)
        issues.append(f"{label}: numeric multiset differs: {dict(delta)}")
    en_refs = re.split(r"(?m)^#{1,3}\s+References\s*$", en, maxsplit=1)
    zh_refs = re.split(r"(?m)^#{1,3}\s+参考文献\s*$", zh, maxsplit=1)
    if len(en_refs) != 2 or len(zh_refs) != 2 or en_refs[1].strip() != zh_refs[1].strip():
        issues.append(f"{label}: English reference entries are not preserved verbatim")
    en_urls = sorted(re.findall(r"https?://[^\s*]+", en))
    zh_urls = sorted(re.findall(r"https?://[^\s*]+", zh))
    if en_urls != zh_urls:
        issues.append(f"{label}: URL inventory differs")
    refs_verbatim = (
        len(en_refs) == 2 and len(zh_refs) == 2 and en_refs[1].strip() == zh_refs[1].strip()
    )
    print(
        f"{label}: mirror formulas {len(en_math[0])}+{len(en_math[1])}; "
        f"numeric kinds {len(en_numbers)}; references verbatim={refs_verbatim}"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-only", action="store_true")
    parser.add_argument("--only", choices=sorted(PAPERS), help="check one paper while iterating")
    parser.add_argument("--suite", choices=["all", "conference", "journal"], default="all",
                        help="check one language pair plus its EN/ZH mirror (default: all)")
    args = parser.parse_args()
    issues: list[str] = []
    for name, cfg in PAPERS.items():
        if args.only and name != args.only:
            continue
        if args.suite != "all" and not name.startswith(args.suite):
            continue
        check_source(name, cfg, issues)
        if not args.source_only:
            check_pdf(name, cfg, issues)
    if not args.only and args.suite in {"all", "conference"}:
        check_mirror_pair(PAPERS["conference-en"]["src"], PAPERS["conference-zh"]["src"], "conference-mirror", issues)
    if not args.only and args.suite in {"all", "journal"}:
        check_mirror_pair(PAPERS["journal-en"]["src"], PAPERS["journal-zh"]["src"], "journal-mirror", issues)
    print(f"venue audit: {len(issues)} issue(s)")
    for issue in issues:
        print("  -", issue)
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
