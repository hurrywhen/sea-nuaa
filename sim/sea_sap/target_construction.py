"""Small synthetic target-construction audit and granularity sensitivity.

This module does not create human annotations.  It reports agreement between two
*deterministic extraction rules*, a frozen arbitration rule, and a merge/split
sensitivity example.  Independent human target validation remains pending.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Mapping

FIXTURE_PATH = Path(__file__).resolve().parent / "fixtures" / "target_construction.json"
TEMPLATE_PATH = Path(__file__).resolve().parent / "fixtures" / "target_construction_human_validation_template.csv"


def _sha(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(",", ":")).encode("utf-8")).hexdigest()


def load_target_fixture(path: Path | None = None) -> dict[str, Any]:
    document = json.loads((path or FIXTURE_PATH).read_text(encoding="utf-8"))
    if document.get("evidence_scope") != "SYNTHETIC_TARGET_CONSTRUCTION__HUMAN_VALIDATION_PENDING":
        raise ValueError("unexpected target-construction evidence scope")
    units = document["candidate_units"]
    if len(units) != len(set(units)):
        raise ValueError("duplicate candidate proposition units")
    for rule in document["extractor_rules"].values():
        if not set(rule["included"]) <= set(units):
            raise ValueError("extractor included unknown proposition unit")
    fine_ids = [target["target_id"] for target in document["fine_targets"]]
    if set(document["adjudication"]["accepted_fine"]) != set(fine_ids):
        raise ValueError("adjudicated fine targets must match fine registry")
    weights = [target["weight"] for target in document["fine_targets"]]
    if not math.isclose(sum(weights), 1.0, rel_tol=0, abs_tol=1e-12):
        raise ValueError("fine target weights must sum to one")
    return document


def cohens_kappa(labels_a: Mapping[str, bool], labels_b: Mapping[str, bool]) -> dict[str, Any]:
    units = sorted(set(labels_a) | set(labels_b))
    if not units:
        raise ValueError("no units")
    a = [bool(labels_a.get(unit, False)) for unit in units]
    b = [bool(labels_b.get(unit, False)) for unit in units]
    observed = sum(x == y for x, y in zip(a, b)) / len(units)
    pa = sum(a) / len(units)
    pb = sum(b) / len(units)
    expected = pa * pb + (1 - pa) * (1 - pb)
    kappa = None if math.isclose(expected, 1.0) else (observed - expected) / (1 - expected)
    return {
        "n_units": len(units), "observed_agreement": observed,
        "expected_agreement_by_marginals": expected, "cohens_kappa": kappa,
        "disagreements": [unit for unit, x, y in zip(units, a, b) if x != y],
        "interpretation": "Agreement between deterministic extraction rules, not human reviewers.",
    }


def granularity_sensitivity(fixture: Mapping[str, Any]) -> dict[str, Any]:
    consumption = fixture["synthetic_consumption_fine"]
    fine_omission = sum(target["weight"] * (1 - int(consumption[target["target_id"]]))
                        for target in fixture["fine_targets"])
    coarse_omission = 0.0
    coarse_rows = []
    for group in fixture["coarse_groups"]:
        consumed = any(int(consumption[member]) for member in group["members"])
        coarse_omission += group["weight"] * (1 - int(consumed))
        coarse_rows.append({"group_id": group["group_id"], "members": group["members"],
                            "weight": group["weight"], "coarse_consumed": int(consumed)})
    return {
        "fine_weighted_omission": fine_omission,
        "coarse_weighted_omission": coarse_omission,
        "coarse_rows": coarse_rows,
        "interpretation": (
            "Merging propositions changes the terminal event to ANY-member consumption. "
            "Weighted omission is not invariant under merge/split unless target weights, "
            "mapping and consumption events are jointly aligned. Version changes create "
            "new SAP instances and are not pooled."
        ),
    }


def audit_target_construction() -> dict[str, Any]:
    fixture = load_target_fixture()
    rules = fixture["extractor_rules"]
    units = fixture["candidate_units"]
    labels = {name: {unit: unit in rule["included"] for unit in units}
              for name, rule in rules.items()}
    names = sorted(labels)
    agreement = cohens_kappa(labels[names[0]], labels[names[1]])
    return {
        "schema": "sea.target-construction-audit/v1",
        "status": "SYNTHETIC_RULE_AGREEMENT_AND_ARBITRATION__INDEPENDENT_HUMAN_VALIDATION_PENDING",
        "fixture_sha256": _sha(fixture),
        "reference_documents": fixture["documents"],
        "extractor_rules": rules,
        "rule_agreement": agreement,
        "adjudication": fixture["adjudication"],
        "fine_targets": fixture["fine_targets"],
        "coarse_groups": fixture["coarse_groups"],
        "granularity_sensitivity": granularity_sensitivity(fixture),
        "dynamic_target_rule": "NEW_SAP_INSTANCE__NO_CROSS_VERSION_POOLING",
        "human_validation_template": str(TEMPLATE_PATH.relative_to(Path(__file__).resolve().parents[2])),
        "human_annotations_created": False,
        "availability_reference_rule": (
            "Availability is relative to a frozen reference corpus snapshot with content hashes "
            "and evidence pointers. Closed-snapshot absence is not open-world nonexistence."
        ),
    }


def write_human_validation_template(path: Path | None = None) -> Path:
    fixture = load_target_fixture()
    target = path or TEMPLATE_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["document_id", "proposition_id", "canonical_text",
                         "annotator_1_label", "annotator_2_label", "arbitration", "notes"])
        for document in fixture["documents"]:
            for unit in fixture["candidate_units"]:
                writer.writerow([document["document_id"], unit, "", "", "", "", ""])
    return target
