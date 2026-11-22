# SEA v1.16 综合评审意见逐条回复与修改说明

**评审对象：**v1.15.0，公开 main 提交 `4f7c3aa7a55c5e9750834ec58d75f92cae717d03`。
**本次修订：**v1.16.0 candidate / prerelease。
**修订性质：**按评审"小修后再审"结论完成三项精确修订（拒绝日志状态效应、冻结切换时机与重置例外、复现命令），并把可代码化的 P1 统计/实验细节一并落实。不新增虚构人类数据、真实测量验证或部署有效性结论；评审确认已解决的外生协议授权、单线控制生命周期、S12 限定、执行器鲁棒性与材料一致性全部保留。独立人工数学复审、独立测量验证、第三方复现、真实匹配实验与人类数据仍诚实列为 pending。

## 作者决定（评审要求二选一事项，均已向作者询问确认）

1. **切换时机冻结机制：冻结期次＋转移时强制校验。**新增 `protocol_switch_timing`（版本→`switch_after_period`），在读取任何处理臂结果前冻结；连续性转移仅在已完成期次数恰为声明边界加一时接受，过早/过晚/读取结果后篡改声明均拒绝。不采用"同时冻结队列窗口"的更严格变体（避免改变纵向演示语义）。
2. **完全重置例外：保留例外＋预声明重置白名单。**保留当前代码行为并显式化：新增 `protocol_reset_targets` 事前白名单；fork 校验白名单成员资格；新实例一律生成独立单版本日程；主文写明"连续性转移严格沿日程向前；完全重置是独立控制实例的例外"。不采用"不允许例外"变体。
3. **P1 范围：本轮完成全部可代码化 P1。**协方差/联合 bootstrap、切换时机负例、分层可迁移性/完成代表性诊断均落地为代码＋测试＋补充材料＋协议字段；独立人工数学复审继续 pending。

## P0-1 "拒绝日志＋零状态变更"与 SAP 状态定义不一致

评审正确：主稿 §3.2 把审计账本 \(L_t\) 纳入状态 \(x_t\)，而 `_reject_switch()` 追加一条审计记录，故"整个 SAP 状态零变更"不成立。这是形式措辞问题，实现行为不变。已统一为评审建议的精确表述：

- **主稿 §3.3/§3.4、§1.3、补充材料 SA.0、协议 §1.3**：改为"拒绝时登记、目标存储、预算与活动路径均不变更，**仅向账本追加一条拒绝审计记录**（账本本身是状态的一部分），资源零扣减"。删除全部 "zero state mutation/零状态变更" 笼统措辞。
- **代码 payload 拆分**（`_reject_switch`）：移除 `state_mutated=False`，改为
  `registry_objective_budget_mutated=False`、`active_path_mutated=False`、`rejection_audit_record_appended=True`、`resources_spent=0`。
- **测试与演示**同步断言新字段；`test_non_family_registry_switch_is_rejected_with_record` 仍断言拒绝后审计记录数 +1，与"仅追加一条拒绝记录"自洽。

## P0-2 外生日程冻结切换时机

评审正确：原日程只有版本顺序，调用者可在任意周期间切换，削弱外生性。已新增冻结时机机制：

- **fixture**：`protocol_switch_timing={"targets-v2":0}`（演示在周期 0 之后、周期 1 之前切换）。加载期校验：多版本日程必须声明时机；时机键恰为日程后继；值为非负整数且沿日程严格递增。
- **执行器**：`continue_with_target_registry()` 在族/哈希/日程校验后检查 `len(period_results)==switch_after_period+1`，否则以新原因码 `switch_timing_mismatch` 拒绝（payload 含 `declared_switch_after_period` 与 `completed_periods`）。
- **声明完整性**：新增 `_declaration_hash()`/`_assert_declaration_intact()`，把族/日程/时机/白名单/冻结内容一并哈希；读取结果后任何修改使哈希失配，以 `protocol_declaration_tampered` 拒绝（转移与 fork 均校验）。
- **负例测试**：`test_switch_timing_is_frozen_and_enforced`（早/晚拒绝＋边界接受）、`test_declaration_tampering_after_results_is_rejected`（时机/日程/族/白名单/冻结内容五种篡改）。演示新增早/晚/篡改三个负例（独立控制实例，拒绝记录单列 `timing_and_declaration_rejection_events`）。
- **协议**：§1.3 将 `switch_after_period` 与重置白名单列为公共预注册必要字段，明确"读取任何处理臂结果之前冻结、不能随中途表现调整"。

## P0-3 完全重置的日程例外与主文统一

评审正确：原 fork 允许父日程外族成员成单版本日程，主文却笼统写 append-only forward。已按"保留例外＋显式声明"统一：

