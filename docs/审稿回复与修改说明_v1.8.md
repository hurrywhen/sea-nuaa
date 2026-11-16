# 审稿回复与修改说明（v1.8，第六轮：独立 Auditor 大修）

> 对应稿件：`input/sovereign_epistemic_acquisition_EN_v1.8.md`（英文主稿）与 `input/主权认知获取_统一理论_v1.8.md`（中文同步稿）。本轮以用户提供的 110 页 SEA 预印本初审、独立 Auditor 修复记录及 problem-net 为审查依据。原 v1.7 工件保留为历史版本，不覆盖。
>
> **裁决**：采纳 **Major Revision**，不升级为 Reject；概念整合与证据披露保留，形式保证、统计推断和引用全面收窄。拆稿仅为 venue-dependent 编辑选项。
>
> **本轮新增证据工作**：没有新增实验或人类数据；新增对现有 292 个 JSONL 的只读完整性审计、旧管线探索性 run-level 复算及后续唯一键受控重算。本仓库目前未归档可独立复现的 Lean 源码或编译日志；审稿人另报告四项官方 Lean Web 局部编译检查，其范围与限制见第七节，不据此主张整篇形式认证。**新一轮独立人类数学签核仍未完成。**

---

## 一、逐条回复（初审 1–15）

### 1. Theorem 5.1：五维精确摘要遗漏 $H_i$ 条件 —— 采纳并修复

- 新增 **(V4a) 收益侧可表示性**：$A_i=\mathcal A(\phi_i)$、$V_i=\mathcal V(\phi_i)$、$e^{-h_i/\lambda}=\mathcal D_\lambda(\phi_i)$、$c_i=\mathcal C(\phi_i)$，防止把 relevance/novelty/durability/credibility 的语义命名误当函数可表示性。
- 新增 **(V4b)**：$H_i=H$ 为标定常数，或显式给出 $H_i=\mathcal H(\phi_i)$ 的已知标定映射；仅说“folded into features”不再视为证明。
- 精确摘要改为显式映射 $v_i^*=\mathcal A(\phi_i)[\mathcal C(\phi_i)\mathcal V(\phi_i)\mathcal D_\lambda(\phi_i)-(1-\mathcal C(\phi_i))\mathcal H(\phi_i)]$，并明确 (V4)+(V4a)+(V4b) 是充分而非必要条件；缺少时只保留分解及增广表示 $(A_i,V_i,h_i,c_i,H_i)$。
- 增加伤害与收益侧反例，并注明相同条件互信息不蕴含相同 Blackwell VOI。
- 同步修复证明、定义 4.1、§5.2、贡献 C2、摘要、附录 A，并将 $v_i^*$ 的域统一为 $\mathbb R$（伤害可主导），不再误写为 $\mathbb R_{\ge0}$。

### 2. Theorem 6.3：非单调目标被赋予标准单调贪心比 —— 采纳并重构

- 不再使用“只在正增益路径上满足 margin”证明 Nemhauser 条件。新增 **(M$_R$) 单调基集证书**：
  $$g_i(\mathcal C_M\setminus\{i\})\ge\lambda\hat m_i\tau_i,\qquad \forall i\in\mathcal C_M.$$
  由次模性，这保证 $U$ 在 $\mathcal C_M$ 的全部子集上非负、单调、次模。
- Theorem 6.3 的最优值明确为 **$\mathcal C_M$ 内最优**，不估计排除完整池其他元素的损失。
- 基数、密度+可行单元素、深度 3 部分枚举+残余容量密度贪心分别写明；排除不可行元素、比较最佳可行单元素，并记录枚举深度与残余容量，不把背包比归给未增强密度贪心。Khuller–Moss–Naor 仅限最大覆盖特例。
- 非单调 $1/e$ 回退仅限**非负、基数约束**问题；不是 randomized double-greedy，不是背包保证，也不适用于可负 $U$。
- Appendix B.4 新增旧 margin 的直接反例：贪心 $1.10$、最优 $1.98$，比值 $0.556<1-1/e$。该反例针对旧条件，**不声称推翻修复后的 (M$_R$) 分支**。
- §8.8 的 $\rho_{\mathrm{push}}$ 同步加上受限域、约束与算法条件。

### 3. 双通道普遍必要性 —— 采纳并全面收窄

- 保留：分布无关容量上界，以及等方差高斯单评分模型中的 $d'\approx4.39$。
- 改为：该结果激励一种**充分**架构修复，不证明本文双通道对所有评分/检索架构普遍必要。
- 文档级 $R_{\mathrm{doc}}$ 与命题级 $R_{\mathrm{prop}}$ 分开。Corollary 6.1(ii) 改为：去重只消除重复占槽，不保证选中关键命题或达到计数上限；删除统一 $\bar r_{\mathrm{top}}$ 倍增益和“不可达”全称断言。
- 摘要、贡献 C3、相关工作、章导言、图注、P3/P4、证据矩阵和结论同步修改。

### 4. Theorem 7.4：pooled $R_{\mathrm{II}}$ 量词、实际预算与零漏报条件 —— 采纳并修复

- 改为逐命题 $q_e$ 与 $R_{\mathrm{II}}(e)$：
  $$P(\mathrm{miss}\,e)=q_e[1-R_{\mathrm{II}}(e)]\le(1-p_{\min})^{k_{\mathrm{eff}}(e)}[1-R_{\mathrm{II}}(e)].$$
  可以使用证书化的一致下界 $R_{\mathrm{II}}^{\inf}$；较弱的无补获界不受影响。
