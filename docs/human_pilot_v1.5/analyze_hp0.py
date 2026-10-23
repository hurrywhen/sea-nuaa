#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HP-0 可行性试点分析脚本（analyze_hp0.py v1.0）。

口径文件：docs/human_pilot_v1.5/HP0_protocol_v1.0.md §8（SAP-1..SAP-4）。
依赖：Python 3 标准库 + numpy（缺失时给出安装提示后退出）。

功能：
  E1  最小声明可行性：完成率（Wilson 95% CI）、耗时、澄清提示、修订数、S-E1 判定。
  E2  校准重测：逐人 W1/W2 Brier、配对差、百分位 bootstrap 95% CI（B=10^4, seed=42）、
      精确 Wilcoxon（探索性）、urge 冲动代理描述。
  E3  课程接受度：极化移动与防御度的暴露周/无暴露周配对差（探索性）、
      S-E3 回火旗标（暴露周 shift 均值 > +0.5 x 合并SD）。
  BH  仅对 E2/E3 的三个探索性 p 值做 Benjamini-Hochberg 校正（封闭族）。

用法：
  python3 analyze_hp0.py --synthetic-dryrun     # 合成数据管线验证（seed 42）
  python3 analyze_hp0.py --input HP0_data.csv   # 真人数据（采集后）

纪律：
  - 一切输出带 UNDERPOWERED / feasibility-only 声明；禁止因果表述。
  - 合成干跑产物带 "SYNTHETIC DATA - NOT HUMAN DATA" 横幅，永不进入论文。
  - participant_id 以 EXAMPLE 开头的行永不进入分析。
