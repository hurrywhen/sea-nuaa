# SEA v1.14 综合评审意见逐条回复与修改说明

**评审对象：**v1.13.0，公开 main 提交 `0f04fe6319dac4bb5ecb1c631e50eb91aa139100`。  
**本次修订：**v1.14.0 candidate / prerelease（小修）。  
**修订性质：**按评审建议把动态目标版本写进形式模型、把异常测量输入和迟发计划错误处理正确、让每份材料只有一个权威来源；不新增虚构人类数据、真实测量验证或部署有效性结论。评审第五节的全部证据边界原样保留。

## P0-1 SAP 元组与控制实例／评价队列的对应关系

已采用评审给出的**方案 B（按控制实例定义 SAP）**，主稿 §3.2 重写：

- 元组改为 \(\mathrm{SAP}=\langle H,\gamma,\mathcal X,\mathcal Y,\widetilde{\mathcal A},\{\mathcal A_t\},P,r,\Phi,\rho_0,\mathcal G,\{\nu^{(v)}\}_{v\in\mathcal V}\rangle\)：固定单一 \(\nu\) 改为预先声明的**版本索引测度族**。
- 状态新增 \(R_t=(v_t,E_{v_t},\mathcal T_{v_t},A^{ref}_{v_t})\)：活性登记版本、命题集、候选—目标映射与参考可用性证据进入状态；登记族有限且事前冻结。
- 版本切换是**受控转移**：替换 \(R_t\)、向 \(L_t\) 追加队列边界记录，可保留目标/授权/审计/资源状态（控制连续性）或按声明完全重置。
- **评价队列**定义为 \(v_t\) 恒定的极大区间；其估计量在评价时选择 \(\nu^{(v_t)}\)，不跨队列合并。
- 闭合性说明：登记族有限且冻结，故 Proposition 3.1 的有限历史存在性论证不变（补充材料 SA.0 新增“Registry-version extension”段）。
- 代码对应：`SAPExecutor` 一个对象服务一个队列；`continue_with_target_registry()` 即受控版本切换转移，`fork_for_target_registry()` 为完全重置选项；执行器输出新增 `sap_tuple_scope` 字段。协议 §1.3 与 REPRODUCIBILITY §8 同步。

两期 fixture 的运行结果不变（数值恒等），但动态目标情形现在在形式模型内闭合，而不是留在元层。

## P0-2 attendance 输入校验与 invalid→unknown

`OperationalAttendanceInstrument.measure()` 重写校验路径，评审实测的三个反例全部修复：

| 输入 | v1.13 输出 | v1.14 输出 |
|---|---|---|
| `coverage_fraction=NaN` | negative | **unknown** |
| `coverage_fraction=inf` | positive | **unknown** |
| `coverage_fraction=1.5` | positive | **unknown** |

新增规则：`math.isfinite()` 检查；`engaged_ms>=0`；\(0\le\text{coverage\_fraction}\le1\)；遥测必须为数值（拒绝布尔与字符串）；`focused_visible`/`content_linked_confirmation` 必须为布尔；`evidence_pointer` 必须为非空字符串；**阈值自身**在注册时检查有限性与范围（`min_engaged_ms>=0`、`min_coverage_fraction∈[0,1]`）。新增负例测试 15 组（NaN/±Inf/越界/负时长/空指针/空白指针/非布尔/字符串数值）与阈值注册拒绝测试 6 组；完整有效但低于阈值的测量仍为 negative，不被误判 unknown。

## P0-3 delivered-未-selected 的事后部分状态变更

已采用评审建议的**无提交选择预演**：

