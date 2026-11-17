# 公开版说明（PUBLIC_NOTES）

本仓库是 SEA（Sovereign Epistemic Acquisition）项目的脱敏公开快照。当前主线为
**v1.11：Conditional Components, Governance Audits, and Weighted Omission**。历史 v1.7、v1.9、
v1.10 及会议/期刊衍生版保留供对照，不代表当前理论或证据口径。

## 当前发布与证据状态

- 英文主稿：`input/sovereign_epistemic_acquisition_EN_v1.11.md`；PDF：
  `latex/SEA_EN_v1.11_draft.pdf`；arXiv 候选源包：`latex/SEA_v1.11_arxiv_source.tar.gz`。
- v1.11.0 是 v1.10 复审意见后的**小修候选 / prerelease**，不是独立核验后的投稿定稿或联合最优算法。
  独立人类数学复审、S2d/S4/S5、时间外/私域语料、point-in-time／记忆审计、实际消费新实验、
  人类数据、第三方复现和公共实验注册均未完成。
- 历史 `picked` 只表示 selected proxy。新口径为 `ALL_EXISTING_RECORD_MEAN_ZERO_EMPTY` 和
  `METRIC_RESOLVED_ZERO_EMPTY`，均为回顾性描述，不是全分配或实际消费分析；旧名称仅为代码输入别名。
- 未来实验按域注册 attendance 工具、阈值验证和盲法，唯一主要结局使用全分配失败复合规则；
  测量失败保留 `unknown`，替代缺失模型仅作敏感性。该协议尚未执行，也不是公共注册。
- 公开仓库：https://github.com/hurrywhen/sea-nuaa 与
  https://gitee.com/jiangsu-yunhefeng-intelligent_0/sea-nuaa 。
- v1.7 的版本 DOI 10.5281/zenodo.23620920 与概念 DOI 10.5281/zenodo.23620919
  **不包含 v1.9、v1.10 或 v1.11**；v1.11 专属 DOI 未登记。

## 脱敏范围

内网地址、推理节点、本机路径和内部备份信息脱敏；Python 示例端点通过环境变量配置。
投稿策略、个人交接、内部网页操作、内部 QC/翻译日志与旧审稿 PDF 不公开。作者署名、论文联系
邮箱和已公开模型名称保留。公开版不包含内部 git 历史或凭据。构建器执行内网地址、私钥、
Bearer token 和常见密钥模式扫描，未通过时不得发布。

## v1.11 复现入口

完整命令见 `docs/REPRODUCIBILITY_v1.11.md`。核心入口：

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v \
  tools/test_v19_math.py tools/test_v110_sap.py
PYTHONDONTWRITEBYTECODE=1 python3 tools/reproduce_v110_sap.py --write --force
PYTHONDONTWRITEBYTECODE=1 python3 \
  sim/sea_pilot/audit_v110_consumption_caliber.py --write --force
PYTHONDONTWRITEBYTECODE=1 python3 \
  sim/sea_pilot/audit_v19_financial_caliber.py --write --force
PYTHONDONTWRITEBYTECODE=1 python3 tools/audit_v111.py
bash tools/build_review_pdf.sh en v1.11
python3 tools/check_pdf_layout.py latex/SEA_EN_v1.11_draft.pdf
bash tools/make_arxiv_source.sh v1.11
```

当前检查包括 13 项数学/SAP、42 项治理/重放/金融/消费口径回归，以及稿件、PDF、arXiv 和
干净公开副本检查；精确最终计数见 `tools/audit_v111_report.json` 与
`tools/clean_verification_v1.11.json`。金融历史 CSV 固定在公开快照内，默认复现不读取 Git。
292 个主分片和 5 个隔离文件保留，arXiv `anc/SHA256SUMS` 可逐文件核验。所有核心 Python
审计不调用 LLM，也不创建人类数据。作者执行的公开副本验证不等于第三方独立复现。

## 主要工件

- `sim/sea_governance/` 与 `sim/pilot/results/governance_conformance_v1.10.json`：S1–S4；
- `sim/theory_v1.10/`：六目标消费链与 17/22 不组合反例；
- `sim/pilot/results/v110_consumption_caliber/`：新回顾性口径、71,970 已存在键、17 情景和未来日志；
- `sim/pilot/results/v19_financial_caliber_audit/`：公开冻结历史输入与扩展 S2p 重建；
- `sim/pilot/results/evidence_status_v1.11.json`：证据状态与不可外推边界；
- `docs/SUPPLEMENT_FORMAL_AND_SECONDARY_v1.11.md`：移出的证明与次要历史表；
- `docs/工件清单_v1.11.{md,json}`：main 上的目标标签／提交清单，非 DOI 或第三方签核。

最终清单在 annotated tag 创建后生成，核验 `target_commit` 与标签解引用结果，再以单独
provenance 提交加入 main；标签不移动。代码与工具采用 MIT（`LICENSE`）；论文文本、表格、
派生数据与冻结实验记录采用 CC BY 4.0（`LICENSE-CONTENT`）。