- pooled 仅保留失败率加权聚合恒等式，不能用于任意命题。正文写入反例：pooled=0.5 时 e2 实际 miss=0.5，而旧上界 0.25 失败。
- 新增 **R4（实际直通可行性）**：真实摄入、观测、溯源验证、正确命题链接、优先预留配额与 $Q_{\mathrm I}+m_{\mathrm{pub}}+m_{\mathrm{slack}}\le m$。预算警报不再被当成投递保证。
- Proposition 7.2 的零漏报仅在 $B_e$（被监控实体真实发布、摄入、验证、链接成功）与 R4 下成立；实体沉默、摄入/链接失败和超载均不归零。
- Theorem 7.1–7.2、7.4、通道 I、P5、H4'/H6'、附录 A 同步加入 R4。

### 5. Theorem 8.1：角点、损失阶数与量纲 —— 采纳并修复

- 保留正确 KKT 核心：正预算用途 $V_u'(x_u^*)=\nu$；零预算用途 $V_u'(0)\le\nu$。充分性证明第二个不等号改正。
- “任何边际不等都次优”改为仅对**可行转移方向**成立；加入 $V_1=x_1,V_2=2x_2$ 的角点反例。
- 误配损失改为完整光滑性界；只有被启用的原零预算用途满足 $V_u'(0)=\nu$ 时，对应一阶项才消失，$V_u'(0)<\nu$ 时通常仍为一阶，不再给普遍 $L/2\|\epsilon\|^2$ 上界。补充边界活跃二次例 $V_1=2x_1-\tfrac12x_1^2$、$V_2=x_2-\tfrac12x_2^2$：最优点 $(1,0)$ 两边际值均为 1，损失恰为 $\epsilon^2$。
- Pandora 改用共同视界 $H$ 的总效用：$X_s^H,B_0^H,z_s^H$，开启成本 $\widetilde c_e=\nu c_e$ 或事前已知的确定性积分成本。若 $\nu(t)$ 随机、依赖探索结果或策略路径，不得直接套用固定成本 Weitzman 定理。免费盒采用 canonical essential-supremum 指数，不再由零成本方程推出唯一 $z=\nu$。
- push 明确 utility/slot 到 utility/minute 的换算；patch 区分效用损失 $\kappa_{sw}$ 与分钟切换时间 $\tau_{sw}$；$R(t^*)=\nu$ 仅在内生长期平均率定义下成立，外部选项停止比较 $G_s'=\nu$。
- Whittle 指数不再仅凭“影子价格”同名就与 $\nu$ 数值同一。

### 6. Theorem 10.1：历史条件漂移、门控后漂移与 $b_0=0$ —— 采纳并重写

- 采用单一的**已执行更新子列**模型，替换为 C1-H、C3-H、C5-H；不再混用日历期和接受后子列。
- C1-H 直接对创新前完整历史 $\mathcal G_j$ 的已执行漂移 $\bar F_j$ 作出收缩假设；C3-H 控制选择/批准后的创新及二阶矩；C5-H 控制实施时刻和间隔。
- $b_0=0$ 由 Robbins–Siegmund 在子列上证明；不再乘接受率，避免重复计算门控。
- 日历期扩展另列所需 $\mathbb E[A_tU_t\mid\mathcal F_t]=\rho_t\bar F_t$、噪声和步长条件；明确“方向独立”不够。
- $b_0>0$ 仍为猜想；除 KC5 外，新增 **KC2 未闭合**：历史条件漂移不自动形成自主 Lipschitz 均值场。撤回“唯一缺口 KC5”和“一至两页标准论证即可完成”。
- Theorem 10.2 改为已执行子列上的常步长期望界，并增加 $0<2ac_0<1$ 稳定条件；删除无依据的 $O(t^{-2/3})$ 速率结论。

### 7. Lemma 12.1 与 Proposition 12.1 —— 采纳并修复

- 引入有机覆盖 $O_i$、植入覆盖 $B_i$ 与实际覆盖 $Z_i=\max\{O_i,B_i\}$，分别定义操纵充分认证 $\mathcal A_{\mathrm{pure}}=\mathcal M_{k_c}$、操纵在场认证 $\mathcal A_{\mathrm{present}}$ 与 but-for 反事实认证 $\mathcal A_{\mathrm{cf}}$。$K=2,k_c=2$ 时，一条植入覆盖加一条有机覆盖可产生后两类认证而 $S_{\mathrm{manip}}=1$，故它们通常不含于 $\mathcal M_2$；即使 $p_i=0$，有机覆盖仍可产生认证。
- 仅对操纵充分事件 $\mathcal M_{k_c}$ 使用精确 Poisson-binomial 尾、二项尾上界或
  $$P(S_{\mathrm{manip}}\ge k_c)\le\binom K{k_c}\bar p_a^{k_c}$$
  的 union bound（可与 1 取 min）。对 $\mathcal A_{\mathrm{cf}}$ 与 $\mathcal A_{\mathrm{present}}$，没有联合有机—操纵模型时只保留 $P(S_{\mathrm{manip}}\ge1)$ 的通用上界，不移用 $k_c$ 阶尾。
- 写入数值回归：$K=3,k_c=2,p=.1$ 时 exact=0.028、union=0.030、旧界 0.010 无效。
- 撤回 $k_{\mathrm{eff}}^a$ 替换；相关时使用联合概率 union bound 或 $\min\{1,K\bar p_a/k_c\}$ 的 Markov 界。
- 明确原始计数与预先认证独立子集是不同规则；质量加权惊讶度不自动继承该尾界，0.615→1.230 等精确率 lift 不是攻击概率验证。
- Proposition 12.1 改为真正的公共公告命题：共同接收、注意、理解及公共可见性本身须为共同知识（S4-PA）。私人回执、普通日志和“人人知道别人采用”不再被当成任意阶共同知识。
- 结论只涉及 $p\in P_t$ 的成员资格共同知识，不涉及命题真值或关键性。Theorem 12.1 的完全合规 Jaccard 界保持独立。

### 8. 实验构念与泄漏 —— 采纳限制；新增主动披露

