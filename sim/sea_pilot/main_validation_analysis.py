"""主验证统计分析：四家族（O/C/Q/G）80 run × 73k+ 有效 agent-day 的统一聚合。

口径冻结于 docs/主验证统计分析规约.md（A1–A5）：
- 分析单元 = agent-day；复制单元 = run；推断以 run 为层/重抽样单位（A3-1）。
- 指标：关键召回、价值增量、McNemar/CMH（LLM 判断臂 vs 半 oracle 参数臂）、
  冲动易感性、诚实特征臂参照、有效率（A2-1…A2-6）。
- 禁区：archive_protocol_v1 / archive_family_F 一律拒绝（A1-2）；
  试点旧 tag（无 _rNN 模式）天然不匹配解析器，不混入（A3-4）。

运行：cd sim && python3 -m sea_pilot.main_validation_analysis [--skip-honest]
输出：pilot/results/main_validation_analysis.json + MAIN_VALIDATION_ANALYSIS.md
"""
from __future__ import annotations

import json
import math
import os
import re
import sys
from collections import defaultdict

import numpy as np

from . import config
from .analyze_families import cmh_test, mcnemar_exact

TAG_RE = re.compile(r"^(oa|od|qc|ga|o|c|q|g)_r(\d{2})([a-f])?$")
FAMILY_OF = {"o": "O", "oa": "O", "od": "O", "c": "C",
             "q": "Q", "qc": "Q", "g": "G", "ga": "G"}
EXPECTED_RUNS = {"O": set(range(1, 31)), "C": set(range(1, 31)),
                 "Q": set(range(1, 11)), "G": set(range(1, 11))}
MIN_VALID_PER_RUN = 900          # A1-3：30 主体 × 30 日
REQUIRED_TOTAL_VALID = 72000     # A1-3
FORBIDDEN_SEGMENTS = ("archive_protocol_v1", "archive_family_F")  # A1-2
BOOTSTRAP_B = 10000              # A2-1
BOOTSTRAP_SEED = 42


def parse_tag(tag: str) -> tuple[str, int]:
    """tag → (家族, run 号)。不匹配主验证命名模式即 ValueError（调用方忽略该文件）。"""
    m = TAG_RE.match(tag)
    if not m:
        raise ValueError(f"非主验证 tag：{tag}")
    return FAMILY_OF[m.group(1)], int(m.group(2))


def is_valid(rec: dict) -> bool:
    return bool(rec.get("picked"))


def run_metrics(records: list[dict]) -> dict:
    """A2-1/A2-2/A2-5 + McNemar 计数。无效记录（picked 空）一律剔除。"""
    valid = [r for r in records if is_valid(r)]
    n = len(valid)
    hits = sum(r.get("hits_llm", 0) for r in valid)
    crit = sum(r.get("n_crit", 0) for r in valid)
    dv = [r.get("value_llm", 0.0) - r.get("value_param", 0.0) for r in valid]
    v_llm = sum(r.get("value_llm", 0.0) for r in valid)
    v_par = sum(r.get("value_param", 0.0) for r in valid)
    susc, susc_cond, n_inj_days = [], [], 0
    for r in valid:
        inj = set(r.get("injected") or [])
        imp = set(r.get("impulse_consumed") or [])
        s = len(imp & inj) / max(len(inj), 1)
        susc.append(s)
        if inj:
            n_inj_days += 1
            susc_cond.append(s)
    b = sum(1 for r in valid if r.get("hits_llm", 0) > r.get("hits_param", 0))
    c = sum(1 for r in valid if r.get("hits_llm", 0) < r.get("hits_param", 0))
    return {
        "n_valid": n,
        "recall": hits / crit if crit else 0.0,
        "dvalue": float(np.mean(dv)) if dv else 0.0,
        "value_ratio": v_llm / v_par if v_par else 0.0,
        "impulse_susc": float(np.mean(susc)) if susc else 0.0,
        "impulse_susc_cond": float(np.mean(susc_cond)) if susc_cond else 0.0,
        "n_injected_days": n_inj_days,
        "mcnemar_b": b, "mcnemar_c": c,
    }


