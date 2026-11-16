# 补充材料 S2：一致性审计——方法、判定规则与实验记录索引（v1.5）

**Consistency Audit: Methodology, Decision Rules, and Experiment-Record Index — Supplementary Material S2 (v1.5)**

说明：按第三轮审稿意见（意见 1 之 P0-5："删除或移出内部 QC/翻译日志；补充材料只保留审计脚本、决策规则和实验记录"），本补充材料自 v1.5 起**不再包含** v1.3 生产周期的 33 条内部 QC/翻译日志原文；该日志保留在项目仓库（`docs/补充材料S2_一致性审计报告_v1.3.md`，仅存档用途）供溯源，不进入投稿包。本文件承载审稿人认可应随稿的三类内容：**审计方法论**、**预注册判定规则**、**实验记录索引**，并附版本演进对账台账（口径裁决的权威记录）。

## 一、审计方法论

一致性审计由 `tools/audit_paper.py`（投稿版随代码发布）对中英双稿机械执行，检查六类对象：

1. **编号交叉引用闭合**：公理/定理/命题/定义/引理/推论/性质/假设的定义集 vs 正文引用集；历史编号引用（指向 v0.1 纲领稿）白名单豁免；
2. **参考文献闭合**：编号连续性（1–136）、正文（姓, 年）引用对与文献表的双向闭合、机构作者条目按缩写闭合、姓氏匹配 Unicode 感知（Matějka / Maćkowiak）；
3. **关键数字对账**：正文数字 vs 冻结结果工件（`sim/pilot/results/*.json`）逐项比对，含 H9 四家族 Brier（`h9_{o,c,q,g}90_h9.json`）、CMH p 值、Ω、ρ_c、P3 贪心对照；
4. **表格完整性**：Markdown 管道表逐行列数 vs 表头列数；
5. **目录—章节一致**：手写目录条目与 `##` 章节标题匹配；
6. **措辞风险扫描**：『进行中/待/排队』类表述逐行列出供人工复核（非错误，是状态披露）。

v1.5 新增第七类检查（**修订核查**）：横向页块已除且宽表并列、弃用措辞（main-validation / 主验证重放 / （主验证））清零、H9 口径注（0.2848）在稿、ref 56/74/130 更正落地、姓氏拼写统一、样本量公式无叠分、P4 域限定注在稿、HP-0 入稿。本轮审计结果：硬性问题 0，v1.5 核查 20/20 满足（`tools/audit_report.json`）。

v1.5 另新增 `tools/check_pdf_textlayer.py`：**最终 PDF 文本层完整性检查**（三审意见③的落实）。对构建产物执行：表格损坏伪影模式扫描（同行 '1 1 1' 类）、全部表格标题可见性、关键字符串可见性（样本量公式、家族代号行、H9 冻结值、ref 130 文章号）、源稿全部 `##` 标题在文本层的完整性（去空白子串匹配，捕捉标题断裂与词序错位）、文本层/源稿字符量比区间。中英两版 PDF 均 0 问题通过。

## 二、预注册判定规则（决策规则摘要）

