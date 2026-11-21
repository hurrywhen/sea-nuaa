"""语料构建：OpenAlex 原始 JSONL → 归一化命题表 + 地面真值 + 监测清单（三种构建法）。

对应论文对象：
  - 命题归并 κ（定义 4.2）：按 arXiv ID 去重（学术流 ρ_c≈1，P3 低冗余画像的真实印证）
  - E*（定义 4.6）：切片内 cited_by_count top-(1-CRITICAL_QUANTILE) —— 重放法"已知未来"真值
  - v_e：log1p(citations)（价值代理，命题 6.2 失真度量用）
  - 监测清单 π_mon（假设 R3）三种**零后见**构建法（只使用重放窗前窗信息）：
      WL-freq：前窗发文频次 top-N 作者（"活跃团队"朴素清单）
      WL-cite：前窗论文引用总量 top-N 作者（"知名作者"清单）
      WL-inst：前窗论文引用总量 top-N 机构（"强实验室"清单——研究者实际的跟踪粒度）
    三种清单的 p̂_min（关键命题覆盖率）与预算占用都被实测：**通道 I 的覆盖是清单
    构建策略与容量的函数**——这是 p_min 内生性（论文 §7.4 R1 弱点讨论）的直接量化。
"""
from __future__ import annotations

import csv
import json
import math
import os
import re

from . import config

_DOI_RE = re.compile(r"arxiv\.([0-9]{4}\.[0-9]{4,5})", re.I)


def _arxiv_id(doi: str | None, openalex_id: str) -> str:
    if doi:
        m = _DOI_RE.search(doi)
        if m:
            return m.group(1).lower()
    return openalex_id.rsplit("/", 1)[-1]


