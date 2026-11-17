"""LLM 智能体层 × P3 真实重放：真实后端在 arXiv 2019-09 语料上做消费决策，与参数化选择器同题对照。

协议（docs/AI智能体实验设计.md §2.2）：
  - 框架层：每日 digest = 通道 I（机构清单直通）全量 + 通道 II proxy 预排序补足至 18 条；
    预算 m=3/日框架强制；S4 审计日志逐日落盘（含冲动注入标记）。
  - LLM 层：persona 卡（P3）+ 决策集声明 → JSON 选择。
  - 对照臂：同一 digest 按 proxy 分数取 top-m（参数化选择器）。
  - 结局：命中 E*（top2% 被引真值）、捕获价值 Σlog1p(cit)。

支持断点续跑：--tag 隔离输出；jsonl 追加模式；已完成的 (agent, day) 自动跳过。
运行：cd sim && python3 -m sea_pilot.run_llm_replay [--days 30] [--agents 8] [--tag ornith30]
"""
from __future__ import annotations

import json
import math
import os
import sys

import numpy as np

from . import config, corpus as cp
from .agents_llm import DigestItem, LLMAgent, MockBackend, OpenAICompatBackend, P3_CARD


def build_days(universe, critical, watchlist, proxy_seed: int = 99):
    rng = np.random.default_rng(proxy_seed)
    zi = np.array([math.log1p(r["cit"]) for r in universe])
    zi = (zi - zi.mean()) / (zi.std() + 1e-9)
    proxy = 0.4 * zi + math.sqrt(1 - 0.16) * rng.standard_normal(len(universe))
    by_day: dict[int, list[int]] = {}
    for i, r in enumerate(universe):
        by_day.setdefault(cp.day_index(r), []).append(i)
    days = []
    for d in sorted(by_day):
        idx = by_day[d]
        ch1 = [i for i in idx if any(e in watchlist["ids"] for e in universe[i]["insts"])]
        ch2 = [i for i in sorted(idx, key=lambda j: -proxy[j]) if i not in set(ch1)]
        digest = (ch1 + ch2)[:18]
        days.append({"day": d, "digest": digest,
                     "critical": [i for i in digest if universe[i]["arxiv_id"] in critical],
                     "proxy_rank": sorted(digest, key=lambda j: -proxy[j])})
    return days


def _arg(name: str, default):
    if f"--{name}" in sys.argv:
        return sys.argv[sys.argv.index(f"--{name}") + 1]
    return default


def verify_complete(log_path: str, expected: int) -> int:
    """规约 WU-4 完整性闸门：返回缺失的有效 agent-day 数（0 = 完整）。

    空选择（picked 为空）不计入有效记录——与续跑清理语义一致。
    """
    try:
        valid = 0
        with open(log_path, encoding="utf-8") as f:
            for line in f:
                try:
                    r = json.loads(line)
                except Exception:  # noqa: BLE001
                    continue
                if r.get("picked") and "agent" in r:
                    valid += 1
    except FileNotFoundError:
        return expected
    return max(0, expected - valid)


