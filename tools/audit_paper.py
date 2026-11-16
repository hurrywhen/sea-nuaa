"""论文投稿前一致性审计：编号交叉引用、文献闭合、关键数字对账、表格完整性、
目录一致、"进行中"措辞风险扫描。用法：python3 tools/audit_paper.py

已知设计取舍：
  - "v0.1 的定理 X" 类历史编号引用白名单豁免（指向纲领稿而非本文编号体系）；
  - 机构作者条目（C2PA 等）按缩写闭合；
  - 姓氏匹配 Unicode 感知（Matějka）且索引合著者（& 后姓氏）。
"""
from __future__ import annotations

import csv
import gzip
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAPER = os.path.join(ROOT, "input", "主权认知获取_统一理论_v1.8.md")
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
    en_path = os.path.join(ROOT, "input", "sovereign_epistemic_acquisition_EN_v1.8.md")
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
        v15.append((f"{tag} 定理8.1 KKT/角点与单位定位",
                    ("KKT characterization" in doc) or ("KKT 刻画" in doc)))
        v15.append((f"{tag} 已执行子列单一账本",
                     ("Why no veto-rate factor appears" in doc) or ("为什么没有否决率因子" in doc)))
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
        v17.append((f"{tag} 猜想10.1 KC2/KC5 未闭合清单",
                    (("Revised checklist for the $b_0>0$ sketch" in doc) or ("修订核验清单" in doc)) and (("Autonomous Lipschitz mean field" in doc) or ("自主 Lipschitz 均值场" in doc))))
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
                    ("Manipulation-sufficient, manipulation-present, and counterfactual attestation" in doc)
                    or ("操纵充分、操纵在场与反事实认证" in doc)))
        v17.append((f"{tag} 1.6 设计引理档约定",
                    ("Design lemmas (conditional)** (added in v1.7" in doc)
                    or ("**条件性设计引理**（v1.7 新增" in doc)))
    for name, ok in v17:
        if not ok:
            issues.append(f"[v1.7] {name} 不满足")
    print(f"8. v1.7 核查：{sum(1 for _, ok in v17 if ok)}/{len(v17)} 项满足")

    # ---------- 9. v1.8 大修专项核查（理论、证据、引用与可复现性）----------
    v18: list[tuple[str, bool]] = []
    for tag, doc in (("ZH", text), ("EN", en)):
        if not doc:
            continue
        def need(name: str, *terms: str) -> None:
            v18.append((f"{tag} {name}", all(term in doc for term in terms)))
        need("V4a/V4b 全部可表示", "(V4a)", "(V4b)", "\\mathcal D_\\lambda", "\\mathcal A(\\phi_i)")
        need("M_R 受限单调证书与受限最优", "(M$_R$)", "restricted feasible problem" if tag == "EN" else "受限可行问题")
        need("R4 实际消费", "R4", "actual consumption" if tag == "EN" else "实际消费")
        need("逐命题 RII 与 pooled 反例", "R_{\\mathrm{II}}(e)", "0.25")
        need("KKT 线性角点一阶损失", "V_1=x_1", "first-order loss" if tag == "EN" else "一阶损失")
        need("Pandora/patch 单位", "\\widetilde c_e", "B_0^H", "\\kappa_{sw}")
        need("历史条件已执行漂移与 KC2", "C1-H", "C3-H", "C5-H", "KC2")
        need("二项尾与数值回归", "\\binom{K}{k_c}", "0.028", "0.030")
        need("公共公告 S4-PA", "S4-PA", "self-evident" if tag == "EN" else "自明")
        need("criticality 目标/代理分离", "E_{\\mathrm{proxy}}", "v_e\\in[0,\\infty)")
        need("重放唯一键与 O 区间", "71,914", "1,633", "LEGACY_EXPLORATORY_NOT_DEDUPLICATED",
             "interval includes zero" if tag == "EN" else "区间跨零")
        need("匹配公共认证口径", "0.615", "1.230", "0.626", "1.359")
        need("引用硬错误修正", "Article 2333", "Shumaylov", "Article 20", "Article 3", "pgaf172")
        need("不可变归档与 v1.8 工作修订", "fdc4912a30174d71b944d1ec83fcfda260f8ebf1",
             "zenodo.23620920", "working-revision" if tag == "EN" else "工作修订")
        need("venue-dependent A/B/C 拆稿", "extreme filtering and redundancy coverage" if tag == "EN" else "极端过滤与冗余覆盖",
             "venue-dependent" if tag == "EN" else "取决于载体")
        need("治理有效性待检验", "propositions to be tested" if tag == "EN" else "待检验命题")
        need("M_R 非负系数", "\\mu\\ge0", "\\hat m_i\\ge0")
        need("patch 穿越条件", "must change from positive to negative" if tag == "EN" else "由正变负")
        need("操纵诱导事件语义", "\\mathcal M_{k_c}", "organic coverage" if tag == "EN" else "有机覆盖")
        need("执行递归可测停时", "strictly increasing stopping-time sequence" if tag == "EN" else "严格递增停时刻列", "M_\\xi<\\infty")
        need("B2 比较梗概非引理", "Heuristic B.2(ii)(b)" if tag == "EN" else "启发式 B.2(ii)(b)")
        need("条件概率正分母与 B4 边界", "P(B_e)>0", "k\\ge1", "dummy")
        need("可用记录与效应优先摘要", "Available raw records" if tag == "EN" else "可用的原始记录",
             "effect-first contrasts" if tag == "EN" else "效应优先对照",
             "successive trials" if tag == "EN" else "连续 trials")
        need("归档警示与三臂 RCT", "Archive warning" if tag == "EN" else "归档警示", "three-arm RCT" if tag == "EN" else "三臂 RCT")
        # 2026-11-03 P0/P1 follow-up: definitions, boundary regimes, and algorithms.
        need("VOI 决策特定而非互信息单调函数", "not a monotone function of conditional mutual information" if tag == "EN" else "而不是条件互信息的单调函数")
        need("KKT 边界活跃二次反例与正增益", "V_1=2x_1-\\tfrac12x_1^2", "V_1'(1)=V_2'(0)=\\nu=1", "o(\\epsilon)>0")
        need("Pandora 事前确定成本", "deterministic path known before opening" if tag == "EN" else "开盒前已知的确定性路径")
        need("Theorem 7.4 统一实际消费事件", "D_{\\mathrm{II}}(e)", "E^*\\setminus\\mathrm{WL}")
        need("Theorem 9.3 有效区间和边界", "0<G<D_m", "G\\ge D_m", "D_s")
        need("Proposition 9.2 gamma 与初值", "\\gamma := \\min\\{\\Pi_h, \\Pi_s\\} - \\Pi_m > 0", "x_m(0)\\in[0,1/2]")
        need("Theorem 11 有限授权与撤销成本", "nonempty finite" if tag == "EN" else "非空有限", "u_{\\mathrm{undo}}", "\\rho_{\\mathrm{adv}}^*")
        need("Theorem 11.2 一般虚警损失与严格条件", "C_F", "if and only if $\\Psi>0$" if tag == "EN" else "当且仅当 $\\Psi>0$")
        need("Lemma 12.1 三类认证与混合反例", "\\mathcal A_{\\mathrm{cf}}", "\\mathcal A_{\\mathrm{present}}", "S_{\\mathrm{manip}}", "O_i")
        need("Proposition 10.2 连接模型且投影", "separate linkage model" if tag == "EN" else "连接模型", "\\Pi_{[0,1]^3}[\\theta_{t_j}+a_{t_j}\\xi_{t_j}]")
        need("B2 确定系数与 B1/B5 边界", "deterministic sequences" if tag == "EN" else "确定数列", "n\\ge1", "finite action set" if tag == "EN" else "有限行动集")
        need("跨章精确摘要含 V4", "(V4), (V4a), and (V4b)" if tag == "EN" else "(V4)、(V4a) 与 (V4b)")
        need("背包可行元素枚举深度残余容量", "depth **three**" if tag == "EN" else "深度 **3**", "residual capacity" if tag == "EN" else "残余容量", "best feasible singleton" if tag == "EN" else "最佳可行单元素")
        need("三家族名义推断与日级敏感性", "nominal within-corpus" if tag == "EN" else "语料内名义推断", "day-cluster" if tag == "EN" else "日聚类", "moving-block" if tag == "EN" else "连续 5 日块")
        need("公共层实际共同消费量词", "\\mathcal C_S", "P(\\mathcal C_S)=1")
        need("紧急接管与抗记忆术语", "memorization-resistant new materials" if tag == "EN" else "抗记忆污染的新材料", "Emergency Override")
        need("log-benefit 含 A 与零收益", "B_i:=A_ic_iV_i", "order-equivalent" if tag == "EN" else "保序等价", "\\log B_i=-\\infty")
        need("Gaussian 独立噪声与 credibility 区分", "independent of $\\omega_d$" if tag == "EN" else "与 $\\omega_d$ 独立", "No map from $c_i$" if tag == "EN" else "模型不蕴含任何 $c_i")
        need("VOI/Blackwell 正则条件", "attainment and integrability" if tag == "EN" else "最大值可达与可积条件", "regular decision problem" if tag == "EN" else "正则决策问题")
        need("两行动虚警分支与非负危害", "C_F=0", "H_{\\max}\\ge0", "P_E=0")
        need("四家族全量重算与缺口分类", "CONTROLLED_UNIQUE_KEY_REANALYSIS__WITHIN_CORPUS_EXPLORATORY",
             "EMPTY_ONLY", "NO_SURVIVING_ROW", "71,573", "70,676", "71,618")
        need("A 主结果与 run-cluster 分歧", "0.443790", "0.532600", "0.516153", "0.519783", "0.160128")
        need("重算场景/CMH/BH 对账", "17 scenarios" if tag == "EN" else "17 个场景", "14,113", "9,371", "957.123190", "BH(4)")
        need("摘要与卷首重算完成状态", "controlled 17-scenario unique-key reanalysis" if tag == "EN" else "17 场景唯一键受控重算")
        need("相关漏网保留路径与期望界", "pathwise bound" if tag == "EN" else "路径界",
             "does not require independence" if tag == "EN" else "不需要独立性")
        need("退出仅移除公共层保证", "public-layer guarantee associated with their participation is removed" if tag == "EN" else "其参与所对应的公共层保证随之移除",
             "pairwise Jaccard overlaps" if tag == "EN" else "成对 Jaccard 重叠")
        need("局部 Lean 报告与非整篇认证", "quadratic_corner_is_optimal", "activation_loss_is_quadratic",
             "producer_threshold_exceeds_one", "mixed_attestation_not_subset_of_two_manipulations",
             "not independently reproduced" if tag == "EN" else "未独立复现")
        need("独立性仅限乘积型概率尾", "product-form union bound" if tag == "EN" else "乘积型 union bound",
             "event identities" if tag == "EN" else "事件恒等式",
             "do not assume independence" if tag == "EN" else "不假设独立性")
        need("跨章重算完成状态一致", "integrity audit and controlled unique-key reanalysis are complete" if tag == "EN" else "完整性审计与唯一键受控全量重算已完成",
             "incorporating the completed controlled unique-key reanalysis" if tag == "EN" else "纳入已完成的受控唯一键重算")
        need("Hoeffding 零暴露分支", "If $n_m=0$" if tag == "EN" else "若 $n_m=0$", "$n_m\\ge1$")
        need("加性评分最优选择遗憾", "V_{\\mathrm{lin}}", "\\arg\\max_{|A|\\le m}", "mD+0+mD=2mD")
        need("备用名额进入预算证明", "cannot also be counted as capacity" if tag == "EN" else "不能同时计作", "m-m_{\\mathrm{pub}}-m_{\\mathrm{slack}}")
        need("紧性构造端点闭合", "0<p_{\\min}<1", "deterministic variables" if tag == "EN" else "确定性变量")
        need("相关矩阵不构成独立证书", "pairwise uncorrelatedness does not imply mutual independence" if tag == "EN" else "两两不相关不蕴含相互独立",
             "neither a certificate nor a rigorous lower or upper bound" if tag == "EN" else "既不是 $k_{\\mathrm{eff}}$ 的证书，也不是其严格下界或上界")
        need("联合覆盖次模与三类反例", "No independence is needed for the set-function claim" if tag == "EN" else "集函数结论不需要独立性",
             ".89>.875", "not a partition" if tag == "EN" else "不给出 $k_{\\mathrm{eff}}$ 个组的分区",
             "upper bound on actual coverage" if tag == "EN" else "实际覆盖率的上界",
             "lower bound on actual miss probability" if tag == "EN" else "实际漏报率的下界")
        need("公共层非空仅示例", "not a guarantee of nonempty daily supply" if tag == "EN" else "不是每日非空供给保证",
             "separate supply and attestation assumptions" if tag == "EN" else "独立的供给与认证假设")
        need("union bound 本身无需独立", "which itself requires no independence" if tag == "EN" else "本身不依赖独立性的 union bound")
        old = ("4 model families × 80 independent runs", "73,547 valid agent-days",
               "Preliminary Validation", "Shumilo", "13, 1732", "randomized double-greedy",
               "the bound holds with $k_c$ replaced by $k_{\\mathrm{eff}}^a$",
               "run the full SEA stack on synthetic ecologies", "All raw records",
               "primary inference", "every printed number", "full two-arm RCT",
               "longitudinal trials", "cross-validating the model-collapse",
               "division-of-labor conclusion reinforced", "dual-domain real-data validation",
               "a finite interior solution exists iff", "P(\\mathrm{attestation})=P(S\\ge k_c)",
               "The proof of the R–S theorem itself is the standard tail-sum reduction",
               "zero and upper-bound uses satisfy",
               "a monotone function of the conditional information gain",
               "The first-order term vanishes only for reallocations",
               "strictly dominated by honesty at every $\\sigma$",
               "so $\\hat\\theta_{\\mathrm{cal}}$ is statistically independent",
               "Suppose $\\alpha_t,\\beta_t$ are predictable",
               "the pre-authorization quadruple",
               "The five-dimensional exact summary requires the sufficient conditions (V4a) and (V4b).",
               "memory-proof new materials", "statistically confirmed",
               "after taking logarithms, the benefit term $cVe^{-h/\\lambda}$",
               "precisely source-noise calibration",
               "In the two-action model of Theorem 11.1(ii), $C_F=c_p$;",
               "duplicate-disposition reanalysis pending", "full reanalysis required after duplicate disposition",
               "unique-key disposition and full reanalysis remain open",
               "requires a pre-specified duplicate-disposition rule followed by full reanalysis",
               "must be regenerated after duplicate disposition",
                "four-family estimates are legacy non-deduplicated exploratory results",
                "pre-specified duplicate disposition and full reanalysis of the reconciled unique keys",
                "no Lean or other formal proof certification", "this revision claims no Lean verification",
                "bound degenerates to the order of the expectation bound",
                "that subject's contribution to the population $\\Omega$ is zeroed",
                "four-family judgment replay under integrity review", "only after unique-key reanalysis",
                "number of merged groups is a lower-bound estimate", "run greedy in units of the $k_{\\mathrm{eff}}$ independent groups",
                "each in/out swap costs", "every day at least 1–2 propositions",
                "If classes are positively correlated, the true $P(\\text{covered by at least one class})$ is lower",
                "so the independence-product coverage formula is conservative")
        if tag == "ZH":
            old += ("精确测量", "全部原始记录", "主要推断", "每一个印刷数字", "完整两臂 RCT",
                    "两域加固", "双域真实数据验证", "存在当且仅当", "上界用途",
                    "条件信息增益的单调函数", "一阶项才消失。只有在同一活跃面", "预先授权四元组",
                    "零后见评估", "紧急覆盖", "防记忆新材料", "判断层增量价值统计确认",
                    "重复处置后的重算待完成", "重复处置后须全量重算", "唯一键处置与全量重算仍未完成",
                    "必须先预定重复处置规则，再作全量重算", "完成重复处置后必须重新生成",
                    "四家族估计均为旧管线未去重探索结果", "也没有 Lean 或其他形式化证明认证",
                    "本修订不声称完成 Lean 验证", "界退化到 $\\delta(1-\\rho_m)n_{\\max}$ 的期望界量级",
                    "该主体对群体 $\\Omega$ 的贡献归零", "退出的代价由本定理显式定价",
                    "四家族判断重放仍处于完整性复核", "须先完成唯一键重算",
                    "合并后的组数即 $k_{\\mathrm{eff}}$ 的下界估计", "以 $k_{\\mathrm{eff}}$ 个独立组为单位做贪心",
                    "每对入出调换的效用代价", "每日至少 1–2 个",
                    "若类间正相关，真实的 $P(\\text{至少一类覆盖})$ 低于独立公式",
                    "故独立乘积覆盖公式是保守的")
        v18.append((f"{tag} 旧过强/错误表述清除", not any(term in doc for term in old)))
    for name, ok in v18:
        if not ok:
            issues.append(f"[v1.8] {name} 不满足")
    print(f"9. v1.8 文本专项：{sum(1 for _, ok in v18 if ok)}/{len(v18)} 项满足")

    integrity = load("REPLAY_INTEGRITY_AUDIT.json")
    data_ok = False
    if integrity:
        totals = integrity.get("totals", {})
        expected = {"raw": 73704, "empty": 157, "valid": 73547, "unique": 71914,
                    "duplicate_excess": 1633, "below_nominal_900": 25,
                    "nominal_agent_days": 72000, "unique_deficit_vs_nominal": 86}
        data_ok = (all(totals.get(k) == v for k, v in expected.items())
                   and len(integrity.get("run_manifest", [])) == 80
                   and integrity.get("source_shards") == 292
                   and integrity.get("status") == "LEGACY_EXPLORATORY_NOT_DEDUPLICATED"
                   and integrity.get("disposition") == "UNRESOLVED_PREREGISTRATION_REQUIRED_THEN_RECOMPUTE")
        fam = integrity.get("family_totals", {})
        data_ok = data_ok and all(fam.get(f, {}).get("nominal_agent_days") == n
                                  for f, n in (("O", 27000), ("C", 27000), ("Q", 9000), ("G", 9000)))
    if not data_ok:
        issues.append("[v1.8] REPLAY_INTEGRITY_AUDIT 唯一键 manifest 对账失败")
    from math import comb
    tail = sum(comb(3, j) * 0.1**j * 0.9**(3-j) for j in range(2, 4))
    miss_display = (1 - 0.910) / (1 - 0.952) - 1
    miss_full = (1 - 0.9097744360902255) / (1 - 0.9523809523809523) - 1
    # Producer threshold must not be clipped: p_plat=.9,p_h=0,cost=0 gives >1.
    producer_sigma = 0.9 / (0.9 - 0.05)
    # Boundary-active quadratic example: both marginals equal one and loss is epsilon^2.
    def v1(x): return 2*x - x*x/2
    def v2(x): return x - x*x/2
    quadratic_losses = [v1(1) - (v1(1-e) + v2(e)) - e*e for e in (0.0, 0.1, 0.5, 1.0)]
    # Mixed raw-count example: one implant + one organic class attests, but is not M_2.
    B = [1, 0]; O = [0, 1]
    mixed_raw_attested = sum(max(b, o) for b, o in zip(B, O)) >= 2
    mixed_manipulation_sufficient = sum(B) >= 2
    # Three positively pairwise-correlated indicators can have union above the independent product formula.
    probs = {(1, 1, 1): .29, (1, 1, 0): .01, (1, 0, 1): .01, (0, 1, 1): .01,
             (1, 0, 0): .19, (0, 1, 0): .19, (0, 0, 1): .19, (0, 0, 0): .11}
    marginals = [sum(p for bits, p in probs.items() if bits[i]) for i in range(3)]
    pair_intersections = [sum(p for bits, p in probs.items() if bits[i] and bits[j])
                          for i, j in ((0, 1), (0, 2), (1, 2))]
    union_probability = 1 - probs[(0, 0, 0)]
    coverage_counterexample_ok = (abs(sum(probs.values()) - 1) < 1e-12
                                  and all(abs(p - .5) < 1e-12 for p in marginals)
                                  and all(abs(p - .30) < 1e-12 for p in pair_intersections)
                                  and union_probability > 1 - .5**3)
    math_ok = (abs(tail - 0.028) < 1e-12 and comb(3, 2) * 0.1**2 >= tail
               and abs(miss_display - 0.875) < 1e-12
               and abs(miss_full - 0.8947368421052632) < 1e-9
               and producer_sigma > 1 and max(abs(x) for x in quadratic_losses) < 1e-12
               and mixed_raw_attested and not mixed_manipulation_sufficient
               and coverage_counterexample_ok)
    if not math_ok:
        issues.append("[v1.8] 数值回归（二项尾/金融漏报/阈值/角点/混合认证/相关覆盖）失败")

    dependence = load("THREE_FAMILY_DEPENDENCE_SENSITIVITY.json")
    dependence_ok = False
    if dependence:
        fams = dependence.get("families", {})
        dependence_ok = (dependence.get("status") == "POST_HOC_WITHIN_CORPUS_DEPENDENCE_SENSITIVITY"
                         and len(fams) == 5
                         and dependence.get("bootstrap", {}).get("resamples_per_method_family_arm") == 10000)
        for tag, item in fams.items():
            for method in ("day_cluster", "moving_block_5"):
                ci = item.get("bootstrap", {}).get(method, {}).get("judgment_minus_parametric_ci95", [])
                dependence_ok = dependence_ok and len(ci) == 2 and ci[0] <= 0 <= ci[1]
        q = fams.get("qwen38all", {})
        dependence_ok = (dependence_ok and q
                         and abs(q.get("point_estimates", {}).get("judgment_minus_parametric", 0) - 0.0668103448275862) < 1e-12)
    if not dependence_ok:
        issues.append("[v1.8] 三家族依赖敏感性工件或参数对照区间对账失败")

    frozen = load("frozen_reanalysis_v1/summary.json")
    frozen_ok = False
    if frozen:
        frozen_ok = (frozen.get("status") == "CONTROLLED_UNIQUE_KEY_REANALYSIS__WITHIN_CORPUS_EXPLORATORY"
                     and frozen.get("input_manifest_count") == 292
                     and len(frozen.get("scenario_order", [])) == 17
                     and frozen.get("not_prospective_preregistration") is True
                     and frozen.get("cross_corpus_confirmatory") is False)
        st = frozen.get("structure", {})
        expected_frozen = {"expected_keys": 72000, "valid_unique_keys": 71914,
                           "empty_only_keys": 56, "no_surviving_row_keys": 30,
                           "resolved_recall_A": 71573, "resolved_value_A": 70676,
                           "resolved_sign_A": 71618, "resolved_B": 70676,
                           "resolved_C": 70306, "resolved_D": 70525, "resolved_E": 71914}
        frozen_ok = frozen_ok and all(st.get(k) == v for k, v in expected_frozen.items())
        scenarios = frozen.get("scenarios", {})
        frozen_ok = frozen_ok and scenarios.get("E", {}).get("all_80_runs", {}).get("paired_inference") is None
        expected_effects = {
            "O": (0.030169581001408607, -0.17501551269772986),
            "C": (0.129282950253562, 0.6673802451225368),
            "Q": (0.11288735607185085, 0.426727386567186),
            "G": (0.08941244179928154, -0.2190528269004773),
        }
        for family, (dr, dv) in expected_effects.items():
            eq = scenarios.get("A", {}).get("families", {}).get(family, {}).get("equal_run", {})
            frozen_ok = (frozen_ok
                         and abs(eq.get("delta_recall", {}).get("estimate", 0) - dr) < 1e-12
                         and abs(eq.get("delta_value", {}).get("estimate", 0) - dv) < 1e-12)
        o_ci = scenarios.get("A", {}).get("families", {}).get("O", {}).get("equal_run", {}).get("delta_recall", {}).get("ci95", [])
        frozen_ok = frozen_ok and len(o_ci) == 2 and o_ci[0] < 0 < o_ci[1]
        flip_o = scenarios.get("A", {}).get("families", {}).get("O", {}).get("paired_inference", {}).get("run_cluster_sign_flip", {})
        frozen_ok = frozen_ok and abs(flip_o.get("p", 0) - 0.16012839871601284) < 1e-12
        cmh = scenarios.get("A", {}).get("all_80_runs", {}).get("paired_inference", {}).get("pooled_cmh_three_formulas", {})
        frozen_ok = (frozen_ok and cmh.get("B") == 14113 and cmh.get("C") == 9371
                     and abs(cmh.get("continuity_corrected", {}).get("chi2", 0) - 957.1231902571964) < 1e-9)
        artifacts = frozen.get("artifacts", {})
        frozen_ok = (frozen_ok and artifacts.get("run_metric_rows") == 1360
                     and artifacts.get("key_ledger_rows") == 72000)
        frozen_dir = os.path.join(RES, "frozen_reanalysis_v1")
        try:
            with open(os.path.join(frozen_dir, "run_metrics.csv"), encoding="utf-8", newline="") as handle:
                frozen_ok = frozen_ok and sum(1 for _ in csv.DictReader(handle)) == 1360
            with gzip.open(os.path.join(frozen_dir, "key_ledger.jsonl.gz"), "rt", encoding="utf-8") as handle:
                frozen_ok = frozen_ok and sum(1 for _ in handle) == 72000
            manifest = json.load(open(os.path.join(frozen_dir, "input_manifest.json"), encoding="utf-8"))
            frozen_ok = frozen_ok and len(manifest) == 292
        except (OSError, EOFError, json.JSONDecodeError):
            frozen_ok = False
    if not frozen_ok:
        issues.append("[v1.8] 四家族唯一键全量重算工件或场景矩阵对账失败")
    print(f"10. 工件与数值回归：manifest={'PASS' if data_ok else 'FAIL'}；math={'PASS' if math_ok else 'FAIL'}；three-family-dependence={'PASS' if dependence_ok else 'FAIL'}；frozen-reanalysis={'PASS' if frozen_ok else 'FAIL'}")

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
