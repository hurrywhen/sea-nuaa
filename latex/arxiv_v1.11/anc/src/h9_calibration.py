"""阶段四（L2 锚点）：H9 校准转移桥首测。

设计：
  人类锚 = Manifold Markets 已解决二元市场的社区终价 Brier（在线免费 API，缓存复用）
           + 文献带（GJP 超级预测者 ~0.15–0.21；普通人群 ~0.25+，Tetlock 传统）
  智能体侧 = 40 道防记忆二元预测题（重放语料地面真值构造）：
    A 型（20）：中位被引段 arXiv 论文"到 2026 年引用是否 ≥ K"（K 按子领域中位数上下对称设置）
    B 型（20）：P2 真实 filing 事件"当日 |收益| 是否 ≥2.5%"（市场真值，基率 ~10%）
  指标：Brier、ECE(10 bins)；判定 = 落入人类带内（允许系统偏移，须单调可校正——论文 H9）。
运行：cd sim && python3 -m sea_pilot.h9_calibration [--model-tag ornith]
"""
from __future__ import annotations

import csv
import json
import math
import os
import sys
import time
import urllib.request

import numpy as np

from . import config

BASE_URL = os.environ.get("SEA_LLM_BASE_URL", "http://127.0.0.1:1234/v1")
API_KEY = os.environ.get("SEA_LLM_API_KEY", "lm-studio")
MODEL = os.environ.get("SEA_LLM_MODEL", "ornith-1.5-35b")
NO_THINK = os.environ.get("SEA_H9_NOTHINK", "0") == "1"
MANIFOLD_CACHE = os.path.join(config.DATA_DIR, "manifold_resolved.json")


# ---------- 人类锚：Manifold ----------

def fetch_manifold() -> dict:
    if os.path.exists(MANIFOLD_CACHE):
        return json.load(open(MANIFOLD_CACHE, encoding="utf-8"))
    url = "https://api.manifold.markets/v0/markets?limit=1000"
    req = urllib.request.Request(url, headers={"User-Agent": "sea-pilot research"})
    with urllib.request.urlopen(req, timeout=60) as r:
        d = json.loads(r.read())
    pairs = []
    for m in d:
        if not m.get("isResolved") or m.get("outcomeType") != "BINARY":
            continue
        p, reso = m.get("probability"), m.get("resolution")
        if p is None or reso not in ("YES", "NO"):
            continue
        pairs.append({"q": m.get("question", "")[:80], "p": float(p),
                      "outcome": 1 if reso == "YES" else 0})
    brier = float(np.mean([(x["p"] - x["outcome"]) ** 2 for x in pairs])) if pairs else None
    out = {"n": len(pairs), "brier_human_manifold": brier,
           "fetched": time.strftime("%F"), "pairs": pairs}
    os.makedirs(os.path.dirname(MANIFOLD_CACHE), exist_ok=True)
    json.dump(out, open(MANIFOLD_CACHE, "w", encoding="utf-8"), ensure_ascii=False)
    return out


# ---------- 智能体题目（防记忆，真值 by construction） ----------

def build_questions() -> list[dict]:
    qs = []
    rng = np.random.default_rng(config.SEED + 3)
    # A 型：P3 论文引用阈值
    rows = list(csv.DictReader(open(os.path.join(config.DATA_DIR, "corpus_2019-09_ai.csv"),
                                                encoding="utf-8")))
    cits = np.array([int(r["cit"]) for r in rows])
    lo, hi = np.quantile(cits, 0.20), np.quantile(cits, 0.80)
    cand = [r for r in rows if lo <= int(r["cit"]) <= hi and 20 <= len(r["title"]) <= 90]
    rng.shuffle(cand)
    sub_med = {}
    for r in rows:
        sub_med.setdefault(r["subfield"], []).append(int(r["cit"]))
    sub_med = {k: float(np.median(v)) for k, v in sub_med.items()}
    picked = 0
    for r in cand:
        if picked >= 20:
            break
        med = sub_med.get(r["subfield"], 5.0)
        above = picked % 2 == 0                      # 一半阈值设在中位上、一半在下
        K = max(1, int(med * (1.6 if above else 0.6)))
        truth = int(r["cit"]) >= K
        qs.append({"kind": "A", "truth": int(truth),
                   "text": f"arXiv 论文《{r['title']}》（2019 年 9 月，{r['subfield']} 子领域）"
                           f"到 2026 年的被引次数是否会达到或超过 {K} 次？"})
        picked += 1
    # B 型：P2 filing 事件的市场移动
    try:
        from .p2_environment import build_all
        env = build_all(verbose=False)
        ev = [p for p in env["props"] if p["family"] in ("8K", "other-filing", "periodic")]
        rng.shuffle(ev)
        for p in ev[:20]:
            qs.append({"kind": "B", "truth": int(p["market_critical"]),
                       "text": f"2019 年 9 月 {p['date'][8:]} 日，{p['ticker']} 向 SEC 提交了 "
                               f"{p['family']} 类文件（当日共 {p['n_docs']} 份文档）。"
                               f"该公司股价当日涨跌幅绝对值是否达到或超过 2.5%？"})
    except Exception as e:  # noqa: BLE001
        print(f"[h9] B 型题构建失败（{e}），仅用 A 型", file=sys.stderr)
    return qs


