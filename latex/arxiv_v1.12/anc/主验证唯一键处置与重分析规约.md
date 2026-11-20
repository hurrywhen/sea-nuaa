# 主验证唯一键处置与重分析规约（v1；冻结于 2026-11-03）

> 本规约适用于四家族、80 个带种子配置、292 个 `llm_replay_*.jsonl` 分片的**受控唯一键重分析**。旧结果已经被查看，因此本工作不是 prospective preregistration，也不得冒称完全盲于旧结果的新确证试验。规则在运行新的结果敏感重算脚本前冻结；所有场景一次性报告，不选择有利场景。
>
> 主状态：`CONTROLLED_UNIQUE_KEY_REANALYSIS__WITHIN_CORPUS_EXPLORATORY`。run 分层、run bootstrap 或 run-cluster 翻转均不能消除 run 内相关、共享语料、共享标签、上游 digest、模型记忆或缺失非随机。

## 1. 输入与不可变边界

1. 唯一输入为 `sim/pilot/results` 顶层符合现有审计 tag 规则的 292 个 JSONL；归档的作废协议和 F 家族不进入分析。三家族文件是另一项实验，不纳入本规约。
2. 期望网格由既有 80-run 清单固定：O/C 各 30 run、Q/G 各 10 run；每 run 为 `agent=0..29 × sim_day=0..29`，共 72,000 个键。唯一键为 `(family, run, agent, sim_day)`。
3. 原始 JSONL 只读，不覆盖旧 `main_validation_analysis.*` 或完整性审计。新结果写入独立目录 `sim/pilot/results/frozen_reanalysis_v1/`。
4. 重算输出必须包含：292 输入文件的相对路径、大小、行数与 SHA-256；本规约快照及 SHA-256；分析脚本 SHA-256；Python/NumPy 版本；逐键处置账本；逐 run 指标；全部场景结果。
5. 原始记录没有 `attempt/timestamp/status/exit/retry` 等可验证仲裁字段。文件行号、`day`、文件 mtime、任务日志和完成旗标不得用于推断哪条冲突记录是“正确 attempt”。`reason/raw_consume` 只作诊断，不用于挑选结果。

## 2. 记录、参数臂与缺口

1. 沿用 V-3：`picked` 非空为有效记录。空 `picked` 不进入有效重复组。
2. 对每个 `(run,sim_day)`，检查全部记录中的 `hits_param,n_crit,value_param` 是否分别唯一；若唯一，则作为该日的规范参数值。若任一不唯一，脚本必须失败而不是仲裁。
3. 86 个无有效键固定区分为：
   - `EMPTY_ONLY`：当前快照只有空 `picked`，预期 56 键；
   - `NO_SURVIVING_ROW`：当前快照无任何记录，预期 30 键。
   “无记录”只描述当前快照，不推断历史从未调用。另有 101 条空记录与有效记录共享键，不属于 86 缺口。
4. 主点估计采用 available-resolved-case：86 键不当作零、不按名义 900 强行补分母、不删除整个 run。参数臂字段可按第 2 条恢复；LLM 结果保持缺失。逐 run 必须报告期望数、已解析数、冲突数、两类缺口和覆盖率。

## 3. 主规则 A：充分统计量一致才解析

对唯一键 \(k\) 的有效记录集合 \(R_k\)，对统计量 \(m\) 定义充分统计值集合 \(U_{k,m}=\{m(r):r\in R_k\}\)。若 \(|U_{k,m}|=1\)，使用唯一值；若 \(|U_{k,m}|>1\)，该键对 \(m\) 标为 `UNRESOLVED_CONFLICT` 并在主点估计中缺失。不得复制首行或末行。

各指标分别判定：

- recall 与 Δrecall：`(hits_llm,n_crit)`；`hits_param` 使用第 2.2 条规范值。结构性预期为 341 个冲突键、71,573 个可解析键。
- Δvalue：`value_llm-value_param`；结构性预期为 1,238 个冲突键、70,676 个可解析键。
- McNemar 配对符号：`sign(hits_llm-hits_param)`；结构性预期为 296 个冲突键、71,618 个可解析键。

这些计数是完整性结构，不是结果效应。不同指标的分析人口不同，必须同时报告共同 cohort 场景 B。

## 4. 预定场景矩阵

所有场景均重算 recall、Δrecall、Δvalue 和 run-level CI；McNemar/CMH 仅在整数命中和配对符号有定义的口径计算。所有场景完整报告，不按效应或 p 值选择。

