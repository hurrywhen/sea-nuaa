"""评分器与理论预言（定理 6.1 的数值实现）。

诚实性约定（论文 §6.2）：评分器不接触关键性标签，只观测"可预测重要性的含噪代理特征"
    proxy = ρ·z(log1p(cit)) + √(1−ρ²)·N(0,1)
ρ 扫描代表不同质量的特征工程；**实测 d′ 由数据算出**，再代入定理 6.1 恒等式产生
预言召回，与仿真实现值对照（可证伪命题 P3）。
"""
from __future__ import annotations

import math

import numpy as np


def norm_sf(x: float) -> float:
    """标准正态尾函数 Φ̄(x)（无 scipy 依赖）。"""
    return 0.5 * math.erfc(x / math.sqrt(2.0))


def norm_ppf_upper(p: float) -> float:
    """Φ̄⁻¹(p)：二分法（p∈(0,1)）。"""
    if p <= 0:
        return 10.0
    if p >= 1:
        return -10.0
    lo, hi = -10.0, 10.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if norm_sf(mid) > p:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def make_scores(universe: list[dict], rho: float, seed: int, hype_align: float) -> dict[str, np.ndarray]:
    """返回 proxy（通道 II 评分）与 hype（S1 参与优化评分），按 universe 顺序对齐。"""
    rng = np.random.default_rng(seed)
    n = len(universe)
    zi = _z(np.array([math.log1p(r["cit"]) for r in universe]))
    proxy = rho * zi + math.sqrt(max(0.0, 1 - rho ** 2)) * rng.standard_normal(n)
    hype = hype_align * zi + math.sqrt(max(0.0, 1 - hype_align ** 2)) * rng.standard_normal(n)
    return {"proxy": proxy, "hype": hype, "zi": zi}


def _z(x: np.ndarray) -> np.ndarray:
    s = x.std()
    return (x - x.mean()) / s if s > 0 else x * 0.0


def measure_dprime(scores: np.ndarray, critical_mask: np.ndarray) -> float:
    """实测分离度 d′ = (μ₁−μ₀)/σ_pooled（等方差假设下的高斯模型，定理 6.1 设定）。"""
    a, b = scores[critical_mask], scores[~critical_mask]
    if len(a) < 2 or len(b) < 2:
        return 0.0
    sp = math.sqrt(((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / (len(a) + len(b) - 2))
    return float((a.mean() - b.mean()) / sp) if sp > 0 else 0.0


def theory_recall(beta: float, pi: float, dprime: float) -> float:
    """定理 6.1(i)：混合尾方程 (1−π)Φ̄(z) + πΦ̄(z−d′) = β 的召回解 R = Φ̄(z−d′)。

    β 单调 ⇒ 二分求 z；β < π·R 的不可行域由容量上限 β/π 截断（定理 6.1(ii)）。
    """
    if beta <= 0:
        return 0.0
    cap = min(1.0, beta / pi) if pi > 0 else 0.0

    def tail_mass(z: float) -> float:
        return (1 - pi) * norm_sf(z) + pi * norm_sf(z - dprime)

    lo, hi = -10.0, 10.0  # tail_mass 关于 z 递减
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if tail_mass(mid) > beta:
            lo = mid
        else:
            hi = mid
    z = 0.5 * (lo + hi)
    return float(min(cap, norm_sf(z - dprime)))


def required_dprime(beta: float, pi: float, target_r: float) -> float | None:
    """定理 6.1(iii)：目标召回所需分离度；β < πR 时不可行返回 None。"""
    if beta < pi * target_r:
        return None
    return norm_ppf_upper((beta - pi * target_r) / (1 - pi)) + (-norm_ppf_upper(target_r))