"""

import argparse
import csv
import datetime
import math
import os
import sys

try:
    import numpy as np
except ImportError:  # graceful message per protocol SAP
    sys.stderr.write(
        "HP-0 analysis requires numpy (stdlib + numpy only).\n"
        "Install it with:  pip install numpy\n"
        "No output files were written.\n"
    )
    sys.exit(2)

SEED = 42
B_BOOT = 10000
Z95 = 1.959964
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

BRIER_COLS = ["brier_item_%02d" % i for i in range(1, 11)]
REQUIRED_COLS = (
    ["participant_id", "day", "week", "arm", "minutes",
     "urge_1", "urge_2", "urge_3", "defensiveness", "exposure_count",
     "extremity_1", "extremity_2", "extremity_3"]
    + BRIER_COLS
    + ["declaration_minutes", "clarifier_prompts", "declaration_revision_count"]
)

NAN = float("nan")


# ---------------------------------------------------------------- helpers

def fnum(x):
    """Parse a CSV cell to float; empty/invalid -> None."""
    if x is None:
        return None
    s = str(x).strip()
    if s == "":
        return None
    try:
        v = float(s)
    except ValueError:
        return None
    return v


def inum(x):
    v = fnum(x)
    return None if v is None else int(round(v))


def mean_of(vals):
    vals = [v for v in vals if v is not None and not math.isnan(v)]
    return sum(vals) / len(vals) if vals else None


def sd_of(vals):
    vals = [v for v in vals if v is not None and not math.isnan(v)]
    if len(vals) < 2:
        return None
    m = sum(vals) / len(vals)
    return math.sqrt(sum((v - m) ** 2 for v in vals) / (len(vals) - 1))


def fmt(v, nd=2):
    if v is None:
        return "—"
    try:
        if math.isnan(v):
            return "—"
    except TypeError:
        return str(v)
    return ("%." + str(nd) + "f") % v


def wilson_ci(k, n, z=Z95):
    """Wilson score 95% CI for a proportion."""
    if n == 0:
        return (NAN, NAN)
    ph = k / n
    den = 1.0 + z * z / n
    center = (ph + z * z / (2 * n)) / den
    half = z * math.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n)) / den
    return (max(0.0, center - half), min(1.0, center + half))


def boot_ci_mean(vals, seed=SEED, B=B_BOOT):
    """Percentile-bootstrap 95% CI of the mean; resampling unit = participant."""
    a = np.asarray([v for v in vals if v is not None and not math.isnan(v)], dtype=float)
    if a.size < 2:
        return (NAN, NAN)
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, a.size, size=(B, a.size))
    means = a[idx].mean(axis=1)
    return (float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5)))


def rankdata_avg(a):
    a = np.asarray(a, dtype=float)
    order = np.argsort(a, kind="mergesort")
    ranks = np.empty(a.size, dtype=float)
    sa = a[order]
    i = 0
    while i < a.size:
        j = i
        while j + 1 < a.size and sa[j + 1] == sa[i]:
            j += 1
        ranks[order[i:j + 1]] = (i + j) / 2.0 + 1.0
        i = j + 1
    return ranks


def wilcoxon_p(diffs):
    """Two-sided Wilcoxon signed-rank; exact enumeration for n<=15, else normal approx."""
    d = np.asarray([v for v in diffs if v is not None and not math.isnan(v)], dtype=float)
    d = d[d != 0.0]
    n = d.size
    if n == 0:
        return NAN
    r = rankdata_avg(np.abs(d))
    w_plus = float(r[d > 0].sum())
    if n <= 15:
        idx = np.arange(1 << n, dtype=np.int64)
        bits = ((idx[:, None] >> np.arange(n)[None, :]) & 1).astype(float)
        sums = bits @ r
        p_le = float(np.mean(sums <= w_plus + 1e-12))
        p_ge = float(np.mean(sums >= w_plus - 1e-12))
        return float(min(1.0, 2.0 * min(p_le, p_ge)))
    mu = n * (n + 1) / 4.0
    _, counts = np.unique(np.abs(d), return_counts=True)
    tie_term = float(((counts ** 3) - counts).sum())
    var = n * (n + 1) * (2 * n + 1) / 24.0 - tie_term / 48.0
    if var <= 0:
        return NAN
    cc = 0.5 if w_plus > mu else (-0.5 if w_plus < mu else 0.0)
    z = (w_plus - mu - cc) / math.sqrt(var)
    return float(math.erfc(abs(z) / math.sqrt(2.0)))


def bh_adjust(pvals):
    """Benjamini-Hochberg adjusted p-values (input order preserved)."""
    p = np.asarray(pvals, dtype=float)
    m = p.size
    if m == 0:
        return np.asarray([])
    order = np.argsort(p)
    adj = p[order] * m / np.arange(1, m + 1)
    adj = np.minimum.accumulate(adj[::-1])[::-1]
    out = np.empty(m, dtype=float)
    out[order] = np.clip(adj, 0.0, 1.0)
    return out


def md_table(headers, rows):
    lines = ["| " + " | ".join(headers) + " |",
             "|" + "|".join(["---"] * len(headers)) + "|"]
    for r in rows:
        lines.append("| " + " | ".join(str(c) for c in r) + " |")
    return "\n".join(lines)


# ---------------------------------------------------------------- data loading

def load_rows(path):
    """Read CSV; return (real_rows, n_example_rows). Validates required columns."""
    if not os.path.exists(path):
        sys.stderr.write("Input file not found: %s\n" % path)
        sys.exit(2)
    with open(path, newline="", encoding="utf-8-sig") as f:
        rdr = csv.DictReader(f)
        header = rdr.fieldnames or []
        missing = [c for c in REQUIRED_COLS if c not in header]
        if missing:
            sys.stderr.write(
                "Input CSV is missing required columns: %s\n" % ", ".join(missing))
            sys.exit(2)
        real, n_ex = [], 0
        for row in rdr:
            pid = (row.get("participant_id") or "").strip()
            if pid == "":
                continue
            if pid.upper().startswith("EXAMPLE"):
                n_ex += 1
                continue
            real.append(row)
    return real, n_ex


# ---------------------------------------------------------------- aggregation

def aggregate(rows):
    """Build per-participant structures from participant-day rows."""
    parts = {}
    for row in rows:
        pid = row["participant_id"].strip()
        p = parts.setdefault(pid, {
            "pid": pid, "days_present": set(), "decl": None,
            "arms": {}, "brier_items": {}, "ext": {}, "defensiveness": {},
            "exposure_count": {}, "urges": {},
        })
        day = inum(row.get("day"))
        if day is None:
            continue
        week = inum(row.get("week"))
        arm = (row.get("arm") or "").strip().upper()
        if week in (1, 2) and arm in ("EXPOSURE", "NO_EXPOSURE"):
            p["arms"].setdefault(week, arm)
        if 1 <= day <= 14:
            p["days_present"].add(day)

        # E1 declaration (normally the day-0 row)
        dm = fnum(row.get("declaration_minutes"))
        if dm is not None and p["decl"] is None:
            p["decl"] = {
                "minutes": dm,
                "prompts": fnum(row.get("clarifier_prompts")),
                "revisions": fnum(row.get("declaration_revision_count")),
            }

        # weekly Brier items (scoring rows: day 7 / day 14)
        items = [fnum(row.get(c)) for c in BRIER_COLS]
        valid = [v for v in items if v is not None]
        if valid and week in (1, 2):
            prev = p["brier_items"].get(week, [])
            if len(valid) > len(prev):
                p["brier_items"][week] = valid

        # extremity time points (day 0 / 7 / 14)
        if day in (0, 7, 14):
            e = [fnum(row.get("extremity_%d" % j)) for j in (1, 2, 3)]
            ev = [abs(v - 4.0) for v in e if v is not None]
            if len(ev) >= 2:  # valid time point: at least 2 of 3 items
                p["ext"][day] = sum(ev) / len(ev)

        # daily diary
        dv = fnum(row.get("defensiveness"))
        if dv is not None and 1 <= day <= 14:
            p["defensiveness"].setdefault(week_of(day), []).append(dv)
        ec = fnum(row.get("exposure_count"))
        if ec is not None and 1 <= day <= 14:
            p["exposure_count"][week_of(day)] = p["exposure_count"].get(week_of(day), 0.0) + ec
        for k in ("urge_1", "urge_2", "urge_3"):
            uv = fnum(row.get(k))
            if uv is not None and 1 <= day <= 14:
                p["urges"].setdefault(week_of(day), []).append(uv)

    # derived quantities
    for p in parts.values():
        p["enrolled"] = p["decl"] is not None
        d = p["decl"]
        p["e1_completed"] = bool(d and d["minutes"] is not None)
        p["e1_clean"] = bool(
            d and d["minutes"] is not None and d["minutes"] <= 15.0
            and (d["prompts"] is None or d["prompts"] <= 2))
        p["adherence"] = len(p["days_present"]) / 14.0
        p["low_adherence"] = len(p["days_present"]) < 10  # >=4 missed days
        for w in (1, 2):
            items = p["brier_items"].get(w, [])
            p["brier_w%d" % w] = (sum(items) / len(items)) if len(items) >= 8 else None
        exp_week = None
        arms = p["arms"]
        if arms.get(1) == "EXPOSURE" and arms.get(2) != "EXPOSURE":
            exp_week = 1
        elif arms.get(2) == "EXPOSURE" and arms.get(1) != "EXPOSURE":
            exp_week = 2
        p["exposure_week"] = exp_week
        p["noexp_week"] = (3 - exp_week) if exp_week else None
        sh = {}
        if p["ext"].get(0) is not None:
            for w, d_end in ((1, 7), (2, 14)):
                sh[w] = (p["ext"][d_end] - p["ext"][0]) if p["ext"].get(d_end) is not None else None
        else:
            sh = {1: None, 2: None}
        p["shift"] = sh
        p["def_mean"] = {w: mean_of(p["defensiveness"].get(w, [])) for w in (1, 2)}
        p["urge_mean"] = {w: mean_of(p["urges"].get(w, [])) for w in (1, 2)}
        p["exp_logged"] = {w: p["exposure_count"].get(w, 0.0) for w in (1, 2)}
    return parts


def week_of(day):
    return 1 if day <= 7 else 2


# ---------------------------------------------------------------- endpoints

def analyze(parts):
    R = {"n_enrolled": 0, "n_rows_ok": len(parts)}
    plist = sorted(parts.values(), key=lambda p: p["pid"])

    # ---- E1
    enrolled = [p for p in plist if p["enrolled"]]
    R["n_enrolled"] = len(enrolled)
    R["e1_rows"] = []
    for p in enrolled:
        d = p["decl"]
        R["e1_rows"].append({
            "pid": p["pid"], "minutes": d["minutes"], "prompts": d["prompts"],
            "revisions": d["revisions"], "completed": p["e1_completed"],
            "clean": p["e1_clean"],
        })
    n = len(enrolled)
    k_comp = sum(1 for p in enrolled if p["e1_completed"])
    k_clean = sum(1 for p in enrolled if p["e1_clean"])
    R["e1"] = {
        "n": n, "k_completed": k_comp, "k_clean": k_clean,
        "ci_completed": wilson_ci(k_comp, n), "ci_clean": wilson_ci(k_clean, n),
        "median_minutes": _median([d["minutes"] for d in (p["decl"] for p in enrolled) if d]),
        "minutes": [p["decl"]["minutes"] for p in enrolled if p["decl"]],
        "prompts": [p["decl"]["prompts"] for p in enrolled if p["decl"] and p["decl"]["prompts"] is not None],
        "revisions": [p["decl"]["revisions"] for p in enrolled if p["decl"] and p["decl"]["revisions"] is not None],
    }
    if n >= 10:
        R["e1"]["verdict"] = "达标 (PASS)" if k_clean >= 8 else ("部分达标" if k_comp >= 8 else "未达标 (FAIL)")
    else:
        R["e1"]["verdict"] = "n<10：按实际人数报告（%d/%d 干净完成）" % (k_clean, n)

    # ---- E2
    e2 = [p for p in plist if p["brier_w1"] is not None and p["brier_w2"] is not None]
    diffs = [p["brier_w2"] - p["brier_w1"] for p in e2]
    lo = boot_ci_mean(diffs)
    R["e2_rows"] = [{"pid": p["pid"], "w1": p["brier_w1"], "w2": p["brier_w2"],
                     "diff": (p["brier_w2"] - p["brier_w1"]) if (p["brier_w1"] is not None and p["brier_w2"] is not None) else None,
                     "low_adh": p["low_adherence"]} for p in plist]
    e2_lo = [p for p in e2 if not p["low_adherence"]]
    R["e2"] = {
        "n_paired": len(e2), "mean_diff": mean_of(diffs), "ci": lo,
        "p_wilcoxon": wilcoxon_p(diffs),
        "mean_w1": mean_of([p["brier_w1"] for p in e2]),
        "mean_w2": mean_of([p["brier_w2"] for p in e2]),
        "mean_diff_excl_lowadh": mean_of([p["brier_w2"] - p["brier_w1"] for p in e2_lo]),
        "n_paired_excl_lowadh": len(e2_lo),
    }
    urges = {1: [], 2: []}
    for p in plist:
        for w in (1, 2):
            if p["urge_mean"][w] is not None:
                urges[w].append(p["urge_mean"][w])
    R["e2"]["urge_w1"] = mean_of(urges[1])
    R["e2"]["urge_w2"] = mean_of(urges[2])

    # ---- E3
    e3 = []
    for p in plist:
        ew, nw = p["exposure_week"], p["noexp_week"]
        if ew is None:
            continue
        if p["shift"].get(ew) is None or p["shift"].get(nw) is None:
            continue
        if p["def_mean"].get(ew) is None or p["def_mean"].get(nw) is None:
            continue
        if p["exp_logged"].get(ew, 0.0) < 1:
            continue
        e3.append(p)
    sd_all = [p["shift"][w] for p in plist for w in (1, 2) if p["shift"].get(w) is not None]
    s_pool = sd_of(sd_all)
    exp_shifts = [p["shift"][p["exposure_week"]] for p in e3]
    noexp_shifts = [p["shift"][p["noexp_week"]] for p in e3]
    shift_diffs = [a - b for a, b in zip(exp_shifts, noexp_shifts)]
    def_diffs = [p["def_mean"][p["exposure_week"]] - p["def_mean"][p["noexp_week"]] for p in e3]
    mean_exp_shift = mean_of(exp_shifts)
    thr = (0.5 * s_pool) if s_pool is not None else None
    flag = (mean_exp_shift > thr) if (thr is not None and mean_exp_shift is not None) else None
    mean_def_diff = mean_of(def_diffs)
    n_pos_def = sum(1 for v in def_diffs if v > 0)
    guard = (mean_def_diff is not None and mean_def_diff > 1.0 and n_pos_def >= 3)
    e3_lo = [p for p in e3 if not p["low_adherence"]]
    R["e3_rows"] = [{"pid": p["pid"],
                     "ew": p["exposure_week"],
                     "shift_exp": p["shift"].get(p["exposure_week"]) if p["exposure_week"] else None,
                     "shift_noexp": p["shift"].get(p["noexp_week"]) if p["noexp_week"] else None,
                     "def_exp": p["def_mean"].get(p["exposure_week"]) if p["exposure_week"] else None,
                     "def_noexp": p["def_mean"].get(p["noexp_week"]) if p["noexp_week"] else None,
                     "n_exp_logs": p["exp_logged"].get(p["exposure_week"], 0.0) if p["exposure_week"] else None,
                     "paired": p in e3} for p in plist]
    R["e3"] = {
        "n_paired": len(e3), "s_pool": s_pool, "mean_exp_shift": mean_exp_shift,
        "mean_noexp_shift": mean_of(noexp_shifts), "threshold": thr, "flag": flag,
        "shift_diff_mean": mean_of(shift_diffs), "shift_diff_ci": boot_ci_mean(shift_diffs),
        "p_shift": wilcoxon_p(shift_diffs),
        "def_diff_mean": mean_def_diff, "def_diff_ci": boot_ci_mean(def_diffs),
        "p_def": wilcoxon_p(def_diffs), "guard": guard, "n_pos_def": n_pos_def,
        "n_paired_excl_lowadh": len(e3_lo),
        "shift_diff_mean_excl_lowadh": mean_of([
            p["shift"][p["exposure_week"]] - p["shift"][p["noexp_week"]] for p in e3_lo]),
    }

    # ---- BH family (closed: exactly the three exploratory contrasts)
    fam = [("E2 Brier W2-W1", R["e2"]["p_wilcoxon"]),
           ("E3 extremity shift (exp - noexp)", R["e3"]["p_shift"]),
           ("E3 defensiveness (exp - noexp)", R["e3"]["p_def"])]
    ok = [(name, pv) for name, pv in fam if pv is not None and not math.isnan(pv)]
    adj = bh_adjust([pv for _, pv in ok]) if ok else []
    R["bh"] = {name: (pv, None) for name, pv in fam}
    for (name, pv), a in zip(ok, adj):
        R["bh"][name] = (pv, float(a))

    # ---- adherence / missingness
    R["adh_rows"] = [{
        "pid": p["pid"], "days": len(p["days_present"]),
        "adherence": p["adherence"], "low": p["low_adherence"],
        "b1": len(p["brier_items"].get(1, [])), "b2": len(p["brier_items"].get(2, [])),
        "ext_pts": sum(1 for d in (0, 7, 14) if p["ext"].get(d) is not None),
        "e2_in": (p["brier_w1"] is not None and p["brier_w2"] is not None),
        "e3_in": p in e3,
    } for p in plist]
    return R


def _median(vals):
    vals = sorted(v for v in vals if v is not None and not math.isnan(v))
    if not vals:
        return None
    m = len(vals) // 2
    return vals[m] if len(vals) % 2 else (vals[m - 1] + vals[m]) / 2.0


# ---------------------------------------------------------------- reporting

BANNER_SYNTH = ("**SYNTHETIC DATA — NOT HUMAN DATA — pipeline validation only** "
                "(合成数据，非真人数据，仅用于分析管线验证；永不进入论文)")
BANNER_UNDER = ("**UNDERPOWERED — feasibility endpoints only.** HP-0 (n<=10) has no power "
                "for hypothesis testing; every contrast below is descriptive or exploratory; "
                "no causal or inferential claim is licensed.")


def render_md(R, mode, input_path, seed_used):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    out = []
    title = "HP-0 干跑结果（合成数据）" if mode == "synthetic" else "HP-0 结果（真人数据）"
    out.append("# %s" % title)
    out.append("")
    out.append("> %s" % (BANNER_SYNTH if mode == "synthetic" else BANNER_UNDER))
    out.append("")
    out.append("生成时间 %s · 输入 `%s` · seed %d · 脚本 analyze_hp0.py v1.0 · 口径见协议 §8" %
               (now, os.path.basename(input_path), seed_used))
    out.append("")

    # E1
    e1 = R["e1"]
    out.append("## E1 最小声明可行性")
    out.append("")
    rows = []
    for r in R["e1_rows"]:
        rows.append([r["pid"], fmt(r["minutes"], 1), fmt(r["prompts"], 0),
                     fmt(r["revisions"], 0), "Y" if r["completed"] else "N",
                     "Y" if r["clean"] else "N"])
    out.append(md_table(["ID", "分钟", "提示", "修订", "完成", "干净"], rows))
    out.append("")
    lo, hi = e1["ci_clean"]
    out.append("- 完成 %d/%d（Wilson 95%% CI %.2f–%.2f）；干净完成（≤15min 且 ≤2 提示）%d/%d（CI %.2f–%.2f）" %
               (e1["k_completed"], e1["n"], e1["ci_completed"][0], e1["ci_completed"][1],
                e1["k_clean"], e1["n"], lo, hi))
    out.append("- 耗时中位数 %s min；提示分布 %s；修订分布 %s" %
               (fmt(e1["median_minutes"], 1),
                sorted(int(x) for x in e1["prompts"]), sorted(int(x) for x in e1["revisions"])))
    out.append("- S-E1 判定（≥8/10 干净完成）：**%s**" % e1["verdict"])
    out.append("")

    # E2
    e2 = R["e2"]
    out.append("## E2 校准重测（W1 vs W2 Brier）")
    out.append("")
    rows = [[r["pid"], fmt(r["w1"], 3), fmt(r["w2"], 3), fmt(r["diff"], 3),
             "是" if r["low_adh"] else ""] for r in R["e2_rows"]]
    out.append(md_table(["ID", "W1", "W2", "差 W2-W1", "低依从"], rows))
    out.append("")
    lo, hi = e2["ci"]
    out.append("- 配对 n=%d；均差 %s，bootstrap 95%% CI %s–%s（B=10^4，参与者重抽样）" %
               (e2["n_paired"], fmt(e2["mean_diff"], 3), fmt(lo, 3), fmt(hi, 3)))
    out.append("- 均值 W1 %s / W2 %s；探索性 Wilcoxon p=%s（BH 后见下表）" %
               (fmt(e2["mean_w1"], 3), fmt(e2["mean_w2"], 3), fmt(e2["p_wilcoxon"], 3)))
    out.append("- 敏感性（剔除低依从）：n=%d，均差 %s" %
               (e2["n_paired_excl_lowadh"], fmt(e2["mean_diff_excl_lowadh"], 3)))
    out.append("- g^(1) 冲动代理（urge 0–4，仅描述）：周均 W1 %s / W2 %s" %
               (fmt(e2["urge_w1"], 2), fmt(e2["urge_w2"], 2)))
    ci_half = (hi - lo) / 2.0 if (not math.isnan(lo) and not math.isnan(hi)) else NAN
    if e2["n_paired"] > 0 and not math.isnan(ci_half) and ci_half > 0.10:
        out.append("- S-E2 预登记备注：CI 半宽 %.2f > 0.10 ⇒ 重测噪声超出可接受测量精度，正式 RCT 前须扩题库/延长测量窗" % ci_half)
    out.append("")

    # E3
    e3 = R["e3"]
    out.append("## E3 课程接受度 / 无回火旗标")
    out.append("")
    rows = []
    for r in R["e3_rows"]:
        rows.append([r["pid"], "W%d" % r["ew"] if r["ew"] else "—",
                     fmt(r["shift_exp"], 2), fmt(r["shift_noexp"], 2),
                     fmt(r["def_exp"], 1), fmt(r["def_noexp"], 1),
                     fmt(r["n_exp_logs"], 0), "Y" if r["paired"] else "N"])
    out.append(md_table(["ID", "暴露周", "shift暴露", "shift无暴露", "防御暴露", "防御无暴露", "暴露日志", "入配对"], rows))
    out.append("")
    out.append("- 配对 n=%d；合并SD s_pool=%s；暴露周 shift 均值=%s；阈值 0.5×s_pool=%s" %
               (e3["n_paired"], fmt(e3["s_pool"], 3), fmt(e3["mean_exp_shift"], 3), fmt(e3["threshold"], 3)))
    if e3["flag"] is None:
        verdict = "无法评估（有效数据不足）"
    elif e3["flag"]:
        verdict = "**BACKFIRE FLAG 升起** ⇒ 按协议 §4.3 暂停暴露组件并再设计（仅可行性旗标，非推断）"
    else:
        verdict = "未升起（仅记录为：未观察到可行性层面的回火信号；不等于证明无回火）"
    out.append("- S-E3 旗标判定：%s" % verdict)
    lo, hi = e3["shift_diff_ci"]
    out.append("- shift 配对差（暴露−无暴露）均值 %s，95%% CI %s–%s；探索性 p=%s" %
               (fmt(e3["shift_diff_mean"], 3), fmt(lo, 3), fmt(hi, 3), fmt(e3["p_shift"], 3)))
    lo, hi = e3["def_diff_ci"]
    out.append("- 防御度配对差均值 %s，95%% CI %s–%s；探索性 p=%s；附加警戒（差>1.0 且 ≥3 人为正）：%s" %
               (fmt(e3["def_diff_mean"], 2), fmt(lo, 2), fmt(hi, 2), fmt(e3["p_def"], 3),
                "触发" if e3["guard"] else "未触发"))
    out.append("- 敏感性（剔除低依从）：n=%d，shift 差均值 %s" %
               (e3["n_paired_excl_lowadh"], fmt(e3["shift_diff_mean_excl_lowadh"], 3)))
    if e3["n_paired"] < 5:
        out.append("- 注：配对集 <5 人，旗标解释力进一步受限（协议 §8.4）。")
    out.append("")

    # BH
    out.append("## 探索性对比族（BH 校正，封闭族 = 3）")
    out.append("")
    rows = []
    for name, (pv, av) in R["bh"].items():
        rows.append([name, fmt(pv, 3), fmt(av, 3)])
    out.append(md_table(["对比", "原始 p", "BH 调整 p"], rows))
    out.append("")
    out.append("全部为**探索性**：BH α=0.05 仅控制此三对比族；结果不构成假设检验结论（协议 SAP/§8.3）。")
    out.append("")

    # adherence
    out.append("## 依从与缺失（不插补，可用例分析）")
    out.append("")
    rows = []
    for r in R["adh_rows"]:
        rows.append([r["pid"], r["days"], fmt(r["adherence"], 2), "是" if r["low"] else "",
                     r["b1"], r["b2"], r["ext_pts"],
                     "Y" if r["e2_in"] else "N", "Y" if r["e3_in"] else "N"])
    out.append(md_table(["ID", "天数", "依从率", "低依从", "W1题数", "W2题数", "极化量点", "E2入组", "E3入组"], rows))
    out.append("")
    out.append("规则：日记缺失日不插补；单周有效预测题 <8 ⇒ 该周 Brier 缺失；"
               "E3 配对要求三个极化量点有效且暴露周日志 ≥1 条；排除均逐人列明（协议 §8.4）。")
    out.append("")
    out.append("## 声明")
    out.append("")
    out.append("- %s" % (BANNER_SYNTH if mode == "synthetic" else BANNER_UNDER))
    out.append("- 论文引用规则：真人数据结果仅在数据采集完成并经 README 规则核对后方可进入稿件；"
                "此前 HP-0 在稿件中一律标注 [designed; data collection pending — no human data exist yet]。")
    out.append("")
    return "\n".join(out)


def console_summary(R, mode, out_path):
    e1, e2, e3 = R["e1"], R["e2"], R["e3"]
    tag = "[DRYRUN-SYNTHETIC]" if mode == "synthetic" else "[HP-0]"
    print("%s underpowered feasibility pilot - no causal claims" % tag)
    print("E1 declaration: %d/%d completed, %d/%d clean (<=15min, <=2 prompts); verdict: %s" %
          (e1["k_completed"], e1["n"], e1["k_clean"], e1["n"], e1["verdict"]))
    print("E2 Brier retest: paired n=%d, mean diff W2-W1=%s, 95%% CI [%s, %s], exploratory p=%s" %
          (e2["n_paired"], fmt(e2["mean_diff"], 3), fmt(e2["ci"][0], 3),
           fmt(e2["ci"][1], 3), fmt(e2["p_wilcoxon"], 3)))
    print("E3 curriculum: paired n=%d, mean exposure shift=%s, threshold 0.5*s_pool=%s, flag=%s" %
          (e3["n_paired"], fmt(e3["mean_exp_shift"], 3), fmt(e3["threshold"], 3),
           {True: "RAISED", False: "not raised", None: "n/a"}[e3["flag"]]))
    print("E3 defensiveness diff=%s (guard=%s)" %
          (fmt(e3["def_diff_mean"], 2), "TRIGGERED" if e3["guard"] else "no"))
    for name, (pv, av) in R["bh"].items():
        print("  BH family: %-38s raw p=%s adj p=%s" % (name, fmt(pv, 3), fmt(av, 3)))
    print("written: %s" % out_path)


# ---------------------------------------------------------------- synthetic

def generate_synthetic(path, seed=SEED):
    """Seed-42 synthetic fixture exercising every code path (incl. missingness)."""
    rng = np.random.default_rng(seed)
    rows = []
    n_part = 10
    for i in range(1, n_part + 1):
        pid = "P%03d" % i
        order_ab = i <= 5
        arm = {1: "EXPOSURE" if order_ab else "NO_EXPOSURE",
               2: "NO_EXPOSURE" if order_ab else "EXPOSURE"}
        base = rng.integers(1, 8, size=3)
        decl_min = int(rng.integers(8, 20))
        prompts = int(rng.integers(0, 4))
        revs = int(rng.integers(0, 4))

        def blank_row(day, week):
            r = {c: "" for c in REQUIRED_COLS}
            r.update({"participant_id": pid, "day": str(day), "week": str(week),
                      "arm": arm[week]})
            return r

        r0 = blank_row(0, 1)
        r0.update({"minutes": str(decl_min + 5), "exposure_count": "0",
                   "extremity_1": str(int(base[0])), "extremity_2": str(int(base[1])),
                   "extremity_3": str(int(base[2])),
                   "declaration_minutes": str(decl_min),
                   "clarifier_prompts": str(prompts),
                   "declaration_revision_count": str(revs)})
        rows.append(r0)

        # exposure days for each exposure week (3 per week)
        exp_days = {}
        for w in (1, 2):
            if arm[w] == "EXPOSURE":
                days = list(range(1, 8)) if w == 1 else list(range(8, 15))
                exp_days[w] = set(int(x) for x in rng.choice(days, size=3, replace=False))
            else:
                exp_days[w] = set()
        # planned missing days (P010 low adherence; plus ~4% random skips)
        skip = set()
        if i == 10:
            skip |= {3, 4, 5, 9}
        drift = {}
        for w in (1, 2):
            drift[w] = rng.normal(0.25, 0.40) if arm[w] == "EXPOSURE" else rng.normal(-0.05, 0.30)
        brier_base = {1: rng.uniform(0.10, 0.28), 2: rng.uniform(0.10, 0.28)}

        for day in range(1, 15):
            w = 1 if day <= 7 else 2
            if day in skip or (day not in (7, 14) and rng.random() < 0.04):
                continue
            r = blank_row(day, w)
            is_exp_day = day in exp_days[w]
            minutes = int(rng.integers(4, 13)) + (6 if is_exp_day else 0)
            defv = int(rng.integers(1, 6))
            if is_exp_day:
                defv = min(7, defv + int(rng.integers(0, 3)))
            r.update({"minutes": str(minutes),
                      "urge_1": str(int(rng.integers(0, 5))),
                      "urge_2": str(int(rng.integers(0, 5))),
                      "urge_3": str(int(rng.integers(0, 5))),
                      "defensiveness": "" if rng.random() < 0.03 else str(defv),
                      "exposure_count": "1" if is_exp_day else "0"})
            if day in (7, 14):
                wk = 1 if day == 7 else 2
                ext = np.clip(np.round(base + drift[wk]), 1, 7).astype(int)
                r.update({"extremity_1": str(int(ext[0])), "extremity_2": str(int(ext[1])),
                          "extremity_3": str(int(ext[2]))})
                items = np.clip(brier_base[wk] + rng.normal(0.0, 0.12, size=10), 0.0, 1.0)
                items = np.round(items, 3)
                if i == 3 and wk == 2:
                    items[7:] = np.nan  # P003 W2: only 7 valid items -> week excluded
                for j in range(10):
                    r[BRIER_COLS[j]] = "" if math.isnan(items[j]) else ("%.3f" % items[j])
            rows.append(r)

    with open(path, "w", newline="", encoding="utf-8") as f:
        wtr = csv.DictWriter(f, fieldnames=REQUIRED_COLS)
        wtr.writeheader()
        for r in rows:
            wtr.writerow(r)
    return len(rows)


# ---------------------------------------------------------------- main

def main(argv=None):
    ap = argparse.ArgumentParser(description="HP-0 feasibility pilot analysis (protocol v1.0 §8)")
    ap.add_argument("--input", default=None, help="participant-day CSV (template-shaped)")
    ap.add_argument("--outdir", default=SCRIPT_DIR, help="output directory (default: script dir)")
    ap.add_argument("--seed", type=int, default=SEED, help="RNG seed (default 42, pre-registered)")
    ap.add_argument("--synthetic-dryrun", action="store_true",
                    help="generate SYNTHETIC seed-42 data and validate the pipeline end-to-end")
    args = ap.parse_args(argv)

    os.makedirs(args.outdir, exist_ok=True)

    if args.synthetic_dryrun:
        mode = "synthetic"
        input_path = os.path.join(args.outdir, "HP0_dryrun_synthetic_data.csv")
        n_rows = generate_synthetic(input_path, seed=args.seed)
        print("[DRYRUN-SYNTHETIC] wrote %d synthetic participant-day rows -> %s" % (n_rows, input_path))
        out_path = os.path.join(args.outdir, "HP0_dryrun_SYNTHETIC.md")
    else:
        mode = "real"
        input_path = args.input
        if input_path is None:
            cand = os.path.join(SCRIPT_DIR, "HP0_data.csv")
            input_path = cand if os.path.exists(cand) else os.path.join(SCRIPT_DIR, "HP0_data_template.csv")
        out_path = os.path.join(args.outdir, "HP0_results.md")

    rows, n_ex = load_rows(input_path)
    if not rows:
        print("No real (non-EXAMPLE) participant rows found in %s." % input_path)
        print("HP-0 remains [designed; data collection pending - no human data exist yet];")
        print("no results file was written. Use --synthetic-dryrun to validate the pipeline.")
        return 3

    parts = aggregate(rows)
    R = analyze(parts)
    md = render_md(R, mode, input_path, args.seed)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(md)
    print("loaded %d real rows (%d EXAMPLE rows skipped); participants: %d" %
          (len(rows), n_ex, len(parts)))
    console_summary(R, mode, out_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
