# SEA v1.13 综合评审意见逐条回复与修改说明

**评审对象：**v1.12.0，公开 main 提交 `fc76ead97ac36479db4c8be9002f3d6d382b0667`。  
**本次修订：**v1.13.0 candidate / prerelease。  
**修订性质：**实质性修改数学边界、账本语义、补充材料同步和执行器时间/链接/资源规则；不新增虚构人类数据或部署有效性结论。

## P0-1 公式（6）修正

已采用推荐方案 A：公式（6）改为**纯操作性 attendance 遗漏边界**

\[
\Delta^{FC}-u_{sea}\le \mathcal M_{\nu,sea}^{Z}-\mathcal M_{\nu,control}^{Z}\le \Delta^{FC}+u_{control}.
\]

不再声称无假设界定潜在真实消费遗漏 \(\mathcal M_\nu\)。主文和协议新增无 unknown 反例：SEA 假阳性 \(Z=1,D=0\)、对照真阳性 \(Z=1,D=1\) 时，操作性边界为 \([0,0]\)，潜在遗漏差值为 1；假阴性可构造反向违反。若要传输到潜在消费，至少需要非 unknown 测量完美分类 \(D\)，否则必须建模臂别敏感度/特异度及不确定性。

`failure_composite_contrast_bounds()` 已改为 `operational_attendance_contrast_bounds()` 的兼容别名，返回 `estimand=operational_attendance_omission_contrast_not_latent_actual_consumption`，并新增误分类反例测试。未来 schema 主规则标识更新为 `ALL_ASSIGNED_FAILURE_COMPOSITE_OPERATIONAL_ATTENDANCE_OMISSION_V1`。

## P0-2 理论账本与可执行账本分离

主文 §4.2 明确两套账本：

- 理论账本终端为 \(D_S=\cup_iD_i\)，定义 \(\mathcal M_\nu\)，不可由操作性遥测单独执行；
- 可执行 operational/FC 账本终端为有效阳性 \(Z_S^+\)，unknown 单独保留，计算 \(\mathcal M_\nu^{FC}\)。

执行器输出改为 `operational_target_ledger`，`ledger_scope` 标明 NOT_LATENT；所有 `latent_actual_consumption` 仍为 null。首个失败阶段分区只声称实现操作性/FC 分区，不再声称实现潜在消费分区。

## P0-3 符号与五维坐标统一

来源覆盖改为 \(G_i(e)\)，操作性 attendance 保留 \(Z_i(e)\)，潜在消费为 \(\Gamma_i/D\)。覆盖概率统一 \(c_e(S)\)，KKT 影子价格统一 \(\lambda_B\)。主稿和补充材料不再使用 actionability 作为当前参考坐标；五维统一为 relevance/novelty/credibility/durability/harm_avoidance。主文“operational-consumption measurement”统一为“operational attendance measurement”。形式补充材料中残余的覆盖符号 \(Z_i(e,\omega)\)（SD.3.6 监控组合）已改为 \(G_i(e,\omega)\)；SD.1 的增益/损失符号 \(G_{i,d}/L_{i,d}\) 改为 \(\mathrm{Gain}_{i,d}/\mathrm{Loss}_{i,d}\)，避免与覆盖 \(G_i(e)\)、链接 \(L_i(e)\) 和守卫 \(\mathcal G\) 冲突。

## P0-4 补充材料同步与统一参考文献

形式补充材料已重排并二次同步：

- SA.0 位于 SA 证明组内；SD 技术基础使用独立编号 SD.1–SD.4，全部命题/推论/定义改为 SD 前缀（Proposition SD.1–SD.10、Definition SD.1、Corollary SD.7），公式号使用 S 前缀，避免与主稿章节号和公式号冲突；SA.1–SA.3 与 SD 内部交叉引用全部更新。
- SD.2.3 的“Table 5”改为 Supplementary Table SD1，消除与主稿表 5 的编号冲突。
- SD.3.4 重写为**两套账本**：理论账本终端 \(\widetilde O\cap D_S^c\) 为潜在消费损失，不可由操作性遥测单独执行；可执行 operational/FC 账本终端 \(\widetilde O\cap(Z_S^+)^c\)，unknown 单独标记；执行器只实现后者。旧“\(\Gamma_i\) (attendance/actual consumption)”混用表述和图注“to actual consumption”已删除，阶段图与主稿图 2 一致。
- SD.3.5 的 Clopper–Pearson 陈述明确为理论账本结果：由操作性遥测实例化 \(X_j\) 需要非 unknown 测量完美分类 \(D\) 的额外假设，否则估计的是 \(\mathcal M_\nu^{FC}\)。
- 旧 \(\kappa_e\)、actionability、attended/consumed、KKT \(\nu\) 影子价格均已替换；“Section 5.4”陈旧交叉引用改为 Section SD.2.4。
- 规范性补充材料章节 S1–S5 改为 N1–N5，避免与治理符合性 S1–S4 冲突。
- 主稿参考文献扩展为 **52 条统一表**，覆盖 Resnick、Karush、Kuhn–Tucker、Charnov、Savage（1951，规范性补充 N2 引用）、Efron、McNemar、Cochran、Mantel–Haenszel 等补充材料引用；Savage 的书目核验已补入 LITERATURE_SEARCH。新增自动检查：统一表中每条文献必须在主稿正文或某一补充材料/检索记录中实际被引用（Allcott、Stray、Santoni de Sio、Papadimitriou–Tsitsiklis 已补入正文相应位置；Efron/Cochran/Mantel–Haenszel 补入回顾性补充 R4/R7）。字符串检查不替代语义审查，本轮另行人工核对了 SD.3.4/SD.3.5/SD.3.6 的测量语义。

