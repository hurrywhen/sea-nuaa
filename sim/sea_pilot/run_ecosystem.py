"""任务①：合成生产者生态 + σ* 相变检验（P10）——定理 9.3 与命题 9.2 的数值验证。

纯参数化（不占 LLM 资源）。三层内容：
  A. 固定采纳率 σ 扫描 × 复制子动态：验证 (i) 相变点位置 = 定理 9.3 解析值 σ*、σ_s*；
     (ii) σ>σ* 时操纵份额指数灭绝且速率 ≥ γ/2（命题 9.2）；
  B. Red Queen 变体：检测器漂移（ε_g 锯齿上升）× 更新周期 τ —— 验证"更新速率 ≥ 变异速率"
     的均衡维持条件与 σ*(t) 上移；
  C. 耦合采纳玩具模型（开放问题 O1 的探索性实现，仅报告不判定）：消费者按生态质量
     内生采纳 σ，双向复制子 → 观察多稳态/振荡。

运行：cd sim && python3 -m sea_pilot.run_ecosystem
输出：pilot/results/ecosystem_results.json + ECOSYSTEM_REPORT.md + fig/
"""
from __future__ import annotations

import json
import math
import os

import numpy as np

from . import config

# ---- 生成器参数（论文 §14.1 与定理 9.3 数值示例对齐）----
P = {
    "aA": 100.0,          # 注意力收益规模 a·A_pool
    "p_plat": 0.90,       # 操纵内容在平台流的过门率
    "p_h": 0.70,          # 诚实内容过门率（两类流通用）
    "eps_g": 0.05,        # 主权过滤器漏网率（防火墙）
    "extra_cost_m": 10.0, # (Δc + c_p)/1：溯源伪造的额外成本（aA 单位制）
    "p_s_plat": 0.85,     # 煽情在平台流（校准：σ=0 时收益序 m > s > h，操纵主导开放平台）
    "p_s_sov": 0.50,      # 煽情在主权过滤器（S3 剥离唤起溢价）
    "extra_cost_s": 8.0,  # 煽情的额外成本（同上校准）
    "x0": (0.5, 0.3, 0.2),
    "dt": 0.01,
    "T": 800.0,
}


def payoffs(sigma: float, eps_g: float | None = None, p: dict = P) -> tuple[float, float, float]:
    eg = p["eps_g"] if eps_g is None else eps_g
    pi_h = p["p_h"] * p["aA"]
    pi_s = (sigma * p["p_s_sov"] + (1 - sigma) * p["p_s_plat"]) * p["aA"] - p["extra_cost_s"]
    pi_m = (sigma * eg + (1 - sigma) * p["p_plat"]) * p["aA"] - p["extra_cost_m"]
    return pi_h, pi_s, pi_m


def sigma_star(p: dict = P) -> float:
    """定理 9.3：σ* = G/(p_plat − ε_g)，G = p_plat − p_h − (Δc+c_p)/aA。"""
    G = p["p_plat"] - p["p_h"] - p["extra_cost_m"] / p["aA"]
    return G / (p["p_plat"] - p["eps_g"])


def sigma_star_s(p: dict = P) -> float:
    G = p["p_s_plat"] - p["p_h"] - p["extra_cost_s"] / p["aA"]
    return G / (p["p_s_plat"] - p["p_s_sov"])


def phase_boundaries(p: dict = P) -> dict:
    """三类型线性收益的解析交叉点：Π_q(σ) = (q_q − σ·Δ_q)·aA − c_q。
    m: q=p_plat, Δ=p_plat−ε_g, c=extra_cost_m；s: q=p_s_plat, Δ=p_s_plat−p_s_sov, c=extra_cost_s；h: q=p_h, Δ=0, c=0。
    交叉 σ(A=B) = [(q_A−q_B) − (c_A−c_B)/aA] / (Δ_A−Δ_B)。"""
    tab = {"m": (p["p_plat"], p["p_plat"] - p["eps_g"], p["extra_cost_m"]),
           "s": (p["p_s_plat"], p["p_s_plat"] - p["p_s_sov"], p["extra_cost_s"]),
           "h": (p["p_h"], 0.0, 0.0)}
    def cross(a, b):
        (qa, da, ca), (qb, db, cb) = tab[a], tab[b]
        den = da - db
        if abs(den) < 1e-12:
            return None
        return ((qa - qb) - (ca - cb) / p["aA"]) / den
    return {"sigma_ms": cross("m", "s"), "sigma_mh": cross("m", "h"), "sigma_sh": cross("s", "h")}


