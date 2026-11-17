# SEA v1.10 审稿回复与修改说明

**审稿对象：**v1.9.0，公开提交 `106b4893aad8d16f60f438db2861495d1edf5595`。  
**本次修订：**v1.10.0 候选公开快照。  
**路线选择：**审稿意见建议的 **路线 A——条件性设计、治理接口与证据审计论文**。不把新增离线测试包装成端到端算法有效性或人类有效性证据。

## 1. P0-1：SAP 形式闭合、组件映射、算例与算法

主稿第 3 节已整体重写：

- 式 (1) 给出完整 SAP 元组；定义全控制状态、观察、可观察历史、监测/pull/push/delivery/override/write 行动、转移与观察核、奖励与伤害、折扣、有限时域、时间/计算/调用/金钱/风险预算、目标写入与回滚状态。
- 目标写入、拒绝、版本栈、回滚和哈希事件进入状态转移；平台只能通过候选生态或经授权的接口影响系统。
- 命题 3.1 使用完整生成模型对历史条件化，显式定义历史条件奖励、下一观察核和期望终端成本；只声称有限离散问题的最优历史策略存在，不声称低维 Markov 性或可计算性。
- 表 2 给出“总问题—子模型—附加假设—所得结论—不组合原因”映射。
- 新增两组来源覆盖反例：贪心监测加后续最优投递得到 17，而另一来源组合得到 22；证明组件近似比不自动成为联合最优。
- 表 3 给出六个目标的原始候选→更新→链接→配额→投递→打开→实际消费的完整数值算例：选择代理召回 3/6，投递和打开代理均为 2/6，实际消费为 1/6，遗漏 5/6=1/6+4/6。
- Algorithm 1 给出 guarded SAP step；固定池排序和目标记账为 `O(n log n+|E|)` 时间、`O(n+|E|)` 工作内存，模型调用数另由日志测量，不声称全局最优。
- `tools/reproduce_v110_sap.py` 与 `tools/test_v110_sap.py` 可重算上述全部数字；4 项回归通过（含对称信道和已测量未出席）。

## 2. P0-2：S1–S4 可执行治理符合性

新增 `sim/sea_governance/`：

- S1：目标、默认值、历史和来源可检查，导出的快照不能反向修改内部状态；
- S2：无授权、错误主体、陈旧版本令牌的写入被拒绝并记录；授权写入和回滚恢复目标字节及精确排序；
- S3：排序不使用平台变量；固定候选池/用户状态的平台反事实不变性单独测试；候选生态变化单独标为 `supply-ecosystem` / `supply-mediated`；
- S4：admission/ranking/delivery/override/rollback 均有证据指针和哈希链；载荷篡改、记录重排、锚定截断可检测；contest/recourse 可链接回放。

执行：

```bash
cd sim
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v sea_governance.test_reference
```

结果为 **14/14 通过**，机器报告为 `sim/pilot/results/governance_conformance_v1.10.json`。授权只是结构性 fixture，不是真实身份认证；哈希链不防御恶意主机整体替换；测试不证明有意义人类控制或端到端效果。

## 3. P0-3：效果识别定位

全文标题、摘要、贡献和结论统一定位为条件组件与审计。第 9 节把现有实验作为“审计如何推翻过强解释”的案例，不再以 agent-day 数暗示独立样本量。

未来协议只设一个主要比较：同模型/原始输入/权限/预算的 SEA 对 S2d 端到端筛选；只设一个主要结局：全分配实际消费加权遗漏。RAG、福利推荐和消融为分层次要分析。样本量通过独立语料/月份上的功效模拟确定。S2d/S4/S5、完整消融、时间外/私域语料、point-in-time 和记忆审计仍未执行。当前路线不以人类 RCT 为投稿前置条件，但也不作人类学习、福利或迁移结论。

## 4. P0-4：选择、投递、打开、实际消费与 ITT

形式模型使用

`available → linked → selected → delivered → opened → attended/consumed`，

每一阶段均可为 0/1/unknown。历史 `picked` 只称 selected proxy；没有补写任何 delivered/opened/attended 或效率数据。

新增 `sim/sea_pilot/audit_v110_consumption_caliber.py` 和 `sim/pilot/results/v110_consumption_caliber/`：

- 72,000 个预期键 = 71,970 个已存在键 + 30 个无记录键；
- 71,970 = 71,914 非空选择键 + 56 空选择键；157 条空记录，154 条存储的 parse-error；
- 主要历史稳健性口径 `ITT_ALL_RECORD_MEAN`：每个已存在键只进入一次，键内全部记录等权，空选择只对 selected proxy 补零，冲突保留为记录尝试均值；30 个无记录键不补零；
- 该口径不是恢复历史真实单次运行，也不是实际消费 ITT。合法 abstention 只有在未来日志明确标识后才进入全分配分母；
- G 的冲突拒绝口径逐指标公开 71,629/70,732/71,674；Rule A 为 71,573/70,676/71,618；strict-singleton 为共同 70,306 键；
- 主文表 9–13 分开报告估计量、键数、聚合规则和探索性 run-level 描述区间；所有 17 情景范围与 `scenario_effects.csv` 公开；
- `future_logging_schema.json` 包含分阶段事件、abstention/parse/transport/execution 状态，以及 calls、input/output tokens、cost、latency、retries。旧日志这些字段均没有，未进行回填。

## 5. P0-5：金融历史输入和公开复现阻断