- `_compute_updated()`、`_selection_decision()` 为纯函数；`GovernanceReference.rank()` 新增 `record=False` 预览模式（不追加审计记录）。
- `run_period()` 顺序：结构校验 → 仪器注册校验 → 纯资源预检 → **commit-free 选择预演** → （全部通过后才）追加 precheck/dry-run 记录 → observation/update/link/select/terminal/ledger。
- “已存在但未被选择候选出现在 delivered 中”在任何状态变更前抛 `ValueError`：专项测试断言审计记录数不变（0 条）、五维资源扣减为 0、`updated_candidates` 与 `period_results` 为空。覆盖两种情形：staged-link 失败候选（SEA 的 c3）与超出选择限额的合格候选（limit=1 时的 c2）。
- 提交阶段的选择与预演使用同一纯决策函数；若两者分歧（理论上不可能，状态相同）在投递扣减前抛 `RuntimeError`。
- 资源预检记录也改为预演通过后才追加，因此资源不足与结构错误两条失败路径都保持零记录零扣减。Algorithm 1 第 0 步与主稿 §3.4 同步更新。

## P0-4 回顾性表格单一权威来源

- 形式补充材料中的 SB.1–SB.3 表格**全部删除**，SB 节改为单源指针；标题改为 “Deferred Proofs and Standard Technical Foundations”。
- Rule A、strict-singleton、17 情景表只保留在 `SUPPLEMENT_RETROSPECTIVE_AUDITS_v1.14.md` §R5 一处。
- 新增 `tools/make_retrospective_tables.py`：从冻结数据文件（`v110_consumption_caliber/scenario_effects.csv` 与 `v19_recall_value_tradeoff/summary.json`）**重新生成** R5 全节（表格与文字断言均先对数据验证后输出），默认只读核对补充材料是否漂移（漂移即退出码 1），`--write --force` 产出专用工件 `sim/pilot/results/retrospective_tables_v1.14/`。发布审计包含同一核对。当前核对结果：MATCH（40 行）。
- 主稿 §5/§6.3 的指针同步：证明与模型计算表在形式补充材料，回顾性估计只在回顾性补充材料。

## P0-5 反例表述补条件

主稿 §4.3 改为：“with no unknowns the operational bounds collapse to \([\Delta^{FC},\Delta^{FC}]\), and to \([0,0]\) when additionally \(\Delta^{FC}=0\)”。反例本身使用零对比，保持有效。测试注释、协议 §1.5 与 evidence_status 同步更新；边界函数代码无需改动（无 unknown 时本就返回 \([\Delta^{FC},\Delta^{FC}]\)）。

## P1-1 最小仪器注册对象：补齐＋显式降级双管齐下

- fixture 注册对象新增 `registry_scope="synthetic_instrument_fixture"`，主稿 §4.3、协议 §1.4、执行器 docstring 与输出均明确：**随附对象是合成 fixture，不是完整预注册仪器登记册**。
- `validation_status="validated"` 时代码强制完整字段：`raw_event_schema`（非空对象）、`validation_data_sha256`/`measurement_code_sha256`（64 位哈希）、`measurement_error`（敏感度/特异度∈[0,1]＋验证集指针）、`alternative_instruments`（非空字符串列表）、`assessor_blinding="arm_and_model_blind"`、`registry_scope="preregistered_instrument"`；缺项或不合法即拒绝注册。新增专项测试（含完整注册被接受并正常判阳性）。
- 合成 fixture 不得冒用 preregistered scope；`synthetic_fixture_only` 必须声明盲法不适用。

## P1-2 跨队列审计归因

每个队列相关审计事件的 payload 统一携带四个字段：`control_instance_id`、`evaluation_cohort_id`、`target_registry_version`、`target_registry_sha256`。覆盖：resource_precheck、selection_dry_run、observation、update、resource_use（全部阶段）、ranking（经 `rank(context=…)`）、selection、period_outcome、override/rollback（经 `write_objective/rollback(context=…)`）。`evaluation_cohort_change` 记录携带控制实例 ID 与新旧队列 ID、新旧登记版本及哈希。新增跨版本切换的全事件归因测试：切换前记录属队列 1、切换后属队列 2，锚点验证通过。共享账本的跨版本不合并分析不再需要推断事件归属。

