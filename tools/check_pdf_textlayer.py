"""最终 PDF 文本层完整性检查（三审意见③的落实）。用法：
    python3 tools/check_pdf_textlayer.py latex/SEA_EN_v1.5_draft.pdf input/sovereign_epistemic_acquisition_EN_v1.5.md
    python3 tools/check_pdf_textlayer.py latex/主权认知获取_统一理论_v1.5_内审稿.pdf input/主权认知获取_统一理论_v1.5.md
检查项：
  1) 无 "1 1 1" 类表格损坏伪影（审稿人上一轮在窄列表格抽取中看到的模式）；
  2) 全部表格标题（表 13-1/14-1/14-2/14-3/15-1、家族映射、B.6 等）在文本层可见；
  3) 关键字符串在文本层可见（样本量公式、家族代号行、H9 冻结值 0.285、ref130 Article 4）；
  4) 源稿全部 ## 级标题在文本层完整出现（去空白后子串匹配，捕捉标题断裂/词序错位）；
  5) 文本层字符量与源稿字符量之比处于合理区间（捕捉整段丢失）。
退出码 0 = 通过。
"""
from __future__ import annotations

import re
import subprocess
import sys
import os

CAPTIONS = [
    "Table 13-1", "Table 14-1", "Table 14-2", "Table 14-3", "Table 15-1",
    "Family-code mapping", "B.6",
    "表 13-1", "表 14-1", "表 14-2", "表 14-3", "表 15-1",
    "家族代号映射", "B.6 正态分位数",
]
KEYSTRINGS = [
    "2(1.96+0.84)", "2(1.96 + 0.84)", "ornith-1.5-35b", "ling-3.0-flash",
    "qwen3.8-27b", "gemma4:26b", "nemotron-3-super-120b",
    "0.285", "Article 4", "0.2848",
]


def norm(t: str) -> str:
    return re.sub(r"\s+", "", t)


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    pdf, src = sys.argv[1], sys.argv[2]
    if not os.path.exists(pdf):
        print(f"[fail] PDF 不存在：{pdf}")
        return 1
    txt = subprocess.run(["pdftotext", pdf, "-"], capture_output=True, text=True).stdout
    issues: list[str] = []

    # 1 corruption artifacts（仅同行内匹配；目录页码竖排不构成伪影）
    for m in re.finditer(r"(?<!\d)1[ \t]+1[ \t]+1(?!\d)", txt):
        line = txt[: m.start()].count("\n") + 1
        issues.append(f"[伪影] 文本层第 {line} 行附近出现 '1 1 1' 模式")
    # 2 captions
    ntxt = norm(txt)
    for c in CAPTIONS:
        if norm(c) not in ntxt:
            # 允许中英稿各自只含其语言的一半
            if c.startswith("Table") or c == "Family-code mapping":
                if "EN" in pdf or "SEA" in pdf:
                    issues.append(f"[标题] 文本层缺少：{c}")
            else:
                if "SEA" not in pdf and "EN" not in pdf:
                    issues.append(f"[标题] 文本层缺少：{c}")
    # 3 key strings
    for k in KEYSTRINGS:
        if norm(k) not in ntxt:
            issues.append(f"[关键串] 文本层缺少：{k}")
    # 4 headings
    md = open(src, encoding="utf-8").read()
    heads = [h.strip() for h in re.findall(r"^##\s+(.+)$", md, re.M)]
    miss = []
    for h in heads:
        h2 = re.sub(r"\*\*|`", "", h)
        if norm(h2) not in ntxt:
            miss.append(h2)
    for h in miss:
        issues.append(f"[标题断裂] 源稿标题未在文本层完整出现：{h}")
    # 5 volume ratio
    ratio = len(ntxt) / max(1, len(norm(md)))
    if not (0.55 <= ratio <= 1.15):
        issues.append(f"[体量] 文本层/源稿去空白字符比 {ratio:.2f} 超出 [0.55, 1.15]")

    pages = txt.count("\f") + (0 if txt.endswith("\f") else 1)
    print(f"PDF={pdf} 页数≈{pages} 文本层字符={len(ntxt)} 源稿字符={len(norm(md))} 比={ratio:.2f}")
    print(f"标题 {len(heads)} 个，断裂 {len(miss)}；问题 {len(issues)}")
    for i in issues[:30]:
        print("  -", i)
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
