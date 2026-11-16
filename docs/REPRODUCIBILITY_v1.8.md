# v1.8 复现说明（工作修订）

## 1. 不可变归档与工作修订的边界

- v1.7 不可变代码/记录：`https://github.com/hurrywhen/sea-nuaa/tree/v1.7.0`
- v1.7 完整 commit：`fdc4912a30174d71b944d1ec83fcfda260f8ebf1`
- 版本 DOI：`https://doi.org/10.5281/zenodo.23620920`
- 概念 DOI：`https://doi.org/10.5281/zenodo.23620919`
- v1.8 源稿与新增审计目前是工作修订，**不包含在上述 v1.7 归档中**。正式公开前须创建新 commit、源/数据快照与 DOI，并回填论文可用性段；不得以 main 分支的浮动状态代替不可变发布。逐项发布闸门见 `docs/RELEASE_CHECKLIST_v1.8.md`，该清单本身不是 release manifest。
- **归档警示**：不可变 v1.7 正文和 Zenodo 元数据仍保留已被取代的“73,547 valid agent-days”称谓；v1.8 审计取代该描述，但不属于 v1.7 归档。正式 v1.8 release metadata 必须改用唯一键口径，不回改不可变 v1.7。

## 2. 重放完整性审计

环境：Python 3.12.3（源码支持 Python ≥3.10）、NumPy 2.3.5。锁定文件：

- `sim/sea_pilot/runtime-replay-integrity.txt`
- `sim/sea_pilot/requirements-replay-integrity.txt`

在仓库根目录：

```bash
python3 -m venv .venv-replay-integrity
.venv-replay-integrity/bin/pip install --requirement sim/sea_pilot/requirements-replay-integrity.txt
PYTHONDONTWRITEBYTECODE=1 .venv-replay-integrity/bin/python sim/sea_pilot/audit_replay_integrity.py
```

默认严格只读，仅向 stdout 输出。只有显式 `--write` 才生成两个专用工件；已有工件还须 `--force` 才覆盖。脚本不会修改 292 个原始 JSONL，也不会选择首条/末条或作其他事后去重。

输出：

- `sim/pilot/results/REPLAY_INTEGRITY_AUDIT.json`：80-run manifest、重复示例和 legacy exploratory CI；
- `sim/pilot/results/REPLAY_INTEGRITY_AUDIT.md`：对账结果和运行说明。

预期总计：73,704 raw、157 empty、73,547 valid、71,914 unique、1,633 duplicate excess、较名义 72,000 缺 86、25/80 runs 少于 900 unique。Legacy CI 标记为 `LEGACY_EXPLORATORY_NOT_DEDUPLICATED`，不是新冻结主结果。

**处置规约与全量重算均已完成**：见 `docs/主验证唯一键处置与重分析规约.md`。主规则按指标充分字段“值一致则归并、值冲突则缺失”，不选择首条/末条；86 缺口分为 56 个仅存空记录与 30 个当前快照无记录，主分析不插补。规约同时固定共同 cohort、严格单例、attempt 等权均值、五种结果盲哈希、零消费情景及部分识别端点。由于旧结果已被查看，这属于 `CONTROLLED_UNIQUE_KEY_REANALYSIS__WITHIN_CORPUS_EXPLORATORY`，不是 prospective preregistration。

```bash
# 默认只在 stdout 重算并打印报告，不写文件
PYTHONDONTWRITEBYTECODE=1 python3 sim/sea_pilot/recompute_replay_frozen.py
# 写入独立工件目录；已有七类工件时须另加 --force
PYTHONDONTWRITEBYTECODE=1 python3 sim/sea_pilot/recompute_replay_frozen.py --write
# 合成测试（20 项）
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=sim python3 -m unittest -v sea_pilot.test_replay_frozen
```

输出目录 `sim/pilot/results/frozen_reanalysis_v1/` 包含：

- `summary.json`：17 场景的全部 run 等权/pooled 估计、CI、McNemar/BH(4)、三种 CMH 和 run-cluster 结果；
- `REPORT.md`：完整场景矩阵与解释限制；
- `run_metrics.csv`：1,360 个 run 场景行；
- `key_ledger.jsonl.gz`：72,000 条逐键处置账本；
- `input_manifest.json`：292 个输入的路径、大小、行数和 SHA-256；
- `SPECIFICATION.md` 与 `environment.json`：规约快照、脚本/规约/输入哈希及环境。

结构核验：A 解析 recall 71,573、Δvalue 70,676、sign 71,618；B/C/D/E 分别为 70,676/70,306/70,525/71,914；56 个 `EMPTY_ONLY` 与 30 个 `NO_SURVIVING_ROW` 分开处理。主规则 A 的 Δrecall 各家族均正，但 O 区间跨零且 O run-cluster p=0.160128；Δvalue C/Q 正、O/G 负。旧管线结果继续保留 `LEGACY_EXPLORATORY_NOT_DEDUPLICATED`，不与新重算混名。

