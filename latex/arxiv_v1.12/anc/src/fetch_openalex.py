"""OpenAlex 数据获取：arXiv 2019-09 重放流 + 前窗作者频次（监控清单真值）。

零 API key（polite pool，mailto 参数）。所有原始抓取缓存到 sim/pilot/data/raw/，
重复运行不重复抓取。派生语料（corpus.csv）由 corpus.py 生成并入库。

数据 provenance：
  - 语料：OpenAlex works，primary_location.source.id = S4306400194 (arXiv, Cornell University)
  - 引用数 cited_by_count 为抓取时点（2026-09）值 —— 重放法的"已知未来"真值
  - 作者频次：group_by=authorships.author.id，2019-07-01..2019-08-31 窗口（构建监控清单，零后见）
"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.parse
import urllib.request

BASE = "https://api.openalex.org/works"
MAILTO = os.environ.get("SEA_MAILTO", "sea-pilot@protonmail.com")
ARXIV_SOURCE = "S4306400194"
SELECT = "id,doi,display_name,publication_date,cited_by_count,primary_topic,authorships"

HERE = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(HERE, "..", "pilot", "data", "raw")


def _get(url: str, retries: int = 6, timeout: int = 60) -> dict:
    delay = 2.0
    last_err = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": f"sea-pilot/0.1 (mailto:{MAILTO})"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:  # noqa: BLE001 - 429/5xx/网络抖动统一退避
            last_err = e
            code = getattr(e, "code", None)
            wait = delay * (2 ** attempt) if code in (429, 500, 502, 503, 504) or code is None else delay
            print(f"  [retry {attempt+1}/{retries}] {e} -> sleep {wait:.0f}s", file=sys.stderr)
            time.sleep(wait)
    raise RuntimeError(f"OpenAlex request failed after {retries} retries: {url}\n{last_err}")


def fetch_window(date_from: str, date_to: str, out_path: str, force: bool = False) -> int:
    """抓取 [date_from, date_to] 内 arXiv 源全部 works 到 JSONL。返回条数。"""
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    if os.path.exists(out_path) and not force:
        n = sum(1 for _ in open(out_path, encoding="utf-8"))
        print(f"[cache] {out_path} ({n} records)")
        return n
    filt = (
        f"primary_location.source.id:{ARXIV_SOURCE},"
        f"from_publication_date:{date_from},to_publication_date:{date_to}"
    )
    url0 = f"{BASE}?filter={urllib.parse.quote(filt, safe=':,_-')}&select={SELECT}&per-page=200&cursor=*&mailto={MAILTO}"
    n, cursor_url, page = 0, url0, 0
    with open(out_path, "w", encoding="utf-8") as f:
        while cursor_url:
            d = _get(cursor_url)
            results = d.get("results", [])
            for w in results:
                f.write(json.dumps(w, ensure_ascii=False) + "\n")
            n += len(results)
            page += 1
            nxt = d.get("meta", {}).get("next_cursor")
            cursor_url = (
                f"{BASE}?filter={urllib.parse.quote(filt, safe=':,_-')}&select={SELECT}"
                f"&per-page=200&cursor={urllib.parse.quote(nxt)}&mailto={MAILTO}"
                if nxt and results else None
            )
            if page % 10 == 0:
                print(f"  ...{n} records")
            time.sleep(0.15)  # polite
    print(f"[fetch] {out_path}: {n} records")
    return n


def fetch_top_authors(date_from: str, date_to: str, out_path: str, force: bool = False) -> list[dict]:
    """group_by 前窗作者发文频次（top-200），监控清单原料。"""
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    if os.path.exists(out_path) and not force:
        d = json.load(open(out_path, encoding="utf-8"))
        print(f"[cache] {out_path} ({len(d)} authors)")
        return d
    filt = (
        f"primary_location.source.id:{ARXIV_SOURCE},"
        f"from_publication_date:{date_from},to_publication_date:{date_to}"
    )
    url = f"{BASE}?filter={urllib.parse.quote(filt, safe=':,_-')}&group_by=authorships.author.id&mailto={MAILTO}"
    d = _get(url)
    groups = [
        {"author_id": g["key"].rsplit("/", 1)[-1], "name": g["key_display_name"], "count": g["count"]}
        for g in d.get("group_by", [])
    ]
    json.dump(groups, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"[fetch] {out_path}: {len(groups)} authors (top by count)")
    return groups


if __name__ == "__main__":
    force = "--force" in sys.argv
    raw = os.path.normpath(RAW_DIR)
    # 主重放窗口：2019-09（30 个模拟日）
    fetch_window("2019-09-01", "2019-09-30", os.path.join(raw, "arxiv_2019-09.jsonl"), force)
    # 前窗：2019-07-01..2019-08-31（监控清单作者频次，零后见）
    fetch_top_authors("2019-07-01", "2019-08-31", os.path.join(raw, "top_authors_2019-07_08.json"), force)
    print("done.")
