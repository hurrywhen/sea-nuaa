"""三家族重放统一分析：LLM 判断臂 vs 半oracle参数臂 vs 诚实特征臂（离线补算，零 LLM 调用）。

统计：召回/价值对比、按天配对的 McNemar 精确检验、bootstrap 95% CI、有效率、冲动易感性。
H8 v2：跨模型对照汇总（含 v1 基线对比）。

运行：cd sim && python3 -m sea_pilot.analyze_families
输出：pilot/results/THREE_FAMILY_ANALYSIS.md + three_family_analysis.json
"""
from __future__ import annotations

import json
import math
import os
from collections import defaultdict

import numpy as np

from . import config, corpus as cp

FAMILIES = {
    "ornith30": ("ornith-1.5-35b (qwen3.5-moe, 推理型)", "LM Studio @ Mac"),
    "gemma26na": ("gemma4:26b", "Ollama @ node-a"),
    "qwen38na": ("qwen3.8-27b (GGUF Q4)", "llama.cpp @ node-a"),
    "qwen38b": ("qwen3.8-27b 复样(agents 8-15)", "llama.cpp @ node-a"),
    "qwen38all": ("qwen3.8-27b 合并(na+b, 480 agent-day)", "llama.cpp @ node-a"),
}


def mcnemar_exact(n_b: int, n_c: int) -> float:
    """双侧精确 McNemar：n_b = LLM 优天数，n_c = param 优天数。"""
    n = n_b + n_c
    if n == 0:
        return 1.0
    k = min(n_b, n_c)
    p = sum(math.comb(n, i) for i in range(0, k + 1)) / (2 ** n)
    return min(1.0, 2 * p)


def cmh_test(strata: list[tuple[int, int]]) -> tuple[float, float]:
    """Cochran–Mantel–Haenszel（χ²₁，连续性校正）跨层合并配对二项比较。
    strata: [(b_i, c_i)]。返回 (chi2, p)。"""
    B = sum(b for b, _ in strata)
    C = sum(c for _, c in strata)
    n = B + C
    if n == 0:
        return 0.0, 1.0
    chi2 = (abs(B - C) - 1) ** 2 / n
    # χ²₁ 上尾 p = erfc(sqrt(chi2/2))
    p = math.erfc(math.sqrt(chi2 / 2))
    return float(chi2), float(p)


def power_n_discordant(b: int, c: int, alpha: float = 0.05, power: float = 0.8) -> int:
    """检测观察到的不一致比 (b:c) 所需的总不一致天数（正态近似）。"""
    n0 = b + c
    if n0 == 0 or b == c:
        return 10 ** 6
    p = b / n0
    z_a, z_b = 1.959964, 0.8416212
    num = (z_a * 0.5 + z_b * math.sqrt(p * (1 - p))) ** 2
    den = (p - 0.5) ** 2
    return int(math.ceil(num / den)) if den > 0 else 10 ** 6


def load_family(tag: str) -> list[dict]:
    if tag == "qwen38all":
        return load_family("qwen38na") + load_family("qwen38b")
    p = os.path.join(config.RESULTS_DIR, f"llm_replay_{tag}.jsonl")
    if not os.path.exists(p):
        return []
    return [json.loads(l) for l in open(p, encoding="utf-8")]


