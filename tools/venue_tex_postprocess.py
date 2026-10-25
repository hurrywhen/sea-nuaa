#!/usr/bin/env python3
"""Post-process pandoc LaTeX for the generic venue-form builds.

The conference build uses a two-column class. Pandoc emits ``longtable`` for
Markdown pipe tables, but longtable does not work in two-column mode. The
conference papers intentionally contain only short tables, so convert each
longtable to a floating table* + tabular, preserving its caption, header, body
and booktabs rules. The journal build leaves longtable unchanged.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path


def _convert_short_table(spec: str, body: str) -> str:
    if "\\endhead" not in body or "\\endlastfoot" not in body:
        raise ValueError("Unrecognised pandoc longtable structure")

    caption = ""
    caption_match = re.search(
        r"\\caption\{(.*?)\}\\tabularnewline\s*", body, flags=re.S
    )
    if caption_match:
        caption = caption_match.group(1).strip()
        body = body[: caption_match.start()] + body[caption_match.end() :]

    if "\\endfirsthead" in body:
        first, remainder = body.split("\\endfirsthead", 1)
    else:
        first, remainder = body.split("\\endhead", 1)
    _, rows = remainder.split("\\endlastfoot", 1)
    first = first.strip()
    rows = rows.strip()
    if "\\bottomrule" not in rows:
        rows = rows + "\n\\bottomrule\\noalign{}"

    caption_tex = f"\\caption{{{caption}}}\n" if caption else ""
    return (
        "\\begin{table*}[t]\n"
        "\\centering\n"
        "\\footnotesize\n"
        "\\setlength{\\tabcolsep}{3pt}\n"
        f"{caption_tex}"
        "\\resizebox{\\textwidth}{!}{%\n"
        f"\\begin{{tabular}}{{{spec}}}\n"
        f"{first}\n"
        f"{rows}\n"
        "\\end{tabular}%\n"
        "}\n"
        "\\end{table*}"
    )


def convert_conference_tables(tex: str) -> tuple[str, int]:
    # Pandoc column specifications such as @{} >{\raggedright}p{...} @{} contain
    # nested braces. A small scanner is more reliable than a single regex.
    starts = list(re.finditer(r"\\begin\{longtable\}\[\]", tex))
    if not starts:
        return tex, 0

    out: list[str] = []
    cursor = 0
    for start in starts:
        spec_start = start.end()
        if spec_start >= len(tex) or tex[spec_start] != "{":
            raise ValueError("Missing longtable column specification")
        depth = 0
        spec_end = None
        for i in range(spec_start, len(tex)):
            if tex[i] == "{":
                depth += 1
            elif tex[i] == "}":
                depth -= 1
                if depth == 0:
                    spec_end = i + 1
                    break
        if spec_end is None:
            raise ValueError("Unclosed longtable column specification")
        end = tex.find("\\end{longtable}", spec_end)
        if end < 0:
            raise ValueError("Unclosed longtable environment")
        whole_end = end + len("\\end{longtable}")
        spec = tex[spec_start + 1 : spec_end - 1]
        body = tex[spec_end:end]
        replacement = _convert_short_table(spec, body)
        out.append(tex[cursor : start.start()])
        out.append(replacement)
        cursor = whole_end
    out.append(tex[cursor:])
    return "".join(out), len(starts)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("tex", type=Path)
    parser.add_argument("--mode", choices=["conference", "journal"], required=True)
    args = parser.parse_args()
    tex = args.tex.read_text(encoding="utf-8")
    if args.mode == "conference":
        tex, count = convert_conference_tables(tex)
        print(f"[venue-postprocess] converted {count} short tables to table*/tabular")
        # Generic conference style: 8 pt references are customary and keep the
        # six-page limit inclusive of bibliography without shrinking body text.
        ref = re.search(r"\\section\{(?:References|参考文献)\}\\label\{[^}]+\}", tex)
        if not ref:
            raise SystemExit("[venue-postprocess] References/参考文献 heading not found")
        tex = tex[: ref.end()] + "\n\\begingroup\\footnotesize" + tex[ref.end() :]
        tex = tex.replace("\\end{document}", "\\endgroup\n\\end{document}", 1)
        print("[venue-postprocess] references set to footnotesize")
        if "\\begin{longtable}" in tex:
            raise SystemExit("[venue-postprocess] longtable remains in two-column source")
    else:
        print("[venue-postprocess] journal source; longtable retained")
    args.tex.write_text(tex, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