## 2b. 三家族依赖敏感性（另一项实验）

三家族实验不继承四家族重复键问题的机械降级。为检验其历史 agent-day 独立近似，新增：

```bash
PYTHONDONTWRITEBYTECODE=1 python3 sim/sea_pilot/audit_three_family_dependence.py
# 仅在需要更新专用工件时：
PYTHONDONTWRITEBYTECODE=1 python3 sim/sea_pilot/audit_three_family_dependence.py --write

# 合成单元测试（口径、日聚类展开与循环块边界）
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=sim python3 -m unittest sim/sea_pilot/test_three_family_dependence.py -v
```

脚本不调用 LLM、不修改原始 JSONL，也不覆盖 `three_family_analysis.json` 或 `THREE_FAMILY_ANALYSIS.md`。诚实特征臂由原确定性管线离线重建。输出为：

- `sim/pilot/results/THREE_FAMILY_DEPENDENCE_SENSITIVITY.json`
- `sim/pilot/results/THREE_FAMILY_DEPENDENCE_SENSITIVITY.md`

每种方法、每家族、每对照使用 10,000 次百分位 bootstrap，种子 20261103。日聚类把同一模拟日的全部记录一起重抽样；循环连续 5 日块进一步保留短程序列结构。参数臂召回对照沿用旧管线“全部记录”口径；诚实特征配对对照沿用非空 `picked` 口径。

这些是**事后、同语料依赖敏感性区间**，不是预注册独立 run 证据。它们不消除共享语料、标签、上游 digest、模型记忆或跨家族依赖。历史 CMH/McNemar 只报告为所述分层和依赖近似下的名义统计量。

## 2c. 审稿人报告的局部 Lean 检查（本仓库未复现）

审稿人报告，官方 Lean Web 已编译 `quadratic_corner_is_optimal`、`activation_loss_is_quadratic`、`producer_threshold_exceeds_one` 与 `mixed_attestation_not_subset_of_two_manipulations`。据该报告，前三项的公理输出为 `propext`、`Classical.choice`、`Quot.sound`，第四项无公理依赖；四项均无 `sorryAx` 或自定义公理。

当前工作树没有相应 `.lean` 源文件、Lean 工具链锁或编译日志，本次修订也没有独立 rerun，故这些内容只能作为**审稿人报告的局部数学对象检查**引用，不能列入本仓库已复现工件。它们不认证整篇论文、现实语义或统计结论。尤其 `mixed_attestation_not_subset_of_two_manipulations` 只表示 raw-count 为 2 而植入数小于 2 的局部计数事实，没有形式化旧 `A_manip`，也没有证明反事实必要性；它与修订后 Lemma 12.1 的混合反例一致，不能称为“Lean 推翻 Lemma 12.1”。p.29 互信息反例及其他文字批评同样不因此获得 Lean 认证。

若正式发布希望把这些检查升级为可复现工件，须另附源码、Lean/Mathlib 版本锁、`#print axioms` 输出和干净环境复验日志；在此之前正文继续保持上述归属与范围限制。

## 3. 论文一致性与 PDF 构建

当前环境：Pandoc 3.6.4；TeX Live 2026（LuaHBTeX 1.24.0；XeTeX 0.999998）。

```bash
python3 tools/audit_paper.py
bash tools/build_review_pdf.sh en
bash tools/build_review_pdf.sh zh
bash tools/make_arxiv_source.sh
python3 tools/check_pdf_textlayer.py latex/SEA_EN_v1.8_draft.pdf
```

中文字体为 Noto Serif CJK SC，西文和等宽字体为构建脚本列出的 DejaVu 变体。arXiv 源包使用 XeLaTeX。上述命令复现源稿一致性检查和 PDF，不重新调用 LLM。

## 4. 数据快照与已知限制

公开源重建脚本只提供溯源路径。实时 API、OpenAlex 引用计数、EDGAR 历史、CDX 抓取与网页内容均可变化，因此逐位一致仅针对已识别发布中的冻结工件，不针对重新下载。

当前发布说明继续保留以下缺口：H9 原始答案记录不完整；嵌入缓存不完整；缺少独立命名的 v2 原始输出；替代引用代理敏感性分析缺少可独立复核工件。没有真实 URL 时，不声称公开 OSF 注册或匿名评审链接。

可用 `sha256sum` 对发布清单中的文件逐项核验；正式 v1.8 发布时应把脚本、manifest、源稿、依赖锁和 PDF 的 SHA-256 一并写入不可变 release manifest。

## 5. 论文主稿

- 英文：`input/sovereign_epistemic_acquisition_EN_v1.8.md`
- 中文：`input/主权认知获取_统一理论_v1.8.md`
- 大修逐条回复：`docs/审稿回复与修改说明_v1.8.md`

本说明不构成形式化证明认证、独立人类数学复核、无泄漏时间外验证或人类有效性证据。
