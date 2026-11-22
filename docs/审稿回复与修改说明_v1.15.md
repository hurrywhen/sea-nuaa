# SEA v1.15 综合评审意见逐条回复与修改说明

**评审对象：**v1.14.0，公开 main 提交 `8ef336ecf70583edd1bbc4218cf15e332ce291d5`。  
**本次修订：**v1.15.0 candidate / prerelease。  
**修订性质：**按评审建议与作者决定，把目标登记切换明确限定为**外生、冻结的评价协议事件**（评审方案 A），并采用**单线控制生命周期**；补齐 S12 的验证集→部署集可迁移性条件、完成子集代表性与近零分母精度预警；统一注册表相关符号；收紧 `validated` 注册的结构校验。不新增虚构人类数据、真实测量验证或部署有效性结论；评审确认已修复的测量边界、账本分离、异常遥测、预检原子性、材料单源与队列归因全部保留。

## 作者决定（评审要求二选一事项）

1. **登记切换语义：方案 A（外生评价协议事件）。**从策略行动集合中删除 registry-version switch；登记族与版本日程在实验前冻结；执行器只接受协议日程的下一成员。评审明示此路线可降为小修后再审，且与论文"有限冻结注册表族"的形式设定最自洽。
2. **生命周期：单线控制模型。**切换后原执行器自动 sealed，禁止再次运行；新执行器是同一控制实例的唯一活动路径。不采用显式分支模型（避免跨分支合并与因果顺序的额外复杂性）。
3. **符号：𝔅 族＋ρ_t，初始分布 ρ_0 改 μ_0。**图 1 中 reflective principal 保留 R，不再冲突。

## P0-1 登记切换的授权与事前注册表族约束

主稿 §3.2 重写，代码与形式模型同步：

- **行动集合**：尝试行动不再含 registry-version switch；新增专条说明登记转移是评价协议事件，位于每个 \(\mathcal A_t\) 之外，策略无权切换。
- **事前族声明**：fixture 新增 `registry_family`（版本→登记内容 SHA-256 allowlist）、`protocol_registry_schedule`（有序版本日程）与 `protocol_registries`（日程后续版本的完整冻结登记内容）。加载期即核验：活性登记必须是族成员且内容哈希与声明一致；日程成员必须属于族；冻结内容哈希必须与族一致。无声明的 fixture 退化为单成员族，任何切换都不可能。
- **授权语义**：明确说明登记转移**不需要也不接受**目标写入式授权（actor/principal/授权 ID/提案哈希/版本令牌/时间戳），因为它不是策略行动；取而代之的是族成员、内容哈希、日程下一位、活动路径四重协议校验。这回答了"谁有权切换"：只有事前冻结的评价协议本身，运行时任意调用者无权切换。
- **拒绝记录**：非族成员（含评审构造的 `unregistered-arbitrary-v999`）、篡改内容哈希、越序/回退、sealed 路径复用四类尝试均追加 `registry_switch_rejected` 记录（含尝试版本/哈希、原因码、`policy_action=False`、`state_mutated=False`、`resources_spent=0`），零状态变更、零扣减。
- **回滚语义**：登记转移只沿日程追加向前，**不存在登记回滚**；目标回滚只恢复目标版本，绝不恢复登记版本（新增正向测试：切换后回滚目标到版本 0，登记版本与哈希不变）。主稿 §3.3 明确 guard 只治理目标写入/回滚，登记校验是协议校验而非授权。
- **存在性论证**：补充材料 SA.0 的 Registry-version extension 改写为外生事件版本——转移不向尝试集合增加任何原始行动，协议事件由声明日程位置决定；有限族＋冻结内容保证有限历史论证不变。

## P0-2 连续性切换的并行控制分支

已采用**单线控制模型**，评审实测的缺口全部封闭：

- `continue_with_target_registry()` 接受转移时：先构造后继执行器（同一 `control_instance_id`、共享 `GovernanceReference`），**预算/历史/周期结果/更新候选改为共享同一对象（不是复制）**，随后封存原路径（`control_path_sealed` 记录，含原因与后继队列 ID），再追加队列边界记录（新增 `event_kind=exogenous_evaluation_protocol_event`、`policy_action=False`、`authorization_required=False`、`old_control_path_sealed=True`、协议声明哈希与日程位置）。
- sealed 对象的 `run_period()`、`write_after_period()`、`rollback_after_period()`、`_spend()` 一律抛 `RuntimeError`；sealed 对象上的切换/fork 尝试留下拒绝记录。资源状态因此唯一：不存在共享控制身份下独立变化的预算副本。
- `fork_for_target_registry()`（完全重置）保留为显式协议选择：新控制实例、独立目标/预算/账本；同样要求族成员＋哈希核验，并封存父路径，保证每个协议运行只有一条活动控制路径。fork 的日程为父日程自 fork 版本起的后缀（或单版本日程）。
- 评价队列定义与单线路径一致：\(v_t\) 恒定的极大区间沿唯一活动路径取；跨队列不合并。
- 新增演示工件 `sim/pilot/results/sap_v1.15/protocol_registry_switch_demo.json`：完整跑通"period 0 → 协议切换 → period 1 → 目标回滚不恢复登记 → 五类拒绝 → sealed 复用拒绝 → fork 新实例"，全部检查为真、审计链验证通过。

