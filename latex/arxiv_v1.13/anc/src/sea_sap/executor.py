"""Minimal longitudinal SAP executor for deterministic synthetic fixtures.

This is an executable *small instance* of the v1.13 SAP interface, not a general
optimizer, an LLM experiment, or deployment-effectiveness evidence.  It keeps
latent actual consumption unobserved.  Operational attendance, the synthetic
machine ingestion-and-task-reference placeholder, and the failure-composite
endpoint are distinct.  The executable ledger is operational/FC, not latent.
"""
from __future__ import annotations

import copy
from dataclasses import dataclass
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Iterable, Mapping, Optional, Sequence

from sea_governance import (
    Authorization,
    GovernanceReference,
    canonical_json,
    domain_digest,
    proposal_digest,
)

RESOURCE_NAMES = ("time", "compute", "calls", "money", "risk")
STAGE_NAMES = ("availability", "linkage", "quota", "delivery", "opening", "attendance")
FIXTURE_PATH = Path(__file__).resolve().parent / "fixtures" / "longitudinal.json"
DYNAMIC_RULES = {
    "NEW_EVALUATION_COHORT__NO_CROSS_VERSION_POOLING",
    "NEW_SAP_INSTANCE__NO_CROSS_VERSION_POOLING",
}


def _detached(value: Any) -> Any:
    return copy.deepcopy(value)