- **三态标注**：[completed]（数据与分析冻结）/ [in progress]（部分数据、未达预注册样本量）/ [design]（方案存档未启动）；任何 [completed] 标签不延伸至未完成的电池（表 14-1 状态注）。
- **扩样规则**：样本扩充只能由事前功效分析触发，禁止事后 p 值筛查（实例：Q 家族 480 agent-day 复样，首跑 p=0.057 → 扩样 → p=0.017）。
- **多重比较**：预注册分层检验序列（先主效应后交互），族内 Benjamini–Hochberg；效应量与 bootstrap CI（10⁴ 重抽样，种子固定）与 p 值同时报告，裸 p 值不单独出现。
- **负结果处置**：先行报告、不做事后合理化；学术域 H4' 强形式被拒、公共层认证反转、H8-B 跨家族方向不一致、裁撤家族 F 均按预注册处置入档。
- **冻结规则**：协议 v2.1 冻结模型实例、提示词、解码参数与种子；跨版本的数字变动必须在表 14-3 台账留痕（见下）。
- **模型分离**：主体 ≠ 评分器 ≠ 生产者/红队 ≠ 评审/归并，≥3 家族；评审侧人工抽检 10%。
- **HP-0 人类试点判定规则**（v1.5 新增，[designed; data collection pending]）：E1 成功判据 ≥8/10 参与者 ≤15 分钟、≤2 次澄清提示完成最小声明；E2 被试内 Brier 差报告百分位 bootstrap 95% CI（不做推断）；E3 旗标规则（曝光周平均极端度位移 > +0.5·s_pool，或防御性差 > +1.0 且 ≥3 人为正）只触发再设计；BH 族封闭于 3 个探索性 p 值。完整规则见 `docs/human_pilot_v1.5/HP0_protocol_v1.0.md`。

## 三、实验记录索引

| 记录 | 位置 | 状态 |
|:---|:---|:---|
| 学术域试点 A（630 run） | sim/pilot/（P2_REPORT.md 等） | [completed] |
| 金融域试点 B（双真值） | sim/pilot/results/P2_REPORT.md | [completed] |
| 三家族判断层重放 | sim/pilot/results/three_family_analysis.json | [completed] |
| 四家族判断层机制重放（80 run, 73,547 agent-day） | sim/sea_pilot/（协议 v2.1） | [completed] |
| H8 电池 v1/v2、H9 四家族锚 | sim/pilot/results/h9_*_h9.json 等 | [completed] |
| P10 相变 33 格点、Ω 验证、认证反转 | sim/pilot/results/p5_omega_results.json、algo_validation*.json | [completed] |
| 群体级 P1–P12 全表 | sim/（调度规约见 docs/主验证调度规约.md） | [in progress] |
| S2d / S4 / S5 基线 | docs/AI智能体实验设计.md | [design] |
| HP-0 人类可行性试点 | docs/human_pilot_v1.5/ | [designed; data collection pending] |

## 四、版本演进对账台账（权威记录）

| 量 | 旧值/旧口径 | 现值/现口径 | 裁决 |
|:---|:---|:---|:---|
| 金融域 d′（市场真值）0.02 | 与 0.54–0.60 同列易误读 | 无新闻层（仅 EDGAR 元数据）消融基线，按构造在被引区间之外 | v1.4 裁决；v1.5 表 14-3 独立注 |
| H9 第四家族 Brier | v1.3 印 0.295 | 冻结记录 0.2848 → 0.285 | v1.4 更正回冻结值；誊录错误、无重冻结；v1.5 表 14-3 台账行 + §15.4 口径注 |
| ref 56 期刊 | Econometrica 83(1), 271–298 | American Economic Review 105(1), 272–298 | v1.5 按 Crossref 沉积更正 |
| ref 74 标题/文章号 | "The fake news game…" Palgrave Commun 5, 13 | "Fake news game confers psychological resistance…" Palgrave Commun 5, 65 | v1.5 按 Crossref 沉积更正（标题—期刊错配） |
| ref 130 页码 | 87(1), 1–10 | 87(1), Article 4 | v1.5 按出版方引用串更正 |
| 引用年份口径 | 隐式 | 在线优先年入正文引用、条目两年并列（refs 129/130/132/133） | v1.5 文献表后口径注 |

## 五、审计脚本与复现

`tools/audit_paper.py`、`tools/check_pdf_textlayer.py`、`tools/build_review_pdf.sh` 随代码仓库发布；构建链（pandoc → lualatex/xelatex）与字体依赖在脚本头注明。全部派生数据集可由随附抓取脚本从公开源确定性重建（种子固定）。

*(Supplementary Material S2, v1.5 · October 2026)*
