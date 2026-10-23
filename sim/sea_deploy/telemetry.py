"""阶段四团队自用遥测：schema + 原子追加 + 周报聚合。

遥测是论文 §15.3 转移桥 L2 的「团队自用」侧——记录智能体（团队成员）每日
所见/所选/所隔离，以及 θ_cal 预测，作为 AI→人 转移系数的真实使用锚点。
隐私：本地优先（local-first），不外发；S4 审计日志同源。
"""
from __future__ import annotations

import json
import os
import tempfile
from collections import defaultdict
from datetime import datetime, timezone

SCHEMA_VERSION = "1.0"

# 每条遥测记录的字段契约（daily_run 写入）
FIELDS = {
    "schema": "遥测 schema 版本",
    "ts": "UTC ISO 时间戳",
    "date": "信息流日期（YYYY-MM-DD）",
    "pid": "画像 id（g² 声明）",
    "domain": "域标签（academic_single_source / financial_multi_class）",
    "n_fetched": "当日抓取的命题（论文）数",
    "n_channel_I": "通道 I（清单直通）候选数",
    "n_channel_II": "通道 II（评分发现）候选数",
    "allocation": "名额分配 {I,II,Q}",
    "selected": "选中项 [{id,title,score,decision,channel}]",
    "quarantined": "A9 防火墙隔离数（arXiv 无 salience 信号 → 0）",
    "llm_used": "是否启用 LLM 判断层",
    "llm_model": "LLM 模型名（含 think 配置）",
    "llm_agreement": "LLM 重排与参数化排序的 top-k 一致率（θ 校准的在线锚）",
    "top_decisions_informed": "当日简报触及的决策集条目",
}


def _atomic_append(path: str, line: str) -> None:
    """单写者原子追加（团队串行运行）：append + flush + fsync。"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(line.rstrip("\n") + "\n")
        f.flush()
        os.fsync(f.fileno())


def append_record(path: str, rec: dict) -> None:
    rec = {"schema": SCHEMA_VERSION, "ts": datetime.now(timezone.utc).isoformat(), **rec}
    _atomic_append(path, json.dumps(rec, ensure_ascii=False))


def atomic_write(path: str, text: str) -> None:
    """简报等文件的原子落盘（temp + rename，抗中断）。"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path), suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(text)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def load_records(path: str) -> list[dict]:
    if not os.path.exists(path):
        return []
    out = []
    for ln in open(path, encoding="utf-8"):
        ln = ln.strip()
        if ln:
            try:
                out.append(json.loads(ln))
            except json.JSONDecodeError:
                continue
    return out


def weekly_report(path: str) -> dict:
    """聚合自用遥测为周报（S4 审计 + θ_cal 纵向追踪底座）。"""
    recs = load_records(path)
    if not recs:
        return {"n_days": 0}
    n = len(recs)
    fetched = sum(r.get("n_fetched", 0) for r in recs)
    selected = sum(len(r.get("selected", [])) for r in recs)
    quarantined = sum(r.get("quarantined", 0) for r in recs)
    llm_days = sum(1 for r in recs if r.get("llm_used"))
    agree = [r["llm_agreement"] for r in recs if r.get("llm_agreement") is not None]
    dec_counts: dict = defaultdict(int)
    for r in recs:
        for d in r.get("top_decisions_informed", []):
            dec_counts[d] += 1
    per_pid = defaultdict(int)
    for r in recs:
        per_pid[r.get("pid", "?")] += 1
    return {
        "n_days": n, "n_fetched_total": fetched, "n_selected_total": selected,
        "select_rate": round(selected / max(1, fetched), 4),
        "quarantined_total": quarantined,
        "llm_days": llm_days,
        "llm_agreement_mean": round(sum(agree) / len(agree), 3) if agree else None,
        "decisions_informed": dict(sorted(dec_counts.items(), key=lambda x: -x[1])),
        "per_persona_days": dict(per_pid),
        "first_day": recs[0].get("date"), "last_day": recs[-1].get("date"),
        "theta_cal_note": "θ_cal 纵向追踪需用户对选中项标注事后价值（引用/采纳）——"
                          "本工具记录选择，结果标注为下一步（A10 部署形态）",
    }