def load_dataset(results_dir: str) -> dict[str, dict[int, list[dict]]]:
    """A1：读入四家族数据并过完整性闸门。任何违例 → SystemExit（非零）。"""
    norm = os.path.normpath(os.path.abspath(results_dir))
    if any(seg in norm.split(os.sep) for seg in FORBIDDEN_SEGMENTS):
        print(f"[禁区守卫] 拒绝读取归档目录：{results_dir}", file=sys.stderr)
        raise SystemExit(2)
    runs: dict[str, dict[int, list[dict]]] = {f: defaultdict(list) for f in EXPECTED_RUNS}
    src_prefix: dict[tuple[str, int], str] = {}
    skipped = []
    for fn in sorted(os.listdir(results_dir)):
        if not (fn.startswith("llm_replay_") and fn.endswith(".jsonl")):
            continue
        tag = fn[len("llm_replay_"):-len(".jsonl")]
        try:
            fam, run_no = parse_tag(tag)
        except ValueError:
            skipped.append(tag)      # 试点旧 tag / 电池产物，不混入（A3-4）
            continue
        prefix = TAG_RE.match(tag).group(1)
        key = (fam, run_no)
        if key in src_prefix and src_prefix[key] != prefix:
            print(f"[seed 守卫] 家族 {fam} run {run_no} 双重来源 "
                  f"（{src_prefix[key]} 与 {prefix}），拒绝", file=sys.stderr)
            raise SystemExit(3)
        src_prefix[key] = prefix
        with open(os.path.join(results_dir, fn), encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    runs[fam][run_no].append(json.loads(line))
    # A1-3 完整性闸门
    problems = []
    total_valid = 0
    for fam, want in EXPECTED_RUNS.items():
        got = set(runs[fam])
        if got != want:
            problems.append(f"家族 {fam} run 集合缺失：{sorted(want - got)}")
        for r in sorted(got & want):
            n_valid = sum(1 for rec in runs[fam][r] if is_valid(rec))
            total_valid += n_valid
            if n_valid < MIN_VALID_PER_RUN:
                problems.append(f"家族 {fam} run {r} 有效 {n_valid} < {MIN_VALID_PER_RUN}")
    if total_valid < REQUIRED_TOTAL_VALID:
        problems.append(f"总有效 {total_valid} < {REQUIRED_TOTAL_VALID}")
    if problems:
        for p in problems:
            print(f"[完整性闸门] {p}", file=sys.stderr)
        raise SystemExit(4)
    if skipped:
        print(f"[口径] 跳过非主验证文件 {len(skipped)} 个：{', '.join(skipped)}",
              file=sys.stderr)
    return {fam: dict(d) for fam, d in runs.items()}


def bootstrap_ci(values: list[float], b: int = BOOTSTRAP_B,
                 seed: int = BOOTSTRAP_SEED) -> tuple[float, float]:
    """A2-1：run 级重抽样 percentile 95% CI。"""
    arr = np.asarray(values, float)
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(arr), size=(b, len(arr)))
    means = arr[idx].mean(axis=1)
    return float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


def bh_adjust(pvals: list[float]) -> list[float]:
    """A3-3：Benjamini–Hochberg 校正（保持输入顺序返回）。"""
    m = len(pvals)
    order = sorted(range(m), key=lambda i: pvals[i])
    adj = [0.0] * m
    running = 1.0
    for rank, i in reversed(list(enumerate(order, start=1))):
        running = min(running, pvals[i] * m / rank)
        adj[i] = min(1.0, running)
    return adj