已将 `8ffc7f5:sim/pilot/results/p2_rows.csv` 逐字节冻结为：

`sim/pilot/results/v19_financial_caliber_audit/historical_p2_rows_8ffc7f5.csv`

- 1,260 数据行，382,663 字节；
- SHA-256：`80e953d19efb44787d4fb8b03e37ee6cbfbfc325488769df8a0e89281b495024`；
- 记录来源提交、来源路径、生成规则、字节数和行数；
- 默认只读冻结 CSV，Git 历史仅是可选 provenance，不再调用 `git show`；
- 仅扩展参数 S2p 实际重建并核对 121/133、114/126；历史 S2p 和两版 S2p-feat 均为冻结行聚合，历史 120/126 和 0.722222 不称独立重建，历史公司—日分母仍未重建。历史供给 4.6/day 标为继承常量，不声称从该 CSV 验证。

新增 `sea_pilot.test_audit_v19_financial_caliber` 三项测试；无 `.git` 且 `PATH` 无 Git 的公开副本中，默认与 `--write --force` 均通过并保持数值不变。

## 6. 理论量词与术语

- 命题 5.1 改为 **clairvoyant/oracle relaxation**；等号要求实际消费已实现 top-m 关键价值，不暗示非先知策略可达。
- Pareto 部分改为 **normalized expected leaked value**，明确是期望之比，不是单次泄漏比例的期望。
- 第 5.4 节直接量化：所有 `i∈C_M` 及所有 `A⊆C_M\{i}` 的增益均须覆盖罚项；不得排除零增益上下文。分别声明 cardinality 普通 greedy、knapsack density-greedy+最佳单例和深度三 partial enumeration 的适用域和比值。
- 定理类编号统一为 Proposition；命题 5.2/5.3/5.4、6.1/6.3、7.1/7.2 不再混用同名 Theorem。关键公式编号 (1)–(11)。
- KKT 增加 `T>0` 的严格正可行点和 Slater 条件；补 Karush、Kuhn–Tucker 原始出处。

## 7. 实证报告与统计

- 全部区间统一称探索性 run-level 描述区间；Q/G 只有 10 run，共享语料、标签、缺失、冲突仲裁和模型依赖不在 bootstrap 内。
- Rule A 与 strict-singleton 不再被呈现为同一总体；每表标明场景、有效键和聚合规则。
- 全部 17 情景：O/C/Q/G 召回差点估计始终为正；O/G 引用收益始终为负，C/Q 始终为正；点估计符号变化均为 0。该事实不表示所有区间跨零情况相同，也不识别因果效应。
- 引用收益分解保留 O critical-item 区间跨零、O/G 非关键项损失更大和总收益为负的结果。
- 未来日志强制效率字段；历史缺少 calls/token/cost/latency/retries，不声称预算优势。
- 补 McNemar、Cochran、Mantel–Haenszel 和 Efron bootstrap 直接文献。

## 8. 文献定位

新增并核验 Lewis et al. (2020) 原始 RAG、Peng et al. (2025) Findings of EMNLP 智能体推荐综述、Lin et al. (2026) 自主信息寻求 roadmap（只称 arXiv 预印本）、RAGAs、ARES，以及 Clopper–Pearson、Karush/KKT、McNemar、CMH、bootstrap 原始方法来源。

因历史检索未保存完整命中/去重日志，本版改称**结构化叙述性文献定位＋定向书目核验**，不伪造 PRISMA 数字。`docs/LITERATURE_SEARCH_v1.10.md` 给出实际查询、数据库/出版商记录、筛选责任、去重规则、排除理由和出版状态。新颖性只保留非穷尽检索下的四条件组合定位，不再暗示首次整合主动性、工具或规划。

## 9. 代码—论文同步

`sim/sea_algo/` 标为历史 A1–A10 算法实验；清除“定理 6.1 分工”“定理 8.2”“引理 12.1”“§15.3”等失效引用，改用稳定实验标识和证据边界。新增 `sim/sea_algo/README.md`。README 的 9/9 只指 2026-09-30 历史套件，不是当前治理 14/14、数学测试或端到端验证。

## 10. 结构、图、表和排版

- 主文收束为目标授权→共享预算→分阶段遗漏→治理与实证审计；人类测量、紧急覆盖、公共议程和 H8/H9 移至 `docs/SUPPLEMENT_NORMATIVE_AND_TRANSFER_v1.10.md`。
- 新增三张 TikZ 图：SAP 信息流、availability→consumption 遗漏链、历史与未来识别结构。
- 15 张表均有编号和标题，正文明确交叉引用；关键公式编号 (1)–(11)。
- 复现命令手动换行；新增 `tools/check_pdf_layout.py`，以 Poppler 坐标检查页面左右安全边界。旧 v1.9 的第 27 页溢出可被该工具复现，v1.10 发布必须通过该检查和页面抽样目检。

## 11. 仍未完成

独立人类数学复审；S2d/S4/S5 与完整匹配消融；独立时间窗、知识截止后/私域语料；严格 point-in-time 和记忆审计；历史实际消费与效率数据；人类数据；公共实验预注册；第三方干净环境独立复现；v1.10 专属 DOI。

当前公开候选标签和全部离线审计不能被解释为上述事项已经完成。v1.7 DOI `10.5281/zenodo.23620920` 仅属历史版本，不覆盖 v1.9 或 v1.10。
