"""P2 投资者画像数据抓取：EDGAR 披露流 + Yahoo 日线（市场真值）+ GDELT 新闻层。

Provenance 与许可：
  - SEC EDGAR（data.sec.gov / www.sec.gov）：美国政府公开数据；要求 User-Agent 声明，限速 ≤10 req/s
  - Yahoo Finance chart API：免费行情（研究用途）；0.5s 节流
  - GDELT DOC 2.0 API：免费；**官方限速 1 请求/5 秒**（本脚本严格遵守）
全部抓取缓存到 sim/pilot/data/raw/p2/，重复运行跳过已有文件。

真值设计（重放法"已知未来"）：
  - E*_legal：8-K 且 items ∈ 法定重大性清单（1.01/1.02/2.01–2.06）
  - E*_market：|日收益率| ≥ 阈值的公司-日（市场的"决策关键"判定）
  - 两者分开报告；召回分母只含"可归因"命题（当日有披露或新闻文档）
"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.normpath(os.path.join(HERE, "..", "pilot", "data", "raw", "p2"))
UA = "SEA-Pilot academic research (team@example.org)"

# 60 家跨行业大盘/中盘公司（2019-09 均在市）
TICKERS = [
    # 科技
    "AAPL", "MSFT", "AMZN", "GOOG", "FB", "NVDA", "AMD", "INTC", "CSCO", "QCOM",
    "TXN", "IBM", "ORCL", "CRM", "ADBE", "NOW", "INTU", "EBAY",
    # 金融
    "JPM", "BAC", "WFC", "C", "GS", "MS", "BLK", "AXP", "V", "MA", "PYPL", "SCHW",
    # 能源
    "XOM", "CVX", "COP", "SLB",
    # 医药
    "JNJ", "PFE", "MRK", "ABBV", "BMY", "AMGN", "GILD", "BIIB",
    # 消费/零售
    "WMT", "COST", "TGT", "HD", "LOW", "NKE", "MCD", "SBUX", "KO", "PEP",
    # 媒体/通信
    "DIS", "NFLX", "CMCSA", "T", "VZ", "TMUS",
    # 工业/运输
    "BA", "CAT", "GE", "F", "GM", "HON", "UPS", "FDX",
]

MONTH = ("2019-09-01", "2019-09-30")


def _get(url: str, ua: str = UA, retries: int = 4, timeout: int = 45, sleep_on_429: float = 6.0):
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": ua})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except Exception as e:  # noqa: BLE001
            code = getattr(e, "code", None)
            if code in (400, 404):      # 永久错误（退市/无效代码）：快速失败
                raise RuntimeError(f"permanent {code}: {url[:80]}") from e
            wait = sleep_on_429 if code == 429 else 2.0 * (attempt + 1)
            print(f"  [retry {attempt+1}] {url[:90]} -> {e}; sleep {wait:.1f}s", file=sys.stderr)
            time.sleep(wait)
    raise RuntimeError(f"failed: {url}")


def fetch_edgar() -> None:
    os.makedirs(RAW, exist_ok=True)
    tick_path = os.path.join(RAW, "company_tickers.json")
    if not os.path.exists(tick_path):
        data = _get("https://www.sec.gov/files/company_tickers.json")
        open(tick_path, "wb").write(data)
        print(f"[edgar] company_tickers.json {len(data)//1024}KB")
    tickers = json.load(open(tick_path, encoding="utf-8"))
    t2cik = {v["ticker"].upper(): str(v["cik_str"]).zfill(10) for v in tickers.values()}

    sub_dir = os.path.join(RAW, "submissions")
    os.makedirs(sub_dir, exist_ok=True)
    for i, t in enumerate(TICKERS):
        cik = t2cik.get(t.upper())
        if not cik:
            print(f"[edgar] no CIK for {t}", file=sys.stderr)
            continue
        p = os.path.join(sub_dir, f"{t}.json")
        if os.path.exists(p):
            continue
        data = _get(f"https://data.sec.gov/submissions/CIK{cik}.json")
        json.dump({"ticker": t, "cik": cik, "raw": json.loads(data)},
                  open(p, "w", encoding="utf-8"))
        time.sleep(0.15)  # ≤10 req/s 且留余量
        if (i + 1) % 15 == 0:
            print(f"[edgar] {i+1}/{len(TICKERS)} submissions cached")
    print("[edgar] done")


def fetch_yahoo() -> None:
    d = os.path.join(RAW, "yahoo")
    os.makedirs(d, exist_ok=True)
    p1, p2 = 1566691200, 1570320000  # 2019-08-25 .. 2019-10-06
    for i, t in enumerate(TICKERS):
        p = os.path.join(d, f"{t}.json")
        if os.path.exists(p):
            continue
        url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{t}"
               f"?period1={p1}&period2={p2}&interval=1d")
        try:
            data = _get(url, ua="Mozilla/5.0", retries=3)
            open(p, "wb").write(data)
        except RuntimeError as e:
            print(f"[yahoo] {t} failed: {e}", file=sys.stderr)
        time.sleep(0.5)
    print(f"[yahoo] done ({len(os.listdir(d))} tickers)")


def fetch_gdelt(half_month: bool = True) -> None:
    """每公司 2 个半月窗查询（maxrecords=250，DateDesc）。官方限速 1 req / 5s。"""
    d = os.path.join(RAW, "gdelt")
    os.makedirs(d, exist_ok=True)
    # 公司名（EDGAR 官方名，减少 GDELT 名称误配）
    names = {}
    sub_dir = os.path.join(RAW, "submissions")
    for t in TICKERS:
        p = os.path.join(sub_dir, f"{t}.json")
        if os.path.exists(p):
            names[t] = json.load(open(p, encoding="utf-8"))["raw"].get("name", t)
    windows = [("20190901000000", "20190915235959"), ("20190916000000", "20190930235959")] \
        if half_month else [("20190901000000", "20190930235959")]
    total = len(names) * len(windows)
    k = 0
    for t, nm in names.items():
        for wi, (ws, we) in enumerate(windows):
            p = os.path.join(d, f"{t}_w{wi}.json")
            k += 1
            if os.path.exists(p):
                continue
            q = urllib.parse.quote(f'"{nm}"')
            url = ("https://api.gdeltproject.org/api/v2/doc/doc?"
                   f"query={q}&mode=ArtList&maxrecords=250&sort=DateDesc"
                   f"&startdatetime={ws}&enddatetime={we}&format=json")
            try:
                data = _get(url, ua="Mozilla/5.0", retries=5, sleep_on_429=6.0)
                j = json.loads(data)
                arts = j.get("articles", [])
                json.dump({"ticker": t, "name": nm, "window": [ws, we], "articles": arts},
                          open(p, "w", encoding="utf-8"))
                print(f"[gdelt {k}/{total}] {t}: {len(arts)} articles")
            except Exception as e:  # noqa: BLE001
                print(f"[gdelt {k}/{total}] {t} FAILED: {e}", file=sys.stderr)
            time.sleep(5.2)  # 官方限速
    print("[gdelt] done")


def fetch_edgar_many(n_extra: int = 440, seed: int = 20260926) -> None:
    """从 company_tickers.json 确定性抽样扩充公司集（P2 universe 规模修复）。"""
    import random
    tick_path = os.path.join(RAW, "company_tickers.json")
    if not os.path.exists(tick_path):
        data = _get("https://www.sec.gov/files/company_tickers.json")
        open(tick_path, "wb").write(data)
    tickers = json.load(open(tick_path, encoding="utf-8"))
    t2cik = {v["ticker"].upper(): str(v["cik_str"]).zfill(10) for v in tickers.values()}
    pool = sorted(t2cik)
    rng = random.Random(seed)
    extra = [t for t in rng.sample(pool, min(n_extra + 200, len(pool))) if t not in TICKERS][:n_extra]
    all_t = list(dict.fromkeys(TICKERS + extra))
    sub_dir = os.path.join(RAW, "submissions")
    os.makedirs(sub_dir, exist_ok=True)
    done = 0
    for i, t in enumerate(all_t):
        p = os.path.join(sub_dir, f"{t}.json")
        if os.path.exists(p):
            continue
        cik = t2cik.get(t)
        if not cik:
            continue
        try:
            data = _get(f"https://data.sec.gov/submissions/CIK{cik}.json", retries=2)
            json.dump({"ticker": t, "cik": cik, "raw": json.loads(data)},
                      open(p, "w", encoding="utf-8"))
            done += 1
        except RuntimeError:
            pass
        time.sleep(0.12)
        if (i + 1) % 100 == 0:
            print(f"[edgar-many] {i+1}/{len(all_t)} (new: {done})", flush=True)
    print(f"[edgar-many] done, new files: {done}")


def fetch_yahoo_many() -> None:
    """为 submissions 缓存中的全部公司抓 2019-08-25..10-06 日线（市场真值用）。"""
    d = os.path.join(RAW, "yahoo")
    sub_dir = os.path.join(RAW, "submissions")
    os.makedirs(d, exist_ok=True)
    ts = sorted(f[:-5] for f in os.listdir(sub_dir) if f.endswith(".json"))
    p1, p2 = 1566691200, 1570320000
    new = 0
    for i, t in enumerate(ts):
        p = os.path.join(d, f"{t}.json")
        if os.path.exists(p):
            continue
        url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{t}"
               f"?period1={p1}&period2={p2}&interval=1d")
        try:
            data = _get(url, ua="Mozilla/5.0", retries=2, timeout=20)
            j = json.loads(data)
            if j.get("chart", {}).get("result"):
                open(p, "wb").write(data)
                new += 1
        except Exception:  # noqa: BLE001
            pass
        time.sleep(0.35)
        if (i + 1) % 100 == 0:
            print(f"[yahoo-many] {i+1}/{len(ts)} (new: {new})", flush=True)
    print(f"[yahoo-many] done, new: {new}")


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("all", "edgar"):
        fetch_edgar()
    if what in ("all", "yahoo"):
        fetch_yahoo()
    if what in ("all", "gdelt"):
        fetch_gdelt()
    if what in ("many",):
        fetch_edgar_many()
        fetch_yahoo_many()


