#!/usr/bin/env bash
# 生成 arXiv 预印本源包（**XeLaTeX**——arXiv 受支持处理器中没有 lualatex）。
# 用法：bash tools/make_arxiv_source.sh
#   产物：latex/arxiv_v1.7/{main.tex,00README.XXX,anc/...} 与 latex/SEA_v1.7_arxiv_source.tar.gz
# 说明：
#   - 预处理与 tools/build_review_pdf.sh 同源（剥离 HTML 注释、手写目录块替换为 \tableofcontents），
#     但**不注入审稿工件身份戳**（预印本不需要）；
#   - 字体以**文件名**加载（DejaVuSerif.ttf 等 12 变体）：arXiv 的 fontconfig 几乎不注册字体，
#     字体名方式会失败；arXiv TeX Live 2025 字体清单已含这些文件，无需随包附字体；
#     正文文本模式含 Unicode 数学符号（≥ ≤ ≠ ⇒ ≈ ∈ ∪ γ δ ′ ⁴ …），Latin Modern 缺字形，故必须用 DejaVu；
#   - 00README.XXX 用旧式指令 `main.tex toplevelfile`（新 JSON 的 toplevel 键不适用于此文件）；
#   - 本地试编译用 **xelatex** 两遍并断言 Missing character = 0；
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

# 4) 字体改为 arXiv 兼容的文件名加载（fontconfig 在 arXiv 几乎不注册字体；
#    arXiv TeX Live 2025 字体清单已含全部 12 个 DejaVu 变体文件，故无需随包附字体）
python3 - "$OUTDIR/main.tex" <<'PY'
import sys
p = sys.argv[1]
t = open(p, encoding="utf-8").read()
repl = [
 (r"\setmainfont[]{DejaVu Serif}",
  r"\setmainfont{DejaVuSerif.ttf}[BoldFont=DejaVuSerif-Bold.ttf,ItalicFont=DejaVuSerif-Italic.ttf,BoldItalicFont=DejaVuSerif-BoldItalic.ttf]"),
 (r"\setsansfont[]{DejaVu Sans}",
  r"\setsansfont{DejaVuSans.ttf}[BoldFont=DejaVuSans-Bold.ttf,ItalicFont=DejaVuSans-Oblique.ttf,BoldItalicFont=DejaVuSans-BoldOblique.ttf]"),
 (r"\setmonofont[]{DejaVu Sans Mono}",
  r"\setmonofont{DejaVuSansMono.ttf}[BoldFont=DejaVuSansMono-Bold.ttf,ItalicFont=DejaVuSansMono-Oblique.ttf,BoldItalicFont=DejaVuSansMono-BoldOblique.ttf]"),
]
for a, b in repl:
    assert a in t, f"未找到字体声明: {a}"
    t = t.replace(a, b)
open(p, "w", encoding="utf-8").write(t)
print("[fonts] 3 处字体声明已改为文件名加载（arXiv 兼容）")
PY

# 5) 00README.XXX（旧式指令：顶层文件为 toplevelfile）
cat > "$OUTDIR/00README.XXX" <<'EOF'
main.tex toplevelfile
EOF

# 5) anc/ 附件：补充材料 S2（投稿版）、HP-0 工具包 zip、四家族冻结分析记录
cp docs/补充材料S2_一致性审计报告_v1.5.md "$OUTDIR/anc/supplement_S2_consistency_audit_v1.5.md"
cp sim/pilot/results/MAIN_VALIDATION_ANALYSIS.md "$OUTDIR/anc/main_validation_analysis_four_family.md"
( cd docs/human_pilot_v1.5 && zip -qr - . ) > "$OUTDIR/anc/hp0_kit_v1.5.zip"

# 6) 本地试编译（**xelatex** 两遍——arXiv 受支持处理器中没有 lualatex），
#    检查 Missing character / 错误。
#    本地字体源：优先 ~/.local/share/sea_fonts/dejavu（官方 2.37 完整包，含全部变体），
#    回退系统目录；arXiv 端由其 TeX Live 字体树提供同名文件，无需随包附字体。
FONT_DIR="${SEA_DEJAVU_DIR:-$HOME/.local/share/sea_fonts/dejavu}"
[ -d "$FONT_DIR" ] || FONT_DIR="/usr/share/fonts/truetype/dejavu"
for f in DejaVuSerif.ttf DejaVuSerif-Bold.ttf DejaVuSerif-Italic.ttf DejaVuSerif-BoldItalic.ttf \
         DejaVuSans.ttf DejaVuSans-Bold.ttf DejaVuSans-Oblique.ttf DejaVuSans-BoldOblique.ttf \
         DejaVuSansMono.ttf DejaVuSansMono-Bold.ttf DejaVuSansMono-Oblique.ttf DejaVuSansMono-BoldOblique.ttf; do
  [ -f "$FONT_DIR/$f" ] || { echo "[fail] 缺少字体变体 $FONT_DIR/$f（请准备完整 DejaVu 包）"; exit 1; }
done
BUILD="$TMP/build"
mkdir -p "$BUILD"
cp -r "$OUTDIR"/. "$BUILD"/
cp "$FONT_DIR"/DejaVuSerif.ttf "$FONT_DIR"/DejaVuSerif-Bold.ttf \
   "$FONT_DIR"/DejaVuSerif-Italic.ttf "$FONT_DIR"/DejaVuSerif-BoldItalic.ttf \
   "$FONT_DIR"/DejaVuSans.ttf "$FONT_DIR"/DejaVuSans-Bold.ttf \
   "$FONT_DIR"/DejaVuSans-Oblique.ttf "$FONT_DIR"/DejaVuSans-BoldOblique.ttf \
   "$FONT_DIR"/DejaVuSansMono.ttf "$FONT_DIR"/DejaVuSansMono-Bold.ttf \
   "$FONT_DIR"/DejaVuSansMono-Oblique.ttf "$FONT_DIR"/DejaVuSansMono-BoldOblique.ttf "$BUILD"/
( cd "$BUILD" && xelatex -interaction=nonstopmode -halt-on-error main.tex >tex1.log 2>&1 \
  && xelatex -interaction=nonstopmode -halt-on-error main.tex >tex2.log 2>&1 ) || {
    echo "[fail] 试编译失败，日志尾部："; tail -25 "$BUILD"/tex2.log "$BUILD"/tex1.log 2>/dev/null; exit 1; }
PAGES=$(pdfinfo "$BUILD/main.pdf" | awk '/^Pages:/{print $2}')
MISS=$(cat "$BUILD"/tex*.log | grep -c "Missing character" || true)
if [ "$MISS" -ne 0 ]; then
  echo "[fail] Missing character 告警 $MISS 处（字体覆盖不足）："; grep "Missing character" "$BUILD"/tex2.log | sort -u | head -10; exit 1; fi
echo "[ok] xelatex 试编译通过：$PAGES 页；Missing character 告警 0 处"

# 7) 打包（arXiv 规范路径：main.tex 与 00README.XXX 在根，anc/ 为附件目录）
tar -czf "$TARBALL" -C "$OUTDIR" main.tex 00README.XXX anc
echo "[ok] 源包：$TARBALL（$(du -h "$TARBALL" | cut -f1)）；目录：$OUTDIR"
echo "[note] arXiv 提交时处理器选择 **XeLaTeX**；anc/ 为附件目录"