def _sha(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _nonnegative_int(value: Any, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{name} must be a nonnegative integer")
    return value


def load_fixture(path: Optional[Path] = None) -> dict[str, Any]:
    """Load and validate the public, entirely synthetic longitudinal fixture."""
    document = json.loads((path or FIXTURE_PATH).read_text(encoding="utf-8"))
    if document.get("evidence_scope") != "SYNTHETIC_FIXTURE__NOT_HUMAN_OR_DEPLOYMENT_DATA":
        raise ValueError("unexpected fixture evidence scope")
    if not document.get("run_id") or not document.get("target_registry"):
        raise ValueError("fixture requires run_id and target_registry")
    validate_target_registry(document["target_registry"])
    candidates = document.get("candidates", [])
    ids = [item["candidate_id"] for item in candidates]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate candidate IDs")
    links = document["target_registry"]["candidate_target_links"]
    if any(candidate["candidate_id"] not in links for candidate in candidates):
        raise ValueError("every raw candidate needs an explicit target-link entry")
    for field in ("reference_link_truth", "staged_link_pass"):
        table = document.get(field, {})
        for candidate_id, targets in links.items():
            for target in targets:
                if target not in table.get(candidate_id, {}):
                    raise ValueError(f"every candidate-target link needs an explicit {field} entry")
    for candidate in candidates:
        if set(candidate["features"]) != {
            "relevance", "novelty", "credibility", "durability", "harm_avoidance"
        }:
            raise ValueError("candidate feature schema does not match governance reference")
        for value in candidate["features"].values():
            _nonnegative_int(value, "candidate feature")
    return _detached(document)


def validate_target_registry(registry: Mapping[str, Any]) -> None:
    """Validate one immutable target population, mapping and reference snapshot."""
    required = {
        "version", "reference_corpus", "targets", "candidate_target_links",
        "availability", "construction_rule", "dynamic_version_rule",
    }
    if set(registry) != required:
        raise ValueError(f"target registry fields must be exactly {sorted(required)}")
    reference = registry["reference_corpus"]
    if not reference.get("snapshot_id") or not reference.get("sha256"):
        raise ValueError("reference corpus needs snapshot identity and hash")
    if reference.get("availability_universe") not in {"closed_snapshot", "open_world"}:
        raise ValueError("availability universe must be declared")
    documents = reference.get("documents")
    if not isinstance(documents, list) or not documents:
        raise ValueError("reference corpus must list auditable source documents")
    document_ids = []
    for document in documents:
        if not document.get("document_id") or not document.get("content_sha256") or not document.get("evidence_pointer"):
            raise ValueError("reference document needs identity, content hash and evidence")
        _nonnegative_int(document.get("first_available_period"), "first_available_period")
        document_ids.append(document["document_id"])
    if len(document_ids) != len(set(document_ids)):
        raise ValueError("duplicate reference document IDs")
    if _sha(documents) != reference["sha256"]:
        raise ValueError("reference corpus hash does not match its documents")
    targets = registry["targets"]
    if not targets:
        raise ValueError("target set cannot be empty")
    target_ids = [target["target_id"] for target in targets]
    if len(target_ids) != len(set(target_ids)):
        raise ValueError("duplicate target IDs")
    weights = [target["weight"] for target in targets]
    if any(isinstance(weight, bool) or not isinstance(weight, (int, float)) or weight <= 0
           for weight in weights):
        raise ValueError("target weights must be positive numbers")
    if not math.isclose(sum(weights), 1.0, rel_tol=0, abs_tol=1e-12):
        raise ValueError("target weights must sum to one")
    for target in targets:
        if not target.get("canonical_text") or not target.get("construction_evidence"):
            raise ValueError("each target needs canonical text and construction evidence")
    for candidate_id, linked in registry["candidate_target_links"].items():
        if not candidate_id or not isinstance(linked, list):
            raise ValueError("candidate_target_links must map IDs to lists")
        if len(linked) != len(set(linked)) or any(target not in target_ids for target in linked):
            raise ValueError("invalid or duplicate target link")
        availability = registry["availability"].get(candidate_id)
        if not isinstance(availability, dict):
            raise ValueError("every linked candidate needs availability evidence")
        for target in linked:
            evidence = availability.get(target)
            if not isinstance(evidence, dict):
                raise ValueError("missing candidate-target availability evidence")
            if evidence.get("status") not in {"available", "unavailable_in_closed_snapshot", "unknown"}:
                raise ValueError("invalid availability status")
            if not evidence.get("evidence_pointer"):
                raise ValueError("availability needs an evidence pointer")
            if evidence["status"] == "available":
                document_id = evidence.get("reference_document_id")
                if document_id not in document_ids:
                    raise ValueError("available item must cite a reference document")
                source = next(item for item in documents if item["document_id"] == document_id)
                if evidence.get("content_sha256") != source["content_sha256"]:
                    raise ValueError("availability content hash must match reference document")
            elif evidence["status"] == "unavailable_in_closed_snapshot":
                if not evidence.get("absence_audit_id"):
                    raise ValueError("closed-snapshot absence needs an absence audit identifier")
            if (reference["availability_universe"] == "open_world"
                    and evidence["status"] == "unavailable_in_closed_snapshot"):
                raise ValueError("open-world absence cannot be asserted from a closed snapshot")
    if registry["dynamic_version_rule"] not in DYNAMIC_RULES:
        raise ValueError("dynamic targets require a declared no-cross-version-pooling rule")


def symmetric_binary_posterior(signal: int, *, prior_milli: int = 500,
                               accuracy_milli: int = 800) -> int:
    """One frozen update kernel, in integer milli-probabilities, for every signal."""
    if signal not in {0, 1}:
        raise ValueError("binary signal required")
    if not (0 < prior_milli < 1000 and 500 < accuracy_milli < 1000):
        raise ValueError("invalid prior or accuracy")
    if signal == 1:
        numerator = accuracy_milli * prior_milli
        denominator = numerator + (1000 - accuracy_milli) * (1000 - prior_milli)
    else:
        numerator = (1000 - accuracy_milli) * prior_milli
        denominator = numerator + accuracy_milli * (1000 - prior_milli)
    return round(numerator / denominator * 1000)


@dataclass(frozen=True)
class AttendanceDecision:
    status: str  # positive, negative, unknown
    reading_event: Optional[bool]
    content_linked_confirmation: Optional[bool]
    reason: str


class OperationalAttendanceInstrument:
    """Frozen AND rule for *operational attendance*, not latent comprehension.

    Positive requires a valid reading event AND content-linked confirmation.
    A complete, validated (or explicitly synthetic-fixture) measurement without
    that conjunction is negative.  Missing/invalid telemetry is unknown.
    """

    def __init__(self, registry: Mapping[str, Any]):
        self.registry = _detached(registry)
        required = {
            "instrument_id", "version", "decision_rule", "thresholds",
            "validation_status", "assessor_blinding", "sensitivity_versions",
        }
        if set(registry) != required:
            raise ValueError("invalid attendance instrument registry")
        if registry["decision_rule"] != "VALID_READING_AND_CONTENT_LINKED_CONFIRMATION":
            raise ValueError("primary attendance rule must be explicit AND")
        if registry["validation_status"] not in {"validated", "synthetic_fixture_only"}:
            raise ValueError("attendance instrument is not validated")
        if registry["assessor_blinding"] not in {
            "arm_and_model_blind", "not_applicable_synthetic_fixture"
        }:
            raise ValueError("assessor blinding requirement is not met")

    def measure(self, event: Mapping[str, Any]) -> AttendanceDecision:
        if event.get("measurement_status") != "complete":
            return AttendanceDecision("unknown", None, None, "measurement_incomplete_or_failed")
        required = {
            "focused_visible", "engaged_ms", "coverage_fraction",
            "content_linked_confirmation", "evidence_pointer",
        }
        if not required <= set(event):
            return AttendanceDecision("unknown", None, None, "missing_telemetry_fields")
        thresholds = self.registry["thresholds"]
        try:
            reading = (
                event["focused_visible"] is True
                and float(event["engaged_ms"]) >= float(thresholds["min_engaged_ms"])
                and float(event["coverage_fraction"]) >= float(thresholds["min_coverage_fraction"])
            )
            confirmation = event["content_linked_confirmation"]
            if not isinstance(confirmation, bool):
                raise ValueError("confirmation must be Boolean")
        except (TypeError, ValueError):
            return AttendanceDecision("unknown", None, None, "invalid_telemetry_values")
        positive = reading and confirmation
        return AttendanceDecision(
            "positive" if positive else "negative", reading, confirmation,
            "frozen_AND_rule_positive" if positive else "complete_measurement_AND_rule_not_met",
        )


def machine_ingestion_and_task_reference(event: Mapping[str, Any]) -> bool:
    """Synthetic placeholder predicate for machine ingestion-and-task-reference.

    This checks only that the fixture supplies three 64-character hash strings
    and that the task-reference string equals the context-receipt string.  It is
    not a cryptographic proof that a real task operation referenced the content.
    Real logs require a bound evidence structure linking content, receipt, and
    task operation; this predicate never measures human attention or information use.
    """
    required = {"content_sha256", "context_receipt_sha256", "task_reference_sha256"}
    if not required <= set(event):
        return False
    values = [event[field] for field in sorted(required)]
    if any(not isinstance(value, str) or len(value) != 64 for value in values):
        return False
    return (event["context_receipt_sha256"] == event["task_reference_sha256"]
            and event["content_sha256"] != event["context_receipt_sha256"])


def operational_attendance_contrast_bounds(
    weighted_fc_omission: Mapping[str, float], weighted_unknown: Mapping[str, float],
) -> dict[str, Any]:
    """Sharp arm-specific bounds for *operational attendance omission*, not latent D.

    Unknown operational outcomes may be assigned to operational success or
    failure.  No independence or MAR assumption is made.  These bounds do NOT
    identify latent actual-consumption omission unless an additional measurement
    consistency assumption is imposed (e.g., non-unknown Z perfectly classifies D).
    With false positives or false negatives, latent omission can lie outside them.
    """
    if set(weighted_fc_omission) != {"sea", "control"} or set(weighted_unknown) != {"sea", "control"}:
        raise ValueError("both sea and control are required")
    sea_fc = float(weighted_fc_omission["sea"])
    control_fc = float(weighted_fc_omission["control"])
    sea_u = float(weighted_unknown["sea"])
    control_u = float(weighted_unknown["control"])
    for value in (sea_fc, control_fc, sea_u, control_u):
        if not 0 <= value <= 1:
            raise ValueError("weighted rates must lie in [0,1]")
    if sea_u > sea_fc + 1e-12 or control_u > control_fc + 1e-12:
        raise ValueError("unknowns are a subset of failure-composite omissions")
    fc_contrast = sea_fc - control_fc
    return {
        "estimand": "operational_attendance_omission_contrast_not_latent_actual_consumption",
        "sea_minus_control_fc": fc_contrast,
        "lower_sea_unknown_operational_success_control_unknown_failure": fc_contrast - sea_u,
        "upper_sea_unknown_operational_failure_control_unknown_success": fc_contrast + control_u,
        "weighted_unknown_sea": sea_u,
        "weighted_unknown_control": control_u,
        "latent_bounds_require_measurement_error_assumptions": True,
    }


# Backwards-compatible name; the estimand is operational attendance omission.
failure_composite_contrast_bounds = operational_attendance_contrast_bounds


class SAPExecutor:
    """Execute a small target registry under one control history and evaluation cohort."""

    def __init__(self, fixture: Mapping[str, Any], *, arm: str = "sea"):
        self.fixture = _detached(fixture)
        self.registry = _detached(fixture["target_registry"])
        validate_target_registry(self.registry)
        self.arm = arm
        self.control_instance_id = domain_digest("sea-sap-control-instance/1", {
            "run_id": fixture["run_id"], "arm": arm,
        })
        self.evaluation_cohort_id = domain_digest("sea-sap-evaluation-cohort/1", {
            "control_instance_id": self.control_instance_id, "target_registry": self.registry,
        })
        self.instance_id = self.evaluation_cohort_id
        self.governance = GovernanceReference()
        self.budget_remaining = {
            name: _nonnegative_int(fixture["initial_budget"][name], f"budget.{name}")
            for name in RESOURCE_NAMES
        }
        self.budget_spent = {name: 0 for name in RESOURCE_NAMES}
        self.history: list[dict[str, Any]] = []
        self.period_results: list[dict[str, Any]] = []
        self.updated_candidates: dict[str, list[dict[str, Any]]] = {}
        self._document_by_id = {
            doc["document_id"]: doc for doc in self.registry["reference_corpus"]["documents"]
        }

    def fork_for_target_registry(self, registry: Mapping[str, Any]) -> "SAPExecutor":
        """Full reset: a new control instance and evaluation cohort.

        This is an evaluation-protocol choice, not a theorem that SAP control must
        reset.  Use continue_with_target_registry to preserve control continuity.
        """
        validate_target_registry(registry)
        fixture = _detached(self.fixture)
        fixture["run_id"] = f"{self.fixture['run_id']}:{registry['version']}"
        fixture["target_registry"] = _detached(registry)
        return SAPExecutor(fixture, arm=self.arm)

    def continue_with_target_registry(self, registry: Mapping[str, Any]) -> "SAPExecutor":
        """Preserve objective/authorization/audit/budget control; start a new evaluation cohort."""
        validate_target_registry(registry)
        fixture = _detached(self.fixture)
        fixture["target_registry"] = _detached(registry)
        continued = SAPExecutor(fixture, arm=self.arm)
        continued.control_instance_id = self.control_instance_id
        continued.governance = self.governance
        continued.budget_remaining = dict(self.budget_remaining)
        continued.budget_spent = dict(self.budget_spent)
        continued.history = _detached(self.history)
        continued.updated_candidates = _detached(self.updated_candidates)
        continued.governance.append_record("evaluation_cohort_change", {
            "old_target_registry_version": self.registry["version"],
            "new_target_registry_version": registry["version"],
            "control_continuity": True,
            "cross_version_pooling_allowed": False,
        }, evidence=[f"fixture:{self.fixture['run_id']}:evaluation-cohort:{registry['version']}"])
        return continued

    def _available_targets(self, candidate_id: str, period: int) -> list[str]:
        links = self.registry["candidate_target_links"][candidate_id]
        availability = self.registry["availability"][candidate_id]
        available = []
        for target in links:
            evidence = availability[target]
            if evidence["status"] != "available":
                continue
            source = self._document_by_id[evidence["reference_document_id"]]
            # first_available_period is persistent: available from that period onward.
            if period >= source["first_available_period"]:
                available.append(target)
        return available

    def _spend(self, cost: Mapping[str, int], *, period: int, stage: str) -> None:
        if set(cost) - set(RESOURCE_NAMES):
            raise ValueError("unknown resource coordinate")
        normalized = {name: _nonnegative_int(cost.get(name, 0), f"cost.{name}")
                      for name in RESOURCE_NAMES}
        if any(normalized[name] > self.budget_remaining[name] for name in RESOURCE_NAMES):
            raise RuntimeError(f"resource-infeasible action at period {period}, stage {stage}")
        before = dict(self.budget_remaining)
        for name in RESOURCE_NAMES:
            self.budget_remaining[name] -= normalized[name]
            self.budget_spent[name] += normalized[name]
        self.governance.append_record("resource_use", {
            "period": period, "stage": stage, "cost": normalized,
            "before": before, "after": dict(self.budget_remaining),
            "measurement_scope": "simulated resource units; no real model calls or fees",
        }, evidence=[f"fixture:{self.fixture['run_id']}:resources:{period}:{stage}"])

    def _precheck_period_resources(self, period: int, plan: Mapping[str, Any]) -> None:
        """Conservative whole-period precheck before any state mutation.

        It budgets the maximum declared selection limit and the planned terminal
        events.  If it fails, no observation, update, spend, or ledger event is
        appended.  Selection may later use fewer resources, but partial execution
        after a late budget failure is not the declared semantics.
        """
        costs = self.fixture["resource_costs"]
        required = {name: 0 for name in RESOURCE_NAMES}
        def add(cost: Mapping[str, int], multiplier: int = 1) -> None:
            for name in RESOURCE_NAMES:
                required[name] += _nonnegative_int(cost.get(name, 0), f"cost.{name}") * multiplier
        add(self.fixture["update_kernel"]["cost_per_candidate"], len(self.fixture["candidates"]))
        add(costs["linkage_per_period"])
        add(costs["selection_per_candidate"], self.fixture["selection_limit"])
        add(costs["delivery_per_candidate"], len(plan.get("delivered", [])))
        add(costs["attendance_per_candidate"], len(plan.get("opened", [])))
        if any(required[name] > self.budget_remaining[name] for name in RESOURCE_NAMES):
            raise RuntimeError(f"whole-period resource precheck failed at period {period}")
        self.governance.append_record("resource_precheck", {
            "period": period, "required_upper_bound": required,
            "remaining_before": dict(self.budget_remaining),
            "semantics": "conservative whole-period precheck before mutation",
        }, evidence=[f"fixture:{self.fixture['run_id']}:resource-precheck:{period}"])

    def _update(self, period: int) -> list[dict[str, Any]]:
        updated = []
        kernel = self.fixture["update_kernel"]
        for raw in self.fixture["candidates"]:
            posterior = symmetric_binary_posterior(
                raw["signal"], prior_milli=kernel["prior_milli"],
                accuracy_milli=kernel["accuracy_milli"],
            )
            self._spend(kernel["cost_per_candidate"], period=period, stage="update")
            candidate = _detached(raw)
            candidate["posterior_relevance_milli"] = posterior
            candidate["features"] = dict(raw["features"])
            candidate["features"]["relevance"] = (
                raw["features"]["relevance"] * posterior // 1000
            )
            candidate["provenance"] = f"fixture:{self.fixture['run_id']}:{raw['candidate_id']}"
            updated.append(candidate)
        self.updated_candidates[str(period)] = _detached(updated)
        self.governance.append_record("update", {
            "period": period, "kernel": "symmetric_binary/1",
            "posteriors_milli": {
                item["candidate_id"]: item["posterior_relevance_milli"] for item in updated
            },
            "same_kernel_for_every_signal": True,
        }, evidence=[f"fixture:{self.fixture['run_id']}:update-kernel"])
        return updated

    def _eligible(self, candidates: Sequence[Mapping[str, Any]], period: int) -> tuple[list[dict[str, Any]], dict]:
        links = self.registry["candidate_target_links"]
        staged = self.fixture["staged_link_pass"]
        truth = self.fixture["reference_link_truth"]
        link_audit = {}
        eligible = []
        for candidate in candidates:
            candidate_id = candidate["candidate_id"]
            target_links = links[candidate_id]
            available_targets = self._available_targets(candidate_id, period)
            staged_linked = [
                target for target in available_targets
                if staged.get(candidate_id, {}).get(target, False)
            ]
            reference_linked = [
                target for target in available_targets
                if truth.get(candidate_id, {}).get(target, False)
            ]
            link_audit[candidate_id] = {
                "available_targets": available_targets,
                "staged_linked_targets": staged_linked,
                "reference_linked_targets": reference_linked,
            }
            # SEA selection uses its staged linkage result.  S2d bypasses staged
            # selection filtering, but evaluation uses arm-independent reference truth.
            if self.arm == "s2d" or staged_linked:
                item = _detached(candidate)
                item["linked_targets"] = staged_linked if self.arm == "sea" else reference_linked
                eligible.append(item)
        return eligible, link_audit

    def _selection_cost(self) -> dict[str, int]:
        return _detached(self.fixture["resource_costs"]["selection_per_candidate"])

    @staticmethod
    def _governance_candidates(eligible: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
        return [{
            "candidate_id": item["candidate_id"], "topic": item["topic"],
            "features": item["features"], "provenance": item["provenance"],
        } for item in eligible]

    def _select(self, period: int, eligible: Sequence[Mapping[str, Any]]) -> tuple[list[dict], list[dict]]:
        user_state = _detached(self.fixture["user_state"])
        ranking = self.governance.rank(
            self._governance_candidates(eligible), user_state,
            self.fixture.get("platform_variables", {}),
            evidence=[f"fixture:{self.fixture['run_id']}:rank:{period}"],
        )
        by_id = {candidate["candidate_id"]: candidate for candidate in eligible}
        selected = []
        covered = set()
        limit = self.fixture["selection_limit"]
        for row in ranking:
            if len(selected) >= limit:
                break
            candidate = by_id[row["candidate_id"]]
            targets = set(candidate["linked_targets"])
            if self.arm == "sea" and targets and targets <= covered:
                continue
            cost = self._selection_cost()
            if any(cost.get(name, 0) > self.budget_remaining[name] for name in RESOURCE_NAMES):
                continue
            self._spend(cost, period=period, stage="selection")
            selected.append(candidate)
            covered.update(targets)
        self.governance.append_record("selection", {
            "period": period, "arm": self.arm,
            "selected_candidate_ids": [item["candidate_id"] for item in selected],
            "covered_linked_targets": sorted(covered), "selection_rule": "ranked_feasible_greedy",
            "selection_link_rule": "staged_link_pass" if self.arm == "sea" else "raw_candidates_no_staged_filter",
        }, evidence=[f"fixture:{self.fixture['run_id']}:selection:{period}"])
        return selected, ranking

    def _target_outcomes(self, selected: Sequence[Mapping[str, Any]], plan: Mapping[str, Any],
                         instrument: OperationalAttendanceInstrument, period: int) -> tuple[list[dict], dict]:
        selected_ids = {item["candidate_id"] for item in selected}
        delivered = set(plan.get("delivered", []))
        opened = set(plan.get("opened", []))
        attendance_events = plan.get("attendance_events", {})
        if not opened <= delivered or not delivered <= selected_ids:
            raise ValueError("stage events must satisfy selected ⊇ delivered ⊇ opened")
        decisions = {}
        machine_flags = {}
        for candidate_id in opened:
            event = attendance_events.get(candidate_id, {"measurement_status": "not_attempted"})
            decisions[candidate_id] = instrument.measure(event)
            machine_flags[candidate_id] = machine_ingestion_and_task_reference(
                plan.get("machine_events", {}).get(candidate_id, {}))
        links = self.registry["candidate_target_links"]
        truth = self.fixture["reference_link_truth"]
        rows = []
        unknown_weight = 0.0
        fc_omission = 0.0
        operational_negative_weight = 0.0
        missing_by_reason: dict[str, float] = {}
        for target in self.registry["targets"]:
            target_id = target["target_id"]
            candidates = [candidate for candidate in self.fixture["candidates"]
                          if target_id in links[candidate["candidate_id"]]]
            available = [candidate["candidate_id"] for candidate in candidates
                         if target_id in self._available_targets(candidate["candidate_id"], period)]
            linked = [candidate_id for candidate_id in available
                      if truth.get(candidate_id, {}).get(target_id, False)]
            selected_linked = [candidate_id for candidate_id in linked if candidate_id in selected_ids]
            delivered_linked = [candidate_id for candidate_id in selected_linked if candidate_id in delivered]
            opened_linked = [candidate_id for candidate_id in delivered_linked if candidate_id in opened]
            positive = any(decisions[candidate_id].status == "positive" for candidate_id in opened_linked)
            unknown = (not positive and any(decisions[candidate_id].status == "unknown"
                                            for candidate_id in opened_linked))
            if positive:
                first_failure = None
                operational = "positive"
            elif not available:
                first_failure = "availability"
                operational = "not_applicable"
            elif not linked:
                first_failure = "linkage"
                operational = "not_applicable"
            elif not selected_linked:
                first_failure = "quota"
                operational = "not_applicable"
            elif not delivered_linked:
                first_failure = "delivery"
                operational = "not_applicable"
            elif not opened_linked:
                first_failure = "opening"
                operational = "not_applicable"
            else:
                first_failure = "attendance"
                operational = "unknown" if unknown else "negative"
            omitted_fc = not positive
            weight = float(target["weight"])
            if omitted_fc:
                fc_omission += weight
            if operational == "negative":
                operational_negative_weight += weight
            if unknown:
                unknown_weight += weight
                reason = next(decisions[candidate_id].reason for candidate_id in opened_linked
                              if decisions[candidate_id].status == "unknown")
                missing_by_reason[reason] = missing_by_reason.get(reason, 0.0) + weight
            rows.append({
                "target_id": target_id, "weight": weight,
                "available_candidate_ids": available, "linked_candidate_ids": linked,
                "selected_candidate_ids": selected_linked,
                "delivered_candidate_ids": delivered_linked, "opened_candidate_ids": opened_linked,
                "operational_attendance": operational,
                "latent_actual_consumption": None,
                "failure_composite_omission": int(omitted_fc),
                "first_failed_stage": first_failure,
            })
        summary = {
            "ledger_scope": "OPERATIONAL_ATTENDANCE_AND_FAILURE_COMPOSITE__NOT_LATENT_ACTUAL_CONSUMPTION",
            "evaluation_link_rule": "reference_link_truth_arm_independent",
            "weighted_fc_omission": fc_omission,
            "weighted_operational_positive": 1.0 - fc_omission,
            "weighted_operational_negative_known": operational_negative_weight,
            "weighted_unknown_terminal": unknown_weight,
            "latent_weighted_actual_omission_M_nu": None,
            "missing_by_reason": missing_by_reason,
            "machine_ingestion_and_task_reference": machine_flags,
            "machine_event_interpretation": "synthetic placeholder predicate only; not attention, comprehension, downstream information use, or a cryptographic evidence chain",
        }
        return rows, summary

    def run_period(self, period: int, plan: Mapping[str, Any]) -> dict[str, Any]:
        """Run precheck → observation → update → link → select → terminal events → ledger.

        Structural plan validation and the conservative whole-period resource
        precheck both run before any state mutation.  The delivered ⊆ selected
        consistency check necessarily runs after selection; an inconsistent
        fixture plan is a declared fixture error, not a resource-exhaustion path.
        """
        candidate_ids = {item["candidate_id"] for item in self.fixture["candidates"]}
        delivered = set(plan.get("delivered", []))
        opened = set(plan.get("opened", []))
        if not delivered <= candidate_ids or not opened <= delivered:
            raise ValueError("invalid terminal plan: delivered/opened must be known candidates with opened ⊆ delivered")
        self._precheck_period_resources(period, plan)
        instrument = OperationalAttendanceInstrument(self.fixture["attendance_instrument"])
        self.governance.append_record("observation", {
            "period": period, "observation": f"fixture-observation-{period}",
            "target_registry_version": self.registry["version"],
            "evaluation_cohort_id": self.evaluation_cohort_id,
        }, evidence=[f"fixture:{self.fixture['run_id']}:observation:{period}"])
        updated = self._update(period)
        eligible, link_audit = self._eligible(updated, period)
        self._spend(self.fixture["resource_costs"]["linkage_per_period"], period=period, stage="linkage")
        selected, ranking = self._select(period, eligible)
        selected_ids = {item["candidate_id"] for item in selected}
        if not delivered <= selected_ids:
            raise ValueError("invalid terminal plan: delivered candidates must be selected")
        for _ in sorted(delivered):
            self._spend(self.fixture["resource_costs"]["delivery_per_candidate"],
                        period=period, stage="delivery")
        for _ in sorted(opened):
            self._spend(self.fixture["resource_costs"]["attendance_per_candidate"],
                        period=period, stage="attendance_measurement")
        outcomes, summary = self._target_outcomes(selected, plan, instrument, period)
        result = {
            "period": period, "objective_version": self.governance.inspect_objective()["version"],
            "evaluation_cohort_id": self.evaluation_cohort_id,
            "ranking": ranking, "selected_candidate_ids": [item["candidate_id"] for item in selected],
            "delivered_candidate_ids": sorted(delivered), "opened_candidate_ids": sorted(opened),
            "link_audit": link_audit, "operational_target_ledger": outcomes, "outcome_summary": summary,
        }
        self.period_results.append(_detached(result))
        self.governance.append_record("period_outcome", _detached(result),
                                      evidence=[f"fixture:{self.fixture['run_id']}:outcome:{period}"])
        self.history.append({"period": period, "observation": f"fixture-observation-{period}"})
        return result

    def write_after_period(self, patch: Mapping[str, Any], *, authorization_id: str,
                           timestamp: str, actor: str = "R") -> dict[str, Any]:
        authorization = Authorization(
            authorization_id=authorization_id, principal="R", operation="objective_write",
            proposal_hash=proposal_digest("objective_write", patch), timestamp=timestamp,
            version_token=self.governance.version_token(),
        )
        return self.governance.write_objective(
            patch, actor=actor, authorization=authorization,
            evidence=[f"fixture:{self.fixture['run_id']}:write:{authorization_id}"],
        )

    def rollback_after_period(self, target_version: int, *, authorization_id: str,
                              timestamp: str, actor: str = "R") -> dict[str, Any]:
        proposal = {"target_version": target_version}
        authorization = Authorization(
            authorization_id=authorization_id, principal="R", operation="rollback",
            proposal_hash=proposal_digest("rollback", proposal), timestamp=timestamp,
            version_token=self.governance.version_token(),
        )
        return self.governance.rollback(
            target_version, actor=actor, authorization=authorization,
            evidence=[f"fixture:{self.fixture['run_id']}:rollback:{authorization_id}"],
        )

    def result(self) -> dict[str, Any]:
        verification = self.governance.verify_audit(anchor=self.governance.audit_anchor())
        return {
            "schema": "sea.sap-longitudinal-executor/v2",
            "status": "SYNTHETIC_IMPLEMENTATION_RUN__NOT_EFFECTIVENESS_EVIDENCE",
            "run_id": self.fixture["run_id"], "arm": self.arm,
            "control_instance_id": self.control_instance_id,
            "evaluation_cohort_id": self.evaluation_cohort_id,
            "instance_id": self.instance_id,
            "fixture_sha256": _sha(self.fixture),
            "target_registry_version": self.registry["version"],
            "ledger_scope": "OPERATIONAL_ATTENDANCE_AND_FAILURE_COMPOSITE__NOT_LATENT_ACTUAL_CONSUMPTION",
            "periods": self.period_results,
            "budget": {"initial": self.fixture["initial_budget"],
                       "spent": self.budget_spent, "remaining": self.budget_remaining},
            "objective": self.governance.inspect_objective(),
            "audit": {"records": self.governance.audit_records(),
                      "anchor": self.governance.audit_anchor(), "verification": verification},
            "new_real_model_calls": 0, "human_data": False,
            "latent_actual_consumption_observed": False,
        }


def run_longitudinal_fixture() -> dict[str, Any]:
    """Two complete periods plus a post-rollback ranking identity check."""
    executor = SAPExecutor(load_fixture(), arm="sea")
    plans = {int(key): value for key, value in executor.fixture["period_plans"].items()}
    first = executor.run_period(0, plans[0])
    mismatch = executor.write_after_period(
        {"weights": {"novelty": 10}}, authorization_id="sigma-demo-write",
        timestamp="logical:00000010", actor="platform",
    )
    accepted = executor.write_after_period(
        {"weights": {"novelty": 10}}, authorization_id="sigma-demo-write",
        timestamp="logical:00000010", actor="R",
    )
    second = executor.run_period(1, plans[1])
    restored = executor.rollback_after_period(
        0, authorization_id="sigma-demo-rollback", timestamp="logical:00000020")
    eligible, _ = executor._eligible(executor.updated_candidates["0"], period=0)
    after = executor.governance.rank(
        executor._governance_candidates(eligible), executor.fixture["user_state"],
        executor.fixture.get("platform_variables", {}),
        evidence=["fixture:longitudinal:post-rollback-rank"],
    )
    identity = [row["candidate_id"] for row in after] == [row["candidate_id"] for row in first["ranking"]]
    result = executor.result()
    result["guard_trace"] = {
        "platform_with_R_authorization_rejected": not mismatch["accepted"]
        and mismatch.get("guard_reject_reason") == "actor_principal_mismatch",
        "authorized_write_accepted": accepted["accepted"],
        "rollback_accepted": restored["accepted"],
        "post_rollback_ranking_equals_baseline": identity,
        "changed_second_period_ranking": [row["candidate_id"] for row in second["ranking"]]
        != [row["candidate_id"] for row in first["ranking"]],
    }
    result["contrast_bound_example"] = operational_attendance_contrast_bounds(
        {"sea": 0.5, "control": 0.4}, {"sea": 0.2, "control": 0.1})
    if not all(result["guard_trace"].values()):
        raise AssertionError("longitudinal guard/ranking checks failed")
    if any(result["budget"]["spent"][name] <= 0 for name in RESOURCE_NAMES):
        raise AssertionError("all five resource coordinates must be exercised")
    return result


def run_matched_implementation_demo() -> dict[str, Any]:
    """Same mock scorer/input/access/budget for staged SEA and direct S2d fixtures."""
    base = load_fixture()
    source_plan = base["period_plans"]["0"]
    plan = {
        "delivered": ["c1"], "opened": ["c1"],
        "attendance_events": {"c1": source_plan["attendance_events"]["c1"]},
        "machine_events": {"c1": source_plan["machine_events"]["c1"]},
    }
    outputs = {}
    for arm in ("sea", "s2d"):
        fixture = _detached(base)
        fixture["run_id"] = f"matched-fixture:{arm}"
        executor = SAPExecutor(fixture, arm=arm)
        period = executor.run_period(0, plan)
        outputs[arm] = {
            "selected_candidate_ids": period["selected_candidate_ids"],
            "outcome_summary": period["outcome_summary"],
            "budget_spent": executor.budget_spent,
            "audit_valid": executor.governance.verify_audit()["valid"],
            "selection_link_rule": "staged_link_pass" if arm == "sea" else "raw_candidates_no_staged_filter",
            "evaluation_link_rule": "reference_link_truth_arm_independent",
        }
    return {
        "schema": "sea.matched-implementation-fixture/v2",
        "status": "MECHANISTIC_MATCHED_FIXTURE__NOT_A_MODEL_OR_DEPLOYMENT_EXPERIMENT",
        "matching": {
            "mock_scorer": "symmetric_binary/1 + GovernanceReference integer ranking",
            "raw_input_sha256": _sha(base["candidates"]),
            "target_registry_sha256": _sha(base["target_registry"]),
            "initial_budget": base["initial_budget"],
            "retrieval_permissions": "same frozen fixture only",
            "external_model_calls": 0,
        },
        "arms": outputs,
        "interpretation": "Only interface execution and accounting are demonstrated; differences are fixture mechanics, not estimated effects.",
    }
