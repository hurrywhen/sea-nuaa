#!/usr/bin/env bash
# 生成 arXiv 预印本源包（LuaLaTeX）。用法：bash tools/make_arxiv_source.sh
#   产物：latex/arxiv_v1.7/{main.tex,00README.XXX,anc/...} 与 latex/SEA_v1.7_arxiv_source.tar.gz
# 说明：
#   - 预处理与 tools/build_review_pdf.sh 同源（剥离 HTML 注释、手写目录块替换为 \tableofcontents），
#     但**不注入审稿工件身份戳**（预印本不需要）；
#   - 字体与内审构建一致（DejaVu Serif/Sans/Mono via fontspec）：arXiv TeX Live 含
#     dejavu/dejavu-otf 包（见 info.arxiv.org/help/texlive_package_list.html），
#     且正文文本模式含 Unicode 数学符号（≥ ≤ ≠ ⇒ ≈ ∈ ∪ γ δ ′ ⁴ …），Latin Modern 缺字形；
#     构建后自动 grep 日志中的 "Missing character" 告警，必须为 0；
#   - anc/ 目录为 arXiv 附件（补充材料 S2、HP-0 工具包 zip、四家族冻结分析记录）。
set -euo pipefail
cd "$(dirname "$0")/.."

SRC="input/sovereign_epistemic_acquisition_EN_v1.7.md"
OUTDIR="latex/arxiv_v1.7"
TARBALL="latex/SEA_v1.7_arxiv_source.tar.gz"
DATE_STR="23 October 2026"

rm -rf "$OUTDIR"
mkdir -p "$OUTDIR/anc"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

# 1) 预处理：剥离 HTML 注释；手写目录块 -> \tableofcontents（无身份戳）
python3 - "$SRC" "$TMP/clean.md" <<'PY'
import re, sys
src, dst = sys.argv[1], sys.argv[2]
text = open(src, encoding="utf-8").read()
text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
lines = text.splitlines(keepends=True)
TOC = ["\n", "\\newpage\n", "\\tableofcontents\n", "\\newpage\n", "\n"]
out, i, n, done = [], 0, len(lines), False
while i < n:
    if not done and re.match(r"^##\s+(Contents|目录)\s*$", lines[i]):
        out.extend(TOC); done = True
        while i < n and not re.match(r"^# Part I", lines[i]):
            i += 1
        continue
    out.append(lines[i]); i += 1
open(dst, "w", encoding="utf-8").writelines(out)
print(f"[preprocess] 目录替换={done}")
PY

# 2) preamble（与内审构建同源，去掉版本戳 hypersetup）
cat > "$TMP/preamble.tex" <<'TEX'
\usepackage{tikz}
\usetikzlibrary{arrows.meta,positioning,shapes.geometric}
\usepackage{etoolbox}
\AtBeginEnvironment{longtable}{\footnotesize}
\setcounter{secnumdepth}{0}
\setcounter{tocdepth}{2}
\renewcommand{\contentsname}{Contents}
\sloppy
\setlength{\parskip}{2pt}
TEX

# 3) pandoc -> main.tex（standalone 文档；默认字体，日期固定避免 \today）
pandoc "$TMP/clean.md" -o "$OUTDIR/main.tex" \
  --standalone \
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
  -V date="$DATE_STR"

# 4) 00README.XXX（arXiv 指令文件）
cat > "$OUTDIR/00README.XXX" <<'EOF'
main.tex toplevel
EOF

# 5) anc/ 附件：补充材料 S2（投稿版）、HP-0 工具包 zip、四家族冻结分析记录
cp docs/补充材料S2_一致性审计报告_v1.5.md "$OUTDIR/anc/supplement_S2_consistency_audit_v1.5.md"
cp sim/pilot/results/MAIN_VALIDATION_ANALYSIS.md "$OUTDIR/anc/main_validation_analysis_four_family.md"
( cd docs/human_pilot_v1.5 && zip -qr - . ) > "$OUTDIR/anc/hp0_kit_v1.5.zip"

# 6) 本地试编译（lualatex 两遍），检查 Missing character / 错误
BUILD="$TMP/build"
mkdir -p "$BUILD"
cp -r "$OUTDIR"/. "$BUILD"/
( cd "$BUILD" && lualatex -interaction=nonstopmode -halt-on-error main.tex >tex1.log 2>&1 \
  && lualatex -interaction=nonstopmode -halt-on-error main.tex >tex2.log 2>&1 ) || {
    echo "[fail] 试编译失败，日志尾部："; tail -25 "$BUILD"/tex2.log "$BUILD"/tex1.log 2>/dev/null; exit 1; }
PAGES=$(pdfinfo "$BUILD/main.pdf" | awk '/^Pages:/{print $2}')
MISS=$(cat "$BUILD"/tex*.log | grep -c "Missing character" || true)
if [ "$MISS" -ne 0 ]; then
  echo "[fail] Missing character 告警 $MISS 处（字体覆盖不足）："; grep "Missing character" "$BUILD"/tex2.log | sort -u | head -10; exit 1; fi
echo "[ok] 试编译通过：$PAGES 页；Missing character 告警 0 处"
cp "$BUILD/main.pdf" "$OUTDIR/_local_compile_check.pdf"

# 7) 打包（不含本地试编译 PDF）
rm -f "$OUTDIR/_local_compile_check.pdf"
tar -czf "$TARBALL" -C "$OUTDIR" .
echo "[ok] 源包：$TARBALL（$(du -h "$TARBALL" | cut -f1)）；目录：$OUTDIR"
echo "[note] arXiv 提交时处理器选择 LuaLaTeX； anc/ 为附件目录"
