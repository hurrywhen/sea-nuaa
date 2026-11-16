# 主权认知获取（SEA）论文项目

[![DOI](https://zenodo.org/badge/1432112122.svg)](https://doi.org/10.5281/zenodo.23620919)

**Sovereign Epistemic Acquisition: Conditional Design for Pull, Push, and Weighted Recall**

人机协同信息获取项目之理论源头工作仓库。（项目原名"主权认识过滤（SEF）"，v1.0 起框架升级为"主权认知获取（SEA）"，SEF 成为其 push 过滤子模块。）

## 项目简介

核心命题：把信息获取从“平台为目标函数优化用户注意力”重构为“智能体为自己的第二序目标函数，在统一认知预算下联合优化主动获取（pull）与被动过滤（push）”。理论结果仅在各自显式假设与适用域内成立；试点证据用于机制检查和边界映射，不构成跨人群、跨语料的一般性验证。

理论源头文档：

- [`input/sovereign_epistemic_acquisition_EN_v1.9.md`](input/sovereign_epistemic_acquisition_EN_v1.9.md) —— **英文主稿（当前工作 master，v1.9 重构版）**：按最新拒稿意见重写为 32 页理论—审计稿。召回主对象改为加权平均召回／期望遗漏及覆盖—投递分解，不再把汇总覆盖当逐点 $p_{\min}$；价值模型改为所有信号共用一个误设更新核；补齐有限 top-$m$、Pareto 精确式、边界、固定容量子集选择和历史状态。证据明确标为 semi-oracle、事后、同语料判断层机制检查，新增金融口径、上游 digest、O/G 引用收益分解及数学回归。配套 [`docs/审稿回复与修改说明_v1.9.md`](docs/审稿回复与修改说明_v1.9.md)、[`docs/MINIMAL_VALID_EXPERIMENT_v1.9.md`](docs/MINIMAL_VALID_EXPERIMENT_v1.9.md)、[`docs/LITERATURE_SEARCH_v1.9.md`](docs/LITERATURE_SEARCH_v1.9.md) 与 [`sim/pilot/results/evidence_status_v1.9.json`](sim/pilot/results/evidence_status_v1.9.json)。复现说明见 [`docs/REPRODUCIBILITY_v1.9.md`](docs/REPRODUCIBILITY_v1.9.md)，候选工作树哈希见 [`docs/工件清单_v1.9.md`](docs/工件清单_v1.9.md)，候选 arXiv 包为 `latex/SEA_v1.9_arxiv_source.tar.gz`。S2d/S4/S5、时间外实验、独立人类数学复审和不可变 v1.9 发布仍未完成。
- [`input/sovereign_epistemic_acquisition_EN_v1.8.md`](input/sovereign_epistemic_acquisition_EN_v1.8.md) —— v1.8 历史主稿（125 页，保留供审稿对照；不作为当前召回与价值理论的权威表述）
- [`input/主权认知获取_统一理论_v1.8.md`](input/主权认知获取_统一理论_v1.8.md) —— 中文 v1.8 历史译文／内部审阅版，**尚未同步 v1.9，引用前须以英文新稿为准**
- **会议版 v1.0（通用双栏，6 页含参考文献；历史衍生版，未同步 v1.8 大修，引用前须复核）**：[`input/SEA_conference_EN_v1.0.md`](input/SEA_conference_EN_v1.0.md) / [`latex/SEA_conference_v1.0.pdf`](latex/SEA_conference_v1.0.pdf)；中文镜像 [`input/主权认知获取_会议版_v1.0.md`](input/主权认知获取_会议版_v1.0.md)。主线为四家族判断层机制重放与两域边界，21 条文献、2 张表。
- **期刊版 v1.0（通用单栏，30 页；历史衍生版，未同步 v1.8 大修，引用前须复核）**：[`input/SEA_journal_EN_v1.0.md`](input/SEA_journal_EN_v1.0.md) / [`latex/SEA_journal_v1.0.pdf`](latex/SEA_journal_v1.0.pdf)；中文镜像 [`input/主权认知获取_期刊版_v1.0.md`](input/主权认知获取_期刊版_v1.0.md)。主线为 SAP、核心定理与证明、精选验证，55 条文献、6 张表。版本分工与投稿适配见 [`docs/会议与期刊版本说明_v1.0.md`](docs/会议与期刊版本说明_v1.0.md)。
- 历史版本：v0.1 纲领稿、v1.0–v1.7（git 历史；逐轮审稿回复见 docs/审稿回复与修改说明_v1.1/v1.2/v1.4/v1.5/v1.6/v1.7.md）
- 工具：v1.9 新增 `tools/reproduce_v19_math.py`（总体/有限 top-m、Pareto、加权遗漏反例、统一更新和 RCT 回归）、`tools/test_v19_math.py`、`sim/sea_pilot/audit_v19_financial_caliber.py`、`audit_v19_upstream_digest.py`、`audit_v19_recall_value_tradeoff.py`；`tools/build_review_pdf.sh`（EN=lualatex / ZH=xelatex，支持 `en v1.9`；注入工件身份戳与 PDF 版本元数据）、`tools/build_venue_pdfs.sh`（会议/期刊 EN+ZH 构建，英文页数硬检查）、`tools/audit_venue_papers.py`（会刊版数值、引用、证据状态与文本层审计）、`tools/make_venue_manifest.py`（页数/公式/表格/SHA 工件清单）、`tools/audit_paper.py`（一致性审计，v1.6 核查 58 项 + v1.7 核查 22 项 + v1.8 专项 124 项及 manifest/数值/依赖/全量重算回归）、`tools/check_pdf_textlayer.py`（最终 PDF 文本层完整性检查）、`tools/make_public.py`（脱敏公开版构建器，GitHub/Gitee 就绪）、`tools/make_arxiv_source.sh`（arXiv 源包：pandoc→main.tex+anc/，本地 **XeLaTeX** 试编译与缺字形断言）；`sim/sea_pilot/audit_replay_integrity.py`（292 分片唯一键对账与 legacy run-level CI，默认只读）、`sim/sea_pilot/audit_three_family_dependence.py`（三家族日聚类/连续日块敏感性）、`sim/sea_pilot/recompute_replay_frozen.py`（四家族 17 场景唯一键全量重算，默认 stdout）、`docs/主验证唯一键处置与重分析规约.md`（冻结的唯一键冲突/缺口与全场景规则）

主要条件性结果（以 v1.9 正文为前提，均不得省略适用域）：

1. **统一误设更新** —— 所有观察信号共用一个更新核；完整模型正确时才有非负 VOI，误设 regret 可超过 VOI。五维评分仅是工程参数化，不是普遍充分统计量。
2. **过滤瓶颈与有限样本区分** —— 4.39 仅为命题级总体高斯单评分阈值模型数值；有限 top-$m$ 用次序统计量另行计算。Pareto 泄漏给精确 Gamma 和与明确近似式；贪心比只在证书化单调基集及匹配算法下成立。
3. **加权召回与覆盖—投递分解** —— 主恒等式为 $m_e=1-\kappa_e\delta_e$ 和 $\mathcal M_\nu=\sum_e\nu_em_e$；pooled 覆盖不是逐点 $p_{\min}$，CP 均值区间不是下确界区间，条件恢复不是独立证书，实际消费失败必须进入估计量。
4. **KKT 与固定容量选择** —— 保留角点 KKT；EIG 次模性要求给定 $(\omega,K)$ 的联合条件独立；top-$m$ 极限在 $m$-子集行动上建模，不使用单备选 logit 充当子集包含概率。
5. **目标写入与公共层** —— S3 改为禁止收入项＋授权写入＋反事实排序不变性；公共公告只具定义性共同知识条件，Jaccard 指标统一称 agenda-overlap index。
6. **证据状态** —— 现有结果仅为 semi-oracle、事后、共享语料的机制检查；S2d/S4/S5、完整时间外验证、人类数据和独立数学复审未完成，不支持 SEA 整体效果或部署召回保证。

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
| 一 | 理论奠基：公理、记号、定理、可检验主张 | ✅ v0.1 纲领稿；🚧 v1.9 条件性框架（2026-11，加权召回与统一误设更新；独立数学复核待完成） |
| 二 | 算法设计：命题图构建、多样性选择（子模优化）、冷却队列调度；v1.0 新增：双通道选择器、EIG 查询规划器、Pandora/Whittle 调度器、边际 VOI 预算分配器 | ✅ **已交付**（2026-09-30）：[`docs/算法设计_v1.0.md`](docs/算法设计_v1.0.md)（A1–A10 规范）+ `sim/sea_algo/` 参考实现 + 九项真实数据验证 **9/9**（含 O7 抗俘获认证首实现：market-only lift 0.615→1.230、market∪legal 0.626→1.359（弱富集，非独立确认）；报告 [`ALGO_VALIDATION_REPORT.md`](sim/pilot/results/ALGO_VALIDATION_REPORT.md)） |
| 三 | 仿真 + **AI 智能体队列机制检查**：合成生态 + 真实语料时序重放、处理臂 S0–S3 与消融、P1–P12、H1'–H9（`docs/AI智能体实验设计.md`） | 🚧 **既有试点已审计，结构识别未完成**：四家族 17 场景唯一键重算完成但属同语料探索；上游仅 70 个不同 digest，O 的 run-cluster p=0.1601，O/G 引用收益为负；金融旧新 m=5 均全部预算报警且为 semi-oracle。S2d/S4/S5、完整 P1–P12、独立时间窗与记忆审计仍未执行 |
| 四 | 在线人类数据锚点 + 团队自用遥测（转移桥） | 🚧 H8/H9 为家族依赖诊断，**现有所有家族均未获人类迁移认证**；不同 Brier 参考带不可通约。团队自用遥测仅有工程烟测，无真值、对照或召回/福利证据 |
| 五 | 实例化部署（个人参数填入） | ✅ **首跑完成、进入常态运转**（2026-09-30）：[`docs/部署手册_阶段五.md`](docs/部署手册_阶段五.md) + `sim/sea_deploy/`（g² 声明模板/每日管线/遥测周报）；域配置=P3 移植结论兑现（A8 关、A5 固定配额）；首跑 60 篇实时抓取 + LLM 重排（top-3 一致率 0.33——判断层实时纠正 v0 评分器语义盲区） |
| 六（推迟） | 人类 RCT（一个主要比较的设计值约 513 人、12 周）——future protocol，外部合作就位或需人类侧直接证据时启动；多重性和纵向功效仍待定 | 推迟 |

## 公开版说明

本仓库为脱敏公开版：内部基础设施信息（备份体系、内网地址、本机路径）已做脱敏处理；研究内容、数据与内部版本一致。详见 `PUBLIC_NOTES.md`。
