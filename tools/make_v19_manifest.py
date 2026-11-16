#!/usr/bin/env python3
"""Create a transparent v1.9 working-artifact manifest (not an immutable release)."""
from __future__ import annotations

import datetime as dt
import hashlib
import os
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "docs" / "工件清单_v1.9.json"
OUT_MD = ROOT / "docs" / "工件清单_v1.9.md"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def record(path: Path) -> dict:
    return {"path": str(path.relative_to(ROOT)), "bytes": path.stat().st_size,
            "sha256": sha256(path)}


def main() -> None:
    files = [
        ROOT / "input/sovereign_epistemic_acquisition_EN_v1.9.md",
        ROOT / "RELEASE_v1.9.md",
        ROOT / "CITATION.cff",
        ROOT / "README.md",
        ROOT / "latex/SEA_EN_v1.9_draft.pdf",
        ROOT / "docs/审稿回复与修改说明_v1.9.md",
        ROOT / "docs/REPRODUCIBILITY_v1.9.md",
        ROOT / "docs/MINIMAL_VALID_EXPERIMENT_v1.9.md",
        ROOT / "docs/LITERATURE_SEARCH_v1.9.md",
        ROOT / "sim/pilot/results/evidence_status_v1.9.json",
        ROOT / "tools/reproduce_v19_math.py",
        ROOT / "tools/test_v19_math.py",
        ROOT / "tools/audit_v19.py",
        ROOT / "tools/audit_v19_report.json",
        ROOT / "tools/make_v19_manifest.py",
        ROOT / "tools/check_pdf_textlayer.py",
        ROOT / "tools/build_review_pdf.sh",
        ROOT / "tools/make_arxiv_source.sh",
        ROOT / "sim/sea_pilot/audit_v19_financial_caliber.py",
        ROOT / "sim/sea_pilot/audit_v19_upstream_digest.py",
        ROOT / "sim/sea_pilot/audit_v19_recall_value_tradeoff.py",
    ]
    for directory in (ROOT / "sim/theory_v1.9", ROOT / "sim/pilot/results/v19_financial_caliber_audit",
                      ROOT / "sim/pilot/results/v19_upstream_digest_audit",
                      ROOT / "sim/pilot/results/v19_recall_value_tradeoff"):
        files.extend(p for p in directory.rglob("*") if p.is_file())
    for optional in (ROOT / "latex/arxiv_v1.9/main.tex", ROOT / "latex/SEA_v1.9_arxiv_source.tar.gz",
                     ROOT / "tools/make_public.py", ROOT / "tools/publish_v19.py"):
        if optional.exists():
            files.append(optional)
    files = sorted(set(files))
    missing = [str(p) for p in files if not p.exists()]
    if missing:
        raise SystemExit(f"Missing manifest inputs: {missing}")

    tag_re = re.compile(r"^(oa|od|qc|ga|o|c|q|g)_r(\d{2})([a-f])?$")
    all_replay_files = sorted((ROOT / "sim/pilot/results").glob("llm_replay_*.jsonl"))
    shards = [p for p in all_replay_files
              if tag_re.match(p.name[len("llm_replay_"):-len(".jsonl")])]
    quarantined = sorted(set(all_replay_files) - set(shards))
    if len(shards) != 292:
        raise SystemExit(f"Expected 292 main replay shards, found {len(shards)}")
    shard_records = [record(p) for p in shards]
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    dirty = bool(subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True).strip())
    audit = json.loads((ROOT / "tools/audit_v19_report.json").read_text())
    pages = None
    pdf = ROOT / "latex/SEA_EN_v1.9_draft.pdf"
    if pdf.exists():
        info = subprocess.check_output(["pdfinfo", str(pdf)], text=True)
        pages = int(re.search(r"^Pages:\s+(\d+)", info, re.M).group(1))
    manifest = {
        "schema": "sea.v19.working-artifact-manifest/v1",
        "release_status": os.environ.get(
            "SEA_RELEASE_STATUS", "CANDIDATE_WORKING_TREE__NOT_AN_IMMUTABLE_PUBLIC_RELEASE"),
        "generated_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "git_head_at_generation": commit,
        "git_tree_dirty_at_generation": dirty,
        "persistent_release_identifier": os.environ.get("SEA_RELEASE_ID") or None,
        "public_repositories": {
            "github": os.environ.get("SEA_GITHUB_URL") or None,
            "gitee": os.environ.get("SEA_GITEE_URL") or None,
        },
        "public_preregistration_url": None,
        "independent_human_mathematical_review": "pending",
        "direct_S2d_S4_S5_experiments": "not executed",
        "pdf_pages": pages,
        "audit_checks": {"passed": audit["n_checks"] - audit["n_failed"],
                         "total": audit["n_checks"], "failed": audit["n_failed"]},
        "core_files": [record(p) for p in files],
        "replay_shards": shard_records,
        "quarantined_non_main_replay_files": [record(p) for p in quarantined],
        "known_limitations": [
            "No independent human mathematical sign-off",
            "No S2d/S4/S5 or full matched ablation results",
            "No post-cutoff/private-corpus or completed memory audit",
            "No human participant data",
            "No immutable public v1.9 archive or public preregistration URL",
        ],
    }
    OUT_JSON.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# v1.9 工件清单（候选工作树，非不可变发布）", "",
        f"- 状态：`{manifest['release_status']}`",
        f"- 生成时 HEAD：`{commit}`（工作树有未提交修改：{dirty}）",
        f"- 发布标识：`{manifest['persistent_release_identifier']}`",
        f"- GitHub：{manifest['public_repositories']['github']}",
        f"- Gitee：{manifest['public_repositories']['gitee']}",
        f"- PDF：{pages} 页；一致性审计：{audit['n_checks']-audit['n_failed']}/{audit['n_checks']} 通过",
        f"- 核心文件：{len(files)}；重放分片：{len(shards)}（逐文件 SHA-256 见 JSON）",
        "- 独立人类数学复审、S2d/S4/S5、时间外/私域语料、人类数据、公共注册和持久发布标识均未完成。", "",
        "本清单只证明生成时工作树中文件的身份，不是 DOI、公共预注册或第三方复核。",
        "完整逐文件哈希见 `docs/工件清单_v1.9.json`。", "",
        "| 文件 | 字节 | SHA-256 |", "|---|---:|---|",
    ]
    lines += [f"| `{r['path']}` | {r['bytes']} | `{r['sha256']}` |" for r in manifest["core_files"]]
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_JSON} and {OUT_MD}")


if __name__ == "__main__":
    main()
