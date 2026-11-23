# 主权认知获取（SEA）论文项目

[![DOI](https://zenodo.org/badge/1432112122.svg)](https://doi.org/10.5281/zenodo.23620919)

**Sovereign Epistemic Acquisition: A Conditional Framework and Synthetic Audit Artifacts**

**当前公开候选快照 `v1.17.0`**：[GitHub](https://github.com/hurrywhen/sea-nuaa) · [Gitee](https://gitee.com/jiangsu-yunhefeng-intelligent_0/sea-nuaa) · [发布说明](RELEASE_v1.17.md)。这是 v1.16.0 综合评审后的小修候选：以只读 `next_period` 和精确连续提交序列阻止重复/倒退/跳期伪造冻结切换边界；零完成测量返回完成率、assigned/completed/unknown 计数及结构化 `not_estimable` 和代表性警告，不再抛 pooled 异常或把份额偏移写成 0；手工 S12 协方差增加联合 3×3 半正定检查；分层误差率与完成率增加分指标异质性、样本量和 Wilson 95% 区间。保留外生冻结协议、单线控制、声明重置例外和精确拒绝语义。不是独立数学复审、真实测量验证、联合最优算法或端到端有效性认证；v1.17 专属 DOI 待登记。页首 Zenodo 徽章仅指向历史 v1.7 概念归档。历史版本见 [`archive/README.md`](archive/README.md)，均已标为已被取代。

## 项目简介

核心问题是：谁有权读取、授权写入、回滚和审计目标，以及 pull/push 如何在多资源预算下把原始候选转变为实际消费。理论结果仅在各自显式假设与适用域内成立；历史重放只提供 selected proxy，不能证明投递、打开、实际阅读、决策价值或人类福利。

当前权威文档：

- [`input/sovereign_epistemic_acquisition_EN_v1.17.md`](input/sovereign_epistemic_acquisition_EN_v1.17.md) —— **当前英文主稿**：条件化 SAP 框架（登记入状态、外生协议转移、严格连续真实期次、冻结切换时机、声明重置例外、单线控制）、治理/纵向执行器工件、操作性 attendance 与失败复合遗漏、目标版本规则、回顾性审计边界。PDF 为 `latex/SEA_EN_v1.17_draft.pdf`，候选 arXiv 包为 `latex/SEA_v1.17_arxiv_source.tar.gz`。
- [`docs/审稿回复与修改说明_v1.17.md`](docs/审稿回复与修改说明_v1.17.md) —— 对 v1.16.0 综合评审意见的逐条回复。
- [`docs/REPRODUCIBILITY_v1.17.md`](docs/REPRODUCIBILITY_v1.17.md) —— 公开复现命令、冻结输入、无 Git 验证和 target-aware provenance 流程。
- [`docs/MINIMAL_VALID_EXPERIMENT_v1.17.md`](docs/MINIMAL_VALID_EXPERIMENT_v1.17.md) —— 尚未执行的匹配实验：唯一主要比较与结局、AND attendance 判定、臂别缺失极端边界、目标版本新评价队列、解锁前误分类验证、可迁移性分层诊断、联合半正定协方差/联合 bootstrap、Wilson 区间、零完成结构化诊断与臂间误差比较（§1.4.1）。
- [`docs/SUPPLEMENT_FORMAL_AND_SECONDARY_v1.17.md`](docs/SUPPLEMENT_FORMAL_AND_SECONDARY_v1.17.md) 与 [`docs/SUPPLEMENT_RETROSPECTIVE_AUDITS_v1.17.md`](docs/SUPPLEMENT_RETROSPECTIVE_AUDITS_v1.17.md) —— 移出的标准证明/数值恒等，以及全部回顾性家族估计、区间、符号计数和 17 情景（Rule A/strict-singleton/17 情景表仅在后者 §R5，由冻结数据再生成核对）。
- [`sim/pilot/results/evidence_status_v1.17.json`](sim/pilot/results/evidence_status_v1.17.json) 与 `docs/工件清单_v1.17.md` —— 机器可读证据状态和目标标签／提交明确的逐文件哈希。
- [`archive/README.md`](archive/README.md) —— 历史版本索引；v1.16 及更早英文稿、中文稿、会议/期刊衍生版均已被取代，中文稿未同步当前英文主稿。

主要工具：`sim/sea_governance/`（18 项治理符合性）、`sim/sea_sap/`（最小纵向执行器、协议登记转移演示、匹配实现 fixture、目标构造审计）、`tools/reproduce_v110_sap.py`（SAP 算例与 17/22 反例）、`sim/sea_pilot/audit_v110_consumption_caliber.py`（三个回顾性口径、72,000 键、17 情景和未来日志 schema）、`tools/check_pdf_layout.py`、`tools/audit_v117.py`、`tools/make_v117_manifest.py`、`tools/make_retrospective_tables.py`。脚本名中的 v110/v19 是为复现保留的稳定文件名，不代表当前稿件版本。

主要条件性结果（均不得省略适用域）：

1. **SAP 闭合但不联合求解** —— 状态、观察、行动、转移、奖励、五类预算、授权和回滚显式定义；组件近似不自动组合为联合最优。
2. **可执行治理** —— 未授权写入拒绝、目标与排序回滚、固定供给不变性、供给生态单独记录、审计篡改检测均有合成测试；不等于恶意主机安全或人类有效控制。
3. **统一误设更新与过滤纠偏** —— 所有信号共用一个更新核；总体阈值不等于有限 top-m；容量下界是 oracle 松弛；Pareto 量是期望之比。
4. **加权遗漏与操作性消费** —— $m_e=1-c_e\delta_e$；选择、投递、打开、操作性 attendance 分别测量，潜在真实消费与失败复合结局分离。历史 `picked` 只是 selected proxy，空选择/无记录补零仅是事后敏感性。
5. **公开复现** —— 金融历史 CSV 固定在快照内并校验 SHA-256，不再依赖公开历史中不存在的 Git 对象；扩展重建与历史冻结行聚合分别标记。
6. **证据边界** —— S2d/S4/S5、时间外/私域语料、point-in-time／记忆审计、人类数据、第三方复现和独立人类数学复审未完成，不支持整体效果或部署召回保证。

## 目录结构

```
input/      理论源头文档（纲领论文各版本稿）
docs/       工作文档（笔记、评审意见、修改记录）
sim/        仿真实现（阶段三，论文第 10 节设计）
latex/      论文排版（后续投稿版本）
```

## 路线图（论文第 13 节）

| 阶段 | 内容 | 状态 |
|---|---|---|
| 一 | 理论奠基：SAP、条件组件、可检验主张 | 🚧 v1.17 严格真实期次、零完成结构化诊断、联合协方差半正定检查与分层 Wilson 区间（2026-11；无联合最优声称，独立数学复核待完成） |
| 二 | 算法设计：命题图构建、多样性选择（子模优化）、冷却队列调度；v1.0 新增：双通道选择器、EIG 查询规划器、Pandora/Whittle 调度器、边际 VOI 预算分配器 | ✅ **已交付**（2026-09-30）：[`docs/算法设计_v1.0.md`](docs/算法设计_v1.0.md)（A1–A10 规范）+ `sim/sea_algo/` 参考实现 + **历史九项验证 9/9（2026-09-30 口径，非当前版本端到端验证）**（含 O7 抗俘获认证首实现：market-only lift 0.615→1.230、market∪legal 0.626→1.359（弱富集，非独立确认）；报告 [`ALGO_VALIDATION_REPORT.md`](sim/pilot/results/ALGO_VALIDATION_REPORT.md)） |
| 三 | 仿真 + **AI 智能体队列机制检查**：合成生态 + 真实语料时序重放、处理臂 S0–S3 与消融、P1–P12、H1'–H9（`docs/AI智能体实验设计.md`） | 🚧 **既有试点已审计，结构识别未完成**：四家族 17 场景唯一键重算完成但属同语料探索；上游仅 70 个不同 digest，O 的 run-cluster p=0.1601，O/G 引用收益为负；金融旧新 m=5 均全部预算报警且为 semi-oracle。S2d/S4/S5、完整 P1–P12、独立时间窗与记忆审计仍未执行 |
| 四 | 在线人类数据锚点 + 团队自用遥测（转移桥） | 🚧 H8/H9 为家族依赖诊断，**现有所有家族均未获人类迁移认证**；不同 Brier 参考带不可通约。团队自用遥测仅有工程烟测，无真值、对照或召回/福利证据 |
| 五 | 实例化部署（个人参数填入） | ✅ **首跑完成、进入常态运转**（2026-09-30）：[`docs/部署手册_阶段五.md`](docs/部署手册_阶段五.md) + `sim/sea_deploy/`（g² 声明模板/每日管线/遥测周报）；域配置=P3 移植结论兑现（A8 关、A5 固定配额）；首跑 60 篇实时抓取 + LLM 重排（top-3 一致率 0.33——判断层实时纠正 v0 评分器语义盲区） |
| 六（推迟） | 人类 RCT——仅未来提出人类学习、福利或迁移主张时必需；不是当前条件性设计／审计论文的前置条件 | 推迟；无参与者数据 |

## 公开版说明

本仓库为脱敏公开版：内部基础设施信息（备份体系、内网地址、本机路径）已做脱敏处理；研究内容、数据与内部版本一致。详见 `PUBLIC_NOTES.md`。