## P0-3 负例测试（评审点名三类＋扩展）

| 负例 | 测试 | 断言 |
|---|---|---|
| 非族成员 `unregistered-arbitrary-v999`（无 actor/授权/时间戳） | `test_non_family_registry_switch_is_rejected_with_record` | 拒绝记录＋原因码；零扣减；原登记不变；未 sealed；fork 同样拒绝 |
| 族成员但内容篡改 | `test_tampered_family_registry_hash_mismatch_is_rejected` | 哈希不匹配拒绝记录；零变更 |
| 越序/回退/超出日程末端 | `test_out_of_schedule_switch_is_rejected` | 回退到 v1 与重复 v2 均拒绝 |
| 原对象复用 | `test_sealed_predecessor_cannot_run_write_rollback_or_switch` | run/write/rollback 抛 RuntimeError；切换留拒绝记录；seal 记录归因正确；后继继续运行且预算唯一 |
| 无族声明 fixture 的切换 | `test_switch_without_family_declaration_is_rejected` | 单成员族下任何他版本拒绝 |
| 冻结声明加载期核验 | `test_frozen_family_declaration_is_verified_at_load` | 哈希漂移/日程越族/冻结内容漂移均拒绝加载 |
| 目标回滚≠登记回滚 | `test_objective_rollback_does_not_restore_registry_version` | 回滚接受且登记版本/哈希不变 |
| 演示全检查 | `test_protocol_registry_switch_demo_passes_all_checks` | 5 拒绝、2 封存、1 队列边界；外生事件字段齐全 |

发布审计另在进程内**功能性复测**评审两个针对性反例（不依赖字符串）：任意 v999 切换被拒绝且零变更；合法切换后原对象 sealed、预算对象同一、控制实例同一。

## P1-1 S12 验证集→部署集误差可迁移条件

补充材料 SD.3.4 新增 **Validation-to-deployment transportability** 段：显式写出

\[
P_{\mathrm{validation}}(Z=1\mid D=1,a)=P_{\mathrm{deployment}}(Z=1\mid D=1,a),
\]

及特异度对应条件；声明这是假设而非 (S12) 的推论；语料域、用户群、测量完成机制差异可破坏该条件；不满足或存疑时改用协变量标准化、分层估计或预注册误差率敏感性网格，不得静默传输点估计。协议 §1.4.1 新增第 4 项（可迁移性条件与完成子集代表性），注册字段强制 `transportability_assumption` 声明。主稿 §4.3/§7 同步。

## P1-2 完成子集代表性与臂间误差差异

- 协议 §1.4.1 第 4 项要求按臂×阶段报告测量完成子集相对全分配单元的代表性；注册强制 `completion_subset_representativeness` 非空说明。
- 臂间误差差异检验（原第 3 项）保留：预声明等效性/不可容忍界值；超界必须附显式误差模型敏感性分析。
- `validated` 注册另强制独立盲法参考集记录（`blinded_reference_set`：构造规则、数据哈希、解锁时间、与调参/主分析语料无重叠声明）。

## P1-3 近零分母精度预警与敏感性网格

- 补充材料 SD.3.4 新增 **Precision warning near a zero denominator** 段：令 \(J_a=se_a+sp_a-1\)，(S12) 除以 \(J_a\)，方差放大 \(1/J_a^2\)；\(J_a\to0\) 时传输高度不稳定、正态近似区间不可靠；预警触发时必须回退到预注册 \((se_a,sp_a)\) 敏感性网格；传输估计越出 \([0,1]\) 表示模型不相容，必须如实报告不得静默截断。
- 参考实现新增 `completed_measurement_transport()`（报告 \(J_a\)、放大因子、预警标志，默认阈值 0.1）与 `completed_measurement_transport_delta_method()`（声明独立输入下的 delta-method 传播；相关输入须加协方差项）。数值测试：完美测量恒等、仅假阴性情形 \(m^D=0\)、 worked example \((0.13-0.1)/0.85\)、\(J=0.05\) 触发预警、\(se+sp=1\) 拒绝、delta-method 方差手算核对。
- 协议 §1.4.1 新增第 6 项（近零分母精度预警与敏感性网格）。

## P1-4 独立人员复核

动态登记状态转移（外生事件＋单线生命周期）、公式（6）、S12 及其可迁移性/精度表述的**独立人类数学复审仍未完成**；主稿、RELEASE 与 evidence_status 继续如实标注 pending。本轮作者侧检查（测试、数值恒等、单源核对、干净副本验证）不替代独立复核。

## P2-1 符号去重

