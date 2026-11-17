"""sea_algo —— 历史 A1–A10 算法实验（v1.0/v1.7 谱系）。

这些模块不是 v1.10 SAP 的端到端实现，也不提供当前主稿的治理符合性或联合最优性验证。
跨版本引用只使用稳定标识 A1–A10；旧“定理/引理/章节”编号不再作为代码契约。
当前 S1–S4 参考接口和 14 项合成测试位于独立的 ``sea_governance`` 包。
纯参数化、确定性、零 LLM 调用；LLM 判断层为可插拔件（接口见 selector.Item.score）。
模块：A1 prop_graph / A2+A9 selector / A3 planner / A4 scheduler / A5 allocator /
      A6+A7 watchlist / A8 certify / A10 calib / validate（历史验证套件）。
"""
from .prop_graph import collapse, aggregate_events
from .certify import certify_scores, precision_at_frac, CLASS_WEIGHTS
from .watchlist import greedy_cover, brute_force_optimal, RollingManager
from .planner import EIGPlanner
from .scheduler import weitzman_bernoulli, PandoraScheduler
from .allocator import MarginalVOIAllocator
from .selector import Item, DualChannelSelector, firewall_sim
from .calib import brier, ece, pava, Recalibrator, ThetaCalTracker, FAMILY_POLICY

__all__ = ["collapse", "aggregate_events", "certify_scores", "precision_at_frac",
           "CLASS_WEIGHTS", "greedy_cover", "brute_force_optimal", "RollingManager",
           "EIGPlanner", "weitzman_bernoulli", "PandoraScheduler",
           "MarginalVOIAllocator", "Item", "DualChannelSelector", "firewall_sim",
           "brier", "ece", "pava", "Recalibrator", "ThetaCalTracker", "FAMILY_POLICY"]
