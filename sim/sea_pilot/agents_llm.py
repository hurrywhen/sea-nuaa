"""任务 3：LLM 智能体层 harness（docs/AI智能体实验设计.md §2 的最小可运行实现）。

设计原则（对应论文）：
  - 框架层强制：预算 T 由 harness 执行，不信任模型自觉（公理 1 的工程化）；
  - g¹ 冲动注入：以画像相关概率在 digest 中插入"高唤起标记"条目（框架层外生注入，
    LLM 无内脏冲动——docs/LLM模拟人类 §2）；
  - 反思层 R：宪法文件（constitution）决定慢尺度批准（试点为规则式自动批准+抽样人审）；
  - S4 审计：每个决策写 JSONL 日志（选项、理由、预算、注入标记）；
  - 后端可插拔：MockBackend（确定性启发式，CI/无 key 环境）与 OpenAI 兼容后端
    （设置 SEA_LLM_BASE_URL / SEA_LLM_API_KEY / SEA_LLM_MODEL 启用真实 LLM）。

本 harness 验证的是接口与协议；行为真实感结论须待真实后端 + 验证电池（H8）后作出。
"""
from __future__ import annotations

import json
import os
import time
import urllib.request
from dataclasses import dataclass, field

# 协议 v2（调度规约 P-4）：思考预算封顶。声明参数，须与论文参数表一致。
MAX_TOKENS_INIT = int(os.environ.get("SEA_MAX_TOKENS_INIT", "1200"))
MAX_TOKENS_CAP = int(os.environ.get("SEA_MAX_TOKENS_CAP", "2400"))
# 规约 R-7/R-8：免费配额节拍（秒/调用，0=不限）与付费成本熔断（美元/进程）。
MIN_INTERVAL = float(os.environ.get("SEA_MIN_INTERVAL", "0"))
COST_CAP_DEFAULT = 2.0
COST_CAP = float(os.environ.get("SEA_COST_CAP", str(COST_CAP_DEFAULT)))

import numpy as np


@dataclass
class PersonaCard:
    pid: str
    summary: str                 # 画像一句话（docs/典型画像_参数标定.md）
    decision_set: list[str]      # g² 声明的决策集 D
    watchlist: list[str]         # 监测清单模板
    budget_per_day: int          # 名额（框架层强制）
    impulse_p: float = 0.15      # g¹ 注入概率（画像相关）
    constitution: str = "默认宪法：仅批准容差带内课程变更；紧急行动限白名单可逆操作"


P3_CARD = PersonaCard(
    pid="P3", summary="AI 方向研究者：选题/实验/写作/合作决策；低冗余域，清单是命脉",
    decision_set=["选题与转向", "实验设计", "论文写作与投稿", "工具/数据集采用", "合作与招聘"],
    watchlist=["top-50 竞争者与协作者作者", "关键机构 release 页", "顶会 accept 列表"],
    budget_per_day=3, impulse_p=0.08)

P2_CARD = PersonaCard(
    pid="P2", summary="投资者：持仓/止损/对冲/事件驱动；高冗余域，时效与防火墙是命脉",
    decision_set=["持仓增减", "止损", "对冲", "事件驱动交易", "欺诈标的回避"],
    watchlist=["持仓公司披露(EDGAR/巨潮)", "交易所公告", "监管公告栏", "通讯社财经频道"],
    budget_per_day=8, impulse_p=0.25)


@dataclass
class DigestItem:
    iid: str
    title: str
    source: str
    salience: float = 0.0        # 框架层注入的唤起标记（g¹ 通道）
    channel: str = "II"          # I=直通, II=评分发现, PUB=公共层


class Backend:
    def complete(self, system: str, user: str) -> str:
        raise NotImplementedError


class MockBackend(Backend):
    """确定性启发式后端：按标题关键词价值排序选 top-k（harness 测试用，非行为结论）。"""

    def complete(self, system: str, user: str) -> str:
        import re
        ids = re.findall(r"\[id=(\S+?)\]", user)
        k = re.search(r"预算=(\d+)", user)
        k = int(k.group(1)) if k else 3
        picked = ids[:k]  # 顺序即框架预排序（mock 不做重排）
        return json.dumps({"consume": picked, "reason": "mock-heuristic"})


