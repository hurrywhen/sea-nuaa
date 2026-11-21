"""调度规约（docs/主验证调度规约.md）的验收测试（stdlib unittest，零依赖）。

TDD：本测试先于调度实现。规约条款在各测试 docstring 中引用。
运行：cd sim && python3 -m unittest sea_pilot.test_dispatch -v
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SIM_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SIM_DIR))

KNOWN_MODULES = {
    "sea_pilot.run_llm_replay",
    "sea_pilot.h8_battery_v2",
    "sea_pilot.h9_calibration",
}
SEED_RANGES = {"O": range(1, 31), "G": range(1, 11), "Q": range(101, 111),
               "C": range(201, 231), "F": range(301, 311)}


def gen_tasks(tmp: Path) -> dict[str, list[str]]:
    """运行生成器到临时目录，返回 {lane: [非注释任务行]}（含子车道 O1/O2/...）。"""
    subprocess.run([sys.executable, "-m", "sea_pilot.make_dispatch_tasks", str(tmp)],
                   cwd=SIM_DIR, check=True, capture_output=True)
    lanes = {}
    for f in sorted(tmp.glob("tasks_*.txt")):
        lane = f.stem[len("tasks_"):]
        lines = f.read_text(encoding="utf-8").splitlines()
        lanes[lane] = [ln.strip() for ln in lines if ln.strip() and not ln.startswith("#")]
    return lanes


class TestTaskLists(unittest.TestCase):
    """规约 WU-1 / WU-3 / P-1。"""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.lanes = gen_tasks(self.tmp)

    def tearDown(self):
        self._tmp.cleanup()

    def test_task_lists_parseable(self):
        """WU-1：每条任务行以已知模块开头且带唯一 --tag/--model-tag。"""
        for lane, tasks in self.lanes.items():
            self.assertTrue(tasks, f"lane {lane} 任务为空")
            for t in tasks:
                words = t.split()
                self.assertIn(words[0], KNOWN_MODULES, f"未知模块: {words[0]}")
                self.assertTrue("--tag" in words or "--model-tag" in words,
                                f"缺 tag: {t}")

    def test_tag_and_seed_unique(self):
        """WU-3 + L-4：tag 全局唯一；(seed, agent-start) 二元组唯一，seed 落在规约区间。"""
        all_tags = []
        for lane, tasks in self.lanes.items():
            tags, pairs = [], []
            for t in tasks:
                words = t.split()
                key = "--tag" if "--tag" in words else "--model-tag"
                tags.append(words[words.index(key) + 1])
                if "--seed" in words:
                    seed = int(words[words.index("--seed") + 1])
                    start = int(words[words.index("--agent-start") + 1])
                    pairs.append((seed, start))
                    family = lane[0]  # 子车道 O1/O2/O3 同属 O 家族区间
                    self.assertIn(seed, SEED_RANGES[family],
                                  f"lane {lane} seed {seed} 越界")
            all_tags += tags
            self.assertEqual(len(pairs), len(set(pairs)),
                             f"lane {lane} (seed, agent-start) 重复（假复制）")
        self.assertEqual(len(all_tags), len(set(all_tags)), "tag 全局重复")

    def test_sharding_layout(self):
        """L-4：O 车道每 run 分 3 片（agent-start 0/10/20 × agents 10），G 车道分 2 片（0/15 × 15）。"""
        def shards(fam):
            out = {}
            for lane, tasks in self.lanes.items():
                if lane[0] != fam:
                    continue
                for t in tasks:
                    if not t.startswith("sea_pilot.run_llm_replay"):
                        continue
                    w = t.split()
                    seed = int(w[w.index("--seed") + 1])
                    out.setdefault(seed, set()).add(
                        (int(w[w.index("--agent-start") + 1]), int(w[w.index("--agents") + 1])))
            return out
        def lane_seeds(lane):
            out = set()
            for t in self.lanes[lane]:
                if t.startswith("sea_pilot.run_llm_replay"):
                    out.add(int(t.split()[t.split().index("--seed") + 1]))
            return out
        o = shards("O")
        self.assertTrue(o, "O 家族无 replay 任务")
        self.assertEqual(sorted(o), list(range(1, 31)), "O 家族应为 run 1–30")
        for seed, parts in o.items():
            if seed <= 22:
                self.assertEqual(parts, {(0, 10), (10, 10), (20, 10)},
                                 f"O run {seed}（1–22）应为 Mac 三分片: {parts}")
            else:
                self.assertEqual(parts, {(0, 15), (15, 15)},
                                 f"O run {seed}（23–30）应为节点双分片: {parts}")
        # 规约 R-16：G 完成后 node-a/node-d 转产 ornith——OA 承担 run 23–28，OD 承担 29–30
        self.assertEqual(lane_seeds("O1") | lane_seeds("O2") | lane_seeds("O3"),
                         set(range(1, 23)))
        self.assertEqual(lane_seeds("OA1") | lane_seeds("OA2"), set(range(23, 29)))
        self.assertEqual(lane_seeds("OD1") | lane_seeds("OD2"), {29, 30})
        g = shards("G")
        self.assertTrue(g, "G 家族无 replay 任务")
        self.assertEqual(sorted(g), list(range(1, 11)), "G 家族应为 run 1–10（规约 R-11）")
        for seed, parts in g.items():
            self.assertEqual(parts, {(0, 15), (15, 15)},
                             f"G run seed={seed} 分片布局错误: {parts}")
        # 规约 R-11：node-d 的 G1/G2 仅 run 1–3，node-a 的 GA1/GA2 承担 run 4–10
        # （node-a 实测 ~28 tok/s 远快于 node-d ~12 tok/s，负载按速率配比）
        def lane_seeds(lane):
            out = set()
            for t in self.lanes[lane]:
                if t.startswith("sea_pilot.run_llm_replay"):
                    out.add(int(t.split()[t.split().index("--seed") + 1]))
            return out
        self.assertEqual(lane_seeds("G1") | lane_seeds("G2"), {1, 2, 3})
        self.assertEqual(lane_seeds("GA1") | lane_seeds("GA2"), {4, 5, 6, 7, 8, 9, 10})
        c = shards("C")
        self.assertTrue(c, "C 家族无 replay 任务")
        self.assertEqual(len(c), 30, f"C 为主力 30 run（规约 R-5），实际 {len(c)}")
        for seed, parts in c.items():
            self.assertEqual(parts, {(i * 5, 5) for i in range(6)},
                             f"C run seed={seed} 分片布局错误: {parts}")
        # 规约 R-18：F 家族已裁撤，任务清单不得再有 F 车道
        self.assertFalse(any(l == "F" for l in self.lanes), "F 家族应已裁撤（规约 R-18）")

    def test_qc_split(self):
        """规约 R-11：Q 本地仅保留已完成的 run 1（seed 101）；QC 云端 run 2–10。"""
        def seeds(lane):
            out = []
            for t in self.lanes[lane]:
                if t.startswith("sea_pilot.run_llm_replay"):
                    out.append(int(t.split()[t.split().index("--seed") + 1]))
            return out
        self.assertEqual(seeds("Q"), [101])
        self.assertEqual(seeds("QC"), list(range(102, 111)))
        for t in self.lanes["QC"]:
            if t.startswith("sea_pilot.run_llm_replay"):
                self.assertIn("--tag qc_", t)
        # 电池随 QC（同型号云端）
        joined = "\n".join(self.lanes["QC"])
        self.assertIn("q90_h8", joined)
        self.assertIn("q90_h9", joined)

    def test_days_not_overclaimed(self):
        """P-1：语料仅 30 模拟日，replay 任务禁止 --days > 30。"""
        for lane, tasks in self.lanes.items():
            for t in tasks:
                if t.startswith("sea_pilot.run_llm_replay"):
                    days = int(t.split()[t.split().index("--days") + 1])
                    self.assertLessEqual(days, 30, f"--days {days} 属虚标")


class TestSeedIndependence(unittest.TestCase):
    """规约 WU-3：异 seed 必须产生真差异，同 seed 必须可复现。"""

    def test_seed_changes_digest_order(self):
        from sea_pilot.run_llm_replay import build_days
        records = [
            {"cit": (i * 37) % 50, "insts": [f"inst{i % 3}"], "arxiv_id": f"id{i}",
             "date": f"2019-09-{(i % 30) + 1:02d}"}
            for i in range(120)
        ]
        critical = {f"id{i}" for i in range(0, 120, 17)}
        watchlist = {"ids": {"inst0"}}
        d1 = build_days(records, critical, watchlist, proxy_seed=99)
        d2 = build_days(records, critical, watchlist, proxy_seed=100)
        d1b = build_days(records, critical, watchlist, proxy_seed=99)
        self.assertEqual([x["digest"] for x in d1], [x["digest"] for x in d1b])
        self.assertNotEqual([x["digest"] for x in d1], [x["digest"] for x in d2])


class TestPreflight(unittest.TestCase):
    """规约 V-1：预检守卫拒绝空内容与退化重复，兼容三种推理字段。"""

    def test_validate_response(self):
        from sea_pilot.preflight import validate_response
        ok = {"model": "m", "choices": [{"message": {"content": "正常"}}]}
        self.assertEqual(validate_response(ok), "m")
        think = {"model": "m", "choices": [{"message": {"content": "", "reasoning": "思考"}}]}
        self.assertEqual(validate_response(think), "m")
        think2 = {"model": "m", "choices": [{"message": {"content": "", "reasoning_content": "思考"}}]}
        self.assertEqual(validate_response(think2), "m")
        with self.assertRaises(AssertionError):
            validate_response({"model": "m", "choices": [{"message": {"content": ""}}]})
        with self.assertRaises(AssertionError):
            validate_response({"model": "m", "choices": [{"message": {"content": "/" * 30}}]})

    def test_preflight_sends_auth(self):
        """规约 V-6：云车道预检须带 Authorization 头（api_key 参数）。"""
        from unittest import mock
        from sea_pilot import preflight
        seen = {}
        resp = {"model": "m", "choices": [{"message": {"content": "正常"}}]}

        class FakeResp:
            def read(self): return json.dumps(resp).encode()
            def __enter__(self): return self
            def __exit__(self, *a): return False

        def fake_urlopen(req, timeout=None):
            seen["auth"] = req.headers.get("Authorization")
            return FakeResp()

        with mock.patch("urllib.request.urlopen", fake_urlopen):
            got = preflight.preflight("http://x/v1", "m", api_key="secret")
        self.assertEqual(got, "m")
        self.assertEqual(seen.get("auth"), "Bearer secret")


class TestTokenBudgetPolicy(unittest.TestCase):
    """规约 P-4：思考预算封顶（协议 v2.1）按家族分档，落实为声明常量。"""

    def test_max_tokens_defaults(self):
        from sea_pilot import agents_llm
        self.assertEqual(agents_llm.MAX_TOKENS_INIT, 1200)   # G/Q 档（默认）
        self.assertEqual(agents_llm.MAX_TOKENS_CAP, 2400)

    def test_lane_budgets_in_launcher(self):
        """启动器必须为 O 车道设置 2400/4800，G/Q/C/F 车道 1200/2400（规约 P-4 分档）。"""
        script = (SIM_DIR / "run_dispatch_3node.sh").read_text(encoding="utf-8")
        for line in script.splitlines():
            if line.strip().startswith("launch "):
                parts = line.split()
                lane = parts[1]
                init = int(parts[4]) if len(parts) > 4 else None
                cap = int(parts[5]) if len(parts) > 5 else None
                if lane.startswith("O"):
                    self.assertEqual((init, cap), (2400, 4800), f"{lane} 预算档错误")
                else:
                    self.assertEqual((init, cap), (1200, 2400), f"{lane} 预算档错误")

    def test_h9_tag_alias(self):
        """规约 R-17：h9_calibration 必须接受 --tag（任务清单契约），默认 ornith。"""
        from sea_pilot import h9_calibration
        self.assertEqual(h9_calibration._resolve_tag(
            ["prog", "--tag", "q90_h9"]), "q90_h9")
        self.assertEqual(h9_calibration._resolve_tag(
            ["prog", "--model-tag", "g90_h9"]), "g90_h9")
        self.assertEqual(h9_calibration._resolve_tag(["prog"]), "ornith")
        # --tag 与 --model-tag 同现时 --model-tag 优先（向后兼容）
        self.assertEqual(h9_calibration._resolve_tag(
            ["prog", "--tag", "x", "--model-tag", "y"]), "y")

    def test_cloud_lanes_in_launcher(self):
        """规约 R-5/R-6/R-7/R-8/R-10/R-15：云车道上线、密钥不入库、节拍、成本熔断。"""
        script = (SIM_DIR / "run_dispatch_3node.sh").read_text(encoding="utf-8")
        for lane in ("C1", "C2", "C3", "C4", "C5", "C6", "QC"):
            self.assertIn(f"launch {lane} ", script, f"启动器缺子车道 {lane}")
        self.assertIn("inclusionai/ling-3.0-flash", script)
        self.assertIn("qwen/qwen3.8-27b", script)          # R-10：QC 同型号增援
        self.assertNotIn("sk-or-v1-", script, "API key 不得写入入库脚本（规约 R-6）")
        self.assertIn("SEA_MIN_INTERVAL", script, "F 免费配额节拍（规约 R-7/R-15）")
        self.assertIn("SEA_COST_CAP", script, "付费车道须设成本熔断（规约 R-8/R-10）")
        self.assertIn(".openrouter_key", script, "密钥应经 gitignored 文件注入")
        # R-18：F 家族已裁撤，启动器不得再有 F 车道
        self.assertNotIn("launch F ", script, "F 家族应已裁撤（规约 R-18）")

    def test_gitignore_covers_keyfile(self):
        gi = (SIM_DIR.parent / ".gitignore").read_text(encoding="utf-8")
        self.assertIn(".openrouter_key", gi, "规约 R-6：密钥文件必须 gitignore")

    def test_cost_cap_exists(self):
        """规约 R-8：后端须有成本熔断常量。"""
        from sea_pilot import agents_llm
        self.assertGreater(agents_llm.COST_CAP_DEFAULT, 0)

    def test_o_recovery_launcher(self):
        """规约 L-6/R-1：O 车道单独恢复脚本存在、语法合法、预算档正确。"""
        script = SIM_DIR / "run_dispatch_o.sh"
        self.assertTrue(script.exists())
        subprocess.run(["bash", "-n", str(script)], check=True)
        text = script.read_text(encoding="utf-8")
        for lane in ("O1", "O2", "O3"):
            self.assertIn(lane, text)
        self.assertIn("2400 4800", text, "O 恢复脚本预算档须为 2400/4800（规约 P-4）")

    def test_launcher_lane_filter(self):
        """规约 R-1：启动器支持车道过滤参数（部分恢复，避免重复启动在跑车道）。"""
        text = (SIM_DIR / "run_dispatch_3node.sh").read_text(encoding="utf-8")
        self.assertIn('ONLY="${2:-}"', text)
        self.assertIn('grep -q " $lane "', text)
        # 幂等守卫：已在运行的车道不得重复启动（避免双写 jsonl；锚定 ^ 防包装壳误匹配）
        self.assertIn('pgrep -f "^bash lane_runner.sh $lane "', text)
        # 规约 R-11：GA 车道用派生模型 gemma4c4k（固化 num_ctx=4096，/v1 忽略 options）
        self.assertEqual(text.count('"gemma4c4k"'), 2, "GA1/GA2 应使用 gemma4c4k")

    def test_min_interval_pacing(self):
        """规约 R-7：SEA_MIN_INTERVAL 时节流生效。"""
        from unittest import mock
        from sea_pilot import agents_llm
        sleeps = []
        resp = {"choices": [{"message": {"content": '{"consume":[],"reason":"ok"}'}}],
                "usage": {"completion_tokens": 1, "cost": 0.0}, "model": "m"}

        class FakeResp:
            def read(self): return json.dumps(resp).encode()
            def __enter__(self): return self
            def __exit__(self, *a): return False

        backend = agents_llm.OpenAICompatBackend.__new__(agents_llm.OpenAICompatBackend)
        backend.base_url, backend.api_key, backend.model = "http://x", "k", "m"
        with mock.patch.dict("os.environ", {"SEA_MIN_INTERVAL": "5"}), \
             mock.patch("urllib.request.urlopen", lambda req, timeout=None: FakeResp()), \
             mock.patch("time.sleep", lambda s: sleeps.append(s)):
            backend.complete("sys", "usr")
        self.assertTrue(any(s >= 5 for s in sleeps), f"未见节拍睡眠: {sleeps}")

    def test_num_ctx_option(self):
        """规约 R-11：SEA_NUM_CTX 时请求体带 options.num_ctx（node-a 防 OOM）。"""
        from unittest import mock
        from sea_pilot import agents_llm
        seen = {}
        resp = {"choices": [{"message": {"content": '{"consume":[],"reason":"ok"}'}}],
                "usage": {"completion_tokens": 1}, "model": "m"}

        class FakeResp:
            def read(self): return json.dumps(resp).encode()
            def __enter__(self): return self
            def __exit__(self, *a): return False

        def fake_urlopen(req, timeout=None):
            seen["body"] = json.loads(req.data)
            return FakeResp()

        backend = agents_llm.OpenAICompatBackend.__new__(agents_llm.OpenAICompatBackend)
        backend.base_url, backend.api_key, backend.model = "http://x", "k", "m"
        with mock.patch.dict("os.environ", {"SEA_NUM_CTX": "4096"}), \
             mock.patch("urllib.request.urlopen", fake_urlopen):
            backend.complete("sys", "usr")
        self.assertEqual(seen["body"].get("options", {}).get("num_ctx"), 4096)
        # 未设置时不带 options 字段（其他车道行为不变）
        with mock.patch.dict("os.environ", {}, clear=False), \
             mock.patch("urllib.request.urlopen", fake_urlopen):
            import os as _os
            _os.environ.pop("SEA_NUM_CTX", None)
            backend.complete("sys", "usr")
        self.assertNotIn("options", seen["body"])

    def test_provider_order_option(self):
        """规约 R-14：SEA_PROVIDER_ORDER 时请求体带 provider.order（F 车道 429 规避）。"""
        from unittest import mock
        from sea_pilot import agents_llm
        seen = {}
        resp = {"choices": [{"message": {"content": '{"consume":[],"reason":"ok"}'}}],
                "usage": {"completion_tokens": 1}, "model": "m"}

        class FakeResp:
            def read(self): return json.dumps(resp).encode()
            def __enter__(self): return self
            def __exit__(self, *a): return False

        def fake_urlopen(req, timeout=None):
            seen["body"] = json.loads(req.data)
            return FakeResp()

        backend = agents_llm.OpenAICompatBackend.__new__(agents_llm.OpenAICompatBackend)
        backend.base_url, backend.api_key, backend.model = "http://x", "k", "m"
        with mock.patch.dict("os.environ", {"SEA_PROVIDER_ORDER": "DeepInfra,DekaLLM"}), \
             mock.patch("urllib.request.urlopen", fake_urlopen):
            backend.complete("sys", "usr")
        self.assertEqual(seen["body"].get("provider", {}).get("order"),
                         ["DeepInfra", "DekaLLM"])
        # 未设置时不带 provider 字段（C/QC 车道行为不变）
        with mock.patch("urllib.request.urlopen", fake_urlopen):
            import os as _os
            _os.environ.pop("SEA_PROVIDER_ORDER", None)
            backend.complete("sys", "usr")
        self.assertNotIn("provider", seen["body"])


class TestFailFast(unittest.TestCase):
    """规约 P-6：HTTP 4xx 确定性故障不得重试。"""

    def test_4xx_fail_fast(self):
        from unittest import mock
        import urllib.error
        from sea_pilot import agents_llm
        calls = []

        def fake_urlopen(req, timeout=None):
            calls.append(1)
            raise urllib.error.HTTPError("http://x", 400, "Bad Request", {}, None)

        backend = agents_llm.OpenAICompatBackend.__new__(agents_llm.OpenAICompatBackend)
        backend.base_url, backend.api_key, backend.model = "http://x", "k", "m"
        with mock.patch("urllib.request.urlopen", fake_urlopen), \
             mock.patch("time.sleep", lambda s: None):
            out = backend.complete("sys", "usr")
        self.assertEqual(len(calls), 1, f"4xx 不应重试，实际 {len(calls)} 次")
        self.assertIn("backend-failure", out)


class TestCompletenessGate(unittest.TestCase):
    """规约 WU-4 强化（2026-10-05 空转事故）：任务缺有效记录不得以 0 退出。"""

    def test_verify_complete(self):
        import os
        from sea_pilot.run_llm_replay import verify_complete
        with tempfile.TemporaryDirectory() as td:
            p = os.path.join(td, "x.jsonl")
            self.assertEqual(verify_complete(p, 10), 10)   # 文件缺失 = 全缺
            with open(p, "w", encoding="utf-8") as f:
                f.write(json.dumps({"picked": ["a"], "agent": 0, "day": 1}) + "\n")
                f.write(json.dumps({"picked": [], "agent": 0, "day": 2}) + "\n")
            self.assertEqual(verify_complete(p, 2), 1)     # 空选择不计
            self.assertEqual(verify_complete(p, 1), 0)     # 完整

    def test_main_exits_nonzero_when_incomplete(self):
        src = (SIM_DIR / "sea_pilot" / "run_llm_replay.py").read_text(encoding="utf-8")
        self.assertIn("verify_complete(", src)
        self.assertIn("sys.exit(1)", src)

    def test_mock_fallback_disabled_in_dispatch(self):
        """调度模式必须禁用 Mock 回退（防 Mock 数据冒充真实记录落盘）。"""
        src = (SIM_DIR / "sea_pilot" / "run_llm_replay.py").read_text(encoding="utf-8")
        self.assertIn("SEA_REQUIRE_REAL_BACKEND", src)
        runner = (SIM_DIR / "lane_runner.sh").read_text(encoding="utf-8")
        self.assertIn("SEA_REQUIRE_REAL_BACKEND=1", runner)

    def test_all_done_flag_requires_zero_failures(self):
        """规约 WU-4 强化：存在 FAILED 任务时不得盖车道总完成旗标（防假 ✅）。"""
        runner = (SIM_DIR / "lane_runner.sh").read_text(encoding="utf-8")
        self.assertIn("FAILED_COUNT", runner)
        self.assertRegex(runner, r'FAILED_COUNT"?\]?\s*-eq\s+0')


class TestProgress(unittest.TestCase):
    """规约 R-3：进度只依据旗标与 jsonl；空选择记录不计（V-3）。"""

    def test_progress_counts(self):
        from sea_pilot import dispatch_progress as dp
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            tasks_dir = tmp / "dispatch_tasks"
            tasks_dir.mkdir()
            (tasks_dir / "tasks_O.txt").write_text(
                "# comment\n"
                "sea_pilot.run_llm_replay --days 30 --agents 2 --seed 1 --tag o_r01\n"
                "sea_pilot.run_llm_replay --days 30 --agents 2 --seed 2 --tag o_r02\n"
                "sea_pilot.h9_calibration --tag o90\n", encoding="utf-8")
            results = tmp / "pilot" / "results"
            flags = results / "dispatch_flags"
            flags.mkdir(parents=True)
            line = "sea_pilot.run_llm_replay --days 30 --agents 2 --seed 1 --tag o_r01"
            key = hashlib.md5(line.encode()).hexdigest()[:12]
            (flags / f"O_{key}.done").touch()
            recs = [{"agent": 0, "day": 0, "picked": ["a"]},
                    {"agent": 0, "day": 1, "picked": ["b"]},
                    {"agent": 1, "day": 0, "picked": []}]
            with open(results / "llm_replay_o_r01.jsonl", "w", encoding="utf-8") as f:
                for r in recs:
                    f.write(json.dumps(r) + "\n")
            lane = dp.compute_progress(tmp)["O"]
            self.assertEqual(lane["tasks_total"], 3)
            self.assertEqual(lane["tasks_done"], 1)
            self.assertEqual(lane["records_done"], 2)
            self.assertGreater(lane["fraction"], 0)
            self.assertLess(lane["fraction"], 1)

    def test_render_bar(self):
        from sea_pilot import dispatch_progress as dp
        self.assertEqual(dp.render_bar(0.0, 10), "[..........]   0.0%")
        self.assertEqual(dp.render_bar(0.5, 10), "[#####.....]  50.0%")
        self.assertEqual(dp.render_bar(1.0, 10), "[##########] 100.0%")


if __name__ == "__main__":
    unittest.main()