## P1-3 first-available-period 到期正向测试

新增 `test_first_available_period_expiry_restores_availability`：doc2 设为 period 1 起可用；period 0 的 e2 为 availability 失败且可用候选为空；period 1 的 e2 可用、链接、选择、投递、打开并获阳性 attendance，`first_failed_stage=None`、终端 unknown 权重为 0。与原延迟不可用测试互补。

## P1-4 真实 attendance 工具的误分类验证与臂间误差比较方案

协议新增 **§1.4.1（解锁前必须完成）**：

1. 独立盲法参考集（时间外验证单元、臂/模型家族/结局盲法、评审间一致性与仲裁）；
2. 臂别敏感度/特异度及区间、AND 规则操作性假阴性率与假阳性率、unknown 率按臂×阶段×原因单列；
3. 预声明臂间误差差异的等效性/不可容忍界值与检验；超界必须附显式误差模型敏感性分析；
4. 显式误差模型下完成测量部分的传输：补充材料 SD.3.4 新增恒等式 (S12) \(m^{D}_a=(m^{Z}_a-(1-se_a))/(se_a+sp_a-1)\)（要求 \(se_a+sp_a>1\)），并传播 \(se_a,sp_a\) 估计不确定性；明确这只是敏感性分析，不是无假设边界；
5. 验证集样本量按目标区间宽度预计；验证失败/盲法破坏的域不得进入主要分析。

主稿 §4.3/§7 增加对应指针。该方案是设计，未执行，不构成真实测量已验证的证据。

## P1-5 独立人员复核

动态目标版本闭合、公式（6）与 CP 测量一致性表述的**独立人类数学复审仍未完成**，主稿、RELEASE 与 evidence_status 继续如实标注 pending。本轮作者侧检查（测试、数值恒等、单源核对、干净副本验证）不替代独立复核。

## P2 编辑性修改

- 分页：附录 B 表格不再以“仅尾部＋大量留白”落在末页（构建后目检与坐标检查确认；详见 REPRODUCIBILITY 与布局报告）。
- tagged PDF 仍未生成，继续列为后续可访问性事项。
- 标题、摘要长度与表 1 的 NC/NI 限定方式保持不变；统一参考文献仍为 52 条（本轮无新增文献，S12 为初等代数反解），自动检查每条均被实际引用。

## 评审第五节证据边界（全部保留）

1. 两套确定性目标提取规则的一致性≠独立人工目标验证（pending）。
2. 合成 attendance fixture≠真实测量工具已验证（pending；§1.4.1 为未来方案）。
3. AND 规则可能增加操作性假阴性；独立验证集的敏感度/特异度与臂间差异报告是解锁前义务。
4. S2/S2d 匹配 fixture 只证明两臂可执行，不识别结构效应。
5. 真实匹配实验、独立时间外语料、第三方复现与人类数据仍是未来有效性主张的必要证据。

本回复与自动测试同样不能替代主稿所声明的独立人类数学复审。

## 验证摘要（作者侧）

- 治理 18/18；纵向执行器 **20/20**（新增 6 项）；目标构造 4/4；消费口径 6/6；冻结重放 20/20；金融 3/3；数学/SAP 13/13。
- 评审三个针对性反例复测：NaN→unknown、inf/1.5→unknown、delivered-未-selected→修改前拒绝（0 记录、0 扣减）。
- 回顾性 R5 单源核对 MATCH；发布审计、20 页级 PDF 文本层/布局检查、arXiv XeLaTeX 0 缺字形、干净公开副本验证与无 Git PATH 金融复现见 `tools/audit_v114_report.json`、`tools/clean_verification_v1.14.json` 与 REPRODUCIBILITY。
- 字符串检查不替代语义一致性验证；本轮另行人工核对了 §3.2 元组闭合、S12 推导方向与 R5 生成断言。