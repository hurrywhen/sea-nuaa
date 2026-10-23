"""A10 校准层 θ_cal（§15.3 H9 转移桥；命题 10.2 测量完整性）。

组件：
  ThetaCalTracker —— 滚动窗 Brier/ECE + 漂移报警（连续两窗 ECE>0.25 ⇒ 降级自动权重）；
  Recalibrator   —— PAVA 等渗回归（保单调——H9 条款"允许系统偏移，须单调可校正"的算法兑现）；
  FAMILY_POLICY  —— 家族初始化策略查表（先验表 v0.1 H9 行：ornith 0.170 / qwen 0.231 /
                    gemma 0.279 差于常数基线 ⇒ 强制重校准 + 置信上限）。
主权约束（命题 10.2）：人类侧 θ_cal 不可由机器代做——AI 队列锚点是转移桥，不是替代。
"""
from __future__ import annotations

from collections import deque

import numpy as np

FAMILY_POLICY = {
    "reasoning": {"brier_ref": 0.170, "policy": "直接使用（超级预测者带内）", "cap": 0.99},
    "qwen38":    {"brier_ref": 0.231, "policy": "轻校准（等渗映射后使用）", "cap": 0.95},
    "gemma":     {"brier_ref": 0.279, "policy": "强制重校准 + 置信上限（差于常数基线）", "cap": 0.90},
}


def brier(pairs: list[tuple[float, int]]) -> float:
    return float(np.mean([(p - y) ** 2 for p, y in pairs])) if pairs else float("nan")


def ece(pairs: list[tuple[float, int]], bins: int = 10) -> float:
    if not pairs:
        return float("nan")
    p = np.array([x[0] for x in pairs])
    y = np.array([x[1] for x in pairs], dtype=float)
    edges = np.linspace(0, 1, bins + 1)
    e = 0.0
    for i in range(bins):
        sel = (p >= edges[i]) & (p < edges[i + 1] if i < bins - 1 else p <= 1.0)
        if sel.sum():
            e += abs(p[sel].mean() - y[sel].mean()) * sel.sum() / len(p)
    return float(e)


def pava(y: np.ndarray) -> np.ndarray:
    """Pool Adjacent Violators：等渗回归（最小二乘投影到单调锥）。"""
    y = np.asarray(y, dtype=float)
    vals = list(y)
    wts = [1.0] * len(y)
    idx_groups = [[i] for i in range(len(y))]
    i = 0
    while i < len(vals) - 1:
        if vals[i] > vals[i + 1] + 1e-12:
            nv = (vals[i] * wts[i] + vals[i + 1] * wts[i + 1]) / (wts[i] + wts[i + 1])
            vals[i:i + 2] = [nv]
            wts[i:i + 2] = [wts[i] + wts[i + 1]]
            idx_groups[i:i + 2] = [idx_groups[i] + idx_groups[i + 1]]
            i = max(0, i - 1)
        else:
            i += 1
    out = np.empty(len(y))
    for v, g in zip(vals, idx_groups):
        for j in g:
            out[j] = v
    return out


class Recalibrator:
    """等渗重校准（保单调可校正——H9 判定条款）。"""

    def __init__(self):
        self.xs: np.ndarray | None = None     # 块代表预测值（升序）
        self.ys: np.ndarray | None = None     # 块校准水平

    def fit(self, pairs: list[tuple[float, int]]) -> "Recalibrator":
        order = np.argsort([p for p, _ in pairs])
        p = np.array([pairs[i][0] for i in order])
        y = np.array([pairs[i][1] for i in order], dtype=float)
        fitted = pava(y)
        # 块代表点：同值块取 (p 均值, fitted 水平)
        xs, ys = [], []
        i = 0
        while i < len(fitted):
            j = i
            while j + 1 < len(fitted) and fitted[j + 1] == fitted[i]:
                j += 1
            xs.append(p[i:j + 1].mean())
            ys.append(fitted[i])
            i = j + 1
        self.xs, self.ys = np.array(xs), np.array(ys)
        return self

    def apply(self, p: float) -> float:
        if self.xs is None:
            return p
        return float(np.clip(np.interp(p, self.xs, self.ys), 0.01, 0.99))


class ThetaCalTracker:
    """滚动窗校准追踪 + 漂移报警。"""

    def __init__(self, window: int = 30, alarm_ece: float = 0.25):
        self.buf: deque = deque(maxlen=window)
        self.alarm_ece = alarm_ece
        self.consecutive_alarm = 0
        self.history: list[dict] = []

    def update(self, p: float, y: int) -> None:
        self.buf.append((float(p), int(y)))

    def snapshot(self) -> dict:
        pairs = list(self.buf)
        s = {"n": len(pairs), "brier": brier(pairs), "ece": ece(pairs)}
        if len(pairs) >= 10:
            if s["ece"] > self.alarm_ece:
                self.consecutive_alarm += 1
            else:
                self.consecutive_alarm = 0
            s["degraded"] = self.consecutive_alarm >= 2   # 连续两窗 ⇒ 降级自动权重
            self.history.append(s)
        return s