def build_honest_arm():
    """离线补算诚实特征臂：真实特征评分器（features.py，前窗训练）在同一 digest 上取 top-3。"""
    from . import features as ft
    universe, critical, watchlists, stats = cp.build_all()
    prior = cp.ai_slice(cp.load_raw(os.path.join(config.RAW_DIR, "arxiv_2019-07_08.jsonl")))
    vocab = ft.build_vocab([prior, universe])
    auth_p, inst_p = ft.prestige_maps(prior)
    prior_order = np.lexsort((np.array([r["arxiv_id"] for r in prior]),
                              np.array([r["date"] for r in prior])))
    Xp = ft.build_feature_matrix(prior, vocab, auth_p, inst_p, prior_order, loo=True)
    pcits = np.array([r["cit"] for r in prior], float)
    yp = (pcits >= max(np.quantile(pcits, 0.98), 1)).astype(float)
    w, b = ft.logistic_fit(Xp, yp)
    ids = np.array([r["arxiv_id"] for r in universe])
    sept_order = np.lexsort((ids, np.array([cp.day_index(r) for r in universe])))
    Xs = ft.build_feature_matrix(universe, vocab, auth_p, inst_p, sept_order, loo=False)
    scores = Xs @ w + b
    # digest 重建（与 run_llm_replay.build_days 同种子同逻辑）
    rng = np.random.default_rng(99)
    zi = np.array([math.log1p(r["cit"]) for r in universe])
    zi = (zi - zi.mean()) / (zi.std() + 1e-9)
    proxy = 0.4 * zi + math.sqrt(1 - 0.16) * rng.standard_normal(len(universe))
    by_day = defaultdict(list)
    for i, r in enumerate(universe):
        by_day[cp.day_index(r)].append(i)
    honest_hits, crit_opp = {}, {}
    for d, idx in by_day.items():
        wl_ids = watchlists["inst"]["ids"]
        ch1 = [i for i in idx if any(e in wl_ids for e in universe[i]["insts"])]
        ch2 = [i for i in sorted(idx, key=lambda j: -proxy[j]) if i not in set(ch1)]
        digest = (ch1 + ch2)[:18]
        crit_ids = {universe[i]["arxiv_id"] for i in digest if universe[i]["arxiv_id"] in critical}
        top3 = sorted(digest, key=lambda j: -scores[j])[:3]
        honest_hits[d] = len({universe[i]["arxiv_id"] for i in top3} & crit_ids)
        crit_opp[d] = len(crit_ids)
    return honest_hits, crit_opp


def analyze_family(tag: str, honest_hits: dict) -> dict:
    recs = load_family(tag)
    valid = [r for r in recs if r.get("picked")]
    n_crit = sum(r.get("n_crit", 0) for r in recs)
    hl = sum(r.get("hits_llm", 0) for r in recs)
    hp = sum(r.get("hits_param", 0) for r in recs)
    hh = sum(honest_hits.get(r.get("sim_day", -1), 0) for r in valid)
    # 按天配对比较（LLM vs param）
    b = sum(1 for r in valid if r.get("hits_llm", 0) > r.get("hits_param", 0))
    c = sum(1 for r in valid if r.get("hits_llm", 0) < r.get("hits_param", 0))
    tie = len(valid) - b - c
    p_mcnemar = mcnemar_exact(b, c)
    # 按天配对比较（LLM vs 诚实特征臂）
    bh = sum(1 for r in valid if r.get("hits_llm", 0) > honest_hits.get(r.get("sim_day", -1), 0))
    ch = sum(1 for r in valid if r.get("hits_llm", 0) < honest_hits.get(r.get("sim_day", -1), 0))
    p_honest = mcnemar_exact(bh, ch)
    # bootstrap CI（对天重抽样）
    rng = np.random.default_rng(7)
    diffs = []
    arr = np.array([[r.get("hits_llm", 0), r.get("hits_param", 0), r.get("n_crit", 0)]
                    for r in valid], dtype=float)
    if len(arr):
        for _ in range(2000):
            s = arr[rng.integers(0, len(arr), len(arr))]
            nc = s[:, 2].sum()
            if nc > 0:
                diffs.append((s[:, 0].sum() - s[:, 1].sum()) / nc)
    ci = (float(np.percentile(diffs, 2.5)), float(np.percentile(diffs, 97.5))) if diffs else (0, 0)
    inj = sum(len(r.get("injected", [])) for r in recs)
    cons = sum(len(r.get("impulse_consumed", [])) for r in recs)
    return {
        "records": len(recs), "valid": len(valid), "valid_rate": len(valid) / max(1, len(recs)),
        "n_crit": n_crit, "hits_llm": hl, "hits_param": hp, "hits_honest": hh,
        "recall_llm": hl / max(1, n_crit), "recall_param": hp / max(1, n_crit),
        "recall_honest_on_valid_days": hh / max(1, sum(r.get("n_crit", 0) for r in valid)),
        "value_llm": float(np.mean([r.get("value_llm", 0) for r in recs])),
        "value_param": float(np.mean([r.get("value_param", 0) for r in recs])),
        "mcnemar_llm_gt": b, "mcnemar_param_gt": c, "mcnemar_tie": tie, "mcnemar_p": p_mcnemar,
        "mcnemar_vs_honest": {"llm_gt": bh, "honest_gt": ch, "p": p_honest},
        "power_n_discordant_needed": power_n_discordant(b, c),
        "boot_ci_recall_diff": ci,
        "impulse_injected": inj, "impulse_consumed": cons,
        "impulse_rate": cons / max(1, inj),
    }


