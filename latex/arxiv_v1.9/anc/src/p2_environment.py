"""P2 投资者画像实验环境：EDGAR 披露流 + Yahoo 市场真值 + GDELT 新闻层 → 命题图。

论文对象映射：
  - 命题 κ 归并（定义 4.2）：(公司, 日, 文档族) 为一个命题；文档 = 单个 filing / 单篇新闻
  - E*（定义 4.6）双真值：
      legal   —— 8-K 且 items ∩ 法定重大性清单 ≠ ∅（1.01/1.02/2.01–2.06）
      market  —— |日收益率| ≥ MKT_THR 的公司-日（可归因命题才计入分母）
  - 信源类（定义 4.4）：监管一手 / 通讯社 / 财经媒体 / 聚合器 / 大众媒体 / 其他
  - 组合监控清单（假设 R3）：persona 持仓子集的全部披露直通
"""
from __future__ import annotations

import json
import math
import os
from collections import defaultdict

from . import config

RAW_P2 = os.path.join(config.RAW_DIR, "p2")

CRITICAL_ITEMS = {"1.01", "1.02", "2.01", "2.02", "2.03", "2.04", "2.05", "2.06"}
MKT_THR = 0.025  # |日收益| ≥ 2.5% → 市场判定"决策关键日"

DOMAIN_CLASSES = {
    "wire": ("reuters.com", "apnews.com", "bloomberg.com", "prnewswire.com", "businesswire.com",
             "globenewswire.com"),
    "fin_media": ("wsj.com", "ft.com", "cnbc.com", "barrons.com", "marketwatch.com",
                  "businessinsider.com", "fortune.com", "investors.com", "nasdaq.com",
                  "fool.com", "reutersmedia.net", "dowjones.com"),
    "aggregator": ("finance.yahoo.com", "yahoo.com", "msn.com", "seekingalpha.com",
                   "benzinga.com", "investing.com", "zacks.com", "barchart.com",
                   "streetinsider.com", "tipranks.com", "simplywall.st", "morningstar.com"),
    "general": ("nytimes.com", "washingtonpost.com", "cnn.com", "theguardian.com", "bbc.com",
                "bbc.co.uk", "usatoday.com", "latimes.com", "nbcnews.com", "cbsnews.com",
                "abcnews.go.com", "npr.org", "time.com", "newsweek.com", "foxnews.com",
                "chicagotribune.com", "seattletimes.com", "boston.com", "startribune.com"),
}


def _domain_class(domain: str) -> str:
    d = (domain or "").lower().replace("www.", "")
    for cls, doms in DOMAIN_CLASSES.items():
        if any(d == x or d.endswith("." + x) for x in doms):
            return cls
    return "other"


def load_filings() -> list[dict]:
    """EDGAR 2019-09 filings（submissions API 缓存）。"""
    out = []
    sub_dir = os.path.join(RAW_P2, "submissions")
    if not os.path.isdir(sub_dir):
        return out
    for fn in sorted(os.listdir(sub_dir)):
        d = json.load(open(os.path.join(sub_dir, fn), encoding="utf-8"))
        t, r = d["ticker"], d["raw"]
        rec = r["filings"]["recent"]
        for i, date in enumerate(rec["filingDate"]):
            if not date.startswith("2019-09"):
                continue
            items = [x.strip() for x in (rec["items"][i].split(",") if rec["items"][i] else [])]
            out.append({
                "ticker": t, "company": r.get("name", t), "date": date,
                "form": rec["form"][i], "items": items,
                "acc": rec["accessionNumber"][i], "size": int(rec["size"][i] or 0),
                "acceptance": rec["acceptanceDateTime"][i],
                "desc": rec["primaryDocDescription"][i],
                "src_class": "regulator",
            })
    return out


def load_returns() -> dict[str, dict[str, float]]:
    """Yahoo 日线 → {ticker: {date: close}}。"""
    out: dict[str, dict[str, float]] = {}
    d = os.path.join(RAW_P2, "yahoo")
    if not os.path.isdir(d):
        return out
    import datetime as _dt
    for fn in sorted(os.listdir(d)):
        try:
            j = json.load(open(os.path.join(d, fn), encoding="utf-8"))
            res = j["chart"]["result"][0]
            ts = res["timestamp"]
            cl = res["indicators"]["quote"][0]["close"]
            t = fn.split(".")[0]
            out[t] = {}
            for tt, cc in zip(ts, cl):
                if cc is None:
                    continue
                day = _dt.datetime.utcfromtimestamp(tt).strftime("%Y-%m-%d")
                out[t][day] = float(cc)
        except Exception:  # noqa: BLE001 - 单票失败不阻塞
            continue
    return out