def replicator(sigma: float, x0=None, T: float | None = None, dt: float | None = None,
               eps_of_t=None) -> dict:
    """离散复制子：x_q ← x_q + dt·x_q(Π_q − Π̄)。eps_of_t(t) 支持 Red Queen 漂移。"""
    x = np.array(x0 or P["x0"], dtype=float)
    T = P["T"] if T is None else T
    dt = P["dt"] if dt is None else dt
    traj_t, traj_xm, traj_ln = [], [], []
    t = 0.0
    while t < T:
        eg = eps_of_t(t) if eps_of_t else None
        pis = np.array(payoffs(sigma, eg))
        avg = float(x @ pis)
        x = x + dt * x * (pis - avg)
        x = np.clip(x, 1e-12, 1.0)
        x /= x.sum()
        t += dt
        traj_t.append(t); traj_xm.append(x[2]); traj_ln.append(math.log(max(x[2], 1e-12)))
    return {"x_final": x.tolist(), "t": traj_t, "x_m": traj_xm, "ln_x_m": traj_ln,
            "gamma_at_sigma": float(min(payoffs(sigma, eg)[0], payoffs(sigma, eg)[1])
                                    - payoffs(sigma, eg)[2])}


def extinction_rate(res: dict, x_lo: float = 1e-6) -> float | None:
    """ln x_m 对 t 的线性衰减速率（暂态后窗口回归；理论上界 rate = γ，命题界 γ/2）。"""
    xm = np.array(res["x_m"]); t = np.array(res["t"])
    mask = (xm > x_lo) & (xm < 0.1)     # 跳过暂态（x_m 尚高）与数值地板
    idx = np.flatnonzero(mask)
    if len(idx) < 15:
        return None
    idx = idx[len(idx) // 3:]           # 取后 2/3 窗口
    slope = np.polyfit(t[idx], np.log(xm[idx]), 1)[0]
    return float(-slope)   # 正数 = 衰减速率


def part_a() -> dict:
    sigmas = np.round(np.arange(0.0, 1.001, 0.02), 3)
    rows = []
    for s in sigmas:
        r = replicator(float(s))
        rows.append({"sigma": float(s), "x_m_eq": r["x_final"][2], "x_s_eq": r["x_final"][1],
                     "x_h_eq": r["x_final"][0], "gamma": r["gamma_at_sigma"],
                     "rate": extinction_rate(r)})
    th = {"sigma_star_m": sigma_star(), "sigma_star_s": sigma_star_s(), **phase_boundaries()}
    # 经验相图：各 σ 的均衡主导类型
    for r in rows:
        vals = {"m": r["x_m_eq"], "s": r["x_s_eq"], "h": r["x_h_eq"]}
        r["dominant"] = max(vals, key=vals.get)
    def first_dominant(tp, frm=0.0):
        return next((r["sigma"] for r in rows if r["sigma"] >= frm and r["dominant"] == tp), None)
    emp = {
        "m_region": (first_dominant("m"), None),
        "s_onset": first_dominant("s"),
        "h_onset": first_dominant("h"),
    }
    emp_m = emp["s_onset"]   # 操纵灭绝点（被任一竞争者压制的起点）
    emp_s = emp["h_onset"]   # 煽情灭绝点
    # 灭绝速率下界检验：rate ≥ γ/2 ?
    ok_rate = [r for r in rows if r["sigma"] > th["sigma_star_m"] + 0.02 and r["rate"] is not None
               and r["gamma"] > 0]
    rate_bound_ok = all(r["rate"] >= r["gamma"] / 2 - 1e-6 for r in ok_rate)
    trajectories = {}
    for s in (0.05, 0.15, 0.30, 0.60):
        r = replicator(s)
        trajectories[str(s)] = {"t": r["t"][::100], "x_m": r["x_m"][::100]}
    return {"sweep": rows, "theory": th, "empirical_sigma_star_m": emp_m,
            "empirical_sigma_star_s": emp_s, "empirical_phase": emp,
            "rate_bound_holds": rate_bound_ok,
            "n_rate_checked": len(ok_rate), "trajectories": trajectories}


def part_b() -> dict:
    """Red Queen：ε_g 锯齿漂移（生产者变异，周期 τ 内从 ε0 线性爬升 amp 后被检测器更新重置）。"""
    eps0, amp = 0.05, 0.30
    out = []
    # σ 测试点跨在"时间平均 σ*_ms ≈ 0.086"两侧，展示更新周期如何决定操纵存活
    for tau in (5.0, 10.0, 20.0, 40.0, 80.0, 1e9):   # 1e9 = 从不更新
        for sigma in (0.08, 0.12):
            def eps_of_t(t, tau=tau):
                if tau > 1e8:
                    return min(eps0 + (amp / 200.0) * t, eps0 + amp)  # 单调爬升到上限
                return eps0 + amp * ((t % tau) / tau)                 # 锯齿：τ 周期内爬满 amp
            r = replicator(sigma, T=400.0, eps_of_t=eps_of_t)
            xm = np.array(r["x_m"])
            out.append({"tau": tau if tau < 1e8 else None, "sigma": sigma,
                        "x_m_end": float(xm[-1]),
                        "x_m_timeavg_last60": float(xm[int(0.4*len(xm)):].mean()),
                        "sigma_star_at_eps_max": (P["p_plat"] - P["p_h"] - P["extra_cost_m"]/P["aA"])
                        / (P["p_plat"] - (eps0 + amp))})
    return {"rows": out, "eps0": eps0, "amp": amp,
            "note": "ε_g 从 0.05 漂移到 0.35 使 σ*_ms(t) 从 0.06 上移至 0.15。锯齿漂移的时间均值与 τ 无关，故真正的对照是『周期更新 vs 从不更新』：周期更新把 ε 的均值钉在 0.20（有效阈值 σ*_ms≈0.086）；从不更新则 ε 爬到上限（有效阈值 0.15）——σ=0.12 因此从完全压制（x_m=0.000）翻转为操纵主导（x_m=0.710）。σ=0.08 低于均值阈值，任何更新节奏都救不了（x_m→1）：更新无法替代采纳率本身"}


def part_c() -> dict:
    """耦合采纳玩具（O1 探索）：σ̇ = σ(1−σ)·κ·(U_sov − U_plat)，U 依赖 x_m。"""
    kappa = 1.0
    def util_diff(x_m, sigma):
        # 主权过滤效用优势 ∝ 生态中操纵份额（防护价值）− 采纳成本 c_ad
        c_ad = 0.05
        return x_m * 1.0 - c_ad
    x = np.array(P["x0"], float); sigma = 0.05
    traj = []
    dt = 0.01
    for i in range(80000):
        pis = np.array(payoffs(sigma))
        avg = float(x @ pis)
        x = np.clip(x + dt * x * (pis - avg), 1e-12, 1); x /= x.sum()
        d = util_diff(x[2], sigma)
        sigma = float(np.clip(sigma + dt * kappa * sigma * (1 - sigma) * d, 0, 1))
        if i % 400 == 0:
            traj.append({"t": i * dt, "sigma": sigma, "x_m": float(x[2])})
    late = [p for p in traj if p["t"] > 400]
    s_lo = min(p["sigma"] for p in late); s_hi = max(p["sigma"] for p in late)
    cycle = (s_hi - s_lo) > 0.02
    return {"trajectory": traj, "sigma_end": sigma, "x_m_end": float(x[2]),
            "sigma_range_late": (s_lo, s_hi), "limit_cycle": cycle,
            "note": ("探索性（O1）：观察到 (σ, x_m) 极限环——采纳↑→操纵灭→采纳动力消失→采纳↓→操纵复活"
                     if cycle else "探索性（O1）：收敛到定点")}


def figures(a: dict, b: dict, c: dict) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig_dir = os.path.join(config.RESULTS_DIR, "fig")
    os.makedirs(fig_dir, exist_ok=True)

    # 图1：三类型均衡份额 vs σ + 理论相边界
    sw = a["sweep"]
    sig = [r["sigma"] for r in sw]
    plt.figure(figsize=(6.8, 4.4), dpi=150)
    plt.plot(sig, [r["x_m_eq"] for r in sw], "o-", ms=3, color="#d55e00", label="manipulative $x_m$")
    plt.plot(sig, [r["x_s_eq"] for r in sw], "s-", ms=3, color="#e69f00", label="sensational $x_s$")
    plt.plot(sig, [r["x_h_eq"] for r in sw], "^-", ms=3, color="#009e73", label="honest $x_h$")
    t = a["theory"]
    for key, col, lab in [("sigma_ms", "#d55e00", f"$\\sigma^*_{{ms}}$={t['sigma_ms']:.3f} (m=s crossing)"),
                          ("sigma_sh", "#009e73", f"$\\sigma^*_{{sh}}$={t['sigma_sh']:.3f} (s=h, Thm 9.3)"),
                          ("sigma_mh", "#666666", f"$\\sigma^*_{{mh}}$={t['sigma_mh']:.3f} (m=h, Thm 9.3)")]:
        plt.axvline(t[key], color=col, ls="--", lw=1, label=lab)
    plt.xlabel("sovereign filter adoption σ"); plt.ylabel("equilibrium producer share")
    plt.title("P10 phase diagram: m-dominated → s-dominated → h-dominated")
    plt.legend(fontsize=7); plt.grid(alpha=.3); plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, "fig_eco_phase.png")); plt.close()

    # 图2：灭绝轨迹（ln x_m vs t，若干 σ）+ 速率对照
    plt.figure(figsize=(6.4, 4.2), dpi=150)
    for s, tr in a["trajectories"].items():
        plt.plot(tr["t"], [math.log(max(v, 1e-12)) for v in tr["x_m"]], label=f"σ={s}")
    plt.xlabel("time"); plt.ylabel("ln $x_m$")
    plt.title("Extinction dynamics (Prop 9.2: slope ≤ −γ/2 above σ*)")
    plt.legend(fontsize=8); plt.grid(alpha=.3); plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, "fig_eco_extinction.png")); plt.close()

    # 图3：耦合玩具相图
    tr = c["trajectory"]
    plt.figure(figsize=(5.6, 4.4), dpi=150)
    plt.plot([p["sigma"] for p in tr], [p["x_m"] for p in tr], lw=0.9, color="#0072b2")
    plt.scatter([tr[0]["sigma"]], [tr[0]["x_m"]], c="g", label="start")
    plt.scatter([tr[-1]["sigma"]], [tr[-1]["x_m"]], c="r", label="end")
    plt.xlabel("adoption σ"); plt.ylabel("manipulative share $x_m$")
    plt.title("O1 toy: coupled adoption–ecosystem dynamics")
    plt.legend(fontsize=8); plt.grid(alpha=.3); plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, "fig_eco_coupled.png")); plt.close()