def main() -> None:
    days_n = int(_arg("days", 30))
    agents_n = int(_arg("agents", 8))
    agent_start = int(_arg("agent-start", 0))
    seed = int(_arg("seed", 0))   # 独立复制的 run 种子（主验证 ≥30 run 依赖此参数）
    tag = str(_arg("tag", "default"))
    universe, critical, watchlists, stats = cp.build_all()
    days = build_days(universe, critical, watchlists["inst"], proxy_seed=99 + seed)[:days_n]
    print(f"[llm-replay:{tag}] {len(days)} 模拟日 × agents[{agent_start}:{agent_start+agents_n}], "
          f"digest≤18/日", flush=True)

    try:
        backend = OpenAICompatBackend()
        bname = f"openai-compat:{backend.model}"
    except RuntimeError as e:
        if os.environ.get("SEA_REQUIRE_REAL_BACKEND") == "1":
            # 调度模式（lane_runner 注入）：禁止 Mock 回退，防 Mock 数据冒充真实记录
            print(f"[llm-replay:{tag}] 真实后端不可用（{e}），调度模式禁用 Mock 回退，退出码 2",
                  flush=True)
            sys.exit(2)
        print(f"[llm-replay:{tag}] 真实后端不可用（{e}），回退 MockBackend（仅管线验证）", flush=True)
        backend = MockBackend()
        bname = "mock"

    log_path = os.path.join(config.RESULTS_DIR, f"llm_replay_{tag}.jsonl")
    done: set[tuple[int, int]] = set()
    if os.path.exists(log_path):
        kept = []
        for line in open(log_path, encoding="utf-8"):
            try:
                r = json.loads(line)
            except Exception:  # noqa: BLE001
                continue
            if r.get("picked") and "agent" in r:      # 仅非空选择算完成（空选择重试）
                done.add((r["agent"], r["day"]))
                kept.append(line)
        # 清理误判记录（解析缺陷期写入的空选择），使其可被重试
        with open(log_path, "w", encoding="utf-8") as f:
            f.writelines(kept)
        print(f"[llm-replay:{tag}] 续跑：已完成 {len(done)} 个 agent-day（空选择记录已清理重试）",
              flush=True)

    for ai in range(agent_start, agent_start + agents_n):
        agent = LLMAgent(P3_CARD, backend, seed=seed * 1000 + ai, log_path=None)  # 日志由本脚本写增强版记录
        agent.card.budget_per_day = 3
        for dd in days:
            if (ai, dd["day"] + 1) in done:
                continue
            items = [DigestItem(universe[i]["arxiv_id"],
                                universe[i]["title"][:90],
                                (universe[i]["insts"][:1] or ["?"])[0],
                                channel=("I" if any(e in watchlists["inst"]["ids"]
                                                    for e in universe[i]["insts"]) else "II"))
                     for i in dd["digest"]]
            rec = agent.daily_step(items)
            rec["agent"] = ai
            rec["sim_day"] = dd["day"]
            # 结局由框架计算（不信任 LLM 自报）
            picked_ids = set(rec["picked"])
            crit_ids = {universe[i]["arxiv_id"] for i in dd["critical"]}
            par_ids = {universe[i]["arxiv_id"] for i in dd["proxy_rank"][:3]}
            rec["hits_llm"] = len(picked_ids & crit_ids)
            rec["hits_param"] = len(par_ids & crit_ids)
            rec["n_crit"] = len(crit_ids)
            rec["value_llm"] = sum(math.log1p(universe[i]["cit"]) for i in dd["digest"]
                                   if universe[i]["arxiv_id"] in picked_ids)
            rec["value_param"] = sum(math.log1p(universe[i]["cit"]) for i in dd["digest"]
                                     if universe[i]["arxiv_id"] in par_ids)
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        print(f"[llm-replay:{tag}] agent{ai} 完成（累计 {len(done) + 0}+）", flush=True)

    # summary 从日志全量重建（含续跑历史）
    recs = [json.loads(l) for l in open(log_path, encoding="utf-8")]
    ok = [r for r in recs if r.get("picked")]
    n_crit = sum(r.get("n_crit", 0) for r in recs)
    summary = {
        "tag": tag, "backend": bname, "records": len(recs), "valid_days": len(ok),
        "recall_llm": sum(r.get("hits_llm", 0) for r in recs) / max(1, n_crit),
        "recall_param": sum(r.get("hits_param", 0) for r in recs) / max(1, n_crit),
        "value_llm_mean": float(np.mean([r.get("value_llm", 0) for r in recs])) if recs else 0,
        "value_param_mean": float(np.mean([r.get("value_param", 0) for r in recs])) if recs else 0,
        "impulse_injected": sum(len(r.get("injected", [])) for r in recs),
        "impulse_consumed": sum(len(r.get("impulse_consumed", [])) for r in recs),
        "n_crit_opportunities": n_crit,
    }
    summary["impulse_rate"] = (summary["impulse_consumed"] / max(1, summary["impulse_injected"]))
    json.dump(summary, open(os.path.join(config.RESULTS_DIR, f"llm_replay_summary_{tag}.json"),
                            "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"[llm-replay:{tag}] SUMMARY recall LLM={summary['recall_llm']:.3f} vs "
          f"param={summary['recall_param']:.3f} | value {summary['value_llm_mean']:.1f} vs "
          f"{summary['value_param_mean']:.1f} | impulse {summary['impulse_consumed']}/"
          f"{summary['impulse_injected']} ({summary['impulse_rate']:.1%})", flush=True)
    # 规约 WU-4 完整性闸门：缺有效 agent-day 则非零退出，lane_runner 不得盖完成旗标
    expected = len(days) * agents_n
    missing = verify_complete(log_path, expected)
    if missing:
        print(f"[llm-replay:{tag}] INCOMPLETE: 缺 {missing}/{expected} 个有效 agent-day，"
              f"退出码 1（重跑自动续补，见规约 WU-4/R-1）", flush=True)
        sys.exit(1)
    print(f"[llm-replay:{tag}] done -> {log_path}", flush=True)


if __name__ == "__main__":
    main()
