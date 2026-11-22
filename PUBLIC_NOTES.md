# 公开版说明（PUBLIC_NOTES）

本仓库是 SEA（Sovereign Epistemic Acquisition）项目的脱敏公开快照。当前主线为
**v1.16：A Conditional Framework and Synthetic Audit Artifacts**。历史版本均已标为已被取代，
索引见 `archive/README.md`。

## 当前发布与证据状态

- 英文主稿：`input/sovereign_epistemic_acquisition_EN_v1.16.md`；PDF：
  `latex/SEA_EN_v1.16_draft.pdf`；arXiv 候选源包：`latex/SEA_v1.16_arxiv_source.tar.gz`。
- v1.16.0 是 v1.15.0 综合评审后的**小修候选 / prerelease**：在已确立的**外生冻结评价协议事件**
  与**单线控制生命周期**基础上，完成三项精确修订——拒绝切换时登记/目标/预算/活动路径不变、
  **仅追加一条拒绝审计记录**（不再笼统称"零状态变更"）；新增**冻结切换期次** `switch_after_period`
  （读取任何处理臂结果前冻结，过早/过晚/篡改声明均拒绝）；**完全重置是声明例外**，只能选事前
  白名单 `protocol_reset_targets` 目标（含回退版本）并生成独立单版本日程。复现命令修正为
  `make_v116_manifest.py`。S12 新增协方差 delta-method、联合/聚类 bootstrap、分层可迁移性与
  完成子集代表性诊断、预注册敏感性网格。
- 四种状态分开：代码测试通过、历史数据可重算、理论经独立复核、系统效果已验证。当前仅完成
  作者侧代码测试和历史数据重算；独立数学复审、第三方复现、真实匹配实验和人类数据未完成。
- 执行器语义：`first_available_period` 纵向可用性（含到期恢复正向测试）；SEA staged linkage
  与臂无关 `reference_link_truth` 分离；整期资源预检＋无提交选择预演；协议登记转移与评价队列分离；
  每个队列相关审计事件携带控制实例/队列/登记版本/登记哈希归因；仪器注册对象显式为
  `synthetic_instrument_fixture`，`validated` 状态强制完整预注册字段（真 64 位十六进制哈希、
  敏感度/特异度区间、可迁移性假设声明、独立盲法参考集构造/解锁记录、完成子集代表性说明）；
  机器事件为合成占位谓词。
- 历史 `picked` 只表示 selected proxy。三个回顾性口径并列；家族估计、区间和名义检验移至补充材料；
  Rule A/strict-singleton/17 情景表只在回顾性补充材料 §R5 一处，由
  `tools/make_retrospective_tables.py` 从冻结数据再生成并核对漂移。
- 未来实验区分潜在真实消费、操作性 attendance 和失败复合结局；数字文本 attendance 为明确 AND；
  协议 §1.4.1 规定解锁前误分类验证、验证集→部署集误差可迁移性条件与完成子集代表性的分层诊断、
  相关输入下的协方差/联合 bootstrap、臂间误差比较与 (S12) 近零分母精度预警/敏感性网格（未执行）。
  协议尚未执行，也不是公共注册。
- 公开仓库：https://github.com/hurrywhen/sea-nuaa 与
  https://gitee.com/jiangsu-yunhefeng-intelligent_0/sea-nuaa 。
- v1.7 DOI **不包含 v1.9–v1.16**；v1.16 专属 DOI 未登记。

## 脱敏范围

内网地址、推理节点、本机路径和内部备份信息脱敏；Python 示例端点通过环境变量配置。
投稿策略、个人交接、内部网页操作、内部 QC/翻译日志不公开。作者署名、论文联系邮箱和已公开
模型名称保留。公开版不包含内部 git 历史或凭据。构建器执行敏感模式扫描（含 arXiv 源包开包检查），
未通过时不得发布。旧审稿 PDF 与旧 arXiv 源包不随当前 main 导出；当前 arXiv 源包若含内部标识，
构建器自动从脱敏树重建并复检。

## v1.16 复现入口

完整命令见 `docs/REPRODUCIBILITY_v1.16.md`。核心入口：

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v \
  tools/test_v19_math.py tools/test_v110_sap.py
PYTHONDONTWRITEBYTECODE=1 python3 tools/reproduce_v110_sap.py --write --force
PYTHONDONTWRITEBYTECODE=1 python3 sim/sea_sap/reproduce.py --write --force
PYTHONDONTWRITEBYTECODE=1 python3 \
  sim/sea_pilot/audit_v110_consumption_caliber.py --write --force
PYTHONDONTWRITEBYTECODE=1 python3 \
  sim/sea_pilot/audit_v19_financial_caliber.py --write --force
PYTHONDONTWRITEBYTECODE=1 python3 tools/make_retrospective_tables.py
PYTHONDONTWRITEBYTECODE=1 python3 tools/audit_v116.py
bash tools/build_review_pdf.sh en v1.16
python3 tools/check_pdf_layout.py latex/SEA_EN_v1.16_draft.pdf
bash tools/make_arxiv_source.sh v1.16
```

精确最终计数见 `tools/audit_v116_report.json` 与 `tools/clean_verification_v1.16.json`。
金融历史 CSV 固定在公开快照内，默认复现不读取 Git。292 个主分片和 5 个隔离文件保留，
arXiv `anc/SHA256SUMS` 可逐文件核验。所有核心 Python 审计不调用 LLM，也不创建人类数据。
作者执行的公开副本验证不等于第三方独立复现。

## 主要工件

- `sim/sea_governance/` 与 `sim/pilot/results/governance_conformance_v1.16.json`：S1–S4；
- `sim/sea_sap/` 与 `sim/pilot/results/sap_v1.16/`：纵向执行器、协议登记转移演示、匹配实现 fixture、目标构造审计；
- `sim/theory_v1.10/`：六目标消费链与 17/22 不组合反例；
- `sim/pilot/results/v110_consumption_caliber/`：三个回顾性口径、72,000 键、17 情景和未来日志；
- `sim/pilot/results/v19_financial_caliber_audit/`：公开冻结历史输入与扩展 S2p 重建；
- `sim/pilot/results/retrospective_tables_v1.16/`：R5 单一来源生成工件；
- `sim/pilot/results/evidence_status_v1.16.json`：证据状态与不可外推边界；
- `docs/SUPPLEMENT_FORMAL_AND_SECONDARY_v1.16.md` 与
  `docs/SUPPLEMENT_RETROSPECTIVE_AUDITS_v1.16.md`：移出的证明、数值恒等和全部回顾性估计；
- `docs/工件清单_v1.16.{md,json}`：main 上的目标标签／提交清单，非 DOI 或第三方签核。

最终清单在 annotated tag 创建后生成，核验 `target_commit` 与标签解引用结果，再以单独
provenance 提交加入 main；标签不移动。代码与工具采用 MIT（`LICENSE`）；论文文本、表格、
派生数据与冻结实验记录采用 CC BY 4.0（`LICENSE-CONTENT`）。
