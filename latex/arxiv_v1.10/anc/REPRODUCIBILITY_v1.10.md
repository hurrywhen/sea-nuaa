# SEA v1.10 公开候选快照复现说明

## 1. 状态与证据边界

- 当前版本：`v1.10.0` candidate / prerelease。
- GitHub：https://github.com/hurrywhen/sea-nuaa
- Gitee：https://gitee.com/jiangsu-yunhefeng-intelligent_0/sea-nuaa
- 路线：条件性组件、治理接口与证据审计；不是联合最优 SAP 算法或已验证系统。
- 独立人类数学复审、第三方干净环境复现、S2d/S4/S5、时间外/私域语料、实际消费新实验、人类数据和公共实验注册仍未完成。
- v1.7 DOI `10.5281/zenodo.23620920` 不覆盖 v1.9/v1.10；v1.10 专属 DOI 未登记。
- 所有核心 Python 审计不调用 LLM、不下载数据、不创建人类数据。默认只读；`--write` 才写专用工件，覆盖还需 `--force`。

## 2. 依赖

核心计算：Python ≥3.10、NumPy。治理参考与 SAP 算例只用标准库。`future_logging_schema.json` 是 Draft 2020-12；结构校验可使用 `jsonschema`，但不是核心审计硬依赖。

论文构建：Pandoc ≥3、LuaLaTeX（内审 PDF）、XeLaTeX（arXiv 候选包）、完整 DejaVu 字体、Poppler（`pdfinfo`、`pdftotext`、`pdftoppm`）。`tools/check_pdf_layout.py` 只需要标准库和 Poppler。

## 3. 关键冻结输入

### 3.1 重放

`sim/pilot/results/` 包含 292 个主重放分片和 5 个隔离的非主 tag 文件。`audit_v110_consumption_caliber.py` 逐文件核验哈希、字节数和行数，并读取既有 `frozen_reanalysis_v1` 的 Rule A/C 与 17 情景结果。

### 3.2 金融历史输入

`sim/pilot/results/v19_financial_caliber_audit/historical_p2_rows_8ffc7f5.csv` 是历史 `p2_rows.csv` 的独立逐字节冻结副本：

- 来源提交：`8ffc7f5`（仅 provenance）；
- 来源路径：`sim/pilot/results/p2_rows.csv`；
- 生成规则：逐字节复制，不过滤、不换行、不重算；
- 数据行：1,260；字节：382,663；
- SHA-256：`80e953d19efb44787d4fb8b03e37ee6cbfbfc325488769df8a0e89281b495024`。

脚本默认验证哈希、字节和行数，**不调用 Git**。历史 120/126 与 0.722222 是冻结行聚合，历史选择和公司—日分母未独立重建；扩展配置的参数 S2p 选择及 121/133、114/126、7/7、150 则实际重建；两个配置的 S2p-feat 都仍是冻结行聚合。历史供给 4.6/day 是继承常量，并非从该 CSV 验证。上述状态不可混写。

## 4. 核心命令

### 4.1 数学、SAP 算例和治理

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v \
  tools/test_v19_math.py tools/test_v110_sap.py

PYTHONDONTWRITEBYTECODE=1 python3 tools/reproduce_v19_math.py \
  --write --force
PYTHONDONTWRITEBYTECODE=1 python3 tools/reproduce_v110_sap.py \
  --write --force

(
  cd sim
  PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v \
    sea_governance.test_reference \
    sea_pilot.test_replay_frozen \
    sea_pilot.test_audit_v19_financial_caliber
)
(
  cd sim
  PYTHONDONTWRITEBYTECODE=1 python3 -m sea_governance.conformance \
    --output pilot/results/governance_conformance_v1.10.json
)
```

预期：9 项旧数学回归、4 项 SAP 算例回归、14 项治理符合性、20 项冻结重放回归、3 项金融公开输入回归。数量表示实现一致性，不是独立数学证明或端到端有效性。

### 4.2 重放、消费口径与金融

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  sim/sea_pilot/audit_v110_consumption_caliber.py --write --force
PYTHONDONTWRITEBYTECODE=1 python3 \
  sim/sea_pilot/audit_v19_financial_caliber.py --write --force
PYTHONDONTWRITEBYTECODE=1 python3 \
  sim/sea_pilot/audit_v19_upstream_digest.py --write --force
PYTHONDONTWRITEBYTECODE=1 python3 \
  sim/sea_pilot/audit_v19_recall_value_tradeoff.py --write --force
```

`v110_consumption_caliber/` 包含七个工件：`summary.json`、`REPORT.md`、`run_metrics.csv`、`scenario_effects.csv`、`key_ledger.jsonl.gz`、`future_logging_schema.json`、`input_manifest.json`。主要结果：