- 所有召回均标明目标代理：学术 top-citation、金融市场移动日、法定 8-K 与 $E_{\mathrm{proxy}}$；不再等同于形式事前目标 $E^*(\tau)$。
- 学术 0.28 只拒绝主引用代理上的 95% 目标；金融 0.952/0.910 是组合内市场日代理；四家族 0.443–0.534 是固定 digest 后的代理关键机会召回。
- 新增记忆与时间戳段：2019 标题/作者/后续影响可能存在于预训练；隐藏引用字段不能去污染；H8 不是 80-run 去污染臂。
- 披露前窗引用数为 2026 抓取值而非 2019 当时快照；金融 EDGAR 盘前过滤、CDX 抓取时间与 Reuters 近似日期均未闭合。
- 结论统一为“泄漏**未被排除**”，不断言泄漏已证实。替代引用代理敏感性分析因缺可独立工件，不再作为已验证结果。
- 时间外、匿名标题/精确匹配记忆审计、post-cutoff/私有新语料与 point-in-time 特征验证列入待完成事项，未伪造完成状态。

### 9. 统计推断 —— 采纳并改为效应量/run-level CI 前置

- 保留 CMH 算术 $\chi^2_1=981.5207$ 和 erfc 数值复核，但明确其为**旧管线、未去重、agent-day 独立近似下的名义尾概率**。
- run 分层不能消除 run 内相关、共享标签/上游 digest、共同 30 天语料和重复键；极端 p 值不再用于跨语料/跨人群推广。
- 四家族统一写成“合计 80 个带种子重放配置（O/C 各 30、Q/G 各 10）”，不是 $4\times80$，也不是 80 个独立语料。
- 新增旧管线 run-level 对照（seed=42、10,000 次 bootstrap）：

| family | judgment−parametric recall contrast [95% CI] | Δvalue [95% CI] |
|---|---:|---:|
| O | +0.029954 [−0.004266, +0.064719] | −0.174953 [−0.292388, −0.054597] |
| C | +0.130914 [+0.100330, +0.160221] | +0.676372 [+0.552233, +0.809795] |
| Q | +0.109360 [+0.080931, +0.141390] | +0.431757 [+0.291113, +0.561243] |
| G | +0.087009 [+0.022198, +0.144005] | −0.223145 [−0.426896, −0.030564] |

- 四个点估计均为正，但 **O 区间跨零**；“命中维度全胜”撤回。上述结果标为 `LEGACY_EXPLORATORY_NOT_DEDUPLICATED`，不是新冻结主结果。
- 0.241 只是 30 天、29 个机会的确定性描述参照；1.838–2.216 倍只是描述性比值。0.443–0.534 均远低于 95%。
- **三家族是另一项实验，不机械继承四家族降级**：历史 CMH 改称“所述分层与依赖近似下的语料内名义推断”。新增 `audit_three_family_dependence.py` 及 `THREE_FAMILY_DEPENDENCE_SENSITIVITY.{json,md}`，按完整模拟日聚类和循环连续 5 日块各 bootstrap 10,000 次。Q 合并 judgment−parametric 点估计 +0.066810 的两种 95% 区间为 [−0.159095,+0.309783] 与 [−0.090533,+0.244565]；所有家族的参数对照区间均跨零，故不再使用“统计确认”。judgment−honest 的 Q 区间仍为正，O 日聚类区间 [−0.004954,+0.432584] 跨零，均只作同语料事后敏感性描述。

### 10. 样本流水 —— 采纳并超额完成唯一键对账

新增 `sim/sea_pilot/audit_replay_integrity.py` 与 `REPLAY_INTEGRITY_AUDIT.{json,md}`：

| 指标 | 审计结果 |
|---|---:|
| 分片 / run | 292 / 80（合计） |
| raw rows | 73,704 |
| 空选择 | 157 |
| 非空 `picked` 管线有效行 | 73,547 |
| 唯一 `(family,run,agent,sim_day)` 键 | **71,914** |
| 重复有效记录超额 | **1,633** |
| 相对名义 72,000 的唯一键缺口 | **86** |
| 唯一键 <900 的 run | **25/80** |
| 重复键 / 其中结果不同 | 1,608 / **1,389** |

因此，73,547 不再称为唯一 agent-day；1,547 只是算术超额，不证明新增独立样本。重复并非都可忽略，不能任意取首条或末条。旧完整性闸门只数非空行，不是唯一性证书。

**后续已完成**：冻结规约后完成 recall、Δvalue、run-level CI、McNemar/CMH、BH(4)、run-cluster 与 17 场景全量重算。86 缺口进一步分为 56 empty-only 与 30 no-surviving-row；A 按指标分别解析 recall 71,573、Δvalue 70,676、sign 71,618，详见第六节及 `frozen_reanalysis_v1/REPORT.md`。旧审计仍不猜测重复的历史原因。

### 11. 基线与归因 —— 采纳并保留 judgment-layer 限定

- S2d、S4、S5 全部标为 **[design] 且无数字**；中文表 14-1 补齐 S4/S5 行。
- 未来各臂须匹配模型、原始输入、推理/token 预算、检索访问和潜在记忆。
- 诚实特征参照不是现代 RAG；半 oracle 使用未来相关引用代理并参与上游 digest，不是可部署诚实评分器。
- “full SEA stack”“所有 P1–P12 均完成”改为：全栈是设计目标，当前只有固定 digest 后判断子实验。未完成端到端比较前，不把增益归因于 SEA 整体结构。

### 12. 结果解释与口径 —— 采纳并修正新增发现