## P0-5 availability_window 纵向语义

已改为 `first_available_period`，并明确持久性假设：自该期起持续可用。执行器 `_available_targets(candidate, period)` 按期过滤。新增延迟可用性测试：doc2 设为 period 2 才可用时，period 0/1 的 e2 均进入 availability 失败，且 period 1 不再产生该终端 unknown。

## P0-6 S2d 选择链接与评价目标对齐

 fixture 分离 `staged_link_pass` 与 `reference_link_truth`：

- SEA 选择时使用 staged linkage 结果；
- S2d 选择时绕过 staged filtering；
- 两臂评价均使用臂无关的 reference target-alignment truth。

新增专项测试：c3 staged-link 失败但 reference truth 通过时，S2d 可选择 c3 且 e3/e4 在评价中视为 linked；SEA 不选择 c3。论文表 3 和 §3.4 明确该区别。

## P1-1 控制延续与评价版本更新

新增 `continue_with_target_registry()`：保留目标、授权、回滚、审计和资源状态，仅创建新 evaluation cohort；`fork_for_target_registry()` 保留为完全重置选项。主文和协议明确完全重置是评价协议选择，不是 SAP 控制的必要定理。动态规则标识改为 `NEW_EVALUATION_COHORT__NO_CROSS_VERSION_POOLING`。

## P1-2 测量验证

当前仍只有合成 fixture 和阈值注册，**不声称已完成真实独立 attendance 测量验证**。协议要求独立验证集估计假阳性、假阴性、臂间差异和不确定性；主文公式（6）已明确没有这些假设时不能界定潜在消费。真实验证仍列为未完成事项。

## P1-3 资源预检与专项测试

执行器新增整期保守资源预检，在任何 observation/update/spend/ledger 修改前检查最大声明选择限额和计划终端事件成本；终端计划的结构校验（delivered/opened 必须是已知候选且 opened ⊆ delivered）也前移到任何状态修改之前。新增测试：time=0 时 run_period 抛错且审计记录与已花费资源不变；非法终端计划同样在修改前抛错。S2d staged-link 失败候选测试已加入。误分类反例测试同时覆盖假阳性（潜在差值 +1 越出 [0,0]）与假阴性（潜在差值 0 越出 [-1,-1]）两个方向。

## P1-4 表 1 否定单元格收窄

表 1 否定单元格改为 NC（cited representative works 中非中心）和 NI（reviewed sources 中未识别），并说明非穷尽检索不支持对整个文献的全称否定。

## P1-5 机器事件谓词

`machine_ingestion_and_task_reference()` 明确为合成占位谓词，仅检查 fixture 哈希字符串关系，不是密码学证据链。主文、协议、执行器输出和测试均标明真实日志需要内容、回执、任务操作绑定证据结构。

## P2 编辑性修改

标题改为 “A Conditional Framework and Synthetic Audit Artifacts”；摘要压缩至约 170 词；删除单独目录页；新增 Part II；Algorithm 1 用 Needspace 保持整体（现整段落于同一页）；哈希 body 字段改为 `sequence`；guard scope 明确为 operation identifier。主稿表 6 的 \(\mathcal T_v\) 范围说明由“新版本创建新 SAP 实例”改为“新版本创建新评价队列；控制连续性可选”，与 §3.1 和协议一致。REPRODUCIBILITY 中未来 schema 版本（/v4）、评价队列表述、测试计数与 PDF 页数（20 页）已同步。tagged PDF 仍未生成，列为后续可访问性事项。

## 验证与仍未完成事项

已完成：18/18 治理；14/14 纵向执行器；4/4 目标构造；6/6 消费口径；13/13 数学/SAP；20/20 冻结重放；3/3 金融公开输入；四类历史数据审计；v1.13 发布审计（112 项，含统一参考文献逐条被引检查、补充材料账本/符号/编号同步检查）；PDF 文本层/坐标/作者元数据；XeLaTeX 缺字检查；无 `.git` 公开副本验证（18/18 组命令、729 个 arXiv 附件哈希）。最终计数和哈希以 `tools/audit_v113_report.json`、`tools/clean_verification_v1.13.json` 和 `docs/工件清单_v1.13.json` 为准。

本轮另修复一处发布溯源缺口：arXiv 附件此前混入 21 个被 `.gitignore` 排除的内部 dispatch 运维日志（含节点地址），导致工作树包（750 项）与公开副本包（729 项）不一致。现 `make_arxiv_source.sh` 不再复制这些内部日志（逐 run 元数据已在被跟踪的 `llm_replay_summary_*.json`），两种构建均为 729 项；`make_public.py` 新增 arXiv 源包开包敏感模式扫描（发现内部标识时自动从脱敏树重建并复检），并停止导出旧版 arXiv 源包与解包目录（与旧审稿 PDF 同一政策）。脱敏公开副本体积由 751M 降至 236M，泄漏自检 0 处。

仍未完成：独立人类数学复审；独立人工目标/attendance 验证；第三方复现；真实匹配实验；独立时间外/私域语料；point-in-time/记忆审计；新消费/效率观测；公共注册；人类数据；v1.13 DOI。历史 v1.7 DOI 不覆盖 v1.9–v1.13。
