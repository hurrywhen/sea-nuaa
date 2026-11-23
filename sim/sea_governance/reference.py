"""Minimal deterministic governance reference for SEA v1.17 S1--S4.

This is an offline, standard-library-only reference interface, not a deployed
service.  Authorization records are structural fixtures, not authenticated
identities.  Hash-chain verification can detect edits relative to retained
records/anchors, but cannot protect against a malicious host or wholesale
replacement of the host and its anchors.  No human-control, deployment, or
end-to-end effectiveness claim is made.

All scores are integers and all ordering ties are broken by ``candidate_id``.
No wall clock or randomness is used: callers may supply timestamps, otherwise
an audit record receives a deterministic logical timestamp.
"""
from __future__ import annotations

import copy
from dataclasses import dataclass
import hashlib
import json
import math
import re
from typing import Any, Iterable, Mapping, Optional, Sequence


SPECIFICATION = "SEA v1.17 minimal governance reference"
INTERFACE_VERSION = "sea-governance-reference/3"
AUDIT_SCHEMA = "sea-governance-audit/2"
GENESIS_HASH = "0" * 64
REFLECTIVE_PRINCIPAL = "R"
OBJECTIVE_TERMS = (
    "relevance",
    "novelty",
    "credibility",
    "durability",
    "harm_avoidance",
)
LIMITATIONS = (
    "Authorization records are structural checks, not identity or signature verification.",
    "Hash chaining does not provide security against malicious hosts or wholesale anchor replacement.",
    "Fixed-supply counterfactuals do not identify platform influence through candidate ecology.",
    "No human-control, deployment-readiness, or end-to-end effectiveness claim is made.",
)

_DEFAULT_OBJECTIVE = {
    "weights": {
        "relevance": 5,
        "novelty": 2,
        "credibility": 4,
        "durability": 3,
        "harm_avoidance": 4,
    },
    "g2": "Prefer useful, credible, durable information while avoiding harm.",
    "monitoring_list": ["finance", "health", "science"],
    "thresholds": {"min_utility": 0},
}

_PROVENANCE = {
    "specification": SPECIFICATION,
    "interface_version": INTERFACE_VERSION,
    "defaults_source": "Explicit illustrative reference defaults; not empirically calibrated.",
    "objective_expression": (
        "score(c,kappa,theta)=sum_j theta.weights[j]*c.features[j]"
        "+kappa.topic_priority.get(c.topic,0)"
    ),
    "objective_terms": list(OBJECTIVE_TERMS),
    "third_party_revenue_term": False,
    "candidate_provenance": "Every candidate carries a nonempty provenance evidence pointer.",
    "time_source": "Caller-supplied timestamps or deterministic logical:<sequence> timestamps.",
    "limitations": list(LIMITATIONS),
}


@dataclass(frozen=True)
class Authorization:
    """Explicit authorization record sigma_R used by the reference interface.

    ``proposal_hash`` must equal ``proposal_digest(operation, proposal)`` and
    ``version_token`` must name the current objective version.  Constructing
    this object does not authenticate a person or a signature.
    """

    authorization_id: str
    principal: str
    operation: str
    proposal_hash: str
    timestamp: str
    version_token: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "authorization_id": self.authorization_id,
            "principal": self.principal,
            "operation": self.operation,
            "proposal_hash": self.proposal_hash,
            "timestamp": self.timestamp,
            "version_token": self.version_token,
        }


def _canonicalize(value: Any) -> Any:
    """Return a detached JSON-compatible value with deterministic map ordering."""
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("NaN and infinity are not canonical JSON values")
        return value
    if isinstance(value, Mapping):
        result = {}
        for key in sorted(value):
            if not isinstance(key, str):
                raise TypeError("JSON object keys must be strings")
            result[key] = _canonicalize(value[key])
        return result
    if isinstance(value, (list, tuple)):
        return [_canonicalize(item) for item in value]
    raise TypeError(f"Unsupported non-JSON value: {type(value).__name__}")


def _canonical_json(value: Any) -> str:
    return json.dumps(
        _canonicalize(value),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )


