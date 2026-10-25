#!/usr/bin/env python3
"""Generate docs/会议与期刊工件清单_v1.0.md after a clean venue audit."""
from __future__ import annotations

import argparse
from datetime import date
import hashlib
import re
import subprocess
from pathlib import Path

from audit_venue_papers import PAPERS, _math_inventory

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "docs/会议与期刊工件清单_v1.0.md"


def pdf_pages(path: Path) -> int:
    info = subprocess.run(["pdfinfo", str(path)], capture_output=True, text=True, check=True).stdout
    return int(re.search(r"(?m)^Pages:\s+(\d+)", info).group(1))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def reference_count(text: str) -> int:
    refs = re.split(r"(?m)^#{1,3}\s+(?:References|参考文献)\s*$", text, maxsplit=1)
    if len(refs) != 2:
        return 0
    bracket = re.findall(r"(?m)^\[(\d+)\]\s+", refs[1])
    plain = re.findall(r"(?m)^(\d+)\.\s+", refs[1])
    return max([int(x) for x in bracket + plain] or [0])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--suite", choices=["all", "conference", "journal"], default="all")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    out = args.output if args.output.is_absolute() else ROOT / args.output
    audit_cmd = ["python3", "tools/audit_venue_papers.py"]
    if args.suite != "all":
        audit_cmd += ["--suite", args.suite]
    audit = subprocess.run(audit_cmd, cwd=ROOT, capture_output=True, text=True)
    if audit.returncode:
        print(audit.stdout)
        print(audit.stderr)
        raise SystemExit("[manifest] venue audit failed; manifest not written")

    suite_label = {"all": "会议与期刊", "conference": "会议", "journal": "期刊"}[args.suite]
    lines = [
        f"# {suite_label}工件清单（v1.0）",
        "",
        f"> 生成日期：{date.today().isoformat()}。本清单由 `python3 tools/make_venue_manifest.py` 自动生成；",
        "> 生成前已强制通过所选稿件来源、冻结数值、引用闭合、PDF 文本层及中英公式/数字同步审计。",
        "> 任何重建都会改变 PDF 的时间戳和 SHA-256，须重新运行本命令并同步投稿信。",
        "",
        "| 版本 | 源稿 | PDF | 页数 | 文献 | 表 | 展示公式 | PDF 字节 | SHA-256 |",
        "|---|---|---|---:|---:|---:|---:|---:|---|",
    ]
    labels = {
        "conference-en": "会议 · 英文",
        "journal-en": "期刊 · 英文",
        "conference-zh": "会议 · 中文镜像",
        "journal-zh": "期刊 · 中文镜像",
    }
    for name, cfg in PAPERS.items():
        if args.suite != "all" and not name.startswith(args.suite):
            continue
        src, pdf = ROOT / cfg["src"], ROOT / cfg["pdf"]
        text = src.read_text(encoding="utf-8")
        tables = len(re.findall(r"(?m)^:\s+(?:Table|表)\s*\d+", text))
        displays, _ = _math_inventory(text)
        lines.append(
            f"| {labels[name]} | `{cfg['src']}` | `{cfg['pdf']}` | {pdf_pages(pdf)} | "
            f"{reference_count(text)} | {tables} | {len(displays)} | {pdf.stat().st_size} | `{sha256(pdf)}` |"
        )
    if args.suite == "all":
        rebuild_commands = [
            "bash tools/build_venue_pdfs.sh conference",
            "bash tools/build_venue_pdfs.sh journal",
            "bash tools/build_venue_pdfs.sh conference-zh",
            "bash tools/build_venue_pdfs.sh journal-zh",
            "python3 tools/audit_venue_papers.py",
            "python3 tools/make_venue_manifest.py",
        ]
    else:
        rebuild_commands = [
            f"bash tools/build_venue_pdfs.sh {args.suite}",
            f"bash tools/build_venue_pdfs.sh {args.suite}-zh",
            f"python3 tools/audit_venue_papers.py --suite {args.suite}",
            f"python3 tools/make_venue_manifest.py --suite {args.suite} --output {out.relative_to(ROOT)}",
        ]
    lines += [
        "",
        "## 页限与版式口径",
        "",
        "- 会议英文版：通用 `IEEEtran` 双栏，**6 页上限含参考文献**；当前为满足页限的正式通用工件。",
        "- 期刊英文版：通用 `article` 单栏 A4，目标约 30 页（构建器接受 28–32 页）。",
        "- 中文稿为内容同步镜像，中文排版页数不用于判断英文会/刊页限是否达标。",
        "- 每个 PDF 均有同名 `.tex` 生成文件。通用版式不是任何具体会/刊的官方模板。",
        "- 会议版署名顺序为 Xutong Wang、Wen Hu、Ya Yu；期刊版/专著版为 Wen Hu、Xutong Wang、Ya Yu。通讯作者仍为 Wen Hu。",
        "",
        "## 本清单生成时已通过的检查",
        "",
        "- 英文会议 ≤6 页、英文期刊 28–32 页；所有 PDF 无缺字形、无未解析 `??`；",
        "- 四个家族的 run 数、有效记录数、召回率/CI、价值增量、总记录数与 CMH 值逐项对照冻结 JSON；",
        "- 参考文献 1..N 连续，正文引用与文献表双向闭合；",
        "- 全部源稿标题在 PDF 文本层可见，关键数值未因排版丢失；",
        "- 中英显示公式与行内公式逐项一致、数字多重集一致（完整日期短语除外）、URL 一致、英文参考文献原文一致；",
        "- P1–P12 进行中、HP-0 已设计待采集、零人类被试数据及人类侧可证伪预测标签均保留。",
        "",
        "## 重建与再生成",
        "",
        "```bash",
        *rebuild_commands,
        "```",
        "",
        "投稿信与网页元数据见 `docs/投稿信_会议版_v1.0.md`、`docs/投稿信_期刊版_v1.0.md`、",
        "`docs/会议与期刊投稿材料_v1.0.md`（内部确认项，不随公开仓发布）。版本分工见",
        "`docs/会议与期刊版本说明_v1.0.md`。",
        "",
    ]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"[manifest] wrote {out.relative_to(ROOT)}")
    print(audit.stdout.strip().splitlines()[-1])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
