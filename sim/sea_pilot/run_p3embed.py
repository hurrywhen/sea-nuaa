"""任务 4 二期：真实嵌入特征评分器（jina-embeddings-v5 @ 本地 LM Studio）。

流程：标题嵌入（批量、缓存 npz）→ walk-forward 嵌入新颖度（1 − cos(标题, 已见均值向量)）
     + 声望/元数据特征 → 前窗训练 logistic → 九月应用 → 实测 d′（对照 TF-IDF 版 0.77）。

运行：cd sim && python3 -m sea_pilot.run_p3embed
依赖：服务端已加载 jina-embeddings-v5-text-small-retrieval-mlx（/v1/embeddings 可用）。
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import time
import urllib.request

import numpy as np

from . import config, corpus as cp
from .scorer import measure_dprime

EMB_URL = os.environ.get("SEA_EMB_URL", "http://127.0.0.1:1234/v1/embeddings")
EMB_MODEL = os.environ.get("SEA_EMB_MODEL", "jina-embeddings-v5-text-small-retrieval-mlx")
CACHE = os.path.join(config.DATA_DIR, "title_embeddings.npz")
BATCH = 32


def _key(t: str) -> str:
    return hashlib.md5(t.encode("utf-8")).hexdigest()


def embed_texts(texts: list[str]) -> np.ndarray:
    """批量嵌入（带缓存：按文本哈希键）。返回 (n, dim) float32，L2 归一化。"""
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    cache: dict[str, np.ndarray] = {}
    if os.path.exists(CACHE):
        z = np.load(CACHE, allow_pickle=False)
        cache = {k: z[k] for k in z.files}
    todo = [t for t in texts if _key(t) not in cache]
    for i in range(0, len(todo), BATCH):
        batch = todo[i:i + BATCH]
        body = json.dumps({"model": EMB_MODEL, "input": batch}).encode()
        req = urllib.request.Request(EMB_URL, data=body,
                                     headers={"Content-Type": "application/json"})
        for attempt in range(3):
            try:
                with urllib.request.urlopen(req, timeout=120) as r:
                    d = json.loads(r.read())
                got = str(d.get("model") or "")
                if got and EMB_MODEL not in got:
                    raise RuntimeError(f"embedding model mismatch: {got}")
                for item, vec in zip(batch, d["data"]):
                    cache[_key(item)] = np.asarray(vec["embedding"], dtype=np.float32)
                break
            except Exception as e:  # noqa: BLE001
                print(f"  [emb retry {attempt+1}] {e}")
                time.sleep(2 * (attempt + 1))
        else:
            raise RuntimeError("embedding backend failed")
        if (i // BATCH) % 20 == 0:
            print(f"  [emb {i+len(batch)}/{len(todo)}]", flush=True)
        time.sleep(0.05)
    M = np.vstack([cache[_key(t)] for t in texts])
    M /= (np.linalg.norm(M, axis=1, keepdims=True) + 1e-9)
    np.savez_compressed(CACHE, **{_key(t): cache[_key(t)] for t in texts})
    return M


def stream_novelty_emb(M: np.ndarray, order: np.ndarray) -> np.ndarray:
    """walk-forward：1 − cos(x_i, 已见标题均值向量)。"""
    nov = np.zeros(len(M), dtype=np.float32)
    cum = np.zeros(M.shape[1], dtype=np.float32)
    for k, i in enumerate(order):
        if k > 0:
            mean = cum / k
            nm = np.linalg.norm(mean)
            nov[i] = 1.0 - (float(mean @ M[i]) / (nm + 1e-9) if nm > 0 else 0.0)
        cum += M[i]
    return nov


def main() -> None:
    universe, critical, watchlists, stats = cp.build_all()
    prior_all = cp.load_raw(os.path.join(config.RAW_DIR, "arxiv_2019-07_08.jsonl"))
    prior = cp.ai_slice(prior_all)
    print(f"[p3embed] universe={len(universe)}, prior={len(prior)} —— 嵌入标题…")
    titles_sep = [r["title"] for r in universe]
    titles_pri = [r["title"] for r in prior]
    t0 = time.time()
    Ms = embed_texts(titles_sep)
    Mp = embed_texts(titles_pri)
    print(f"[p3embed] 嵌入完成 {Ms.shape} + {Mp.shape}（{time.time()-t0:.0f}s）")

    ids = np.array([r["arxiv_id"] for r in universe])
    crit = np.isin(ids, list(critical))

    # 特征：嵌入新颖度 + 声望 + 元数据（与 features.py 同构，仅新颖度换真实嵌入）
    from . import features as ft
    auth_p, inst_p = ft.prestige_maps(prior)
    nov_s = stream_novelty_emb(Ms, np.lexsort((ids, np.array([cp.day_index(r) for r in universe]))))
    nov_p = stream_novelty_emb(Mp, np.lexsort((np.array([r["arxiv_id"] for r in prior]),
                                               np.array([r["date"] for r in prior]))))

    def feats(recs, nov):
        ap = np.array([max((auth_p.get(a, 0.0) for a in r["authors"]), default=0.0) for r in recs])
        ip = np.array([sum(inst_p.get(e, 0.0) for e in r["insts"]) for r in recs])
        cols = [nov, np.log1p(ap), np.log1p(ip),
                np.log1p([len(r["authors"]) for r in recs]),
                np.log1p([len(r["insts"]) for r in recs]),
                [len(r["title"]) for r in recs]]
        F = np.array(cols, dtype=float).T
        return (F - F.mean(0)) / (F.std(0) + 1e-9)

    Xp = feats(prior, nov_p)
    pcits = np.array([r["cit"] for r in prior], float)
    yp = (pcits >= max(np.quantile(pcits, 0.98), 1)).astype(float)
    w, b = ft.logistic_fit(Xp, yp)
    Xs = feats(universe, nov_s)
    scores = Xs @ w + b
    d_embed = measure_dprime(scores, crit)
    print(f"[p3embed] **嵌入特征实测 d′ = {d_embed:.2f}**（对照：TF-IDF 0.77 / proxy(ρ=0.4) 1.23 / 需求线 4.39）")

    out = {"d_prime_embed_title_novelty": float(d_embed),
           "d_prime_tfidf_reference": 0.77, "d_prime_proxy_rho04_reference": 1.23,
           "d_prime_required_95pct": 4.39,
           "n_titles": len(titles_sep) + len(titles_pri),
           "embedding_model": EMB_MODEL}
    json.dump(out, open(os.path.join(config.RESULTS_DIR, "p3embed_results.json"), "w",
                        encoding="utf-8"), indent=1)
    print("[p3embed] done ->", os.path.join(config.RESULTS_DIR, "p3embed_results.json"))


if __name__ == "__main__":
    main()
