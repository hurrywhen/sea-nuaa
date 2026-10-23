"""A3 EIG 查询规划器（定理 8.2：最优查询最大化单位成本期望信息增益；定理 5.1 价值分解）。

候选查询 q = (实体 e, 信源类 c)。零后见 walk-forward 估计：
    EIG(q) = p̂(crit|c,e,t)·V − κ·cost(c)
    p̂ = p̂_c(类基率, Laplace 向全局基率收缩) × recency(e) × entity_mult(e)
    recency(e) = 1/(1 + 0.5·Δdays)；entity_mult = clip(p̂_e/base, ≤3)
    cost(c) = 类均文档数（注意力成本代理）
估计饥饿由 A5 探索底线覆盖（Red Queen 教训：估计不更新 = 漂移失效）。
"""
from __future__ import annotations

from collections import defaultdict


class EIGPlanner:
    def __init__(self, classes: list[str], base_rate: float = 0.107,
                 kappa: float = 0.01, value: float = 1.0):
        self.base = base_rate
        self.kappa = kappa
        self.value = value
        self.classes = list(classes)
        self.class_stats = {c: [0.0, 0] for c in classes}       # [crit_hits, covered_events]
        self.cost_stats = {c: [0.0, 0] for c in classes}        # [docs, events]
        self.ent_stats: dict = defaultdict(lambda: [0, 0.0, None])  # [n_ev, n_crit, last_day]

    # ---- walk-forward 学习（只用已消费/已见事件） ----
    def update_day(self, day: int, day_events: list[dict]) -> None:
        for ev in day_events:
            st = self.ent_stats[ev["entity"]]
            st[0] += 1
            st[1] += float(ev["market_critical"])
            st[2] = day
            share = ev["n_docs"] / max(1, len(ev["classes"]))
            for c in ev["classes"]:
                if c in self.class_stats:
                    self.class_stats[c][1] += 1
                    self.class_stats[c][0] += float(ev["market_critical"])
                    self.cost_stats[c][0] += share
                    self.cost_stats[c][1] += 1

    # ---- 估计 ----
    def p_hat(self, entity: str, cls: str, day: int) -> float:
        hits, n = self.class_stats.get(cls, (0.0, 0))
        p_c = (hits + self.base * 2.0) / (n + 2.0)
        ne, ncrit, last = self.ent_stats[entity]
        rec = 1.0 if last is None else 1.0 / (1.0 + 0.5 * max(0, day - last))
        ent = ((ncrit + self.base * 2.0) / (ne + 2.0)) / max(self.base, 1e-9)
        return min(0.95, p_c * rec * min(ent, 3.0))

    def cost(self, cls: str) -> float:
        s, n = self.cost_stats.get(cls, (0.0, 0))
        return max(1.0, s / n) if n else 1.0

    def rank(self, day: int, candidates: list[tuple[str, str]]) -> list[dict]:
        """candidates: [(entity, class)]；返回按 EIG 降序的查询表。"""
        rows = []
        for (e, c) in candidates:
            p = self.p_hat(e, c, day)
            rows.append({"entity": e, "class": c, "p_hat": p, "cost": self.cost(c),
                         "eig": p * self.value - self.kappa * self.cost(c)})
        rows.sort(key=lambda r: (-r["eig"], r["entity"], r["class"]))
        return rows
