"""sea_algo —— 阶段二参考实现（docs/算法设计_v1.0.md 的可运行对应物）。

纯参数化、确定性、零 LLM 调用；LLM 判断层为可插拔件（接口见 selector.Item.score）。
模块：A1 prop_graph / A2+A9 selector / A3 planner / A4 scheduler / A5 allocator /
      A6+A7 watchlist / A8 certify / A10 calib / validate（验证套件）。
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