# ---------- 调用 ----------

def _post(messages, temperature=0.3, max_tokens=6000, retries=8, timeout=600):
    mm = 0
    for attempt in range(retries):
        body_d = {"model": MODEL, "messages": messages, "temperature": temperature,
                  "max_tokens": max_tokens}
        if NO_THINK:
            body_d["chat_template_kwargs"] = {"enable_thinking": False}
        try:
            req = urllib.request.Request(f"{BASE_URL}/chat/completions",
                                         data=json.dumps(body_d).encode(),
                                         headers={"Content-Type": "application/json",
                                                  "Authorization": f"Bearer {API_KEY}"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                d = json.loads(r.read())
            got = str(d.get("model") or "")
            if got and MODEL not in got:
                mm += 1
                if mm > 8:
                    return ""
                time.sleep(30); continue
            c = d["choices"][0]["message"].get("content") or ""
            if c.strip():
                return c
            max_tokens = min(max_tokens * 2, 12000)
        except Exception as e:  # noqa: BLE001
            print(f"  [h9] attempt {attempt+1}: {e}", file=sys.stderr)
            time.sleep(min(30, 5 * (attempt + 1)))
    return ""


def _parse_probs(text: str, k: int):
    import re
    t = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.M).strip()
    m = re.search(r"[\{\[].*[\}\]]", t, re.S)
    if m:
        try:
            d = json.loads(m.group(0))
            arr = d.get("probs") if isinstance(d, dict) else d
            if arr and len(arr) == k:
                return [float(x) for x in arr]
        except Exception:  # noqa: BLE001
            pass
    nums = re.findall(r"\d+(?:\.\d+)?", t)
    vals = [float(x) for x in nums if 0 <= float(x) <= 100]
    if len(vals) >= k:
        return [v / 100 if v > 1 else v for v in vals[:k]]
    return None


def _resolve_tag(argv) -> str:
    """解析模型 tag：--model-tag 优先（向后兼容），--tag 为别名（规约 R-17）。"""
    if "--model-tag" in argv:
        return argv[argv.index("--model-tag") + 1]
    if "--tag" in argv:
        return argv[argv.index("--tag") + 1]
    return "ornith"


def main() -> None:
    tag = _resolve_tag(sys.argv)
    anchor = fetch_manifold()
    print(f"[h9:{tag}] 人类锚（Manifold 已解决二元市场）：n={anchor['n']}, "
          f"Brier={anchor['brier_human_manifold']}")
    qs = build_questions()
    print(f"[h9:{tag}] 题目 {len(qs)} 道（A 型 {sum(q['kind']=='A' for q in qs)}, "
          f"B 型 {sum(q['kind']=='B' for q in qs)}），基率 "
          f"{np.mean([q['truth'] for q in qs]):.2f}")
    probs: list[float | None] = [None] * len(qs)
    B = 10
    for b0 in range(0, len(qs), B):
        batch = qs[b0:b0 + B]
        lines = "\n".join(f"{i+1}. {q['text']}" for i, q in enumerate(batch))
        out = _post([{"role": "system", "content":
                      "你是校准良好的预测者。不要输出思考过程；只输出 JSON。"},
                     {"role": "user", "content":
                      f"对下列每个问题给出事件发生的概率（0 到 1 之间的小数）：\n{lines}\n"
                      f"只输出 JSON：{{\"probs\": [p1, ..., p{len(batch)}]}}"}])
        pv = _parse_probs(out, len(batch))
        if pv:
            for i, p in enumerate(pv):
                probs[b0 + i] = min(max(p, 0.01), 0.99)
        else:
            print(f"  [h9] batch {b0} 解析失败")
    ok = [(p, q["truth"], q["kind"]) for p, q in zip(probs, qs) if p is not None]
    if not ok:
        print("[h9] 无有效应答"); return
    brier = float(np.mean([(p - t) ** 2 for p, t, _ in ok]))
    # ECE 10 bins
    bins = np.linspace(0, 1, 11)
    ece = 0.0
    rel = []
    for i in range(10):
        sel = [(p, t) for p, t, _ in ok if bins[i] <= p < bins[i + 1] or (i == 9 and p == 1.0)]
        if sel:
            gap = abs(np.mean([p for p, _ in sel]) - np.mean([t for _, t in sel]))
            ece += gap * len(sel) / len(ok)
            rel.append({"bin": f"{bins[i]:.1f}-{bins[i+1]:.1f}", "n": len(sel),
                        "mean_p": float(np.mean([p for p, _ in sel])),
                        "freq": float(np.mean([t for _, t in sel]))})
    by_kind = {k: float(np.mean([(p - t) ** 2 for p, t, kk in ok if kk == k]))
               for k in ("A", "B") if any(kk == k for _, _, kk in ok)}
    base = float(np.mean([t for _, t, _ in ok]))
    brier_base = base * (1 - base)   # 常数预测基线的 Brier
    lit = {"gjp_super": (0.15, 0.21), "lay": (0.24, 0.30)}
    in_manifold = (anchor["brier_human_manifold"] is not None and
                   0.5 * anchor["brier_human_manifold"] <= brier <= 2 * anchor["brier_human_manifold"])
    res = {"tag": tag, "model": MODEL, "n_questions": len(qs), "n_answered": len(ok),
           "brier_agent": brier, "brier_by_kind": by_kind, "ece": float(ece),
           "brier_constant_baseline": brier_base,
           "human_anchor_manifold": anchor["brier_human_manifold"],
           "human_anchor_n": anchor["n"],
           "literature_bands": lit, "reliability": rel,
           "in_human_band_x2": bool(in_manifold),
           "verdict": ("落入人类量级带（±2×）" if in_manifold else "超出人类带（见报告）")}
    os.makedirs(config.RESULTS_DIR, exist_ok=True)
    json.dump(res, open(os.path.join(config.RESULTS_DIR, f"h9_{tag}.json"), "w",
                        encoding="utf-8"), ensure_ascii=False, indent=1)
    L = [f"# H9 校准转移桥首测：{tag}（{MODEL}）\n",
         f"题目：{len(qs)} 道防记忆二元预测（A 型引用阈值 {sum(q['kind']=='A' for q in qs)}、"
         f"B 型市场移动 {sum(q['kind']=='B' for q in qs)}），有效应答 {len(ok)}，基率 {base:.2f}\n",
         "| 量 | 值 |",
         "|---|---|",
         f"| **智能体 Brier** | **{brier:.4f}** |",
         f"| 常数基线 Brier（题目基率） | {brier_base:.4f} |",
         f"| 智能体 ECE（10 bins） | {ece:.4f} |",
         f"| A 型 / B 型 Brier | {by_kind.get('A', float('nan')):.4f} / {by_kind.get('B', float('nan')):.4f} |",
         f"| 人类锚：Manifold 已解决二元市场（n={anchor['n']}） | {anchor['brier_human_manifold']:.4f} |",
         f"| 文献带：GJP 超级预测者 / 普通人 | 0.15–0.21 / 0.24–0.30 |",
         "",
         f"**H9 判定**：{res['verdict']}。",
         "",
         "## 可靠性表\n",
         "| bin | n | 平均预测 | 实际频率 |", "|---|---|---|---|"]
    for r_ in res["reliability"]:
        L.append(f"| {r_['bin']} | {r_['n']} | {r_['mean_p']:.2f} | {r_['freq']:.2f} |")
    L += ["",
          "## 注记\n",
          "1. Manifold 锚的口径限制：社区终价、题目异质、时限不一——只作量级带（±2×）不作点估计；",
          "2. A 型题防记忆设计：中位被引段论文 + 阈值按子领域中位数对称设置（模型无法靠背答案）；",
          "3. B 型题基率 ~10%，主要检验低基率事件的概率表述是否保守；",
          "4. 本测试是 θ_cal 初始化的量级锚（论文 §15.3 H9）；跨模型比较在其余两家族补跑后进行。"]
    open(os.path.join(config.RESULTS_DIR, f"H9_REPORT_{tag}.md"), "w",
         encoding="utf-8").write("\n".join(L))
    print(f"[h9:{tag}] Brier={brier:.4f} (常数基线 {brier_base:.4f}, 人类锚 "
          f"{anchor['brier_human_manifold']:.4f}, ECE={ece:.3f}) -> {res['verdict']}")


if __name__ == "__main__":
    main()
