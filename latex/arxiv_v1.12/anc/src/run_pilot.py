"""阶段三试点主入口：P3 研究者画像 × arXiv 2019-09 重放 × H4'（双通道 vs 纯评分）。

实验因子：臂 (S0/S1/S2/S2c) × 清单构建法 (freq/cite，仅对 S2 有效) × ρ 扫描 × 预算档 × 30 智能体。

运行：cd sim && python3 -m sea_pilot.run_pilot
输出：sim/pilot/data/corpus_2019-09_ai.csv
      sim/pilot/results/pilot_rows.csv / pilot_agg.csv / pilot_summary.json
"""
from __future__ import annotations

import csv
import json
import math
import os

import numpy as np

from . import config, corpus as cp
from .metrics import aggregate, arm_metrics
from .scorer import make_scores, measure_dprime, theory_recall
from .strategies import select

ARMS = ("S0", "S1", "S2", "S2c")
WL_VARIANTS = ("freq", "cite", "inst", "inst10")


def main() -> None:
    os.makedirs(config.RESULTS_DIR, exist_ok=True)
    universe, critical, watchlists, stats = cp.build_all()
    n = len(universe)
    print(f"universe(P3 AI slice) N={n}, critical K*={len(critical)}, π={stats['pi_critical_frac']:.4f}")
    for k, v in stats["watchlists"].items():
        print(f"  WL-{k}: size={v['size']}, 覆盖关键命题 {v['critical_covered_n']}/{stats['critical_n']}"
              f" (p̂_min={v['p_min_hat_coverage_of_critical']:.3f}), 清单内论文 {v['papers_in_universe']}")

    cp.export_corpus_csv(universe, critical, watchlists,
                         os.path.join(config.DATA_DIR, "corpus_2019-09_ai.csv"))

    ids = np.array([r["arxiv_id"] for r in universe])
    crit_mask = np.isin(ids, list(critical))
    value = np.array([math.log1p(r["cit"]) for r in universe])
    order = np.lexsort((ids, np.array([cp.day_index(r) for r in universe])))
    wl_masks = {k: np.array([cp.wl_covered(r, wl) for r in universe])
                for k, wl in watchlists.items()}

    rows: list[dict] = []
    theory_checks: list[dict] = []
    for ri, rho in enumerate(config.RHO_SWEEP):
        for ai in range(config.N_AGENTS):
            m = config.BUDGETS_PER_DAY[ai % len(config.BUDGETS_PER_DAY)]
            budget = m * config.SIM_DAYS
            sc = make_scores(universe, rho, seed=config.SEED + 1000 * ri + ai,
                             hype_align=config.HYPE_ALIGN)
            dprime = measure_dprime(sc["proxy"], crit_mask)
            beta = budget / n
            pi = float(crit_mask.mean())
            pred = theory_recall(beta, pi, dprime)
            for arm in ARMS:
                variants = WL_VARIANTS if arm == "S2" else ("na",)
                for wlv in variants:
                    wl_mask = wl_masks.get(wlv, np.zeros(n, dtype=bool))
                    selected, info = select(arm, budget, order=order, hype=sc["hype"],
                                            proxy=sc["proxy"], wl_mask=wl_mask)
                    met = arm_metrics(selected, critical=crit_mask, value=value, wl_mask=wl_mask,
                                      budget=budget, info=info,
                                      dprime=dprime if arm == "S2c" else None,
                                      theory_pred=pred if arm == "S2c" else None)
                    rows.append({"arm": arm, "wl": wlv, "rho": rho, "agent": ai,
                                 "budget_per_day": m, "budget": budget, **met})
                    if arm == "S2c":
                        theory_checks.append({"rho": rho, "budget_per_day": m, "beta": beta,
                                              "pi": pi, "dprime": dprime,
                                              "pred": pred, "realized": met["recall"]})

    _write_csv(os.path.join(config.RESULTS_DIR, "pilot_rows.csv"), rows)
    agg = aggregate(rows, keys=["arm", "wl", "rho", "budget_per_day"])
    _write_csv(os.path.join(config.RESULTS_DIR, "pilot_agg.csv"), agg)

    tc = np.array([[t["pred"], t["realized"]] for t in theory_checks])
    ident_mae = float(np.abs(tc[:, 0] - tc[:, 1]).mean())
    ident_r = float(np.corrcoef(tc[:, 0], tc[:, 1])[0, 1]) if len(tc) > 2 else float("nan")
    bound_ok = all(r["distortion_bound_ok"] for r in rows)
    cap_ok = all((r["recall"] <= min(1.0, r["cap_beta_over_pi"]) + 1e-9) for r in rows)

    def _mean(arm: str, key: str, rho: float = 0.4, wl: str | None = None) -> float:
        v = [r[key] for r in rows if r["arm"] == arm and r["rho"] == rho
             and (wl is None or r["wl"] == wl)]
        return float(np.mean(v)) if v else float("nan")

    h4 = {}
    base = {"S2c": _mean("S2c", "recall"), "S1": _mean("S1", "recall"), "S0": _mean("S0", "recall")}
    for wlv in WL_VARIANTS:
        h4[f"S2[{wlv}]"] = _mean("S2", "recall", wl=wlv)
        h4[f"S2[{wlv}]_wl_covered_part"] = _mean("S2", "recall_wl_covered", wl=wlv)
        h4[f"S2[{wlv}]_not_wl_part"] = _mean("S2", "recall_not_wl", wl=wlv)
        h4[f"gap_S2[{wlv}]_minus_S2c"] = h4[f"S2[{wlv}]"] - base["S2c"]
    h4.update(base)

    summary = {
        "corpus_stats": stats,
        "config": {
            "n_agents": config.N_AGENTS, "arms": list(ARMS), "wl_variants": list(WL_VARIANTS),
            "rho_sweep": list(config.RHO_SWEEP), "budgets_per_day": list(config.BUDGETS_PER_DAY),
            "sim_days": config.SIM_DAYS, "critical_quantile": config.CRITICAL_QUANTILE,
            "watchlist_size": config.WATCHLIST_SIZE,
            "replay_month": list(config.REPLAY_MONTH), "prior_window": list(config.PRIOR_WINDOW),
            "seed": config.SEED,
        },
        "theory_checks": {
            "P3_gaussian_identity_mae": ident_mae,
            "P3_gaussian_identity_corr": ident_r,
            "P2_distortion_bound_holds_all_runs": bound_ok,
            "theorem61_ii_cap_holds_all_runs": cap_ok,
            "dprime_by_rho_agent0": {str(rho): measure_dprime(
                make_scores(universe, rho, seed=config.SEED + 1000 * ri,
                            hype_align=config.HYPE_ALIGN)["proxy"], crit_mask)
                for ri, rho in enumerate(config.RHO_SWEEP)},
            "capacity_cap_by_budget": {str(m): min(1.0, (m * config.SIM_DAYS / n)
                                                    / stats["pi_critical_frac"])
                                       for m in config.BUDGETS_PER_DAY},
        },
        "H4prime_headline_rho0.4": h4,
        "budget_alarms_S2": {wlv: sum(r["alarm_budget_conflict"] for r in rows
                                      if r["arm"] == "S2" and r["wl"] == wlv)
                             for wlv in WL_VARIANTS},
    }
    json.dump(summary, open(os.path.join(config.RESULTS_DIR, "pilot_summary.json"), "w",
                            encoding="utf-8"), ensure_ascii=False, indent=1)

    print("\n===== H4' headline（ρ=0.4，全预算档平均）=====")
    for k in ("S0", "S1", "S2c", "S2[freq]", "S2[cite]", "S2[inst]", "S2[inst10]"):
        print(f"  {k:12s} recall = {h4[k]:.3f}")
    for wlv in WL_VARIANTS:
        print(f"  架构增益 S2[{wlv}]−S2c = {h4[f'gap_S2[{wlv}]_minus_S2c']:+.3f}")
    print(f"\n定理6.1恒等式（S2c 实测 vs 理论）: MAE={ident_mae:.4f}, corr={ident_r:.4f}")
    print(f"命题6.2失真下界全部成立: {bound_ok}; 定理6.1(ii)容量上限全部成立: {cap_ok}")
    print(f"S2 预算冲突报警（命题6.3）: {summary['budget_alarms_S2']}")
    print("done ->", config.RESULTS_DIR)


def _write_csv(path: str, rows: list[dict]) -> None:
    if not rows:
        return
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    main()