- 0.443–0.534 相对 0.241 为 1.838–2.216 倍，但远低于 95%，且不是端到端召回。
- 金融展示值漏报率 4.8%→9.0%，相对增加 **87.5%**；未舍入值约 **89.47%**。目标数 **18→19**、供给 **4.6→4.733**，不是同分母配对因果效应，0.910 未达 95%。
- 公共认证纠正初审所沿用的混口径：不是单一 0.63→1.23。按冻结 `algo_validation.json`：
  - market-only：**0.615→1.230**；
  - market∪legal：**0.626→1.359**。
  两者均使用 432/1,771（24.39%）认证覆盖率，分别相对各自基率；仍为同语料事后弱富集，独立确认与对抗稳健性待检验。

### 13. 引用抽查 —— 采纳并逐条修复

- Pennycook & Rand (2022)：文章号 **2333**、题名用 for、DOI `10.1038/s41467-022-30073-5`；正文不再单向声称耐久性存疑，明确其纵向试验未见显著衰减。
- Kommers et al. (2026)：标为《Why Slop Matters》概念评论，不再称规模测量；补 Article 3 与 DOI `10.1145/3786777`。
- Wang et al. (2025)：改为五项预注册**模拟 feed**研究，不是真实平台 field test；补 DOI。
- Stray et al.：改用 2024 ACM TORS version of record、完整正式作者群、2(3) Article 20、57 pages、DOI `10.1145/3632297`；正文年份改 2024。
- Shumailov et al.：改为六位正式作者，**Shumaylov** 拼写及顺序修正，补 DOI `10.1038/s41586-024-07566-y`。
- 139 条参考文献编号连续；审计正文—文献闭合 0 未解析。此次仍是抽查修正，不冒充完整系统文献综述。

### 14. 可复现性 —— 采纳并补可执行信息

正文直接给出：

- v1.7 tag：`https://github.com/hurrywhen/sea-nuaa/tree/v1.7.0`；
- 完整 commit：`fdc4912a30174d71b944d1ec83fcfda260f8ebf1`；
- 版本 DOI：`10.5281/zenodo.23620920`；概念 DOI：`10.5281/zenodo.23620919`；
- 新审计命令：`PYTHONDONTWRITEBYTECODE=1 python3 sim/sea_pilot/audit_replay_integrity.py`；
- 构建命令、依赖锁 `sim/sea_pilot/{requirements,runtime}-replay-integrity.txt` 和 `docs/REPRODUCIBILITY_v1.8.md`。

**v1.8 是工作修订，不冒称已包含于 v1.7 DOI/tag。** 正式发布前仍须生成新不可变 commit、源/数据快照、release manifest 和 DOI。公开源实时下载不承诺逐位一致；H9 原始答案、嵌入缓存、v2 原始输出和替代代理工件缺口主动披露。无真实 URL 的 OSF/匿名链接表述已删除。

### 15. 结构 —— 采纳为 venue-dependent 建议

§18.1 改为：

- **A 极端过滤/冗余覆盖**：§§3–7，并纳入第 8 章，除非其算法与实验扩充；
- **B 目标捕获/慢速控制/公共层**：§§9–12；
- **C 双领域与 agent 试点**：§§13–15，须先完成唯一键重算、无泄漏时间外测试和 S2d/S4/S5。

不再声称“拆分无需改写”；各篇需独立动机、记号、局限与交叉引用。当前专著形态保留为一种载体，拆稿不是科学硬条件。

---

## 二、独立 Auditor 校准意见的落实

- **Theorem 7.4**：按善意修读采用逐命题 $R_{\mathrm{II}}(e)$；pooled 反例只用于澄清量词，无 $R_{\mathrm{II}}$ 的较弱上界保留。
- **Theorem 6.3**：不以违反 margin 的反例宣称推翻 margin 分支；直接反例只否定旧证明所需条件，新的 (M$_R$) 分支独立给出充分条件。保留有条件的非单调 fallback，但不扩张到背包。
- **Theorem 6.1**：明确区分分布无关容量/阈值恒等式与高斯 4.39，不笼统称全定理仅限高斯。
- **实验**：保留作者已有的 post-hoc 和 run-level CI 披露；泄漏写为未排除，样本流水先称未对账，再用新增只读审计给出实际唯一键结果，不宣称历史成因。
- **Proposition 12.1**：承认原稿有公共公告叙述，进一步补足回执及协议公共可见性，避免把有限回执链误当任意阶知识。
- **零 miss watchlist**：在 Theorem 7.4 中显式保留“实体实际发布相关内容”及摄入、链接、R4 条件。

---

## 三、状态边界：已完成、探索性、待完成

### 已完成（本轮文档/审计）

- v1.8 中英主稿理论条件、证明、摘要、贡献、预测矩阵、局限与结论同步修订；
- 292 分片唯一键 manifest 与旧管线 run-level 探索性 CI；
- 修正引用与公共认证匹配口径；
- 可执行审计、依赖锁、复现说明和数值回归；
- 自动审计：编号 0 未解析；139 refs 连续且引用闭合；数字 9/9；v1.6 58/58；v1.7 22/22；v1.8 50/50；manifest=PASS；math=PASS。

### 探索性（不得当作确证或跨语料证据）

- 旧管线未去重的 recall、Δvalue、McNemar/CMH、run-level CI；
- 新完成的 `CONTROLLED_UNIQUE_KEY_REANALYSIS__WITHIN_CORPUS_EXPLORATORY` 及全部 17 场景；它不是 prospective preregistration；
- 三家族日聚类与连续日块事后依赖敏感性；
- 重复键的结果异同分类；
- 本文 AI 辅助证明修订与自动一致性检查，不等同独立人类或形式化证明核验。

### 待完成（未伪造结果）

1. 人类作者/独立数学复核，必要时 Lean 或其他形式验证；
2. 时间外无泄漏、记忆消融和 point-in-time 特征/时间戳测试；
3. S2d/S4/S5 与逐项消融，匹配模型、输入、预算和记忆；
4. 新不可变 v1.8 commit、数据快照、release manifest、DOI；
5. HP-0、后续充分功效人类研究，以及治理部署有效性检验。