- **代码**：fork 新增白名单校验（`reset_target_not_declared`）；新实例日程一律 `[version]`、时机清空 `{}`（不再沿用父日程后缀）。
- **fixture**：`protocol_reset_targets=["targets-v1","targets-v2"]`（含回退到 v1）。
- **主稿 §3.2/§1.3、补充材料 SA.0、协议 §1.3**：写明"连续性转移严格沿日程追加向前；完全重置是独立控制实例的例外，可选择事前声明允许的重置目标（含回退版本或父日程外族成员，前提是已声明），生成全新独立单版本日程；回退重置是新控制实例，不是对已封存父路径的登记回滚"。
- **测试/演示**：`test_full_reset_requires_declared_reset_target`（未声明拒绝＋缺省=全族）、`test_backward_full_reset_is_new_instance_with_single_version_schedule`（回退新实例、独立账本/预算、父路径封存且登记版本不变、无后继日程）；演示新增 v2→v1 回退重置链。

## P0-4 复现文档脚本名错误

`docs/REPRODUCIBILITY_v1.15.md:142` 误写 `make_v114_manifest.py`。v1.16 复现文档第 6 节已更正为 `tools/make_v116_manifest.py`，并核对同页环境变量（`SEA_RELEASE_ID/SEA_TARGET_TAG=v1.16.0`）、标签名与目标提交说明全部指向 v1.16。发布脚本 `publish_v116.py` 调用 `make_v116_manifest.py`。发布审计新增字符串检查防止回归。

## P1-1 相关输入的协方差/联合 bootstrap

- **delta-method**：`completed_measurement_transport_delta_method` 新增 `cov_se_sp/cov_mz_se/cov_mz_sp` 三个协方差项，完整二阶展开；零协方差标记 `input_independence_assumed=True`，非零标记 False；协方差导致负方差即拒绝（不静默修正）。
- **联合/聚类 bootstrap**：新增 `completed_measurement_transport_joint_bootstrap`，成对重抽验证记录并联合重估 se/sp（保留同验证集依赖），`cluster_key` 整群重抽；非正 Youden 分母或丢失 truth 类的重抽样本计数报告（`degenerate_replicates`），不静默丢弃；m^Z 来自独立部署样本时保持固定并声明其不确定性未建模；固定种子可复现。
- **测试**：`test_s12_delta_method_covariance_terms`、`test_s12_joint_bootstrap_preserves_dependence_and_is_deterministic`。补充材料新增 "Dependent inputs" 段（完整协方差公式）；协议 §1.4.1 第 5 项强制"同验证集/聚类不得默认独立"。

## P1-2 误差可迁移性与完成子集代表性的可检验化

- 新增 `transportability_stratified_diagnostics`：验证集分层 se/sp、各层相对合并估计最大绝对偏差＋异质性阈值预警、缺 truth 类层"不可估计"标记、分层完成率、完成子集层份额偏移、提供部署记录时的分层完成率差距与单侧缺失层清单。明确"诊断支持但永不证明可迁移性"。
- 新增 `completed_measurement_transport_sensitivity_grid`：预注册网格全评估，非正分母单元报"不可容许"，返回传输范围与越出 [0,1] 比例，不静默跳过/截断。
- **测试**：`test_transportability_stratified_diagnostics`、`test_s12_sensitivity_grid_reports_inadmissible_and_range`。补充材料 transportability 段与协议 §1.4.1 第 4/6 项同步，把文字假设转化为分层/敏感性强制报告。

## P1-3 切换时机不可随结果改变的负例/协议检查

见 P0-2：早/晚/篡改三类负例＋声明完整性哈希＋协议预注册字段，均已落地为代码与测试。

## P1-4 独立人工复核

仍诚实列为 pending。自动测试与本评审不能替代独立人类数学复审；主稿标题页与证据矩阵继续声明 "independent human mathematical review remains pending"，重点复核外生转移、单线生命周期、公式 (6) 与 S12（含新增协方差/bootstrap/分层诊断）。

## P2 编辑性事项

保持当前标题、摘要与证据矩阵定位，不增加防御性篇幅。分页经目检维持 21 页：参考文献填满参考文献页，表 6/表 7 整页容纳于末页、无孤儿行。tagged PDF 与 v1.16 持久版本标识（DOI）仍列为后续 pending。

## 保留与边界

评审确认的优点全部保留：外生协议路线（族 allowlist＋冻结内容＋有序日程＋非族/篡改/越序/sealed 负例）、单线控制生命周期（sealed＋唯一共享预算/历史/账本＋fork 封存父路径）、S12 限定（完成测量部分、条件稳定性、完成子集代表性、误差不确定性传播、近零分母预警、越界不截断）、执行器鲁棒性（无效遥测→unknown、validated 强制字段）、回顾性表格单源与队列归因。系统有效性、真实测量效度与人类层面结论仍须等待后续独立实验验证；本轮不声称任何新增有效性证据。
