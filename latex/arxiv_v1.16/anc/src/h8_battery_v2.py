"""H8 验证电池 v2.1：新颖刺激 + 分级难度 + 双模型 + **看门狗环境加固**。

v2 → v2.1 的可靠性加固（应对 node-a llama.cpp 的看门狗/定时重启）：
  1. 垃圾内容检测：退化输出（重复字符占比>60%）视为失败重试，不消耗参与者名额；
  2. 参与者级断点：每个参与者完成即原子落盘（tmp+rename），服务重启零丢失、续跑不重做；
  3. 更长骑窗：单调用最多 12 次重试、退避至 60s，可骑过分钟级重启窗口。

范式：A2 准确性提示（分级材料）/ B2 对立暴露（Bail 范式）/ C2 构造关系型辨别（防记忆）。
运行：cd sim && python3 -m sea_pilot.h8_battery_v2 --model-tag <tag> [--n-a 20 --n-b 10 --n-c 20]
输出：pilot/results/h8v2_{tag}.json + H8_V2_REPORT_{tag}.md（跨模型对照自动扫描）
"""
from __future__ import annotations

import csv
import json
import math
import os
import sys
import time
from collections import Counter

import numpy as np

from . import config

BASE_URL = os.environ.get("SEA_LLM_BASE_URL", "http://127.0.0.1:1234/v1")
API_KEY = os.environ.get("SEA_LLM_API_KEY", "lm-studio")
MODEL = os.environ.get("SEA_LLM_MODEL", "ornith-1.5-35b")
NO_THINK = os.environ.get("SEA_H8_NOTHINK", "0") == "1"   # qwen3.8@llama.cpp 需置 1（enable_thinking=false）

PERSONAS = [
    ("P2 投资者", "你是一名个人投资者，日常关注财经信息，习惯快速浏览大量资讯。"),
    ("P3 研究者", "你是一名 AI 方向的研究者，习惯批判性阅读，对证据质量敏感。"),
    ("P5 家长", "你是一名普通上班族兼家长，关注健康与生活信息，时间有限。"),
    ("中立成人", "你是一名普通成年人，日常使用社交媒体获取信息。"),
]

SYS_JSON = "不要输出任何思考过程、解释或代码围栏；第一个字符必须是 {，只输出一个 JSON 对象。"

# ---- A2：分级难度声明（12 真 / 12 假，全部有文献共识）----
ITEMS_A2 = [
    ("疫苗会导致自闭症", False, "obvious"),
    ("抗生素能治疗普通感冒等病毒感染", False, "obvious"),
    ("咖啡灌肠可以治愈癌症", False, "obvious"),
    ("人类只使用了大脑的 10%", False, "obvious"),
    ("用肥皂洗手能减少传染病传播", True, "obvious"),
    ("吸烟是全球最主要的可预防死因", True, "obvious"),
    ("安全带显著降低车祸死亡风险", True, "obvious"),
    ("孕早期补充叶酸可降低神经管缺陷风险", True, "obvious"),
    ("适量饮用红酒能显著延长寿命", False, "subtle"),
    ("维生素 E 等抗氧化补充剂可以预防癌症", False, "subtle"),
    ("麸质对非乳糜泻人群的健康有害", False, "subtle"),
    ("通过饮食可以把'酸性体质'调理成'碱性体质'从而防病", False, "subtle"),
    ("电子烟已被证明是完全无害的戒烟替代品", False, "subtle"),
    ("顺势疗法制剂具有超越安慰剂的治疗作用", False, "subtle"),
    ("有机食品的营养价值显著高于常规种植食品", False, "subtle"),
    ("抗抑郁药会成瘾，感觉好转就应立即自行停药", False, "subtle"),
    ("适量饮用咖啡（约 3–4 杯/日）对多数成年人总体是安全的", True, "subtle"),
    ("加工肉制品被 IARC 列为 1 类致癌物", True, "subtle"),
    ("'每天必须喝 8 杯水'的教条缺乏严格科学依据，需水量因人而异", True, "subtle"),
    ("规律运动对轻中度抑郁有辅助改善作用", True, "subtle"),
    ("久坐与心血管代谢风险上升相关，规律中断久坐有益", True, "subtle"),
    ("多数益生菌产品对健康人群肠道健康的改善证据有限", True, "subtle"),
    ("PM2.5 空气污染暴露与心血管疾病风险上升相关", True, "subtle"),
    ("正确使用防晒霜可降低皮肤鳞状细胞癌风险", True, "subtle"),
]