def load_raw(path: str) -> list[dict]:
    recs, seen = [], {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            w = json.loads(line)
            aid = _arxiv_id(w.get("doi"), w.get("id", ""))
            topic = w.get("primary_topic") or {}
            authors, insts, names = [], set(), []
            for a in (w.get("authorships") or []):
                au = a.get("author") or {}
                aid2 = (au.get("id") or "").rsplit("/", 1)[-1]
                if aid2:
                    authors.append(aid2)
                names.append(au.get("display_name") or "")
                for ins in (a.get("institutions") or []):
                    iid = (ins.get("id") or "").rsplit("/", 1)[-1]
                    if iid:
                        insts.add(iid)
            rec = {
                "arxiv_id": aid,
                "title": w.get("display_name") or "",
                "date": w.get("publication_date") or "",
                "cit": int(w.get("cited_by_count") or 0),
                "field": ((topic.get("field") or {}).get("display_name")) or "",
                "subfield": ((topic.get("subfield") or {}).get("display_name")) or "",
                "topic": topic.get("display_name") or "",
                "authors": authors,
                "author_names": names,
                "insts": sorted(insts),
            }
            # κ 归并：同 arXiv ID 保留引用数较高者（防 OpenAlex 重复记录）
            if aid in seen:
                if rec["cit"] > seen[aid]["cit"]:
                    rec["_idx"] = seen[aid]["_idx"]
                    recs[seen[aid]["_idx"]] = rec
                    seen[aid]["cit"] = rec["cit"]
                continue
            seen[aid] = {"cit": rec["cit"], "_idx": len(recs)}
            recs.append(rec)
    return recs


def ai_slice(recs: list[dict]) -> list[dict]:
    """P3 监测宇宙：CS 领域 × AI 主题关键词。"""
    out = []
    for r in recs:
        if r["field"] != config.CS_FIELD:
            continue
        hay = (r["topic"] + " " + r["subfield"] + " " + r["title"]).lower()
        if any(k in hay for k in config.AI_TOPIC_KEYWORDS):
            out.append(r)
    return out


def build_ground_truth(universe: list[dict], quantile: float) -> set[str]:
    cits = sorted(r["cit"] for r in universe)
    thr = cits[min(len(cits) - 1, int(quantile * len(cits)))]
    return {r["arxiv_id"] for r in universe if r["cit"] >= thr and r["cit"] > 0}


# ---- 监测清单构建（全部零后见：只用前窗 2019-07/08 信息）----

def build_watchlist_freq(top_authors: list[dict], n: int) -> dict:
    return {"kind": "author", "ids": {a["author_id"] for a in top_authors[:n] if a["author_id"]}}


def _rank_by_prior_citations(prior_recs: list[dict], level: str) -> list[str]:
    tot: dict[str, int] = {}
    for r in prior_recs:
        keys = r["authors"] if level == "author" else r["insts"]
        for k in keys:
            if k:
                tot[k] = tot.get(k, 0) + r["cit"]
    return [k for k, _ in sorted(tot.items(), key=lambda kv: (-kv[1], kv[0]))]


def build_watchlist_cite(prior_recs: list[dict], n: int) -> dict:
    return {"kind": "author", "ids": set(_rank_by_prior_citations(prior_recs, "author")[:n])}


def build_watchlist_inst(prior_recs: list[dict], n: int) -> dict:
    return {"kind": "inst", "ids": set(_rank_by_prior_citations(prior_recs, "inst")[:n])}


def build_watchlist_inst10(prior_recs: list[dict]) -> dict:
    """可行清单变体：top-10 机构（供给 ≈ 预算的容量档，检验直通保证的正常工作区）。"""
    return {"kind": "inst", "ids": set(_rank_by_prior_citations(prior_recs, "inst")[:10])}


def wl_covered(rec: dict, wl: dict) -> bool:
    if wl["kind"] == "author":
        return any(a in wl["ids"] for a in rec["authors"])
    return any(i in wl["ids"] for i in rec["insts"])


def day_index(rec: dict) -> int:
    d = rec["date"]
    if len(d) == 10 and d[:7] == "2019-09":
        return int(d[8:10]) - 1
    return 29


def export_corpus_csv(universe: list[dict], critical: set[str],
                      watchlists: dict[str, dict], path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["arxiv_id", "date", "day", "title", "cit", "value", "critical"]
                   + [f"wl_{k}" for k in watchlists] + ["topic", "subfield", "n_authors", "n_insts"])
        for r in universe:
            w.writerow([
                r["arxiv_id"], r["date"], day_index(r), r["title"][:120], r["cit"],
                f"{math.log1p(r['cit']):.4f}", int(r["arxiv_id"] in critical),
                *[int(wl_covered(r, wl)) for wl in watchlists.values()],
                r["topic"], r["subfield"], len(r["authors"]), len(r["insts"]),
            ])


def _build_from_lite(path: str):
    """派生副本回退：无 raw/ 缓存（公开仓库）时精确复现 build_all 输出。
    corpus_lite.json = {universe 记录, watchlists(kind+ids), inst_curve, 计数}（tools 导出）。"""
    d = json.load(open(path, encoding="utf-8"))
    universe = d["universe"]
    critical = build_ground_truth(universe, config.CRITICAL_QUANTILE)
    watchlists = {k: {"kind": v["kind"], "ids": set(v["ids"])}
                  for k, v in d["watchlists"].items()}

    def _cov(wl: dict) -> dict:
        wl_crit = sum(1 for r in universe if r["arxiv_id"] in critical and wl_covered(r, wl))
        return {"kind": wl["kind"], "size": len(wl["ids"]),
                "papers_in_universe": sum(1 for r in universe if wl_covered(r, wl)),
                "p_min_hat_coverage_of_critical": wl_crit / max(1, len(critical)),
                "critical_covered_n": wl_crit}

    stats = {
        "raw_records_dedup": d.get("raw_records_dedup", len(universe)),
        "rho_c_documents_per_proposition": 1.0,
        "universe_n": len(universe),
        "universe_by_day_mean": len(universe) / config.SIM_DAYS,
        "critical_n": len(critical),
        "pi_critical_frac": len(critical) / max(1, len(universe)),
        "cit_median": sorted(r["cit"] for r in universe)[len(universe) // 2],
        "cit_max": max(r["cit"] for r in universe),
        "prior_window_records_ai_slice": d.get("prior_window_records_ai_slice", 0),
        "watchlists": {k: _cov(v) for k, v in watchlists.items()},
        "inst_watchlist_capacity_curve": d.get("inst_curve", []),
        "_source": "corpus_lite.json",
    }
    return universe, critical, watchlists, stats


def build_all():
    """返回 (universe, critical, watchlists{freq,cite,inst}, stats)。"""
    raw_path = os.path.join(config.RAW_DIR, "arxiv_2019-09.jsonl")
    auth_path = os.path.join(config.RAW_DIR, "top_authors_2019-07_08.json")
    prior_path = os.path.join(config.RAW_DIR, "arxiv_2019-07_08.jsonl")

    lite_path = os.path.join(config.DATA_DIR, "corpus_lite.json")
    if (not os.path.exists(raw_path) or os.environ.get("SEA_FORCE_LITE") == "1") \
            and os.path.exists(lite_path):
        return _build_from_lite(lite_path)

    recs = load_raw(raw_path)
    universe = ai_slice(recs)
    critical = build_ground_truth(universe, config.CRITICAL_QUANTILE)
    top_authors = json.load(open(auth_path, encoding="utf-8"))
    prior_recs = ai_slice(load_raw(prior_path)) if os.path.exists(prior_path) else []

    watchlists: dict[str, dict] = {"freq": build_watchlist_freq(top_authors, config.WATCHLIST_SIZE)}
    if prior_recs:
        watchlists["cite"] = build_watchlist_cite(prior_recs, config.WATCHLIST_SIZE)
        watchlists["inst"] = build_watchlist_inst(prior_recs, config.WATCHLIST_INST_SIZE)
        watchlists["inst10"] = build_watchlist_inst10(prior_recs)
    else:
        watchlists["cite"] = dict(watchlists["freq"])
        watchlists["inst"] = dict(watchlists["freq"])
        watchlists["inst10"] = dict(watchlists["freq"])

    def _cov(wl: dict) -> dict:
        wl_crit = sum(1 for r in universe if r["arxiv_id"] in critical and wl_covered(r, wl))
        return {
            "kind": wl["kind"], "size": len(wl["ids"]),
            "papers_in_universe": sum(1 for r in universe if wl_covered(r, wl)),
            "p_min_hat_coverage_of_critical": wl_crit / max(1, len(critical)),
            "critical_covered_n": wl_crit,
        }

    # 清单容量—覆盖曲线（p̂_min 的内生性：机构粒度）
    inst_curve = []
    if prior_recs:
        ranked_inst = _rank_by_prior_citations(prior_recs, "inst")
        for size in config.WATCHLIST_SIZE_SWEEP:
            wl = {"kind": "inst", "ids": set(ranked_inst[:size])}
            cov = sum(1 for r in universe if r["arxiv_id"] in critical and wl_covered(r, wl))
            papers = sum(1 for r in universe if wl_covered(r, wl))
            inst_curve.append({"size": size, "coverage_of_critical": cov / max(1, len(critical)),
                               "papers_in_universe_frac": papers / max(1, len(universe))})

    stats = {
        "raw_records_dedup": len(recs),
        "rho_c_documents_per_proposition": 1.0,  # arXiv 单源命题流（P3 低冗余画像实证）
        "universe_n": len(universe),
        "universe_by_day_mean": len(universe) / config.SIM_DAYS,
        "critical_n": len(critical),
        "pi_critical_frac": len(critical) / max(1, len(universe)),
        "cit_median": sorted(r["cit"] for r in universe)[len(universe) // 2],
        "cit_max": max(r["cit"] for r in universe),
        "prior_window_records_ai_slice": len(prior_recs),
        "watchlists": {k: _cov(v) for k, v in watchlists.items()},
        "inst_watchlist_capacity_curve": inst_curve,
    }
    return universe, critical, watchlists, stats
