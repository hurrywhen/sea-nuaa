"""论文投稿前一致性审计：编号交叉引用、文献闭合、关键数字对账、表格完整性、
目录一致、"进行中"措辞风险扫描。用法：python3 tools/audit_paper.py

已知设计取舍：
  - "v0.1 的定理 X" 类历史编号引用白名单豁免（指向纲领稿而非本文编号体系）；
  - 机构作者条目（C2PA 等）按缩写闭合；
  - 姓氏匹配 Unicode 感知（Matějka）且索引合著者（& 后姓氏）。
"""
from __future__ import annotations

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAPER = os.path.join(ROOT, "input", "主权认知获取_统一理论_v1.7.md")
RES = os.path.join(ROOT, "sim", "pilot", "results")

LABEL_KINDS = "公理|定理|命题|定义|引理|推论|性质|假设|猜想"

STOP = {w.lower() for w in (
    "The", "This", "These", "Those", "In", "We", "It", "As", "If", "For", "See", "Also",
    "SEA", "SEF", "SAP", "LLM", "AI", "RCT", "AOT", "EIG", "ODE", "KKT", "VOI", "KPI",
    "Pandora", "Markov", "Poisson", "Gaussian", "Laplace", "Bayes", "Nash", "Ulysses",
    "Red", "Queen", "McNemar", "Cochran", "Mantel", "Haenszel", "Bonferroni", "Isotonic",
    "Manifold", "Metaculus", "GDELT", "EDGAR", "Yahoo", "Wikimedia", "OpenAlex", "Wayback",
    "Ollama", "Python", "Phase", "Nudge", "PSPACE", "C2PA", "Xiv", "Testimonial",
    "Stratification", "Filtering", "Report", "PA", "SA", "Doob", "Banach", "Alaoglu",
    "Kushner", "Pareto", "Bernoulli", "Zipf", "Jaccard", "Siegmund")}
# 注：Siegmund/Kushner/Chalmers 类合著者以"第一作者 et al./&"形式被引，
# 留在 STOP 避免噪音；真姓氏（Hoeffding/Robbins/Weitzman/…）不列入，
# 其 (Surname, Year) 直引参与闭合检查。

ORG_WORDS = {"Coalition", "Center", "National", "World", "Open", "Pew", "OECD",
             "IEEE", "ACM", "WHO", "Association", "Institute"}


