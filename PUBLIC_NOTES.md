# 公开版说明（PUBLIC_NOTES）

本仓库是 SEA（Sovereign Epistemic Acquisition）项目的脱敏公开快照。当前主线为
**v1.9：Conditional Design for Pull, Push, and Weighted Recall**。历史 v1.7、会议/期刊
衍生版保留供对照，不代表当前理论或证据口径。

## 当前发布与证据状态

- 英文主稿：`input/sovereign_epistemic_acquisition_EN_v1.9.md`；PDF：
  `latex/SEA_EN_v1.9_draft.pdf`；arXiv 候选源包：`latex/SEA_v1.9_arxiv_source.tar.gz`。
- v1.9.0 是**候选公开快照 / prerelease**，不是独立核验后的投稿定稿。独立人类数学复审、
  S2d/S4/S5 和完整消融、时间外或私域语料、严格 point-in-time 与记忆审计、人类数据均未完成。
- 当前实证只支持 semi-oracle、事后、共享语料的判断层机制检查；不支持 95% 部署召回、
  SEA 整体优于端到端 LLM/RAG/福利推荐，或任何人类福利外推。
- 公开仓库：
  - GitHub: https://github.com/hurrywhen/sea-nuaa
  - Gitee: https://gitee.com/jiangsu-yunhefeng-intelligent_0/sea-nuaa
- v1.7 的历史不可变归档：版本 DOI 10.5281/zenodo.23620920，概念 DOI
  10.5281/zenodo.23620919。该 DOI **不包含 v1.9**；新的 v1.9 DOI 未回填前不得混用。

## 脱敏范围

- 内网地址与推理节点标识脱敏；Python 示例端点改为 `127.0.0.1`，实际端点通过
  `SEA_LLM_BASE_URL`、`SEA_LLM_MODEL`、`SEA_EMB_URL` 等环境变量配置。
- 本机路径改为 `~/sea`、`~/models/`；内部代码托管和备份说明移除。
- 投稿策略、个人交接、内部网页操作、内部 QC/翻译日志与旧审稿 PDF 不公开。
- 作者署名、论文联系邮箱和论文已公开的模型名称保留。公开版不包含内部 git 历史或凭据。

研究内容、冻结数据与结果与内部当前快照一致；仅文件范围和基础设施标识不同。构建器还执行
内网地址、私钥、Bearer token 和常见密钥模式扫描，未通过时不得发布。

## v1.9 复现入口

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tools/test_v19_math.py
PYTHONDONTWRITEBYTECODE=1 python3 tools/audit_v19.py
PYTHONDONTWRITEBYTECODE=1 python3 tools/reproduce_v19_math.py --write --force
PYTHONDONTWRITEBYTECODE=1 python3 sim/sea_pilot/audit_v19_financial_caliber.py --write --force
PYTHONDONTWRITEBYTECODE=1 python3 sim/sea_pilot/audit_v19_upstream_digest.py --write --force
PYTHONDONTWRITEBYTECODE=1 python3 sim/sea_pilot/audit_v19_recall_value_tradeoff.py --write --force
bash tools/build_review_pdf.sh en v1.9
bash tools/make_arxiv_source.sh v1.9
```

当前检查：9 项数学单元测试、100/100 项一致性检查、32 页 PDF 文本层无断裂、
XeLaTeX 缺字形 0。候选包包含 292 个主重放分片及 5 个隔离的非主 tag 文件；
`anc/SHA256SUMS` 可逐文件核验。上述命令不调用 LLM，也不创建人类数据。金融旧配置读取
内部 git 历史提交 `8ffc7f5`；公开快照的复现说明同时给出冻结结果和输入哈希。

## 主要审计工件

- `sim/theory_v1.9/`：总体/有限 top-m、Pareto、统一更新和 RCT 数值；
- `sim/pilot/results/v19_financial_caliber_audit/`：命题/公司—日、feature scorer、配额与时间戳；
- `sim/pilot/results/v19_upstream_digest_audit/`：80 个模型—种子配置对应 70 个不同 digest；
- `sim/pilot/results/v19_recall_value_tradeoff/`：严格单例的引用代理收益分解；
- `sim/pilot/results/frozen_reanalysis_v1/`：既有 17 场景唯一键重分析；
- `sim/pilot/results/evidence_status_v1.9.json`：统一的估计量、证据状态与不可外推边界；
- `docs/工件清单_v1.9.{md,json}`：候选工作树逐文件 SHA-256，非 DOI 或第三方签核。

代码与工具采用 MIT（`LICENSE`）；论文文本、表格、派生数据与冻结实验记录采用 CC BY 4.0
（`LICENSE-CONTENT`）。公开复现不等于独立数学复审、时间外验证或人类有效性证据。
