"""A6 次模清单构建（定理 7.3）+ A7 滚动清单管理器。

A6：覆盖函数次模 ⇒ 贪心 (1−1/e)≈0.632 保证；P12 证伪项监控（比值持续 <0.63 即告警）。
粒度教训（实测）：机构 0.231–0.269 ≫ 作者 0.02——粒度错误会摧毁 p̂_min。
A7：月度重建 + Jaccard 漂移监控（月换手实测 0.39）+ B 类快速审批（新实体试用期清单，
S2 签字标记）+ 剔除实体 30 天影子监测。滚动收益 = 覆盖上限而非即时召回（诚实负结果继承）。
"""
from __future__ import annotations

from itertools import combinations


def greedy_cover(cov: dict[str, set], k: int) -> tuple[list[str], set]:
    """懒贪心最大化覆盖（定理 7.3）。cov: 实体 -> 覆盖的命题集合。"""
    selected: list[str] = []
    covered: set = set()
    for _ in range(min(k, len(cov))):
        best, gain = None, 0
        for e, s in cov.items():
            if e in selected:
                continue
            g = len(s - covered)
            if g > gain:
                gain, best = g, e
        if best is None:
            break
        selected.append(best)
        covered |= cov[best]
    return selected, covered


def brute_force_optimal(cov: dict[str, set], k: int) -> int:
    """小实例穷举最优覆盖（审计用，验证贪心比值）。"""
    best = 0
    ents = list(cov)
    for comb in combinations(ents, min(k, len(ents))):
        u: set = set()
        for e in comb:
            u |= cov[e]
        best = max(best, len(u))
    return best


class RollingManager:
    """A7 滚动清单管理器。"""

    def __init__(self, k: int = 50, shadow_days: int = 30):
        self.k = k
        self.shadow_days = shadow_days
        self.current: list[str] | None = None
        self.shadow: dict[str, int] = {}    # 被剔除实体 -> 影子监测剩余天数
        self.history: list[dict] = []       # S4 审计：每次重建的 diff

    def rebuild(self, cov_window: dict[str, set], day: int = 0) -> dict:
        new, covered = greedy_cover(cov_window, self.k)
        old = self.current or []
        inter = set(new) & set(old)
        jaccard = len(inter) / max(1, len(set(new) | set(old)))
        added = sorted(set(new) - set(old))
        dropped = sorted(set(old) - set(new))
        for e in dropped:
            self.shadow[e] = self.shadow_days       # 影子监测防覆盖回归
        report = {"day": day, "jaccard": jaccard, "added": added, "dropped": dropped,
                  "b_class_fast_track": added,      # 新实体立即入试用期清单（低配额+S2 标记）
                  "coverage": len(covered), "shadow_watch": sorted(self.shadow)}
        self.current = new
        self.history.append(report)
        # 影子监测倒计时
        for e in list(self.shadow):
            self.shadow[e] -= 1
            if self.shadow[e] <= 0:
                del self.shadow[e]
        return report