class OpenAICompatBackend(Backend):
    def __init__(self, base_url: str | None = None, api_key: str | None = None,
                 model: str | None = None, timeout: int = 60):
        self.base_url = (base_url or os.environ.get("SEA_LLM_BASE_URL", "")).rstrip("/")
        self.api_key = api_key or os.environ.get("SEA_LLM_API_KEY", "")
        self.model = model or os.environ.get("SEA_LLM_MODEL", "")
        self.timeout = timeout
        if not (self.base_url and self.api_key and self.model):
            raise RuntimeError("需要 SEA_LLM_BASE_URL / SEA_LLM_API_KEY / SEA_LLM_MODEL")

    def complete(self, system: str, user: str) -> str:
        import sys as _sys
        import time as _time
        interval = float(os.environ.get("SEA_MIN_INTERVAL", str(MIN_INTERVAL)))
        cost_cap = float(os.environ.get("SEA_COST_CAP", str(COST_CAP)))
        if interval > 0:
            _time.sleep(interval)   # 规约 R-7：免费配额节拍（车道内串行，等效节流）
        max_tokens = MAX_TOKENS_INIT   # 协议 v2（规约 P-4）
        mismatch_waits = 0
        for attempt in range(12):
            payload = {
                "model": self.model,
                "messages": [{"role": "system", "content": system},
                             {"role": "user", "content": user}],
                "temperature": 0.3,
                "max_tokens": max_tokens,
            }
            num_ctx = os.environ.get("SEA_NUM_CTX")   # 规约 R-11：node-a 防 OOM
            if num_ctx:
                payload["options"] = {"num_ctx": int(num_ctx)}
            provider_order = os.environ.get("SEA_PROVIDER_ORDER")   # 规约 R-14：F 429 规避
            if provider_order:
                payload["provider"] = {"order": [p.strip() for p in provider_order.split(",") if p.strip()]}
            body = json.dumps(payload).encode()
            req = urllib.request.Request(
                f"{self.base_url}/chat/completions", data=body,
                headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.api_key}"})
            try:
                with urllib.request.urlopen(req, timeout=600) as r:
                    d = json.loads(r.read())
                # 规约 R-8：付费成本熔断（OpenRouter 在 usage.cost 返回美元成本）
                cost = (d.get("usage") or {}).get("cost")
                if cost is not None:
                    self._cost = getattr(self, "_cost", 0.0) + float(cost)
                    if self._cost > cost_cap:
                        print(f"  [backend] 成本熔断：累计 ${self._cost:.4f} > ${cost_cap}",
                              file=_sys.stderr)
                        return json.dumps({"consume": [], "reason": "backend-failure-costcap"})
                got_model = str(d.get("model") or "")
                if got_model and self.model and got_model != self.model:
                    # 服务端被其他任务抢占（响应来自别的模型）：等待窗口后重试
                    mismatch_waits += 1
                    if mismatch_waits > 8:
                        raise RuntimeError(f"model mismatch persists: {got_model}")
                    print(f"  [backend] 服务端当前由 {got_model} 应答（抢占），30s 后重试 "
                          f"({mismatch_waits}/8)", file=_sys.stderr)
                    _time.sleep(30)
                    continue
                c = d["choices"][0]["message"].get("content") or ""
                if c.strip():
                    return c
                # 推理型模型可能把预算耗在 reasoning_content：加倍重试（协议 v2 上限 2400）
                max_tokens = min(max_tokens * 2, MAX_TOKENS_CAP)
                print(f"  [backend] attempt {attempt+1}: empty content, doubling budget",
                      file=_sys.stderr)
            except Exception as e:  # noqa: BLE001
                import urllib.error as _ue
                if isinstance(e, _ue.HTTPError) and e.code == 429:
                    # 规约 R-7：限流是瞬态故障，延长退避
                    wait = min(600, 60 * (attempt + 1))
                    print(f"  [backend] HTTP 429 限流，{wait}s 后重试", file=_sys.stderr)
                    _time.sleep(wait)
                    continue
                if isinstance(e, _ue.HTTPError) and 400 <= e.code < 500:
                    # 规约 P-6：4xx 是确定性故障（如模型被卸载），立即失败，勿重试
                    print(f"  [backend] HTTP {e.code}（确定性故障，快速失败）", file=_sys.stderr)
                    return json.dumps({"consume": [], "reason": f"backend-failure-http{e.code}"})
                print(f"  [backend] attempt {attempt+1} failed: {e}", file=_sys.stderr)
                _time.sleep(min(30, 5 * (attempt + 1)))
        return json.dumps({"consume": [], "reason": "backend-failure"})