def market_moving_days(closes: dict[str, dict[str, float]], thr: float = MKT_THR) -> set[tuple[str, str]]:
    """|日收益| ≥ thr 的 (ticker, date) 集合。"""
    out = set()
    for t, series in closes.items():
        days = sorted(series)
        for a, b in zip(days, days[1:]):
            p0, p1 = series[a], series[b]
            if p0 > 0 and abs(p1 / p0 - 1) >= thr:
                out.add((t, b))
    return out


def load_news() -> list[dict]:
    """新闻层：archive.org CDX 通道（news_cdx.jsonl + news_cdx2.jsonl）+ GDELT 通道。"""
    out = []
    for fname in ("news_cdx.jsonl", "news_cdx2.jsonl"):
        p = os.path.join(RAW_P2, fname)
        if not os.path.exists(p):
            p = os.path.join(config.DATA_DIR, fname)
        if os.path.exists(p):
            for line in open(p, encoding="utf-8"):
                a = json.loads(line)
                out.append({"ticker": a["ticker"], "company": "", "date": a["date"],
                            "title": "", "url": a["url"], "domain": a.get("domain", ""),
                            "src_class": a.get("src_class") or _domain_class(a.get("domain", "")),
                            "lang": ""})
    d = os.path.join(RAW_P2, "gdelt")
    if os.path.isdir(d):
        for fn in sorted(os.listdir(d)):
            j = json.load(open(os.path.join(d, fn), encoding="utf-8"))
            for a in j.get("articles", []):
                sd = a.get("seendate", "")
                if len(sd) >= 8 and sd[:8].isdigit():
                    date = f"{sd[:4]}-{sd[4:6]}-{sd[6:8]}"
                else:
                    continue
                if not date.startswith("2019-09"):
                    continue
                dom = a.get("domain", "")
                out.append({"ticker": j["ticker"], "company": j["name"], "date": date,
                            "title": a.get("title", ""), "url": a.get("url", ""), "domain": dom,
                            "src_class": _domain_class(dom), "lang": a.get("language", "")})
    # 去重（同 URL）
    seen, uniq = set(), []
    for a in out:
        if a["url"] in seen:
            continue
        seen.add(a["url"])
        uniq.append(a)
    return uniq


def load_pageviews() -> dict[str, dict[str, int]]:
    """Wikimedia 日浏览量 {ticker: {YYYYMMDD: views}}（S1 参与度基线协变量）。"""
    p = os.path.join(RAW_P2, "pageviews.json")
    if not os.path.exists(p):
        p = os.path.join(config.DATA_DIR, "pageviews.json")
    if os.path.exists(p):
        try:
            return json.load(open(p, encoding="utf-8"))
        except Exception:  # noqa: BLE001
            return {}
    return {}


def build_portfolio(tickers: list[str], n: int = 25) -> set[str]:
    """P2 persona 持仓组合（确定性等距抽样 n 家，模拟"分散持仓 25 只"）。"""
    s = sorted(set(tickers))
    if len(s) <= n:
        return set(s)
    step = len(s) / n
    return {s[int(i * step)] for i in range(n)}


FORM_FAMILY = {"8-K": "8K", "8-K/A": "8K", "10-Q": "periodic", "10-K": "periodic",
               "10-K/A": "periodic"}


