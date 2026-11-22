"""Minimal longitudinal SAP executor for deterministic synthetic fixtures.

This is an executable *small instance* of the v1.15 SAP interface, not a general
optimizer, an LLM experiment, or deployment-effectiveness evidence.  It keeps
latent actual consumption unobserved.  Operational attendance, the synthetic
machine ingestion-and-task-reference placeholder, and the failure-composite
endpoint are distinct.  The executable ledger is operational/FC, not latent.

v1.15 semantics: the SAP tuple is defined per control instance with the active
target registry in state (main text, Section 3.2).  Registry-version transitions
are **exogenous frozen evaluation-protocol events, not policy actions**: the
protocol declares ex ante a finite registry family (version -> content-hash
allowlist with frozen registry content) and an ordered version schedule.
continue_with_target_registry advances the single control path to the next
scheduled family member and seals the predecessor path (single-line control:
exactly one active control path per control instance, one shared budget and
ledger).  fork_for_target_registry is the declared full-reset protocol choice
starting a new control instance; it also seals the parent path.  Objective
rollback never restores a registry version; registry transitions are
append-only forward along the schedule.  Every cohort-scoped audit event carries
control_instance_id, evaluation_cohort_id, target_registry_version and the
registry hash.  All structural terminal-plan errors, including
delivered-but-not-selected, are detected by a commit-free selection dry run
before any state mutation.  Invalid attendance telemetry is unknown, never
negative; the shipped instrument object is a synthetic fixture, not a complete
preregistered instrument registry.
"""
from __future__ import annotations

import copy
from dataclasses import dataclass
import hashlib
import json
import math
from pathlib import Path
import re
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


_SHA256_HEX = re.compile(r"[0-9a-f]{64}")


def _is_sha256_hex(value: Any) -> bool:
    """True 64-character lowercase hexadecimal SHA-256 check, not length only."""
    return isinstance(value, str) and _SHA256_HEX.fullmatch(value) is not None


def _parse_protocol_declaration(fixture: Mapping[str, Any],
                                registry: Mapping[str, Any]) -> tuple[dict, list, dict]:
    """Validate the ex-ante frozen registry family and version schedule.

    The protocol declaration is part of the fixture, frozen before the run:

    - ``registry_family``: version -> SHA-256 content-hash allowlist of the
      finite frozen family (main text $\\mathfrak R$).  The active registry
      must be a member whose content hash matches the declaration.
    - ``protocol_registry_schedule``: ordered version list; the active version
      must appear, and continuity transitions may only advance to the next
      scheduled member.  Without a declaration the schedule is the single
      active version, so no transition is possible.
    - ``protocol_registries``: frozen full content for scheduled versions other
      than the initial one, making the allowlist self-contained.

    A fixture without any declaration derives the single-member family
    {active version: content hash}; arbitrary runtime switching is then
    impossible because no other version is a family member.
    """
    version = registry["version"]
    registry_hash = _sha(registry)
    family = fixture.get("registry_family")
    schedule = fixture.get("protocol_registry_schedule")
    frozen = fixture.get("protocol_registries", {})
    if family is None:
        if schedule is not None or frozen:
            raise ValueError("schedule/frozen registries require a declared registry_family")
        family = {version: registry_hash}
    else:
        if not isinstance(family, dict) or not family:
            raise ValueError("registry_family must be a nonempty version->hash allowlist")
        for key, value in family.items():
            if not isinstance(key, str) or not key or not _is_sha256_hex(value):
                raise ValueError("registry_family entries need version keys and 64-hex content hashes")
        if version not in family:
            raise ValueError("active registry version is not a declared family member")
        if family[version] != registry_hash:
            raise ValueError("active registry content hash does not match the frozen family declaration")
    if schedule is None:
        schedule = [version]
    if (not isinstance(schedule, list) or not schedule
            or any(not isinstance(item, str) or not item for item in schedule)
            or len(set(schedule)) != len(schedule)):
        raise ValueError("protocol_registry_schedule must be a nonempty list of unique versions")
    if any(item not in family for item in schedule):
        raise ValueError("every scheduled version must be a declared family member")
    if version not in schedule:
        raise ValueError("active registry version must appear in the protocol schedule")
    if not isinstance(frozen, dict):
        raise ValueError("protocol_registries must map versions to frozen registry content")
    for key, content in frozen.items():
        if key not in family:
            raise ValueError("frozen protocol registry is not a declared family member")
        validate_target_registry(content)
        if content["version"] != key:
            raise ValueError("frozen protocol registry version does not match its key")
        if _sha(content) != family[key]:
            raise ValueError("frozen protocol registry content hash does not match the family")
        if key == version and content != registry:
            raise ValueError("frozen content for the active version must equal the active registry")
    return dict(family), list(schedule), _detached(frozen)


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
    OperationalAttendanceInstrument(document["attendance_instrument"])
    _parse_protocol_declaration(document, document["target_registry"])
    return _detached(document)