- 注册表族 \(\mathfrak R=\{\rho^{(1)},\ldots,\rho^{(K)}\}\)（有限、事前冻结、含内容哈希）；活性登记 \(\rho_t=(v_t,E_{v_t},\mathcal T_{v_t},A^{ref}_{v_t})\)；元组测度族索引改为 \(\{\nu^{(v)}\}_{\rho^{(v)}\in\mathfrak R}\)。
- 初始分布 \(\rho_0\) 全文改 \(\mu_0\)（主稿、补充材料、协议、evidence_status 同步）；目标回滚版本历史保留 \(\mathcal V_t\)，不再与族索引冲突；图 1 reflective principal 保留 R。
- 补充材料 SD 编号约定段显式声明符号表；SD.2.1 极限中的标量 \(\rho\) 是局部约束比率（bound variable），与登记状态 \(\rho_t\) 无关，已在符号约定中注明。
- 附录 A 表 6 新增 𝔅 与 μ_0 行、更新 ρ_t 行；附录 B 表 7 新增"Protocol registry governance"可证伪行。

## P2-2 validated 注册对象进一步严格

`OperationalAttendanceInstrument` 的 `validated` 分支新增：

- **真 64 位十六进制哈希校验**（`_is_sha256_hex`，小写 hex 全匹配，而非仅长度）：验证数据哈希、测量代码哈希、盲法参考集数据哈希；参考语料快照/文档内容哈希与机器事件谓词同步升级。
- **敏感度/特异度区间**：`sensitivity_interval`/`specificity_interval` 必须为有限二元区间、覆盖点估计且含于 \([0,1]\)。
- **独立盲法参考集构造与解锁时间**：`blinded_reference_set` 四字段强制，重叠声明必须为 False。
- **完成子集代表性说明**与**可迁移性假设声明**强制非空。
- 新增三组专项负例测试（非 hex/大小写/长度错误、区间缺失/逆序/越界/非有限、参考集字段缺失/重叠为真、代表性缺失）。
- 明确这些是**结构性注册检查**，不构成已完成真实测量验证；随附对象仍为 `synthetic_instrument_fixture`，不得当作已验证实例（主稿 §4.3、协议 §1.4、docstring 同步）。

## P2-3 编辑与可访问性

- **分页**：删除附录前强制分页，附录 A 紧随参考文献自然起排，消除 v1.14 参考文献末页大量留白；表 6 以重复表头合理跨页（前页 6 行、后页 8 行），表 7 不跨页；全文 21 页。构建后目检首页、算法页（Algorithm 1 整块在第 9 页）、p20/p21 与坐标检查确认。
- **tagged PDF** 仍未生成，继续列为后续可访问性事项（低优先级，不影响科学内容）。
- 统一参考文献仍为 52 条（本轮无新增文献；可迁移性条件为显式假设陈述，Youden 指数作为诊断试验标准术语描述性使用）；自动检查每条均被实际引用。

## 评审确认已修复事项（全部保留，未重构）

公式（6）只处理 operational attendance omission、无 unknown 时 \([\Delta^{FC},\Delta^{FC}]\) 且仅另给 \(\Delta^{FC}=0\) 才 \([0,0]\)；S12 代数与限定；NaN/±Inf/越界/负时长/非布尔/空指针→unknown；阈值注册校验；delivered-未-selected 无提交预演拒绝（零记录零扣减）；队列全事件归因；回顾性表格单源（R5 再生成核对 MATCH）；主文不以历史 selected-proxy 数字支持结构效果。

## 证据边界（全部保留）

1. 两套确定性目标提取规则的一致性≠独立人工目标验证（pending）。
2. 合成 attendance fixture≠真实测量工具已验证（pending；§1.4.1 为未来方案，含可迁移性与代表性义务）。
3. AND 规则可能增加操作性假阴性；独立验证集的敏感度/特异度、臂间差异与可迁移性报告是解锁前义务。
4. S2/S2d 匹配 fixture 与协议转移演示只证明接口可执行，不识别结构效应。
5. 真实匹配实验、独立时间外语料、第三方复现与人类数据仍是未来有效性主张的必要证据。
6. 外生协议事件语义是**形式/接口设计**，不是对真实实验治理机制的已验证实现；授权记录仍是结构性 fixture，不是认证身份。

本回复与自动测试同样不能替代主稿所声明的独立人类数学复审。

## 验证摘要（作者侧）

- 治理 18/18；纵向执行器 **32/32**（新增 12 项）；目标构造 4/4；消费口径 6/6；冻结重放 20/20；金融 3/3；数学/SAP 13/13（sim 合计 83 项）。
- 评审两个针对性反例功能性复测：`unregistered-arbitrary-v999` 无授权切换→拒绝记录＋零变更；连续性切换后原对象 sealed、预算唯一共享、无并行活动路径。v1.13 轮三个反例（NaN/inf/1.5→unknown、delivered-未-selected→修改前拒绝）继续复测通过。
- 回顾性 R5 单源核对 MATCH（40 行）；发布审计 **140/140**（含 PDF 文本层 0 问题、布局 PASS、21 页）；arXiv XeLaTeX 0 缺字形；干净公开副本验证与无 Git PATH 金融复现见 `tools/audit_v115_report.json`、`tools/clean_verification_v1.15.json` 与 REPRODUCIBILITY。
- 字符串检查不替代语义一致性验证；本轮另行人工核对了 §3.2 外生事件/单线生命周期表述、SA.0 扩展、S12 可迁移性条件方向与 delta-method 偏导数。
