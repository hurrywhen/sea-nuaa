"""指标与理论界检验（论文 §13 P2/P3/P5 的试点实现）。"""
from __future__ import annotations

import numpy as np


def arm_metrics(selected: np.ndarray, *, critical: np.ndarray, value: np.ndarray,
                wl_mask: np.ndarray, budget: int, info: dict,
                dprime: float | None = None, theory_pred: float | None = None) -> dict:
    n = len(critical)
    sel = np.zeros(n, dtype=bool)
    sel[selected] = True
    n_crit = int(critical.sum())
    hit = sel & critical
    recall = float(hit.sum() / n_crit) if n_crit else float("nan")
    crit_wl = critical & wl_mask
    crit_nwl = critical & ~wl_mask
    r_wl = float((hit & crit_wl).sum() / crit_wl.sum()) if crit_wl.sum() else float("nan")
    r_nwl = float((hit & crit_nwl).sum() / crit_nwl.sum()) if crit_nwl.sum() else float("nan")
    precision = float(critical[sel].sum() / sel.sum()) if sel.sum() else float("nan")
    captured = float(value[sel].sum())
    missed_value = float(value[critical & ~sel].sum())
    # 命题 6.2 失真下界：完美排序下预算外的关键价值
    v_crit_sorted = np.sort(value[critical])[::-1]
    d_star = float(v_crit_sorted[budget:].sum()) if len(v_crit_sorted) > budget else 0.0
    return {
        "recall": recall,
        "recall_wl_covered": r_wl,
        "recall_not_wl": r_nwl,
        "precision": precision,
        "value_captured": captured,
        "distortion_D": missed_value,
        "distortion_lower_bound_Dstar": d_star,
        "distortion_bound_ok": bool(missed_value >= d_star - 1e-9),
        "budget_used": int(sel.sum()),
        "alarm_budget_conflict": bool(info.get("alarm_budget_conflict", False)),
        "dprime_measured": dprime,
        "theorem61_pred_recall": theory_pred,
        "beta": budget / n,
        "pi": n_crit / n,
        "cap_beta_over_pi": (budget / n_crit) if n_crit else float("nan"),
    }


def aggregate(rows: list[dict], keys: list[str]) -> list[dict]:
    """按 keys 分组求均值/标准差（纯 numpy，无 pandas 依赖）。"""
    groups: dict[tuple, list[dict]] = {}
    for r in rows:
        groups.setdefault(tuple(r[k] for k in keys), []).append(r)
    out = []
    num_keys = ["recall", "recall_wl_covered", "recall_not_wl", "precision", "value_captured",
                "distortion_D", "distortion_lower_bound_Dstar", "alarm_budget_conflict",
                "dprime_measured", "theorem61_pred_recall", "cap_beta_over_pi",
                "recall_mkt_port", "recall_mkt_out", "recall_legal_port",
                "dprime_market", "dprime_legal"]
    for gk, rs in sorted(groups.items()):
        row = dict(zip(keys, gk))
        row["n_agents"] = len(rs)
        for k in num_keys:
            vals = np.array([r.get(k, np.nan) for r in rs], dtype=float)
            vals = vals[~np.isnan(vals)]
            row[f"{k}_mean"] = float(vals.mean()) if len(vals) else float("nan")
            row[f"{k}_std"] = float(vals.std(ddof=1)) if len(vals) > 1 else 0.0
        row["bound_ok_all"] = all(r["distortion_bound_ok"] for r in rs)
        out.append(row)
    return out
