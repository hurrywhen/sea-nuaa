"""监测清单构建的优化升级（任务 2）：定理 7.3 次模贪心 + 命题 8.1 Pandora 准入。

替代 top-N 启发式。全部估计只用前窗数据（零后见）。

定理 7.3 实例：max U(S) = Σ_e w_e·(1 − Π_{i∈S}(1−p_ie))，s.t. Σ_i supply_i ≤ quota
  - p_ie：实体 i 覆盖关键事件 e 的概率（前窗经验频率，二值覆盖矩阵）
  - 密度贪心（边际增益/供给成本），每步留审计痕迹（S4）
命题 8.1 实例：z_i 解 E[(X_i − z)^+] = c_i；准入当且仅当 z_i ≥ ν
  - X_i：实体月度关键产出（前窗估计，Poisson 抽样）
  - c_i：探索/维护成本（以供给槽位计）
  - ν：预算影子价格（取贪心轨迹的最后入选边际增益）
"""
from __future__ import annotations

import math
from collections import defaultdict

import numpy as np


# ---------------- 定理 7.3：预算约束下的最大概率覆盖贪心 ----------------

def build_coverage(prior_events: list[dict], entity_key: str = "insts",
                   value_key: str = "cit", critical_top: float = 0.02) -> dict:
    """从前窗语料估计覆盖结构。

    prior_events: 前窗论文记录（含 insts/authors、cit）
    返回 {entities: {e: supply(篇/月)}, events: [eid], w: {eid: 权重},
          M: {eid: set(entities)}}  —— M 为二值覆盖矩阵（稀疏表示）
    """
    n = len(prior_events)
    cits = sorted(e[value_key] for e in prior_events)
    thr = cits[min(n - 1, int((1 - critical_top) * n))] if n else 0
    crit = [e for e in prior_events if e[value_key] >= thr and e[value_key] > 0]
    months = 2.0  # 前窗 2019-07/08
    supply: dict[str, float] = defaultdict(float)
    for e in prior_events:
        for ent in e.get(entity_key, []):
            supply[ent] += 1.0 / months
    M = {}
    w = {}
    for j, e in enumerate(crit):
        M[j] = {ent for ent in e.get(entity_key, []) if ent}
        w[j] = math.log1p(e[value_key])
    return {"entities": dict(supply), "events": list(range(len(crit))), "w": w, "M": M}


def _utility(S: set[str], cov: dict) -> float:
    U = 0.0
    for j in cov["events"]:
        p_miss = 1.0
        for ent in cov["M"][j]:
            if ent in S:
                p_miss = 0.0  # 二值覆盖：清单含该实体即必达
                break
        U += cov["w"][j] * (1.0 - p_miss)
    return U


def greedy_watchlist(cov: dict, quota: float, max_size: int = 400) -> tuple[list[str], list[dict]]:
    """密度贪心（边际增益/供给成本），供给约束 Σ supply ≤ quota。返回（清单, 审计痕迹）。

    反向索引实现：cov_by_ent[ent] = 该实体覆盖的（尚未覆盖）关键事件集合。
    """
    S: set[str] = set()
    used = 0.0
    trace = []
    cur_u = 0.0
    cov_by_ent: dict[str, set[int]] = defaultdict(set)
    for j, ents in cov["M"].items():
        for ent in ents:
            if ent in cov["entities"]:
                cov_by_ent[ent].add(j)
    alive = {j for j, ents in cov_by_ent.items() if ents}
    while len(S) < max_size:
        best, best_gain, best_density = None, 0.0, 0.0
        for ent in alive:
            if ent in S:
                continue
            sup = cov["entities"].get(ent, 0.0)
            if sup <= 0 or used + sup > quota:
                continue
            gain = sum(cov["w"][j] for j in cov_by_ent[ent])
            dens = gain / sup
            if dens > best_density:
                best, best_gain, best_density = ent, gain, dens
        if best is None:
            break
        S.add(best)
        used += cov["entities"][best]
        cur_u += best_gain
        for j in list(cov_by_ent[best]):
            for e2 in cov["M"][j]:
                if e2 in cov_by_ent:
                    cov_by_ent[e2].discard(j)
        alive = {e for e, js in cov_by_ent.items() if js}
        trace.append({"step": len(trace), "entity": best,
                      "supply": cov["entities"][best], "marginal_gain": best_gain,
                      "density": best_density, "cum_utility": cur_u, "used_supply": used})
    return sorted(S), trace


# ---------------- 命题 8.1：Pandora 保留指数与准入 ----------------

