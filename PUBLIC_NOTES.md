# 公开版说明（PUBLIC_NOTES）

本仓库是 SEA（Sovereign Epistemic Acquisition）项目的脱敏公开快照。当前主线为
**v1.12：Conditional Components, Governance Audits, and Weighted Omission**。历史 v1.7、v1.9、
v1.10、v1.11 及会议/期刊衍生版保留供对照，均已标为已被取代，不代表当前理论或证据口径。
历史版本索引见 `archive/README.md`。

## 当前发布与证据状态

- 英文主稿：`input/sovereign_epistemic_acquisition_EN_v1.12.md`；PDF：
  `latex/SEA_EN_v1.12_draft.pdf`；arXiv 候选源包：`latex/SEA_v1.12_arxiv_source.tar.gz`。
- v1.12.0 是 v1.11 综合评审后的**大修候选 / prerelease**，贡献收束为条件化框架＋治理/执行器
  参考工件＋可 falsify 审计规范。不是独立核验后的投稿定稿、联合最优算法或已验证系统。
- 四种状态分开：代码测试通过、历史数据可重算、理论经独立复核、系统效果已验证。当前仅完成
  作者侧代码测试和历史数据重算；独立数学复审、第三方复现、真实匹配实验和人类数据未完成。
- 新增 `sim/sea_sap/` 最小纵向执行器和目标构造审计；治理参考修复 actor–principal、时间戳、
  授权重用和哈希规范。合成执行器不是部署有效性证据。
- 历史 `picked` 只表示 selected proxy。三个回顾性口径并列：
  `ALL_EXISTING_RECORD_MEAN_ZERO_EMPTY`、`ALL_EXPECTED_RECORD_MEAN_ZERO_EMPTY_NO_ROW`、
  `METRIC_RESOLVED_ZERO_EMPTY`。家族估计、区间和名义检验移至补充材料，不用于主文效果主张。
- 未来实验区分潜在真实消费、操作性 attendance 和失败复合结局；数字文本 attendance 为明确 AND，
  机器事件称 `machine_ingestion_and_task_reference`。协议尚未执行，也不是公共注册。
- 公开仓库：https://github.com/hurrywhen/sea-nuaa 与
  https://gitee.com/jiangsu-yunhefeng-intelligent_0/sea-nuaa 。
- v1.7 的版本 DOI 10.5281/zenodo.23620920 与概念 DOI 10.5281/zenodo.23620919
  **不包含 v1.9、v1.10、v1.11 或 v1.12**；v1.12 专属 DOI 未登记。

## 脱敏范围

内网地址、推理节点、本机路径和内部备份信息脱敏；Python 示例端点通过环境变量配置。
投稿策略、个人交接、内部网页操作、内部 QC/翻译日志不公开。作者署名、论文联系邮箱和已公开
模型名称保留。公开版不包含内部 git 历史或凭据。构建器执行内网地址、私钥、Bearer token 和
常见密钥模式扫描，未通过时不得发布。旧审稿 PDF 不随当前 main 导出，避免误引旧主张。

## v1.12 复现入口

完整命令见 `docs/REPRODUCIBILITY_v1.12.md`。核心入口：

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v \
  tools/test_v19_math.py tools/test_v110_sap.py
PYTHONDONTWRITEBYTECODE=1 python3 tools/reproduce_v110_sap.py --write --force
PYTHONDONTWRITEBYTECODE=1 python3 sim/sea_sap/reproduce.py --write --force
PYTHONDONTWRITEBYTECODE=1 python3 \
  sim/sea_pilot/audit_v110_consumption_caliber.py --write --force
PYTHONDONTWRITEBYTECODE=1 python3 \
  sim/sea_pilot/audit_v19_financial_caliber.py --write --force
PYTHONDONTWRITEBYTECODE=1 python3 tools/audit_v112.py
bash tools/build_review_pdf.sh en v1.12
python3 tools/check_pdf_layout.py latex/SEA_EN_v1.12_draft.pdf
bash tools/make_arxiv_source.sh v1.12
```

精确最终计数见 `tools/audit_v112_report.json` 与 `tools/clean_verification_v1.12.json`。
金融历史 CSV 固定在公开快照内，默认复现不读取 Git。292 个主分片和 5 个隔离文件保留，
arXiv `anc/SHA256SUMS` 可逐文件核验。所有核心 Python 审计不调用 LLM，也不创建人类数据。
作者执行的公开副本验证不等于第三方独立复现。

## 主要工件

- `sim/sea_governance/` 与 `sim/pilot/results/governance_conformance_v1.12.json`：S1–S4；
- `sim/sea_sap/` 与 `sim/pilot/results/sap_v1.12/`：纵向执行器、匹配实现 fixture、目标构造审计；
- `sim/theory_v1.10/`：六目标消费链与 17/22 不组合反例；
- `sim/pilot/results/v110_consumption_caliber/`：三个回顾性口径、72,000 键、17 情景和未来日志；
- `sim/pilot/results/v19_financial_caliber_audit/`：公开冻结历史输入与扩展 S2p 重建；
- `sim/pilot/results/evidence_status_v1.12.json`：证据状态与不可外推边界；
- `docs/SUPPLEMENT_FORMAL_AND_SECONDARY_v1.12.md` 与
  `docs/SUPPLEMENT_RETROSPECTIVE_AUDITS_v1.12.md`：移出的证明、数值表和历史估计；
- `docs/工件清单_v1.12.{md,json}`：main 上的目标标签／提交清单，非 DOI 或第三方签核。

最终清单在 annotated tag 创建后生成，核验 `target_commit` 与标签解引用结果，再以单独
provenance 提交加入 main；标签不移动。代码与工具采用 MIT（`LICENSE`）；论文文本、表格、
派生数据与冻结实验记录采用 CC BY 4.0（`LICENSE-CONTENT`）。