def validate_target_registry(registry: Mapping[str, Any]) -> None:
    """Validate one immutable target population, mapping and reference snapshot."""
    required = {
        "version", "reference_corpus", "targets", "candidate_target_links",
        "availability", "construction_rule", "dynamic_version_rule",
    }
    if set(registry) != required:
        raise ValueError(f"target registry fields must be exactly {sorted(required)}")
    if not isinstance(registry["version"], str) or not registry["version"]:
        raise ValueError("target registry version must be a nonempty string")
    reference = registry["reference_corpus"]
    if not reference.get("snapshot_id") or not _is_sha256_hex(reference.get("sha256")):
        raise ValueError("reference corpus needs snapshot identity and a 64-hex content hash")
    if reference.get("availability_universe") not in {"closed_snapshot", "open_world"}:
        raise ValueError("availability universe must be declared")
    documents = reference.get("documents")
    if not isinstance(documents, list) or not documents:
        raise ValueError("reference corpus must list auditable source documents")
    document_ids = []
    for document in documents:
        if not document.get("document_id") or not document.get("evidence_pointer"):
            raise ValueError("reference document needs identity and evidence")
        if not _is_sha256_hex(document.get("content_sha256")):
            raise ValueError("reference document content hash must be 64 lowercase hex characters")
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
    that conjunction is negative.  Missing or invalid telemetry is unknown:
    non-finite values, negative engaged time, coverage outside [0,1], non-Boolean
    flags, and empty evidence pointers never produce positive or negative.

    The shipped registry object is a **synthetic instrument fixture**
    (``registry_scope="synthetic_instrument_fixture"``), not a complete
    preregistered instrument registry.  A registry claiming
    ``validation_status="validated"`` must instead declare
    ``registry_scope="preregistered_instrument"`` and carry the full
    preregistration fields: raw-event schema, true 64-hex validation-data and
    measurement-code hashes, measurement error with sensitivity/specificity
    intervals and a declared validation-to-deployment transportability
    assumption, an independent blinded reference-set construction and unlock
    record, a completion-subset representativeness statement, alternative
    instruments, and arm-and-model blinding.  These are structural registration
    checks; they do not themselves perform or certify real measurement
    validation, and the shipped synthetic fixture is never a validated
    instrument instance.
    """

    FULL_REGISTRATION_FIELDS = {
        "raw_event_schema", "validation_data_sha256", "measurement_code_sha256",
        "measurement_error", "alternative_instruments",
        "blinded_reference_set", "completion_subset_representativeness",
    }

    def __init__(self, registry: Mapping[str, Any]):
        self.registry = _detached(registry)
        required = {
            "instrument_id", "version", "decision_rule", "thresholds",
            "validation_status", "assessor_blinding", "sensitivity_versions",
            "registry_scope",
        }
        if not required <= set(registry):
            raise ValueError("invalid attendance instrument registry")
        if registry["registry_scope"] not in {
            "synthetic_instrument_fixture", "preregistered_instrument"
        }:
            raise ValueError("instrument registry scope must be declared")
        if registry["decision_rule"] != "VALID_READING_AND_CONTENT_LINKED_CONFIRMATION":
            raise ValueError("primary attendance rule must be explicit AND")
        if registry["validation_status"] not in {"validated", "synthetic_fixture_only"}:
            raise ValueError("attendance instrument is not validated")
        if registry["validation_status"] == "synthetic_fixture_only":
            if registry["registry_scope"] != "synthetic_instrument_fixture":
                raise ValueError("synthetic fixture cannot claim preregistered scope")
            if registry["assessor_blinding"] != "not_applicable_synthetic_fixture":
                raise ValueError("synthetic fixture must declare blinding not applicable")
        else:
            if registry["registry_scope"] != "preregistered_instrument":
                raise ValueError("validated instrument requires preregistered scope")
            if registry["assessor_blinding"] != "arm_and_model_blind":
                raise ValueError("assessor blinding requirement is not met")
            missing = self.FULL_REGISTRATION_FIELDS - set(registry)
            if missing:
                raise ValueError(
                    f"validated instrument lacks preregistration fields: {sorted(missing)}")
            if not isinstance(registry["raw_event_schema"], dict) or not registry["raw_event_schema"]:
                raise ValueError("raw-event schema must be a nonempty object")
            for field in ("validation_data_sha256", "measurement_code_sha256"):
                if not _is_sha256_hex(registry[field]):
                    raise ValueError(f"{field} must be a 64-character lowercase hexadecimal hash")
            error = registry["measurement_error"]
            if not isinstance(error, dict) or not {"sensitivity", "specificity"} <= set(error):
                raise ValueError("measurement error needs sensitivity and specificity")
            for key in ("sensitivity", "specificity"):
                value = error[key]
                if (isinstance(value, bool) or not isinstance(value, (int, float))
                        or not math.isfinite(value) or not 0 <= value <= 1):
                    raise ValueError(f"measurement error {key} must lie in [0,1]")
                interval = error.get(f"{key}_interval")
                if (not isinstance(interval, (list, tuple)) or len(interval) != 2
                        or any(isinstance(bound, bool) or not isinstance(bound, (int, float))
                               or not math.isfinite(bound) for bound in interval)):
                    raise ValueError(f"measurement error {key} needs a finite two-sided interval")
                low, high = float(interval[0]), float(interval[1])
                if not 0 <= low <= float(value) <= high <= 1:
                    raise ValueError(f"measurement error {key} interval must cover the point estimate within [0,1]")
            if not error.get("validation_set_pointer"):
                raise ValueError("measurement error needs a validation-set pointer")
            if not isinstance(error.get("transportability_assumption"), str) or not error["transportability_assumption"].strip():
                raise ValueError("measurement error needs a declared validation-to-deployment transportability assumption")
            reference_set = registry["blinded_reference_set"]
            if not isinstance(reference_set, dict) or not {
                "construction_rule", "reference_data_sha256", "unlock_timestamp",
                "overlap_with_tuning_or_main_corpus",
            } <= set(reference_set):
                raise ValueError("blinded reference set needs construction, hash, unlock time, and overlap declaration")
            if not isinstance(reference_set["construction_rule"], str) or not reference_set["construction_rule"].strip():
                raise ValueError("blinded reference set construction rule must be a nonempty string")
            if not _is_sha256_hex(reference_set["reference_data_sha256"]):
                raise ValueError("blinded reference set data hash must be 64 lowercase hex characters")
            if not isinstance(reference_set["unlock_timestamp"], str) or not reference_set["unlock_timestamp"].strip():
                raise ValueError("blinded reference set needs a declared unlock timestamp")
            if reference_set["overlap_with_tuning_or_main_corpus"] is not False:
                raise ValueError("blinded reference set must declare no overlap with tuning or main-analysis corpora")
            representativeness = registry["completion_subset_representativeness"]
            if not isinstance(representativeness, str) or not representativeness.strip():
                raise ValueError("completion-subset representativeness must be a nonempty statement")
            alternatives = registry["alternative_instruments"]
            if (not isinstance(alternatives, list) or not alternatives
                    or any(not isinstance(item, str) or not item for item in alternatives)):
                raise ValueError("alternative instruments must be a nonempty string list")
        thresholds = registry["thresholds"]
        if not isinstance(thresholds, dict) or set(thresholds) != {
            "min_engaged_ms", "min_coverage_fraction"
        }:
            raise ValueError("attendance thresholds must declare both frozen coordinates")
        engaged = thresholds["min_engaged_ms"]
        coverage = thresholds["min_coverage_fraction"]
        for name, value in (("min_engaged_ms", engaged), ("min_coverage_fraction", coverage)):
            if (isinstance(value, bool) or not isinstance(value, (int, float))
                    or not math.isfinite(value)):
                raise ValueError(f"threshold {name} must be a finite number")
        if engaged < 0:
            raise ValueError("min_engaged_ms must be nonnegative")
        if not 0 <= coverage <= 1:
            raise ValueError("min_coverage_fraction must lie in [0,1]")

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
            focused = event["focused_visible"]
            confirmation = event["content_linked_confirmation"]
            if not isinstance(focused, bool) or not isinstance(confirmation, bool):
                raise ValueError("visibility and confirmation must be Boolean")
            engaged_raw = event["engaged_ms"]
            coverage_raw = event["coverage_fraction"]
            if (isinstance(engaged_raw, bool) or isinstance(coverage_raw, bool)
                    or not isinstance(engaged_raw, (int, float))
                    or not isinstance(coverage_raw, (int, float))):
                raise ValueError("telemetry values must be numeric")
            engaged = float(engaged_raw)
            coverage = float(coverage_raw)
            if not math.isfinite(engaged) or not math.isfinite(coverage):
                raise ValueError("telemetry values must be finite")
            if engaged < 0:
                raise ValueError("engaged_ms must be nonnegative")
            if not 0 <= coverage <= 1:
                raise ValueError("coverage_fraction must lie in [0,1]")
            pointer = event["evidence_pointer"]
            if not isinstance(pointer, str) or not pointer.strip():
                raise ValueError("evidence_pointer must be a nonempty string")
            reading = (
                focused
                and engaged >= float(thresholds["min_engaged_ms"])
                and coverage >= float(thresholds["min_coverage_fraction"])
            )
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
    if any(not _is_sha256_hex(value) for value in values):
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


def completed_measurement_transport(m_z: float, sensitivity: float, specificity: float, *,
                                    precision_warning_threshold: float = 0.1) -> dict[str, Any]:
    """Supplement identity (S12) with a Youden-denominator precision warning.

    Sensitivity analysis only: applies to completed (non-unknown) measurements
    under an explicit arm-specific error model whose rates are assumed
    conditionally stable between the validation and deployment populations
    (transportability).  It is not an assumption-free bound.  When
    J = se + sp - 1 approaches zero the transport is highly unstable: estimation
    variance is amplified by 1/J^2, so a precision warning is raised below the
    declared threshold and a sensitivity grid over error rates is required.
    """
    values = {"m_z": m_z, "sensitivity": sensitivity, "specificity": specificity,
              "precision_warning_threshold": precision_warning_threshold}
    for name, value in values.items():
        if (isinstance(value, bool) or not isinstance(value, (int, float))
                or not math.isfinite(value)):
            raise ValueError(f"{name} must be a finite number")
    if not 0 <= m_z <= 1 or not 0 <= sensitivity <= 1 or not 0 <= specificity <= 1:
        raise ValueError("omission and error rates must lie in [0,1]")
    if not 0 < precision_warning_threshold <= 1:
        raise ValueError("precision warning threshold must lie in (0,1]")
    youden = sensitivity + specificity - 1
    if youden <= 0:
        raise ValueError("S12 requires se+sp>1 (positive Youden denominator)")
    m_d = (m_z - (1 - sensitivity)) / youden
    return {
        "identity": "S12",
        "scope": "completed measurements only; explicit-error-model sensitivity analysis, not an assumption-free bound",
        "m_Z": float(m_z), "m_D": m_d,
        "sensitivity": float(sensitivity), "specificity": float(specificity),
        "youden_denominator": youden,
        "variance_amplification_factor": 1.0 / (youden * youden),
        "precision_warning": youden < precision_warning_threshold,
        "precision_warning_threshold": float(precision_warning_threshold),
        "transportability_assumption_required": True,
        "latent_estimate_outside_unit_interval": not 0 <= m_d <= 1,
    }


def completed_measurement_transport_delta_method(
    m_z: float, sensitivity: float, specificity: float, *,
    var_m_z: float, var_se: float, var_sp: float,
    precision_warning_threshold: float = 0.1,
) -> dict[str, Any]:
    """Delta-method uncertainty propagation for (S12), assuming independent inputs.

    With N = m^Z - 1 + se and J = se + sp - 1, the partial derivatives are
    d/se = (J - N)/J^2, d/sp = -N/J^2, d/m^Z = 1/J.  If the inputs are dependent,
    covariance terms must be added; this helper deliberately does not invent them.
    The normal-approximation interval is unreliable when the precision warning
    fires (J near zero); use a sensitivity grid instead.
    """
    base = completed_measurement_transport(
        m_z, sensitivity, specificity,
        precision_warning_threshold=precision_warning_threshold)
    for name, value in (("var_m_z", var_m_z), ("var_se", var_se), ("var_sp", var_sp)):
        if (isinstance(value, bool) or not isinstance(value, (int, float))
                or not math.isfinite(value) or value < 0):
            raise ValueError(f"{name} must be a finite nonnegative variance")
    youden = base["youden_denominator"]
    numerator = m_z - 1 + sensitivity
    d_se = (youden - numerator) / (youden * youden)
    d_sp = -numerator / (youden * youden)
    d_mz = 1.0 / youden
    variance = d_se * d_se * var_se + d_sp * d_sp * var_sp + d_mz * d_mz * var_m_z
    half_width = 1.959963984540054 * math.sqrt(variance)
    return dict(
        base,
        delta_method_variance=variance,
        approx_95_interval=[base["m_D"] - half_width, base["m_D"] + half_width],
        input_independence_assumed=True,
        covariance_note="add covariance terms if m^Z, se, sp estimates are dependent",
    )


class SAPExecutor:
    """Execute a small target registry under one control history and evaluation cohort.

    Under the v1.15 tuple, the SAP control instance spans evaluation cohorts:
    the active registry is part of state, and a registry-version transition is
    an **exogenous frozen evaluation-protocol event, not a policy action**.
    The protocol declares ex ante a finite registry family (content-hash
    allowlist) and an ordered schedule.  This object serves one cohort (one
    constant registry version).  continue_with_target_registry advances the
    single control path to the next scheduled family member, seals this
    predecessor path, and shares the unique objective/authorization/audit/
    budget state; fork_for_target_registry is the declared full-reset protocol
    choice starting a new control instance.  Objective rollback never restores
    a registry version.
    """

    def __init__(self, fixture: Mapping[str, Any], *, arm: str = "sea"):
        self.fixture = _detached(fixture)
        self.registry = _detached(fixture["target_registry"])
        validate_target_registry(self.registry)
        (self.registry_family, self.protocol_registry_schedule,
         self._frozen_protocol_registries) = _parse_protocol_declaration(fixture, self.registry)
        self._schedule_index = self.protocol_registry_schedule.index(self.registry["version"])
        self.protocol_declaration_sha256 = _sha({
            "registry_family": self.registry_family,
            "protocol_registry_schedule": self.protocol_registry_schedule,
            "protocol_registries": self._frozen_protocol_registries,
        })
        self.arm = arm
        self.control_instance_id = domain_digest("sea-sap-control-instance/1", {
            "run_id": fixture["run_id"], "arm": arm,
        })
        self.evaluation_cohort_id = domain_digest("sea-sap-evaluation-cohort/1", {
            "control_instance_id": self.control_instance_id, "target_registry": self.registry,
        })
        self.instance_id = self.evaluation_cohort_id
        self.registry_sha256 = _sha(self.registry)
        self.governance = GovernanceReference()
        self.budget_remaining = {
            name: _nonnegative_int(fixture["initial_budget"][name], f"budget.{name}")
            for name in RESOURCE_NAMES
        }
        self.budget_spent = {name: 0 for name in RESOURCE_NAMES}
        self.history: list[dict[str, Any]] = []
        self.period_results: list[dict[str, Any]] = []
        self.updated_candidates: dict[str, list[dict[str, Any]]] = {}
        self._sealed = False
        self._seal_reason: Optional[str] = None
        self._document_by_id = {
            doc["document_id"]: doc for doc in self.registry["reference_corpus"]["documents"]
        }

    def _cohort_context(self) -> dict[str, str]:
        """Attribution carried by every cohort-scoped audit event payload."""
        return {
            "control_instance_id": self.control_instance_id,
            "evaluation_cohort_id": self.evaluation_cohort_id,
            "target_registry_version": self.registry["version"],
            "target_registry_sha256": self.registry_sha256,
        }

    def _assert_active(self) -> None:
        if self._sealed:
            raise RuntimeError(
                f"control path is sealed ({self._seal_reason}); only the successor "
                "evaluation cohort is the active control path (single-line control)")

    def _seal(self, reason: str, *, successor_evaluation_cohort_id: Optional[str] = None) -> None:
        """Seal this control path; append the sealing record before the boundary record."""
        self._sealed = True
        self._seal_reason = reason
        payload = {
            **self._cohort_context(),
            "reason": reason,
            "protocol_declaration_sha256": self.protocol_declaration_sha256,
        }
        if successor_evaluation_cohort_id is not None:
            payload["successor_evaluation_cohort_id"] = successor_evaluation_cohort_id
        self.governance.append_record(
            "control_path_sealed", payload,
            evidence=[f"fixture:{self.fixture['run_id']}:control-path-sealed:{self.registry['version']}"])

    def _reject_switch(self, registry: Any, reason: str,
                       attempted_hash: Optional[str] = None) -> None:
        """Log a rejected protocol-transition attempt with zero state mutation."""
        version = registry.get("version") if isinstance(registry, Mapping) else None
        payload = {
            **self._cohort_context(),
            "attempted_target_registry_version": version if isinstance(version, str) else None,
            "attempted_target_registry_sha256": attempted_hash,
            "reason": reason,
            "policy_action": False,
            "protocol_declaration_sha256": self.protocol_declaration_sha256,
            "state_mutated": False,
            "resources_spent": 0,
        }
        self.governance.append_record(
            "registry_switch_rejected", payload,
            evidence=[f"fixture:{self.fixture['run_id']}:registry-switch-rejected:{reason}"])
        raise ValueError(f"registry switch rejected: {reason}")

    def fork_for_target_registry(self, registry: Mapping[str, Any]) -> "SAPExecutor":
        """Declared full-reset protocol choice: a NEW control instance and cohort.

        This is an evaluation-protocol choice, not a theorem that SAP control
        must reset, and not a policy action.  The forked registry must be a
        content-hash-verified member of the frozen family.  The parent path is
        sealed so that exactly one active control path remains per protocol
        run; the new instance has its own control identity, objective store,
        budget, and ledger.  Its schedule is the declared suffix starting at
        the fork version (or a single-version schedule if the version is a
        family member outside the parent schedule).
        """
        if self._sealed:
            self._reject_switch(registry, "sealed_control_path")
        validate_target_registry(registry)
        version = registry["version"]
        attempted_hash = _sha(registry)
        if version not in self.registry_family:
            self._reject_switch(registry, "version_not_in_registry_family", attempted_hash)
        if self.registry_family[version] != attempted_hash:
            self._reject_switch(registry, "registry_content_hash_mismatch", attempted_hash)
        fixture = _detached(self.fixture)
        fixture["run_id"] = f"{self.fixture['run_id']}:{version}"
        fixture["target_registry"] = _detached(registry)
        if version in self.protocol_registry_schedule:
            index = self.protocol_registry_schedule.index(version)
            fixture["protocol_registry_schedule"] = self.protocol_registry_schedule[index:]
        else:
            fixture["protocol_registry_schedule"] = [version]
        forked = SAPExecutor(fixture, arm=self.arm)
        self._seal("protocol_full_reset_new_control_instance",
                   successor_evaluation_cohort_id=forked.evaluation_cohort_id)
        return forked

    def continue_with_target_registry(self, registry: Mapping[str, Any]) -> "SAPExecutor":
        """Exogenous protocol transition: advance the single control path one cohort.

        Not a policy action: no actor, principal, or authorization record is
        required or accepted, because registry transitions are outside the
        policy action space (main text, Section 3.2).  Instead the transition
        is validated against the ex-ante frozen protocol declaration: the new
        registry must be the NEXT scheduled family member with a matching
        content hash.  Non-family, tampered, out-of-schedule, and sealed-path
        attempts are logged as rejections with zero state mutation and zero
        resource spend.  On acceptance the predecessor path is sealed
        (single-line control), objective/authorization/audit/budget state is
        shared as the unique control state, and a cohort-boundary record is
        appended.  The transition is append-only forward: objective rollback
        never restores a registry version.
        """
        if self._sealed:
            self._reject_switch(registry, "sealed_control_path")
        validate_target_registry(registry)
        version = registry["version"]
        attempted_hash = _sha(registry)
        if version not in self.registry_family:
            self._reject_switch(registry, "version_not_in_registry_family", attempted_hash)
        if self.registry_family[version] != attempted_hash:
            self._reject_switch(registry, "registry_content_hash_mismatch", attempted_hash)
        schedule = self.protocol_registry_schedule
        if self._schedule_index + 1 >= len(schedule) or schedule[self._schedule_index + 1] != version:
            self._reject_switch(registry, "version_not_next_in_protocol_schedule", attempted_hash)
        fixture = _detached(self.fixture)
        fixture["target_registry"] = _detached(registry)
        continued = SAPExecutor(fixture, arm=self.arm)
        continued.control_instance_id = self.control_instance_id
        continued.governance = self.governance
        # Single-line control: one unique resource/history state, shared (not
        # copied) with the sealed predecessor, which can no longer mutate it.
        continued.budget_remaining = self.budget_remaining
        continued.budget_spent = self.budget_spent
        continued.history = self.history
        continued.period_results = self.period_results
        continued.updated_candidates = self.updated_candidates
        self._seal("protocol_registry_switch",
                   successor_evaluation_cohort_id=continued.evaluation_cohort_id)
        self.governance.append_record("evaluation_cohort_change", {
            "old_target_registry_version": self.registry["version"],
            "new_target_registry_version": registry["version"],
            "old_evaluation_cohort_id": self.evaluation_cohort_id,
            "new_evaluation_cohort_id": continued.evaluation_cohort_id,
            "old_target_registry_sha256": self.registry_sha256,
            "new_target_registry_sha256": continued.registry_sha256,
            "control_instance_id": self.control_instance_id,
            "control_continuity": True,
            "cross_version_pooling_allowed": False,
            "event_kind": "exogenous_evaluation_protocol_event",
            "policy_action": False,
            "authorization_required": False,
            "authorization_scope_note": "registry transitions are outside the policy action space; the objective-write guard does not apply",
            "protocol_declaration_sha256": self.protocol_declaration_sha256,
            "old_schedule_index": self._schedule_index,
            "new_schedule_index": continued._schedule_index,
            "old_control_path_sealed": True,
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
        self._assert_active()
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
            **self._cohort_context(),
        }, evidence=[f"fixture:{self.fixture['run_id']}:resources:{period}:{stage}"])

    def _precheck_period_resources(self, period: int, plan: Mapping[str, Any]) -> dict[str, int]:
        """Pure conservative whole-period precheck; no record, no mutation.

        It budgets the maximum declared selection limit and the planned terminal
        events.  If it fails, no observation, update, spend, or ledger event is
        appended.  Selection may later use fewer resources, but partial execution
        after a late budget failure is not the declared semantics.  The audit
        record is appended by run_period only after the dry run also passes.
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
        return required

    def _compute_updated(self, period: int) -> list[dict[str, Any]]:
        """Pure posterior computation for the dry run and the committing update.

        No resource spend, no audit record, no state mutation.  An invalid
        signal raises before any candidate is committed.
        """
        updated = []
        kernel = self.fixture["update_kernel"]
        for raw in self.fixture["candidates"]:
            posterior = symmetric_binary_posterior(
                raw["signal"], prior_milli=kernel["prior_milli"],
                accuracy_milli=kernel["accuracy_milli"],
            )
            candidate = _detached(raw)
            candidate["posterior_relevance_milli"] = posterior
            candidate["features"] = dict(raw["features"])
            candidate["features"]["relevance"] = (
                raw["features"]["relevance"] * posterior // 1000
            )
            candidate["provenance"] = f"fixture:{self.fixture['run_id']}:{raw['candidate_id']}"
            updated.append(candidate)
        return updated

    def _update(self, period: int) -> list[dict[str, Any]]:
        updated = self._compute_updated(period)
        kernel = self.fixture["update_kernel"]
        for _ in self.fixture["candidates"]:
            self._spend(kernel["cost_per_candidate"], period=period, stage="update")
        self.updated_candidates[str(period)] = _detached(updated)
        self.governance.append_record("update", {
            "period": period, "kernel": "symmetric_binary/1",
            "posteriors_milli": {
                item["candidate_id"]: item["posterior_relevance_milli"] for item in updated
            },
            "same_kernel_for_every_signal": True,
            **self._cohort_context(),
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

    def _selection_decision(self, eligible: Sequence[Mapping[str, Any]],
                            ranking: Sequence[Mapping[str, Any]],
                            budget_remaining: Mapping[str, int]) -> tuple[list[dict], set]:
        """Pure ranked-feasible-greedy decision; no spend, no records, no mutation.

        Shared by the commit-free dry run and the committing selection so both
        compute exactly the same selected set from identical state.
        """
        by_id = {candidate["candidate_id"]: candidate for candidate in eligible}
        selected = []
        covered: set = set()
        remaining = dict(budget_remaining)
        limit = self.fixture["selection_limit"]
        cost = self._selection_cost()
        for row in ranking:
            if len(selected) >= limit:
                break
            candidate = by_id[row["candidate_id"]]
            targets = set(candidate["linked_targets"])
            if self.arm == "sea" and targets and targets <= covered:
                continue
            if any(cost.get(name, 0) > remaining[name] for name in RESOURCE_NAMES):
                continue
            for name in RESOURCE_NAMES:
                remaining[name] -= cost.get(name, 0)
            selected.append(candidate)
            covered.update(targets)
        return selected, covered

    def _dry_run_selection(self, period: int, plan: Mapping[str, Any]) -> list[str]:
        """Commit-free selection preview run before any state mutation.

        Detects late structural plan errors — in particular a delivered
        candidate that the frozen selection rule would not select — without
        spending resources or appending observation/update/ranking/ledger
        records.  A failed dry run leaves the executor state untouched.
        """
        updated = self._compute_updated(period)
        eligible, _ = self._eligible(updated, period)
        ranking = self.governance.rank(
            self._governance_candidates(eligible), _detached(self.fixture["user_state"]),
            self.fixture.get("platform_variables", {}),
            evidence=[f"fixture:{self.fixture['run_id']}:rank-dry-run:{period}"],
            record=False,
        )
        selected, _ = self._selection_decision(eligible, ranking, self.budget_remaining)
        selected_ids = {item["candidate_id"] for item in selected}
        delivered = set(plan.get("delivered", []))
        if not delivered <= selected_ids:
            raise ValueError(
                "invalid terminal plan: delivered candidates must be selected "
                "(commit-free selection dry run, before any mutation)")
        return sorted(selected_ids)

    def _select(self, period: int, eligible: Sequence[Mapping[str, Any]]) -> tuple[list[dict], list[dict]]:
        ranking = self.governance.rank(
            self._governance_candidates(eligible), _detached(self.fixture["user_state"]),
            self.fixture.get("platform_variables", {}),
            evidence=[f"fixture:{self.fixture['run_id']}:rank:{period}"],
            context=self._cohort_context(),
        )
        selected, covered = self._selection_decision(eligible, ranking, self.budget_remaining)
        for _ in selected:
            self._spend(self._selection_cost(), period=period, stage="selection")
        self.governance.append_record("selection", {
            "period": period, "arm": self.arm,
            "selected_candidate_ids": [item["candidate_id"] for item in selected],
            "covered_linked_targets": sorted(covered), "selection_rule": "ranked_feasible_greedy",
            "selection_link_rule": "staged_link_pass" if self.arm == "sea" else "raw_candidates_no_staged_filter",
            **self._cohort_context(),
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
        """Run precheck + dry run → observation → update → link → select → terminal → ledger.

        All structural plan validation runs before any state mutation: known
        candidates and opened ⊆ delivered are checked directly, the conservative
        whole-period resource precheck is computed purely, and delivered ⊆
        selected is checked by a commit-free selection dry run.  An infeasible
        plan therefore leaves budgets, ledgers, and audit records untouched.
        """
        self._assert_active()
        candidate_ids = {item["candidate_id"] for item in self.fixture["candidates"]}
        delivered = set(plan.get("delivered", []))
        opened = set(plan.get("opened", []))
        if not delivered <= candidate_ids or not opened <= delivered:
            raise ValueError("invalid terminal plan: delivered/opened must be known candidates with opened ⊆ delivered")
        instrument = OperationalAttendanceInstrument(self.fixture["attendance_instrument"])
        required = self._precheck_period_resources(period, plan)
        preview_selected = self._dry_run_selection(period, plan)
        self.governance.append_record("resource_precheck", {
            "period": period, "required_upper_bound": required,
            "remaining_before": dict(self.budget_remaining),
            "semantics": "conservative whole-period precheck before mutation",
            **self._cohort_context(),
        }, evidence=[f"fixture:{self.fixture['run_id']}:resource-precheck:{period}"])
        self.governance.append_record("selection_dry_run", {
            "period": period,
            "preview_selected_candidate_ids": preview_selected,
            "terminal_plan_feasible": True,
            "semantics": "commit-free selection preview before mutation; no resources spent",
            **self._cohort_context(),
        }, evidence=[f"fixture:{self.fixture['run_id']}:selection-dry-run:{period}"])
        self.governance.append_record("observation", {
            "period": period, "observation": f"fixture-observation-{period}",
            **self._cohort_context(),
        }, evidence=[f"fixture:{self.fixture['run_id']}:observation:{period}"])
        updated = self._update(period)
        eligible, link_audit = self._eligible(updated, period)
        self._spend(self.fixture["resource_costs"]["linkage_per_period"], period=period, stage="linkage")
        selected, ranking = self._select(period, eligible)
        selected_ids = {item["candidate_id"] for item in selected}
        if sorted(selected_ids) != preview_selected:
            raise RuntimeError("committing selection diverged from the commit-free dry run")
        for _ in sorted(delivered):
            self._spend(self.fixture["resource_costs"]["delivery_per_candidate"],
                        period=period, stage="delivery")
        for _ in sorted(opened):
            self._spend(self.fixture["resource_costs"]["attendance_per_candidate"],
                        period=period, stage="attendance_measurement")
        outcomes, summary = self._target_outcomes(selected, plan, instrument, period)
        result = {
            "period": period, "objective_version": self.governance.inspect_objective()["version"],
            **self._cohort_context(),
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
        self._assert_active()
        authorization = Authorization(
            authorization_id=authorization_id, principal="R", operation="objective_write",
            proposal_hash=proposal_digest("objective_write", patch), timestamp=timestamp,
            version_token=self.governance.version_token(),
        )
        return self.governance.write_objective(
            patch, actor=actor, authorization=authorization,
            evidence=[f"fixture:{self.fixture['run_id']}:write:{authorization_id}"],
            context=self._cohort_context(),
        )

    def rollback_after_period(self, target_version: int, *, authorization_id: str,
                              timestamp: str, actor: str = "R") -> dict[str, Any]:
        self._assert_active()
        proposal = {"target_version": target_version}
        authorization = Authorization(
            authorization_id=authorization_id, principal="R", operation="rollback",
            proposal_hash=proposal_digest("rollback", proposal), timestamp=timestamp,
            version_token=self.governance.version_token(),
        )
        return self.governance.rollback(
            target_version, actor=actor, authorization=authorization,
            evidence=[f"fixture:{self.fixture['run_id']}:rollback:{authorization_id}"],
            context=self._cohort_context(),
        )

    def result(self) -> dict[str, Any]:
        verification = self.governance.verify_audit(anchor=self.governance.audit_anchor())
        return {
            "schema": "sea.sap-longitudinal-executor/v4",
            "status": "SYNTHETIC_IMPLEMENTATION_RUN__NOT_EFFECTIVENESS_EVIDENCE",
            "run_id": self.fixture["run_id"], "arm": self.arm,
            "control_instance_id": self.control_instance_id,
            "evaluation_cohort_id": self.evaluation_cohort_id,
            "instance_id": self.instance_id,
            "fixture_sha256": _sha(self.fixture),
            "target_registry_version": self.registry["version"],
            "target_registry_sha256": self.registry_sha256,
            "sap_tuple_scope": "control_instance_registry_in_state__exogenous_protocol_single_line__cohort_separated",
            "control_path_status": "sealed" if self._sealed else "active",
            "seal_reason": self._seal_reason,
            "registry_family_sha256": _sha(self.registry_family),
            "protocol_registry_schedule": list(self.protocol_registry_schedule),
            "protocol_schedule_index": self._schedule_index,
            "protocol_declaration_sha256": self.protocol_declaration_sha256,
            "instrument_registry_scope": self.fixture["attendance_instrument"]["registry_scope"],
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
        context=executor._cohort_context(),
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
        "schema": "sea.matched-implementation-fixture/v4",
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


def run_protocol_registry_switch_demo() -> dict[str, Any]:
    """Exogenous protocol transition, single-line sealing, and rejection negatives.

    Demonstrates the v1.15 registry governance semantics on the shipped frozen
    family/schedule declaration: a protocol event advances the single control
    path and seals the predecessor; non-family, tampered-hash, out-of-schedule,
    and sealed-path attempts are rejected with logged records and zero
    mutation; objective rollback does not restore the registry version.
    Synthetic interface demonstration only, not effectiveness evidence.
    """
    fixture = load_fixture()
    executor = SAPExecutor(fixture, arm="sea")
    plans = {int(key): value for key, value in fixture["period_plans"].items()}
    first = executor.run_period(0, plans[0])
    executor.write_after_period({"weights": {"novelty": 10}},
                                authorization_id="protocol-demo-write",
                                timestamp="logical:00000010")
    registry_v2 = fixture["protocol_registries"]["targets-v2"]
    continued = executor.continue_with_target_registry(registry_v2)
    second = continued.run_period(1, plans[1])
    restored = continued.rollback_after_period(
        0, authorization_id="protocol-demo-rollback", timestamp="logical:00000020")

    def expect_rejection(method, registry, reason):
        before_records = len(executor.governance.audit_records())
        before_budget = dict(continued.budget_remaining)
        try:
            method(registry)
        except ValueError as exc:
            records = executor.governance.audit_records()
            return (str(exc) == f"registry switch rejected: {reason}"
                    and len(records) == before_records + 1
                    and records[-1]["event"] == "registry_switch_rejected"
                    and records[-1]["payload"]["reason"] == reason
                    and records[-1]["payload"]["state_mutated"] is False
                    and records[-1]["payload"]["resources_spent"] == 0
                    and dict(continued.budget_remaining) == before_budget)
        return False

    arbitrary = _detached(registry_v2)
    arbitrary["version"] = "unregistered-arbitrary-v999"
    tampered = _detached(registry_v2)
    tampered["targets"][0]["canonical_text"] = "Tampered proposition text."
    registry_v1 = fixture["target_registry"]
    negatives = {
        "non_family_version_rejected": expect_rejection(
            continued.continue_with_target_registry, arbitrary, "version_not_in_registry_family"),
        "tampered_family_hash_rejected": expect_rejection(
            continued.continue_with_target_registry, tampered, "registry_content_hash_mismatch"),
        "backward_out_of_schedule_rejected": expect_rejection(
            continued.continue_with_target_registry, registry_v1, "version_not_next_in_protocol_schedule"),
        "sealed_predecessor_switch_rejected": expect_rejection(
            executor.continue_with_target_registry, registry_v2, "sealed_control_path"),
        "sealed_predecessor_fork_rejected": expect_rejection(
            executor.fork_for_target_registry, registry_v2, "sealed_control_path"),
    }
    sealed_reuse = {}
    for name, call in (
        ("run_period", lambda: executor.run_period(1, plans[1])),
        ("objective_write", lambda: executor.write_after_period(
            {"weights": {"novelty": 9}}, authorization_id="sealed-write",
            timestamp="logical:00000030")),
        ("objective_rollback", lambda: executor.rollback_after_period(
            0, authorization_id="sealed-rollback", timestamp="logical:00000031")),
    ):
        try:
            call()
            sealed_reuse[name] = False
        except RuntimeError:
            sealed_reuse[name] = True
    predecessor_sealed_successor_active = executor._sealed and not continued._sealed
    forked = continued.fork_for_target_registry(registry_v2)
    checks = {
        **negatives,
        "sealed_predecessor_run_rejected": sealed_reuse["run_period"],
        "sealed_predecessor_write_rejected": sealed_reuse["objective_write"],
        "sealed_predecessor_rollback_rejected": sealed_reuse["objective_rollback"],
        "single_control_instance_across_switch": continued.control_instance_id == executor.control_instance_id,
        "distinct_evaluation_cohorts": continued.evaluation_cohort_id != executor.evaluation_cohort_id,
        "unique_shared_budget_state": continued.budget_remaining is executor.budget_remaining
        and continued.budget_spent is executor.budget_spent,
        "unique_shared_history": continued.history is executor.history,
        "predecessor_sealed_successor_active": predecessor_sealed_successor_active,
        "objective_rollback_does_not_restore_registry": restored["accepted"]
        and continued.registry["version"] == "targets-v2"
        and continued.governance.inspect_objective()["version"] == restored["version"],
        "fork_is_new_control_instance": forked.control_instance_id != continued.control_instance_id
        and forked.budget_spent == {name: 0 for name in RESOURCE_NAMES},
        "fork_seals_parent": continued._sealed and not forked._sealed,
        "periods_stay_cohort_separated": first["evaluation_cohort_id"] != second["evaluation_cohort_id"]
        and first["target_registry_version"] == "targets-v1"
        and second["target_registry_version"] == "targets-v2",
        "audit_chain_valid": continued.governance.verify_audit(
            anchor=continued.governance.audit_anchor())["valid"],
    }
    if not all(checks.values()):
        raise AssertionError(f"protocol registry-switch demo checks failed: {checks}")
    records = continued.governance.audit_records()
    return {
        "schema": "sea.protocol-registry-switch-demo/v1",
        "status": "SYNTHETIC_PROTOCOL_TRANSITION_DEMO__NOT_EFFECTIVENESS_EVIDENCE",
        "run_id": fixture["run_id"],
        "semantics": {
            "registry_transition": "exogenous frozen evaluation-protocol event, not a policy action",
            "authorization": "no objective-write authorization required or accepted; family/schedule validation instead",
            "lifecycle": "single-line control: predecessor sealed, one active path, unique shared budget/ledger",
            "rollback_interaction": "objective rollback never restores a registry version; transitions append-only forward",
        },
        "protocol_declaration_sha256": executor.protocol_declaration_sha256,
        "registry_family_sha256": _sha(executor.registry_family),
        "protocol_registry_schedule": executor.protocol_registry_schedule,
        "checks": checks,
        "rejection_events": [record["payload"] for record in records
                             if record["event"] == "registry_switch_rejected"],
        "seal_events": [record["payload"] for record in records
                        if record["event"] == "control_path_sealed"],
        "cohort_change_events": [record["payload"] for record in records
                                 if record["event"] == "evaluation_cohort_change"],
        "audit": {"records": records,
                  "anchor": continued.governance.audit_anchor(),
                  "verification": continued.governance.verify_audit(
                      anchor=continued.governance.audit_anchor())},
        "new_real_model_calls": 0, "human_data": False,
    }