- 72,000 预期键 = 71,970 已存在键 + 30 缺失键；
- `ITT_ALL_RECORD_MEAN`：已存在键内所有记录等权，`picked=[]` 只对 selected proxy 补零；不是实际消费 ITT；
- G：71,629/70,732/71,674；Rule A：71,573/70,676/71,618；strict-singleton：70,306；
- 全部 17 情景和符号变化公开；区间为探索性 run-level 描述区间。

### 4.3 稿件、布局与 arXiv 包

```bash
PYTHONDONTWRITEBYTECODE=1 python3 tools/audit_v110.py
bash tools/build_review_pdf.sh en v1.10
python3 tools/check_pdf_textlayer.py \
  latex/SEA_EN_v1.10_draft.pdf \
  input/sovereign_epistemic_acquisition_EN_v1.10.md
python3 tools/check_pdf_layout.py \
  latex/SEA_EN_v1.10_draft.pdf \
  --json tools/pdf_layout_v1.10.json
bash tools/make_arxiv_source.sh v1.10
```

`check_pdf_layout.py` 以页面坐标检查左右 20pt 安全带，能复现旧 v1.9 第 27 页的横向溢出；发布还需用 `pdftoppm` 渲染并目检 SAP 图、遗漏图、识别图、宽表和复现命令页。文本层检查和坐标检查都不能单独替代完整视觉审阅。

## 5. 无 `.git` 公开副本检查

金融脚本必须在无 `.git` 且 `PATH` 没有 Git 的环境中完成默认和 `--write --force`。其他核心 Python 审计也只使用快照内冻结输入。可这样检查金融项：

```bash
env -i HOME="$HOME" PATH=/usr/bin:/bin \
  PYTHONDONTWRITEBYTECODE=1 \
  /usr/bin/python3 sim/sea_pilot/audit_v19_financial_caliber.py
```

如果 Python/NumPy 安装在其他前缀，应使用对应解释器，而不是恢复 Git 依赖。发布者另在干净公开副本中执行第 4.1–4.2 节命令并比较工件。第三方独立重跑仍不得因此宣称已完成。

本版已在无 `.git` 的脱敏公开副本实际完成 17 组验证命令：13 项数学/SAP、37 项治理/重放/金融测试、四类数据审计、100 项发布审计、PDF/arXiv 构建，以及 PATH 无 Git 的金融默认和 `--write --force`。公开 arXiv 的 714 个附件哈希全部通过。机器报告为 `tools/clean_verification_v1.10.json`。这是**作者执行的公开副本验证**，不是第三方独立复现；不同时刻的 PDF/压缩包可因构建时间产生不同二进制哈希，报告将“干净重建哈希”与金融固定输入哈希分开。

## 6. 工件清单与 arXiv 附件

发布者在 Git 工作树中运行：

```bash
SEA_RELEASE_STATUS=PUBLIC_CANDIDATE_RELEASE__PRERELEASE \
SEA_RELEASE_ID=v1.10.0 \
SEA_GITHUB_URL=https://github.com/hurrywhen/sea-nuaa \
SEA_GITEE_URL=https://gitee.com/jiangsu-yunhefeng-intelligent_0/sea-nuaa \
PYTHONDONTWRITEBYTECODE=1 python3 tools/make_v110_manifest.py
```

生成 `docs/工件清单_v1.10.{md,json}`，记录核心文件、292 主分片和 5 隔离文件的 SHA-256。清单不是 DOI 或第三方签核。arXiv 候选包位于 `latex/SEA_v1.10_arxiv_source.tar.gz`，其 `anc/SHA256SUMS` 可逐文件核验；处理器选择 XeLaTeX。

## 7. 不可从历史数据重建的内容

历史分片没有 delivered/opened/attended/actual-consumption 字段，也没有完整 calls、input/output tokens、cost、latency、retries。`raw_consume` 是原始输出诊断，`impulse_consumed` 是注入冲动指标，均不能替代目标信息的实际消费。空选择也无法统一区分为合法 abstention 或静默执行失败。任何这些字段的“恢复”都必须是新实验，而不是本次离线重分析。

## 8. 后续直接实验

`docs/MINIMAL_VALID_EXPERIMENT_v1.10.md` 冻结了建议的识别结构：唯一主要比较为 SEA 对同模型端到端筛选，唯一主要结局为全分配实际消费加权遗漏；RAG、福利推荐和消融为次要分析。需要独立语料/月份功效模拟、锁定语料、严格 point-in-time、记忆审计、效率日志和结果解锁前公共注册。该协议目前未执行。