def analyze(ds: dict[str, dict[int, list[dict]]], honest_arm: bool = True) -> dict:
    fam_out = {}
    strata_all = []
    n_valid_total = 0
    for fam in ("O", "C", "Q", "G"):
        per_run = {r: run_metrics(recs) for r, recs in sorted(ds[fam].items())}
        recalls = [m["recall"] for m in per_run.values()]
        b = sum(m["mcnemar_b"] for m in per_run.values())
        c = sum(m["mcnemar_c"] for m in per_run.values())
        strata_all.extend((m["mcnemar_b"], m["mcnemar_c"]) for m in per_run.values())
        n_valid_total += sum(m["n_valid"] for m in per_run.values())
        fam_out[fam] = {
            "n_runs": len(per_run),
            "n_valid": sum(m["n_valid"] for m in per_run.values()),
            "recall_mean": float(np.mean(recalls)),
            "recall_ci95": list(bootstrap_ci(recalls)),
            "recall_runs": recalls,
            "dvalue_mean": float(np.mean([m["dvalue"] for m in per_run.values()])),
            "value_ratio_mean": float(np.mean([m["value_ratio"] for m in per_run.values()])),
            "impulse_susc_mean": float(np.mean([m["impulse_susc"] for m in per_run.values()])),
            "impulse_susc_cond_mean": float(np.mean([m["impulse_susc_cond"]
                                                     for m in per_run.values()])),
            "mcnemar_b": b, "mcnemar_c": c,
            "mcnemar_p": mcnemar_exact(b, c),
            "per_run": {str(r): m for r, m in per_run.items()},
        }
    fams = ["O", "C", "Q", "G"]
    adj = bh_adjust([fam_out[f]["mcnemar_p"] for f in fams])
    for f, a in zip(fams, adj):
        fam_out[f]["mcnemar_p_bh"] = a
    out = {
        "protocol": "v2.1 / 主验证统计分析规约 A1–A5",
        "families": fam_out,
        "pooled_cmh": list(cmh_test(strata_all)),
        "n_valid_total": n_valid_total,
    }
    if honest_arm:
        from .analyze_families import build_honest_arm
        hh, opp = build_honest_arm()
        honest_recall = sum(hh.values()) / sum(opp.values()) if opp else 0.0
        out["honest_arm"] = {"recall": honest_recall,
                             "n_days": len(hh),
                             "crit_opp": int(sum(opp.values()))}
    return out


def render_md(out: dict) -> str:
    lines = ["# 主验证统计分析报告（协议 v2.1，四家族 80 run）", ""]
    lines.append("| 家族 | run | 有效记录 | 关键召回 [95% CI] | Δvalue | 价值比 | "
                 "McNemar p (BH) | 冲动易感性 |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for f in ("O", "C", "Q", "G"):
        a = out["families"][f]
        lo, hi = a["recall_ci95"]
        lines.append(
            f"| {f} | {a['n_runs']} | {a['n_valid']} | "
            f"{a['recall_mean']:.3f} [{lo:.3f}, {hi:.3f}] | "
            f"{a['dvalue_mean']:+.3f} | {a['value_ratio_mean']:.3f}× | "
            f"{a['mcnemar_p']:.2e} ({a['mcnemar_p_bh']:.2e}) | "
            f"{a['impulse_susc_mean']:.3f} |")
    chi2, p = out["pooled_cmh"]
    lines += ["", f"**跨家族合并 CMH（以 run 为层，80 层）**：χ²₁={chi2:.2f}，p={p:.3e}",
              f"**总有效记录**：{out['n_valid_total']}"]
    if "honest_arm" in out:
        h = out["honest_arm"]
        lines.append(f"**诚实特征臂参照**：召回 {h['recall']:.3f}"
                     f"（{h['n_days']} 天，关键机会 {h['crit_opp']}）")
    lines += ["", "_口径：分析单元 agent-day，复制单元 run；推断以 run 为层（规约 A3-1）。"
              " F 家族已裁撤（R-18），其归档数据未进入本分析。_"]
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    skip_honest = "--skip-honest" in argv
    ds = load_dataset(config.RESULTS_DIR)
    out = analyze(ds, honest_arm=not skip_honest)
    jpath = os.path.join(config.RESULTS_DIR, "main_validation_analysis.json")
    mpath = os.path.join(config.RESULTS_DIR, "MAIN_VALIDATION_ANALYSIS.md")
    with open(jpath, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    with open(mpath, "w", encoding="utf-8") as f:
        f.write(render_md(out))
    print(f"已写出 {jpath}\n已写出 {mpath}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
