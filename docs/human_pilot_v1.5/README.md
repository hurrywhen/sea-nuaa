# HP-0 人类可行性试点工具包 v1.5 / Human Pilot Kit

> 状态：**[designed; data collection pending — no human data exist yet]**
> 定位：SEA 论文（v1.4）对审稿意见 R1/P2-14 与 R3/意见3 的最小人类侧回应；
> n ≤ 10、每日 ≤20 min、14 天、被试内、仅可行性端点（明确 UNDERPOWERED，不做假设检验）。

## 1. 文件清单 / File Inventory

| 文件 | 内容 | 状态 |
|---|---|---|
| HP0_protocol_v1.0.md | 协议（中文 + 英文摘要）：设计、端点、预注册判定、SAP、伦理、局限 | 冻结待备案 |
| HP0_consent_form_v1.0.md | 知情同意书（中文正文 + 英文摘要 + 签署栏） | 冻结待备案 |
| HP0_materials_v1.0.md | 参与者材料：声明工作单、预测表、日记、暴露日志、极化量表 | 冻结 |
| HP0_data_template.csv | 数据模板（表头 + 2 行 EXAMPLE 示例；EXAMPLE 行永不进入分析） | 冻结 |
| analyze_hp0.py | 分析脚本（Python3 + numpy；E1/E2/E3、Wilson、bootstrap、Wilcoxon、BH） | 干跑通过 |
| HP0_dryrun_SYNTHETIC.md | 合成数据干跑产物（**非真人数据**，永不进入论文） | 自动生成 |
| HP0_dryrun_synthetic_data.csv | 干跑合成数据（seed 42） | 自动生成 |
| README.md | 本文件：运行手册与稿件引用规则 | v1.0 |

## 2. 每日运行手册（一次坐完 / one sitting per day）

- **D0（导入日，≤20 min）**：出示伦理备案文件 → 签署同意书 → 计时完成声明工作单（协调员按话术卡记录澄清提示与修订次数）→ 3 题基线极化自评 → 告知随机顺序（AB/BA）→ 录入 day-0 行。
- **D1–D14 每日一次坐完（典型 5–10 min）**：晨间收 3 条投递条目 → 每条 urge 打分（0–4）→ 5 项日记 → 录入当日行。暴露周参与者在该周内任选 3 天加做一次对立阅读（≤10 min）+ 暴露日志（当日 exposure_count=1）。
- **D1 / D8（≤15 min）**：加填当周 10 题预测表（概率区间圈选）；决议值由双人核对后于 D7/D14 行录入 brier_item_01..10（= 每题 (p−o)²，三位小数）。
- **D7 / D14（≤10–20 min）**：极化量点 #2/#3；D14 另发放全部 20 题决议反馈（此前不反馈）+ 结题三问。
- **录入约定**：participant_id 用 P001–P010 伪名；缺失一律留空（不插补、不填 0）；arm 列填该周的 EXPOSURE / NO_EXPOSURE。

## 3. 分析运行

```bash
# 管线验证（合成数据，seed 42；产物带 SYNTHETIC 横幅）
python3 docs/human_pilot_v1.5/analyze_hp0.py --synthetic-dryrun

# 真人数据（采集完成后；默认读 docs/human_pilot_v1.5/HP0_data.csv）
python3 docs/human_pilot_v1.5/analyze_hp0.py --input docs/human_pilot_v1.5/HP0_data.csv
```

- 输出：`HP0_results.md`（真人）或 `HP0_dryrun_SYNTHETIC.md`（干跑）+ 控制台摘要。
- numpy 缺失时脚本给出安装提示并安全退出（exit 2）；仅含 EXAMPLE 行时提示"无真人数据"并退出（exit 3），不写结果文件。
- 一切数值口径以 HP0_protocol_v1.0.md §8（SAP）为准；脚本与规约冲突时，先改规约（留痕）再改代码。

## 4. 稿件引用规则（强制）

1. **结果进入论文的唯一路径**：真人数据采集完成 → `HP0_results.md` 生成并归档 → 按协议 §12（PR-3）核对 → 方可写入稿件/回复信。
2. **在此之前**，论文与回复信中凡提及 HP-0 处，一律标注：
   **[designed; data collection pending — no human data exist yet]**；
   全部人类侧陈述保持"predictions-to-be-tested"措辞（R1/P2-14 的备选项）。
3. 干跑产物（HP0_dryrun_SYNTHETIC.md / HP0_dryrun_synthetic_data.csv）为管线验证件，
   **永不**作为数据、证据或示例数字进入稿件（论文 §15.6：模拟数据不得冒充人类数据）。
4. HP-0 数值即使采集完成，也只能支撑"可行性/需修改"表述，**禁止**任何因果、效力或
   群体推断表述（协议 §2.2、§11 随结果强制引用）。

## 5. 启动前检查单

- [ ] 本地伦理委员会豁免/快速审查认定文件已归档（不声称已有批准）
- [ ] 协议 v1.0 + 脚本 git tag 冻结（预注册 PR-1/PR-2）
- [ ] 随机化顺序种子已生成并记录（入组前）
- [ ] 预测题库 20 题（W1/W2 各 10）已按材料 §B.3 规则预建并预登记决议源
- [ ] 协调员已完成 ≤1 h 培训并持话术卡
- [ ] 本地加密存储目录与伪名对照表（分离存放）已就位
