"""三车道调度进度条（调度规约 R-3）。

数据源仅为任务清单、完成旗标与 jsonl 日志——不依赖进程状态猜测，
进程崩溃后进度显示依然正确。

用法：cd sim && python3 -m sea_pilot.dispatch_progress [--watch 秒数]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import time
from pathlib import Path

SIM_DIR = Path(__file__).resolve().parent.parent
FAMILY_LABEL = {"O": "ornith-1.5-35b @MacStudio", "Q": "qwen3.8-27b @node-a",
                "G": "gemma4:26b   @node-d"}


def _lane_ids(sim_dir: Path) -> list[str]:
    """从任务清单文件发现车道 id（含子车道 O1/O2/...）。"""
    tasks_dir = sim_dir / "dispatch_tasks"
    if not tasks_dir.exists():
        return []
    return sorted(f.stem[len("tasks_"):] for f in tasks_dir.glob("tasks_*.txt"))


def _read_tasks(sim_dir: Path, lane: str) -> list[str]:
    path = sim_dir / "dispatch_tasks" / f"tasks_{lane}.txt"
    if not path.exists():
        return []
    return [ln.strip() for ln in path.read_text(encoding="utf-8").splitlines()
            if ln.strip() and not ln.startswith("#")]


def _done_flags(sim_dir: Path, lane: str) -> set[str]:
    flag_dir = sim_dir / "pilot" / "results" / "dispatch_flags"
    if not flag_dir.exists():
        return set()
    return {p.name[len(lane) + 1:-len(".done")] for p in flag_dir.glob(f"{lane}_*.done")
            if p.name != f"{lane}_ALL.done"}


def _count_records(sim_dir: Path, tag: str) -> tuple[int, int]:
    """返回 (有效记录数, 空选择记录数)——规约 V-3：空选择不计完成。"""
    path = sim_dir / "pilot" / "results" / f"llm_replay_{tag}.jsonl"
    if not path.exists():
        return 0, 0
    ok = empty = 0
    with open(path, encoding="utf-8") as f:
        for line in f:
            try:
                r = json.loads(line)
            except Exception:  # noqa: BLE001
                continue
            if "agent" not in r:
                continue
            if r.get("picked"):
                ok += 1
            else:
                empty += 1
    return ok, empty


def compute_progress(sim_dir: Path | str) -> dict[str, dict]:
    sim_dir = Path(sim_dir)
    out: dict[str, dict] = {}
    for lane in _lane_ids(sim_dir):
        tasks = _read_tasks(sim_dir, lane)
        flags = _done_flags(sim_dir, lane)
        tasks_done = sum(1 for t in tasks
                         if hashlib.md5(t.encode()).hexdigest()[:12] in flags)
        records_done = records_total = 0
        for t in tasks:
            words = t.split()
            if words[0] != "sea_pilot.run_llm_replay":
                continue
            tag = words[words.index("--tag") + 1]
            days = int(words[words.index("--days") + 1])
            agents = int(words[words.index("--agents") + 1])
            ok, _empty = _count_records(sim_dir, tag)
            records_done += ok
            records_total += days * agents
        # 综合进度：非 replay 任务按任务粒度、replay 任务按记录粒度
        replay_tasks = [t for t in tasks if t.startswith("sea_pilot.run_llm_replay")]
        other_tasks = [t for t in tasks if not t.startswith("sea_pilot.run_llm_replay")]
        other_done = sum(1 for t in other_tasks
                         if hashlib.md5(t.encode()).hexdigest()[:12] in flags)
        units_total = records_total + len(other_tasks)
        units_done = records_done + other_done
        out[lane] = {
            "tasks_total": len(tasks), "tasks_done": tasks_done,
            "replay_tasks": len(replay_tasks),
            "records_done": records_done, "records_total": records_total,
            "fraction": units_done / units_total if units_total else 0.0,
            "all_done": (sim_dir / "pilot" / "results" / "dispatch_flags"
                         / f"{lane}_ALL.done").exists(),
        }
    return out


def render_bar(fraction: float, width: int = 30) -> str:
    fraction = max(0.0, min(1.0, fraction))
    filled = int(round(fraction * width))
    return f"[{'#' * filled}{'.' * (width - filled)}] {fraction * 100:5.1f}%"


def render(sim_dir: Path | str) -> str:
    prog = compute_progress(sim_dir)
    lines = []
    total_done = total_units = 0
    for lane in sorted(prog):
        p = prog[lane]
        mark = " ✅" if p["all_done"] else ""
        lines.append(
            f"  子车道 {lane:3s} {render_bar(p['fraction'], 20)}  "
            f"任务 {p['tasks_done']}/{p['tasks_total']}  "
            f"记录 {p['records_done']}/{p['records_total']}{mark}")
        total_done += p["records_done"] + (p["tasks_done"] - 0)
        total_units += p["records_total"] + (p["tasks_total"] - p["replay_tasks"])
    # 家族聚合行
    fam_lines = []
    for fam in sorted({lane[0] for lane in prog}):
        members = [prog[l] for l in prog if l[0] == fam]
        done = sum(m["records_done"] + m["tasks_done"] for m in members)
        total = sum(m["records_total"] + (m["tasks_total"] - m["replay_tasks"]) for m in members)
        frac = done / total if total else 0.0
        fam_lines.append(f"车道 {fam} ({FAMILY_LABEL.get(fam, '?')}) {render_bar(frac)}")
    overall = total_done / total_units if total_units else 0.0
    return "\n".join(fam_lines + lines + [f"总体 {render_bar(overall)}"])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--watch", type=float, default=0, help="刷新间隔秒数（0=只打印一次）")
    args = ap.parse_args()
    while True:
        text = render(SIM_DIR)
        if args.watch <= 0:
            print(text)
            return
        os.system("clear")
        print(text)
        print(f"\n（每 {args.watch:g}s 刷新，Ctrl-C 退出）")
        time.sleep(args.watch)


if __name__ == "__main__":
    main()
