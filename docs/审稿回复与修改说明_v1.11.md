# SEA v1.11 复审意见逐条回复与修改说明

**复审对象：**v1.10.0，公开提交 `817de9839d4bcc9446d39e631b14ab1c387ad0bd`。  
**本次修订：**v1.11.0 candidate / prerelease。  
**修订性质：**按“小修后再审”意见进行数学措辞、历史口径、未来测量协议、复杂度和文本结构修订；不改变条件性组件／治理接口／证据审计路线，不新增或虚构端到端有效性、人类数据或实际消费观测。

## 1. 修正 \(17/22\) 与 75% 的比较错误

已接受并修正第 3.4 节的明确措辞错误。新表述为：实现值 \(17/22\approx77.27\%\) **高于**两步贪心的 75% 最坏情况保证，但仍低于联合最优值 22。因此没有违反贪心近似保证，同时“贪心监测＋后续最优投递”仍非联合最优。

`tools/reproduce_v110_sap.py` 的数值工件保持 17、22 和 0.75 不变；`tools/audit_v111.py` 新增语义检查，明确禁止恢复 `does not exceed` 的错误句子。自动审计仍只作实现一致性检查，不替代人工数学复审。

## 2. 历史分析彻底取消不准确的 ITT 命名

主文、表题、证据状态和新生成结果统一采用：

- `ALL_EXISTING_RECORD_MEAN_ZERO_EMPTY`：**designated retrospective descriptive caliber**；
- `METRIC_RESOLVED_ZERO_EMPTY`：冲突拒绝的 zero-empty 回顾性口径（冻结 G）。

“Primary historical robustness summary”已改为“Designated retrospective descriptive caliber”。历史分析不再以 ITT 为名称或免责声明式标签；30 个无记录键仍缺失，空选择仍不能区分合法 abstention 与执行失败，记录均值仍不恢复历史真实单次运行，`picked` 仍只表示 selected proxy。

两个旧标识仅在 `sim/sea_pilot/audit_v110_consumption_caliber.py` 的 `LEGACY_CALIBER_ALIASES` 中作为**输入兼容别名**保留；summary、CSV、72,000 键 ledger 和报告均只输出新名称。重新生成后，320/320 条 run-metric 行在统一标签后逐字段一致，未改变数值、冻结输入或 17 情景结果。新增 5 项回归覆盖别名、输出字段、ledger、未来 schema 和数值稳定性。

## 3. 闭合未来 attendance 测量和主要缺失规则

主文第 8.2 节与 `docs/MINIMAL_VALID_EXPERIMENT_v1.11.md` 第 1.3–1.4 节现规定：

1. **按语料域注册工具。**结果解锁前冻结 `instrument_registry`，包括工具版本、原始事件 schema、判定阈值、验证集与代码哈希、测量误差、替代工具和敏感性阈值。
2. **数字文本。**默认主要工具是有效阅读事件（聚焦可见、有效参与时长、内容覆盖）与内容相关主动确认或任务相关操作的组合；打开、点击、停留或滚动本身不构成实际消费。
3. **金融／决策任务。**任务操作须与内容哈希绑定，例如批注、保存到决策工作区或引用到预声明决策输入；仅下载或无内容引用的点击不算 attendance。
4. **机器到机器私域。**完整内容哈希进入声明的下游任务上下文并被后续任务操作引用，可称 machine consumption；必须经合成 fixture 验证并与人类注意分开，不作人类学习或福利外推。
5. **阈值验证和盲法。**阈值由独立测量验证集和盲法参考标注确定，在比较结局解锁前冻结；完整报告替代工具和阈值敏感性。attendance 标注、 adjudication、测量验证和结果审计对处理臂、模型家族和比较结局盲法。
6. **失败即 unknown。**工具缺失、崩溃、遥测无效或评审不能判定时，原始 attendance 为 `unknown`，不自动记为已消费或未消费。

唯一主要结局改为**全分配失败复合的确认实际消费加权遗漏**：只有有效阳性 consumption 测量记成功；明确未消费、合法 abstention 和终端 unknown 均按主要规则记遗漏。合法 abstention 是处理策略结局，不是缺失；解析、运输、执行和仪器失败不得在事后追认为合法 abstention。原始 `unknown` 不因主要结局编码而被改写成观测到的未消费。

unknown 全部按已消费、冻结的处理臂感知逆概率加权和另行论证的预注册多重插补只作敏感性；complete-case 只作描述。主规则在结果解锁前固定，不能看到结果后切换。文中同时明确：失败复合编码对单臂遗漏水平保守，但不保证两臂差值方向保守，因此须按臂×阶段×原因公开缺失率。

未来 `/v2` JSON Schema 将 `attended` 统一为唯一终端 attendance/consumption 事件，并记录仪器版本、阈值、验证、盲法、证据指针及 `outcome_protocol`。历史数据未按该 schema 回填。

## 4. 限定 Algorithm 1 的复杂度适用范围

主文第 3.6 节不再把 \(O(n\log n+|E|)\) 写成整个 guarded SAP step 的复杂度。现分解为：

