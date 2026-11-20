"""试点配置：P3 研究者画像 × arXiv 2019-09 重放流 × H4' 检验。

所有可调参数集中于此（论文 §14.6：参数符号化，扫描后赋值）。
"""
from __future__ import annotations

import os

HERE = os.path.dirname(os.path.abspath(__file__))
PILOT_DIR = os.path.normpath(os.path.join(HERE, "..", "pilot"))
DATA_DIR = os.path.join(PILOT_DIR, "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
RESULTS_DIR = os.path.join(PILOT_DIR, "results")

# ---- 重放窗口 ----
REPLAY_MONTH = ("2019-09-01", "2019-09-30")   # 30 个模拟日
PRIOR_WINDOW = ("2019-07-01", "2019-08-31")   # 监控清单前窗（零后见）

# ---- P3 画像：AI 方向研究者 ----
# 语料切片：OpenAlex field = Computer Science 且主题命中 AI 关键词
CS_FIELD = "Computer Science"
AI_TOPIC_KEYWORDS = (
    "artificial intelligence", "machine learning", "neural", "deep learning",
    "natural language", "language model", "computer vision", "image", "video",
    "speech", "reinforcement", "representation learning", "pattern recognition",
    "optimization", "generative", "transformer", "reasoning", "knowledge graph",
    "robot", "autonomous", "detection", "segmentation", "retrieval", "recommendation",
)

# 决策集 D（P3：选题/实验设计/论文写作/工具采用）→ 关键性 = 事后高被引
CRITICAL_QUANTILE = 0.98        # E* = 切片内引用数 top 2%
CRITICAL_SENSITIVITY = (0.95, 0.99)  # 敏感性分析分位

# 监测清单（通道 I）：三种零后见构建法（作者频次 / 作者引用 / 机构引用）
WATCHLIST_SIZE = 50            # 作者粒度清单规模
WATCHLIST_INST_SIZE = 50       # 机构粒度清单规模
WATCHLIST_SIZE_SWEEP = (10, 20, 50, 100, 200, 400)  # 容量—覆盖曲线（p̂_min 内生性）
# 通道 I 预算配额上限（交付规则；余量保底给通道 II，命题 6.3 可行性报警仍生效）
CHANNEL1_QUOTA = 0.6

# 智能体与预算
N_AGENTS = 30
BUDGETS_PER_DAY = (1, 2, 3, 4)  # 每日深读名额（P3: T≈90min，15–30min/篇）
SIM_DAYS = 30

# 评分器（通道 II）：可观测特征对重要性的预测相关度 ρ 扫描
# proxy = ρ·z(log1p(cit)) + √(1−ρ²)·N(0,1)；实测 d′ 由数据算出（定理 6.1 检验用）
RHO_SWEEP = (0.2, 0.4, 0.6)
# S1 参与优化基线：hype 与真实价值弱相关（平台的 g¹ 代理）
HYPE_ALIGN = 0.25

SEED = 20260926

# ---- P2 投资者画像（第二阶段试点）----
SIM_DAYS_P2 = 30
BUDGETS_PER_DAY_P2 = (1, 2, 3, 5)   # 投资者日处理容量（披露命题；紧预算制造过滤压力）
PORTFOLIO_SIZE = 25                   # persona 持仓组合（通道 I 直通范围）
MKT_THR = 0.025                       # 市场真值：|日收益| ≥ 2.5%
