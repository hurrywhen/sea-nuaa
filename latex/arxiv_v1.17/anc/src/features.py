"""任务 4：真实特征评分器（P3 学术域）——元数据 + 标题 TF-IDF 新颖度，零后见。

特征（决策时点全部可观测）：
  f1 流内新颖度：1 − cos(tfidf(title), K̄)，K̄ = 此前已见论文的滚动均值向量（walk-forward）
  f2 作者声望：max_a(前窗引用总量(a))，z 化（对前窗内训练用 leave-one-out）
  f3 机构声望：Σ_e(前窗引用总量(e))，z 化（同上）
  f4 log1p(n_authors)   f5 log1p(n_insts)   f6 z(title_len)
  f7.. subfield one-hot（top-6）
训练：前窗（2019-07/08）论文，标签 = 前窗内 top2% 被引；logistic 回归（numpy GD）。
应用：2019-09 宇宙 → **实测真实世界的 d′**（对照定理 6.1 的 4.39 需求线）。
"""
from __future__ import annotations

import math
import re
from collections import Counter, defaultdict

import numpy as np

_TOKEN = re.compile(r"[a-z0-9]{2,}")
STOP = {"the", "of", "and", "for", "with", "that", "this", "from", "are", "was", "were",
        "can", "using", "use", "based", "via", "towards", "toward", "under", "over"}


def tokenize(title: str) -> list[str]:
    return [t for t in _TOKEN.findall(title.lower()) if t not in STOP]


def build_vocab(recs_list: list[list[dict]], top: int = 2500, min_df: int = 5) -> dict[str, int]:
    df: Counter = Counter()
    for recs in recs_list:
        for r in recs:
            df.update(set(tokenize(r["title"])))
    words = [w for w, c in df.most_common(top * 3) if c >= min_df][:top]
    return {w: i for i, w in enumerate(sorted(words))}


def tfidf_matrix(recs: list[dict], vocab: dict[str, int]) -> np.ndarray:
    n, V = len(recs), len(vocab)
    X = np.zeros((n, V), dtype=np.float32)
    df = np.zeros(V, dtype=np.float32)
    for i, r in enumerate(recs):
        toks = [t for t in tokenize(r["title"]) if t in vocab]
        c = Counter(toks)
        for w, k in c.items():
            X[i, vocab[w]] = 1.0 + math.log(k)
        if c:
            uniq = np.fromiter({vocab[w] for w in c}, dtype=np.int64, count=len(c))
            df[uniq] += 1
    idf = np.log((n + 1) / (df + 1)) + 1.0
    X *= idf
    norms = np.linalg.norm(X, axis=1, keepdims=True) + 1e-9
    return X / norms


def stream_novelty(X: np.ndarray, order: np.ndarray) -> np.ndarray:
    """walk-forward 新颖度：1 − cos(x_i, 已见论文均值)。order = 时间序索引。"""
    nov = np.zeros(len(X), dtype=np.float32)
    mean = np.zeros(X.shape[1], dtype=np.float32)
    for k, i in enumerate(order):
        if k > 0:
            m = mean / max(k, 1)
            nm = np.linalg.norm(m)
            nov[i] = 1.0 - (float(x_i_dot(X[i], m)) / (nm + 1e-9) if nm > 0 else 0.0)
        mean += X[i]
    return nov


def x_i_dot(a: np.ndarray, b: np.ndarray) -> float:
    return float(a @ b)


def prestige_maps(prior_recs: list[dict]) -> tuple[dict[str, float], dict[str, float]]:
    auth, inst = defaultdict(float), defaultdict(float)
    for r in prior_recs:
        for a in r["authors"]:
            auth[a] += r["cit"]
        for e in r["insts"]:
            inst[e] += r["cit"]
    return dict(auth), dict(inst)


def build_feature_matrix(recs: list[dict], vocab: dict[str, int],
                         auth_p: dict[str, float], inst_p: dict[str, float],
                         order: np.ndarray, loo: bool = False) -> np.ndarray:
    X_t = tfidf_matrix(recs, vocab)
    nov = stream_novelty(X_t, order)
    ap = np.array([max((auth_p.get(a, 0.0) for a in r["authors"]), default=0.0) for r in recs])
    ip = np.array([sum(inst_p.get(e, 0.0) for e in r["insts"]) for r in recs])
    if loo:  # 前窗内训练：扣除本文引用（零自引泄漏）
        ap = np.array([max((auth_p.get(a, 0.0) - (r["cit"] if a in r["authors"] else 0.0)
                            for a in r["authors"]), default=0.0) for r in recs])
        ip = np.array([sum(inst_p.get(e, 0.0) - (r["cit"] if e in r["insts"] else 0.0)
                            for e in r["insts"]) for r in recs])
    subs = Counter(r["subfield"] for r in recs)
    top_subs = [s for s, _ in subs.most_common(6)]
    cols = [nov, np.log1p(ap), np.log1p(ip),
            np.log1p([len(r["authors"]) for r in recs]),
            np.log1p([len(r["insts"]) for r in recs]),
            [len(r["title"]) for r in recs]]
    F = np.array(cols, dtype=float).T
    onehot = np.array([[1.0 if r["subfield"] == s else 0.0 for s in top_subs] for r in recs])
    F = np.hstack([F, onehot])
    return (F - F.mean(0)) / (F.std(0) + 1e-9)


def logistic_fit(X: np.ndarray, y: np.ndarray, l2: float = 1e-2, iters: int = 500,
                 lr: float = 0.1) -> tuple[np.ndarray, float]:
    w = np.zeros(X.shape[1]); b = 0.0; n = len(y)
    for _ in range(iters):
        p = 1.0 / (1.0 + np.exp(-(X @ w + b)))
        g = (p - y) / n
        w -= lr * (X.T @ g + l2 * w)
        b -= lr * g.sum()
    return w, b
