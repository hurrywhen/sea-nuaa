# v1.17 结构化叙述性文献定位与定向书目核验记录

> **v1.17 版本说明：**本轮为新增的分层小样本区间补充 1 条标准方法文献 Wilson (1927)，主稿统一参考文献表由 52 条增至 **53 条**；已于 2026-11-23 通过 Crossref 核验题名、作者、卷期页与 DOI。严格连续期次、联合协方差半正定检查和零完成诊断均属执行器语义与统计边界修正，不新增效果文献。既有检索与核验记录沿用 v1.13 轮（检索日期 2026-11-16 至 2026-11-17），未补造命中数。

## 1. 方法定位与责任边界

- 检索与核验日期：2026-11-16 至 2026-11-17。
- 类型：**结构化叙述性文献定位（structured narrative positioning）＋定向书目核验**；不是系统综述、PRISMA 范围综述或元分析。
- 原因：v1.9 及更早检索未保存每个数据库的完整命中集、逐条去重日志和排除清单。本版不补造命中数或筛选数，也不再使用“targeted scoping review”称谓。
- 筛选执行：AI 助手按下列规则生成候选并逐条核对出版记录；未进行第二名评审者的独立筛选，作者对文献表的最终人工签核仍属投稿前事项。
- 去重规则：优先 DOI，其次 ACL Anthology/NeurIPS 正式论文 ID 和 arXiv 版本 ID，最后使用规范化题名＋首作者＋年份。预印本与正式论文不混作同一出版状态的证据。
- 纳入标准：直接支持正文实际使用的模型、方法、统计程序或研究定位；优先原始论文、正式会议/期刊记录和标准统计来源。近期路线图只用于收缩新颖性，不用于支持效果。
- 排除标准：仅有相同关键词但无共同对象；无法核验的二手引文；供应商博客作为理论来源；把 arXiv DOI 当正式会议 DOI；把只有预印本记录的工作写成同行评审论文。
- 下方定向核验清单共 14 条：既有 13 条（含此前评审修订补入的 Savage 1951），加本轮 Wilson 1927 一条；均纳入主稿统一参考文献表（正文或补充材料实际引用）。该数字只描述明确列出的核验清单，**不是全部搜索命中的筛选流图**。

## 2. 检索入口与代表性完整查询

