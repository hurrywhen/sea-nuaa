"""A1 命题图构建器（定义 4.2 κ 归并、定义 4.3 ρ_c、定义 4.4 信源类）。

文档流 → 命题（转载自动坍缩，评论降为注解层）→ (entity, date) 事件级归并。
事件级归并是认证（A8）与查询（A3）的粒度——阶段三教训：文档族级归并破坏认证语义。
"""
from __future__ import annotations

from collections import defaultdict


def collapse(docs: list[dict], key_fn, class_fn, crit_fn) -> list[dict]:
    """κ 归并：docs → props。

    key_fn(doc) -> 命题键（可哈希）；class_fn(doc) -> 信源类名；
    crit_fn(key, docs) -> (legal_critical, market_critical)。
    """
    groups: dict = defaultdict(list)
    for d in docs:
        groups[key_fn(d)].append(d)
    props = []
    for k in sorted(groups, key=str):
        ds = groups[k]
        legal, market = crit_fn(k, ds)
        props.append({"key": k, "n_docs": len(ds),
                      "classes": sorted({class_fn(x) for x in ds}),
                      "legal_critical": bool(legal), "market_critical": bool(market)})
    return props


def aggregate_events(props: list[dict], entity_key: str = "ticker",
                     date_key: str = "date") -> list[dict]:
    """(entity, date) 事件级归并。props 须含 entity/date/classes/n_docs/双真值字段。"""
    ev: dict = {}
    for p in props:
        k = (p[entity_key], p[date_key])
        if k not in ev:
            ev[k] = {"entity": k[0], "date": k[1], "classes": set(), "n_docs": 0,
                     "legal_critical": False, "market_critical": False, "props": []}
        e = ev[k]
        e["classes"].update(p["classes"])
        e["n_docs"] += p["n_docs"]
        e["legal_critical"] |= bool(p["legal_critical"])
        e["market_critical"] |= bool(p["market_critical"])
        e["props"].append(p)
    out = list(ev.values())
    for e in out:
        e["classes"] = sorted(e["classes"])
    out.sort(key=lambda e: (e["date"], e["entity"]))
    return out


def day_index(events: list[dict]) -> dict[str, int]:
    """日期字符串 → 模拟日序号（0 起）。"""
    dates = sorted({e["date"] for e in events})
    return {d: i for i, d in enumerate(dates)}
