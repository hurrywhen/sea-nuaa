"""P3 升级实验（任务 2 + 任务 4 合并验证）：
  (a) 清单构建：top-N 引用启发式 vs 定理 7.3 次模贪心（供给配额约束）vs 命题 8.1 Pandora 准入
  (b) 评分器：参数 proxy（ρ=0.4）vs 真实特征评分器（features.py，零后见训练）→ 实测真实 d′

运行：cd sim && python3 -m sea_pilot.run_p3up
输出：pilot/results/p3up_results.json / p3up_report.md
"""
from __future__ import annotations

import json
import math
import os
from collections import defaultdict

import numpy as np

from . import config, corpus as cp
from . import features as ft
from . import watchlist_opt as wo
from .metrics import arm_metrics
from .scorer import measure_dprime
from .strategies import select


def main() -> None:
    os.makedirs(config.RESULTS_DIR, exist_ok=True)
    universe, critical, wls, stats = cp.build_all()
    n = len(universe)
    prior_all = cp.load_raw(os.path.join(config.RAW_DIR, "arxiv_2019-07_08.jsonl"))
    prior = cp.ai_slice(prior_all)
    print(f"[p3up] universe={n}, prior={len(prior)}, critical={len(critical)}")

    ids = np.array([r["arxiv_id"] for r in universe])
    crit_mask = np.isin(ids, list(critical))
    value = np.array([math.log1p(r["cit"]) for r in universe])
    order = np.lexsort((ids, np.array([cp.day_index(r) for r in universe])))

    # ---------- (b) 真实特征评分器：前窗训练 → 九月应用（零后见） ----------
    vocab = ft.build_vocab([prior, universe])
    auth_p, inst_p = ft.prestige_maps(prior)
    prior_order = np.lexsort((np.array([r["arxiv_id"] for r in prior]),
                              np.array([r["date"] for r in prior])))
    Xp = ft.build_feature_matrix(prior, vocab, auth_p, inst_p, prior_order, loo=True)
    pcits = np.array([r["cit"] for r in prior], float)
    thr = np.quantile(pcits, 0.98)
    yp = (pcits >= max(thr, 1)).astype(float)
    w_l, b_l = ft.logistic_fit(Xp, yp)
    sept_order = order
    Xs = ft.build_feature_matrix(universe, vocab, auth_p, inst_p, sept_order, loo=False)
    real_scores = Xs @ w_l + b_l
    d_real = measure_dprime(real_scores, crit_mask)
    # 参数 proxy 对照（ρ=0.4）
    rng = np.random.default_rng(config.SEED)
    zi = (np.log1p([r["cit"] for r in universe]) - np.mean(np.log1p([r["cit"] for r in universe])))
    zi = zi / (zi.std() + 1e-9)
    proxy = 0.4 * zi + math.sqrt(1 - 0.16) * rng.standard_normal(n)
    d_proxy = measure_dprime(proxy, crit_mask)
    print(f"[p3up] 实测 d′: 真实特征={d_real:.2f}, 参数proxy(ρ=0.4)={d_proxy:.2f} "
          f"(95%召回需求线=4.39)")

    # ---------- (a) 清单构建多法对比（配额 = 0.6·m·30，逐预算档） ----------
    cov = wo.build_coverage(prior, entity_key="insts", value_key="cit", critical_top=0.02)
    supply_m = cov["entities"]                      # 机构供给（篇/月，前窗）
    k_prior = len(cov["events"])                    # 前窗关键事件数
    hits = defaultdict(int)                         # 机构对前窗关键事件的命中数
    pcits_sorted = np.sort(pcits)
    pthr = pcits_sorted[min(len(pcits_sorted) - 1, int(0.98 * len(pcits_sorted)))]
    inst_crit_count = defaultdict(float)
    for r in prior:
        is_c = r["cit"] >= pthr and r["cit"] > 0
        if is_c:
            for e in set(r["insts"]):
                hits[e] += 1
                inst_crit_count[e] += 1.0 / 2.0     # 月度产率
    wbar = float(np.mean([math.log1p(r["cit"]) for r in prior
                          if r["cit"] >= pthr and r["cit"] > 0]) or 1.0)

    results = {"d_prime_real_features": d_real, "d_prime_proxy_rho0.4": d_proxy,
               "d_prime_required_for_95pct": 4.39, "budgets": {}}
    idx_by_score = np.argsort(-real_scores)

    for m in config.BUDGETS_PER_DAY:
        quota = config.CHANNEL1_QUOTA * m * config.SIM_DAYS  # 月配额（篇）
        budget = m * config.SIM_DAYS
        # ν̂：边际消费价值 = 评分排序第 B 位的价值（影子价格的直接估计）
        nu_hat = float(value[idx_by_score[min(budget, n - 1)]])
        greedy_bin, trace_bin = wo.greedy_watchlist(cov, quota=quota)
        greedy_prob, trace_prob = wo.greedy_watchlist_prob(hits, k_prior, supply_m, quota)
        pandora_list, ptable = wo.pandora_quota_list(dict(inst_crit_count), supply_m,
                                                     nu_hat, quota, scale=wbar)
        lists = [
            ("topN-cite(50)", "author", wls["cite"]["ids"]),
            ("topN-inst(50)", "inst", wls["inst"]["ids"]),
            ("greedy-setcover", "inst", set(greedy_bin)),
 ("greedy-prob", "inst", set(greedy_prob)),
            ("pandora-quota", "inst", set(pandora_list)),
        ]
        rows = {}
        for lname, kind, idset in lists:
            wl_mask = np.array([any(e in idset for e in (r["insts"] if kind == "inst" else r["authors"]))
                                for r in universe])
            sel, info = select("S2", budget, order=order, hype=np.zeros(n),
                               proxy=real_scores, wl_mask=wl_mask)
            met = arm_metrics(sel, critical=crit_mask, value=value, wl_mask=wl_mask,
                              budget=budget, info=info)
            p_min_hat = float((wl_mask & crit_mask).sum() / max(1, crit_mask.sum()))
            rows[lname] = {"list_size": len(idset), "supply_per_day": float(wl_mask.sum()) / config.SIM_DAYS,
                           "p_min_hat": p_min_hat, "recall": met["recall"],
                           "recall_wl_covered": met["recall_wl_covered"],
                           "alarm": met["alarm_budget_conflict"]}
        # S2c 对照（纯真实特征评分）
        sel, info = select("S2c", budget, order=order, hype=np.zeros(n),
                           proxy=real_scores, wl_mask=np.zeros(n, bool))
        met = arm_metrics(sel, critical=crit_mask, value=value,
                          wl_mask=np.zeros(n, bool), budget=budget, info=info)
        rows["S2c(realfeat,无清单)"] = {"list_size": 0, "supply_per_day": 0.0,
                                        "p_min_hat": 0.0, "recall": met["recall"],
                                        "recall_wl_covered": float("nan"), "alarm": False}
        results["budgets"][str(m)] = {"quota_channel1": quota, "nu_hat": nu_hat, "arms": rows}
        print(f"[p3up] m={m} (ν̂={nu_hat:.2f}): " + " | ".join(
            f"{k}: p̂={v['p_min_hat']:.2f} R={v['recall']:.3f}" for k, v in rows.items()))

    json.dump(results, open(os.path.join(config.RESULTS_DIR, "p3up_results.json"), "w",
                            encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    _write_md(results)
    print("[p3up] done ->", os.path.join(config.RESULTS_DIR, "p3up_report.md"))


def _write_md(res: dict) -> None:
    L = ["# P3 升级实验：清单构建优化（定理 7.3 / 命题 8.1）× 真实特征评分器（任务 2+4）\n"]
    L.append(f"- **实测真实 d′（元数据+标题 TF-IDF 新颖度，零后见训练）= {res['d_prime_real_features']:.2f}**"
             f"（参数 proxy ρ=0.4 对照 = {res['d_prime_proxy_rho0.4']:.2f}；"
             f"95% 召回需求线 = 4.39）→ 定理 6.1 瓶颈在真实特征下的位置\n")
    L.append("| m(篇/日) | 清单构建法 | 规模 | 供给(篇/日) | p̂_min | 总召回 | 覆盖段召回 | 报警 |")
    L.append("|---|---|---|---|---|---|---|---|")
    for m, blk in res["budgets"].items():
        for lname, v in blk["arms"].items():
            L.append(f"| {m} | {lname} | {v['list_size']} | {v['supply_per_day']:.1f} | "
                     f"{v['p_min_hat']:.3f} | {v['recall']:.3f} | "
                     f"{v['recall_wl_covered'] if isinstance(v['recall_wl_covered'], str) else format(v['recall_wl_covered'], '.3f')} | "
                     f"{'⚠' if v['alarm'] else ''} |")
    L.append("\n注：通道 II 统一用真实特征评分器（清单构建法是唯一变量）；贪心清单受通道 I 配额 "
             "quota=0.6·m·30 约束（定理 7.3 的背包形式）；Pandora 准入按 z≥ν（ν=贪心末位密度）。")
    open(os.path.join(config.RESULTS_DIR, "p3up_report.md"), "w", encoding="utf-8").write("\n".join(L))


if __name__ == "__main__":
    main()
