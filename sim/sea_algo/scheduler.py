"""A4 Pandora/Whittle 调度器（命题 8.1 Pandora 配额；§8.6 Whittle 指数；定理 8.1 影子价格）。

两点分布（收益 V·Bernoulli(p̂)，开箱成本 c）的 Weitzman 保留值：
    z = V − c/p̂        （由 p̂(V−z) = c 解出）
准入规则 z ≥ ν 等价于校准阈值  p̂ ≥ c/(V−ν)  ——指数策略退化为阈值策略，
这正是注意力无套利定理（定理 8.1）的算法面：跨通道套利被同一影子价格 ν 禁止。
p̂ 按（family × 首类）walk-forward 估计，Laplace 向全局基率收缩。未用完名额交还 A5。
"""
from __future__ import annotations

from collections import defaultdict


def weitzman_bernoulli(p: float, c: float, v: float = 10.0) -> float:
    """两点分布 Weitzman 保留值 z = V − c/p（p>0）；p=0 时 z=−∞ 以 0 截断表示不开箱。"""
    if p <= 0:
        return 0.0
    return max(0.0, v - c / p)


def admission_threshold(c: float, v: float, nu: float) -> float:
    """准入 z≥ν 的等价概率阈值 p̂ ≥ c/(V−ν)（ν<V）。"""
    if nu >= v:
        return 1.1      # 影子价格过高：不开任何箱
    return c / (v - nu)


class PandoraScheduler:
    def __init__(self, base: float = 0.107, c: float = 1.0, v: float = 10.0):
        self.base = base
        self.c = c
        self.v = v
        self.stats: dict = defaultdict(lambda: [0.0, 0])   # (family, cls) -> [hits, n]

    def key(self, prop: dict) -> tuple:
        cls = prop["classes"][0] if prop.get("classes") else "other"
        return (prop.get("family", "other"), cls)

    def p_hat(self, prop: dict) -> float:
        h, n = self.stats[self.key(prop)]
        return (h + self.base * 4.0) / (n + 4.0)

    def update(self, prop: dict, hit: bool) -> None:
        st = self.stats[self.key(prop)]
        st[0] += float(hit)
        st[1] += 1

    def order(self, props: list[dict]) -> list[dict]:
        """按保留值降序（等价于 p̂ 降序——单调变换），附 z 与 p̂。"""
        rows = [{"prop": p, "p_hat": self.p_hat(p),
                 "z": weitzman_bernoulli(self.p_hat(p), self.c, self.v)} for p in props]
        rows.sort(key=lambda r: (-r["z"], str(r["prop"].get("pid", ""))))
        return rows

    def admit(self, props: list[dict], nu: float) -> list[dict]:
        """准入制选择：仅保留 z≥ν 的项（未用完名额由调用方交还 A5）。"""
        thr = admission_threshold(self.c, self.v, nu)
        return [r for r in self.order(props) if r["p_hat"] >= thr]
