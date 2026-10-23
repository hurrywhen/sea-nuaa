"""A8 抗俘获认证统计量（引理 12.1 修正 + 开放问题 O7 的首个工程实现）。

背景：P2 认证反转——新闻层扩至 10 域后，原始类覆盖计数（k_c=2）的精确率跌破基率
（lift 0.63×）：多类覆盖俘获的是高注意力公司而非高关键性事件。
重设计：质量加权的惊讶度覆盖  s(e) = Σ_c w_c · (1 − r̂_c(entity))
  - w_c 按实测 p̂_min 序（regulator 1.00 > wire 0.25 > fin 0.15 > tech 0.04）；
    aggregator 权重 0（不计入认证——转载机器不产生独立性）；
  - r̂_c(t) = 实体 t 历史事件被类 c 覆盖的 walk-forward 比率（Laplace 0.5/1）：
    注意力磁石 r̂→1 ⇒ 贡献归零；沉默实体突发高权重覆盖 ⇒ 强认证信号。
对抗自稳定：刷覆盖须同时刷高 w 类且维持低 r̂，成本随历史长度上升；
协同刷抬高全体基线 ⇒ 折扣自动生效（完整博弈分析留 O7 论文项）。
治理不变：θ 是公开参数，§12.1(a) "策展权被单参数吸收" 不受影响；
定理 12.1 的 Ω 下界与认证质量无关，不受影响。
"""
from __future__ import annotations

from collections import defaultdict

CLASS_WEIGHTS = {"regulator": 1.0, "wire": 0.9, "fin_media": 0.6, "tech_media": 0.6,
                 "general": 0.3, "other": 0.2, "aggregator": 0.0}


def certify_scores(events: list[dict], method: str = "scarcity") -> list[float]:
    """对事件列表计算认证分数。events 须按日期排序（walk-forward 前提）。

    method: "raw"（原始类计数，已冻结——仅作对照）| "quality"（仅质量加权）
            | "scarcity"（质量加权 × 惊讶度折扣，推荐）。
    """
    base_n: dict = defaultdict(int)     # entity -> 历史事件数
    base_c: dict = defaultdict(int)     # (entity, class) -> 历史覆盖数
    out = []
    for e in events:                    # 调用方保证已按 (date, entity) 排序
        t = e["entity"]
        if method == "raw":
            s = float(len(e["classes"]))
        elif method == "quality":
            s = sum(CLASS_WEIGHTS.get(c, 0.2) for c in e["classes"])
        elif method == "scarcity":
            n_t = base_n[t]
            s = 0.0
            for c in e["classes"]:
                r = (base_c[(t, c)] + 0.5) / (n_t + 1.0)   # Laplace；冷启动 r=0.5 中性
                s += CLASS_WEIGHTS.get(c, 0.2) * (1.0 - r)
        else:
            raise ValueError(method)
        out.append(s)
        # 更新 walk-forward 基线（用当日事件全体——正常消费即可见，零后见）
        base_n[t] += 1
        for c in e["classes"]:
            base_c[(t, c)] += 1
    return out


def precision_at_frac(events: list[dict], scores: list[float], target_frac: float,
                      crit_key: str = "market_critical") -> dict:
    """在与目标覆盖率匹配的分数阈值下测精确率/lift/关键召回。"""
    n = len(events)
    k = max(1, int(round(target_frac * n)))
    idx = sorted(range(n), key=lambda i: (-scores[i], i))[:k]
    n_crit = sum(bool(e[crit_key]) for e in events)
    base = n_crit / n
    hits = sum(bool(events[i][crit_key]) for i in idx)
    return {"certified": k, "certified_frac": k / n, "precision": hits / k,
            "base_rate": base, "lift": (hits / k) / base if base > 0 else float("nan"),
            "recall_of_critical": hits / max(1, n_crit)}
