#!/usr/bin/env bash
# Build the generic conference/journal submission forms from their EN masters or ZH mirrors.
# Usage: bash tools/build_venue_pdfs.sh [conference|journal|conference-zh|journal-zh|en|zh|all]
# The conference PDF is hard-limited to 6 pages including references; the journal target is 28–32 pages.
set -euo pipefail
cd "$(dirname "$0")/.."
MODE="${1:-en}"

run_build() {
  local kind="$1" lang="$2"
  local src out stem documentclass classoption geometry
  if [ "$kind" = "conference" ]; then
    documentclass="IEEEtran"       # generic double-column layout; not a claim of venue selection
    classoption="conference,10pt"
    geometry="letterpaper,margin=0.68in,columnsep=0.22in"
  else
    documentclass="article"
    classoption="11pt"
    geometry="a4paper,margin=2.5cm"
  fi
  if [ "$lang" = "zh" ]; then
    if [ "$kind" = "conference" ]; then
      src="input/主权认知获取_会议版_v1.0.md"
      stem="主权认知获取_会议版_v1.0"
    else
      src="input/主权认知获取_期刊版_v1.0.md"
      stem="主权认知获取_期刊版_v1.0"
    fi
  else
    if [ "$kind" = "conference" ]; then
      src="input/SEA_conference_EN_v1.0.md"
      stem="SEA_conference_v1.0"
    else
      src="input/SEA_journal_EN_v1.0.md"
      stem="SEA_journal_v1.0"
    fi
  fi
  out="latex/${stem}.pdf"
  [ -f "$src" ] || { echo "[fail] missing source: $src"; return 1; }

  local build="/tmp/opencode/sea_venue_${kind}_${lang}"
  rm -rf "$build"
  mkdir -p "$build" latex
  cp "$src" "$build/source.md"

  # Strip HTML comments as a defensive measure; venue masters should not contain them.
  python3 - "$build/source.md" "$build/clean.md" <<'PY'
import re, sys
text = open(sys.argv[1], encoding="utf-8").read()
text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
open(sys.argv[2], "w", encoding="utf-8").write(text)
PY

  local pdftitle="${stem} (generic ${kind} submission form)"
  cat > "$build/preamble.tex" <<TEX
\\usepackage{graphicx}
\\usepackage{tikz}
\\usetikzlibrary{arrows.meta,positioning,shapes.geometric}
\\usepackage{etoolbox}
\\usepackage{hyperref}
\\ifPDFTeX\\else
  \\setmainfont{DejaVuSerif.ttf}[BoldFont=DejaVuSerif-Bold.ttf,ItalicFont=DejaVuSerif-Italic.ttf,BoldItalicFont=DejaVuSerif-BoldItalic.ttf]
  \\setsansfont{DejaVuSans.ttf}[BoldFont=DejaVuSans-Bold.ttf,ItalicFont=DejaVuSans-Oblique.ttf,BoldItalicFont=DejaVuSans-BoldOblique.ttf]
  \\setmonofont{DejaVuSansMono.ttf}[BoldFont=DejaVuSansMono-Bold.ttf,ItalicFont=DejaVuSansMono-Oblique.ttf,BoldItalicFont=DejaVuSansMono-BoldOblique.ttf]
\\fi
\\setcounter{secnumdepth}{0}
\\setcounter{tocdepth}{1}
\\sloppy
\\setlength{\\emergencystretch}{2em}
\\hypersetup{colorlinks=true,linkcolor=NavyBlue,urlcolor=NavyBlue,citecolor=NavyBlue,pdftitle={$pdftitle},pdfsubject={Generic ${kind} submission form, v1.0},pdfkeywords={SEA; epistemic sovereignty; information acquisition; ${kind}}}
TEX
  if [ "$kind" = "conference" ]; then
    cat >> "$build/preamble.tex" <<'TEX'
\setlength{\parskip}{0pt}
\setlength{\parindent}{1em}
\setlength{\abovecaptionskip}{3pt}
\setlength{\belowcaptionskip}{2pt}
\AtBeginEnvironment{figure}{\footnotesize}
TEX
  else
    cat >> "$build/preamble.tex" <<'TEX'
\usepackage{caption}
\captionsetup{font=small,labelfont=bf,skip=4pt}
\AtBeginEnvironment{longtable}{\footnotesize}
\linespread{1.10}\selectfont
\setlength{\parskip}{3pt}
\setlength{\parindent}{0pt}
TEX
  fi

  local -a lang_opts=()
  if [ "$lang" = "zh" ]; then
    lang_opts=(-V lang=zh-CN -V CJKmainfont="Noto Serif CJK SC")
  fi
  pandoc "$build/clean.md" --from=markdown+smart+tex_math_single_backslash --to=latex --standalone --wrap=none \
    --output="$build/paper.tex" \
    -H "$build/preamble.tex" \
    -V documentclass="$documentclass" \
    -V classoption="$classoption" \
    -V geometry:"$geometry" \
    "${lang_opts[@]}"

  python3 tools/venue_tex_postprocess.py "$build/paper.tex" --mode "$kind"

  # Full DejaVu variant set for file-name lookup (portable across XeLaTeX installations).
  local font_dir="${SEA_DEJAVU_DIR:-$HOME/.local/share/sea_fonts/dejavu}"
  [ -d "$font_dir" ] || font_dir="/usr/share/fonts/truetype/dejavu"
  local f
  for f in DejaVuSerif.ttf DejaVuSerif-Bold.ttf DejaVuSerif-Italic.ttf DejaVuSerif-BoldItalic.ttf \
           DejaVuSans.ttf DejaVuSans-Bold.ttf DejaVuSans-Oblique.ttf DejaVuSans-BoldOblique.ttf \
           DejaVuSansMono.ttf DejaVuSansMono-Bold.ttf DejaVuSansMono-Oblique.ttf DejaVuSansMono-BoldOblique.ttf; do
    [ -f "$font_dir/$f" ] || { echo "[fail] missing font variant: $font_dir/$f"; return 1; }
    cp "$font_dir/$f" "$build/"
  done

  ( cd "$build" && xelatex -interaction=nonstopmode -halt-on-error paper.tex >tex1.log 2>&1 \
    && xelatex -interaction=nonstopmode -halt-on-error paper.tex >tex2.log 2>&1 ) || {
      echo "[fail] XeLaTeX failed for $kind/$lang; log tail:"
      tail -35 "$build"/tex2.log "$build"/tex1.log 2>/dev/null || true
      return 1
    }
  local missing
  missing=$(cat "$build"/tex*.log | grep -c "Missing character" || true)
  [ "$missing" -eq 0 ] || {
    echo "[fail] Missing character warnings ($missing) for $kind/$lang"
    grep "Missing character" "$build"/tex2.log | sort -u | head -12
    return 1
  }

  local overfull
  overfull=$(cat "$build"/tex*.log | grep -c "Overfull" || true)
  [ "$overfull" -eq 0 ] || {
    echo "[fail] Overfull warnings ($overfull) for $kind/$lang"
    grep "Overfull" "$build"/tex2.log | head -12
    return 1
  }

  cp "$build/paper.tex" "latex/${stem}.tex"
  cp "$build/paper.pdf" "$out"
  local pages
  pages=$(pdfinfo "$out" | awk '/^Pages:/{print $2}')
  if [ "$lang" = "en" ] && [ "$kind" = "conference" ] && [ "$pages" -gt 6 ]; then
    echo "[fail] conference PDF has $pages pages; hard limit is 6 including references"
    return 1
  fi
  if [ "$lang" = "en" ] && [ "$kind" = "journal" ] && { [ "$pages" -lt 28 ] || [ "$pages" -gt 32 ]; }; then
    echo "[fail] journal PDF has $pages pages; target is 28–32 pages"
    return 1
  fi
  echo "[ok] $out: $pages pages; missing glyphs 0; source latex/${stem}.tex"
}

case "$MODE" in
  conference) run_build conference en ;;
  journal) run_build journal en ;;
  conference-zh) run_build conference zh ;;
  journal-zh) run_build journal zh ;;
  en) run_build conference en; run_build journal en ;;
  zh) run_build conference zh; run_build journal zh ;;
  all) run_build conference en; run_build journal en; run_build conference zh; run_build journal zh ;;
  *) echo "Usage: bash tools/build_venue_pdfs.sh [conference|journal|conference-zh|journal-zh|en|zh|all]"; exit 2 ;;
esac
