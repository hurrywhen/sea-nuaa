# v1.8 不可变发布闸门（未发布）

> 本清单是发布操作规范，不是 release manifest，也不证明 v1.8 已公开。当前工作树、PDF、哈希和 arXiv 候选包均属于本地候选工件。v1.7 的 tag、commit 与 DOI 只标识 v1.7，不能核验 v1.8 新增定理、统计规约或重分析结果。

## A. 投稿前必须完成的科学闸门

- [ ] 独立人类数学复核者签核 v1.8 的定理、定义与证明；AI 审核和自动检查不代替该签核。
- [x] 四家族唯一键全量重算完成，并公开全部预定场景、逐 run 结果、run-level CI、McNemar/CMH、多重校正与敏感性，而非只保留有利场景（见 `sim/pilot/results/frozen_reanalysis_v1/`）。
- [x] 中文“零后见评估”已全部消除，统一为按窗口限制但非严格 point-in-time 的口径。
- [ ] Lemma 12.1、Theorem 9.3/9.2、Theorem 11.1/11.2 的定义与前提由人类复核确认闭合。
- [x] 三家族历史 CMH 只称所述分层与依赖近似下的语料内名义推断，并附日级依赖敏感性（见 `THREE_FAMILY_DEPENDENCE_SENSITIVITY.{json,md}`）。

## B. 新不可变 commit 与源快照

- [ ] 将中英主稿、审稿回复、全部新脚本、规约、依赖锁和结果工件纳入一个实际的新 git commit；记录完整 40 位 SHA，不使用浮动 `main` 链接代替。
- [ ] 确认该 commit 包含四家族重算脚本与最终输出，而非只有旧完整性审计。
- [ ] 创建 v1.8 专用 tag 和 GitHub 不可变 release；保留 v1.7 tag 与历史工件，不回改。
- [ ] 用 `git archive` 或等价方式生成该 commit 的源快照，并记录快照 SHA-256。
- [ ] 从新 commit 的干净工作树重建中英 PDF 与 arXiv 源包，重新运行全部测试，避免把未提交修改误装入发布包。

## C. 数据快照与逐 run manifest

- [ ] 冻结 292 个原始四家族 JSONL 的发布快照；manifest 逐项记录相对路径、字节数、行数和 SHA-256。
- [ ] 冻结三家族输入及其独立分析口径；`qwen38all` 标为 na+b 派生合并，不作为额外独立复制。
- [ ] 纳入 80-run 完整性 manifest、唯一键处置账本、全场景结果和输入/规约/脚本哈希。
- [ ] 保留旧管线 `LEGACY_EXPLORATORY_NOT_DEDUPLICATED` 与新受控重分析的清晰边界；不得把旧统计改名为新冻结主结果。
- [ ] 记录已知缺口：H9 原始答案、嵌入缓存、独立 v2 原始输出、替代引用代理工件；不得用“可公开重建”掩盖缺失。
- [ ] 数据快照使用固定媒体（Zenodo 或等价不可变存储），记录其独立校验值与访问 URL。

## D. 锁定环境与复验

- [ ] 记录 Python、NumPy、Pandoc、TeX Live、字体和操作系统版本；依赖锁与运行环境文件随包发布。
- [ ] 从锁定环境执行唯一键重算、三家族依赖敏感性、合成测试、论文一致性审计、PDF 文本层检查和 SHA-256 对账。
- [ ] 发布 `release-manifest.json`，包含所有主稿、脚本、规约、输入 manifest、结果、PDF、源包和数据快照的 SHA-256。
- [ ] 若将审稿人报告的四项局部 Lean 检查升级为发布方可复现工件，附 `.lean` 源码、Lean/Mathlib 版本锁、`#print axioms` 输出及干净环境复验日志；未补齐前只能按审稿人报告归属，不得列入本仓库已复现证明。
- [ ] 对发布包执行独立解压/下载后的复算，确认没有依赖本地未提交文件。

## E. 新 DOI 与论文元数据回填

- [ ] 创建 v1.8 的版本 DOI；如概念 DOI 采用 Zenodo 自动汇聚机制，同时记录版本 DOI 与概念 DOI 的区别。
- [ ] 在论文 *Data and Code Availability*、`CITATION.cff`、README、审稿回复和工件清单中回填新 commit、tag、版本 DOI、数据快照和 release manifest URL。
- [ ] `CITATION.cff` 的软件 `version/date-released/doi` 只有在实际发布后才能改为 v1.8；在此之前继续明确其指向 v1.7。
- [ ] 元数据不得沿用“73,547 valid agent-days”旧称谓；采用 71,914 唯一有效键及重分析后的各指标已解析键口径。
- [ ] 回填后重新构建 PDF 和源包，确认回填本身也包含在同一个最终 release commit 中，避免自指不一致。

## F. 不属于本次发布完成声明的事项

时间外无泄漏复制、ex ante 关键性标签、point-in-time 特征/时间戳验证、S2d/S4/S5 与逐项消融、公共层独立确认、HP-0 和后续充分功效人类研究仍是后续工作。即使上述发布闸门全部完成，也不得将这些未完成研究写成已解决。
