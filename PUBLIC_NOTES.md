# 公开版说明（PUBLIC_NOTES）

本仓库是 SEA（Sovereign Epistemic Acquisition）项目的脱敏公开快照。当前主线为
**v1.10：Conditional Components, Governance Audits, and Weighted Omission**。历史 v1.7、v1.9
及会议/期刊衍生版保留供对照，不代表当前理论或证据口径。

## 当前发布与证据状态

- 英文主稿：`input/sovereign_epistemic_acquisition_EN_v1.10.md`；PDF：
  `latex/SEA_EN_v1.10_draft.pdf`；arXiv 候选源包：`latex/SEA_v1.10_arxiv_source.tar.gz`。
- v1.10.0 是**候选公开快照 / prerelease**，不是独立核验后的投稿定稿或联合最优算法。
  独立人类数学复审、S2d/S4/S5、时间外/私域语料、point-in-time／记忆审计、实际消费新实验、
  人类数据、第三方复现和公共实验注册均未完成。
- 历史 `picked` 只表示 selected proxy，不能证明 delivered/opened/attended/actual consumption。
  空选择补零是历史敏感性，不是实际消费 ITT；不支持部署召回、端到端优势或人类福利外推。
- 公开仓库：https://github.com/hurrywhen/sea-nuaa 与
  https://gitee.com/jiangsu-yunhefeng-intelligent_0/sea-nuaa 。
- v1.7 的版本 DOI 10.5281/zenodo.23620920 与概念 DOI 10.5281/zenodo.23620919
  **不包含 v1.9 或 v1.10**；v1.10 专属 DOI 未登记。

## 脱敏范围

内网地址、推理节点、本机路径和内部备份信息脱敏；Python 示例端点通过环境变量配置。
投稿策略、个人交接、内部网页操作、内部 QC/翻译日志与旧审稿 PDF 不公开。作者署名、论文联系
邮箱和已公开模型名称保留。公开版不包含内部 git 历史或凭据。构建器执行内网地址、私钥、
Bearer token 和常见密钥模式扫描，未通过时不得发布。

## v1.10 复现入口

完整命令见 `docs/REPRODUCIBILITY_v1.10.md`。核心入口：

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v   tools/test_v19_math.py tools/test_v110_sap.py
PYTHONDONTWRITEBYTECODE=1 python3 tools/reproduce_v110_sap.py --write --force
PYTHONDONTWRITEBYTECODE=1 python3   sim/sea_pilot/audit_v110_consumption_caliber.py --write --force
PYTHONDONTWRITEBYTECODE=1 python3   sim/sea_pilot/audit_v19_financial_caliber.py --write --force
PYTHONDONTWRITEBYTECODE=1 python3 tools/audit_v110.py
bash tools/build_review_pdf.sh en v1.10
python3 tools/check_pdf_layout.py latex/SEA_EN_v1.10_draft.pdf
bash tools/make_arxiv_source.sh v1.10
```

当前检查包括 9 项旧数学、4 项 SAP、14 项治理、20 项重放和 3 项金融回归，100 项稿件/工件
一致性检查，42 页 PDF 文本层与页面坐标检查，XeLaTeX 缺字形 0。金融历史 CSV 固定在公开
快照内，默认复现不读取 Git 历史。292 个主分片和 5 个隔离文件保留，arXiv `anc/SHA256SUMS`
可逐文件核验。所有核心 Python 审计不调用 LLM，也不创建人类数据。

## 主要工件

- `sim/sea_governance/` 与 `sim/pilot/results/governance_conformance_v1.10.json`：S1–S4；
- `sim/theory_v1.10/`：六目标消费链与 17/22 不组合反例；
- `sim/pilot/results/v110_consumption_caliber/`：71,970 已存在键、Rule A/C、17 情景和未来日志；
- `sim/pilot/results/v19_financial_caliber_audit/`：公开冻结历史输入与扩展 S2p 重建；
- `sim/pilot/results/evidence_status_v1.10.json`：证据状态与不可外推边界；
- `docs/工件清单_v1.10.{md,json}`：候选快照逐文件 SHA-256，非 DOI 或第三方签核。

代码与工具采用 MIT（`LICENSE`）；论文文本、表格、派生数据与冻结实验记录采用 CC BY 4.0
（`LICENSE-CONTENT`）。公开复现不等于独立数学复审、时间外验证或人类有效性证据。