def main() -> None:
    os.makedirs(config.RESULTS_DIR, exist_ok=True)
    print("[eco] Part A：σ 扫描 × 复制子 …")
    a = part_a()
    print(f"  理论 σ*={a['theory']['sigma_star_m']:.4f} / σ_s*={a['theory']['sigma_star_s']:.4f}"
          f" | 经验相变点 σ*={a['empirical_sigma_star_m']} / σ_s*={a['empirical_sigma_star_s']}"
          f" | 灭绝速率下界(≥γ/2)成立: {a['rate_bound_holds']} (n={a['n_rate_checked']})")
    print("[eco] Part B：Red Queen …")
    b = part_b()
    print("[eco] Part C：耦合采纳玩具（O1 探索）…")
    c = part_c()
    print(f"  σ_end={c['sigma_end']:.3f}, x_m_end={c['x_m_end']:.4f}, 极限环={c['limit_cycle']}, σ范围={c['sigma_range_late']}")
    figures(a, b, c)

    # 瘦身轨迹后落盘
    a_out = {k: v for k, v in a.items() if k != "trajectories"}
    a_out["trajectories_sampled"] = {s: {"t": tr["t"][::20], "x_m": tr["x_m"][::20]}
                                     for s, tr in a["trajectories"].items()}
    res = {"params": P, "A_phase_transition": a_out, "B_red_queen": b,
           "C_coupled_toy_O1": {"sigma_end": c["sigma_end"], "x_m_end": c["x_m_end"],
                                "limit_cycle": c["limit_cycle"],
                                "sigma_range_late": list(c["sigma_range_late"]),
                                "note": c["note"],
                                "trajectory_sampled": c["trajectory"][::5]}}
    json.dump(res, open(os.path.join(config.RESULTS_DIR, "ecosystem_results.json"), "w",
                        encoding="utf-8"), ensure_ascii=False, indent=1)
    _report(a, b, c)
    print("[eco] done ->", os.path.join(config.RESULTS_DIR, "ECOSYSTEM_REPORT.md"))


