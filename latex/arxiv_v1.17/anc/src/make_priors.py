"""默认先验表 v0.1 生成器（论文 §14.6 的阶段三交付物）。

汇总全部试点/实验的实测参数为部署期个人参数化的起点（非任何个人偏好的直接输入）；
每个参数标注来源、状态（实测 / 机制验证 / 条件性 / 冻结待标定）与适用范围。
运行：cd sim && python3 -m sea_pilot.make_priors
输出：pilot/results/DEFAULT_PRIORS_v0.1.md + default_priors_v0.1.json
"""
from __future__ import annotations

import json
import os

from . import config

RES = config.RESULTS_DIR


def _load(name):
    p = os.path.join(RES, name)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}


def main() -> None:
    pilot = _load("pilot_summary.json")          # P3
    p2 = _load("p2_summary.json")                # P2 v3
    p3up = _load("p3up_results.json")
    p3emb = _load("p3embed_results.json")
    eco = _load("ecosystem_results.json")
    roll = _load("rolling_results.json")
    om = _load("p5_omega_results.json")
    fam = _load("three_family_analysis.json")
    h9o = _load("h9_ornith.json")

    rows = []  # (参数, 默认先验, 来源, 状态, 适用范围/条件)
    A = rows.append

    # ---- 结构参数 ----
    A(("ρ_c 命题坍缩比（学术域）", "1.0", "P3 arXiv 2019-09 实测", "实测",
       "单源预印本流；期刊/会议转载会抬高"))
    A(("ρ_c（金融域）", f"{p2.get('rho_c_measured', 8.19):.1f}",
       "P2 EDGAR+10 域新闻层实测", "实测", "落入论文先验区间 [5,20]；新闻层再扩会续升"))
    A(("p_min 监管一手类（法定真值）", "1.00", "P2 实测（8-K 四日规则）", "实测",
       "法律强制披露域特有；不可迁移到无披露义务域"))
    A(("p_min 监管一手类（市场真值）", f"{p2['env']['class_coverage']['regulator']['p_min_hat_market']:.2f}",
       "P2 实测", "实测", "价格移动不必有披露"))
    A(("p_min 通讯社/财经/科技媒体类（市场真值）",
       f"{p2['env']['class_coverage']['wire']['p_min_hat_market']:.2f} / "
       f"{p2['env']['class_coverage']['fin_media']['p_min_hat_market']:.2f} / "
       f"{p2['env']['class_coverage']['tech_media']['p_min_hat_market']:.2f}",
       "P2 实测（CDX 10 域）", "实测", "多类冗余结构 k_eff≥2 可用"))
    A(("p_min 学术域机构清单（top-50）", f"{roll.get('p_min_hat', {}).get('rolling', 0.269):.2f}（滚动）",
       "滚动更新实验（10 月评估）", "实测", "静态清单 0.231；作者粒度仅 0.02——机构粒度+月度滚动"))

    # ---- 评分质量 ----
    d_tf = p3up.get("d_prime_real_features", 0.77)
    d_emb = p3emb.get("d_prime_embed_title_novelty", 0.73)
    A(("d′ 评分分离度（学术域）", f"TF-IDF {d_tf:.2f} / 嵌入 {d_emb:.2f}",
       "P3 真实特征实测（零后见）", "实测", "距 95% 召回需求线 4.39 一个量级——召回必须由架构承担"))
    fs = p2.get("feature_scorer", {})
    A(("d′（金融域，双真值分裂）", f"legal {fs.get('d_prime_legal', 3.49):.2f} / "
       f"market {fs.get('d_prime_market', 0.54):.2f}",
       "P2 v3 实测（walk-forward）", "实测", "法定关键性可预测、市场关键性弱——评分职责按真值类型分工"))
    A(("d′ 需求线（95% 召回）", "≈4.4（β=0.0125, π=0.01 典型参数）", "定理 6.1(iii) 解析",
       "机制验证", "恒等式在两域实测 corr 0.968–0.987"))

    # ---- 行为参数（LLM 智能体）----
    fams = fam.get("families", {})
    imp = {t: f.get("impulse_rate") for t, f in fams.items()}
    A(("冲动注入消费率（δ 显著性代理）",
       " / ".join(f"{k}:{v:.2f}" for k, v in imp.items() if v is not None),
       "三家族重放（各 240 agent-day）", "实测",
       "推理型最高（ornith 0.45）；入 O6 转移系数库；人类 δ 维持文献先验"))
    h8tags = ("ornith", "gemma26na", "qwen38na")
    a2 = {}
    for t in h8tags:
        d = _load(f"h8v2_{t}.json")
        if d.get("A2"):
            a2[t] = d["A2"].get("effect_cohend_false_share")
    A(("准确性提示效应 d（A2，假分享）",
       " / ".join(f"{k}:{v:+.2f}" for k, v in a2.items() if v is not None),
       "H8 v2.1 三家族", "实测（方向入先验）", "方向三家族一致为负；量级按家族配系数"))
    b2 = {}
    for t in h8tags:
        d = _load(f"h8v2_{t}.json")
        if d.get("B2"):
            b2[t] = d["B2"].get("effect_cohend_extremity")
    A(("对立暴露极端度 d（B2）", " / ".join(f"{k}:{v:+.2f}" for k, v in b2.items() if v is not None),
       "H8 v2.1", "**冻结（跨家族方向不一致）**", "不得入先验；进 O6"))
    c2 = {}
    for t in h8tags:
        d = _load(f"h8v2_{t}.json")
        if d.get("C2"):
            c2[t] = d["C2"].get("dprime_mean")
    A(("辨别 d′（C2 防记忆材料）", " / ".join(f"{k}:{v:.2f}" for k, v in c2.items() if v),
       "H8 v2.1", "实测", "落人类区间 1.0–1.8 近旁——材料有效"))
    h9s = {t: _load(f"h9_{t}.json") for t in ("ornith", "gemma26na", "qwen38na")}
    h9s = {t: v for t, v in h9s.items() if v}
    if h9s:
        anchor = next(iter(h9s.values())).get("human_anchor_manifold", float("nan"))
        parts = ", ".join(f"{t} {v.get('brier_agent', float('nan')):.3f}" for t, v in h9s.items())
        A(("θ_cal 初始化锚（Brier，40 题防记忆）", f"{parts}；人类锚(Manifold n=151) {anchor:.3f}",
           "H9 三家族", "**家族依赖**", "ornith 落带内（超级预测者水平）；qwen 略超带；"
           "gemma 差于常数基线 0.219（过度自信）——θ_cal 锚仅推理型家族成立，进 O6"))

    # ---- 生态与公共性 ----
    th = eco.get("A_phase_transition", {}).get("theory", {})
    A(("σ*_ms / σ*_sh（生态相边界）", f"{th.get('sigma_ms', 0.06):.3f} / {th.get('sigma_sh', 0.2):.3f}",
       "合成生态（生成器参数 aA=100, ε_g=0.05 标定）", "机制验证（条件性）",
       "数值随生成器参数变；相图与解析精确吻合"))
    A(("检测器更新价值（Red Queen）", "有效 σ* 从 0.15（最坏漂移）钉回 0.086（均值漂移）",
       "合成生态 B 部", "机制验证", "更新不能替代采纳"))
    om_w = om.get("omega", {})
    A(("公共层 γ", f"{om_w.get('gamma', 0.2)}（默认上限）", "Ω 仿真验证", "机制验证",
       f"Ω={om_w.get('with_public', 0.168):.3f} ≥ 下界 {om_w.get('theory_floor', 0.111):.3f}；无公共层 {om_w.get('without_public', 0.066):.3f}"))
    A(("认证阈值 k_c", "冻结（原候选 2）", "认证反转发现（lift 0.63×）", "**冻结待重设计**",
       "原始类覆盖计数被注意力俘获；需相对稀缺性/质量加权标准"))

    # ---- 运行参数 ----
    A(("通道 I 配额 CHANNEL1_QUOTA", "0.6", "P2/P3 全程报警机制有效", "机制验证",
       "供给>配额时召回以清单内排序质量为中介"))
    A(("清单粒度/节奏", "机构粒度 top-50 / 月度滚动", "滚动实验（Jaccard 0.39 月换手）", "实测",
       "低冗余域必须滚动；B 类快速审批通道"))
    A(("预算 m（画像默认）", "P3: 3 篇/日深读；P2: 5 命题/日（H4 达成档）", "画像试点", "实测",
       "P2 组合内召回 0.952 @ m=5"))
    A(("LLM 后端工程参数", "max_tokens 4500–6000（推理型加倍至上限）；qwen 系 enable_thinking=false；"
       "垃圾输出检测阈值 60%；重试 8–12 次退避 ≤60s", "三次服务端事故复盘", "运维规程",
       "AI智能体实验设计 §2.4"))

    os.makedirs(RES, exist_ok=True)
    json.dump([{"param": r[0], "prior": r[1], "source": r[2], "status": r[3], "scope": r[4]}
               for r in rows],
              open(os.path.join(RES, "default_priors_v0.1.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    L = ["# 默认先验表 v0.1（阶段三交付物，论文 §14.6）\n",
         "部署期个人参数化的**起点**而非终点；全部默认值公开并附来源（§16.2 默认值即价值观）。",
         "状态口径：**实测** = 真实数据直接测量；**机制验证** = 理论关系在仿真/重放中确认（数值随环境变）；"
         "**冻结** = 发现失效模式，暂停使用待重设计。\n",
         "| 参数 | 默认先验 | 来源 | 状态 | 适用范围/条件 |",
         "|---|---|---|---|---|"]
    for r in rows:
        L.append("| " + " | ".join(str(x) for x in r) + " |")
    L += ["", "## 使用规则\n",
          "1. 个人化修订一律走 B 类决策（S2 签字 + 冷却期），修订历史入 S4 日志；",
          "2. **冻结项**（k_c、B2 效应量）不得进入任何自动决策路径；",
          "3. 条件性数值（σ* 系）只在对应生成器参数带内引用；",
          "4. 本表随每次实验轮次增量更新（`python3 -m sea_pilot.make_priors` 重生成）。"]
    open(os.path.join(RES, "DEFAULT_PRIORS_v0.1.md"), "w", encoding="utf-8").write("\n".join(L))
    print(f"[priors] {len(rows)} 个参数 -> {os.path.join(RES, 'DEFAULT_PRIORS_v0.1.md')}")


if __name__ == "__main__":
    main()
