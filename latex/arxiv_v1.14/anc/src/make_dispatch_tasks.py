"""生成三节点调度的任务清单（规约 L-4 子车道分片版）。

车道—角色分配（规约 R-5，满足 ≥3 家族分离 + 按实测吞吐配载 + 规约 L-4 并发分片）：
  O1/O2/O3 (ornith-1.5-35b, Mac Studio)：主力车道，3 并发分片（Mac 实测有余量）
  C1..C6   (ling-3.0-flash, OpenRouter 付费)：主力车道，6 并发分片（~5s/调用，~$3 总成本）
  Q        (qwen3.8-27b,    node-a)    ：锚点车道（GPU 饱和，单流）
  G1/G2    (gemma4:26b,     node-d)    ：锚点车道（已降为 10 run），2 分片
  F        (nemotron-3-super-120b:free, OpenRouter 免费)：锚点车道，单流 + 配额节拍

注意：当前仅 run_llm_replay / h8_battery_v2 / h9_calibration 可直接调度。
处理臂（S0–S3 × 对抗环境）的臂感知主验证模块尚未实现（论文表 14-1 标 [进行中]/[设计]），
本生成器把臂级单元写成注释行（lane_runner 会跳过），待模块落地后取消注释即可。

用法：python3 -m sea_pilot.make_dispatch_tasks [输出目录，默认 ../dispatch_tasks]
"""
from __future__ import annotations

import os
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "dispatch_tasks")
os.makedirs(OUT, exist_ok=True)

# ---- 可调参数（预注册口径见论文 §15.2；调度规约 docs/主验证调度规约.md）----
DAYS = 30                 # 规约 P-1：重放语料仅 30 模拟日（arXiv 2019-09）；90 日须待语料扩展
AGENTS_PER_RUN = 30       # 缩减版队列（试点 N_AGENTS=30 口径；全规模 100–300 需 API 补充）
N_RUNS = 30               # 主力车道（O/C）每单元预注册 run 数（≥30）
N_RUNS_ANCHOR = 10        # 锚点车道（Q/G/F）run 数（规约 R-5：G 已降为锚点）
SHARDS = {"O": [(0, 10), (10, 10), (20, 10)],   # 规约 L-4：3 并发分片
          "G": [(0, 15), (15, 15)],             # 2 分片（待 NUM_PARALLEL 生效）
          "C": [(i * 5, 5) for i in range(6)]}  # 云车道 6 分片（L-4 修订：云 ≤8）
SEED_BASE = {"O": 0, "G": 0, "Q": 100, "C": 200}
ARMS_MAIN = ("S0", "S1", "S2", "S3")
ARMS_ABLATION = ("S2a", "S2b", "S2c")

lanes: dict[str, list[str]] = {}

# --- O/C 家族：分片独立复制（--seed 保证真独立；断点续跑由 jsonl 日志保证）---
# 规约 R-16：O 的 run 1–22 留在 Mac（O1/O2/O3），run 23–30 由 node-a/node-d 转产承担
for fam, n_runs in (("O", 22), ("C", N_RUNS)):
    for si, (start, n_ag) in enumerate(SHARDS[fam], start=1):
        lane = f"{fam}{si}"
        tasks = []
        for r in range(1, n_runs + 1):
            tag = f"{fam.lower()}_r{r:02d}{chr(96 + si)}"   # o_r01a / c_r01f / ...
            tasks.append(
                f"sea_pilot.run_llm_replay --days {DAYS} --agents {n_ag} "
                f"--agent-start {start} --seed {SEED_BASE[fam] + r} --tag {tag}")
        if si == 1:
            # H8/H9 验证电池（换版或主 run 前必须重跑锚点，§15.2 统计规范；tag 全局唯一）
            tasks.append(f"sea_pilot.h8_battery_v2 --model-tag {fam.lower()}90_h8 --n-a 20 --n-b 10 --n-c 20")
            tasks.append(f"sea_pilot.h9_calibration --tag {fam.lower()}90_h9")
            for arm in ARMS_MAIN + ARMS_ABLATION:
                tasks.append(
                    f"# [待模块] 臂 {arm} × 30 run × {DAYS}日：待 run_main_validation.py（表14-1 [进行中]）")
        lanes[lane] = tasks

# --- O 家族增援（规约 R-16）：node-a（OA1/OA2）run 23–28，node-d（OD1/OD2）run 29–30 ---
for node_tag, run_range in (("A", range(23, 29)), ("D", range(29, 31))):
    for si, (start, n_ag) in enumerate(((0, 15), (15, 15)), start=1):
        lane = f"O{node_tag}{si}"
        lanes[lane] = [
            f"sea_pilot.run_llm_replay --days {DAYS} --agents {n_ag} "
            f"--agent-start {start} --seed {r} --tag o{node_tag.lower()}_r{r:02d}{chr(96 + si)}"
            for r in run_range
        ]

# --- G 家族（规约 R-11 双节点，负载按实测速率配比）---
# node-d（G1/G2，~12 tok/s）承担 run 1–3；node-a（GA1/GA2，~28 tok/s，num_ctx=4096）承担 run 4–10
for node_tag, run_range in (("", range(1, 4)), ("A", range(4, 11))):
    for si, (start, n_ag) in enumerate(SHARDS["G"], start=1):
        lane = f"G{node_tag}{si}"
        tasks = []
        for r in run_range:
            tag = f"g{node_tag.lower()}_r{r:02d}{chr(96 + si)}"   # g_r01a / ga_r06a / ...
            tasks.append(
                f"sea_pilot.run_llm_replay --days {DAYS} --agents {n_ag} "
                f"--agent-start {start} --seed {r} --tag {tag}")
        if si == 1 and not node_tag:
            tasks.append("sea_pilot.h8_battery_v2 --model-tag g90_h8 --n-a 20 --n-b 10 --n-c 20")
            tasks.append("sea_pilot.h9_calibration --tag g90_h9")
        lanes[lane] = tasks

# --- Q：qwen 家族（规约 R-11：全量上云）---
# 本地仅保留已完成的 run 1（账目行，旗标已盖）；QC 承担 run 2–10 + 验证电池
lanes["Q"] = [
    f"sea_pilot.run_llm_replay --days {DAYS} --agents {AGENTS_PER_RUN} "
    f"--agent-start 0 --seed 101 --tag q_r01",
]
qc = []
for r in range(2, N_RUNS_ANCHOR + 1):
    qc.append(f"sea_pilot.run_llm_replay --days {DAYS} --agents {AGENTS_PER_RUN} "
              f"--agent-start 0 --seed {SEED_BASE['Q'] + r} --tag qc_r{r:02d}")
qc.append("sea_pilot.h8_battery_v2 --model-tag q90_h8 --n-a 20 --n-b 10 --n-c 20")
qc.append("sea_pilot.h9_calibration --tag q90_h9")
lanes["QC"] = qc

# --- F 家族已裁撤（规约 R-18，2026-10-12）：产物归档 archive_family_F/，不纳入主分析 ---

for lane, tasks in lanes.items():
    path = os.path.join(OUT, f"tasks_{lane}.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# Lane {lane} 任务清单（{len(tasks)} 条）——由 make_dispatch_tasks.py 生成\n")
        f.write("\n".join(tasks) + "\n")
    print(f"lane {lane}: {len(tasks)} tasks -> {path}")