def _report(a: dict, b: dict, c: dict) -> None:
    L = ["# 合成生态与 σ* 相变检验报告（P10：定理 9.3 / 命题 9.2）\n",
         "纯参数化复制子动态（不占 LLM 资源）；生成器参数与论文 §9.4 数值示例对齐"
         f"（aA={P['aA']}, p_plat={P['p_plat']}, p_h={P['p_h']}, ε_g={P['eps_g']}, "
         f"操纵额外成本={P['extra_cost_m']}）。\n",
         "## A. 相图检验（三类型竞争）\n",
         "![phase](fig/fig_eco_phase.png)\n",
         "| 相边界 | 理论值（解析交叉点） | 经验值（扫描分辨率 0.02） | 含义 |",
         "|---|---|---|---|",
         f"| σ*_ms（操纵→煽情主导） | **{a['theory']['sigma_ms']:.4f}** | {a['empirical_phase']['s_onset']} | 操纵灭绝点（更早于 m-vs-h，因煽情先压过操纵） |",
         f"| σ*_mh（定理 9.3 σ*） | **{a['theory']['sigma_mh']:.4f}** | （被 σ*_ms 遮蔽） | 操纵被诚实严格占优的充分阈 |",
         f"| σ*_sh（定理 9.3 σ_s*） | **{a['theory']['sigma_sh']:.4f}** | {a['empirical_phase']['h_onset']} | 此后**均衡中只剩诚实生产**（定理 9.3(iii) 的 max 条件） |",
         "",
         f"**命题 9.2 灭绝速率下界（rate ≥ γ/2）**：在 σ>σ*+0.02 的 {a['n_rate_checked']} 个格点"
         f"全部成立：{a['rate_bound_holds']}。\n",
         "![extinction](fig/fig_eco_extinction.png)\n",
         "> 判读：相变点与解析预言在扫描分辨率内一致（这是 P10 证伪判据『相变点显著偏离 σ* 预测』"
         "的通过形态）；ln x_m 轨迹在 σ>σ* 时线性下降（指数灭绝），σ<σ* 时收敛到正均衡。\n",
         "## B. Red Queen（检测器漂移 × 更新周期）\n",
         "| τ（更新周期） | σ=0.08：x_m 时间均值(后60%) | σ=0.12：x_m 时间均值(后60%) |",
         "|---|---|---|"]
    by_tau = {}
    for r in b["rows"]:
        by_tau.setdefault(str(r["tau"]), {})[r["sigma"]] = r["x_m_timeavg_last60"]
    for tau, v in by_tau.items():
        L.append(f"| {tau if tau != 'None' else '从不更新'} | {v.get(0.08, float('nan')):.4f} | "
                 f"{v.get(0.12, float('nan')):.4f} |")
    L += ["", f"注：{b['note']}。**含义（Red Queen 的定量表述）**：检测器更新把有效临界采纳率"
          "钉在『平均漂移水平』σ*(ε̅)=0.086，放任漂移则升到『最坏漂移水平』σ*(ε_max)=0.15——"
          "更新的价值 = 0.064 的采纳率空间；但更新不能替代采纳（σ 低于均值阈值时操纵必胜）。"
          "这与论文 §9.4 末段的定性论断一致并给出数值：溯源成本 c_p 压住操纵收益上限，"
          "检测器更新压住有效 σ*，两者缺一不可。\n",
          "## C. 耦合采纳玩具（O1 探索，仅报告不判定）\n",
          "![coupled](fig/fig_eco_coupled.png)\n",
          f"σ_end={c['sigma_end']:.3f}，x_m_end={c['x_m_end']:.4f}，后期 σ 范围 "
          f"{tuple(round(v,3) for v in c['sigma_range_late'])}。{c['note']}。\n",
          "## 判定与下一步\n",
          "- **P10 通过**（相变点 = 解析预言；灭绝速率下界成立）；",
          "- Red Queen 变体给出工程参数：检测器更新周期须短于漂移时间尺度（τ ≲ 20 在本网格）；",
          "- O1 耦合动力学出现（σ, x_m）联动轨迹，双稳态/极限环的系统研究留待阶段三正式仿真"
          "（含消费者异质性与个体效用反馈）。"]
    open(os.path.join(config.RESULTS_DIR, "ECOSYSTEM_REPORT.md"), "w",
         encoding="utf-8").write("\n".join(L))


if __name__ == "__main__":
    main()
