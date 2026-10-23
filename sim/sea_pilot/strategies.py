"""对照策略（论文 §14.3 的试点子集）：S0 / S1 / S2 / S2c。

S0  原始流：按到达顺序消费至预算耗尽
S1  参与优化：按 hype 排序取 top-B（平台基线，g¹ 代理）
S2  完整 SEA（试点版双通道，定义 6.2）：
      通道 I  监测清单直通（假设 R3）：清单覆盖论文按 proxy 排序优先占额；
              若通道 I 已耗尽预算 → 触发命题 6.3 可行性报警（记录 alarm）
      通道 II 评分发现：剩余名额按 proxy top 填充
S2c 纯评分消融：只走通道 II（检验定理 6.1 瓶颈：召回应贴近理论恒等式且受 β/π 上限压制）
"""
from __future__ import annotations

import numpy as np

from . import config


def _topk(scores: np.ndarray, k: int, eligible: np.ndarray | None = None) -> np.ndarray:
    """返回得分 top-k 的索引（eligible 掩码限定候选）。稳定确定性：并列按索引升序。"""
    if eligible is not None:
        idx = np.flatnonzero(eligible)
    else:
        idx = np.arange(len(scores))
    if len(idx) == 0 or k <= 0:
        return idx[:0]
    order = idx[np.lexsort((idx, -scores[idx]))]
    return order[:k]


def select(arm: str, budget: int, *, order: np.ndarray, hype: np.ndarray,
           proxy: np.ndarray, wl_mask: np.ndarray) -> tuple[np.ndarray, dict]:
    info: dict = {"alarm_budget_conflict": False}
    if budget <= 0:
        return np.array([], dtype=int), info
    if arm == "S0":
        return order[:budget], info
    if arm == "S1":
        return _topk(hype, budget), info
    if arm == "S2c":
        return _topk(proxy, budget), info
    if arm == "S2":
        import math as _m
        ch1_cap = max(1, _m.ceil(config.CHANNEL1_QUOTA * budget))   # 通道 I 配额上限
        ch1 = _topk(proxy, ch1_cap, eligible=wl_mask)               # 清单直通（proxy 定序）
        taken = np.zeros(len(proxy), dtype=bool)
        taken[ch1] = True
        if len(ch1) >= ch1_cap and wl_mask.sum() > ch1_cap:
            info["alarm_budget_conflict"] = True                    # 命题 6.3：清单供给超配额
        rest = budget - len(ch1)
        ch2 = _topk(proxy, rest, eligible=~taken) if rest > 0 else np.array([], dtype=int)
        return np.concatenate([ch1, ch2]), info
    raise ValueError(f"unknown arm {arm}")
