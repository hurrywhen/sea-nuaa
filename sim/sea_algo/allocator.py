"""A5 边际 VOI 预算分配器（定理 8.1 注意力无套利：名额跨通道边际价值相等）。

算法：
  1. rate_c = (近 window 日命中 + 先验·2)/(近 window 日名额 + 2)  ——收缩到先验表类 p̂_min；
  2. marginal(c, s) = rate_c · decay^s   ——几何边际递减（依据：清单内排序质量随深度
     衰减的实测瓶颈，滚动实验与 P2 同构）；
  3. 贪心逐名额 argmax marginal；
  4. 探索底线：每 explore_period 日每通道至少 1 名额（Red Queen：估计须持续更新；
     O1 极限环警告采纳×更新耦合）。
全部改派写 S4 审计日志。
"""
from __future__ import annotations


class MarginalVOIAllocator:
    def __init__(self, channels: list[str], m: int, prior: dict[str, float],
                 window: int = 7, decay: float = 0.8, explore_period: int = 3):
        self.channels = list(channels)
        self.m = m
        self.prior = dict(prior)
        self.window = window
        self.decay = decay
        self.explore_period = explore_period
        self.hist: dict[str, list[tuple[int, int]]] = {c: [] for c in channels}
        self.day = 0
        self.audit: list[dict] = []

    def rate(self, c: str) -> float:
        h = self.hist[c][-self.window:]
        if not h:
            return self.prior.get(c, 0.1)
        hits = sum(x[0] for x in h)
        slots = sum(x[1] for x in h)
        return (hits + self.prior.get(c, 0.1) * 2.0) / (slots + 2.0)

    def marginal(self, c: str, s: int) -> float:
        return self.rate(c) * (self.decay ** s)

    def allocate(self) -> dict[str, int]:
        alloc = {c: 0 for c in self.channels}
        explore = (self.day % self.explore_period == 0)
        if explore and self.m >= len(self.channels):
            for c in self.channels:
                alloc[c] = 1
        for _ in range(max(0, self.m - sum(alloc.values()))):
            c = max(self.channels, key=lambda x: (self.marginal(x, alloc[x]), x))
            alloc[c] += 1
        self.audit.append({"day": self.day, "alloc": dict(alloc), "explore": explore,
                           "rates": {c: round(self.rate(c), 4) for c in self.channels}})
        self.day += 1
        return alloc

    def update(self, day_report: dict[str, tuple[int, int]]) -> None:
        """day_report: {channel: (hits, slots_used)}。"""
        for c in self.channels:
            h, s = day_report.get(c, (0, 0))
            self.hist[c].append((int(h), int(s)))