| 主题 | 数据库/权威记录 | 实际查询或标识符 | 核验结果与用途 |
|---|---|---|---|
| RAG 原始模型 | NeurIPS Proceedings；arXiv 仅用于版本区分 | `Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks Lewis NeurIPS 2020`；正式记录 hash `6b493230205f780e1bc26945df7481e5`；`arXiv:2005.11401` | Lewis et al. (2020)，NeurIPS 33:9459–9474。正式记录未列 proceedings DOI，故不把 arXiv DOI 写成会议 DOI |
| RAG 组件评价 | ACL Anthology；Crossref | `RAGAs Automated Evaluation of Retrieval Augmented Generation`；`ARES Automated Evaluation Framework Retrieval-Augmented Generation Systems` | Es et al. (2024)，DOI `10.18653/v1/2024.eacl-demo.16`；Saad-Falcon et al. (2024)，DOI `10.18653/v1/2024.naacl-long.20`。只支持 context/faithfulness/answer 分层，不支持生产效率 |
| 智能体推荐综述 | ACL Anthology；Crossref | `site:aclanthology.org 2025 Findings EMNLP agents recommender systems survey`；`10.18653/v1/2025.findings-emnlp.620` | Peng et al. (2025)，11574–11583。用于 profile/memory/planning/action 和评价版图，不证明 SEA 优势 |
| 2026 自主信息寻求路线图 | Web 搜索；arXiv abstract/API；DataCite；全文 HTML | `2026 roadmap LLM agents recommender systems pull push tool use planning evaluation survey`；`Autonomous Information Seeking: A Roadmap for Agentic Recommender Systems`；`arXiv:2607.04433` | Lin et al. (2026)，arXiv v1，2026-07-05。覆盖 reactive/proactive/mixed initiative、工具、规划、延迟/token 评价；未核实同行评审 venue，故只称预印本 |
| 路线图否定性核对 | arXiv 全文 | `pull`、`push`、`proactive`、`tool`、`planning`、`evaluation`、`cost` | 未在已检查文本中识别 SEA 字面 pull/push 统一认知预算；因此只能作为相邻路线图，不得宣称其已发表 SAP 组合 |
| 用户控制与目标配置 | ACM DOI/出版商记录 | `user control recommender systems putting users in control of their recommendations Harper 2015 objective configuration` | Harper et al. (2015)；Jugovac & Jannach (2017)。否定“过去无人研究用户目标控制”的表述 |
| 多样化检索与次模摘要 | ACM/SIGIR；ACL Anthology | `Carbonell Goldstein 1998 maximal marginal relevance SIGIR`；`xQuAD Santos Macdonald Ounis 2010`；`Dang Croft 2012 PM-2`；`Lin Bilmes 2011 class submodular functions document summarization` | MMR、xQuAD、PM-2、Lin–Bilmes；SEA 只实例化既有工具 |
| 误设学习 | 期刊出版记录 | `misspecified learning Berk Nash equilibrium Esponda Pouzo 2016 active learning misspecified prior` | Berk (1966)、Esponda–Pouzo (2016)、Fudenberg et al. (2017) |
| 拒答、级联与检索评价 | IEEE/ACM 出版记录 | `Chow 1970 optimum recognition error reject tradeoff`；`cascade ranking model efficient ranked retrieval Wang Lin Metzler 2011`；`Voorhees 1998 relevance judgments retrieval effectiveness` | 支持 abstention、阶段召回和判断变异；不支持把 selected 当 consumed |
| 人类控制与可争议性 | ACM/期刊出版记录 | `meaningful human control contestability value sensitive design algorithmic systems`；`Hirsch Designing Contestability 2017 DIS` | Santoni de Sio–van den Hoven、Hirsch et al.、Friedman–Hendry；形式测试不等于有意义控制 |
| Clopper–Pearson | Oxford Biometrika；Crossref；JSTOR | `The Use of Confidence or Fiducial Limits Illustrated in the Case of the Binomial`；`10.1093/biomet/26.4.404`；JSTOR `2331986` | Clopper & Pearson (1934)。exact 指二项反演，离散情形不保证每点恰好名义覆盖 |
| KKT | Springer；UC Press/Crossref；Project Euclid | `Karush Minima of Functions of Several Variables with Inequalities as Side Conditions`；`Nonlinear Programming Kuhn Tucker 1951` | Karush (1939；2014 reprint DOI `10.1007/978-3-0348-0439-4_10`)；Kuhn–Tucker (1951)，DOI `10.1525/9780520411586-036`。正文同时写 Slater 条件 |
| Minimax-regret 判据 | JASA/Taylor & Francis；Crossref | `Savage The Theory of Statistical Decision 1951`；`10.1080/01621459.1951.10500768` | Savage (1951)，JASA 46(253):55–68。规范性补充材料 N2 引为标准 minimax-regret 判据来源；评审修订补入统一参考文献，不是新 regret 定理 |
| McNemar 与 CMH | Psychometrika/Crossref；JSTOR；Oxford JNCI；PubMed | `Note on the Sampling Error of the Difference Between Correlated Proportions or Percentages`；`Some Methods for Strengthening the Common Chi Square Tests`；`Statistical Aspects of the Analysis of Data from Retrospective Studies of Disease` | McNemar (1947)，`10.1007/BF02295996`；Cochran (1954)，`10.2307/3001616`；Mantel–Haenszel (1959)，`10.1093/jnci/22.4.719`。paired binary 与 stratified 2×2 设计不混用 |
| Bootstrap | IMS/Crossref；Project Euclid | `Bootstrap Methods Another Look at the Jackknife`；`10.1214/aos/1176344552` | Efron (1979)。只支持重抽样方法来源，不能替代聚类单位和共享语料不确定性分析 |
| Wilson 比例区间 | Crossref API（2026-11-23） | `10.1080/01621459.1927.10502953`；返回题名 `Probable Inference, the Law of Succession, and Statistical Inference` | Wilson, Edwin B. (1927)，*Journal of the American Statistical Association* 22(158):209–212。仅支持 Wilson score 区间的方法来源，不支持把单位级边际区间当作聚类、同时或联合区间 |
| 通知、议程与共同知识 | ACM/期刊/出版社记录 | `Pielot Church de Oliveira 2014 mobile notifications`；`batching notifications well-being 2019`；`Chwe Rational Ritual common knowledge` | 保留为补充材料背景，不承担主文效果识别 |

## 3. 新增文献的精确书目状态

1. **Lewis et al. (2020)**：正式 NeurIPS 论文，9459–9474；官方页面 https://proceedings.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html 。
2. **Peng et al. (2025)**：Findings of EMNLP 2025，DOI https://doi.org/10.18653/v1/2025.findings-emnlp.620 。
3. **Lin et al. (2026)**：仅核实 arXiv:2607.04433v1，DOI https://doi.org/10.48550/arXiv.2607.04433 ；不得称同行评审综述。
4. **Es et al. (2024)** 与 **Saad-Falcon et al. (2024)**：ACL 正式论文，分别对应 RAGAs 和 ARES；效率结论是评价效率，不是部署 token/时延效率。
5. **Karush (1939)** 的 DOI 属于 2014 重印，不倒填为 1939 年学位论文当时已有 DOI。
6. **Savage (1951)**：JASA 46(253):55–68，DOI https://doi.org/10.1080/01621459.1951.10500768 ；评审修订补入统一参考文献，由规范性补充材料 N2 引用。

## 4. 新颖性表述的最终约束

本检索否定“既有研究没有询问谁能配置推荐目标”和“2026 年尚无自主信息获取/智能体推荐路线图”这类宽泛说法。正文仅保留：

> 在上述非穷尽结构化叙述检索中，尚未识别到一个同时显式包含 (a) pull/push 多资源共同预算，(b) 目标读取、授权写入、回滚和审计，(c) 终端实际消费的加权遗漏，以及 (d) 固定供给与供给生态两类反事实审计的形式化组合。各组件均有重要上游，本文贡献是条件化接口、可执行一致性与证据口径纠偏。

该表述不证明“没有任何团队完成同样组合”，不支持 SEA 优于 RAG、可控推荐或福利推荐，也不把经典定理数量当作理论创新性。投稿前若改称系统/范围综述，必须另行保存数据库导出、完整命中、去重和逐条排除日志，并进行独立人工筛选。
