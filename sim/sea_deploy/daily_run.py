"""阶段五实例化部署 + 阶段四团队自用遥测：每日主动获取管线。

流程（对应 docs/算法设计_v1.0.md 的每日循环）：
  fetch（arXiv live）→ A1 命题图（每篇=1 命题，ρ_c=1）→ v0 相关性评分（g² 决策集关键词）
  → A2 双通道（I=清单直通：强相关/清单作者；II=评分发现）→ A5 名额分配（P3 域=fixed，
  域配置来自移植验证）→ A9 防火墙（arXiv 无 salience 信号→隔离 0，机制在位）
  → [可选 --llm] LLM 判断层（gemma4:26b @ 127.0.0.1，native API + think:false）重排
  → 简报落盘（原子）+ 遥测追加（S4 审计同源）。

运行：cd sim && python3 -m sea_deploy.daily_run [--llm] [--date 2026-09-30] [--max 60]
诚实声明：v0 评分器 = 关键词重叠启发式（2026 实时论文无地面真值——引用年延迟）；
遥测累积后训练/校准（A10）。LLM 层失败自动回退参数化排序（管线不因后端中断而断）。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

from sea_deploy import telemetry

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PERSONA = os.path.join(HERE, "personas", "researcher.example.json")
OUT = os.path.join(HERE, "out")
ARXIV = "https://export.arxiv.org/api/query"


def fetch_arxiv(categories: list[str], max_results: int = 60, timeout: int = 60) -> list[dict]:
    q = " OR ".join(f"cat:{c}" for c in categories)
    params = {"search_query": q, "start": 0, "max_results": max_results,
              "sortBy": "submittedDate", "sortOrder": "descending"}
    url = ARXIV + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "sea-deploy research (team-local)"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = r.read()
    ns = {"a": "http://www.w3.org/2005/Atom"}
    root = ET.fromstring(data)
    papers = []
    for e in root.findall("a:entry", ns):
        def txt(tag):
            n = e.find(tag, ns)
            return " ".join(n.text.split()) if n is not None and n.text else ""
        idn = e.find("a:id", ns)
        if idn is None or not idn.text:
            continue
        papers.append({"id": idn.text.split("/abs/")[-1], "title": txt("a:title"),
                       "abstract": txt("a:summary"),
                       "authors": [a.find("a:name", ns).text for a in e.findall("a:author", ns)],
                       "categories": [c.get("term") for c in e.findall("a:category", ns)],
                       "published": txt("a:published")})
    return papers


def score_relevance(paper: dict, decision_set: list[dict]) -> tuple[float, str | None, dict]:
    """v0 启发式：标题+摘要 与 g² 决策集关键词的重叠率（按决策取最大）。"""
    text = (paper["title"] + " " + paper["abstract"]).lower()
    best, best_d, per = 0.0, None, {}
    for dec in decision_set:
        kws = [k for k in dec.get("keywords", []) if k]
        if not kws:
            continue
        hits = sum(1 for k in kws if k.lower() in text)
        sc = hits / len(kws)
        per[dec["d"]] = round(sc, 3)
        if sc > best:
            best, best_d = sc, dec["d"]
    return best, best_d, per


def llm_rerank(cands: list[dict], persona: dict, llm_cfg: dict, timeout: int = 180) -> dict | None:
    """LLM 判断层（可插拔件）：native /api/chat + think:false（gemma4:26b 思考型守卫）。

    返回 {id: {"rel":float,"decision":str,"why":str}} 或 None（失败→调用方回退参数化序）。
    模型一致性守卫 + 3 次重试（阶段三运维教训内建）。
    """
    dec_lines = "；".join(f"{d['d']}（关键词：{','.join(d['keywords'][:5])}）"
                          for d in persona["g2_decision_set"] if d.get("keywords"))
    items = "\n".join(f"{i+1}. [id={p['id']}] {p['title']}\n   摘要：{p['abstract'][:380]}"
                      for i, p in enumerate(cands))
    prompt = (f"你是下述研究者的主权信息获取助手。其活跃决策集（g² 声明）：{dec_lines}。\n"
              f"对下列每篇候选论文，评估它对『该研究者当前活跃决策』的相关性 rel（0 到 1 小数）、"
              f"指出最相关的决策条目 decision、一句话理由 why（≤30字）。\n{items}\n"
              f'只输出 JSON：{{"ratings":[{{"id":"...","rel":0.0,"decision":"...","why":"..."}}]}}')
    body = {"model": llm_cfg["model"], "stream": False, "think": bool(llm_cfg.get("think", False)),
            "options": {"temperature": 0, "num_predict": 1500},
            "messages": [{"role": "system", "content": "只输出 JSON，无其它文本。"},
                         {"role": "user", "content": prompt}]}
    url = llm_cfg["base_url"].rstrip("/") + "/api/chat"
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, data=json.dumps(body).encode(),
                                         headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                d = json.loads(r.read())
            got = str(d.get("model") or "")
            if got and llm_cfg["model"].split(":")[0] not in got:
                print(f"  [llm] 模型守卫：期望 {llm_cfg['model']} 实得 {got}，重试", file=sys.stderr)
                time.sleep(10)
                continue
            content = (d.get("message") or {}).get("content") or ""
            content = re.sub(r"^```(?:json)?|```$", "", content.strip(), flags=re.M).strip()
            m = re.search(r"\{.*\}", content, re.S)
            if not m:
                print(f"  [llm] 无 JSON（content 前 60：{content[:60]!r}），重试", file=sys.stderr)
                time.sleep(5)
                continue
            ratings = json.loads(m.group(0)).get("ratings", [])
            rmap = {r["id"]: r for r in ratings if isinstance(r, dict) and "id" in r}
            if rmap:
                return rmap
        except Exception as e:                                   # noqa: BLE001
            print(f"  [llm] attempt {attempt+1} 失败：{e}", file=sys.stderr)
            time.sleep(5)
    return None


def select(scored: list[dict], persona: dict, m: int) -> tuple[list[dict], dict]:
    """A2 双通道 + A5 名额分配（persona.channels.allocator：fixed/adaptive——域配置）。"""
    quota = persona.get("channels", {}).get("quota_I", 0.6)
    ch_i = sorted([s for s in scored if s["channel"] == "I"], key=lambda x: -x["rel"])
    ch_ii = sorted([s for s in scored if s["channel"] == "II"], key=lambda x: -x["rel"])
    mode = persona.get("channels", {}).get("allocator", "fixed")
    if mode == "fixed":
        m1 = max(1, int(round(quota * m)))
        alloc = {"I": min(m1, len(ch_i)), "II": 0, "Q": 0}
        alloc["II"] = m - alloc["I"]
    else:  # adaptive（多类域/供给波动大的画像用；P3 域默认 fixed——移植验证结论）
        from sea_algo import allocator as alloc_mod
        al = alloc_mod.MarginalVOIAllocator(["I", "II"], m, prior={"I": 0.15, "II": 0.03})
        a = al.allocate()
        alloc = {"I": min(a["I"], len(ch_i)), "II": min(a["II"], len(ch_ii)), "Q": 0}
        # 供给报警改派：不足名额转投另一通道
        leftover = m - sum(alloc.values())
        for c, pool in (("II", ch_ii), ("I", ch_i)):
            take = min(leftover, len(pool) - alloc[c])
            alloc[c] += max(0, take)
            leftover -= max(0, take)
    picked = ch_i[:alloc["I"]] + ch_ii[:alloc["II"]]
    picked = sorted(picked, key=lambda x: -x["rel"])[:m]
    alarm = len(ch_i) < max(1, int(round(quota * m)))     # A2 通道 I 供给不足报警
    return picked, {"allocation": alloc, "alarm_ch1_undersupply": alarm,
                    "n_channel_I": len(ch_i), "n_channel_II": len(ch_ii)}


def build_digest(date: str, persona: dict, picked: list[dict], info: dict,
                 llm_map: dict | None, n_fetched: int) -> str:
    L = [f"# SEA 每日简报 · {date} · {persona['pid']}\n",
         f"> g² 决策集：{'、'.join(d['d'] for d in persona['g2_decision_set'])}；"
         f"预算 m={persona['budget_per_day']}；分配 {info['allocation']}"
         f"{'；⚠️ 通道 I 供给不足报警' if info['alarm_ch1_undersupply'] else ''}"
         f"；LLM 判断层：{'启用（' + persona['llm']['model'] + '，think:false）' if llm_map else '未启用/回退参数化'}\n",
         f"抓取 {n_fetched} 篇（{', '.join(persona['watchlist']['categories'])} 最新）；"
         f"通道 I 候选 {info['n_channel_I']}、通道 II 候选 {info['n_channel_II']}；"
         f"A9 隔离 {info.get('quarantined', 0)}（arXiv 无 salience 信号，防火墙机制在位）\n",
         "## 今日深读名额\n"]
    for i, p in enumerate(picked):
        llm_note = ""
        if llm_map and p["id"] in llm_map:
            r = llm_map[p["id"]]
            llm_note = f"\n   - LLM 判断：rel={r.get('rel')}，决策={r.get('decision')}，理由：{r.get('why', '')}"
        L += [f"### {i+1}. {p['title']}",
              f"- id: {p['id']} | 通道 {p['channel']} | 参数化相关度 {p['rel']:.2f}"
              f"（决策：{p['decision'] or '—'}）| 分类 {','.join(p['categories'][:3])}",
              f"- 作者：{', '.join(p['authors'][:4])}{' 等' if len(p['authors'])>4 else ''}",
              f"- 摘要：{p['abstract'][:260]}…{llm_note}",
              f"- https://arxiv.org/abs/{p['id']}", ""]
    L += ["## 主权审计（S4 同源）\n",
          "- 本简报全部选择/隔离/改派已写入遥测（`sea_deploy/out/telemetry.jsonl`）；",
          "- 个人化修订（g² 决策集/清单/白名单）须走 S2 签字 + 冷却期（A7 B 类快速审批通道）；",
          "- 事后价值标注（引用/采纳）将用于 θ_cal 纵向追踪（A10）——遥测周报：`python3 -m sea_deploy.telemetry_report`。"]
    return "\n".join(L)


def main() -> None:
    ap = argparse.ArgumentParser(description="SEA 每日主动获取管线（阶段五部署 + 阶段四遥测）")
    ap.add_argument("--persona", default=DEFAULT_PERSONA)
    ap.add_argument("--date", default=None, help="信息流日期标签（默认今日 UTC）")
    ap.add_argument("--max", type=int, default=60)
    ap.add_argument("--llm", action="store_true", help="启用 LLM 判断层（native API + think:false）")
    ap.add_argument("--llm-top", type=int, default=8, help="送 LLM 重排的候选数")
    ap.add_argument("--out", default=OUT)
    args = ap.parse_args()

    persona = json.load(open(args.persona, encoding="utf-8"))
    date = args.date or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    print(f"[daily:{persona['pid']}] fetch arXiv {persona['watchlist']['categories']} (max {args.max})…")
    papers = fetch_arxiv(persona["watchlist"]["categories"], max_results=args.max)
    if not papers:
        print("[daily] 未抓到论文（网络/限流）——不写遥测（避免污染纵向记录）")
        return
    print(f"[daily] 抓到 {len(papers)} 篇（A1：每篇=1 命题，ρ_c=1.0）")

    thr = persona.get("channel_I_rule", {}).get("relevance_threshold", 0.34)
    wl_authors = set(persona["watchlist"].get("authors", []))
    scored = []
    for p in papers:
        rel, dec, per = score_relevance(p, persona["g2_decision_set"])
        ch = "I" if (rel >= thr or (set(p["authors"]) & wl_authors)) else "II"
        scored.append({**p, "rel": rel, "decision": dec, "per": per, "channel": ch,
                       "salience": 0.0})     # arXiv 无平台显著性信号 → A9 防火墙空转（机制在位）

    m = int(persona.get("budget_per_day", 3))
    picked, info = select(scored, persona, m)
    info["quarantined"] = 0

    # 可选 LLM 判断层：对候选 top-k 重排（失败自动回退——管线不断）
    llm_map, llm_agree = None, None
    if args.llm:
        cands = sorted(scored, key=lambda x: -x["rel"])[:args.llm_top]
        llm_map = llm_rerank(cands, persona, persona["llm"])
        if llm_map:
            for s in cands:
                if s["id"] in llm_map:
                    try:
                        s["rel_llm"] = float(llm_map[s["id"]].get("rel", s["rel"]))
                    except (TypeError, ValueError):
                        s["rel_llm"] = s["rel"]
                else:
                    s["rel_llm"] = s["rel"] * 0.5      # LLM 未覆盖 → 降权
            param_top = [s["id"] for s in sorted(cands, key=lambda x: -x["rel"])[:m]]
            llm_top = [s["id"] for s in sorted(cands, key=lambda x: -x.get("rel_llm", 0))[:m]]
            llm_agree = len(set(param_top) & set(llm_top)) / max(1, m)
            # 用 LLM 序重挑（判断层增量价值——三家族重放 p=6.8e-28 的部署面）
            picked = sorted([s for s in cands if s["id"] in set(llm_top)],
                            key=lambda x: -x.get("rel_llm", 0))
            print(f"[daily] LLM 重排完成（top-{m} 一致率 {llm_agree:.2f}）")
        else:
            print("[daily] LLM 层失败 → 回退参数化排序（诚实记录 llm_used=false）")

    digest = build_digest(date, persona, picked, info, llm_map, len(papers))
    dpath = os.path.join(args.out, f"digest_{date}.md")
    telemetry.atomic_write(dpath, digest)
    rec = {"date": date, "pid": persona["pid"], "domain": persona.get("domain", ""),
           "n_fetched": len(papers), "n_channel_I": info["n_channel_I"],
           "n_channel_II": info["n_channel_II"], "allocation": info["allocation"],
           "selected": [{"id": p["id"], "title": p["title"][:80], "score": round(p["rel"], 3),
                         "decision": p["decision"], "channel": p["channel"]} for p in picked],
           "quarantined": info["quarantined"],
           "llm_used": bool(llm_map), "llm_model": persona["llm"]["model"] + "|think:false" if llm_map else None,
           "llm_agreement": llm_agree,
           "top_decisions_informed": sorted({p["decision"] for p in picked if p["decision"]})}
    telemetry.append_record(os.path.join(args.out, "telemetry.jsonl"), rec)
    print(f"[daily] 简报 -> {dpath}")
    print(f"[daily] 遥测 -> {os.path.join(args.out, 'telemetry.jsonl')}（选中 {len(picked)} 篇，"
          f"决策触及 {rec['top_decisions_informed']}）")


if __name__ == "__main__":
    main()
