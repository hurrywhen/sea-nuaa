"""P2 投资者画像试点：EDGAR 2019-09 重放 × H4 强形式（高 p_min 域）× 特征评分器。

臂：S0 时序 / S1 参与度（形态显著性+噪声）/ S2c 纯评分（参数 proxy，ρ 扫描）
    S2[port] 双通道（通道 I = 组合持仓 25 家披露直通）/ S2[all] 全监控（超额供给演示）
    S2c-feat / S2[port]-feat 特征评分器（可观测元数据，walk-forward 训练，任务 4 的金融域实现）
真值：E*_legal（法定重大 8-K items）与 E*_market（|日收益|≥2.5% 且可归因）分别报告。

运行：cd sim && python3 -m sea_pilot.run_p2
"""
from __future__ import annotations

import csv
import json
import math
import os

import numpy as np

from . import config
from .metrics import aggregate, arm_metrics
from .p2_environment import build_all
from .scorer import make_scores  # noqa: F401  (保持接口一致；P2 自建评分)
from .scorer import measure_dprime, theory_recall
from .strategies import select

ARMS = ("S0", "S1", "S2c", "S2p", "S2a", "S2c-feat", "S2p-feat")
ARM_WL = {"S0": None, "S1": None, "S2c": None, "S2p": "port", "S2a": "all",
          "S2c-feat": None, "S2p-feat": "port"}


# ---------- 特征评分器（任务 4：可观测元数据 + walk-forward，零后见） ----------

def firm_aug_freq() -> dict[str, int]:
    """每家公司 2019-08 申报频次（来自 submissions 缓存，零后见）。"""
    sub = os.path.join(config.RAW_DIR, "p2", "submissions")
    out: dict[str, int] = {}
    if not os.path.isdir(sub):
        return out
    for fn in os.listdir(sub):
        d = json.load(open(os.path.join(sub, fn), encoding="utf-8"))
        t = d["ticker"]
        dates = d["raw"]["filings"]["recent"]["filingDate"]
        out[t] = sum(1 for x in dates if x.startswith("2019-08"))
    return out


def build_features(props: list[dict]) -> np.ndarray:
    freq = firm_aug_freq()
    cols = []
    for p in props:
        cols.append([
            p["n_docs"],
            float(p["is_8k"]),
            len(p["items"]),
            1.0 if 0 <= p["acceptance_hour"] < 13 else 0.0,   # 美东盘前接受
            float(freq.get(p["ticker"], 0)),
            len(p["classes"]),
        ])
    return np.array(cols, dtype=float)


def logistic_fit(X: np.ndarray, y: np.ndarray, l2: float = 1e-2, iters: int = 400,
                 lr: float = 0.1) -> tuple[np.ndarray, float]:
    mu, sd = X.mean(0), X.std(0) + 1e-9
    Z = (X - mu) / sd
    w = np.zeros(Z.shape[1]); b = 0.0
    n = len(y)
    for _ in range(iters):
        p = 1.0 / (1.0 + np.exp(-(Z @ w + b)))
        g = (p - y) / n
        w -= lr * (Z.T @ g + l2 * w)
        b -= lr * g.sum()
    return w, b


def feature_scores(X: np.ndarray, w: np.ndarray, b: float, mu: np.ndarray, sd: np.ndarray) -> np.ndarray:
    return ((X - mu) / sd) @ w + b


# ---------- 主流程 ----------

