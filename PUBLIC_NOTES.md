# 公开版说明（PUBLIC_NOTES）

本仓库是《主权认知获取：有限智能体主动信息获取与主权过滤的统一数学框架》（SEA，
*Sovereign Epistemic Acquisition*）项目的**脱敏公开版**（专著 v1.7 + 会议/期刊拆分版 v1.0
对应快照），由内部工作仓库经自动构建器生成（构建器为内部工具，脱敏规则摘要如下）。

## 脱敏范围

- 内网地址（推理节点/开发机 IP）→ `<内网地址已脱敏>`（Python 代码内 → `127.0.0.1`，
  推理端点一律支持环境变量覆盖：`SEA_LLM_BASE_URL`/`SEA_LLM_MODEL`/`SEA_EMB_URL` 等）；
- 本机文件系统路径 → `~/sea`、`~/models/`；
- 内部代码托管与备份体系信息 → 移除/脱敏；
- 投稿信与网页元数据（含场馆策略、CRediT/ORCID 等待确认项）、含内部 QC/翻译日志原文的
  v1.3 版补充材料 S2、已被取代的历轮审稿 PDF（v1.0–v1.6）不随公开版发布；
- **不脱敏**：模型名（`ornith-1.5-35b` 已由作者团队公开论文 arXiv:2609.14883 披露）、
  作者署名与联系邮箱（有意公开）、计算节点标签（node-a 等，无地址映射）。

## 与内部版的差异

研究内容、实验数据与结果**完全一致**；仅上述基础设施标识符与文件范围不同。内部 git
历史不随公开版发布（历史提交信息含内网运维细节），公开版为单提交快照。

## 许可内容

代码与工具：MIT（`LICENSE`）；论文文本、表格、派生数据与冻结实验记录：CC BY 4.0
（`LICENSE-CONTENT`）。与作者已发表论文 arXiv:2609.14883 的 CC BY 4.0 一致。
本仓库快照（tag `v1.7.0`）已归档于 Zenodo：DOI 10.5281/zenodo.23620920（概念 DOI
10.5281/zenodo.23620919）。后续会议/期刊拆分版的公开 main 快照不改变该已归档 tag 的指向。

## 会议与期刊拆分版（v1.0）

- 会议英文版：通用双栏 **6 页（含参考文献）**，四家族判断层机制重放与两域适用边界；
  源稿 `input/SEA_conference_EN_v1.0.md`，PDF/LaTeX `latex/SEA_conference_v1.0.{pdf,tex}`。
- 期刊英文版：通用单栏 **30 页**，SAP 与核心定理/证明为主、精选验证为辅；
  源稿 `input/SEA_journal_EN_v1.0.md`，PDF/LaTeX `latex/SEA_journal_v1.0.{pdf,tex}`。
- 两版均有中文同步稿；通用版式不代表已选定会/刊。具体官方模板、匿名化和相关投稿政策
  需在投出前适配。版本分工见 `docs/会议与期刊版本说明_v1.0.md`。
- 构建：`bash tools/build_venue_pdfs.sh en`（或 `zh`）；审计：`python3 tools/audit_venue_papers.py`。

## 快速复现（<2 分钟，零 LLM 调用，完全离线）

```bash
python3 tools/audit_paper.py       # 论文一致性审计（编号/文献/数字对账/公式级核查；仓库根目录）
cd sim
python3 -m sea_algo.validate       # 阶段二算法参考实现九项验证（P2 金融域）
python3 -m sea_algo.validate_p3    # P3 学术域移植验证八项
```

公开版随附**紧凑派生副本**（`sim/pilot/data/corpus_lite.json` 与 `p2_env_lite.json`，
共 ~1.7MB）：无 raw/ 原始缓存时环境构建器自动回退到副本，**验证数值与内部全量版
逐位一致**（P2：认证 lift 0.61→1.23×、T7 11:10；P3：贪心 25 vs 随机 15、T7 12:16；
一致性自检：`SEA_FORCE_LITE=1` 可在有 raw 的机器上强制副本路径对比）。
唯一例外：P2 验证的 T1（命题图恒等式，需原始 EDGAR 文档流重建）在公开版如实标记为
跳过，其全量验证结果（1876 命题、ρ_c=8.1919 逐位一致）记录于内部版报告；
其余测试全部照常执行。

## 实验记录与数据

- **四家族 LLM 智能体判断层机制重放**（80 run、73,547 有效 agent-日）的冻结分析记录：
  `sim/pilot/results/main_validation_analysis.json` 与 `MAIN_VALIDATION_ANALYSIS.md`
  （跨家族 CMH χ²₁=981.52、p=1.867e-215；逐家族 McNemar/效应量/bootstrap CI）；
  H8/H9 转移桥逐家族记录见 `sim/pilot/results/h8v2_*.json`、`h9_*.json` 与对应报告。
- **HP-0 人类可行性试点工具包**（已设计、零人类数据）：`docs/human_pilot_v1.5/`
  （方案、双语知情同意、参与材料、数据模板、分析管线与 SYNTHETIC 干跑）。
- 派生数据集（arXiv 语料 CSV、EDGAR 命题层副本、CDX 新闻层 JSONL、pageviews、
  Manifold 人类锚）已随仓库提供；`raw/` 原始缓存可由 `sim/sea_pilot/fetch_*.py`
  从公开源重建（arXiv/OpenAlex/EDGAR/archive.org/Wikimedia/Manifold）。
- 论文一致性审计（v1.6 核查 58 项 + v1.7 公式级核查 22 项，中英双稿）与 PDF 文本层
  完整性检查工具随仓库提供（`tools/audit_paper.py`、`tools/check_pdf_textlayer.py`）。

完整实验脚本（`run_p2`、`run_llm_replay` 等）需 raw 缓存与推理端点，属内部全量流程；
公开版的承诺范围是上述验证套件、冻结记录与审计工具的离线复现。

## 每日部署管线（阶段五）

`sim/sea_deploy/daily_run.py` 中的推理端点示例配置指向已脱敏占位符——公开使用者请
填入自己的 Ollama/LM Studio 端点（personas/researcher.example.json 的 `llm` 段）。