---

## 四、复现命令

```bash
PYTHONDONTWRITEBYTECODE=1 python3 sim/sea_pilot/audit_replay_integrity.py
PYTHONDONTWRITEBYTECODE=1 python3 sim/sea_pilot/recompute_replay_frozen.py
PYTHONDONTWRITEBYTECODE=1 python3 sim/sea_pilot/audit_three_family_dependence.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=sim python3 -m unittest sea_pilot.test_replay_frozen sea_pilot.test_three_family_dependence
python3 tools/audit_paper.py
bash tools/build_review_pdf.sh en
bash tools/build_review_pdf.sh zh
bash tools/make_arxiv_source.sh
```

依赖与构建环境见 `docs/REPRODUCIBILITY_v1.8.md`。本轮实际构建：EN 118 页、ZH 81 页，文本层均 0 问题、缺字形均 0；arXiv XeLaTeX 两遍通过，119 页、缺字形 0。PDF、源包、审计脚本与 manifest 的 SHA-256 已记入 `docs/工件清单_v1.8.md`。该清单是当前工作树构建记录，不冒充新的不可变 release；未发布的 v1.8 工作树不赋予虚构 commit 或 DOI。

---

## 五、2026-11-03 独立理论与实证终审后的二次修复

### 理论与附录

- Theorem 5.1 在 (V4b) 之外追加 (V4a)，解决 $A_i,V_i,h_i,c_i$ 未形式化为 $\phi$ 函数的问题；“only under”改为充分条件，互信息只作需标定的代理。
- Theorem 6.2 明确 $v_e,\mu,\lambda,\hat m_i,\mathrm{sim}\ge0$；B.4 补 $k=0$ 与元素耗尽/dummy 边界。
- Proposition 8.2 删除 $\kappa_{sw}<\bar c$ 的错误 iff，改为 $h(t)=G-tG'$ 的穿越条件；外部价格停止规则限定有限内点最优，边界另列。Proposition 8.1 将精确常数 $\nu$/积分成本与近似指数分开。
- Corollary 6.1(iii) 把严格单调性限定于 $\pi_p=\pi_d$、$\beta_p\le1$ 且固定 $\pi,R$ 的理想比较，近似情形另行计算。
- Proposition 7.2 增加 $P(B_e)>0$；pooled 公式约定 $q_e=0\Rightarrow q_eR_{\mathrm{II}}(e):=0$；长尾归零均保留 $B_e$+R3–R4。
- Lemma 12.1 改为操纵诱导覆盖/认证事件 $\mathcal M_{k_c}$，不再等同于全部 attestation。
- Proposition 12.1 改为只有协议 (i) 是事先共同知识，公共公告事件 $B$ 自明后再用 partition 证明，避免前提同义反复。
- §10.1 原始日历期动力学改为唯一的执行时刻递归；C1-H/C3-H/C5-H 增加可测性、固定 $\theta^*$、有限 $M_\xi$、无限严格递增停时和有限间隔条件。
- B.2 删除非 adapted 尾和草证，直接引用 Robbins–Siegmund；a.s. ODE 部分降为 `Heuristic B.2(ii)(b)`，KC2/KC5 与随机时刻细节均不作为已证引理。B.3 同步补齐停时量词。
- Theorem 10.2 不再声称有 $\sigma_\theta$ 自动敏感性公式；Theorem 8.1 的引言统一为所有 funded uses 等式、unfunded uses 不等式，不虚构独立上界约束。

### 实证、写作与可用性

- 删除“已经运行 full SEA stack”和“exact measurement”，改为设计目标与回顾代理计算。
- “All raw records”改为“Available raw records”，并指向 H9/缓存/v2/替代代理的完整性缺口。
- `primary inference` 改为“旧管线探索分析内的主要描述性摘要”，明确重复处置和全量重算前不作 confirmatory inference。
- 预注册绝对化表述增加新唯一键审计和事后公共认证例外。
- Pennycook & Rand 改为“单次 session 内 successive trials 无显著衰减”，不再写 long-term longitudinal durability。
- “every printed number”改为“selected high-risk numbers, formulas, and artifact totals”，覆盖集合由脚本列明。
- 学术代理正式写为 $E_{\mathrm{proxy}}$，不再误写 $E^*$；漏报改为对冻结回顾代理清单的确定性计算。
- 明确表 14-1 家族级 McNemar 用 BH（A3-3），H1′–H7′ 用 Holm；金融配置变化和公共 lift 是描述性比较。
- 清除“reinforced”“dual-domain real-data validation”“cross-validating model collapse”等过强表述；full RCT 统一为三臂。
- 待办改为预定重复处置/结果仲裁和 86 个名义缺口处理，唯一键本身已固定。
- v1.7 不可变正文及元数据的旧 `valid agent-days` 称谓增加归档警示，不回改旧归档；正式 v1.8 release metadata 必须采用唯一键口径。

**更新后自动审计**：v1.8 专项由 34 项增至 **50 项**，全部通过；编号 0 未解析，139 refs 连续且引用闭合，manifest=PASS，math=PASS，硬性问题 0。

---

## 六、2026-11-03 后续 P0/P1 复核（第七轮）

本轮确认 v1.8 已完成的 Theorem 5.1、6.3、双通道、7.4 主体、8.1 主体、10.1/10.2、Lemma 12.1 概率计算、Proposition 12.1、实验披露与五项文献修复，不重复原样旧批评。以下只处理尚未闭合的定义、边界、统计重算与发布问题。

### 1. P0 理论定义与前提闭合