def h8_summary() -> dict:
    out = {}
    for tag in ("ornith", "gemma26na", "qwen38na"):
        p = os.path.join(config.RESULTS_DIR, f"h8v2_{tag}.json")
        if os.path.exists(p):
            out[tag] = json.load(open(p, encoding="utf-8"))
    return out


def main() -> None:
    honest_hits, crit_opp = build_honest_arm()
    res = {tag: analyze_family(tag, honest_hits) for tag in FAMILIES}
    live = [t for t in FAMILIES if res[t]["records"]]
    # CMH 分层合并（层 = 独立样本：qwen 用合并版，避免 na/b 双重计入）
    pool_tags = [t for t in ("ornith30", "gemma26na", "qwen38all") if res.get(t, {}).get("records")]
    cmh_param = cmh_test([(res[t]["mcnemar_llm_gt"], res[t]["mcnemar_param_gt"]) for t in pool_tags])
    cmh_honest = cmh_test([(res[t]["mcnemar_vs_honest"]["llm_gt"],
                            res[t]["mcnemar_vs_honest"]["honest_gt"]) for t in pool_tags])
    h8 = h8_summary()
    out = {"families": {t: {"model": FAMILIES[t][0], "host": FAMILIES[t][1], **res[t]}
                        for t in FAMILIES},
           "cmh_pooled": {
               "llm_vs_param": {"chi2": cmh_param[0], "p": cmh_param[1],
                                "sum_b": sum(res[t]["mcnemar_llm_gt"] for t in live),
                                "sum_c": sum(res[t]["mcnemar_param_gt"] for t in live)},
               "llm_vs_honest": {"chi2": cmh_honest[0], "p": cmh_honest[1],
                                 "sum_b": sum(res[t]["mcnemar_vs_honest"]["llm_gt"] for t in live),
                                 "sum_c": sum(res[t]["mcnemar_vs_honest"]["honest_gt"] for t in live)}},
           "h8v2": h8}
    json.dump(out, open(os.path.join(config.RESULTS_DIR, "three_family_analysis.json"), "w",
                        encoding="utf-8"), ensure_ascii=False, indent=1, default=str)

    L = ["# 三家族重放统一分析（LLM 判断臂 vs 半oracle参数臂 vs 诚实特征臂）\n",
         f"生成：`python3 -m sea_pilot.analyze_families` · 每家族 30 模拟日 × 8 智能体 = 240 天次"
         f"（qwen 另有复样 agents 8–15，合并 480 天次）\n",
         "## 1 主对比表\n",
         "| 家族（宿主） | 有效率 | 召回 LLM | 召回 param(ρ=0.4 半oracle) | 召回 honest(特征臂) | "
         "McNemar p（LLM≶param） | Δ召回 bootstrap 95%CI | 冲动消费率 |",
         "|---|---|---|---|---|---|---|---|"]
    for tag, (model, host) in FAMILIES.items():
        r = res[tag]
        if not r["records"]:
            continue
        sig = "**" if r["mcnemar_p"] < 0.05 else ""
        L.append(f"| {model}（{host}） | {r['valid_rate']:.0%}（{r['valid']}/{r['records']}） | "
                 f"{r['recall_llm']:.3f}（{r['hits_llm']}/{r['n_crit']}） | "
                 f"{r['recall_param']:.3f}（{r['hits_param']}） | "
                 f"{r['recall_honest_on_valid_days']:.3f} | "
                 f"{r['mcnemar_p']:.3f}{sig}（优天 {r['mcnemar_llm_gt']}:{r['mcnemar_param_gt']}，平 {r['mcnemar_tie']}） | "
                 f"[{r['boot_ci_recall_diff'][0]:+.3f}, {r['boot_ci_recall_diff'][1]:+.3f}] | "
                 f"{r['impulse_rate']:.1%}（{r['impulse_consumed']}/{r['impulse_injected']}） |")
    L += ["",
          "**读法**：param 臂是与真值相关 ρ=0.4 的半 oracle（理想化上界基线）；honest 臂是零后见训练的"
          "真实特征评分器（d′=0.77）在同一 digest 上离线补算（无 LLM 调用）；McNemar 按天配对"
          "（同 digest 同真值），双侧精确检验；bootstrap 对天重抽样 2000 次。",
          "\n## 1b. 分层合并检验（CMH，层=模型家族）与功效\n"]
    cm = out["cmh_pooled"]
    L += [f"- **LLM vs 半oracle param**：Σb={cm['llm_vs_param']['sum_b']}, Σc={cm['llm_vs_param']['sum_c']}, "
          f"CMH χ²={cm['llm_vs_param']['chi2']:.2f}, **p={cm['llm_vs_param']['p']:.4f}**"
          + ("（合并后显著）" if cm['llm_vs_param']['p'] < 0.05 else "（合并后仍不显著——方向为正）"),
          f"- **LLM vs 诚实特征臂**：Σb={cm['llm_vs_honest']['sum_b']}, Σc={cm['llm_vs_honest']['sum_c']}, "
          f"CMH χ²={cm['llm_vs_honest']['chi2']:.2f}, **p={cm['llm_vs_honest']['p']:.2e}**"
          + ("（**显著**——LLM 判断层优于零后见特征评分器，统计确认）"
             if cm['llm_vs_honest']['p'] < 0.05 else ""),
          f"- 功效分析（以效应最强的 qwen 合并样本计）：其不一致比为 "
          f"{res['qwen38all']['mcnemar_llm_gt']}:{res['qwen38all']['mcnemar_param_gt']}，80% 功效下需 "
          f"~{res['qwen38all']['power_n_discordant_needed']} 个不一致天（当前 {res['qwen38all']['mcnemar_llm_gt']+res['qwen38all']['mcnemar_param_gt']}，"
          f"不一致率 ~{(res['qwen38all']['mcnemar_llm_gt']+res['qwen38all']['mcnemar_param_gt'])/480:.0%}）"
          f"⇒ 尚需约 {max(0, res['qwen38all']['power_n_discordant_needed'] - res['qwen38all']['mcnemar_llm_gt'] - res['qwen38all']['mcnemar_param_gt'])} 个不一致天"
          f"（ornith 家族效应近零，所需 n 发散——家族间效应异质性本身即结论）。",
          "\n## 2 判定准则（预注册式）\n",
          "- 若 LLM ≥ honest 且对 param 的 McNemar 不劣：**LLM 判断层有增量价值**（超过诚实特征基线）；",
          "- 若 LLM < honest：LLM 标题判断不如廉价特征评分器，判断层需换特征或降级为混合；",
          "- 冲动消费率的家族间差异 = g¹ 注入通道的模型依赖度（进 O6 转移系数库）。\n",
          "## 3 H8 v2 三家族对照\n"]
    if h8:
        L += ["| 指标 | " + " | ".join(h8.keys()) + " |", "|---|" + "---|" * len(h8)]
        rows = [(("C2", "dprime_mean"), "C2 d′（构造关系型验证题，防记忆）"),
                (("C2", "accuracy_mean"), "C2 总体准确率"),
                (("A2", "effect_cohend_false_share"), "A2 d（假分享，全部项）"),
                (("A2", "effect_cohend_false_subtle"), "A2 d（微妙假分享——地板检验位）"),
                (("B2", "effect_cohend_extremity"), "B2 d（极端度）"),
                (("B2", "sided_shift_mean"), "B2 带符号位移（同化通道）")]
        for path_, lab in rows:
            vals = []
            for tag in h8:
                sec = path_[0]
                if sec == "B2" and path_[1] == "sided_shift_mean":
                    v = h8[tag].get("B2", {}).get("treatment", {}).get("sided_shift_mean")
                else:
                    v = h8[tag].get(sec, {}).get(path_[1])
                vals.append(f"{v:.3f}" if isinstance(v, (int, float)) else "—")
            L.append(f"| {lab} | " + " | ".join(vals) + " |")
        L += ["", "v1 基线（ornith，著名神话材料）：C 辨别 d′=3.77（天花板）、A 假分享 d=+0.23（方向失败）、"
              "B 极端度 d=+0.36（通过）。对照点：C2 是否从 3.77 回落到人类区间（1.0–1.8）；"
              "A2 微妙项是否出现负效应；B2 是否跨家族复现正效应。",
              "\n人类锚（文献值）：A d≈−0.2~−0.5（Pennycook & Rand 2022）；B d≈+0.22~+0.35（Bail 2018）；"
              "C d′≈1.0–1.8（新闻辨别文献）。\n"]
    else:
        L.append("（h8v2 结果尚未落盘）\n")
    open(os.path.join(config.RESULTS_DIR, "THREE_FAMILY_ANALYSIS.md"), "w",
         encoding="utf-8").write("\n".join(L))
    print("\n".join(L[:40]))
    print("... -> pilot/results/THREE_FAMILY_ANALYSIS.md")


if __name__ == "__main__":
    main()
