#!/usr/bin/env python3
"""Create the v1.13 candidate-artifact manifest and replay-shard hashes."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "docs" / "工件清单_v1.13.json"
OUT_MD = ROOT / "docs" / "工件清单_v1.13.md"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def record(path: Path) -> dict:
    return {"path": str(path.relative_to(ROOT)), "bytes": path.stat().st_size,
            "sha256": sha256(path)}


def main() -> None:
    files = [
        ROOT / "input/sovereign_epistemic_acquisition_EN_v1.13.md",
        ROOT / "RELEASE_v1.13.md", ROOT / "CITATION.cff", ROOT / "README.md",
        ROOT / "latex/SEA_EN_v1.13_draft.pdf",
        ROOT / "docs/审稿回复与修改说明_v1.13.md",
        ROOT / "docs/REPRODUCIBILITY_v1.13.md",
        ROOT / "docs/MINIMAL_VALID_EXPERIMENT_v1.13.md",
        ROOT / "docs/LITERATURE_SEARCH_v1.13.md",
        ROOT / "docs/SUPPLEMENT_NORMATIVE_AND_TRANSFER_v1.13.md",
        ROOT / "docs/SUPPLEMENT_FORMAL_AND_SECONDARY_v1.13.md",
        ROOT / "docs/SUPPLEMENT_RETROSPECTIVE_AUDITS_v1.13.md",
        ROOT / "archive/README.md",
        ROOT / "sim/pilot/results/evidence_status_v1.13.json",
        ROOT / "sim/pilot/results/governance_conformance_v1.13.json",
        ROOT / "tools/reproduce_v110_sap.py", ROOT / "tools/test_v110_sap.py",
        ROOT / "tools/reproduce_v19_math.py", ROOT / "tools/test_v19_math.py",
        ROOT / "tools/audit_v113.py", ROOT / "tools/audit_v113_report.json",
        ROOT / "tools/make_v113_manifest.py", ROOT / "tools/check_pdf_textlayer.py",
        ROOT / "tools/check_pdf_layout.py", ROOT / "tools/clean_verification_v1.13.json",
        ROOT / "tools/build_review_pdf.sh",
        ROOT / "tools/make_arxiv_source.sh",
        ROOT / "sim/sea_pilot/audit_v110_consumption_caliber.py",
        ROOT / "sim/sea_pilot/test_audit_v110_consumption_caliber.py",
        ROOT / "sim/sea_pilot/audit_v19_financial_caliber.py",
        ROOT / "sim/sea_pilot/audit_v19_upstream_digest.py",
        ROOT / "sim/sea_pilot/audit_v19_recall_value_tradeoff.py",
    ]
    for directory in (
        ROOT / "sim/theory_v1.10", ROOT / "sim/theory_v1.9",
        ROOT / "sim/sea_governance",
        ROOT / "sim/sea_sap",
        ROOT / "sim/pilot/results/sap_v1.13",
        ROOT / "sim/pilot/results/v110_consumption_caliber",
        ROOT / "sim/pilot/results/v19_financial_caliber_audit",
        ROOT / "sim/pilot/results/v19_upstream_digest_audit",
        ROOT / "sim/pilot/results/v19_recall_value_tradeoff",
    ):
        files.extend(path for path in directory.rglob("*") if path.is_file())
    for optional in (
        ROOT / "latex/arxiv_v1.13/main.tex", ROOT / "latex/SEA_v1.13_arxiv_source.tar.gz",
        ROOT / "tools/make_public.py", ROOT / "tools/publish_v113.py",
    ):
        if optional.exists():
            files.append(optional)
    files = sorted(set(files))
    missing = [str(path) for path in files if not path.exists()]
    if missing:
        raise SystemExit(f"Missing manifest inputs: {missing}")

    tag_re = re.compile(r"^(oa|od|qc|ga|o|c|q|g)_r(\d{2})([a-f])?$")
    all_replay = sorted((ROOT / "sim/pilot/results").glob("llm_replay_*.jsonl"))
    shards = [path for path in all_replay
              if tag_re.match(path.name[len("llm_replay_"):-len(".jsonl")])]
    quarantined = sorted(set(all_replay) - set(shards))
    if len(shards) != 292:
        raise SystemExit(f"Expected 292 main replay shards, found {len(shards)}")
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    dirty = bool(subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True).strip())
    target_tag = os.environ.get("SEA_TARGET_TAG") or os.environ.get("SEA_RELEASE_ID") or None
    target_commit = os.environ.get("SEA_TARGET_COMMIT") or None
    target_tag_object = None
    target_verified = False
    if target_commit is not None or os.environ.get("SEA_TARGET_TAG"):
        if not target_tag or not target_commit or not re.fullmatch(r"[0-9a-f]{40}", target_commit):
            raise SystemExit("Final provenance requires SEA_TARGET_TAG and a full 40-hex SEA_TARGET_COMMIT")
        target_tag_object = subprocess.check_output(
            ["git", "rev-parse", target_tag], cwd=ROOT, text=True).strip()
        peeled = subprocess.check_output(
            ["git", "rev-parse", f"{target_tag}^{{}}"], cwd=ROOT, text=True).strip()
        target_verified = peeled == target_commit and commit == target_commit
        if not target_verified:
            raise SystemExit(
                f"Target mismatch: tag peels to {peeled}, generation HEAD is {commit}, "
                f"requested target is {target_commit}")
        if dirty:
            raise SystemExit("Final post-tag provenance requires a clean tree before manifest generation")
    audit = json.loads((ROOT / "tools/audit_v113_report.json").read_text(encoding="utf-8"))
    info = subprocess.check_output(
        ["pdfinfo", str(ROOT / "latex/SEA_EN_v1.13_draft.pdf")], text=True)
    pages = int(re.search(r"^Pages:\s+(\d+)", info, re.M).group(1))
    manifest = {
        "schema": "sea.v113.candidate-artifact-manifest/v1",
        "release_status": os.environ.get(
            "SEA_RELEASE_STATUS", "CANDIDATE_WORKING_TREE__NOT_AN_IMMUTABLE_PUBLIC_RELEASE"),
        "generated_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "git_head_at_generation": commit,
        "git_tree_dirty_at_generation": dirty,
        "persistent_release_identifier": os.environ.get("SEA_RELEASE_ID") or None,
        "target_tag": target_tag,
        "target_commit": target_commit,
        "target_tag_object": target_tag_object,
        "target_commit_verified_against_tag": target_verified,
        "target_commit_matches_generation_head": target_verified,
        "provenance_mode": ("POST_TAG_GENERATION__PROVENANCE_COMMIT_ON_MAIN"
                            if target_verified else "PRE_RELEASE_WORKING_TREE"),
        "public_repositories": {
            "github": os.environ.get("SEA_GITHUB_URL") or None,
            "gitee": os.environ.get("SEA_GITEE_URL") or None,
        },
        "public_preregistration_url": None,
        "independent_human_mathematical_review": "pending",
        "third_party_clean_environment_reproduction": "pending",
        "direct_S2d_S4_S5_experiments": "not executed",
        "pdf_pages": pages,
        "audit_checks": {"passed": audit["n_passed"], "total": audit["n_checks"],
                         "failed": audit["n_failed"]},
        "core_files": [record(path) for path in files],
        "replay_shards": [record(path) for path in shards],
        "quarantined_non_main_replay_files": [record(path) for path in quarantined],
        "known_limitations": [
            "No independent human mathematical sign-off",
            "No S2d/S4/S5 or full matched ablation results",
            "No historical delivery/opening/attendance or efficiency observations",
            "No post-cutoff/private-corpus or completed memory audit",
            "No human participant data",
            "No v1.13-specific DOI, public experimental preregistration URL, or third-party independent reproduction",
        ],
    }
    OUT_JSON.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# v1.13 工件清单（公开候选／prerelease）", "",
        f"- 状态：`{manifest['release_status']}`",
        f"- 生成时 HEAD：`{commit}`（工作树有未提交修改：{dirty}）",
        f"- 发布标识：`{manifest['persistent_release_identifier']}`",
        f"- 目标标签：`{target_tag}`",
        f"- 目标提交：`{target_commit}`",
        f"- 标签对象：`{target_tag_object}`",
        f"- 目标提交已对标签解引用并与生成时 HEAD 核验：{target_verified}",
        f"- 溯源模式：`{manifest['provenance_mode']}`",
        f"- GitHub：{manifest['public_repositories']['github']}",
        f"- Gitee：{manifest['public_repositories']['gitee']}",
        f"- PDF：{pages} 页；一致性审计：{audit['n_passed']}/{audit['n_checks']} 通过",
        f"- 核心文件：{len(files)}；重放分片：{len(shards)}（逐文件 SHA-256 见 JSON）",
        "- 独立人类数学复审、直接匹配实验、时间外/私域语料、人类数据、公共注册、v1.13 DOI 和第三方复现均未完成。", "",
        "本清单证明生成时文件身份，不是 DOI、公共预注册、独立数学证明或第三方复核。",
        "完整逐文件哈希见 `docs/工件清单_v1.13.json`。", "",
        "| 文件 | 字节 | SHA-256 |", "|---|---:|---|",
    ]
    lines += [f"| `{r['path']}` | {r['bytes']} | `{r['sha256']}` |" for r in manifest["core_files"]]
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_JSON} and {OUT_MD}")


if __name__ == "__main__":
    main()