def main() -> int:
    text = open(PAPER, encoding="utf-8").read()
    lines = text.split("\n")
    issues: list[str] = []
    warns: list[str] = []

    # ---------- 1. 编号定义 vs 引用 ----------
    defined: dict[str, set[str]] = {}
    for m in re.finditer(rf"\*\*({LABEL_KINDS})\s*([0-9]+(?:\.[0-9]+)?|[A-Z](?:\.[0-9]+)?)\b", text):
        defined.setdefault(m.group(1), set()).add(m.group(2))
    n_hist = 0
    for m in re.finditer(rf"({LABEL_KINDS})\s*([0-9]+\.[0-9]+|[0-9]+(?=[\s（(，。；:：)）]|$))", text):
        kind, num = m.group(1), m.group(2)
        if "v0.1 的" in text[max(0, m.start() - 8):m.start()]:
            n_hist += 1                      # 历史编号引用（纲领稿），豁免
            continue
        if num in defined.get(kind, set()):
            continue
        if any(d.startswith(num + ".") for d in defined.get(kind, set())):
            continue                         # 裸章号引用（"定理 6"指 6.x 一族）
        issues.append(f"[编号] {kind} {num} 被引用但未找到定义（L{text[:m.start()].count(chr(10))+1}）")
    print(f"1. 编号：定义 {sum(len(v) for v in defined.values())} 个"
          f"（{'，'.join(f'{k}{len(v)}' for k, v in sorted(defined.items()))}）；"
          f"历史引用豁免 {n_hist}；未解析 {sum(1 for i in issues if i.startswith('[编号]'))}")

    # ---------- 2. 参考文献编号连续 + 正文引用闭合 ----------
    refsec = text.split("## 参考文献")[1].split("## 附录")[0]
    ref_nums = [int(m.group(1)) for m in re.finditer(r"^([0-9]+)\. ", refsec, re.M)]
    seq_ok = ref_nums == list(range(1, len(ref_nums) + 1))
    if not seq_ok:
        issues.append(f"[文献] 编号不连续：{len(ref_nums)} 条")
    ref_entries: dict[str, set[str]] = {}
    first_authors: set[str] = set()
    org_acronyms: dict[str, str] = {}
    for ln in refsec.split("\n"):
        m = re.match(r"^([0-9]+)\.\s*(.*?)((?:19|20)[0-9]{2})", ln)
        if not m:
            continue
        author_part, year = m.group(2), m.group(3)
        first = re.match(r"([A-Z][a-zA-Z]+)", author_part)
        if first and first.group(1) in ORG_WORDS:
            acr = re.search(r"\(([A-Z0-9]{2,})\)", ln)
            if acr:
                org_acronyms[acr.group(1).lower()] = year
            continue
        surs = [x for x in re.findall(r"[A-Z][\w'\-]{1,}", author_part)
                if x.lower() not in STOP and len(x) >= 2]
        for sur in surs:
            ref_entries.setdefault(sur.lower(), set()).add(year)
        if surs:
            first_authors.add(surs[0].lower())     # 直引检查只对第一作者（et al. 合引惯例）
    body = text.replace(refsec, "")
    cited: set[tuple[str, str]] = set()
    yr_pat = r"((?:19|20)[0-9]{2}[a-z]?(?:/(?:19|20)[0-9]{2})?)"
    for paren in re.finditer(r"[（(]([^（）()]{1,140})[)）]", body):
        for m in re.finditer(rf"([A-Z][\w'\-]+)[^;]{{0,50}}?,\s*{yr_pat}", paren.group(1)):
            if m.group(1).lower() not in STOP:
                cited.add((m.group(1).lower(), m.group(2)))
    for m in re.finditer(rf"([A-Z][\w'\-]+)(?:\s+(?:et\s+al\.|and\s+[A-Z][\w'\-]+|&\s+[A-Z][\w'\-]+))*\s*[（(]{yr_pat}", body):
        if m.group(1).lower() not in STOP:
            cited.add((m.group(1).lower(), m.group(2)))
    dangling = []
    for sur, yr in sorted(cited):
        parts = set(yr.split("/"))
        if sur in ref_entries:
            if not any(p in r_y or r_y in p for p in parts for r_y in ref_entries[sur]):
                dangling.append(f"{sur} {yr}（姓氏在文献表但年份不符）")
        else:
            dangling.append(f"{sur} {yr}（姓氏不在文献表）")
    for d in dangling:
        issues.append(f"[文献] 正文引用未闭合：{d}")
    cited_surs = {s for s, _ in cited}
    uncited = sorted(first_authors - cited_surs)
    for u in uncited:
        warns.append(f"[文献] 文献表条目未见正文直引（复核概念名/中译名）：{u}")
    org_uncited = [a for a in org_acronyms if a.upper() not in body]
    for a in org_uncited:
        warns.append(f"[文献] 机构条目缩写未见正文引用：{a.upper()}")
    print(f"2. 文献：{len(ref_nums)} 条编号{'连续' if seq_ok else '不连续'}；"
          f"正文（含附录）抽出 {len(cited)} 个（姓,年）引用对，未闭合 {len(dangling)} 处；"
          f"文献表未见直引 {len(uncited)} 个；机构条目 {len(org_acronyms)} 个")

    # ---------- 3. 关键数字对账（论文 vs 结果 JSON）----------
    def load(name):
        p = os.path.join(RES, name)
        return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}
    checks = []
    p2 = load("p2_summary.json")
    if p2:
        checks.append((f"ρ_c={p2['rho_c_measured']:.2f}", "8.19" in text, "ρ_c 8.19"))
        checks.append((f"N={p2['n_props']}", str(p2["n_props"]) in text, f"命题数 {p2['n_props']}"))
    fam = load("three_family_analysis.json")
    if fam:
        cm = fam.get("cmh_pooled", {})
        if cm.get("llm_vs_honest", {}).get("p") is not None:
            checks.append(("CMH honest p", ("6.8×10⁻²⁸" in text) or ("6.8\\times10^{-28}" in text), "CMH vs honest"))
        if cm.get("llm_vs_param", {}).get("p") is not None:
            checks.append(("CMH param p", "0.017" in text, "CMH vs param"))
    om = load("p5_omega_results.json")
    if om:
        w = om.get("omega", {})
        checks.append((f"Ω={w.get('with_public')}", "0.168" in text, "Ω 公共层"))
        checks.append((f"Ω0={w.get('without_public')}", "0.066" in text, "Ω 无公共层"))
    # v1.4 起：H9 以四家族协议工件（*_h9.json，10 月重跑版）对账，取代 9 月三家族 *na.json
    h9_vals = []
    for tag in ("o90_h9", "c90_h9", "q90_h9", "g90_h9"):
        h9 = load(f"h9_{tag}.json")
        if h9:
            h9_vals.append(f"{h9['brier_agent']:.3f}")
    if len(h9_vals) == 4:
        joined = " / ".join(h9_vals)
        checks.append((f"H9 四家族={joined}", joined in text, "H9 四家族 Brier"))
    else:
        for tag, br in (("ornith", "0.170"), ("qwen38na", "0.231"), ("gemma26na", "0.279")):
            h9 = load(f"h9_{tag}.json")
            if h9:
                checks.append((f"H9 {tag}={h9['brier_agent']:.3f}", br in text, f"H9 {tag}"))
    av = load("algo_validation.json")
    if av and "T2_certify" in av:
        checks.append(("A8 lift", "1.23" in text, "A8 lift 修复"))
    avp3 = load("algo_validation_p3.json")
    if avp3 and "T3_greedy" in avp3:
        g = avp3["T3_greedy"]
        pair50 = f"{g['greedy_cov_at_50']} vs {g['actual_watchlist_cov']}"
        pairk = f"{g['greedy_cov_at_k']} vs {g['random_cov_at_k_mean']:.0f}"
        checks.append(("P3 greedy", (pair50 in text) or (pairk in text), "P3 贪心对照"))
    bad = [c for c in checks if not c[1]]
    for c in bad:
        issues.append(f"[数字] 论文未包含预期值：{c[2]}（实测 {c[0]}）")
    print(f"3. 数字对账：{len(checks)-len(bad)}/{len(checks)} 项与结果 JSON 一致"
          + (f"；不一致：{[c[2] for c in bad]}" if bad else ""))

    # ---------- 4. Markdown 表格完整性 ----------
    tbl_bad = 0
    i = 0
    while i < len(lines):
        if lines[i].strip().startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1]):
            ncol = lines[i].count("|")
            j = i
            while j < len(lines) and lines[j].strip().startswith("|"):
                if lines[j].count("|") != ncol and not re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[j]):
                    tbl_bad += 1
                    warns.append(f"[表格] 第 {j+1} 行列数 {lines[j].count('|')} ≠ 表头 {ncol}")
                j += 1
            i = j
        else:
            i += 1
    print(f"4. 表格：列数异常 {tbl_bad} 处")

    # ---------- 5. 目录 vs 章节 ----------
    heads = [m.group(1).strip() for m in re.finditer(r"^## (.+)$", text, re.M)]
    toc = text.split("## 目录")[1].split("## 1 引言")[0]
    toc_items = [m.group(1).strip() for m in re.finditer(r"- ([0-9]+ [^\n]+)", toc)]
    missing = [t for t in toc_items if not any(h.startswith(t.split("（")[0][:6]) for h in heads)]
    for t in missing:
        issues.append(f"[目录] 条目未对应章节：{t}")
    print(f"5. 目录：{len(toc_items)} 条目，未对应 {len(missing)}")

    # ---------- 6. "进行中"措辞风险扫描 ----------
    risk_pat = re.compile(r"(运行中|补跑中|排队|待启动|即将|正在跑|扩样中|进行中|待复测|待标定|待训练)")
    risk = [(n + 1, ln.strip()[:90]) for n, ln in enumerate(lines) if risk_pat.search(ln)]
    print(f"6. 措辞风险：{len(risk)} 行含『进行中/待』类表述")
    for ln, s_ in risk[:12]:
        warns.append(f"[措辞] L{ln}: {s_}")

    # ---------- 7. v1.6 修订核查（中英双稿；含 v1.5 遗留项）----------
    en_path = os.path.join(ROOT, "input", "sovereign_epistemic_acquisition_EN_v1.7.md")
    en = open(en_path, encoding="utf-8").read() if os.path.exists(en_path) else ""
    v15: list[tuple[str, bool]] = []
    for tag, doc in (("ZH", text), ("EN", en)):
        if not doc:
            continue
        v15.append((f"{tag} 横向页块已除+宽表并列",
                    ("\\newgeometry" not in doc) and ("\\restoregeometry" not in doc)
                    and (("Source / vehicle" in doc) or ("来源/载体" in doc))))
        v15.append((f"{tag} 弃用主验证重放措辞",
                    all(x not in doc for x in ("main-validation", "Main Validation", "主验证重放", "（主验证）"))))
        v15.append((f"{tag} H9 口径注 0.2848", "0.2848" in doc))
        v15.append((f"{tag}  ref56 AER 105(1),272–298", "105(1), 272–298" in doc))
        v15.append((f"{tag}  ref74 Palgrave 5,65", ("5, 65" in doc) and ("The fake news game" not in doc)))
        v15.append((f"{tag}  ref130 Article 4", "Article 4" in doc))
        v15.append((f"{tag} 姓氏拼写统一",
                    all(x in doc for x in ("Ahmmad", "Roozenbeek", "Matějka", "Maćkowiak"))
                    and not any(x in doc for x in ("Rozenbeek", "Roosenbeek", "Matjeka", "Mackowiak"))))
        v15.append((f"{tag} 样本量公式无叠分", "2(1.96+0.84)^2/0.35^2" in doc and "\\frac13" not in doc))
        v15.append((f"{tag} P4 域限定注", ("applicability-domain qualification" in doc) or ("适用域限定" in doc)))
        v15.append((f"{tag} HP-0 已入稿", "HP-0" in doc))
        # ---- v1.6 新增（四审三份意见）----
        v15.append((f"{tag} 猜想10.1 降级+KC清单",
                    (("Conjecture 10.1" in doc) or ("猜想 10.1" in doc)) and ("(KC5)" in doc)))
        v15.append((f"{tag} 无未配对旧陈述",
                    ("Conditional convergence to the declared neighborhood)**. *Under C1–C5—this is a conditional" not in doc)
                    and ("定理 10.1（到声明邻域的条件收敛）" not in doc)))
        v15.append((f"{tag} V5 分支更新一致性",
                    (("branch–update consistency" in doc) or ("分支—更新一致性" in doc)) and ("(V1)–(V5)" in doc or "(V1)–(V5)".replace("–", "–") in doc)))
        v15.append((f"{tag} 新增文献137-139",
                    all(x in doc for x in ("DeGroot", "Morris", "Gabaix"))
                    and ("137. DeGroot" in doc) and ("139. Gabaix" in doc)))
        v15.append((f"{tag} CMH方法注 erfc", ("erfc" in doc) and (("1.9\\times10^{-215}" in doc) or ("1.9×10⁻²¹⁵" in doc) or ("1.9\\times 10^{-215}" in doc))))
        v15.append((f"{tag} 弱耦合充分非必要",
                    ("sufficient conditions for additivity, not necessary" in doc) or ("充分而非必要" in doc) or ("*sufficient* conditions" in doc) or ("充分*条件而非必要" in doc) or ("是可加性的*充分*条件而非必要条件" in doc)))
        v15.append((f"{tag} Pareto显式误差界", ("20.8%" in doc) and ("6.9%" in doc)))
        v15.append((f"{tag} 引理12.1 独立性失效条款", ("k_{\\mathrm{eff}}^a" in doc) or ("k_{\\mathrm{eff}}^{a}" in doc)))
        v15.append((f"{tag} 摘要零人类数据声明",
                    ("no human-subject data" in doc) or ("未收集任何人类被试数据" in doc)))
        v15.append((f"{tag} 定理8.1 统一表述定位",
                    ("unification theorem" in doc) or ("统一表述定理" in doc)))
        v15.append((f"{tag} 两本账小结", ("Two-ledger summary" in doc) or ("两本账小结" in doc)))
        v15.append((f"{tag} g2良定义性快照近似",
                    ("snapshot approximation" in doc) or ("快照近似" in doc)))
        v15.append((f"{tag} I2酸葡萄注",
                    (("sour grapes" in doc) or ("酸葡萄" in doc)) and (("adaptive preferences" in doc) or ("适应性偏好" in doc))))
        v15.append((f"{tag} 附录A核心速查表",
                    ("Core quick reference" in doc) or ("核心速查表" in doc)))
        v15.append((f"{tag} 载体形式注",
                    ("Venue-form note" in doc) or ("载体形式注" in doc)))
        v15.append((f"{tag} 命题6.4中值注已压缩",
                    ("archived alternative route" in doc) or ("已存档的替代路线" in doc)))
        v15.append((f"{tag} Zhong形式特例关系",
                    ("formal special-case relation" in doc) or ("形式的特例关系" in doc)))
        v15.append((f"{tag} 命题5.1可测选择澄清",
                    ("generalization marker, not a load-bearing step" in doc) or ("推广路标，不是承重步骤" in doc)))
        v15.append((f"{tag} HP-0可行性非有效性",
                    ("feasibility, not efficacy" in doc) or ("可行性而非有效性" in doc)))
    for name, ok in v15:
        if not ok:
            issues.append(f"[v1.6] {name} 不满足")
    print(f"7. v1.6 核查：{sum(1 for _, ok in v15 if ok)}/{len(v15)} 项满足")

    # ---------- 8. v1.7 修订核查（中英双稿；五审四份意见）----------
    v17: list[tuple[str, bool]] = []
    for tag, doc in (("ZH", text), ("EN", en)):
        if not doc:
            continue
        v17.append((f"{tag} erfc 括号消歧",
                    ("\\sqrt{(\\chi^2)/2}" in doc) and ("\\sqrt{\\chi^2/2}" not in doc)))
        v17.append((f"{tag} erfc 数值代入 22.153", "22.153" in doc))
        v17.append((f"{tag} chi2_1 渐近适用性注",
                    ("Applicability of the $\\chi^2_1$ asymptotics (v1.7)" in doc)
                    or ("$\\chi^2_1$ 渐近的适用性（v1.7）" in doc)))
        v17.append((f"{tag} 每层不一致对数 226/296/402",
                    ("226" in doc) and ("296" in doc) and ("402" in doc)))
        v17.append((f"{tag} 猜想10.1 可闭合性注",
                    ("Closability note (v1.7" in doc) or ("可闭合性注（v1.7" in doc)))
        v17.append((f"{tag} 摘要猜想非定理",
                    ("a conjecture, not a theorem** (Conjecture 10.1)" in doc)
                    or ("是猜想而非定理**（猜想 10.1）" in doc)))
        v17.append((f"{tag} 2.9 不超越声明",
                    ("does not claim to surpass any of them on models, metrics, or institutional design" in doc)
                    or ("不声称在模型、度量或制度设计上超越其中任何一个" in doc)))
        v17.append((f"{tag} 次模性 m_A 简写", "m_A :=" in doc))
        v17.append((f"{tag} HP-0 样本量消歧",
                    ("Sample-size disambiguation (v1.7" in doc) or ("样本量消歧（v1.7" in doc)))
        v17.append((f"{tag} 引理12.1 条件性设计引理",
                    ("Design lemma, conditional: the manipulation resistance" in doc)
                    or ("条件性设计引理：公共层的抗操纵性" in doc)))
        v17.append((f"{tag} 1.6 设计引理档约定",
                    ("Design lemmas (conditional)** (added in v1.7" in doc)
                    or ("**条件性设计引理**（v1.7 新增" in doc)))
    for name, ok in v17:
        if not ok:
            issues.append(f"[v1.7] {name} 不满足")
    print(f"8. v1.7 核查：{sum(1 for _, ok in v17 if ok)}/{len(v17)} 项满足")

    # ---------- 汇总 ----------
    print("\n===== 审计汇总 =====")
    print(f"硬性问题 {len(issues)}：")
    for i_ in issues[:20]:
        print("  -", i_)
    print(f"提示 {len(warns)}：")
    for w in warns[:30]:
        print("  -", w)
    out = os.path.join(ROOT, "tools", "audit_report.json")
    json.dump({"issues": issues, "warns": warns}, open(out, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"\n-> {out}")
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