- **Lemma 12.1**：不再使用含义未闭合的 $\mathcal A_{\mathrm{manip}}$。在同一撤销操纵耦合上定义 $O_i,B_i,Z_i$、$N_O,N_{\mathrm{raw}},S_{\mathrm{manip}}$，区分操纵充分、操纵在场与 but-for 反事实认证。$k_c$ 类 Poisson-binomial/union tail 只用于 $\mathcal A_{\mathrm{pure}}=\mathcal M_{k_c}$；$K=2,k_c=2$ 的一条植入加一条有机覆盖构成明确的混合反例。反事实与在场事件另给“至少一次植入”通用界，精细因果尾界须另有 $(O_i,B_i)$ 联合模型。
- **Theorem 9.3**：正式加入 $aA>0$、$D_m>0$ 与 $0<G<D_m$ 的内部有效区间；分别处理 $G<0$、$G=0$、$G\ge D_m$。$G=0,\sigma=0$ 不再误称严格占优，越界阈值不截断。煽情分支直接使用正确的 $D_s=p_s^{plat}-p_s^{sov}\ge\Delta_p>0$ 及同样的有效区间，静态 payoff 比较不再直接写成均衡消亡。
- **Proposition 9.2**：直接假设固定 payoff 下 $\gamma>0$，并加入 $x_m(0)\in[0,1/2]$ 的全局 $\gamma/2$ 界及正向不变性证明；$x_m(0)=0$ 单列。另给 $0<x_m(0)<1$ 的 odds 形式全局消亡界，避免把初值限制误读为初值大时不收敛。没有采用“$\sigma>\max\{\sigma^*,\sigma_s^*\}$ 即可”的替代条件，因为它只比较两类非诚实策略与诚实策略，不能保证 $\Pi_m,\Pi_s$ 的相互大小。
- **Theorem 11.1/11.2**：$D_{\mathrm{adv}}$ 扩为含 $\Omega,L,u_{\mathrm{undo}}$ 的七元有限授权，$\mathcal A_{\mathrm{safe}}$ 与 $\Omega$ 非空有限，minimizer 与有限枚举可计算性成为显式前提。一般遗憾结论改为定义给出的等式；可逆性直接取平局集 undo-cost minimizer。一般虚警损失改为 $C_F=\mathbb E[L(a^*,\omega)\mid F]$，两行动模型进一步按实际选择区分 $a_p\Rightarrow C_F=c_p$ 与 $a_\varnothing\Rightarrow C_F=0$，并列服从既定加细；补 $H_{\max}\ge0$ 与 $P_E=0$ 时加权项取零。严格占优直接要求 $\Psi>0$ 或正概率严格增损事件，不再由目标不同、攻击面非空或 Premise 5 推出。
- **Theorem 7.4**：recover/deliver/miss 全部统一为实际消费事件，量词固定为 $e\in E^*\setminus\mathrm{WL}$；R4 明确为覆盖所有相关时期与命题的概率一事件。

### 2. P1 局部数学、算法与编辑统一

- VOI 改为决策特定量；Blackwell 序不再被用来推出“VOI 是条件互信息的单调函数”，互信息只在独立标定后作工程代理。log-benefit 补为 $\log B_i=\log A_i+\log c_i+\log V_i-h_i/\lambda$，只称保序等价并处理零收益；Gaussian 后验明确 $\epsilon_i\perp\omega_d$，且真分支概率 $c_i$ 与分支内噪声 $\sigma_i^2$ 不再混同。Lemma 5.1、Definition 5.2 与 B.5 统一最大值可达、可积和正则决策问题条件。
- KKT 一阶项改为：被启用的原零预算用途满足 $V_u'(0)=\nu$ 时才消失。新增数值回归通过的二次反例，并保留英文证明中的 `> 0`。
- Proposition 8.1 要求开盒前已知的确定性成本；随机或路径依赖 $\nu(t)$ 不得套用固定成本 Weitzman 定理。
- Proposition 10.2 保留投影递归，机器判断改为“未经连接模型便不是人类校准的已识别测量”，不再声称统计独立；B.2(ii)(a) 限确定系数与固定有限 $\tau$。B.1/B.5 补 $n\ge1$ 与最大值/可积性条件。
- Theorem 6.3 与 B.4 明确正成本、可行元素、最佳可行单元素、深度 3 枚举、残余容量与完成规则；跨章精确摘要补齐 (V4)+(V4a)+(V4b)。
- 中文“零后见评估”统一改为“金融域，按窗口限制但非严格 point-in-time 的评估”；“紧急覆盖”统一为“紧急接管（Emergency Override）”；`memory-proof` 改为抗记忆污染表述；公共层使用“对抗鲁棒性”。

### 3. 三家族：保留独立实验定位，校准强推断

历史 CMH 不机械删除，也不沿用四家族重复键问题作机械降级；改称所述分层与依赖近似下的语料内名义推断。新增日聚类与连续 5 日块依赖敏感性后，所有家族参数对照区间均跨零，强推断解释随之撤回。Q 合并 judgment−honest 区间仍为正，O 日聚类区间跨零；这些全是同语料事后敏感性，不证明跨语料有效性。

### 4. 四家族唯一键全量重算（已完成）与发布状态

- 已执行 `sim/sea_pilot/recompute_replay_frozen.py`，冻结 `docs/主验证唯一键处置与重分析规约.md`：充分字段一致才解析，冲突缺失；86 缺口拆为 56 empty-only 与 30 no-surviving-row；共同 cohort、严格单例、attempt 等权均值、五种结果盲哈希、零消费情景与部分识别端点一次性全部输出，不选择有利场景。
- A 的解析人口为 recall **71,573**（341 冲突）、Δvalue **70,676**（1,238 冲突）、sign **71,618**（296 冲突）；B/C/D/E 为 70,676/70,306/70,525/71,914。A 不插补 86 缺口、不删除 run，日级参数不唯一即失败。
- 主规则 A（run 等权，10,000 次 run bootstrap，seed=42）：

