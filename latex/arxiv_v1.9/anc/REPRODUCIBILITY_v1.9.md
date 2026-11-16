# v1.9 复现说明（工作修订，非不可变发布）

## 1. 边界

- 英文主稿：`input/sovereign_epistemic_acquisition_EN_v1.9.md`
- PDF：`latex/SEA_EN_v1.9_draft.pdf`
- 审稿回复：`docs/审稿回复与修改说明_v1.9.md`
- 证据状态：`sim/pilot/results/evidence_status_v1.9.json`
- 本工作树**不是** v1.7 DOI 归档的一部分，也尚不是带持久标识的 v1.9 公共复现包。
- 以下脚本不调用 LLM、不创建人类数据；新增分析均为同语料、事后、描述性审计，不是前瞻确证实验。

## 2. 环境

已实际使用：Python 3.12.3、NumPy 2.3.5、Pandoc、LuaLaTeX、pdftotext/pdfinfo、DejaVu 字体。有限 top-$m$ 的计算只依赖 NumPy 和标准库，不需要 SciPy。

## 3. 数学回归

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tools/test_v19_math.py
PYTHONDONTWRITEBYTECODE=1 python3 tools/reproduce_v19_math.py --write --force
```

输出：

- `sim/theory_v1.9/math_results.json`
- `sim/theory_v1.9/MATH_REPORT.md`
- `sim/theory_v1.9/script_sha256.txt`

覆盖：4.389337888、AUC、1.5/2.5 召回、Pareto 精确/近似、有限 top-$m$ 精确积分与 Monte Carlo、加权遗漏反例、统一更新二元例和 RCT 设计值。九项单元测试通过，覆盖高预算、极尾、在线阈值边界和 KL 子集选择。Monte Carlo 区间只量化数值模拟误差，不是实证置信区间。

## 4. 金融口径审计

```bash
PYTHONDONTWRITEBYTECODE=1 python3 sim/sea_pilot/audit_v19_financial_caliber.py --write --force
```

输出目录：`sim/pilot/results/v19_financial_caliber_audit/`。

- 当前配置逐 agent/proxy 重建选择，命题召回与冻结 `p2_rows.csv` 在 1e-12 内一致；
- 旧配置通过 `git show 8ffc7f5:sim/pilot/results/p2_rows.csv` 只读取得；
- 旧 120/126、新 121/133，新配置另有 19 命题、18 公司—日、10 公司；
- 公司—日敏感性 114/126；
- 旧新 m=5 全部报警、每月 150 位置、非严格每日上限；
- supervised feature-scorer 0.722222/0.789474（前半月已实现标签监督训练、全月描述评价、确定性选择重复记账，不是独立 held-out 实验）；
- 19 个目标的接受时刻分类和逐命题×类别覆盖矩阵。

该脚本依赖仓库 git 历史读取旧配置；公开复现包应把相应旧快照及 SHA-256 一并归档，而不能只依赖浮动分支。

## 5. 上游 digest 审计

```bash
PYTHONDONTWRITEBYTECODE=1 python3 sim/sea_pilot/audit_v19_upstream_digest.py --write --force
```

输出目录：`sim/pilot/results/v19_upstream_digest_audit/`。

52 个目标中每个 run 有 24–33 个进入 digest；80 个模型—种子配置对应 70 个不同完整 digest，O/G 有 10 对共享 digest。所有 Channel-II digest 均由 2026 引用相关 proxy 构造。输出每个 run 的目标数、比例和完整 digest SHA-256，并分别记录 `run_seed` 与实际 `proxy_seed=99+run_seed`、lite 输入哈希和构造脚本哈希。

## 6. 引用收益分解

```bash
PYTHONDONTWRITEBYTECODE=1 python3 sim/sea_pilot/audit_v19_recall_value_tradeoff.py --write --force
```

输出目录：`sim/pilot/results/v19_recall_value_tradeoff/`。

使用严格单例场景 C（70,306 键），逐键核对记录的 `value_llm/value_param` 与重新映射的 $\log(1+\text{citation})$ 总收益，再分解为关键项和非关键项。80 个 run 全部保留，run 等权均值与 10,000 次 run bootstrap 一并输出。该指标不是决策效用或福利；分解不构成因果解释。脚本还逐 run 断言 80/80 的 recall、return 和 cell 数与冻结 Scenario C 一致，O 的关键项分量区间跨零、C/Q 的非关键分量区间跨零均保留。

## 7. 既有唯一键重分析

```bash
PYTHONDONTWRITEBYTECODE=1 python3 sim/sea_pilot/recompute_replay_frozen.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=sim python3 -m unittest -v sea_pilot.test_replay_frozen
```

既有 292 分片、17 场景、唯一键账本和输入 SHA-256 位于 `sim/pilot/results/frozen_reanalysis_v1/`。其状态仍是 `CONTROLLED_UNIQUE_KEY_REANALYSIS__WITHIN_CORPUS_EXPLORATORY`，不是 prospective preregistration。

## 8. PDF 构建与检查

```bash
bash tools/build_review_pdf.sh en v1.9
python3 tools/check_pdf_textlayer.py \
  latex/SEA_EN_v1.9_draft.pdf \
  input/sovereign_epistemic_acquisition_EN_v1.9.md
```

当前结果：32 页；文本层/源稿去空白字符比 0.92；18 个二级标题无断裂；问题 0。另有 `PYTHONDONTWRITEBYTECODE=1 python3 tools/audit_v19.py` 对源稿、关键数值、覆盖矩阵、证据状态和 PDF 的 **100/100 项检查通过**，报告为 `tools/audit_v19_report.json`。这些检查不证明数学正确性或所有页面的视觉质量；正式投稿前仍需独立人类复审和逐页目检。

候选 arXiv 源包可用 `bash tools/make_arxiv_source.sh v1.9` 构建。当前 XeLaTeX 试编译为 32 页、Missing character=0；`latex/SEA_v1.9_arxiv_source.tar.gz` 约 26 MB，含 main.tex、00README.XXX、anc/SHA256SUMS、全部 292 个主重放分片和 5 个隔离的非主 tag 文件（共 297 个 JSONL）、数据快照、日志和审计源码。它是**候选工作包**，不是带 DOI 的不可变正式发布。

## 9. 发布前缺口

1. 独立人类数学签核；
2. S2d/S4/S5、完整消融、独立时间窗和知识截止后/私域语料；
3. 匿名化记忆审计和严格 point-in-time 特征；
4. 公共注册 URL；
5. 不可变 commit、全部数据快照、全部 292 分片与日志、模型/量化/访问日期、哈希 manifest 和持久 DOI/URL；
6. 干净环境第三方重跑。

因此，当前文档只能称**可复核的工作修订**，不能称独立核验后的公开定稿。
