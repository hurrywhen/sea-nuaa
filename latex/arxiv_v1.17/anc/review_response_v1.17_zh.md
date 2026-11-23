# SEA v1.17 综合评审意见逐条回复与修改说明

**评审对象：**v1.16.0，公开 main 提交 `3f6a5e0452d845615ed22b6bb419972db8248202`。  
**本次修订：**v1.17.0 candidate / prerelease。  
**修订性质：**按“小修后再审”结论修复两个执行器边界反例，并完成全部可代码化 P1 统计改进。标题、摘要、证据矩阵和回顾性结果定位保持不变；不新增虚构人类数据、真实测量验证或系统有效性结论。独立人工数学复核、独立目标/attendance 仪器验证、第三方复现、真实匹配实验、公共预注册和人类数据仍诚实列为 pending。

## 作者决定（已向作者询问并确认）

1. **期次模型：严格连续期次。**每个控制实例只接受 `period == next_period`，重复、倒退、跳期均拒绝；连续性切换沿共享历史递增，完全重置的新实例从 0 开始。不引入 period/attempt 双层模型，也不允许跳期。
2. **修改范围：P0＋全部可代码化 P1。**本轮同时完成零完成结构化诊断、手工协方差联合半正定检查、分层小样本区间和完成率不确定性。独立人工复核与真实测量验证不属于可编码事项，继续 pending。

## P0-1/P0-2 重复期次绕过冻结切换边界

评审反例成立：v1.16 的 `completed_periods = len(self.period_results)` 统计的是结果行数，`run_period()` 未限制 period 唯一性和递增性，因此两次 period 0 可以满足 `switch_after_period=1`。

### 修复

- **真实期次而非结果行数。**`next_period` 现在是只读 property：核验已提交结果序列恰为 $0,\ldots,N-1$，然后返回 $N$。它不是公开可写时钟，也不是对任意结果列表直接取 `len`。序列被手工破坏为重复、倒退或跳期时抛出完整性错误，不能用于切换。
- **执行规则。**`run_period(period, plan)` 在任何候选、预算、资源预检或审计操作之前要求 `period` 是非布尔整数且等于 `next_period`；只有成功提交结果后才扩展序列。重复、倒退、跳期、负数、布尔、浮点和字符串 period 均在任何状态变化前拒绝。
- **切换/重置。**`continue_with_target_registry()` 使用 `next_period == switch_after_period + 1`；连续性切换共享结果序列，所以 predecessor/successor 的时钟不会漂移；完全重置的新实例结果序列为空，从 0 开始。切换本身、目标写入和回滚不额外推进 period。
- **算法与形式材料。**主稿 §3.1–§3.4、Algorithm 1、表 3/表 6/表 7、补充材料 SA.0、协议 §1.3 和复现说明均明确上述规则。

### 对抗性测试与演示

新增并通过：

- `test_duplicate_period_cannot_advance_frozen_switch_boundary`：声明 `switch_after_period=1`，重复 period 0 后仍只有真实期次 1，切换继续以 `switch_timing_mismatch` 拒绝；只有真正完成 period 1 才能切换；
- `test_regressed_period_is_rejected_before_mutation`；
- `test_skipped_period_is_rejected_before_mutation`（同时覆盖非整数输入）；
- `test_old_period_after_switch_is_rejected_before_mutation`；
- `test_period_clock_is_read_only_and_shared_history_cannot_drift`：手工赋时钟不能绕过早切换，sealed predecessor 与 successor 的共享历史时钟一致，损坏的重复结果序列不能通过完整性检查。

协议演示新增独立 duplicate-period probe，并在 `duplicate_period_switch_rejection_events` 中保留“重复后切换仍过早”的拒绝记录。无效 `run_period` 本身在预检前拒绝，不追加任何记录；被拒绝的规范切换尝试仍按既有规则只追加一条拒绝审计记录，资源零扣减。

## P0-3/P0-4 零完成测量的诊断结果不正确

评审反例成立：v1.16 在 paired records 为空时调用 `_binary_validation_rates()`，抛出 pooled truth-class 异常；`total_complete=0` 时又把 share shift 填为 0，可能误读为完成子集完全具有代表性。

### 修复后的返回语义

`transportability_stratified_diagnostics()` 现在先独立完成完成率诊断，不再让 pooled error-rate 异常阻断输出：

- `completion_rate = 0`，总体和分层完成率的 Wilson 区间仍返回；
- assigned、completed（显式 0）和 unknown 计数全部保留；
- 每个 stratum 的 completed-subset share shift 及 `max_share_shift` 均为 `None`，状态为 `not_estimable`，原因是 `no_completed_measurements`；
- `sensitivity_specificity_estimable=False`、`error_rates_estimable=False`；
- `completion_warning=True`、`representativeness_warning=True`、`reason="no_completed_measurements"`；
- sensitivity、specificity、不可估计异质性分别为 `None`，不写成 0；
- 每个 assigned stratum 即使完全 unknown 也保留在输出中。