def _digest(domain: str, value: Any) -> str:
    material = _canonical_json({"domain": domain, "value": value}).encode("utf-8")
    return hashlib.sha256(material).hexdigest()


def canonical_json(value: Any) -> str:
    """Public canonical-JSON rule shared by the paper, executor and verifier."""
    return _canonical_json(value)


def domain_digest(domain: str, value: Any) -> str:
    """Public domain-separated SHA-256 rule used by all audit records."""
    return _digest(domain, value)


_LOGICAL_TIMESTAMP = re.compile(r"logical:([0-9]{8})")
_RFC3339_TIMESTAMP = re.compile(
    r"([0-9]{4})-([0-9]{2})-([0-9]{2})T"
    r"([01][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])Z"
)


def _timestamp_key(timestamp: Any) -> Optional[tuple[str, Any]]:
    """Return a structural ordering key; never consult a wall clock.

    Guard writes use either deterministic ``logical:NNNNNNNN`` timestamps or
    RFC3339 UTC seconds. A single reference instance cannot mix the two clock
    domains, because no ordering between them is invented.
    """
    if not isinstance(timestamp, str):
        return None
    logical = _LOGICAL_TIMESTAMP.fullmatch(timestamp)
    if logical:
        return "logical", int(logical.group(1))
    match = _RFC3339_TIMESTAMP.fullmatch(timestamp)
    if match:
        year, month, day, hour, minute, second = map(int, match.groups())
        try:
            import datetime as dt
            moment = dt.datetime(year, month, day, hour, minute, second, tzinfo=dt.timezone.utc)
        except ValueError:
            return None
        return "rfc3339", moment
    return None


def _clone(value: Any) -> Any:
    return copy.deepcopy(value)


def proposal_digest(operation: str, proposal: Any) -> str:
    """Bind an authorization record to an operation and its exact proposal."""
    if not isinstance(operation, str) or not operation:
        raise ValueError("operation must be a nonempty string")
    return _digest(
        "sea-governance-proposal/2",
        {"operation": operation, "proposal": _canonicalize(proposal)},
    )