def main() -> None:
    os.makedirs(config.RESULTS_DIR, exist_ok=True)
    env = build_all(verbose=True)
    props = env["props"]
    n = len(props)
    if n == 0:
        raise SystemExit("P2 环境为空：请先运行 fetch_p2.py（EDGAR/Yahoo）")

    day = np.array([int(p["date"][8:10]) - 1 for p in props])
    crit_legal = np.array([p["legal_critical"] for p in props])
    crit_market = np.array([p["market_critical"] for p in props])
    imp = 2.0 * crit_legal + 2.0 * crit_market + 0.5 * _z(np.array([p["n_docs"] for p in props], float))
    value = imp.copy()
    # S1 参与度基线：真实注意力信号（新闻量 + 维基浏览异常）+ 噪声
    from .p2_environment import load_pageviews
    pv = load_pageviews()
    n_news = np.array([p["n_news"] for p in props], float)
    pv_anom = np.zeros(len(props))
    for i, p in enumerate(props):
        ser = pv.get(p["ticker"]) or {}
        if ser:
            key = p["date"].replace("-", "")
            med = float(np.median(list(ser.values()))) if ser else 0.0
            pv_anom[i] = (ser.get(key, med) / med - 1.0) if med > 0 else 0.0
    hype = (0.7 * _z(n_news) + 0.4 * _z(pv_anom)
            + 0.9 * np.random.default_rng(config.SEED).standard_normal(len(props)))
    order = np.lexsort((np.array([p["pid"] for p in props]), day))

    port_mask = np.array([p["in_portfolio"] for p in props])
    all_mask = np.ones(n, dtype=bool)
    # 组合条件化真值：P2 的 E* 是组合相对的（核心职责 = 持仓内事件；发现 = 持仓外）
    crit_m_port = crit_market & port_mask
    crit_m_out = crit_market & ~port_mask
    crit_l_port = crit_legal & port_mask

    # 特征评分器：前半月训练（walk-forward，零后见于测试半段）
    X = build_features(props)
    y = (crit_legal | crit_market).astype(float)
    train = day < 15
    mu, sd = X[train].mean(0), X[train].std(0) + 1e-9
    wf, bf = logistic_fit((X[train] - mu) / sd, y[train])
    feat = feature_scores(X, wf, bf, mu, sd)
    d_feat_test = measure_dprime(feat[~train], (crit_legal | crit_market)[~train])
    d_feat_all = measure_dprime(feat, crit_legal | crit_market)
    d_feat_market = measure_dprime(feat, crit_market)
    d_feat_legal = measure_dprime(feat, crit_legal)

    rows: list[dict] = []
    ident: list[dict] = []
    for ri, rho in enumerate(config.RHO_SWEEP):
        for ai in range(config.N_AGENTS):
            m = config.BUDGETS_PER_DAY_P2[ai % len(config.BUDGETS_PER_DAY_P2)]
            budget = m * config.SIM_DAYS_P2
            rng = np.random.default_rng(config.SEED + 7000 * ri + ai)
            zi = _z(imp)
            proxy = rho * zi + math.sqrt(max(0.0, 1 - rho ** 2)) * rng.standard_normal(n)
            d_proxy = measure_dprime(proxy, crit_market)
            d_proxy_legal = measure_dprime(proxy, crit_legal)
            for arm in ARMS:
                use_feat = arm.endswith("-feat")
                scores = feat if use_feat else proxy
                wl = ARM_WL[arm]
                wl_mask = port_mask if wl == "port" else (all_mask if wl == "all" else np.zeros(n, bool))
                base_arm = "S2c" if arm.startswith("S2c") else ("S2" if arm.startswith("S2") else arm)
                selected, info = select(base_arm, budget, order=order, hype=hype,
                                        proxy=scores, wl_mask=wl_mask)
                for tag, cm in (("legal", crit_legal), ("market", crit_market)):
                    met = arm_metrics(selected, critical=cm, value=value, wl_mask=wl_mask,
                                      budget=budget, info=info,
                                      dprime=d_proxy if (arm == "S2c" and tag == "market") else None,
                                      theory_pred=None)
                    rows.append({"arm": arm, "rho": rho, "agent": ai, "budget_per_day": m,
                                 "budget": budget, "truth": tag,
                                 "dprime_scorer": d_feat_all if use_feat else d_proxy,
                                 "dprime_market": d_feat_market if use_feat else d_proxy,
                                 "dprime_legal": d_feat_legal if use_feat else d_proxy_legal,
                                 "recall_mkt_port": _recall(selected, crit_m_port),
                                 "recall_mkt_out": _recall(selected, crit_m_out),
                                 "recall_legal_port": _recall(selected, crit_l_port),
                                 **met})
                if arm == "S2c" :
                    beta = budget / n
                    pi = float(crit_market.mean())
                    ident.append({"rho": rho, "m": m, "beta": beta, "pi": pi, "dprime": d_proxy,
                                  "pred": theory_recall(beta, pi, d_proxy),
                                  "realized": rows[-2]["recall"] if rows[-2]["truth"] == "market" else rows[-1]["recall"]})

    _write_csv(os.path.join(config.RESULTS_DIR, "p2_rows.csv"), rows)
    agg = aggregate([r for r in rows], keys=["arm", "rho", "truth", "budget_per_day"])
    _write_csv(os.path.join(config.RESULTS_DIR, "p2_agg.csv"), agg)

    I = np.array([[t["pred"], t["realized"]] for t in ident])
    summary = {
        "env": {k: v for k, v in env.items() if k not in ("props", "crit_legal", "crit_market")},
        "n_props": n,
        "rho_c_measured": env["rho_c"],
        "K_legal": int(crit_legal.sum()), "K_market": int(crit_market.sum()),
        "pi_market": float(crit_market.mean()), "pi_legal": float(crit_legal.mean()),
        "portfolio": env["portfolio"],
        "feature_scorer": {"d_prime_test_half": d_feat_test, "d_prime_all": d_feat_all,
                            "d_prime_market": d_feat_market, "d_prime_legal": d_feat_legal,
                            "train_days": "<15", "test_days": ">=15"},
        "identity_check_S2c_market": {
            "corr": float(np.corrcoef(I[:, 0], I[:, 1])[0, 1]) if len(I) > 2 else None,
            "mae": float(np.abs(I[:, 0] - I[:, 1]).mean()) if len(I) else None,
        },
    }
    json.dump(summary, open(os.path.join(config.RESULTS_DIR, "p2_summary.json"), "w",
                            encoding="utf-8"), ensure_ascii=False, indent=1, default=str)

    print("\n===== P2 H4 强形式检验（market 真值，ρ=0.4，全预算档平均）=====")
    for arm in ARMS:
        v = [r["recall"] for r in rows if r["arm"] == arm and r["rho"] == 0.4 and r["truth"] == "market"]
        vl = [r["recall"] for r in rows if r["arm"] == arm and r["rho"] == 0.4 and r["truth"] == "legal"]
        vp = [r["recall_mkt_port"] for r in rows if r["arm"] == arm and r["rho"] == 0.4 and r["truth"] == "market"]
        vo = [r["recall_mkt_out"] for r in rows if r["arm"] == arm and r["rho"] == 0.4 and r["truth"] == "market"]
        if v:
            print(f"  {arm:9s} recall_market={np.mean(v):.3f} (组合内={np.nanmean(vp):.3f}/组合外={np.nanmean(vo):.3f})"
                  f"  recall_legal={np.mean(vl):.3f}")
    print(f"\n特征评分器实测 d′: market={d_feat_market:.2f}, legal={d_feat_legal:.2f}, "
          f"复合(全月)={d_feat_all:.2f}, 复合(test半段)={d_feat_test:.2f}（任务4金融域首测）")
    print(f"恒等式检验(S2c×market): corr={summary['identity_check_S2c_market']['corr']}, "
          f"MAE={summary['identity_check_S2c_market']['mae']}")
    print("done ->", config.RESULTS_DIR)


def _z(x: np.ndarray) -> np.ndarray:
    s = x.std()
    return (x - x.mean()) / s if s > 0 else x * 0.0


def _recall(selected: np.ndarray, crit: np.ndarray) -> float:
    if crit.sum() == 0:
        return float("nan")
    sel = np.zeros(len(crit), dtype=bool)
    sel[selected] = True
    return float((sel & crit).sum() / crit.sum())


def _write_csv(path: str, rows: list[dict]) -> None:
    if not rows:
        return
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    main()
