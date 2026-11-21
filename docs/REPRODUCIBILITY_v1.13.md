# SEA v1.13 公开候选快照复现说明

## 1. 状态与证据边界

- 当前版本：`v1.13.0` candidate / prerelease。
- GitHub：https://github.com/hurrywhen/sea-nuaa
- Gitee：https://gitee.com/jiangsu-yunhefeng-intelligent_0/sea-nuaa
- 路线：条件化框架＋治理/执行器参考工件＋可 falsify 审计规范；不是联合最优 SAP 算法或已验证系统。
- 四种状态必须分开：代码测试通过、历史数据可重算、理论经独立复核、系统效果已验证。当前仅前两项中的作者侧检查完成；独立数学复核、第三方复现、真实匹配实验和人类数据均未完成。
- v1.7 DOI `10.5281/zenodo.23620920` 不覆盖 v1.9/v1.10/v1.11/v1.13；v1.13 专属 DOI 未登记。
- 所有核心 Python 审计不调用 LLM、不下载数据、不创建人类数据。默认只读；`--write` 才写专用工件，覆盖还需 `--force`。

## 2. 依赖

核心计算：Python ≥3.10、NumPy。治理参考、SAP 算例和纵向执行器只用标准库。`future_logging_schema.json` 是 Draft 2020-12；结构校验可使用 `jsonschema`，但不是核心审计硬依赖。

论文构建：Pandoc ≥3、LuaLaTeX（内审 PDF）、XeLaTeX（arXiv 候选包）、完整 DejaVu 字体、Poppler（`pdfinfo`、`pdftotext`、`pdftoppm`）。`tools/check_pdf_layout.py` 只需要标准库和 Poppler。

## 3. 关键冻结输入

### 3.1 重放

`sim/pilot/results/` 包含 292 个主重放分片和 5 个隔离的非主 tag 文件。`audit_v110_consumption_caliber.py` 逐文件核验哈希、字节数和行数，并读取既有 `frozen_reanalysis_v1` 的 Rule A/C 与 17 情景结果。

### 3.2 金融历史输入

`sim/pilot/results/v19_financial_caliber_audit/historical_p2_rows_8ffc7f5.csv` 是历史 `p2_rows.csv` 的独立逐字节冻结副本：

- 来源提交：`8ffc7f5`（仅 provenance）；
- 数据行：1,260；字节：382,663；
- SHA-256：`80e953d19efb44787d4fb8b03e37ee6cbfbfc325488769df8a0e89281b495024`。

脚本默认验证哈希、字节和行数，**不调用 Git**。历史 120/126 与 0.722222 是冻结行聚合，历史选择和公司—日分母未独立重建；扩展配置的参数 S2p 选择及 121/133、114/126、7/7、150 则实际重建；两个配置的 S2p-feat 都仍是冻结行聚合。历史供给 4.6/day 是继承常量，并非从该 CSV 验证。

### 3.3 合成纵向执行器输入

`sim/sea_sap/fixtures/longitudinal.json` 与 `target_construction.json` 是公开合成 fixture，不含人类数据。参考语料快照哈希、候选—目标链接、可用性证据、资源成本、attendance 阈值和终端事件均显式冻结。执行器不访问网络或真实模型。

## 4. 核心命令

### 4.1 数学、SAP 算例、治理与纵向执行器

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
    sea_pilot.test_audit_v19_financial_caliber \
    sea_pilot.test_audit_v110_consumption_caliber \
    sea_sap.test_executor \
    sea_sap.test_target_construction
)
(
  cd sim
  PYTHONDONTWRITEBYTECODE=1 python3 -m sea_governance.conformance \
    --output pilot/results/governance_conformance_v1.13.json
)
PYTHONDONTWRITEBYTECODE=1 python3 sim/sea_sap/reproduce.py \
  --write --force