- 排序：仅候选引用的比较排序为 \(O(n\log n)\)，不含评分；
- 链接与目标记账：定义 \(L_\kappa=\sum_i|\kappa(x_i)|\)，遍历已计算关联并初始化目标账本为 \(O(L_\kappa+|E|)\)，关联物化内存、流式替代和 \(C_{\mathrm{link}}\) 另述；
- 资源可行子集选择：另记 \(T_{\mathrm{select}}\)。精确 m 子集枚举检查 \(\binom nm\) 个子集，普通贪心、背包和部分枚举各按具体算法报告，不能继承排序界；
- 审计：canonicalization/hash chaining 随 \(B_{\mathrm{audit}}\) 字节数线性增长，持久化存储另计；
- 更新、评分和模型调用：以 \(C_{\mathrm{score}}\)、调用、token、费用、延迟和重试日志测量，不能由 \(n\) 推断。

文中给出的总量表达式只是这些实现成本之和的会计模板，不是通用运行时间定理。

## 5. 消除唯一主要结局与多个主要结局的矛盾

未来协议现在只有：一个主要比较（SEA 对同模型原始流端到端筛选）和一个主要结局（上述失败复合加权遗漏）。协议第 5.1 节已改为“唯一主要结局先检验；主要结局与分层次要结局采用预先声明的 gatekeeping”。RAG、福利推荐、决策价值、效率和消融均为次要分析；不存在多个主要结局。历史“designated”描述口径也不与未来 primary outcome 混称。

## 6. 补充零概率历史处理

SAP 初始联合分布条目已删除“所有条件历史律均已定义”的过强推论。命题 3.1 的证明现在：

- 先固定对每个非空可行行动集均有正概率的参考行为策略 \(\beta\)，再在其正概率历史／行动支持上定义条件奖励、下一观察核和终端条件成本，避免以待求最优策略作循环条件化；
- 对在 \(\beta\) 下为零概率、因而任何策略均不可达的历史不要求后验，指定任意固定可行动作和有限延续值；
- 明确这些指定不影响正概率可达历史上的值和最优性，再以有限集最大值和固定平局规则完成递归存在性证明。

该修改是形式完备性修补，不扩张为连续空间定理、可计算算法或低维信念充分性结论。

## 7. 主文压缩与重复内容整理

- 在线阈值边界归纳、EIG 熵证明和 KL 子集选择证明移至 `docs/SUPPLEMENT_FORMAL_AND_SECONDARY_v1.11.md` 的 SA.1–SA.3；主文保留命题、适用域和指针。
- Rule A、strict-singleton 和 17 情景范围表移至同一补充附录 SB.1–SB.3；主文保留口径对照表、全已存在记录主表及情景符号结论。
- onboarding declaration 表移至 Supplementary Appendix SC；主文由 15 张编号表减为 11 张，保留 3 张图和 11 个编号公式。
- 已移至规范补充材料的人类测量／议程段落及其 9 条孤立参考文献从主文删除；相关论证仍在补充材料中，主文参考文献由 60 篇减为 51 篇。
- Data and Code Availability 删除整段命令，仅保留仓库、工件入口和复现文档指针；完整命令集中在 `docs/REPRODUCIBILITY_v1.11.md`。
- 摘要、贡献、限制和结论合并重复证据边界；附录删除已移至规范补充材料的 Jaccard 和 agenda-overlap 条目。
- PDF 增加 Wen Hu、Xutong Wang、Ya Yu 的 Author 元数据，标题和页面布局在发布检查中重新核验。

## 8. 发布工件与溯源

`tools/make_v111_manifest.py` 新增 `target_tag`、`target_commit`、`target_tag_object`、`target_commit_verified_against_tag` 和 `provenance_mode`。为处理 Git 提交不能包含自身哈希的事实，发布流程为：

1. 构建并提交候选内容，创建 annotated tag；
2. 在干净工作树中解引用该标签，生成目标提交明确的最终清单；
3. 仅在 main 追加 provenance 清单提交，不移动标签；
4. 非强推 main 和标签到 GitHub/Gitee，再创建 prerelease 发布页。

因此 main 可以比标签多一个清单提交，最终清单的目标提交与标签解引用提交一致，不再只依赖“上一提交＋dirty tree”。

## 9. 验证与仍未完成事项

已完成发布前重跑：13/13 项数学/SAP 回归；42/42 项治理、重放、金融和消费口径回归；四类数据审计；112/112 项 v1.11 稿件／工件审计；无 `.git` 公开副本的 17/17 组验证及无 Git 可执行命令的金融默认和强制写入；39 页 PDF 的文本层、页面坐标和作者元数据；XeLaTeX 缺字警告 0；公开 arXiv 附件哈希 716/716。最终通过数、页数和哈希以 `tools/audit_v111_report.json`、`tools/clean_verification_v1.11.json` 和 `docs/工件清单_v1.11.json` 为准。

独立人类数学复审、第三方独立复现、S2d/S4/S5 和匹配消融、独立时间外／私域语料、严格 point-in-time 和记忆审计、新实际消费与效率观测、公共实验注册、人类数据及 v1.11 专属 DOI 仍未完成。历史 v1.7 DOI `10.5281/zenodo.23620920` 不覆盖 v1.9、v1.10 或 v1.11。
