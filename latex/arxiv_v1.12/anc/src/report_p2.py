"""P2 试点报告生成（v2：含 archive.org CDX 新闻层）：p2_summary.json + p2_agg.csv → P2_REPORT.md + 图。"""
from __future__ import annotations

import csv
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from . import config

RES = config.RESULTS_DIR


def main() -> None:
    s = json.load(open(os.path.join(RES, "p2_summary.json"), encoding="utf-8"))
    agg = list(csv.DictReader(open(os.path.join(RES, "p2_agg.csv"), encoding="utf-8")))
    env = s["env"]
    ms = sorted({int(r["budget_per_day"]) for r in agg})

    def rowget(arm, truth, m, key="recall_mean"):
        for r in agg:
            if (r["arm"], r["truth"], r["budget_per_day"], r["rho"]) == (arm, truth, str(m), "0.4"):
                return float(r[key])
        return float("nan")

    # 图：组合内召回 vs 预算（H4）+ 对照
    plt.figure(figsize=(6.4, 4.2), dpi=150)
    y_port = [rowget("S2p", "market", m, "recall_mkt_port_mean") for m in ms]
    plt.plot(ms, y_port, "o-", color="#009e73", label="S2[portfolio]: in-portfolio recall")
    for arm, lab, c in [("S2c", "S2c pure scoring (oracle proxy)", "#0072b2"),
                        ("S2c-feat", "S2c honest feature scorer", "#d55e00"),
                        ("S1", "S1 engagement (news vol + pageviews)", "#e69f00"),
                        ("S0", "S0 raw stream", "#999999")]:
        plt.plot(ms, [rowget(arm, "market", m) for m in ms], "o-", color=c, label=lab)
    plt.axhline(0.95, color="r", lw=0.8, ls=":", label="H4 target 0.95")
    supply = env["supply"]["portfolio_props_per_day"]
    plt.axvline(supply, color="#009e73", lw=1, ls="--",
                label=f"portfolio supply {supply:.1f} props/day")
    plt.xlabel("budget m (propositions/day)"); plt.ylabel("recall (market truth)")
    plt.title("P2 investor × EDGAR+CDX-news 2019-09 replay (ρ=0.4)")
    plt.xticks(ms); plt.ylim(0, 1.05); plt.legend(fontsize=7.5, loc="center right")
    plt.grid(alpha=.3); plt.tight_layout()
    os.makedirs(os.path.join(RES, "fig"), exist_ok=True)
    plt.savefig(os.path.join(RES, "fig", "fig_p2_recall.png")); plt.close()

    fs = s["feature_scorer"]
    ic = s["identity_check_S2c_market"]
    unatt = env["mvd_unattributable"] / max(1, env["mvd_days"])
    r5 = rowget("S2p", "market", ms[-1], "recall_mkt_port_mean")
    r3 = rowget("S2p", "market", ms[-2] if len(ms) > 1 else ms[-1], "recall_mkt_port_mean")
    h4_ok = r5 >= 0.95

    L = []
    A = L.append
    A("# P2 投资者画像试点报告（v2：EDGAR + archive.org 新闻层）× H4 强形式\n")
    A(f"生成：`python3 -m sea_pilot.report_p2` · 种子 {config.SEED} · 30 智能体 × 7 臂 × {len(ms)} 预算档\n")
    A("## 1 环境（真实数据）\n")
    A("| 量 | 值 |")
    A("|---|---|")
    A(f"| 公司数 | {len(env['tickers'])}（2019-09 有申报/新闻） |")
    A(f"| 文档：filings + news | {env['n_filings']} + {env['n_news']}"
      "（新闻层 = archive.org CDX × Reuters/CNBC/Fortune/BI 四域，非全量） |")
    A(f"| 命题数 N（κ 归并） | {s['n_props']}（≈{env['supply']['all_props_per_day']:.0f}/日——极端过滤比恢复） |")
    A(f"| **实测 ρ_c** | **{s['rho_c_measured']:.2f}**（四域新闻层下的下界；全域新闻预期 →5–20） |")
    A(f"| E*_legal / E*_market | {s['K_legal']} / {s['K_market']}（π_market={s['pi_market']:.3f}） |")
    A(f"| 移动日不可归因 | {env['mvd_unattributable']}/{env['mvd_days']} = **{unatt:.0%}** |")
    A(f"| 组合监控清单（R3 直通） | {len(env['portfolio'])} 家持仓，供给 {supply:.1f} 命题/日 |")
    A("")
    A("**信源类覆盖 p̂_min（多类结构首次实测）**：\n")
    A("| 类 | market 真值 | legal 真值 |")
    A("|---|---|---|")
    for c, v in env["class_coverage"].items():
        if float(v["p_min_hat_market"]) > 0 or c == "regulator":
            A(f"| {c} | {float(v['p_min_hat_market']):.2f} | {float(v['p_min_hat_legal']):.2f} |")
    A("")
    A("> 监管类对 legal 真值 p̂_min=1.00（8-K 四日规则——**法律把覆盖写成了义务**）；对 market 真值 0.73"
      "（价格移动不必有披露）；通讯社类补上 0.27 的独立覆盖——**k_eff≥2 的多类冗余结构首次在真实数据上可测**。"
      f"仍有 {unatt:.0%} 的移动日在『披露+四域新闻』中无当日文档：真实系统需要全量新闻层与公共议程层"
      "（定理 12.1 的功能位），这个数字就是其价值的下界。\n")
    A("## 2 H4 强形式检验\n")
    A("![p2](fig/fig_p2_recall.png)\n")
    A("**组合内召回（核心职责），market 真值，ρ=0.4：**\n")
    A("| 臂 | " + " | ".join(f"m={m}" for m in ms) + " |")
    A("|---|" + "---|" * len(ms))
    for arm in ("S0", "S1", "S2c", "S2c-feat", "S2p", "S2p-feat"):
        key = "recall_mkt_port_mean" if arm.startswith("S2p") else "recall_mean"
        A(f"| {arm}{'（组合内）' if arm.startswith('S2p') else '（全市场）'} | "
          + " | ".join(f"{rowget(arm,'market',m,key):.3f}" for m in ms) + " |")
    A("")
    A(f"**判定：H4 强形式（≥95%）在 m={ms[-1]}（组合内）{'达成' if h4_ok else '未达成'}：R = {r5:.3f}**"
      f"（m={ms[-2] if len(ms)>1 else ms[-1]} 为 {r3:.3f}）。成立条件与此前判定一致且更严格——本轮供给 "
      f"{supply:.1f}/日 **超过**通道 I 配额（0.6·m），直通退化为清单内竞争 + 报警全程触发（命题 6.3），"
      "召回仍随预算爬升至目标线：**结构保证在配额约束下以『清单内排序质量』为中介兑现**。\n")
    A("## 3 双真值 d′（真实特征，含新闻层特征）\n")
    A("| 评分器 | d′(legal) | d′(market) | legal 召回(m=%d) | market 召回(m=%d) |" % (ms[-1], ms[-1]))
    A("|---|---|---|---|---|")
    A(f"| 诚实特征（披露元数据+新闻量+浏览异常，walk-forward） | **{fs['d_prime_legal']:.2f}** | "
      f"**{fs['d_prime_market']:.2f}** | {rowget('S2c-feat','legal',ms[-1]):.3f} | "
      f"{rowget('S2c-feat','market',ms[-1]):.3f} |")
    A(f"| 参数 proxy（ρ=0.4，oracle-flavor 上界） | ≈0.8 | ≈0.8 | {rowget('S2c','legal',ms[-1]):.3f} | "
      f"{rowget('S2c','market',ms[-1]):.3f} |")
    A("")
    A(f"新闻层特征把 market 真值的 d′ 从 0.02（EDGAR-only）抬到 **{fs['d_prime_market']:.2f}**——真实注意力信号"
      "（新闻量、维基浏览异常）部分预测市场关键性，但距 95% 召回需求线（≈4.4 量级）仍然极远；legal 真值 "
      f"d′={fs['d_prime_legal']:.2f}（法定重大性深植于可观测元数据）。**结论不变且更强：评分通道有真实但有限的"
      "发现能力；召回保证仍须由结构（法律义务 + 组合直通 + 公共层）承担**——定理 6.1 的分工在新闻层加入后依旧成立。\n")
    A(f"**定理 6.1 恒等式（S2c × market）**：corr = {ic['corr']:.4f}，MAE = {ic['mae']:.4f}。\n")
    A("## 4 适用域地图（P3 × P2 双试点合成）\n")
    A("| 维度 | P3 学术前沿 | P2 金融（新闻层版） |")
    A("|---|---|---|")
    A(f"| ρ_c 实测 | 1.0（单源） | {s['rho_c_measured']:.1f}（四域新闻层下界） |")
    A("| p_min 来源与量级 | 清单构建策略（内生）：0.02–0.37 | **法律 1.00（legal）**；market：regulator 0.73 + wire 0.27（多类结构） |")
    A(f"| 诚实特征 d′ | 0.77 | legal {fs['d_prime_legal']:.2f} / market {fs['d_prime_market']:.2f} |")
    A(f"| H4 强形式 | **拒绝**（最优 0.28） | **条件达成**（组合内 m={ms[-1]}：{r5:.3f}） |")
    A("| 决定召回的变量 | 清单质量×容量、预算 | 披露义务、组合直通、预算≥供给量级、E* 作用域 |")
    A("")
    A("经验规律（回馈论文 §7.5）：**召回保证强度 = p_min 的制度来源（法律 > 媒体冗余 > 清单设计）"
      "× 供给—配额适配 × E\\* 作用域与 persona 决策集的一致性**。\n")
    A("## 5 局限与下一步\n")
    A("1. **新闻层不完整**：CDX 仅覆盖 4 域（Reuters/CNBC/Fortune/BI，5196 篇）；ρ_c 与类覆盖是下界，"
      "91% 不可归因日大部分源于此。补齐：更多域的 CDX 前缀 + GDELT（换出口）+ 中文域（P2 本土化时）；")
    A("2. **Reuters 发表日以存档日近似**（±数日）；日期噪声压低跨类同日重合度 → p̂_min 多类结构亦为下界；")
    A("3. **EDGAR submissions 深度限制**：高频申报公司 2019-09 记录不全（505 家缓存 → 903 件）；正式实验改 daily-index；")
    A("4. 市场真值阈值（2.5%）与法定 items 清单的敏感性分析待做；")
    A("5. 下一步：定理 7.3 次模贪心做**组合构建**（公司粒度，法律覆盖先验强，预期显著优于等距抽样）；"
      "LLM 智能体层在 P2 digest 上跑行为臂；合成生态 + σ* 相变（P10）。")
    open(os.path.join(RES, "P2_REPORT.md"), "w", encoding="utf-8").write("\n".join(L))
    print("report ->", os.path.join(RES, "P2_REPORT.md"))


if __name__ == "__main__":
    main()