# ---- B2：中性议题与双侧对称论据 ----
ISSUES = [
    ("四天工作制应当被广泛推广",
     "支持论据：多项企业试点评估显示，四天工作制与员工保留率、心理健康指标的可测改善相关，产出型岗位的生产率未降反升；对知识型岗位，压缩工时减少了会议碎片化。",
     "反对论据：多项行业分析指出，四天工作制在制造业与医疗等连续运营部门会推高人力成本并造成排班缺口；部分试点企业在压缩工时下报告了单位产出质量下降与加班隐性化。"),
    ("AI 生成内容应当强制加注标识",
     "支持论据：来源标识研究表明，清晰的出处标注帮助公众大规模识别合成媒体，降低误导内容在纠正前的传播时间，并为司法与平台治理提供可执行的问责锚点。",
     "反对论据：有技术政策研究指出，强制标识在执行上面临开源模型无法追溯、修改链条断裂等问题；标识泛滥还可能让公众对未标识内容产生过度信任，形成新的误导面。"),
    ("城市应当征收中心城区拥堵费",
     "支持论据：伦敦、斯德哥尔摩等城市的收费前后研究显示，拥堵收费显著降低中心城区车流量与事故率，空气质量指标改善，收入定向投入公共交通形成正循环。",
     "反对论据：交通经济学的批评意见认为，拥堵费对低收入通勤者构成累退负担；若公共交通替代不足，收费只会转移出行成本而不会减少总通勤时间。"),
    ("大学研究应当全部免费公开（开放获取强制化）",
     "支持论据：引用分析显示开放获取论文获得显著更多引用并更快抵达实践者；多家资助机构的强制政策表明过渡期后出版成本趋稳，公共资金效率净改善。",
     "反对论据：出版经济学研究提示，全面强制开放获取会把成本从读者端转移到作者端（APC），对资助薄弱学科的学者不利，并可能挤压学会期刊的生存空间。"),
    ("大型公司应当强制公布薪酬比率",
     "支持论据：披露制度实证研究发现，薪酬比率披露强化了股东薪酬投票与媒体监督的依据，部分公司高管薪酬增速回落而经营表现未受影响。",
     "反对论据：公司治理研究中的质疑意见认为，单一比率指标忽略了行业资本结构差异，可能诱发短期化的薪酬操纵，且披露的合规成本对小股东利益是净损耗。"),
    ("平台应当对独立核查判定为假的内容降权",
     "支持论据：降权机制的对照实验显示，降权使假内容传播量下降约五至八成，对合法言论影响有限；相比删除，降权保留记录、允许申诉，是问责友好的治理工具。",
     "反对论据：言论治理研究提醒，核查机构自身存在错误率与立场偏差，把降权权力集中于少数核查方，可能造成寒蝉效应并削弱对核查机构的问责激励。"),
]
NEUTRAL_FACTS = [
    "中性事实一：海獭在睡觉时会手拉手漂浮，以防被水流冲散。",
    "中性事实二：地球上已知的最深海沟是马里亚纳海沟，最深处约 11000 米。",
]


# ---------------- 加固版后端调用 ----------------

def _is_garbage(c: str) -> bool:
    """退化输出检测：非空白字符中占比最高者 >60% 视为垃圾（llama.cpp 退化态特征）。"""
    nz = [ch for ch in c if not ch.isspace()]
    if len(nz) < 20:
        return False
    return Counter(nz).most_common(1)[0][1] / len(nz) > 0.60


