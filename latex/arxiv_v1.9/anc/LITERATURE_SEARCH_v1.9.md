# v1.9 范围综述检索记录

## 1. 定位与可复核边界

- 检索日期：2026-11-16。
- 类型：**针对性的范围综述（targeted scoping review）**，不是 PRISMA 系统综述或元分析，不声称穷尽文献。
- 使用的检索入口：本次工作会话的 Web 搜索集成；出版商/会议页面、ACM DOI 页面、ACL Anthology、PMC/PubMed、作者公开论文页用于核对题名与出处。既有 v1.8 文献表仅作为候选来源，是否纳入以本稿实际论证需要为准。
- 纳入标准：与本文至少一个核心对象直接相关——用户目标配置与可控推荐；覆盖/多样性/次模摘要；误设学习；选择性预测与高召回级联；recall@k 与检索评价；个人信息管理/通知与数字福祉；有意义人类控制、可争议性与价值敏感设计；议程设置与公共共同知识。优先原始模型、定理来源、经典实证研究和高质量综述。
- 排除标准：仅因题名含 “sovereignty”“filtering”“value” 而相关但无共同数学对象或设计问题；无法核对出处的二手引文；把供应商博客当作理论依据；与本文结论相同但缺少方法信息的材料。
- 引用方式：正文统一为作者—年份；文后按作者字母排序，不再使用作者—年份正文与编号追加文献表的混合格式。

## 2. 检索主题与实际查询

以下保留本轮使用的查询语义；在不同搜索入口可将自然语言查询拆为题名关键词。检索结果经题名与出版来源人工核对后纳入，未记录命中总数，因此不报告夸大精确性的“筛选掉 N 篇”流程。

| 主题 | 实际查询（原样或主要词组） | 核对到的代表来源 |
|---|---|---|
| 用户控制与目标配置 | `user control recommender systems putting users in control of their recommendations Harper 2015 objective configuration` | Harper et al. (2015)，用户可调节 popularity/recency 等推荐目标；Jugovac & Jannach 的交互推荐综述作为延伸候选 |
| 多样化检索与摘要 | `Carbonell Goldstein 1998 maximal marginal relevance SIGIR citation xQuAD Santos Macdonald Ounis 2010 WSDM Dang Croft 2012 PM-2`；`Lin Bilmes 2011 class submodular functions document summarization ACL citation` | MMR（Carbonell & Goldstein, 1998）；xQuAD（Santos et al., 2010）；PM-2（Dang & Croft, 2012）；次模摘要（Lin & Bilmes, 2011，ACL Anthology P11-1052） |
| 误设学习 | `misspecified learning Berk Nash equilibrium Esponda Pouzo 2016 active learning misspecified prior` | Esponda & Pouzo (2016)；Fudenberg et al. (2017)，并回溯 Berk (1966) 的误设渐近传统 |
| 拒答与级联检索 | `Chow 1970 optimum recognition error reject tradeoff IEEE selective classification Geifman El-Yaniv 2017`；`cascade ranking model efficient ranked retrieval Wang Lin Metzler 2011 SIGIR dynamic cutoff high recall retrieval` | Chow (1970)，DOI 10.1109/TIT.1970.1054406；Geifman & El-Yaniv (2017)；Wang et al. (2011)，DOI 10.1145/2009916.2009934 |
| 有意义控制与可争议性 | `meaningful human control contestability value sensitive design algorithmic systems references`；`Hirsch Designing Contestability Interaction Design Machine Learning Mental Health 2017 DIS citation` | Santoni de Sio & van den Hoven (2018)；Hirsch et al. (2017)，DOI 10.1145/3064663.3064703；Friedman & Hendry (2019) |
| 通知与数字福祉 | `notification management digital wellbeing personal information management common knowledge agenda setting Chwe rational ritual references`；`Pielot Church de Oliveira 2014 in-situ study mobile phone notifications MobileHCI citation batching notifications well-being 2019` | Pielot et al. (2014)；Fitz et al. (2019)；个人信息管理经典文献与 Chwe (2001)、McCombs & Shaw (1972) |

## 3. 对“研究空白”表述的约束

检索结果直接否定“既有研究没有回答谁拥有并写入目标函数”的二分表述。Harper et al. (2015) 已允许用户调整推荐目标，既有可控推荐、解释、交互式偏好 elicitation 与价值敏感设计也覆盖部分写入和审计问题。因此，新稿只主张：

> 据上述非穷尽检索，尚缺少一个同时显式包含 (a) pull 与 push 的统一认知预算，(b) 目标读取/授权写入/审计权，(c) 端到端实际消费口径的加权遗漏分解，以及 (d) 对这些条件的联合反事实审计的形式化整合。各组成部分及其许多审计机制均有既有上游，本文贡献是条件化组合与口径对齐，而非首次发现这些问题。

同样，MMR、xQuAD、PM-2、facility-location 与次模摘要已经研究覆盖—多样性及贪心机制。新稿明确把本文集合函数写作这些标准工具的实例化，并逐一比较目标函数、约束和保证，不再把次模性或贪心比列为新数学发现。

## 4. 尚不能由该检索支持的结论

1. 不能证明“没有任何团队做过同样的四条件整合”；只能使用“据所检索文献，尚未识别到……”。
2. 不能由检索结果推断 SEA 的效果优于可控推荐、现代 RAG 或福利优化推荐；这需要同输入、同模型、同权限和同预算的直接实验。
3. 不能把不同任务、期限和基准率的校准或 Brier 数字作跨研究排名；新稿的人类迁移门槛要求同题集配对比较。
4. 本记录是修订时可复核的范围检索，不替代投稿前按目标期刊要求完成的数据库导出、去重日志和最新文献更新。
