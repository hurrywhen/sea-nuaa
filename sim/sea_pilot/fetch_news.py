"""新闻层抓取（无需换网络出口）：archive.org CDX 前缀查询 + Wikimedia pageviews。

背景：GDELT DOC API 对本机房 IP 限流（429）；archive.org CDX 与 wikimedia REST 均可达。
方法：
  - Reuters：按公司 slug 前缀 `reuters.com/article/us-{slug}*`（2019 URL 结构），
    capture 窗口 2019-08-25..10-15，collapse=urlkey 去重；发表日以 capture 日近似（±数日，已记录）
  - CNBC / Fortune：URL 含发表日（/2019/09/DD/），按月前缀一次抓全，客户端匹配公司 slug
  - Business Insider：按公司词前缀 `businessinsider.com/{slug}`，客户端从 URL 尾提取 2019-9
  - Wikimedia pageviews：公司维基页日浏览量（S1 参与度基线与显著性协变量）
输出：sim/pilot/data/raw/p2/news_cdx.jsonl、pageviews.json
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.normpath(os.path.join(HERE, "..", "pilot", "data", "raw", "p2"))
UA = "sea-pilot academic research (team@example.org)"

# 公司 → slug 词表（覆盖 2019 新闻量主体；slug 用于 URL 前缀与客户端匹配）
SLUGS: dict[str, list[str]] = {
    "AAPL": ["apple", "aapl"], "MSFT": ["microsoft", "msft"], "AMZN": ["amazon", "amzn"],
    "GOOG": ["google", "alphabet", "googl"], "FB": ["facebook"], "NVDA": ["nvidia", "nvda"],
    "TSLA": ["tesla", "tsla"], "AMD": ["amd"], "INTC": ["intel", "intc"], "QCOM": ["qualcomm"],
    "TXN": ["texas-instruments"], "IBM": ["ibm"], "ORCL": ["oracle"], "CRM": ["salesforce"],
    "ADBE": ["adobe"], "NOW": ["servicenow"], "INTU": ["intuit"], "EBAY": ["ebay"],
    "JPM": ["jpmorgan"], "BAC": ["bank-of-america"], "WFC": ["wells-fargo"], "C": ["citigroup"],
    "GS": ["goldman-sachs"], "MS": ["morgan-stanley"], "BLK": ["blackrock"],
    "AXP": ["american-express"], "V": ["visa"], "MA": ["mastercard"], "PYPL": ["paypal"],
    "SCHW": ["charles-schwab", "schwab"],
    "XOM": ["exxon"], "CVX": ["chevron"], "COP": ["conocophillips"], "SLB": ["schlumberger"],
    "JNJ": ["johnson-johnson", "jnj"], "PFE": ["pfizer"], "MRK": ["merck"], "ABBV": ["abbvie"],
    "BMY": ["bristol-myers"], "AMGN": ["amgen"], "GILD": ["gilead"], "BIIB": ["biogen"],
    "WMT": ["walmart", "wal-mart"], "COST": ["costco"], "TGT": ["target"], "HD": ["home-depot"],
    "LOW": ["lowes"], "NKE": ["nike"], "MCD": ["mcdonald"], "SBUX": ["starbucks"],
    "KO": ["coca-cola"], "PEP": ["pepsico"],
    "DIS": ["disney", "walt-disney"], "NFLX": ["netflix"], "CMCSA": ["comcast"],
    "T": ["at-t", "att"], "VZ": ["verizon"], "TMUS": ["t-mobile"],
    "BA": ["boeing"], "CAT": ["caterpillar"], "GE": ["general-electric"], "F": ["ford"],
    "GM": ["general-motors"], "HON": ["honeywell"], "UPS": ["ups"], "FDX": ["fedex"],
}
DOMAIN_CLASS = {
    "reuters.com": "wire", "cnbc.com": "fin_media", "fortune.com": "fin_media",
    "businessinsider.com": "fin_media",
}
MONTH_FROM, MONTH_TO = "20190825", "20191015"


def _get(url: str, timeout: int = 90, retries: int = 3) -> bytes:
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except Exception as e:  # noqa: BLE001
            print(f"  [retry {attempt+1}] {url[:100]} -> {e}", file=sys.stderr)
            time.sleep(3 * (attempt + 1))
    return b""


def _cdx(params: dict) -> list[str]:
    q = urllib.parse.urlencode(params)
    data = _get(f"http://web.archive.org/cdx/search/cdx?{q}")
    return data.decode("utf-8", "ignore").strip().splitlines() if data else []


def _match_ticker(url: str) -> tuple[str | None, str | None]:
    u = url.lower()
    best, best_slug = None, ""
    for t, slugs in SLUGS.items():
        for s in slugs:
            if len(s) > len(best_slug) and re.search(rf"[-/.]{re.escape(s)}([-/.%]|\d|$)", u):
                best, best_slug = t, s
    return best, (best_slug or None)


def _pub_date(url: str, capture_ts: str) -> str | None:
    m = re.search(r"/2019[/-]0?9[/-](\d{2})", url)          # cnbc/fortune: /2019/09/12/
    if m:
        return f"2019-09-{m.group(1)}"
    m = re.search(r"-2019-(\d{1,2})(?:[.-]|$)", url)          # BI/marketwatch 风格尾部日期
    if m:
        return f"2019-09-{int(m.group(1)):02d}"
    if capture_ts.startswith("201909") or capture_ts.startswith("201908") \
            or capture_ts.startswith("201910"):
        return f"{capture_ts[:4]}-{capture_ts[4:6]}-{capture_ts[6:8]}"  # reuters: capture 近似
    return None


def fetch_cdx_news(out_path: str) -> int:
    if os.path.exists(out_path):
        n = sum(1 for _ in open(out_path, encoding="utf-8"))
        print(f"[cache] {out_path} ({n})")
        return n
    rows: dict[str, dict] = {}
    queries: list[tuple[str, dict]] = []
    # CNBC / Fortune：按月前缀
    for dom in ("cnbc.com", "fortune.com"):
        queries.append((dom, {"url": f"{dom}/2019/09/", "collapse": "urlkey",
                              "fl": "original,timestamp", "limit": "12000"}))
    # Reuters / BI：按公司前缀
    for t, slugs in SLUGS.items():
        for s in slugs[:1]:  # 首选 slug
            queries.append(("reuters.com", {"url": f"reuters.com/article/us-{s}*",
                                            "from": MONTH_FROM, "to": MONTH_TO,
                                            "collapse": "urlkey", "fl": "original,timestamp",
                                            "limit": "400"}))
            queries.append(("businessinsider.com", {"url": f"businessinsider.com/{s}-",
                                                    "from": MONTH_FROM, "to": MONTH_TO,
                                                    "collapse": "urlkey", "fl": "original,timestamp",
                                                    "limit": "200"}))
    done = 0
    for dom, params in queries:
        lines = _cdx(params)
        done += 1
        for ln in lines:
            parts = ln.split()
            if len(parts) < 2:
                continue
            url, ts = parts[0], parts[1]
            if not url.startswith("http"):
                url = "https://" + url
            t, slug = _match_ticker(url)
            if not t:
                continue
            d = _pub_date(url, ts)
            if not d or not d.startswith("2019-09"):
                continue
            key = (t, url.split("#")[0])
            if key in rows:
                continue
            rows[key] = {"ticker": t, "date": d, "url": url,
                         "domain": dom, "src_class": DOMAIN_CLASS.get(dom, "other"),
                         "capture_ts": ts}
        if done % 20 == 0:
            print(f"  [cdx {done}/{len(queries)}] rows={len(rows)}", flush=True)
        time.sleep(1.0)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        for r in rows.values():
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"[cdx] {out_path}: {len(rows)} articles")
    return len(rows)


def fetch_cdx_news2(out_path: str) -> int:
    """第二批：日期在 URL 路径中的域，按月前缀一次抓全（客户端匹配公司 slug）。"""
    if os.path.exists(out_path):
        n = sum(1 for _ in open(out_path, encoding="utf-8"))
        print(f"[cache] {out_path} ({n})")
        return n
    monthly = [
        ("techcrunch.com", "techcrunch.com/2019/09/*", "tech_media"),
        ("theverge.com", "theverge.com/2019/9/*", "tech_media"),
        ("theverge.com", "theverge.com/2019/09/*", "tech_media"),
        ("arstechnica.com", "arstechnica.com/2019/09/*", "tech_media"),
        ("fool.com", "fool.com/articles/2019/09/*", "fin_media"),
        ("fool.com", "fool.com/investing/2019/09/*", "fin_media"),
        ("benzinga.com", "benzinga.com/news/2019/09/*", "fin_media"),
        ("cnbc.com", "cnbc.com/2019/09/*", "fin_media"),
        ("fortune.com", "fortune.com/2019/09/*", "fin_media"),
    ]
    rows: dict[tuple, dict] = {}
    for k, (dom, prefix, cls) in enumerate(monthly):
        lines = _cdx({"url": prefix, "collapse": "urlkey",
                      "fl": "original,timestamp", "limit": "12000"})
        for ln in lines:
            parts = ln.split()
            if len(parts) < 2:
                continue
            url, ts = parts[0], parts[1]
            if not url.startswith("http"):
                url = "https://" + url
            t, _slug = _match_ticker(url)
            if not t:
                continue
            d = _pub_date(url, ts)
            if not d or not d.startswith("2019-09"):
                continue
            key = (t, url.split("#")[0])
            if key in rows:
                continue
            rows[key] = {"ticker": t, "date": d, "url": url, "domain": dom,
                         "src_class": cls, "capture_ts": ts}
        print(f"  [cdx2 {k+1}/{len(monthly)}] {prefix} rows={len(rows)}", flush=True)
        time.sleep(1.0)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        for r in rows.values():
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"[cdx2] {out_path}: {len(rows)} articles")
    return len(rows)


def fetch_pageviews(out_path: str) -> None:
    if os.path.exists(out_path):
        print(f"[cache] {out_path}")
        return
    titles = {"AAPL": "Apple_Inc.", "MSFT": "Microsoft", "AMZN": "Amazon_(company)",
              "GOOG": "Google", "FB": "Facebook", "NVDA": "Nvidia", "TSLA": "Tesla,_Inc.",
              "AMD": "Advanced_Micro_Devices", "INTC": "Intel", "IBM": "IBM",
              "ORCL": "Oracle_Corporation", "BA": "Boeing", "JPM": "JPMorgan_Chase",
              "XOM": "ExxonMobil", "JNJ": "Johnson_&_Johnson", "PFE": "Pfizer",
              "WMT": "Walmart", "DIS": "The_Walt_Disney_Company", "NFLX": "Netflix",
              "V": "Visa_Inc.", "KO": "The_Coca-Cola_Company", "MCD": "McDonald's",
              "NKE": "Nike,_Inc.", "GE": "General_Electric", "F": "Ford_Motor_Company",
              "GM": "General_Motors", "VZ": "Verizon", "T": "AT%26T", "CMCSA": "Comcast",
              "PYPL": "PayPal", "GS": "Goldman_Sachs", "CAT": "Caterpillar_Inc.",
              "SBUX": "Starbucks", "HD": "The_Home_Depot", "MRK": "Merck_&_Co.",
              "PEP": "PepsiCo", "UPS": "United_Parcel_Service", "QCOM": "Qualcomm",
              "ADBE": "Adobe_Inc.", "CRM": "Salesforce"}
    out = {}
    for t, title in titles.items():
        url = ("https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"
               f"en.wikipedia/all-access/user/{title}/daily/20190901/20190930")
        data = _get(url, timeout=30)
        if data:
            try:
                j = json.loads(data)
                out[t] = {it["timestamp"][:8]: it["views"] for it in j.get("items", [])}
            except Exception:  # noqa: BLE001
                pass
        time.sleep(0.25)
    json.dump(out, open(out_path, "w", encoding="utf-8"))
    print(f"[pageviews] {out_path}: {len(out)} companies")


if __name__ == "__main__":
    os.makedirs(RAW, exist_ok=True)
    fetch_cdx_news(os.path.join(RAW, "news_cdx.jsonl"))
    fetch_cdx_news2(os.path.join(RAW, "news_cdx2.jsonl"))
    fetch_pageviews(os.path.join(RAW, "pageviews.json"))
    print("done")
