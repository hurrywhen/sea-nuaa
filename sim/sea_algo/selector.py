"""A2 双通道选择器 + A9 冲动防火墙/冷却队列。

A2（定理 6.1 分工：召回由结构承担、精度由评分承担；定理 6.3 贪心+阈值）：
  通道 I（清单直通）名额 = ⌈quota·m⌉，内部按 A4 保留值序；
  通道 II（评分发现）名额 = 余量，按诚实特征评分序（d′ 0.54–0.77 实测——只作排序不作召回保证）；
  供给不足报警 → 触发 A5 重分配（配额饱和是常态，报警机制全程有效系 P2/P3 实测）。
A9（g¹ 通道防御；定理 11.1 Ulysses 预先授权）：
  salience 超阈条目不得直接占用名额 → 隔离 → 冷却 τ 日 → 实质审查再入（salience 按
  decay^τ 折减后以内容效用参与排序）；白名单（g² 声明的紧急类）旁路但强制 S4 审计；
  白名单本身只能经 S2 签字修订（防火墙的防火墙）。
  框架层强制、不依赖模型自律——LLM 冲动消费率实测 29–45%（推理型最高）。
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Item:
    iid: str
    channel: str = "II"          # I=清单直通, II=评分发现, Q=主动查询, PUB=公共层
    score: float = 0.0           # 通道内排序分（A4 保留值 / 诚实评分 / EIG）
    salience: float = 0.0        # 框架层注入的唤起标记（g¹ 通道）
    utility: float = 0.0         # 真实效用（验证用；部署时由 A10 校准后的判断层给出）
    critical: bool = False       # 地面真值（仅验证用）
    meta: dict = field(default_factory=dict)


class DualChannelSelector:
    def __init__(self, m: int, quota: float = 0.6, sal_thr: float = 0.5,
                 cooldown_tau: int = 2, salience_decay: float = 0.5,
                 whitelist: tuple = (), firewall: bool = True):
        self.m = m
        self.quota = quota
        self.sal_thr = sal_thr
        self.tau = cooldown_tau
        self.decay = salience_decay
        self.whitelist = set(whitelist)
        self.firewall = firewall
        self.cooldown: list[tuple[int, Item]] = []
        self.audit: list[dict] = []

    def select_day(self, day: int, items: list[Item]) -> dict:
        # 1) 冷却期满 → 实质审查再入（salience 已衰减；以 utility 作为再入排序分）
        reentered, still = [], []
        for (ready, it) in self.cooldown:
            if day >= ready:
                it.salience *= self.decay ** self.tau
                it.score = it.utility                       # 实质审查：内容效用取代凡性
                reentered.append(it)
                self.audit.append({"day": day, "iid": it.iid, "act": "cooldown_release"})
            else:
                still.append((ready, it))
        self.cooldown = still

        # 2) 防火墙：salience 超阈 → 隔离（白名单旁路 + S4 强制审计，定理 11.1）
        pool = []
        quarantined = 0
        for it in list(items) + reentered:
            if (self.firewall and it.salience > self.sal_thr
                    and it.meta.get("tag") not in self.whitelist):
                self.cooldown.append((day + self.tau, it))
                quarantined += 1
                self.audit.append({"day": day, "iid": it.iid, "act": "quarantine"})
            elif it.salience > self.sal_thr:               # 白名单旁路
                self.audit.append({"day": day, "iid": it.iid, "act": "whitelist_bypass"})
                pool.append(it)
            else:
                pool.append(it)

        # 3) 双通道配额选择
        m1 = max(1, int(round(self.quota * self.m)))
        ch1 = sorted([i for i in pool if i.channel == "I"], key=lambda x: -x.score)
        rest = sorted([i for i in pool if i.channel != "I"], key=lambda x: -x.score)
        consumed = ch1[:min(m1, len(ch1))]
        slots_left = self.m - len(consumed)
        consumed += rest[:slots_left]
        alarm = len(ch1) < m1                              # 通道 I 供给不足报警 → A5
        return {"day": day, "consumed": consumed, "quarantined": quarantined,
                "alarm_ch1_undersupply": alarm,
                "wasted_slots": self.m - len(consumed)}


def firewall_sim(days: int, m: int, impulse_p: float, useful_frac: float = 0.2,
                 n_crit_per_day: int = 2, tau: int = 2, firewall: bool = True,
                 seed: int = 0, n_base: int = 8) -> dict:
    """A9 参数化机制仿真（非 LLM；impulse_p 取先验表家族实测 0.29–0.45）。

    每日 n_base 个常规通道 I 条目（含 n_crit_per_day 个关键）+ 逐名额冲动注入：
    每个名额以 impulse_p 概率出现 salience 条目（真实效用 u~U(0,1)，u>1−useful_frac 为有用）。
    无防火墙：salience 条目直接以唤起强度抢占名额（消费与 u 无关——显著性劫持）；
    有防火墙：隔离→τ 日冷却→实质审查（接受当且仅当 u 过阈）——有用冲动延迟回收、
    无用冲动丢弃、常规名额受保护。
    """
    import random
    rng = random.Random(seed)
    crit_hits = wasted = imp_consumed = imp_useful_total = imp_useful_recovered = 0
    pending: list[tuple[int, float]] = []                  # (ready_day, u)
    for d in range(days):
        ready = [u for (rd, u) in pending if rd <= d]
        pending = [(rd, u) for (rd, u) in pending if rd > d]
        slots = m
        # 冷却再入的实质审查：u 过阈才占名额
        for u in ready:
            if u > 1.0 - useful_frac and slots > 0:
                imp_useful_recovered += 1
                slots -= 1
        crit_pool = n_crit_per_day
        base_avail = n_base
        while slots > 0 and base_avail > 0:
            if rng.random() < impulse_p:                   # 冲动注入抢占该名额
                imp_consumed += 1
                u = rng.random()
                imp_useful_total += int(u > 1.0 - useful_frac)
                if firewall:
                    pending.append((d + tau, u))           # 隔离进冷却
                    # 名额未被消费（防火墙保护）：继续用常规条目填
                else:
                    slots -= 1                             # 无防火墙：名额被显著性吃掉
                    base_avail -= 0
                    continue
            # 常规条目填位
            if crit_pool > 0 and rng.random() < crit_pool / max(1, base_avail):
                crit_hits += 1
                crit_pool -= 1
            base_avail -= 1
            slots -= 1
        wasted += slots
    return {"impulse_p": impulse_p, "firewall": firewall, "crit_hits": crit_hits,
            "impulse_consumed": imp_consumed,
            "impulse_useful_seen": imp_useful_total,
            "impulse_useful_recovered": imp_useful_recovered,
            "wasted_slots": wasted,
            "crit_recall": crit_hits / max(1, days * n_crit_per_day)}