```

预期：9 项旧数学回归、4 项 SAP 算例回归、18 项治理符合性、20 项冻结重放回归、3 项金融公开输入回归、6 项消费口径／未来 schema 回归、14 项纵向执行器回归和 4 项目标构造回归。数量表示实现一致性，不是独立数学证明或端到端有效性。

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

`v110_consumption_caliber/` 包含七个工件。三个回顾性口径并列：

- `ALL_EXISTING_RECORD_MEAN_ZERO_EMPTY`：71,970 已存在键；空选择 selected-proxy 补零；30 无记录键缺失；冲突取尝试均值。
- `ALL_EXPECTED_RECORD_MEAN_ZERO_EMPTY_NO_ROW`：72,000 预期键；30 无记录键按选择失败补零；冲突仍取尝试均值。保守描述敏感性，不是实际消费。
- `METRIC_RESOLVED_ZERO_EMPTY`：71,629/70,732/71,674；冲突按指标拒绝；无记录键缺失。

旧 v1.10 名称只在代码中作为输入兼容别名。原 320 条 run-metric 行在标签归一化后保持不变；新增保守口径使新输出为 400 行。全部家族估计、离散度、符号计数、区间和 17 情景移到 `docs/SUPPLEMENT_RETROSPECTIVE_AUDITS_v1.13.md`，主文不以其支持结构效果。

`future_logging_schema.json` 升级为 `/v4`：`attended` 是操作性终端 attendance 测量，不是潜在真实消费；`outcome_protocol` 记录失败复合主规则（`ALL_ASSIGNED_FAILURE_COMPOSITE_OPERATIONAL_ATTENDANCE_OMISSION_V1`）、明确 AND 判定、仪器注册哈希、敏感性阈值和机器事件术语。测量失败保留 `unknown`。该 schema 只约束未来日志，不填补历史数据。

### 4.3 稿件、布局与 arXiv 包

```bash
PYTHONDONTWRITEBYTECODE=1 python3 tools/audit_v113.py
bash tools/build_review_pdf.sh en v1.13
python3 tools/check_pdf_textlayer.py \
  latex/SEA_EN_v1.13_draft.pdf \
  input/sovereign_epistemic_acquisition_EN_v1.13.md
python3 tools/check_pdf_layout.py \
  latex/SEA_EN_v1.13_draft.pdf \
  --json tools/pdf_layout_v1.13.json
bash tools/make_arxiv_source.sh v1.13
```

发布还需用 `pdftoppm` 渲染并目检首页标题、宽表、图和附录分页。文本层检查和坐标检查都不能单独替代完整视觉审阅。arXiv 附件只包含被 Git 跟踪的公开内容：内部 dispatch 运维日志（被 `.gitignore` 排除、含节点地址）不进入源包，工作树构建与脱敏副本构建均核验同一 729 项 `anc/SHA256SUMS`。`make_public.py` 对导出的 arXiv 源包执行开包敏感模式扫描，发现内部标识时自动从脱敏树重建并复检；旧版 arXiv 源包与解包目录不随公开快照导出。

## 5. 无 `.git` 公开副本检查

金融脚本必须在无 `.git` 且 `PATH` 没有 Git 的环境中完成默认和 `--write --force`。其他核心 Python 审计也只使用快照内冻结输入。注意某些机器的 `/usr/bin` 本身含 `git`，因此 `PATH=/usr/bin:/bin` 不足以证明无 Git；应构造仅含解释器的专用 PATH。金融脚本无任何 subprocess/系统调用，可这样检查：

```bash
mkdir -p /tmp/sea-nogit-bin
ln -sf "$(command -v python3)" /tmp/sea-nogit-bin/python3
env -i HOME="$HOME" PATH=/tmp/sea-nogit-bin \
  PYTHONDONTWRITEBYTECODE=1 \
  /usr/bin/python3 sim/sea_pilot/audit_v19_financial_caliber.py