| family | Rllm [95% CI] | Δrecall [95% CI] | Δvalue [95% CI] |
|---|---|---|---|
| O | 0.443790 [0.433311,0.454506] | +0.030170 [−0.003971,+0.064767] | −0.175016 [−0.293452,−0.053577] |
| C | 0.532600 [0.525874,0.539520] | +0.129283 [+0.098441,+0.158663] | +0.667380 [+0.539180,+0.802858] |
| Q | 0.516153 [0.503543,0.528210] | +0.112887 [+0.081432,+0.147666] | +0.426727 [+0.295044,+0.548216] |
| G | 0.519783 [0.497670,0.539156] | +0.089412 [+0.022924,+0.148522] | −0.219053 [−0.427112,−0.025626] |

- A 的精确 McNemar/BH(4) 已重算，但只作名义 agent-day 近似。run-cluster 敏感性为：O **0.160128**（MC）、C 0.00001（MC）、Q 0.001953（精确 $2^{10}$）、G 0.015625（精确 $2^{10}$）。因此 O 的 agent-day 显著性不能代表 run 级稳健性。
- 80-run 汇总 B=14,113、C=9,371：未校正 $\chi^2=957.526997$（名义 $p=3.066\times10^{-210}$）；采用 $\max(0,|B-C|-1)$ 的修正 $\chi^2=957.123190$（名义 $p=3.753\times10^{-210}$）；80-run cluster MC $p=0.00001$。旧 981.52/1.9×10⁻²¹⁵ 仅保留为旧管线溯源，不是当前主结果。
- 全部 17 场景保持 Δrecall 点估计为正、Δvalue C/Q 正而 O/G 负，但包含有意方向端点，不能据此作 blanket robustness 认证。完整结果见 `sim/pilot/results/frozen_reanalysis_v1/REPORT.md` 与 `summary.json`；工件含 1,360 个 run 场景行、72,000 条逐键账本和 292 输入 SHA-256。
- 验证：20 项重算合成测试通过；独立对账确认 17 场景、CSV/账本行数、输入 manifest、主估计、CMH 与 run-cluster 均一致。旧管线永久保留 `LEGACY_EXPLORATORY_NOT_DEDUPLICATED`，新结果为 `CONTROLLED_UNIQUE_KEY_REANALYSIS__WITHIN_CORPUS_EXPLORATORY`，不是 prospective preregistration。
- v1.8 新不可变 commit、公开源/数据快照、release manifest 与 DOI 仍需正式发布流程；当前工作树哈希不冒充不可变发布。逐步闸门见 `docs/RELEASE_CHECKLIST_v1.8.md`，该清单本身不是发布证明。

**二次独立 AI 数学复核**：上述五处二次修复及 Proposition 9.2 的直接 $\gamma>0$ 条件均已复核闭合，中英一致，未发现新的同类分支遗漏。该记录仍不替代独立人类数学签核或 Lean 形式认证。

**该轮自动审计**：v1.8 专项 **96/96**，硬性问题 0；manifest/math/three-family-dependence 均 PASS；三家族合成单元测试 3/3 通过。该轮构建的英文内审 PDF 为 123 页、中文 84 页，文本层与标题断裂均 0 问题；arXiv XeLaTeX 源包 123 页、缺字形 0。全部 17 场景重算、规约、脚本、测试与复现附件已纳入源包。最新补充答复后的复验记录见第七节末尾。

---

## 七、最新独立 Auditor 初审的补充答复与边界确认

### 1. 明确撤回已经修复的旧批评

本轮不沿用“同一批评逐版重复”的写法，正式确认：

1. **Theorem 5.1**：(V4)+(V4a)+(V4b) 已封闭 $H_i$ 与收益侧可表示性；撤回“五维精确摘要无条件为假”的表述。它现在是充分条件下的条件定理。
2. **Theorem 6.3**：(M$_R$) 上的非负单调基集与受限 OPT 已成立；撤回把全局非单调 $U$ 的旧反例直接套到受限分支。密度+最佳可行单元素、深度 3 枚举、残余容量完成和非单调 fallback 已分别规定。
3. **双通道**：仅为一种充分工程响应；撤回“正文仍主张双通道对所有架构普遍必要”的旧批评。
4. **Theorem 7.4**：逐命题 $R_{\mathrm{II}}(e)$、$q_e=0$、失败率加权聚合和 R4 已修复 pooled 反例；本轮又把 recover/deliver/miss 统一为实际消费事件，并明确 $e\in E^*\setminus\mathrm{WL}$。
5. **Theorem 8.1**：内点/角点、单位、免费盒 ess-sup 与无一普遍二阶保证均已修复；新的边界活跃二次例精确给出 $\epsilon^2$ 损失。
6. **Theorem 10.1/10.2**：C1-H/C3-H/C5-H 与执行子列模型下，$b_0=0$ 作为条件定理接受；$b_0>0$ 仍只是猜想，KC2/KC5 不得写成已闭合。
7. **Lemma 12.1**：至少 $k_c$ 类的 Poisson-binomial 尾、union bound、0.028 回归与非独立回退已修复；针对这些旧概率计算错误的批评予以撤回。最新工作只闭合事件语义，不重复宣称原尾公式错误。
8. **Proposition 12.1**：公共自明事件和 S4-PA 下的任意阶共同知识接受，结论仅限成员资格而非命题真值。
9. **实验披露**：唯一键流水、四家族降级、post-hoc/泄漏披露、87.5%/89.47%、两组公共 lift、五项文献与 v1.7 归档边界均已回应；唯一键重算现已完成，不再把“尚未重算”作为当前状态。

### 2. 审稿人报告的四项 Lean 检查：承认局部结果，不扩大认证范围

