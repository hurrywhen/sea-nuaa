#!/usr/bin/env bash
# 生成内审稿 PDF。用法：bash tools/build_review_pdf.sh [zh|en|zh-preprint]
#   zh（默认）：input/主权认知获取_统一理论_v1.7.md -> latex/主权认知获取_统一理论_v1.7_内审稿.pdf（xelatex，CJK）
#   en        ：input/sovereign_epistemic_acquisition_EN_v1.7.md -> latex/SEA_EN_v1.7_draft.pdf（lualatex，完整 Unicode 文本层）
#   zh-preprint：同 zh 源稿但不注入审稿工件身份戳 -> latex/主权认知获取_统一理论_v1.7_预印本.pdf（ChinaXiv 等公开预印本用）
# v1.4 起：源文件禁止任何 HTML 注释（含嵌套）；预处理仍剥离注释作为保险，并对残留告警。
# v1.6 起：工件身份戳（版本+构建日期）注入标题页首行之下并写入 PDF 元数据（pdftitle/pdfsubject），
#          以杜绝"评审读到陈旧工件"类混淆（四审意见2 的教训）；构建后必须跑 tools/check_pdf_textlayer.py。
# 依赖：pandoc（>=3）、xelatex、lualatex、Noto Serif CJK SC 与 DejaVu 字体。
set -euo pipefail
cd "$(dirname "$0")/.."
MODE="${1:-zh}"
BUILD_DATE="$(date +%F)"
PDFVER="v1.7"

if [ "$MODE" = "en" ]; then
  SRC="input/sovereign_epistemic_acquisition_EN_v1.7.md"
  OUT="latex/SEA_EN_v1.7_draft.pdf"
  ENGINE="lualatex"
  LANG=""
  CONTENTS="Contents"
  FIRSTPART='^# Part I'
  STAMP="*Review artifact: **v1.7** · built ${BUILD_DATE} · authoritative PDF — verify version and page count against the cover-letter manifest before reviewing (v1.7 body+appendices = see manifest; earlier v1.4/v1.5/v1.6 PDFs are superseded).*"
  PDFTITLE="Sovereign Epistemic Acquisition (SEA) v1.7 - built ${BUILD_DATE}"
else
  SRC="input/主权认知获取_统一理论_v1.7.md"
  OUT="latex/主权认知获取_统一理论_v1.7_内审稿.pdf"
  ENGINE="xelatex"
  LANG="zh-CN"
  CONTENTS="目录"
  FIRSTPART='^#\s+第一部分'
  STAMP="*审稿工件：**v1.7** · 构建于 ${BUILD_DATE} · 本 PDF 为权威审稿工件——评审前请对照投稿信清单核验版本与页数（v1.4/v1.5/v1.6 旧 PDF 已被取代）。*"
  PDFTITLE="主权认知获取（SEA）v1.7 - 构建于 ${BUILD_DATE}"
fi
if [ "$MODE" = "zh-preprint" ]; then
  # 预印本用中文 PDF：与内审稿同源但**不含审稿工件身份戳**（公开预印本不需要）
  SRC="input/主权认知获取_统一理论_v1.7.md"
  OUT="latex/主权认知获取_统一理论_v1.7_预印本.pdf"
  ENGINE="xelatex"
  LANG="zh-CN"
  CONTENTS="目录"
  FIRSTPART='^#\s+第一部分'
  STAMP=""
  PDFTITLE="主权认知获取（SEA）v1.7 预印本 - ${BUILD_DATE}"
fi

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

# 1) 预处理：剥离 HTML 注释；在标题行下注入工件身份戳；把手写目录区块替换为带页码的 \tableofcontents（前后分页）
python3 - "$SRC" "$TMP/clean.md" "$FIRSTPART" "$STAMP" <<'PY'
import re, sys
src, dst, firstpart, stamp = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
text = open(src, encoding="utf-8").read()
text = re.sub(r"<!--.*?-->", "", text, flags=re.S)          # 剥离全部 HTML 注释
lines = text.splitlines(keepends=True)
# 工件身份戳：注入到第一个 '# ' 标题行之后
out, stamped = [], False
for ln in lines:
    out.append(ln)
    if not stamped and ln.startswith("# ") and stamp.strip():
        out.append("\n" + stamp + "\n")
        stamped = True
lines = out
TOC = ["\n", "\\newpage\n", "\\tableofcontents\n", "\\newpage\n", "\n"]
out, i, n, done = [], 0, len(lines), False
while i < n:
    if not done and re.match(r"^##\s+(目录|Contents)\s*$", lines[i]):
        out.extend(TOC); done = True
        while i < n and not re.match(firstpart, lines[i]):
            i += 1
        continue
    out.append(lines[i]); i += 1
open(dst, "w", encoding="utf-8").writelines(out)
left = len(re.findall(r"<!--", open(dst, encoding="utf-8").read()))
if left:
    print(f"[warn] 剥离后仍残留 {left} 处 '<!--'（v1.4 起源文件应无注释，请检查嵌套注释）")
print(f"[preprocess] {len(lines)} -> {len(out)} 行, 目录替换={done}, 身份戳={stamped}")
PY

# 2) preamble：原稿为手工编号 -> 关闭 LaTeX 自动编号；目录深度 2
#    v1.5：宽表用 footnotesize longtable（etoolbox 钩子）；v1.6：PDF 元数据写入版本戳
cat > "$TMP/preamble.tex" <<TEX
\usepackage{tikz}
\usetikzlibrary{arrows.meta,positioning,shapes.geometric}
\usepackage{etoolbox}
\AtBeginEnvironment{longtable}{\footnotesize}
\setcounter{secnumdepth}{0}
\setcounter{tocdepth}{2}
\renewcommand{\contentsname}{$CONTENTS}
\sloppy
\setlength{\parskip}{2pt}
\AtBeginDocument{\hypersetup{pdftitle={$PDFTITLE},pdfsubject={Review artifact $PDFVER (built $BUILD_DATE)},pdfkeywords={SEA; SAP; epistemic sovereignty; $PDFVER}}}
TEX

# 3) pandoc -> xelatex
pandoc "$TMP/clean.md" -o "$OUT" \
  --pdf-engine="$ENGINE" \
  -H "$TMP/preamble.tex" \
  -V documentclass=article \
  -V classoption=11pt \
  -V mainfont="DejaVu Serif" \
  -V sansfont="DejaVu Sans" \
  -V monofont="DejaVu Sans Mono" \
  -V geometry:a4paper \
  -V geometry:margin=2.5cm \
  -V colorlinks=true \
  -V linkcolor=NavyBlue \
  -V urlcolor=NavyBlue \
  ${LANG:+-V lang="$LANG"} \
  ${LANG:+-V CJKmainfont="Noto Serif CJK SC"}

echo "[ok] 已生成 $OUT"
pdfinfo "$OUT" | grep -E 'Pages|Page size' || true