def _finish_env(props: list[dict], tickers: list[str], mvd: set, portfolio: set,
                n_docs_total: int, n_news: int, n_filings: int,
                verbose: bool = True, lite: bool = False) -> dict:
    """由命题层组装 env（正常路径与 lite 副本路径共用——保证公开版数值逐位一致）。"""
    crit_legal = {p["pid"] for p in props if p["legal_critical"]}
    # market 真值只保留"可归因"命题（该公司-日至少有一个命题文档）
    attributable = {(p["ticker"], p["date"]) for p in props}
    crit_market = {p["pid"] for p in props if p["market_critical"]}
    unattributable = len(mvd - attributable)

    # ---- 信源类覆盖率 p̂_min（对 E*_market 与 E*_legal 分别测）----
    all_classes = ["regulator", "wire", "fin_media", "tech_media", "aggregator", "general", "other"]
    cov = {}
    for cname in all_classes:
        cl = {c for c in crit_market if any(cname in p["classes"] for p in props if p["pid"] == c)}
        cl2 = {c for c in crit_legal if any(cname in p["classes"] for p in props if p["pid"] == c)}
        cov[cname] = {
            "p_min_hat_market": len(cl) / max(1, len(crit_market)),
            "p_min_hat_legal": len(cl2) / max(1, len(crit_legal)),
        }

    # 组合直通（通道 I）供给
    port_props = [p for p in props if p["in_portfolio"]]
    env = {
        "props": props, "tickers": tickers, "portfolio": sorted(portfolio),
        "crit_legal": crit_legal, "crit_market": crit_market,
        "n_docs_total": n_docs_total, "n_props": len(props),
        "rho_c": n_docs_total / max(1, len(props)),
        "mvd_days": len(mvd), "mvd_unattributable": unattributable,
        "class_coverage": cov,
        "supply": {
            "all_props_per_day": len(props) / config.SIM_DAYS_P2,
            "portfolio_props_per_day": len(port_props) / config.SIM_DAYS_P2,
            "news_per_day": n_news / config.SIM_DAYS_P2,
        },
        "n_news": n_news, "n_filings": n_filings,
        "_source": "p2_env_lite.json" if lite else "raw",
    }
    if verbose:
        print(f"[P2 env] filings={n_filings}, news={n_news} (域名分类), 命题={len(props)}, "
              f"文档={n_docs_total}, ρ_c={env['rho_c']:.2f}")
        print(f"  E*_legal={len(crit_legal)}, E*_market={len(crit_market)} "
              f"(不可归因移动日 {unattributable}/{len(mvd)}), 组合={len(portfolio)}家")
        print(f"  供给: 全部 {env['supply']['all_props_per_day']:.1f} 命题/日, "
              f"组合直通 {env['supply']['portfolio_props_per_day']:.1f}/日")
        for c, v in cov.items():
            if v["p_min_hat_market"] > 0 or c == "regulator":
                print(f"  类覆盖 p̂_min[{c}]: market={v['p_min_hat_market']:.2f}, legal={v['p_min_hat_legal']:.2f}")
    return env


def build_all(verbose: bool = True):
    """构建 P2 实验环境。返回 env dict。
    无 raw/p2/submissions 缓存（公开仓库）时回退 p2_env_lite.json 派生副本（精确复现）。"""
    lite_path = os.path.join(config.DATA_DIR, "p2_env_lite.json")
    subs_missing = not os.path.isdir(os.path.join(RAW_P2, "submissions"))
    if (subs_missing or os.environ.get("SEA_FORCE_LITE") == "1") and os.path.exists(lite_path):
        d = json.load(open(lite_path, encoding="utf-8"))
        return _finish_env(d["props"], d["tickers"], {tuple(x) for x in d["mvd"]},
                           set(d["portfolio"]), d["n_docs_total"], d["n_news"],
                           d["n_filings"], verbose, lite=True)
    filings = load_filings()
    news = load_news()
    closes = load_returns()
    mvd = market_moving_days(closes)

    tickers = sorted({f["ticker"] for f in filings})
    portfolio = build_portfolio(tickers)

    # ---- 命题归并 κ：(ticker, date, family) ----
    docs: dict[tuple, list[dict]] = defaultdict(list)
    for f in filings:
        fam = FORM_FAMILY.get(f["form"], "other-filing")
        docs[(f["ticker"], f["date"], fam)].append(f)
    for a in news:
        docs[(a["ticker"], a["date"], "news")].append(a)

    props = []
    for (t, date, fam), ds in sorted(docs.items()):
        items = set()
        for x in ds:
            items.update(x.get("items", []))
        is_8k = fam == "8K"
        legal = bool(items & CRITICAL_ITEMS) and is_8k
        market = (t, date) in mvd
        n_news = sum(1 for x in ds if x["src_class"] != "regulator")
        classes = {("regulator" if x["src_class"] == "regulator" else x["src_class"]) for x in ds}
        props.append({
            "pid": f"{t}|{date}|{fam}", "ticker": t, "date": date, "family": fam,
            "n_docs": len(ds), "n_news": n_news, "is_8k": is_8k,
            "items": sorted(items), "legal_critical": legal, "market_critical": market,
            "classes": sorted(classes), "in_portfolio": t in portfolio,
            "acceptance_hour": _hour(ds[0].get("acceptance", "")) if fam != "news" else -1,
        })

    return _finish_env(props, tickers, mvd, portfolio,
                       sum(p["n_docs"] for p in props), len(news), len(filings), verbose)


def _hour(acc: str) -> int:
    try:
        return int(acc[11:13])
    except Exception:  # noqa: BLE001
        return -1