审稿人报告官方 Lean Web 已编译 `quadratic_corner_is_optimal`、`activation_loss_is_quadratic`、`producer_threshold_exceeds_one` 和 `mixed_attestation_not_subset_of_two_manipulations`。据报告，前三项公理输出为 `propext`、`Classical.choice`、`Quot.sound`，第四项无公理依赖；四项均无 `sorryAx` 或自定义公理。本文据此撤回“完全没有任何局部 Lean 检查”的笼统表述。

但当前工作树没有对应 `.lean` 源码、工具链锁或日志，本次也未独立 rerun，故只称其为**审稿人报告的局部数学对象检查**，不列为本仓库已复现工件，不称为整篇论文或现实语义的形式认证。尤其混合计数定理只证明 raw-count=2 而 implant<2，未形式化旧 `A_manip`，未证明操纵是认证的反事实必要原因；它与修订后 Lemma 12.1 的混合反例一致，不能称为“Lean 推翻 Lemma 12.1”。p.29 互信息反例及其他文字批评仍属审稿推导。复现和正式发布闸门已分别加入源码、版本锁与 `#print axioms` 日志要求。

### 3. 最后一轮跨章一致性修复

- 英文卷首不再把唯一键全量重算写为待完成；中英文摘要及中文稿内嵌英文摘要均区分旧未去重工件与新受控重算，二者都不作确证推断。
- 相关漏网注改为：任意相关下路径界 $D\le\delta n_{\max}$ 与期望界仍成立，失效的是 Hoeffding 集中项；不再声称正相关使高概率界“退化为期望界量级”。全漏/全不漏的完全耦合例说明为何在 $\beta<1-\rho_m$ 时仅凭边际概率无非平凡高概率改进。
- 公共层退出段改为只移除该主体参与所对应的公共层保证；不再称其成对重叠、对 $\Omega$ 的总贡献或实际福利代价归零。
- Lemma 12.1 的独立性措辞限定于精确 Poisson-binomial、二项尾支配与乘积型 union bound；事件恒等式和联合概率/Markov 回退不依赖独立性。
- 主稿、回复和复现说明均明确局部 Lean 报告的来源与未复现状态，不再使用“没有 Lean”的笼统句。

### 4. 独立只读扫描后的追加数学与跨章修复

在阶段候选哈希快照上另做独立只读 AI 扫描后，继续完成以下最小修复；该扫描不替代人类签核：

- 清除 §15.2“四家族仍处于完整性复核”和 §18.1“唯一键重算仍待完成”两处陈旧状态；计算重算已完成，未完成的仅是独立人类复核、时间外测试和基线。
- Lemma 12.1 的结果标注和证明明确：独立性用于乘积概率，union bound 本身不需要独立性。Theorem 9.2 证明补 $n_m=0$ 平凡分支，避免除零。
- Proposition 9.1 限定加性线性评分目标，明确 $A^*$ 与 $\widetilde A$ 分别是原评分和扰动评分下的最优选择；以 $|\widetilde V_{\mathrm{lin}}(A)-V_{\mathrm{lin}}(A)|\le mD$ 和最优性恒等式证明 $2mD$ 遗憾，不再把原始条目价值差误界为 $2D$，也不扩张到任意选择或完整集合级 $U$。
- Proposition 6.3 的证明把 $m_{\mathrm{slack}}$ 纳入声明目标不可用名额，使命题上界与证明一致。
- Proposition 7.1 的组构造限 $0<p_{\min}<1$；$p_{\min}=0$ 时界 1 平凡取紧，$p_{\min}=1$ 时确定性覆盖使漏报为 0，不再误称同组非独立。
- 相关矩阵和并查集只用于启发式候选分组；两两不相关不蕴含相互独立，组数不再是 $k_{\mathrm{eff}}$ 的证书或严格上/下界。
- Theorem 7.3 的单调次模性改为逐实现覆盖函数加期望的证明，对任意联合分布成立，乘积式仅是 R2 下求值。两类时明确独立乘积是实际覆盖率上界、实际漏报率下界，不笼统称为保守公式；三类反例给出边际 $.5$、两两交集 $.30$ 而并集 $.89>.875$，撤回“三类以上两两正相关必降低并集”的全称方向。最大独立子集不再被当作独立分组或分组贪心规则。
- 公共层数值段改为 $m=10$、非空且完全共同消费示例下的 1–2 条；定义的上限 $|P_t|\le2$ 不再被误读为每日非空保证。

### 5. 当前裁决与仍未完成事项

理论文本、P1 编辑项、四家族唯一键全量重算及三家族依赖敏感性已在工作树完成；这回应了“有针对性的 Major Revision”，不是否定 SEA 框架，也不自动等于最终投稿版。独立人类数学签核和不可变 v1.8 commit/公开快照/release manifest/DOI 仍是投稿前闸门。时间外无泄漏复制、ex ante 关键性标签、point-in-time 特征与时间戳、记忆消融、S2d/S4/S5、公共层独立确认、HP-0 和后续人类研究继续属于后续研究；维持“条件性框架+探索性判断层试点”定位时，不把它们伪写为已完成。

**第七节复验记录**：论文专项审计增至 **124/124**，硬性问题 0；manifest/math/three-family-dependence/frozen-reanalysis 全部 PASS，重算与三家族合成测试合计 **23/23**。两个默认 stdout 的只读复算分别与冻结四家族 `REPORT.md`、三家族敏感性报告一致（仅 stdout 多一个末尾换行）。最新英文内审 PDF **125 页**、中文 **86 页**；英文 26 个、中文 27 个标题断裂均为 0，文本层问题均为 0。最终 arXiv XeLaTeX 构建与工件哈希以 `docs/工件清单_v1.8.md` 为准。上述检查不构成独立人类数学签核，也不把审稿人报告的局部 Lean 检查变成本仓库已复现证明。