```

如果 Python/NumPy 安装在其他前缀，应使用对应解释器，而不是恢复 Git 依赖。发布者另在干净公开副本中执行第 4.1–4.3 节命令并比较工件。第三方独立重跑仍不得因此宣称已完成。

本版已在无 `.git` 的脱敏公开副本实际完成 **18/18 组验证命令**：13 项数学/SAP、65 项治理/重放/金融/消费口径/执行器/目标构造测试、四类数据审计、合成 SAP 工件重建、发布审计、20 页 PDF/arXiv 构建，以及专用无 Git PATH（`shutil.which('git')` 为 None）下的金融默认和 `--write --force`。公开 arXiv 的 **729/729** 个附件哈希全部通过。机器报告为 `tools/clean_verification_v1.13.json`。这是**作者执行的公开副本验证**，不是第三方独立复现；不同时刻的 PDF/压缩包可因构建时间产生不同二进制哈希，arXiv 包另因附件基础设施标识脱敏而不同，报告将“干净重建哈希”与金融固定输入哈希分开。

## 6. 工件清单与 arXiv 附件

发布分两步解决“提交不能包含自身哈希”的溯源问题。先提交候选内容并创建 annotated tag，再在标签已存在且可解引用时生成最终清单：

```bash
SEA_RELEASE_STATUS=PUBLIC_CANDIDATE_RELEASE__PRERELEASE \
SEA_RELEASE_ID=v1.13.0 \
SEA_TARGET_TAG=v1.13.0 \
SEA_TARGET_COMMIT=<v1.13.0^{} 的完整 40 位提交哈希> \
SEA_GITHUB_URL=https://github.com/hurrywhen/sea-nuaa \
SEA_GITEE_URL=https://gitee.com/jiangsu-yunhefeng-intelligent_0/sea-nuaa \
PYTHONDONTWRITEBYTECODE=1 python3 tools/make_v113_manifest.py
```

生成器核验 `SEA_TARGET_COMMIT` 与本地 annotated tag 解引用结果一致，并记录 `target_tag`、`target_commit`、`target_tag_object` 和 `target_commit_verified_against_tag`。随后只提交这两个清单文件到 main，标签不移动。

`docs/工件清单_v1.13.{md,json}` 记录核心文件、292 主分片和 5 隔离文件的 SHA-256。清单不是 DOI 或第三方签核。arXiv 候选包位于 `latex/SEA_v1.13_arxiv_source.tar.gz`，其 `anc/SHA256SUMS` 可逐文件核验；处理器选择 XeLaTeX。

## 7. 不可从历史数据重建的内容

历史分片没有 delivered/opened/attended/actual-consumption 字段，也没有完整 calls、input/output tokens、cost、latency、retries。`raw_consume` 是原始输出诊断，`impulse_consumed` 是注入冲动指标，均不能替代目标信息的实际消费。空选择也无法统一区分为合法 abstention 或静默执行失败。任何这些字段的“恢复”都必须是新实验，而不是本次离线重分析。

## 8. 后续直接实验

`docs/MINIMAL_VALID_EXPERIMENT_v1.13.md` 给出建议的识别结构：唯一主要比较为 SEA 对同模型端到端筛选，唯一主要结局为全分配失败复合操作性 attendance 加权遗漏 \(\mathcal M_\nu^{FC}\)，与潜在 \(\mathcal M_\nu\) 分离。协议按域注册 attendance 工具、明确 AND 判定、阈值验证和盲法，报告臂别 unknown 极端边界（操作性 attendance 遗漏差值，不是潜在消费差值），unknown 在主分析中进入失败复合结局。目标集版本变更创建新评价队列（`NEW_EVALUATION_COHORT__NO_CROSS_VERSION_POOLING`），控制实例可保留目标、授权、回滚、审计和资源状态；完全重置只是可选协议选择。还需要独立语料/月份功效模拟、锁定语料、严格 point-in-time、记忆审计、效率日志和结果解锁前公共注册。该协议目前未执行，也不等于已经公共注册。