单真值类不再抛异常：可估计的一侧仍返回点估计、样本量和区间，另一侧为 `None` 并给出 `no_truth_positive_units` 或 `no_truth_negative_units`。仅一个 stratum 有完成测量、完全 unknown stratum、部署集缺失 stratum、无共同 strata 均保留结构化原因；无共同 strata 时 `max_completion_rate_gap=None`。

新增测试：`test_stratified_zero_completion_returns_structured_not_estimable`、`test_stratified_single_truth_class_is_not_estimable_not_exception`、`test_stratified_single_completed_stratum_and_missing_stratum_remain_visible`，并覆盖 validation/deployment 同时零完成和省略 test/truth 字段的 unknown-only 记录。

## P1-1 手工协方差输入的联合合法性

仅检查 S12 梯度方向上的最终标量方差不足以证明三个输入可联合成立。`completed_measurement_transport_delta_method` 现在额外检查完整 $3\times3$ 协方差矩阵半正定：

- 零方差坐标的所有协方差必须严格为 0；
- 对正方差坐标计算归一化 pairwise 相关，逐次除法避免原始方差乘积上溢/下溢；
- 三个方差均为正时检查相关矩阵行列式；
- 仅允许无量纲 $10^{-12}$ 的舍入容差，其他大方差坐标不能掩盖小方差子块非法；不投影、不截断、不修复输入；
- 最终标量方差仍必须有限且非负，使用 `math.fsum` 累加九项。

测试包含：所有 pairwise 二阶条件通过但行列式为负且 S12 方向方差仍为正的联合反例；大方差掩盖小子块、零方差非零协方差、极端尺度、全零方差及合法奇异 PSD 边界。联合/聚类 bootstrap 仍是共享或聚类验证单元的优先替代方法，不被手工 PSD 检查取代。

## P1-2 分层小样本区间与完成率不确定性

- sensitivity、specificity 和 completion rate 均报告分子、分母、样本量、独立可估计状态和 **95% Wilson score 区间**；$n=0$ 返回 `None`，$0/n$、$n/n$ 不使用退化 Wald 区间。
- Wilson 区间是单位级、边际二项近似，不称 exact，不做聚类调整或多层同时校正；两个边际区间的笛卡尔积不是 S12 联合置信区域。聚类设计仍须设计一致的 cluster 方法，联合传输仍用完整协方差或联合/聚类 bootstrap。
- 异质性按 sensitivity/specificity 分别计算：每个指标至少需要两个可估计 strata 和可估计 pooled rate；单层与 pooled 的平凡零偏差不被解释为“跨层异质性为 0”。只有一侧可估计的 stratum 仍可参与该侧诊断，不再整层丢弃。
- 新增 Wilson (1927) 一条方法文献，已于 2026-11-23 通过 Crossref 核验 DOI `10.1080/01621459.1927.10502953`；统一参考文献表现为 53 条。

## P1-3 独立人工复核与真实测量验证

仍诚实列为 pending。自动测试、AI 辅助推导和作者侧干净副本重跑不能替代独立人类数学复审，也不能替代独立目标/attendance 仪器验证。后续复核重点包括严格真实期次、共享历史/重置时钟、S12 协方差展开与 PSD 条件、零完成语义和 Wilson 区间适用条件。真实验证必须按协议 §1.4.1 使用独立盲法参考集，不能继续只扩合成 fixture 后宣称完成。

## P2 编辑性事项

保持当前标题、摘要和证据矩阵，不增加防御性效果叙述。新增内容仅用于解释两项边界修复及其统计适用条件。tagged PDF 和 v1.17 专属 DOI 仍 pending。内审 PDF 实测 22 页，表 6/表 7 共同完整位于最后一页；发布审计（含 PDF）157/157 通过。arXiv XeLaTeX 同为 22 页、缺字形 0，733/733 附件哈希通过；无 `.git` 脱敏副本 19/19 组验证通过。上述数字均来自本次机器报告，不复制 v1.16 结论。

## 保留与边界

v1.16 已确认的拒绝状态效应、冻结切换时机、声明完整性哈希、完全重置白名单、单线控制、S12 协方差/联合 bootstrap/敏感性网格和回顾性证据定位全部保留。执行器源测试现为 **49 项**；测试数量本身不作为严谨性或有效性的证明。新增结果仍是条件化框架、合成接口与统计方法工件，不支持系统有效性、真实测量效度或人类层面结论。
