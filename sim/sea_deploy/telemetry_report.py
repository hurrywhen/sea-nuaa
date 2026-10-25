"""遥测周报生成器：python3 -m sea_deploy.telemetry_report [--path out/telemetry.jsonl]"""
from __future__ import annotations

import json
import os
import sys

from sea_deploy import telemetry

HERE = os.path.dirname(os.path.abspath(__file__))


def main() -> None:
    path = sys.argv[sys.argv.index("--path") + 1] if "--path" in sys.argv \
        else os.path.join(HERE, "out", "telemetry.jsonl")
    rep = telemetry.weekly_report(path)
    if not rep.get("n_days"):
        print("[telemetry] 无记录")
        return
    L = ["# SEA 团队自用遥测周报（阶段四 L2 转移桥·团队自用侧）\n",
         f"窗口：{rep['first_day']} → {rep['last_day']}（{rep['n_days']} 个运行日）\n",
         "| 量 | 值 |", "|---|---|",
         f"| 抓取命题总数 | {rep['n_fetched_total']} |",
         f"| 深读选中总数 | {rep['n_selected_total']}（选择率 {rep['select_rate']:.1%}） |",
         f"| A9 隔离总数 | {rep['quarantined_total']} |",
         f"| LLM 判断层启用天数 | {rep['llm_days']} |",
         f"| LLM×参数化 top-k 一致率均值 | {rep['llm_agreement_mean']} |",
         f"| 按画像运行日 | {rep['per_persona_days']} |",
         "\n## 决策集触及频次（g² 审计）\n",
         "| 决策 | 天数 |", "|---|---|"]
    for d, c in rep["decisions_informed"].items():
        L.append(f"| {d} | {c} |")
    L += ["\n## θ_cal 纵向追踪（A10）\n", f"- {rep['theta_cal_note']}；",
          "- 转移桥含义：团队自用遥测 = L2 锚点的『真实使用』侧数据，与 AI 队列（L1）对照，"
          "为 AI→人 转移系数（O6）提供第一批真实使用条目。"]
    out = os.path.join(os.path.dirname(path), "TELEMETRY_REPORT.md")
    open(out, "w", encoding="utf-8").write("\n".join(L))
    print(json.dumps(rep, ensure_ascii=False, indent=1))
    print(f"[telemetry] report -> {out}")


if __name__ == "__main__":
    main()