def _nonempty_string(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a nonempty string")
    return value


def _integer(value: Any, name: str, *, nonnegative: bool = False) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be an integer")
    if nonnegative and value < 0:
        raise ValueError(f"{name} must be nonnegative")
    return value


def _evidence(evidence: Sequence[str]) -> list[str]:
    if isinstance(evidence, (str, bytes)) or not isinstance(evidence, Sequence):
        raise ValueError("evidence must be a sequence of pointers")
    result = [_nonempty_string(pointer, "evidence pointer") for pointer in evidence]
    if not result:
        raise ValueError("at least one evidence pointer is required")
    if len(set(result)) != len(result):
        raise ValueError("evidence pointers must be unique")
    return result


def _validate_objective(objective: Mapping[str, Any]) -> dict[str, Any]:
    if set(objective) != {"weights", "g2", "monitoring_list", "thresholds"}:
        raise ValueError("objective has unknown or missing fields")
    weights = objective["weights"]
    if not isinstance(weights, Mapping) or set(weights) != set(OBJECTIVE_TERMS):
        raise ValueError("weights must contain exactly the five declared objective terms")
    for term in OBJECTIVE_TERMS:
        _integer(weights[term], f"weights.{term}", nonnegative=True)
    _nonempty_string(objective["g2"], "g2")
    monitoring = objective["monitoring_list"]
    if not isinstance(monitoring, list):
        raise ValueError("monitoring_list must be a list")
    for topic in monitoring:
        _nonempty_string(topic, "monitoring topic")
    if len(set(monitoring)) != len(monitoring):
        raise ValueError("monitoring_list entries must be unique")
    thresholds = objective["thresholds"]
    if not isinstance(thresholds, Mapping) or set(thresholds) != {"min_utility"}:
        raise ValueError("thresholds must contain exactly min_utility")
    _integer(thresholds["min_utility"], "thresholds.min_utility")
    return _canonicalize(objective)


def _merge_objective(current: Mapping[str, Any], patch: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(patch, Mapping):
        raise ValueError("objective patch must be a mapping")
    if set(patch) - {"weights", "g2", "monitoring_list", "thresholds"}:
        raise ValueError("objective patch contains an undeclared field")
    merged = _clone(current)
    for section in ("weights", "thresholds"):
        if section in patch:
            if not isinstance(patch[section], Mapping):
                raise ValueError(f"{section} patch must be a mapping")
            merged[section].update(_clone(patch[section]))
    for field in ("g2", "monitoring_list"):
        if field in patch:
            merged[field] = _clone(patch[field])
    return _validate_objective(merged)


def _normalize_user_state(user_state: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(user_state, Mapping) or set(user_state) != {"topic_priority"}:
        raise ValueError("user_state must contain exactly topic_priority")
    priorities = user_state["topic_priority"]
    if not isinstance(priorities, Mapping):
        raise ValueError("topic_priority must be a mapping")
    normalized = {}
    for topic, priority in priorities.items():
        _nonempty_string(topic, "topic_priority key")
        _integer(priority, f"topic_priority.{topic}")
        normalized[topic] = priority
    return {"topic_priority": _canonicalize(normalized)}


def _normalize_candidates(candidates: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    if isinstance(candidates, (str, bytes, Mapping)):
        raise ValueError("candidates must be an iterable of candidate mappings")
    normalized = []
    seen = set()
    for candidate in candidates:
        if not isinstance(candidate, Mapping):
            raise ValueError("each candidate must be a mapping")
        if set(candidate) != {"candidate_id", "topic", "features", "provenance"}:
            raise ValueError("candidate has unknown or missing fields")
        candidate_id = _nonempty_string(candidate["candidate_id"], "candidate_id")
        if candidate_id in seen:
            raise ValueError(f"duplicate candidate_id: {candidate_id}")
        seen.add(candidate_id)
        _nonempty_string(candidate["topic"], "candidate.topic")
        _nonempty_string(candidate["provenance"], "candidate.provenance")
        features = candidate["features"]
        if not isinstance(features, Mapping) or set(features) != set(OBJECTIVE_TERMS):
            raise ValueError("candidate features must contain exactly the five objective terms")
        for term in OBJECTIVE_TERMS:
            _integer(features[term], f"features.{term}", nonnegative=True)
        normalized.append(_canonicalize(candidate))
    normalized.sort(key=lambda item: item["candidate_id"])
    return normalized


def _normalize_platform_variables(platform_variables: Optional[Mapping[str, Any]]) -> dict[str, Any]:
    if platform_variables is None:
        return {}
    if not isinstance(platform_variables, Mapping):
        raise ValueError("platform_variables must be a mapping")
    # These values are recorded for counterfactual audit only.  They are never
    # passed to _score or _rank_normalized.
    return _canonicalize(platform_variables)


class GovernanceReference:
    """In-memory deterministic reference implementing the S1--S4 interfaces."""

    def __init__(self) -> None:
        self._defaults = _validate_objective(_DEFAULT_OBJECTIVE)
        self._objective = _clone(self._defaults)
        self._versions = [
            {
                "version": 0,
                "objective": _clone(self._objective),
                "timestamp": "genesis",
                "authorization_id": None,
                "evidence": ["defaults:sea-v1.17"],
                "restored_from": None,
                "audit_sequence": None,
            }
        ]
        self._current_version = 0
        self._records: list[dict[str, Any]] = []
        self._used_authorization_ids: set[str] = set()
        self._last_guard_timestamp: Optional[tuple[str, Any]] = None

    # S1: inspectability -------------------------------------------------
    def inspect_objective(self) -> dict[str, Any]:
        """Return current objective, immutable defaults, history and provenance."""
        return _clone(
            {
                "specification": SPECIFICATION,
                "objective": self._objective,
                "defaults": self._defaults,
                "version": self._current_version,
                "version_token": self.version_token(),
                "objective_sha256": hashlib.sha256(self.objective_bytes()).hexdigest(),
                "versions": self._versions,
                "provenance": _PROVENANCE,
            }
        )

    def objective_bytes(self) -> bytes:
        """Canonical UTF-8 objective bytes used by byte-exact rollback tests."""
        return _canonical_json(self._objective).encode("utf-8")

    def version_token(self) -> str:
        """Unambiguously bind an authorization to version number and bytes."""
        return _digest(
            "sea-governance-version/2",
            {"version": self._current_version, "objective": self._objective},
        )

    # Audit primitives ---------------------------------------------------
    def _append(
        self,
        event: str,
        payload: Mapping[str, Any],
        evidence: Sequence[str],
        timestamp: Optional[str],
    ) -> int:
        sequence = len(self._records) + 1
        if timestamp is None:
            timestamp = f"logical:{sequence:08d}"
        _nonempty_string(timestamp, "timestamp")
        body = {
            "schema": AUDIT_SCHEMA,
            "sequence": sequence,
            "event": _nonempty_string(event, "event"),
            "timestamp": timestamp,
            "evidence": _evidence(evidence),
            "payload": _canonicalize(payload),
            "previous_hash": self._records[-1]["record_hash"] if self._records else GENESIS_HASH,
        }
        record = dict(body)
        record["record_hash"] = _digest("sea-governance-record/2", body)
        self._records.append(record)
        return sequence

    def append_record(self, event: str, payload: Mapping[str, Any], *,
                      evidence: Sequence[str], timestamp: Optional[str] = None) -> int:
        """Append an observed executor event using the one public hash specification.

        This records evidence; it does not itself authorize an objective write or
        assert that a payload is true outside the declared synthetic/reference run.
        """
        return self._append(event, payload, evidence, timestamp)

    def audit_records(self) -> list[dict[str, Any]]:
        """Return a detached export; there is no public edit/delete operation."""
        return _clone(self._records)

    def audit_anchor(self) -> dict[str, Any]:
        """Retain this anchor externally to detect truncation as well as edits."""
        return {
            "length": len(self._records),
            "record_hash": self._records[-1]["record_hash"] if self._records else GENESIS_HASH,
        }

    def verify_audit(
        self,
        records: Optional[Sequence[Mapping[str, Any]]] = None,
        *,
        anchor: Optional[Mapping[str, Any]] = None,
    ) -> dict[str, Any]:
        """Verify record hashes, chain order, evidence and an optional anchor.

        Verification returns diagnostics instead of raising on malformed input.
        Without ``anchor``, a valid prefix cannot be distinguished from a
        truncated log; this limitation is intentional and explicit.
        """
        source = self._records if records is None else records
        errors: list[str] = []
        if not isinstance(source, Sequence) or isinstance(source, (str, bytes)):
            return {"valid": False, "errors": ["records must be a sequence"], "length": 0,
                    "head": GENESIS_HASH}
        previous = GENESIS_HASH
        for index, record in enumerate(source, start=1):
            if not isinstance(record, Mapping):
                errors.append(f"record {index}: not a mapping")
                previous = GENESIS_HASH
                continue
            if record.get("sequence") != index:
                errors.append(f"record {index}: invalid sequence")
            if record.get("schema") != AUDIT_SCHEMA:
                errors.append(f"record {index}: invalid schema")
            if record.get("previous_hash") != previous:
                errors.append(f"record {index}: previous_hash mismatch")
            evidence = record.get("evidence")
            if (not isinstance(evidence, list) or not evidence
                    or any(not isinstance(item, str) or not item for item in evidence)):
                errors.append(f"record {index}: missing evidence pointer")
            try:
                body = {key: _clone(value) for key, value in record.items() if key != "record_hash"}
                expected = _digest("sea-governance-record/2", body)
                if record.get("record_hash") != expected:
                    errors.append(f"record {index}: record_hash mismatch")
            except (TypeError, ValueError) as exc:
                errors.append(f"record {index}: noncanonical content ({exc})")
            supplied_hash = record.get("record_hash")
            previous = supplied_hash if isinstance(supplied_hash, str) else GENESIS_HASH
        head = previous if source else GENESIS_HASH
        if anchor is not None:
            if not isinstance(anchor, Mapping) or set(anchor) != {"length", "record_hash"}:
                errors.append("invalid anchor")
            else:
                if anchor["length"] != len(source):
                    errors.append("anchor length mismatch")
                if anchor["record_hash"] != head:
                    errors.append("anchor head mismatch")
        return {"valid": not errors, "errors": errors, "length": len(source), "head": head}

    # Deterministic admission, ranking and delivery ---------------------
    @staticmethod
    def _score(candidate: Mapping[str, Any], user_state: Mapping[str, Any],
               objective: Mapping[str, Any]) -> int:
        return (
            sum(objective["weights"][term] * candidate["features"][term]
                for term in OBJECTIVE_TERMS)
            + user_state["topic_priority"].get(candidate["topic"], 0)
        )

    @staticmethod
    def _rank_normalized(candidates: Sequence[Mapping[str, Any]],
                         user_state: Mapping[str, Any],
                         objective: Mapping[str, Any]) -> list[dict[str, Any]]:
        scored = [
            {"candidate_id": candidate["candidate_id"],
             "score": GovernanceReference._score(candidate, user_state, objective)}
            for candidate in candidates
        ]
        scored.sort(key=lambda item: (-item["score"], item["candidate_id"]))
        return scored

    def _rank_inputs(self, candidates: Iterable[Mapping[str, Any]],
                     user_state: Mapping[str, Any],
                     platform_variables: Optional[Mapping[str, Any]]) -> tuple[
                         list[dict[str, Any]], dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
        normalized_candidates = _normalize_candidates(candidates)
        normalized_user = _normalize_user_state(user_state)
        normalized_platform = _normalize_platform_variables(platform_variables)
        ranking = self._rank_normalized(normalized_candidates, normalized_user, self._objective)
        return normalized_candidates, normalized_user, normalized_platform, ranking

    def rank(self, candidates: Iterable[Mapping[str, Any]],
             user_state: Mapping[str, Any],
             platform_variables: Optional[Mapping[str, Any]], *,
             evidence: Sequence[str], timestamp: Optional[str] = None,
             record: bool = True,
             context: Optional[Mapping[str, Any]] = None) -> list[dict[str, Any]]:
        """Rank by candidate features and user state, never by platform variables.

        ``record=False`` is a commit-free preview: it returns the same ranking
        without appending an audit record (used by executor selection dry runs).
        ``context`` optionally merges cohort-attribution fields into the payload.
        """
        normalized_candidates, normalized_user, normalized_platform, ranking = self._rank_inputs(
            candidates, user_state, platform_variables
        )
        if record:
            payload = {
                "objective_version": self._current_version,
                "objective_hash": _digest("sea-governance-objective/1", self._objective),
                "candidates": normalized_candidates,
                "candidate_set_hash": _digest("sea-governance-candidates/1", normalized_candidates),
                "user_state": normalized_user,
                "platform_variables": normalized_platform,
                "ranking": ranking,
                "ranking_hash": _digest("sea-governance-ranking/1", ranking),
            }
            if context is not None:
                payload.update(_canonicalize(context))
            self._append("ranking", payload, evidence, timestamp)
        return _clone(ranking)

    def admit(self, candidate: Mapping[str, Any], user_state: Mapping[str, Any], *,
              evidence: Sequence[str], timestamp: Optional[str] = None) -> bool:
        normalized = _normalize_candidates([candidate])[0]
        normalized_user = _normalize_user_state(user_state)
        score = self._score(normalized, normalized_user, self._objective)
        monitored = (not self._objective["monitoring_list"]
                     or normalized["topic"] in self._objective["monitoring_list"])
        admitted = monitored and score >= self._objective["thresholds"]["min_utility"]
        self._append(
            "admission",
            {
                "candidate": normalized,
                "user_state": normalized_user,
                "objective_version": self._current_version,
                "score": score,
                "monitored": monitored,
                "threshold": self._objective["thresholds"]["min_utility"],
                "admitted": admitted,
            },
            evidence,
            timestamp,
        )
        return admitted

    def deliver(self, candidates: Iterable[Mapping[str, Any]],
                user_state: Mapping[str, Any],
                platform_variables: Optional[Mapping[str, Any]], *,
                limit: int, evidence: Sequence[str],
                timestamp: Optional[str] = None) -> list[str]:
        _integer(limit, "limit", nonnegative=True)
        ranking = self.rank(
            candidates, user_state, platform_variables, evidence=evidence, timestamp=timestamp
        )
        ranking_sequence = len(self._records)
        delivered = ranking[:limit]
        self._append(
            "delivery",
            {
                "ranking_sequence": ranking_sequence,
                "limit": limit,
                "delivered_candidate_ids": [item["candidate_id"] for item in delivered],
                "delivered_scores": delivered,
            },
            evidence,
            timestamp,
        )
        return [item["candidate_id"] for item in delivered]

    # S2: authorized objective writes and rollback ----------------------
    def _authorization_error(self, authorization: Optional[Authorization],
                             operation: str, proposal: Any, actor: str) -> Optional[str]:
        if not isinstance(authorization, Authorization):
            return "missing_or_malformed_authorization"
        if actor != REFLECTIVE_PRINCIPAL or authorization.principal != actor:
            return "actor_principal_mismatch"
        if authorization.operation != operation:
            return "operation_mismatch"
        if not authorization.authorization_id:
            return "missing_authorization_id"
        if authorization.authorization_id in self._used_authorization_ids:
            return "authorization_reuse"
        if authorization.version_token != self.version_token():
            return "stale_version_token"
        if authorization.proposal_hash != proposal_digest(operation, proposal):
            return "proposal_hash_mismatch"
        timestamp = _timestamp_key(authorization.timestamp)
        if timestamp is None:
            return "invalid_timestamp"
        if self._last_guard_timestamp is not None:
            previous_family, previous_value = self._last_guard_timestamp
            family, value = timestamp
            if family != previous_family or value <= previous_value:
                return "nonmonotonic_timestamp"
        return None

    def _authorization_valid(self, authorization: Optional[Authorization],
                             operation: str, proposal: Any, actor: str) -> bool:
        return self._authorization_error(authorization, operation, proposal, actor) is None

    def _consume_authorization(self, authorization: Authorization) -> None:
        """Consume a guard-admitted authorization exactly once."""
        self._used_authorization_ids.add(authorization.authorization_id)
        timestamp = _timestamp_key(authorization.timestamp)
        assert timestamp is not None
        self._last_guard_timestamp = timestamp

    @staticmethod
    def _authorization_dict(authorization: Optional[Authorization]) -> Optional[dict[str, Any]]:
        return authorization.as_dict() if isinstance(authorization, Authorization) else None

    def write_objective(self, patch: Mapping[str, Any], *,
                        actor: str, authorization: Optional[Authorization],
                        evidence: Sequence[str],
                        context: Optional[Mapping[str, Any]] = None) -> dict[str, Any]:
        """Apply an explicit patch only with a matching sigma_R record.

        ``weights`` and ``thresholds`` are partial nested patches; ``g2`` and
        ``monitoring_list`` are replacements.  Rejections are also audited.
        ``context`` optionally merges cohort-attribution fields into the payload.
        """
        _nonempty_string(actor, "actor")
        _evidence(evidence)  # validate before any state transition
        normalized_patch = _canonicalize(patch)
        base = {
            "decision": "objective_write",
            "actor": actor,
            "authorization": self._authorization_dict(authorization),
            "patch": normalized_patch,
            "old_value": _clone(self._objective),
            "old_version_token": self.version_token(),
        }
        if context is not None:
            base.update(_canonicalize(context))
        authorization_error = self._authorization_error(
            authorization, "objective_write", normalized_patch, actor)
        if authorization_error is not None:
            payload = dict(base, accepted=False, reason="unauthorized",
                           guard_reject_reason=authorization_error,
                           new_value=_clone(self._objective))
            sequence = self._append("override", payload, evidence, None)
            return {"accepted": False, "reason": "unauthorized",
                    "guard_reject_reason": authorization_error,
                    "version": self._current_version, "audit_sequence": sequence}
        assert isinstance(authorization, Authorization)
        self._consume_authorization(authorization)
        try:
            updated = _merge_objective(self._objective, normalized_patch)
        except (TypeError, ValueError) as exc:
            payload = dict(base, accepted=False, reason=f"invalid_objective: {exc}",
                           new_value=_clone(self._objective))
            sequence = self._append("override", payload, evidence, authorization.timestamp)
            return {"accepted": False, "reason": "invalid_objective",
                    "version": self._current_version, "audit_sequence": sequence}
        if updated == self._objective:
            payload = dict(base, accepted=False, reason="no_change", new_value=_clone(self._objective))
            sequence = self._append("override", payload, evidence, authorization.timestamp)
            return {"accepted": False, "reason": "no_change",
                    "version": self._current_version, "audit_sequence": sequence}

        old_value = _clone(self._objective)
        new_version = len(self._versions)
        sequence = len(self._records) + 1
        self._objective = updated
        self._current_version = new_version
        self._versions.append(
            {
                "version": new_version,
                "objective": _clone(updated),
                "timestamp": authorization.timestamp,
                "authorization_id": authorization.authorization_id,
                "evidence": list(evidence),
                "restored_from": None,
                "audit_sequence": sequence,
            }
        )
        payload = dict(
            base,
            accepted=True,
            reason="authorized",
            new_value=_clone(updated),
            old_version=new_version - 1,
            new_version=new_version,
            new_version_token=self.version_token(),
        )
        actual_sequence = self._append("override", payload, evidence, authorization.timestamp)
        assert actual_sequence == sequence
        return {"accepted": True, "reason": "authorized",
                "version": new_version, "audit_sequence": sequence}

    def rollback(self, target_version: int, *, authorization: Optional[Authorization],
                 evidence: Sequence[str], actor: str = REFLECTIVE_PRINCIPAL,
                 context: Optional[Mapping[str, Any]] = None) -> dict[str, Any]:
        """Append a new version whose objective exactly restores a prior snapshot."""
        _integer(target_version, "target_version", nonnegative=True)
        _nonempty_string(actor, "actor")
        _evidence(evidence)
        proposal = {"target_version": target_version}
        base = {
            "target_version": target_version,
            "actor": actor,
            "authorization": self._authorization_dict(authorization),
            "old_value": _clone(self._objective),
            "old_version_token": self.version_token(),
        }
        if context is not None:
            base.update(_canonicalize(context))
        authorization_error = self._authorization_error(authorization, "rollback", proposal, actor)
        if authorization_error is not None:
            payload = dict(base, accepted=False, reason="unauthorized",
                           guard_reject_reason=authorization_error,
                           new_value=_clone(self._objective))
            sequence = self._append("rollback", payload, evidence, None)
            return {"accepted": False, "reason": "unauthorized",
                    "guard_reject_reason": authorization_error,
                    "version": self._current_version, "audit_sequence": sequence}
        assert isinstance(authorization, Authorization)
        self._consume_authorization(authorization)
        if target_version >= len(self._versions):
            payload = dict(base, accepted=False, reason="unknown_version", new_value=_clone(self._objective))
            sequence = self._append("rollback", payload, evidence, authorization.timestamp)
            return {"accepted": False, "reason": "unknown_version",
                    "version": self._current_version, "audit_sequence": sequence}

        restored = _clone(self._versions[target_version]["objective"])
        old_version = self._current_version
        new_version = len(self._versions)
        sequence = len(self._records) + 1
        self._objective = _clone(restored)
        self._current_version = new_version
        self._versions.append(
            {
                "version": new_version,
                "objective": _clone(restored),
                "timestamp": authorization.timestamp,
                "authorization_id": authorization.authorization_id,
                "evidence": list(evidence),
                "restored_from": target_version,
                "audit_sequence": sequence,
            }
        )
        payload = dict(
            base,
            accepted=True,
            reason="authorized_rollback",
            new_value=_clone(restored),
            old_version=old_version,
            new_version=new_version,
            new_version_token=self.version_token(),
            restored_from=target_version,
        )
        actual_sequence = self._append("rollback", payload, evidence, authorization.timestamp)
        assert actual_sequence == sequence
        return {"accepted": True, "reason": "authorized_rollback",
                "version": new_version, "audit_sequence": sequence}

    # S3: explicit fixed-supply / supply-ecosystem counterfactuals -------
    def compare_counterfactual(self, baseline: Mapping[str, Any],
                               counterfactual: Mapping[str, Any], *,
                               evidence: Sequence[str],
                               timestamp: Optional[str] = None) -> dict[str, Any]:
        """Compare rankings and classify whether candidate supply was held fixed.

        Each scenario contains ``candidates``, ``user_state`` and optional
        ``platform_variables``.  User state must be identical.  Candidate
        ecology changes are never mislabeled as direct platform invariance.
        """
        def prepare(scenario: Mapping[str, Any]) -> tuple[Any, ...]:
            if not isinstance(scenario, Mapping):
                raise ValueError("scenario must be a mapping")
            if set(scenario) - {"candidates", "user_state", "platform_variables"}:
                raise ValueError("scenario has unknown fields")
            if "candidates" not in scenario or "user_state" not in scenario:
                raise ValueError("scenario requires candidates and user_state")
            return self._rank_inputs(
                scenario["candidates"], scenario["user_state"], scenario.get("platform_variables")
            )

        baseline_inputs = prepare(baseline)
        counterfactual_inputs = prepare(counterfactual)
        if baseline_inputs[1] != counterfactual_inputs[1]:
            raise ValueError("counterfactual requires fixed user_state")
        fixed_supply = baseline_inputs[0] == counterfactual_inputs[0]
        baseline_ranking = baseline_inputs[3]
        counterfactual_ranking = counterfactual_inputs[3]
        invariant_holds = baseline_ranking == counterfactual_ranking if fixed_supply else None
        payload = {
            "classification": "fixed-supply" if fixed_supply else "supply-ecosystem",
            "mechanism": "direct-platform-fixed-supply" if fixed_supply else "supply-mediated",
            "objective_version": self._current_version,
            "user_state": baseline_inputs[1],
            "baseline": {
                "candidate_set_hash": _digest("sea-governance-candidates/1", baseline_inputs[0]),
                "platform_variables": baseline_inputs[2],
                "ranking": baseline_ranking,
                "ranking_hash": _digest("sea-governance-ranking/1", baseline_ranking),
            },
            "counterfactual": {
                "candidate_set_hash": _digest("sea-governance-candidates/1", counterfactual_inputs[0]),
                "platform_variables": counterfactual_inputs[2],
                "ranking": counterfactual_ranking,
                "ranking_hash": _digest("sea-governance-ranking/1", counterfactual_ranking),
            },
            "ranking_changed": baseline_ranking != counterfactual_ranking,
            "fixed_supply_invariant_holds": invariant_holds,
        }
        sequence = self._append("counterfactual", payload, evidence, timestamp)
        return dict(_clone(payload), audit_sequence=sequence)

    # S4: contestation and recourse --------------------------------------
    def contest(self, target_sequence: int, *, claimant: str, reason: str,
                requested_recourse: str, evidence: Sequence[str],
                timestamp: Optional[str] = None) -> int:
        _integer(target_sequence, "target_sequence", nonnegative=True)
        if not 1 <= target_sequence <= len(self._records):
            raise ValueError("target_sequence does not identify an audit record")
        return self._append(
            "contestation",
            {
                "target_sequence": target_sequence,
                "claimant": _nonempty_string(claimant, "claimant"),
                "reason": _nonempty_string(reason, "reason"),
                "requested_recourse": _nonempty_string(requested_recourse, "requested_recourse"),
                "status": "open",
            },
            evidence,
            timestamp,
        )

    def record_recourse(self, contestation_sequence: int, *, reviewer: str,
                        outcome: str, evidence: Sequence[str],
                        timestamp: Optional[str] = None) -> int:
        _integer(contestation_sequence, "contestation_sequence", nonnegative=True)
        if not 1 <= contestation_sequence <= len(self._records):
            raise ValueError("contestation_sequence does not identify an audit record")
        if self._records[contestation_sequence - 1]["event"] != "contestation":
            raise ValueError("contestation_sequence must reference a contestation record")
        return self._append(
            "recourse",
            {
                "contestation_sequence": contestation_sequence,
                "reviewer": _nonempty_string(reviewer, "reviewer"),
                "outcome": _nonempty_string(outcome, "outcome"),
                "status": "recorded",
            },
            evidence,
            timestamp,
        )
