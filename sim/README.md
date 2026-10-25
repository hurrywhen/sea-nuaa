# sim/ — 阶段三：仿真与 AI 智能体实验

论文《主权认知获取》验证纲领（§14–§15）的实现。**当前状态（2026-09-27）：双域试点 v2 + H8 验证电池首跑（本地真实 LLM）+ LLM 智能体重放接入**。

| 实验 | 报告 | 一句话结论 |
|---|---|---|
| P3 研究者 × arXiv 2019-09（OpenAlex） | [`pilot/results/PILOT_REPORT.md`](pilot/results/PILOT_REPORT.md) | 定理 6.1 恒等式 corr=0.968；H4 强形式在低冗余域**被拒绝**并精确化；发现 p̂_min 内生性（机构清单 0.17–0.37 vs 作者清单 0.02） |
| P2 投资者 × EDGAR + archive.org 新闻层（10 域）2019-09（v3） | [`pilot/results/P2_REPORT.md`](pilot/results/P2_REPORT.md) | **ρ_c=8.19 落入论文区间 [5,20]**；多类 p̂_min（监管 1.00/0.70 + 通讯社 0.25 + 财经 0.15）；诚实 d′ 双真值分裂（legal **3.49** / market 0.54）；组合直通 m=5 组合内召回 **0.910**（v2 为 0.952，新闻稀释效应——H4 逼近未越线）；恒等式 corr=0.987；90% 移动日不可归因 → 公共层刚需 |
| 阶段三交付物：**默认先验表 v0.1** | [`pilot/results/DEFAULT_PRIORS_v0.1.md`](pilot/results/DEFAULT_PRIORS_v0.1.md) | 22 参数全量汇总（实测/机制验证/条件性/冻结四态口径），`make_priors.py` 可再生成 |
| H9 校准转移桥（三家族完成） | [`pilot/results/H9_REPORT_ornith.md`](pilot/results/H9_REPORT_ornith.md) 等 | ornith Brier=**0.170**（带内，超级预测者水平）/ qwen 0.231（略超带）/ gemma **0.279 差于常数基线**——θ_cal 锚**仅推理型家族成立**，校准质量成选型硬指标（O6） |
| **阶段二算法参考实现（sea_algo A1–A10）** | [`pilot/results/ALGO_VALIDATION_REPORT.md`](pilot/results/ALGO_VALIDATION_REPORT.md) | 九项真实数据验证 **9/9**：A1 恒等式逐位复现（1876 命题/ρ_c 8.19）；**A8 抗俘获认证把 lift 0.61×修复至 1.23×**（联合口径 0.63→1.36，O7 首实现）；A3 EIG 查询 6 vs 随机 2 vs 频率 4；A5 自适应分配命中 11≥固定 10 且浪费名额 0 vs 11；A9 防火墙三档冲动率下关键召回最高 0.341→0.581、有用冲动回收 ~93%；A10 等渗重校准 ECE 0.288→0.113（保单调）；A4 诚实零结果（p̂ 排序无增益——价值在名额阈值纪律）；A6 贪心/最优比 1.000；A7 金融域半月 Jaccard 0.09（换手远剧于学术域） |
| **阶段二 P3 学术域移植验证** | [`pilot/results/ALGO_VALIDATION_REPORT_P3.md`](pilot/results/ALGO_VALIDATION_REPORT_P3.md) | 域可移植性 **8/8**（ρ_c=1.0、单信源类、引用真值年延迟）：**A8 认证在单类域退化**（k_c≥2 不可达——理论预言的移植边界，非缺陷）；A6 贪心@k=15 覆盖 25 critical vs 随机 15（次模优势）且 > 部署 cite-ranked 清单 19；**A5 自适应命中 12<固定 16（诚实负结果）**——P3 清单供给稳定、固定已零浪费，自适应探索成净成本 ⇒ A5 价值 ∝ 通道 I 供给波动性（域条件性，按波动性门控降级）；A3 EIG ≥随机但输纯频率（真值延迟）⇒ 主动查询价值 ∝ 1/真值延迟 |
| **阶段五部署首跑 + 阶段四遥测上线（2026-09-30）** | [`sea_deploy/out/digest_2026-09-30.md`](sea_deploy/out/digest_2026-09-30.md) · [`docs/部署手册_阶段五.md`](../docs/部署手册_阶段五.md) | arXiv 实时 60 篇 → g² 决策集评分 → gemma4:26b（native API + **think:false** 守卫）重排 → 简报 + 遥测首条落盘；LLM×参数化 top-3 一致率 0.33——判断层实时纠正关键词评分器语义盲区（把 LLM 校准论文关联到『实验设计』rel=0.9，关键词只给『工具』0.29）＝判断层增量价值（p=6.8×10⁻²⁸）的部署实例；新节点 <内网地址已脱敏> 三模型接入（ornith prefill 4.2 tok/s ⇒ 长提示场景禁用） |
| 统计强化（CMH，含 qwen 复样 480 agent-day） | [`pilot/results/THREE_FAMILY_ANALYSIS.md`](pilot/results/THREE_FAMILY_ANALYSIS.md) | LLM vs 诚实特征臂 **p=6.8×10⁻²⁸**（Σb:Σc=457:123）；vs 半oracle **p=0.017**（qwen 家族 p=0.036，CI [+0.002,+0.130]）——判断层价值与对半oracle优势均统计确认 |
| P3 升级：清单优化（定理 7.3/命题 8.1）× 真实特征评分器 | [`pilot/results/p3up_report.md`](pilot/results/p3up_report.md) | 真实特征 d′=**0.77**；**嵌入二期 d′=0.73**（nomic-embed-v2@Ollama，6606 标题）——两个独立特征族收敛同水平：瓶颈在关键性的内在不可预测性，不在表示工程（距需求线 4.39 一个量级）；配额可行清单覆盖—可行性权衡是绑定约束；零后见清单跨月迁移弱 ⇒ 滚动更新必需 |
| **H8 验证电池（ornith-1.5-35b 本地后端）** | [`pilot/results/H8_REPORT.md`](pilot/results/H8_REPORT.md) | 三范式一过一败一天花板：Bail 反噬方向通过（d=0.36，人类同带）但机制不同构（LLM 大幅同化）；准确性提示方向失败（地板效应+机制缺席）；d′=3.77 触知识天花板 ⇒ **双向失真预言被证实**，仅 B 纳入先验 |
| LLM 智能体 × P3 真实重放（**三家族定稿**） | [`pilot/results/llm_replay_STATUS.md`](pilot/results/llm_replay_STATUS.md) · [`THREE_FAMILY_ANALYSIS.md`](pilot/results/THREE_FAMILY_ANALYSIS.md) | 240 agent-day × 3 家族 + qwen 复样 480：LLM 判断臂召回 0.401/0.457/**0.515** **全部≈2× 诚实特征臂（0.23–0.25）**；**qwen 合并对半 oracle 参数臂（0.448）McNemar p=0.036 显著、三家族 CMH p=0.017**；冲动消费率 45→29% 跨家族；**H8 v2.1 三家族定稿**：C2 防记忆材料 d′ 回落人类区间（1.13/1.41/1.99）✓、A2 方向三家族一致为负（−0.52~−0.55 强）✓、**B2 极端度跨家族方向不一致（+1.26/+0.84/−0.75）⇒ 不入先验进 O6**、同化通道三家族同号（最稳健 LLM 特有发现） |

| 合成生态与 σ* 相变（P10，纯参数化） | [`pilot/results/ECOSYSTEM_REPORT.md`](pilot/results/ECOSYSTEM_REPORT.md) | 三类型相图与定理 9.3 解析边界**精确吻合**（σ*_ms=0.06、σ*_sh=0.20）；命题 9.2 灭绝速率下界 33 格点全成立；Red Queen 定量化（检测器更新把有效 σ* 从最坏漂移 0.15 钉回均值 0.086）；O1 耦合玩具发现 (σ,x_m) **极限环** |
| 清单滚动更新对照（10 月评估，零后见） | [`pilot/results/ROLLING_REPORT.md`](pilot/results/ROLLING_REPORT.md) | 新鲜清单（8–9月窗）p̂_min 0.231→0.269，机构月换手 Jaccard 0.39（61% 换血）——滚动重建必要；但总召回对新鲜度不敏感：配额饱和下瓶颈是清单内排序质量（与 P2 发现同构） |
| 公共层 Ω 下界 × 冗余认证（定理 12.1 / 引理 12.1） | [`pilot/results/P5_OMEGA_REPORT.md`](pilot/results/P5_OMEGA_REPORT.md) | 500 主体 × P2 真实语料：**Ω=0.168 ≥ γ/(2−γ)=0.111 下界成立**（无公共层 0.066，共享现实 2.5×，下界紧）；**认证反转发现**：新闻层扩至 10 域后 k_c=2 认证 lift 0.63×<1——原始覆盖计数被注意力俘获，认证统计量须改相对稀缺性/质量加权（论文 §12.2 实证限定 + 开放问题 O7） |

两域对照构成理论的第一张**实证适用域地图**：召回保证强度 = $p_{\min}$ 的制度来源（法律 > 媒体冗余 > 清单设计）× 供给—配额适配 × E* 作用域与 persona 决策集的一致性。

## 快速开始

```bash
cd sim
# 数据（有缓存则跳过；raw/ 不入库，可重建）
python3 sea_pilot/fetch_openalex.py     # P3：arXiv 2019-09 + 前窗（OpenAlex）
python3 sea_pilot/fetch_p2.py many      # P2：EDGAR submissions ×505 + Yahoo 日线 ×309
python3 sea_pilot/fetch_news.py         # P2 新闻层：archive.org CDX（Reuters/CNBC/Fortune/BI）+ Wikimedia pageviews
python3 sea_pilot/fetch_p2.py gdelt     # （可选）GDELT DOC API——数据中心 IP 被限流，需换出口
# 实验
python3 -m sea_pilot.run_pilot          # P3 试点（<2s）
python3 -m sea_pilot.run_p2             # P2 试点 v2（~1s）
python3 -m sea_pilot.run_p3up           # 清单优化 × 真实特征评分器（~2s）
python3 -m sea_pilot.h8_battery         # H8 验证电池（本地 LLM，~22 min）
SEA_LLM_BASE_URL=http://<内网地址已脱敏>:1234/v1 SEA_LLM_API_KEY=lm-studio SEA_LLM_MODEL=ornith-1.5-35b \
  python3 -m sea_pilot.run_llm_replay --days 8 --agents 2   # LLM 智能体真实重放（已跑通：15/16 天）
SEA_EMB_URL=http://<内网地址已脱敏>:11434/v1/embeddings SEA_EMB_MODEL=nomic-embed-text-v2-moe:latest \
  python3 -m sea_pilot.run_p3embed      # 嵌入特征评分器（Ollama，~5.5 min，d′=0.73）
python3 -m sea_pilot.agents_llm         # harness mock 演示（--openai 用真实后端）
# 第二模型家族（模型分离原则）：gemma4:31b-it-bf16 @ http://<内网地址已脱敏>:11434/v1（Ollama，与 LM Studio 隔离）
# 报告
python3 -m sea_pilot.report && python3 -m sea_pilot.report_p2
# 纯参数化实验（不占 LLM 资源）
python3 -m sea_pilot.run_ecosystem      # 合成生态 + σ* 相变（P10）+ Red Queen + O1 玩具（~1 min）
python3 -m sea_pilot.run_rolling        # 清单滚动更新对照（10 月评估；需先抓 arxiv_2019-10）
python3 -m sea_pilot.run_p5_omega       # 公共层 Ω 下界（定理 12.1）+ 冗余认证（引理 12.1）
python3 -m sea_pilot.analyze_families   # 三家族重放统一分析（McNemar + CMH 分层合并 + bootstrap + 诚实特征臂）
python3 -m sea_pilot.make_priors        # 默认先验表 v0.1（阶段三交付物，可再生成）
python3 -m sea_pilot.h9_calibration --model-tag ornith   # H9 校准转移桥（Manifold 人类锚 × 智能体 Brier）
python3 -m sea_algo.validate          # 阶段二参考实现九项验证（A1–A10，零 LLM、<60s）
python3 -m sea_algo.validate_p3       # P3 学术域移植验证（ρ_c=1.0、单类、延迟真值，<30s）
python3 -m sea_deploy.daily_run --llm # 阶段五部署：每日简报（arXiv 实时流×g²画像×LLM判断层）+阶段四遥测
python3 -m sea_deploy.telemetry_report  # 团队自用遥测周报（S4 审计同源）
python3 sea_pilot/fetch_news.py         # 新闻层第二批（10 域，CDX wildcard 前缀）
```

依赖：Python ≥3.10、numpy、matplotlib（仅报告图）。无 scipy/pandas/torch 依赖；LLM 层零依赖（urllib + OpenAI 兼容接口，`SEA_LLM_BASE_URL/SEA_LLM_API_KEY/SEA_LLM_MODEL`）。

## 模块结构

```
sea_pilot/
  config.py            全部可调参数（画像、预算、ρ 扫描、配额、真值阈值）
  fetch_openalex.py    P3 数据通道（OpenAlex works + group_by 作者频次）
  fetch_p2.py          P2 数据通道（EDGAR submissions / Yahoo chart / GDELT DOC）
  fetch_news.py        P2 新闻层（archive.org CDX 前缀查询 + Wikimedia pageviews，无需换出口）
  corpus.py            P3 命题归并 κ、E* 真值、三种零后见监测清单
  p2_environment.py    P2 命题归并、双真值（legal/market）、信源类、组合清单、新闻层合并
  scorer.py            参数 proxy、实测 d′、定理 6.1 恒等式（纯 numpy 正态尾函数）
  features.py          真实特征评分器：TF-IDF 新颖度 + 声望 + logistic（零后见训练）
  watchlist_opt.py     定理 7.3 次模贪心（二值/概率两版）+ 命题 8.1 Pandora 指数
  strategies.py        S0/S1/S2（双通道+配额）/S2c
  metrics.py           召回（含组合条件分解）、精度、失真 D vs D*、理论界检验
  agents_llm.py        LLM 智能体层：persona 卡、宪法门控、冲动注入、S4 日志、双后端
  h8_battery.py        H8 验证电池：三范式重放（准确性提示/对立暴露/辨别 d′）+ 效应量报告
  run_pilot.py         P3 主实验    run_p2.py  P2 主实验    run_p3up.py  升级实验
  run_llm_replay.py    LLM 智能体 × P3 真实重放（真实后端 vs 参数化对照臂）
  report.py / report_p2.py          报告与图生成
pilot/
  data/raw/            原始抓取缓存（gitignore；OpenAlex ~55MB、EDGAR ~300MB、Yahoo、news_cdx）
  data/corpus_2019-09_ai.csv        P3 派生语料（入库）
  results/             明细/聚合 CSV、summary JSON、四份报告、fig/、llm_demo/llm_replay 日志
```

## 下一步（P2 报告 §5 + p3up 报告）

(a) 换网络出口补齐 GDELT 新闻层 → 复测 ρ_c、S1 基线与不可归因日；(b) EDGAR daily-index 全量抓取修复宇宙稀疏；(c) 清单**滚动更新**策略（月度重估）对 p̂_min 迁移性的修复实验；(d) 真实 LLM 后端接入 + H8 验证电池（重放 Bail/Pennycook 范式）；(e) 合成生态生成器（§14.1）与 σ* 相变（P10）。