def _post(messages: list[dict], temperature: float = 0.7, max_tokens: int | None = None,
          retries: int = 12, timeout: int = 600) -> str:
    import urllib.request
    start_tok = max_tokens or int(os.environ.get("SEA_H8_MAXTOK", "6000"))
    cap_tok = int(os.environ.get("SEA_H8_MAXCAP", "16000"))
    max_tokens = start_tok
    mismatch_waits = 0
    t0 = time.time()
    for attempt in range(retries):
        body_d = {"model": MODEL, "messages": messages, "temperature": temperature,
                  "max_tokens": max_tokens}
        if NO_THINK:
            body_d["chat_template_kwargs"] = {"enable_thinking": False}
        body = json.dumps(body_d).encode()
        try:
            req = urllib.request.Request(f"{BASE_URL}/chat/completions", data=body,
                                         headers={"Content-Type": "application/json",
                                                  "Authorization": f"Bearer {API_KEY}"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                d = json.loads(r.read())
            got = str(d.get("model") or "")
            if got and MODEL not in got:
                mismatch_waits += 1
                if mismatch_waits > 10:
                    raise RuntimeError(f"model mismatch persists: {got}")
                print(f"  [v2.1] 被 {got} 应答（抢占），30s 后重试", file=sys.stderr, flush=True)
                time.sleep(30)
                continue
            c = d["choices"][0]["message"].get("content") or ""
            if c.strip() and not _is_garbage(c):
                print(f"  [v2.1 call] ok {time.time()-t0:.0f}s tok={max_tokens}",
                      file=sys.stderr, flush=True)
                return c
            if _is_garbage(c):
                print(f"  [v2.1 call] 退化输出（重复垃圾），{time.time()-t0:.0f}s，重试",
                      file=sys.stderr, flush=True)
                time.sleep(min(60, 10 * (attempt + 1)))     # 骑窗看门狗重启
                continue
            if max_tokens < cap_tok:
                max_tokens = min(max_tokens * 2, cap_tok)
                print(f"  [v2.1 call] empty content {time.time()-t0:.0f}s, budget→{max_tokens}",
                      file=sys.stderr, flush=True)
            else:
                print(f"  [v2.1 call] empty at cap, give up this participant",
                      file=sys.stderr, flush=True)
                return ""
        except Exception as e:  # noqa: BLE001
            print(f"  [v2.1] attempt {attempt+1}: {e}", file=sys.stderr, flush=True)
            time.sleep(min(60, 10 * (attempt + 1)))         # 退避加长：骑过重启窗口
    return ""


def _parse_json(text: str):
    import re
    t = text.strip()
    t = re.sub(r"^```(?:json)?|```$", "", t, flags=re.M).strip()
    m = re.search(r"[\{\[].*[\}\]]", t, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except Exception:  # noqa: BLE001
        return None


def _probit(p: float) -> float:
    from .scorer import norm_ppf_upper
    return -norm_ppf_upper(p)


def _atomic_save(res: dict, path: str) -> None:
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    os.replace(tmp, path)     # 原子替换：重启不产生半写文件


# ---------------- C2：构造关系型验证题（防记忆） ----------------

def build_c2_items(n_true: int = 12, seed: int = 20260928) -> list[tuple[str, bool, str]]:
    rng = np.random.default_rng(seed)
    csvp = os.path.join(config.DATA_DIR, "corpus_2019-09_ai.csv")
    rows = list(csv.DictReader(open(csvp, encoding="utf-8")))
    cits = np.array([int(r["cit"]) for r in rows])
    lo, hi = np.quantile(cits, 0.40), np.quantile(cits, 0.70)
    cand = [r for r in rows if lo <= int(r["cit"]) <= hi and r["subfield"]
            and 20 <= len(r["title"]) <= 90 and '"' not in r["title"]]
    subfields = sorted({r["subfield"] for r in cand})
    rng.shuffle(cand)
    picked, used = [], set()
    for r in cand:
        if r["arxiv_id"] in used:
            continue
        picked.append(r); used.add(r["arxiv_id"])
        if len(picked) >= n_true:
            break
    items = []
    for r in picked:
        items.append((f"arXiv 预印本《{r['title']}》于 2019 年 9 月提交，属于「{r['subfield']}」子领域。",
                      True, "true"))
    for i, r in enumerate(picked):
        if i < n_true // 2:
            month = str(rng.choice([7, 8, 10, 11]))
            items.append((f"arXiv 预印本《{r['title']}》于 2019 年 {month} 月提交，属于「{r['subfield']}」子领域。",
                          False, "perturb-date"))
        else:
            alt = [sf for sf in subfields if sf != r["subfield"]]
            sf2 = alt[int(rng.integers(len(alt)))]
            items.append((f"arXiv 预印本《{r['title']}》于 2019 年 9 月提交，属于「{sf2}」子领域。",
                          False, "perturb-subfield"))
    rng.shuffle(items)
    return items


def paradigm_c2(n: int, res: dict, save) -> dict:
    items = build_c2_items()
    lines = "\n".join(f"{j+1}. {t}" for j, (t, _, _) in enumerate(items))
    agents = res.setdefault("C2_agents", [])
    for i in range(len(agents), n):
        pname, ptext = PERSONAS[i % len(PERSONAS)]
        out = _post([{"role": "system", "content": ptext + SYS_JSON},
                     {"role": "user", "content":
                      f"对下列每条关于 arXiv 预印本的陈述，判断其是否准确（你可能并不认识这些论文——"
                      f"请基于陈述内部一致性与领域常识尽力判断，不确定时猜测）。\n{lines}\n"
                      f"只输出 JSON：{{\"judge\": [\"true\"/\"false\", ...]}}，共 {len(items)} 项。"}],
                    temperature=0.3)
        d = _parse_json(out)
        if not d or len(d.get("judge", [])) != len(items):
            agents.append({"ok": False})
            save(); continue
        jud = np.array([1 if str(x).lower().startswith("t") else 0 for x in d["judge"]])
        truth = np.array([1 if t else 0 for _, t, _ in items])
        hr = (jud[truth == 1] == 1).mean(); far = (jud[truth == 0] == 1).mean()
        nt, nf = int(truth.sum()), int((1 - truth).sum())
        h = min(max(hr, 1 / (2 * nt)), 1 - 1 / (2 * nt))
        f = min(max(far, 1 / (2 * nf)), 1 - 1 / (2 * nf))
        agents.append({"ok": True, "acc": float((jud == truth).mean()),
                       "dprime": float(_probit(h) - _probit(f))})
        save()
    good = [a for a in agents if a.get("ok")]
    ds = [a["dprime"] for a in good]
    return {"n": len(good), "n_attempted": len(agents),
            "dprime_mean": float(np.mean(ds)) if ds else None,
            "dprime_sd": float(np.std(ds, ddof=1)) if len(ds) > 1 else None,
            "accuracy_mean": float(np.mean([a["acc"] for a in good])) if good else None,
            "dprime_by_agent": ds,
            "note": "构造关系型验证题（论文×日期×子领域），中位被引段防记忆；参与者级断点"}


# ---------------- A2：准确性提示（分级材料） ----------------

def paradigm_a2(n_per_arm: int, res: dict, save) -> dict:
    lines = "\n".join(f"{j+1}. {t}" for j, (t, _, _) in enumerate(ITEMS_A2))
    recs = res.setdefault("A2_agents", [])
    total_needed = 2 * n_per_arm
    for k in range(len(recs), total_needed):
        arm = "control" if k < n_per_arm else "accuracy"
        i = k % n_per_arm
        instr = ("对下面每条声明，评估你把它分享到自己社交圈的可能性（1=绝不，10=一定会）。"
                 if arm == "control" else
                 "在评估之前，请先思考：一条声明在事实上是否准确取决于什么证据？然后对每条声明评估你把它分享到自己社交圈的可能性（1=绝不，10=一定会）。")
        pname, ptext = PERSONAS[i % len(PERSONAS)]
        prompt = (f"{instr}\n\n声明列表：\n{lines}\n\n"
                  f"只输出 JSON：{{\"ratings\": [r1, ..., r{len(ITEMS_A2)}]}}。")
        out = _post([{"role": "system", "content": ptext + SYS_JSON},
                     {"role": "user", "content": prompt}], temperature=0.7)
        d = _parse_json(out)
        if not d or len(d.get("ratings", [])) != len(ITEMS_A2):
            recs.append({"arm": arm, "ok": False}); save(); continue
        r = np.array([float(x) for x in d["ratings"]])
        lab = np.array([t for _, t, _ in ITEMS_A2])
        sub = np.array([g == "subtle" for _, _, g in ITEMS_A2])
        recs.append({"arm": arm, "ok": True,
                     "false_share": float(r[~lab].mean()), "true_share": float(r[lab].mean()),
                     "false_subtle": float(r[~lab & sub].mean()),
                     "true_subtle": float(r[lab & sub].mean())})
        save()
    arms = {}
    for arm in ("control", "accuracy"):
        g = [x for x in recs if x["arm"] == arm and x.get("ok")]
        arms[arm] = {"n": len(g),
                     **{k: (float(np.mean([x[k] for x in g])) if g else None)
                        for k in ("false_share", "true_share", "false_subtle", "true_subtle")},
                     "false_share_by_agent": [x["false_share"] for x in g]}
    a, b = arms["accuracy"], arms["control"]
    if a["false_share_by_agent"] and b["false_share_by_agent"]:
        x, y = np.array(a["false_share_by_agent"]), np.array(b["false_share_by_agent"])
        sp = math.sqrt((x.var(ddof=1) + y.var(ddof=1)) / 2) if min(len(x), len(y)) > 1 else 1.0
        arms["effect_cohend_false_share"] = float((x.mean() - y.mean()) / sp) if sp > 0 else None
        arms["effect_cohend_false_subtle"] = (
            float((a["false_subtle"] - b["false_subtle"]) / sp)
            if sp > 0 and a["false_subtle"] is not None else None)
    return arms


# ---------------- B2：对立暴露 ----------------

def paradigm_b2(n_per_arm: int, res: dict, save, rng_seed: int = 5) -> dict:
    recs = res.setdefault("B2_agents", [])
    total_needed = 2 * n_per_arm
    # 议题抽样序列与参与者序号绑定（续跑时复现同一分配）
    for k in range(len(recs), total_needed):
        rng = np.random.default_rng(rng_seed + k)
        arm = "treatment" if k < n_per_arm else "control"
        i = k % n_per_arm
        pname, ptext = PERSONAS[i % len(PERSONAS)]
        idx = rng.choice(len(ISSUES), 3, replace=False)
        issues = [ISSUES[j] for j in idx]
        init_side = [int(rng.integers(0, 2)) for _ in issues]
        q = "\n".join(f"{kk+1}. {t}" for kk, (t, _, _) in enumerate(issues))
        pre = _post([{"role": "system", "content": ptext + SYS_JSON},
                     {"role": "user", "content":
                      f"作为{pname}，请对下列议题给出你的立场分（1=强烈反对 … 7=强烈支持）：\n{q}\n"
                      f"只输出 JSON：{{\"pre\": [s1, s2, s3]}}"}], temperature=0.7)
        dp = _parse_json(pre)
        if not dp or len(dp.get("pre", [])) != 3:
            recs.append({"arm": arm, "ok": False}); save(); continue
        pre_v = np.array([float(x) for x in dp["pre"]])
        expo = ("\n\n".join(contra if side == 1 else pro
                            for (_, pro, contra), side in zip(issues, init_side))
                if arm == "treatment" else "\n".join(NEUTRAL_FACTS))
        post = _post([{"role": "system", "content": ptext + SYS_JSON},
                      {"role": "user", "content":
                      f"请阅读以下材料：\n\n{expo}\n\n阅读后，请重新对下列议题给出立场分"
                      f"（1=强烈反对 … 7=强烈支持）：\n{q}\n只输出 JSON：{{\"post\": [s1, s2, s3]}}"}],
                     temperature=0.7)
        dq = _parse_json(post)
        if not dq or len(dq.get("post", [])) != 3:
            recs.append({"arm": arm, "ok": False}); save(); continue
        post_v = np.array([float(x) for x in dq["post"]])
        side_sign = np.where(pre_v >= 4, 1.0, -1.0)
        recs.append({"arm": arm, "ok": True,
                     "extremity": float(np.mean(np.abs(post_v - 4) - np.abs(pre_v - 4))),
                     "sided": float(np.mean(side_sign * (post_v - pre_v)))})
        save()
    arms = {}
    for arm in ("treatment", "control"):
        g = [x for x in recs if x["arm"] == arm and x.get("ok")]
        arms[arm] = {"n": len(g),
                     "extremity_delta_mean": float(np.mean([x["extremity"] for x in g])) if g else None,
                     "sided_shift_mean": float(np.mean([x["sided"] for x in g])) if g else None,
                     "extremity_by_agent": [x["extremity"] for x in g]}
    t, c = arms["treatment"], arms["control"]
    if t["extremity_by_agent"] and c["extremity_by_agent"]:
        x, y = np.array(t["extremity_by_agent"]), np.array(c["extremity_by_agent"])
        sp = math.sqrt((x.var(ddof=1) + y.var(ddof=1)) / 2) if min(len(x), len(y)) > 1 else 1.0
        arms["effect_cohend_extremity"] = float((x.mean() - y.mean()) / sp) if sp > 0 else None
    return arms


# ---------------- 主流程 ----------------

def main() -> None:
    tag = sys.argv[sys.argv.index("--model-tag") + 1] if "--model-tag" in sys.argv else "ornith"
    n_a = int(sys.argv[sys.argv.index("--n-a") + 1]) if "--n-a" in sys.argv else 20
    n_b = int(sys.argv[sys.argv.index("--n-b") + 1]) if "--n-b" in sys.argv else 10
    n_c = int(sys.argv[sys.argv.index("--n-c") + 1]) if "--n-c" in sys.argv else 20
    out_path = os.path.join(config.RESULTS_DIR, f"h8v2_{tag}.json")
    res = json.load(open(out_path, encoding="utf-8")) if os.path.exists(out_path) else {}
    t0 = time.time()

    def save():
        res["meta"] = {"model": MODEL, "base_url": BASE_URL, "tag": tag,
                       "elapsed_sec": round(time.time() - t0, 1),
                       "n": {"A2": n_a, "B2": n_b, "C2": n_c}, "version": "v2.1",
                       "no_think": NO_THINK}
        _atomic_save(res, out_path)

    print(f"[H8v2.1:{tag}] model={MODEL} @ {BASE_URL} (no_think={NO_THINK})", flush=True)
    if "C2" not in res:
        print("[H8v2.1] C2 构造关系型辨别 …", flush=True)
        res["C2"] = paradigm_c2(n_c, res, save); save()
    if "A2" not in res:
        print("[H8v2.1] A2 准确性提示（分级材料）…", flush=True)
        res["A2"] = paradigm_a2(n_a, res, save); save()
    if "B2" not in res:
        print("[H8v2.1] B2 对立暴露 …", flush=True)
        res["B2"] = paradigm_b2(n_b, res, save); save()
    save()
    _report(tag, res)
    print(f"[H8v2.1:{tag}] done -> {out_path}", flush=True)


def _report(tag: str, res: dict) -> None:
    A, B, C = res.get("A2", {}), res.get("B2", {}), res.get("C2", {})
    L = [f"# H8 验证电池 v2.1 报告：{tag}（{res['meta']['model']}）\n",
         f"n：A2={res['meta']['n']['A2']}/臂, B2={res['meta']['n']['B2']}/臂, C2={res['meta']['n']['C2']} · "
         f"耗时 {res['meta']['elapsed_sec']}s · no_think={res['meta'].get('no_think')}\n",
         "**判定规则**：方向与人类文献一致即『方向通过』；效应量按家族入 O6 转移系数库，不外推人类。\n",
         "## C2 构造关系型辨别（防记忆）\n"]
    if C:
        L += [f"- d′ = {_fmt(C.get('dprime_mean'))} ± {_fmt(C.get('dprime_sd'))}"
              f"（有效 {C.get('n')}/{C.get('n_attempted', C.get('n'))}），准确率 {_fmt(C.get('accuracy_mean'))}",
              f"- 对照 v1（著名神话）d′=3.77 天花板；人类文献 1.0–1.8",
              f"- **判定**：{'落入/接近人类区间 ⇒ 材料有效' if C.get('dprime_mean') is not None and 0.3 <= C['dprime_mean'] <= 2.5 else ('仍触天花板' if (C.get('dprime_mean') or 0) > 2.5 else '低于人类区间')}\n"]
    if A:
        L += ["## A2 准确性提示（分级材料）\n",
              "| 指标 | accuracy 臂 | control 臂 |", "|---|---|---|",
              f"| 假声明分享（全部） | {_fmt(A['accuracy'].get('false_share'))} | {_fmt(A['control'].get('false_share'))} |",
              f"| 假声明分享（微妙项） | {_fmt(A['accuracy'].get('false_subtle'))} | {_fmt(A['control'].get('false_subtle'))} |",
              f"| d（全部 / 微妙） | **{_fmt(A.get('effect_cohend_false_share'))} / {_fmt(A.get('effect_cohend_false_subtle'))}** | |",
              "",
              f"人类锚：d≈−0.2~−0.5。**方向判定**：{'通过' if (A.get('effect_cohend_false_share') or 0) < 0 else '未通过'}"
              f"（全部项）/ {'通过' if (A.get('effect_cohend_false_subtle') or 0) < 0 else '未通过'}（微妙项）\n"]
    if B:
        L += ["## B2 对立暴露反噬\n",
              "| 指标 | treatment | control |", "|---|---|---|",
              f"| 极端度变化 | {_fmt(B['treatment'].get('extremity_delta_mean'))} | {_fmt(B['control'].get('extremity_delta_mean'))} |",
              f"| 带符号位移（同化通道） | {_fmt(B['treatment'].get('sided_shift_mean'))} | {_fmt(B['control'].get('sided_shift_mean'))} |",
              f"| Cohen's d | **{_fmt(B.get('effect_cohend_extremity'))}** | |",
              "",
              f"人类锚（Bail 2018）：d≈+0.22~+0.35。**方向判定**：{'通过' if (B.get('effect_cohend_extremity') or -1) > 0 else '未通过'}；"
              "同化位移作为跨家族比较项保留。\n"]
    # 跨模型对照（自动扫描）
    import glob
    others = [os.path.basename(p)[len("h8v2_"):-len(".json")]
              for p in glob.glob(os.path.join(config.RESULTS_DIR, "h8v2_*.json"))]
    for other in [o for o in others if o != tag]:
        o = json.load(open(os.path.join(config.RESULTS_DIR, f"h8v2_{other}.json"), encoding="utf-8"))
        o_model = o.get("meta", {}).get("model", other)
        L += [f"## 跨模型家族对照（vs {other}：{o_model}）\n",
              f"| 指标 | {tag} | {other} |", "|---|---|---|"]
        for path_, lab in [(("C2", "dprime_mean"), "C2 d′"),
                           (("A2", "effect_cohend_false_share"), "A2 d(假分享)"),
                           (("A2", "effect_cohend_false_subtle"), "A2 d(微妙假分享)"),
                           (("B2", "effect_cohend_extremity"), "B2 d(极端度)")]:
            v1 = res.get(path_[0], {}).get(path_[1])
            v2 = o.get(path_[0], {}).get(path_[1])
            L.append(f"| {lab} | {_fmt(v1)} | {_fmt(v2)} |")
        L += ["", "**模型分离原则检查点**：方向一致 ⇒ 『跨家族稳健』；不一致 ⇒ 不得入先验（O6）。\n"]
    open(os.path.join(config.RESULTS_DIR, f"H8_V2_REPORT_{tag}.md"), "w",
         encoding="utf-8").write("\n".join(L))


def _fmt(v):
    return f"{v:.3f}" if isinstance(v, (int, float)) else "—"


if __name__ == "__main__":
    main()