| ID | 规则与用途 |
|---|---|
| A `metric_resolved` | 第 3 节主规则；86 不插补。 |
| B `common_cohort` | `(hits_llm,hits_param,n_crit,value_llm,value_param)` 五字段一致才保留；预期 70,676 键。用于共同分析人口。 |
| C `strict_singleton` | 每键恰有一条有效记录才保留；预期 70,306 键。最强来源保守性。 |
| D `audit_six_consistent` | 审计六字段（五字段加 `picked`）一致才保留；预期 70,525 键。 |
| E `attempt_mean` | 每个有效唯一键内对 attempt 数值等权取均值，每键只计一次；预期 71,914 键。它估计“已记录 attempt 平均”，不是恢复单次运行真值。分数化命中不做精确 McNemar/CMH。 |
| F00–F04 `hash_salt00..04` | 每键按 `SHA256("SEA-80run-dedup-v1\0"+salt+family/run/agent/sim_day/source_file/source_line)` 最小者选一条；salt 固定为 `salt00` 至 `salt04`。不哈希任何结果或理由字段。五种盐全部报告；这只是结果盲机械敏感性，不是找出真值。 |
| G `empty_only_zero` | 在 A 基础上，仅把 56 个 `EMPTY_ONLY` 键的 LLM hits/value 置零；30 个无记录键仍缺失。表示已观察失败即零消费的运维情景。 |
| H `all_gap_zero` | 在 A 基础上，把 86 个缺口全部按 LLM 零消费处理。它改变 estimand，只是保守运维情景，不得冒充主结果。 |
| I `favor_param` / `favor_llm` / `unresolved_tie` | 在 A 已解析键之外，所有冲突及缺口分别按协议允许的最不利/最有利/平结局赋值。用于方向与符号敏感性，不是点估计。 |
| J `lower_value` / `upper_value` | 在 A 之外，冲突与缺口的 LLM recall 分别取 `0` / `n_crit`；LLM value 分别取 `0` / 当日全部论文中最高三项 `log1p(cit)` 之和。后者是比 digest 更宽的协议上界。用于 recall、Δrecall、Δvalue 部分识别端点。 |

I 中参数侧使用第 2.2 条规范值： favor_param 使用 `hits_llm=0` 对应符号，favor_llm 使用 `hits_llm=n_crit` 对应符号，unresolved_tie 将未解析符号置平。I 不宣称穷举得到最小或最大 p 值；只报告三个预定符号情景。

## 5. 点估计与区间

1. 每 run 在其已解析键集合上计算：
   \[
   R^{LLM}_r=\frac{\sum hits_{LLM}}{\sum n_{crit}},\qquad
   R^{param}_r=\frac{\sum hits_{param}}{\sum n_{crit}},\qquad
   \Delta R_r=R^{LLM}_r-R^{param}_r,
   \]
   \[
   \Delta V_r=\operatorname{mean}(value_{LLM}-value_{param}).
   \]
2. 家族主估计为**等权 run 均值**；另输出 pooled agent-day 加权估计作敏感性，不能替换主口径后只报一个。
3. run-level CI：以整个 run 为重抽样单位，percentile 95%，10,000 次，seed=42。所有场景使用相同 run 数与种子以复用重抽样索引。对 \(R^{LLM}\)、\(R^{param}\)、Δrecall、Δvalue 均输出区间。
4. CI 只描述 run 间变异，不包含仲裁/缺口不确定性；后者由场景矩阵和 J 端点承担。Q/G 各 10 run，区间只作小样本探索描述。
5. 当前四家族单一 honest=0.241 不是逐 run 同 digest 配对臂：主重放 proxy seed 随 run 改变，而旧 honest 重建固定 seed=99。故本规约不把 0.241 变成新的 80-run 配对推断，只保留为固定描述参照。

## 6. McNemar、CMH、多重校正与 run-cluster 敏感性

1. 在主规则 A 下，每 run 计算 `b=#(hits_llm>hits_param)`、`c=#(hits_llm<hits_param)`、其余为 tie；同键不得重复贡献。家族内用双侧精确 McNemar。
2. 四个家族 McNemar 构成唯一 BH(4) 检验族。CI 不做 BH，也不由 CI 跨零反推未校正 p 值。pooled CMH 是预先声明的描述性汇总，不加入或退出校正族以迎合结果。
3. 80-run 汇总同时报告：
   - 未校正式 \(\chi^2=(B-C)^2/(B+C)\)；
   - 修正的连续性校正式 \(\chi^2=\max(0,|B-C|-1)^2/(B+C)\)，`B=C` 时必须为 0；
   - 旧实现 `(abs(B-C)-1)^2/(B+C)`，仅用于前后可比。
   三者均只是名义 agent-day 独立近似，不作跨语料校准错误率。
4. run-cluster 符号翻转统计量为 \(T=\sum_r(b_r-c_r)\)。对每个 run 整体翻转 LLM/param 标签，使用双侧 \(|T|\)。Q/G 精确枚举 \(2^{10}\)；O/C 和 80-run 汇总用 100,000 次 Monte Carlo，seed=42，报告 `(1+extreme)/(1+N)`。这检验 run 间交换对称性，不证明 run 内独立。
5. E 不做精确 McNemar/CMH；I/J 只作情景描述，不进入 BH(4)。只有 A 的四个家族精确 McNemar 进入 BH(4)。

## 7. 报告与解释纪律

1. 输出 `summary.json`、`REPORT.md`、`run_metrics.csv`、压缩逐键账本、输入 manifest、规约快照和环境信息；默认 stdout，只有显式 `--write` 才写新目录，覆盖需 `--force`。
2. 旧 73,547 行结果永久标为 `LEGACY_EXPLORATORY_NOT_DEDUPLICATED`，不得改名为新冻结主结果。新结果标为 `CONTROLLED_UNIQUE_KEY_REANALYSIS__WITHIN_CORPUS_EXPLORATORY`，不是 prospective preregistration 或跨语料确证。
3. 报告全部场景，不选择“最好看”的 salt、仲裁或缺口规则。主结论必须同时说明 A、B、E、F、G–J 是否同向，及哪些结论对规则敏感。
4. 缺失与冲突不能解释为随机；available-case 可能选择偏倚。attempt 均值是不同 estimand；哈希不是历史真相；零消费是运维情景；J 是端点而非新点估计。
5. 即使完成本重算，时间外无泄漏复制、point-in-time 特征、记忆消融、S2d/S4/S5、公共层独立确认、HP-0 与后续人类研究仍未完成。
