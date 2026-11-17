"""主验证统计分析模块 TDD 验收（规约 A1–A5，docs/主验证统计分析规约.md）。

运行：cd sim && python3 -m unittest sea_pilot.test_analysis
"""
from __future__ import annotations

import json
import os
import tempfile
import unittest

from sea_pilot import main_validation_analysis as mva


def _rec(day=1, picked=("x",), hits_llm=1, hits_param=0, n_crit=2,
         value_llm=5.0, value_param=4.0, injected=None, impulse=None):
    return {
        "day": day, "picked": list(picked), "injected": injected or [],
        "impulse_consumed": impulse or [], "reason": "t", "raw_consume": list(picked),
        "agent": 0, "sim_day": day - 1, "hits_llm": hits_llm, "hits_param": hits_param,
        "n_crit": n_crit, "value_llm": value_llm, "value_param": value_param,
    }


def _write(results_dir, tag, records):
    with open(os.path.join(results_dir, f"llm_replay_{tag}.jsonl"), "w",
              encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def _make_mini_dataset(results_dir):
    """微型合规数据集：O/C 各 30 run、Q/G 各 10 run，每 run 900 条已知值记录。"""
    for fam, n_runs, prefix in (("O", 30, "o"), ("C", 30, "c"), ("Q", 10, "q"),
                                ("G", 10, "g")):
        for r in range(1, n_runs + 1):
            # Q 家族按规约 R-11：run 1 本地 q_r01，run 2-10 云端 qc_rNN
            if fam == "Q":
                tag = "q_r01" if r == 1 else f"qc_r{r:02d}"
            elif fam == "G" and r >= 4:
                tag = f"ga_r{r:02d}a"
                _write(results_dir, tag, [_rec(day=d) for d in range(1, 31)] * 15)
                _write(results_dir, f"ga_r{r:02d}b", [_rec(day=d) for d in range(1, 31)] * 15)
                continue
            elif fam == "O" and r >= 23:
                for part, pre in (("a", "oa"), ("b", "oa")):
                    _write(results_dir, f"{pre}_r{r:02d}{part}",
                           [_rec(day=d) for d in range(1, 31)] * 15)
                continue
            else:
                tag = f"{prefix}_r{r:02d}"
            _write(results_dir, tag, [_rec(day=d) for d in range(1, 31)] * 30)


class TestParsing(unittest.TestCase):
    def test_tag_parsing(self):
        cases = {"o_r05a": ("O", 5), "oa_r24b": ("O", 24), "od_r30a": ("O", 30),
                 "c_r12f": ("C", 12), "q_r01": ("Q", 1), "qc_r07": ("Q", 7),
                 "g_r02b": ("G", 2), "ga_r09a": ("G", 9)}
        for tag, want in cases.items():
            self.assertEqual(mva.parse_tag(tag), want, tag)

    def test_run_metrics_exact(self):
        """T-A1：合成已知值 → recall/Δvalue 精确断言。"""
        recs = [_rec(hits_llm=1, n_crit=2), _rec(hits_llm=2, n_crit=2),
                _rec(hits_llm=0, n_crit=0), _rec(picked=[])]  # n_crit=0 不计入；空记录无效
        m = mva.run_metrics(recs)
        self.assertEqual(m["n_valid"], 3)
        self.assertAlmostEqual(m["recall"], (1 + 2) / (2 + 2))
        self.assertAlmostEqual(m["dvalue"], 1.0)          # 5.0-4.0
        self.assertAlmostEqual(m["value_ratio"], 5.0 / 4.0)

    def test_impulse_susceptibility(self):
        recs = [_rec(injected=["i1", "i2"], impulse=["i1"]),
                _rec(injected=["i3"], impulse=[])]
        m = mva.run_metrics(recs)
        self.assertAlmostEqual(m["impulse_susc"], (1 / 2 + 0 / 1) / 2)


class TestGuards(unittest.TestCase):
    def test_integrity_gate(self):
        """T-A2：记录不足时非零退出（WU-4 同构完整性闸门）。"""
        with tempfile.TemporaryDirectory() as d:
            _write(d, "o_r01", [_rec()] * 10)   # 远不足 900
            with self.assertRaises(SystemExit) as cm:
                mva.load_dataset(d)
            self.assertNotEqual(cm.exception.code, 0)

    def test_archive_forbidden(self):
        """T-A3：archive_* 路径拒绝。"""
        with self.assertRaises(SystemExit):
            mva.load_dataset("pilot/results/archive_protocol_v1")
        with self.assertRaises(SystemExit):
            mva.load_dataset("pilot/results/archive_family_F")

    def test_duplicate_run_rejected(self):
        """T-A4：同家族同 run 号双重来源（如 o_r05a + oa_r05a）即拒绝。"""
        with tempfile.TemporaryDirectory() as d:
            _make_mini_dataset(d)
            _write(d, "oa_r05a", [_rec(day=dd) for dd in range(1, 31)] * 15)
            with self.assertRaises(SystemExit):
                mva.load_dataset(d)


class TestRealDataSmoke(unittest.TestCase):
    """T-A5：现役 73k 真实记录冒烟（跳过诚实臂离线补算）。"""

    def test_real_dataset(self):
        results = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                               "pilot", "results")
        if not os.path.exists(os.path.join(results, "llm_replay_c_r01a.jsonl")):
            self.skipTest("真实数据不在本机")
        ds = mva.load_dataset(results)
        self.assertEqual({k: len(v) for k, v in ds.items()},
                         {"O": 30, "C": 30, "Q": 10, "G": 10})
        out = mva.analyze(ds, honest_arm=False)
        for fam in ("O", "C", "Q", "G"):
            agg = out["families"][fam]
            self.assertTrue(0 <= agg["recall_mean"] <= 1, fam)
            self.assertTrue(0 <= agg["mcnemar_p"] <= 1, fam)
            self.assertEqual(len(agg["recall_ci95"]), 2)
        chi2, p = out["pooled_cmh"]
        self.assertTrue(0 <= p <= 1)
        self.assertGreaterEqual(out["n_valid_total"], 72000)


if __name__ == "__main__":
    unittest.main()