class LLMAgent:
    def __init__(self, card: PersonaCard, backend: Backend, seed: int = 0,
                 log_path: str | None = None):
        self.card = card
        self.backend = backend
        self.rng = np.random.default_rng(seed)
        self.consumed: set[str] = set()
        self.day = 0
        self.impulse_hits = 0     # g¹ 注入被消费的次数（俘获面测量）
        self.log = open(log_path, "a", encoding="utf-8") if log_path else None

    def daily_step(self, digest: list[DigestItem]) -> dict:
        self.day += 1
        # 框架层：g¹ 冲动注入（外生，画像相关概率）
        injected = []
        for it in digest:
            if self.rng.random() < self.card.impulse_p:
                it.salience = 1.0
                it.title = "【突发】" + it.title
                injected.append(it.iid)
        # 框架层：预排序（直通优先 → 公共层 → 评分；唤起标记影响呈现顺序 = 攻击面）
        order = sorted(digest, key=lambda x: (x.channel != "I", x.channel != "PUB", -x.salience))
        budget = self.card.budget_per_day
        sys_p = (f"你是 {self.card.pid} 画像的信息获取代理。委托人决策集：{self.card.decision_set}。"
                 f"宪法：{self.card.constitution}。推理从简。只输出 JSON：{{\"consume\": [id...], \"reason\": str（一句话）}}")
        lines = [f"第{self.day}日候选（预算={budget}，超限无效）："]
        for it in order[:18]:
            lines.append(f"[id={it.iid}] ({it.channel}|{it.source}) {it.title}")
        raw = self.backend.complete(sys_p, "\n".join(lines))
        dec, picked = None, []
        try:
            dec = json.loads(raw[raw.find("{"): raw.rfind("}") + 1])
            valid = [x.iid for x in order]
            vset = set(valid)
            consume = dec.get("consume", [])
            if isinstance(consume, str):                       # 容错：逗号分隔字符串
                consume = [s.strip() for s in consume.split(",")]
            seen = set()
            for p in consume:
                s = str(p).strip().strip('"\'` ')
                hit = None
                if s in vset:
                    hit = s
                else:                                           # 容错：ID 嵌入在更长字符串中
                    for v in valid:
                        if v and v in s:
                            hit = v
                            break
                if hit and hit not in seen:
                    seen.add(hit)
                    picked.append(hit)
                if len(picked) >= budget:
                    break
        except Exception:  # noqa: BLE001
            dec = {"reason": "parse-error", "raw_head": raw[:200]}
        self.consumed.update(picked)
        self.impulse_hits += sum(1 for p in picked if p in injected)
        rec = {"day": self.day, "picked": picked, "injected": injected,
               "impulse_consumed": [p for p in picked if p in injected],
               "reason": (dec or {}).get("reason", ""),
               "raw_consume": (dec or {}).get("consume", None)}   # 原始输出留痕（S4）
        if self.log:
            self.log.write(json.dumps(rec, ensure_ascii=False) + "\n")
            self.log.flush()
        return rec


def run_demo(n_agents: int = 3, days: int = 5, backend: Backend | None = None,
             out: str = "pilot/results/llm_demo.jsonl") -> dict:
    """Mock 后端演示：验证 harness 协议（预算强制/注入/审计日志）。"""
    backend = backend or MockBackend()
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w").close()
    rng = np.random.default_rng(11)
    agents = [LLMAgent(P3_CARD if i % 2 == 0 else P2_CARD, backend, seed=i, log_path=out)
              for i in range(n_agents)]
    for d in range(days):
        digest = [DigestItem(f"d{d}i{j}", f"候选内容 {j}（模拟）", f"src{j%7}",
                             channel=("I" if j % 11 == 0 else "II")) for j in range(40)]
        for a in agents:
            a.daily_step([DigestItem(x.iid, x.title, x.source, x.salience, x.channel) for x in digest])
    summary = {
        "backend": type(backend).__name__, "n_agents": n_agents, "days": days,
        "consumed_per_agent": [len(a.consumed) for a in agents],
        "budget_compliance": all(len(a.consumed) <= a.card.budget_per_day * days for a in agents),
        "impulse_hits": [a.impulse_hits for a in agents],
        "log": out,
    }
    return summary


if __name__ == "__main__":
    import sys
    be = None
    if "--openai" in sys.argv:
        be = OpenAICompatBackend()
    s = run_demo(backend=be)
    print(json.dumps(s, ensure_ascii=False, indent=1))