def pandora_index(lam: float, c: float, n_samples: int = 400, seed: int = 7,
                  scale: float = 1.0, z_hi: float | None = None) -> float:
    """解 E[(X − z)^+] = c，X = scale·Poisson(lam)（蒙特卡洛 + 二分）。"""
    rng = np.random.default_rng(seed)
    X = rng.poisson(lam, size=n_samples).astype(float) * scale
    hi = z_hi if z_hi is not None else float(X.max() + lam + c + 1.0)
    lo = -1.0

    def f(z: float) -> float:
        return float(np.mean(np.maximum(X - z, 0.0))) - c

    if f(lo) < 0:   # 探索成本高于任何收益
        return lo
    if f(hi) > 0:
        return hi
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if f(mid) > 0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def pandora_admission(yields: dict[str, float], costs: dict[str, float], nu: float,
                      scale: float = 1.0, seed: int = 7) -> tuple[list[str], list[dict]]:
    """按保留指数降序探索；z ≥ ν 者准入。返回（准入清单按 z 降序, 全表）。"""
    table = []
    for ent, lam in yields.items():
        c = max(costs.get(ent, 0.0), 1e-9)
        z = pandora_index(lam, c, seed=seed, scale=scale)
        table.append({"entity": ent, "lambda_monthly_critical": lam, "cost_supply": c, "z": z})
    table.sort(key=lambda r: -r["z"])
    admitted = [r["entity"] for r in table if r["z"] >= nu]
    return admitted, table


def greedy_watchlist_prob(hits: dict[str, int], k_prior: int, supply: dict[str, float],
                          quota: float, w_total: float = 1.0,
                          max_size: int = 400) -> tuple[list[str], list[dict]]:
    """定理 7.3 的稳健（概率）形式：实体命中率 p_i = hits_i / k_prior（前窗关键事件的经验
    命中频率），未来关键事件的覆盖视为独立 Bernoulli(p_i)：
        U(S) = W·(1 − Π_{i∈S}(1 − p_i))
    密度贪心 + 供给配额 Σ supply ≤ quota。

    与二值集合覆盖版（greedy_watchlist）的区别：二值版把"覆盖了前窗特定事件"当作
    "会覆盖未来事件"，在稀疏数据上过拟合；概率版估计的是实体的**产率**，跨窗迁移更稳。
    """
    S: list[str] = []
    used = 0.0
    trace = []
    p_miss = 1.0  # Π(1−p_i)
    while len(S) < max_size:
        best, best_density, best_gain = None, 0.0, 0.0
        for ent, sup in supply.items():
            if ent in S or sup <= 0 or used + sup > quota:
                continue
            p = hits.get(ent, 0) / max(1, k_prior)
            if p <= 0:
                continue
            gain = w_total * p_miss * p
            dens = gain / sup
            if dens > best_density:
                best, best_density, best_gain = ent, dens, gain
        if best is None:
            break
        S.append(best)
        used += supply[best]
        p_miss *= (1.0 - hits.get(best, 0) / max(1, k_prior))
        trace.append({"step": len(S), "entity": best, "supply": supply[best],
                      "p_hit": hits.get(best, 0) / max(1, k_prior),
                      "marginal_gain": best_gain, "density": best_density,
                      "used_supply": used})
    return S, trace


def pandora_quota_list(yields: dict[str, float], supply: dict[str, float], nu: float,
                       quota: float, scale: float = 1.0, seed: int = 7) -> tuple[list[str], list[dict]]:
    """命题 8.1 的配额化：保留指数 z_e 解 E[(X−z)^+] = c_e（X = scale·Poisson(月度关键产出)，
    c_e = supply_e × ν = 维护该清单席位的槽位机会成本），按 z 降序填充至配额。"""
    table = []
    for ent, lam in yields.items():
        sup = supply.get(ent, 0.0)
        if lam <= 0 or sup <= 0:
            continue
        z = pandora_index(lam, sup * max(nu, 1e-9), seed=seed, scale=scale)
        table.append({"entity": ent, "lambda": lam, "supply": sup, "cost": sup * nu, "z": z})
    table.sort(key=lambda r: -r["z"])
    picked, used = [], 0.0
    for r in table:
        if used + r["supply"] > quota:
            continue
        picked.append(r["entity"])
        used += r["supply"]
    return picked, table


def shadow_price_nu(trace: list[dict]) -> float:
    """ν 的经验估计：贪心轨迹最后入选实体的边际增益/供给（边际槽位价值）。"""
    if not trace:
        return 0.0
    return trace[-1]["density"]
