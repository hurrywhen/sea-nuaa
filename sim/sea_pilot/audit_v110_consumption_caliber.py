#!/usr/bin/env python3
"""Selected-proxy consumption-caliber audit of the frozen four-family replay.

This is a post-hoc, within-corpus sensitivity analysis.  It makes no model calls,
uses only the 292 immutable replay shards and existing frozen reanalysis outputs,
and never turns ``picked`` into delivered, opened, attended, or actually consumed
items.  Empty ``picked`` lists are a zero **selected proxy**, not proof of zero
historical consumption or of a valid abstention.

Three retrospective descriptive calibers are computed on unique ``(family, run, agent, sim_day)`` keys:

* ``ALL_EXISTING_RECORD_MEAN_ZERO_EMPTY``: every existing key contributes once; within a key,
  every structurally parseable policy record contributes equally, including an
  empty-picked record as zero.  This gives complete 71,970-existing-key support,
  but is a recorded-attempt-mean estimand, not recovered single-run truth.
* ``METRIC_RESOLVED_ZERO_EMPTY``: empty-only keys are zero-filled, while conflicting
  nonempty duplicates remain unresolved separately for recall, citation return,
  and paired sign.  This is frozen scenario G and is checked against all 80 of
  its frozen run rows.  Missing keys are not zero-filled in this caliber.
* ``ALL_EXPECTED_RECORD_MEAN_ZERO_EMPTY_NO_ROW``: all 72,000 expected keys contribute;
  existing keys use the same recorded-attempt mean, and the 30 no-row keys are
  assigned selected-proxy zero as a conservative selection-failure sensitivity.
  This is still not actual consumption or a prospective all-assigned analysis.

Existing nonempty Rule A and strict-singleton scenario C remain secondary.  All
17 existing frozen scenarios are summarized without rerunning them.  A
prospective selected -> delivered -> opened -> operational attendance JSON Schema,
including efficiency measurements, is emitted; no historical values are
backfilled into that schema.

Run from the repository root::

    PYTHONDONTWRITEBYTECODE=1 python3 sim/sea_pilot/audit_v110_consumption_caliber.py
    PYTHONDONTWRITEBYTECODE=1 python3 sim/sea_pilot/audit_v110_consumption_caliber.py --write

Default behavior is stdout only.  ``--write`` emits only the dedicated artifacts
under ``sim/pilot/results/v110_consumption_caliber/``.  Replacement requires
``--force``.  Dependencies: Python >= 3.10 and NumPy.
"""
from __future__ import annotations

import argparse
import collections
import csv
import gzip
import hashlib
import io
import json
import math
import os
import platform
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Iterator, Sequence

import numpy as np

try:  # Support direct execution and module imports without running any replay.
    from .audit_replay_integrity import (
        EXPECTED_RUNS,
        EXPECTED_SHARDS,
        FAMILY_OF,
        FAMILY_ORDER,
        TAG_RE,
    )
except ImportError:  # pragma: no cover - used by the documented CLI
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from sea_pilot.audit_replay_integrity import (
        EXPECTED_RUNS,
        EXPECTED_SHARDS,
        FAMILY_OF,
        FAMILY_ORDER,
        TAG_RE,
    )

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "sim" / "pilot" / "results"
FROZEN_DIR = RESULTS / "frozen_reanalysis_v1"
FROZEN_SUMMARY = FROZEN_DIR / "summary.json"
FROZEN_RUN_METRICS = FROZEN_DIR / "run_metrics.csv"
OUTDIR = RESULTS / "v110_consumption_caliber"
VERSION = "1.2.0"
SCHEMA = "sea.v110.selected-proxy-consumption-caliber/v3"
STATUS = "POST_HOC_SELECTED_PROXY_RETROSPECTIVE_DESCRIPTIVE__WITHIN_CORPUS_EXPLORATORY"
NOMINAL_PER_RUN = 900
NOMINAL_TOTAL = 72000
BOOTSTRAP_B = 10000
BOOTSTRAP_SEED = 42
NEW_CALIBERS = (
    "ALL_EXISTING_RECORD_MEAN_ZERO_EMPTY",
    "METRIC_RESOLVED_ZERO_EMPTY",
    "ALL_EXPECTED_RECORD_MEAN_ZERO_EMPTY_NO_ROW",
)
MEAN_CALIBERS = {
    "ALL_EXISTING_RECORD_MEAN_ZERO_EMPTY",
    "ALL_EXPECTED_RECORD_MEAN_ZERO_EMPTY_NO_ROW",
}
# Input-only aliases for external code written against v1.10. Outputs never use
# the misleading historical intention-to-treat labels.
LEGACY_CALIBER_ALIASES = {
    "ITT_ALL_RECORD_MEAN": "ALL_EXISTING_RECORD_MEAN_ZERO_EMPTY",
    "ITT_METRIC_RESOLVED": "METRIC_RESOLVED_ZERO_EMPTY",
}
SECONDARY_CALIBERS = ("RULE_A_NONEMPTY", "STRICT_SINGLETON_NONEMPTY")
ARTIFACT_NAMES = (
    "summary.json",
    "REPORT.md",
    "run_metrics.csv",
    "scenario_effects.csv",
    "key_ledger.jsonl.gz",
    "future_logging_schema.json",
    "input_manifest.json",
)
RUN_COLUMNS = (
    "caliber", "source", "family", "run", "expected_keys", "existing_keys",
    "nonempty_keys", "empty_only_keys", "missing_keys", "raw_records",
    "nonempty_records", "empty_records", "empty_records_on_nonempty_keys",
    "nonempty_duplicate_excess", "n_recall", "n_return", "n_sign",
    "sum_n_crit_recall", "sum_hits_llm", "sum_hits_param", "sum_delta_return",
    "recall_llm", "recall_param", "delta_recall", "delta_return",
    "recall_conflicts", "return_conflicts", "sign_conflicts",
    "any_six_field_conflicts", "excluded_conflict_recall",
    "excluded_conflict_return", "excluded_conflict_sign",
)


@dataclass(frozen=True, slots=True)
class PolicyRecord:
    """A structurally parseable log row; this is not LLM-output validity."""

    agent: int
    sim_day: int
    picked: tuple[Any, ...]
    hits_llm: int
    hits_param: int
    n_crit: int
    value_llm: float
    value_param: float
    source_file: str
    source_line: int
    reason_class: str
    raw_consume_class: str

    @property
    def nonempty(self) -> bool:
        return bool(self.picked)

    @property
    def delta_return(self) -> float:
        # Empty picked is forced to selected-proxy zero by construction/validation.
        return float(self.value_llm) - float(self.value_param)

    @property
    def sign(self) -> int:
        return (self.hits_llm > self.hits_param) - (self.hits_llm < self.hits_param)

    @property
    def six_field_signature(self) -> str:
        return json.dumps(
            [self.picked, self.hits_llm, self.hits_param, self.n_crit,
             self.value_llm, self.value_param],
            ensure_ascii=False, separators=(",", ":"), allow_nan=False,
        )


@dataclass(frozen=True, slots=True)
class CanonicalDay:
    hits_param: int
    n_crit: int
    value_param: float


@dataclass(slots=True)
class KeyState:
    family: str
    run: int
    agent: int
    sim_day: int
    records: list[PolicyRecord]
    canonical: CanonicalDay
    full_hits_llm: float | None
    full_delta_return: float | None
    resolved_recall: tuple[float, float, float] | None
    resolved_delta_return: float | None
    resolved_sign: int | None
    recall_conflict: bool
    return_conflict: bool
    sign_conflict: bool
    any_six_field_conflict: bool

    @property
    def nonempty_records(self) -> list[PolicyRecord]:
        return [record for record in self.records if record.nonempty]

    @property
    def n_empty(self) -> int:
        return len(self.records) - sum(record.nonempty for record in self.records)

    @property
    def existing(self) -> bool:
        return bool(self.records)

    @property
    def empty_only(self) -> bool:
        return bool(self.records) and not any(record.nonempty for record in self.records)

    @property
    def nonempty_key(self) -> bool:
        return any(record.nonempty for record in self.records)


@dataclass(slots=True)
class LoadResult:
    runs: dict[tuple[str, int], list[PolicyRecord]]
    manifest: list[dict[str, Any]]
    skipped: list[str]
    observability: dict[str, Any]


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _sha256_json(value: Any) -> str:
    data = json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")
    return _sha256_bytes(data)


def _relative(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def _finite_number(value: Any, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{label} must be numeric, got {value!r}")
    answer = float(value)
    if not math.isfinite(answer):
        raise ValueError(f"{label} must be finite")
    return answer


def _nonnegative_integer(value: Any, label: str) -> int:
    number = _finite_number(value, label)
    if not number.is_integer() or number < 0:
        raise ValueError(f"{label} must be a nonnegative integer, got {value!r}")
    return int(number)


def _raw_consume_class(value: Any) -> str:
    if value is None:
        return "NULL"
    if isinstance(value, list):
        return "EMPTY_LIST" if not value else "NONEMPTY_LIST"
    return type(value).__name__.upper()


def _parse_policy_record(
    value: Any, family: str, run: int, source_file: str, source_line: int,
) -> PolicyRecord:
    """Validate log structure, never the historical cause of an empty selection."""
    label = f"{source_file}:{source_line}"
    if not isinstance(value, dict):
        raise ValueError(f"{label}: top-level JSON value is not an object")
    required = {
        "agent", "sim_day", "picked", "hits_llm", "hits_param", "n_crit",
        "value_llm", "value_param",
    }
    missing = sorted(required - set(value))
    if missing:
        raise ValueError(f"{label}: missing policy fields {missing}")
    agent = value["agent"]
    day = value["sim_day"]
    if (isinstance(agent, bool) or not isinstance(agent, int) or not 0 <= agent < 30
            or isinstance(day, bool) or not isinstance(day, int) or not 0 <= day < 30):
        raise ValueError(f"{label}: out-of-grid agent/sim_day {(agent, day)!r}")
    picked_value = value["picked"]
    if not isinstance(picked_value, list):
        raise ValueError(f"{label}: picked must be a list")
    if any(isinstance(item, bool) or not isinstance(item, (str, int)) for item in picked_value):
        raise ValueError(f"{label}: picked ids must be strings or integers")
    picked = tuple(picked_value)
    hl = _nonnegative_integer(value["hits_llm"], f"{label}.hits_llm")
    hp = _nonnegative_integer(value["hits_param"], f"{label}.hits_param")
    nc = _nonnegative_integer(value["n_crit"], f"{label}.n_crit")
    vl = _finite_number(value["value_llm"], f"{label}.value_llm")
    vp = _finite_number(value["value_param"], f"{label}.value_param")
    if hl > nc or hp > nc:
        raise ValueError(f"{label}: hits exceed n_crit")
    if vl < 0 or vp < 0:
        raise ValueError(f"{label}: negative citation return")
    if not picked and (hl != 0 or vl != 0):
        raise ValueError(f"{label}: empty picked has nonzero selected-proxy outcome")
    reason = value.get("reason")
    reason_class = "POLICY_PARSE_ERROR" if reason == "parse-error" else "OTHER"
    return PolicyRecord(
        agent=agent, sim_day=day, picked=picked, hits_llm=hl, hits_param=hp,
        n_crit=nc, value_llm=vl, value_param=vp, source_file=source_file,
        source_line=source_line, reason_class=reason_class,
        raw_consume_class=_raw_consume_class(value.get("raw_consume")),
    )


def load_raw(results_dir: Path, frozen_manifest: list[dict[str, Any]]) -> LoadResult:
    """Read bytes once, hash-check the frozen inputs, and classify failures explicitly."""
    expected_by_file = {entry["file"]: entry for entry in frozen_manifest}
    runs: dict[tuple[str, int], list[PolicyRecord]] = collections.defaultdict(list)
    manifest: list[dict[str, Any]] = []
    skipped: list[str] = []
    counts: collections.Counter[str] = collections.Counter()
    reason_by_family: dict[str, collections.Counter[str]] = {
        family: collections.Counter() for family in FAMILY_ORDER
    }
    raw_consume_on_empty: collections.Counter[str] = collections.Counter()
    field_presence: collections.Counter[str] = collections.Counter()
    picked_length: collections.Counter[str] = collections.Counter()
    invalid_examples: list[dict[str, Any]] = []
    transport_examples: list[dict[str, Any]] = []

    for path in sorted(results_dir.glob("llm_replay_*.jsonl")):
        tag = path.name[len("llm_replay_"):-len(".jsonl")]
        match = TAG_RE.match(tag)
        if not match:
            skipped.append(tag)
            continue
        family = FAMILY_OF[match.group(1)]
        run = int(match.group(2))
        counts["accepted_shards"] += 1
        try:
            data = path.read_bytes()
        except (OSError, UnicodeError) as exc:  # Observable current-file transport only.
            counts["file_transport_failures"] += 1
            transport_examples.append({"file": path.name, "error": str(exc)})
            continue
        entry = {
            "path": _relative(path), "file": path.name, "size_bytes": len(data),
            "line_count": sum(bool(line.strip()) for line in data.splitlines()),
            "line_count_definition": "nonblank JSONL records",
            "sha256": _sha256_bytes(data),
        }
        expected = expected_by_file.get(path.name)
        entry["matches_frozen_manifest"] = bool(
            expected and all(entry[field] == expected[field] for field in
                             ("path", "size_bytes", "line_count", "sha256"))
        )
        if entry["matches_frozen_manifest"]:
            counts["manifest_matching_shards"] += 1
        manifest.append(entry)
        for line_number, raw_line in enumerate(data.splitlines(), start=1):
            if not raw_line.strip():
                counts["blank_lines"] += 1
                continue
            counts["nonblank_lines"] += 1
            try:
                text = raw_line.decode("utf-8")
                value = json.loads(text)
            except (UnicodeError, json.JSONDecodeError) as exc:
                counts["jsonl_decode_or_parse_failures"] += 1
                if len(invalid_examples) < 20:
                    invalid_examples.append({
                        "file": path.name, "line": line_number,
                        "class": "JSONL_DECODE_OR_PARSE", "error": str(exc),
                    })
                continue
            if isinstance(value, dict):
                field_presence.update(value.keys())
            try:
                record = _parse_policy_record(value, family, run, path.name, line_number)
            except (ValueError, TypeError) as exc:
                counts["invalid_policy_records"] += 1
                if len(invalid_examples) < 20:
                    invalid_examples.append({
                        "file": path.name, "line": line_number,
                        "class": "INVALID_POLICY_RECORD", "error": str(exc),
                    })
                continue
            counts["valid_parseable_policy_records"] += 1
            counts["nonempty_records" if record.nonempty else "empty_records"] += 1
            picked_length[str(len(record.picked))] += 1
            if not record.nonempty:
                reason_by_family[family][record.reason_class] += 1
                raw_consume_on_empty[record.raw_consume_class] += 1
                if record.reason_class == "POLICY_PARSE_ERROR":
                    counts["policy_reported_parse_error_records"] += 1
                else:
                    counts["empty_records_with_other_reason"] += 1
            runs[(family, run)].append(record)

    got_runs = {family: {run for fam, run in runs if fam == family}
                for family in EXPECTED_RUNS}
    missing_runs = {
        family: sorted(EXPECTED_RUNS[family] - got_runs[family])
        for family in FAMILY_ORDER
        if EXPECTED_RUNS[family] - got_runs[family]
    }
    if counts["accepted_shards"] != EXPECTED_SHARDS or len(manifest) != EXPECTED_SHARDS:
        raise ValueError(f"Expected {EXPECTED_SHARDS} accepted shards, got {len(manifest)}")
    if missing_runs:
        raise ValueError(f"Missing expected runs: {missing_runs}")
    if set(expected_by_file) != {entry["file"] for entry in manifest}:
        raise ValueError("Current accepted shard names differ from the frozen manifest")
    if counts["manifest_matching_shards"] != EXPECTED_SHARDS:
        mismatches = [entry["file"] for entry in manifest if not entry["matches_frozen_manifest"]]
        raise ValueError(f"Frozen input hash/size/line-count mismatch: {mismatches[:20]}")
    if counts["file_transport_failures"] or counts["jsonl_decode_or_parse_failures"] or counts["invalid_policy_records"]:
        raise ValueError(
            "The frozen snapshot no longer satisfies the validated all-record schema; "
            f"transport={counts['file_transport_failures']}, "
            f"json={counts['jsonl_decode_or_parse_failures']}, "
            f"invalid={counts['invalid_policy_records']}; examples={invalid_examples or transport_examples}"
        )

    observed_fields = sorted(field_presence)
    prospective_stage_fields = (
        "delivered", "delivered_at", "delivery_status", "opened", "opened_at",
        "open_status", "attended", "attended_at", "attendance_status", "consumed",
        "consumed_at", "consumption_status", "actual_consumption",
    )
    efficiency_fields = (
        "calls", "input_tokens", "output_tokens", "cost", "cost_usd",
        "latency", "latency_ms", "retries",
    )
    observability = {
        "scope": "Fields and failures observable in the frozen JSONL snapshot only; not a reconstruction of historical API transport.",
        "counts": dict(sorted(counts.items())),
        "invalid_record_examples_capped20": invalid_examples,
        "transport_error_examples_capped20": transport_examples,
        "policy_reported_parse_errors_by_family": {
            family: dict(sorted(reason_by_family[family].items())) for family in FAMILY_ORDER
        },
        "raw_consume_type_on_empty_picked": dict(sorted(raw_consume_on_empty.items())),
        "picked_length_records": dict(sorted(picked_length.items(), key=lambda item: int(item[0]))),
        "observed_top_level_field_union": observed_fields,
        "delivery_open_attendance_actual_consumption_field_counts": {
            field: field_presence[field] for field in prospective_stage_fields
        },
        "historical_efficiency_field_counts": {
            field: field_presence[field] for field in efficiency_fields
        },
        "impulse_consumed_interpretation": "Present, but counts injected-impulse events; it is not delivered/opened/attended/actual consumption of picked items.",
        "raw_consume_interpretation": "Raw policy-output diagnostic only; it is not delivery, opening, attendance, or actual-consumption evidence.",
        "empty_selection_identification_limit": (
            "Historical logs cannot distinguish a valid abstention from silent empty-selection "
            "execution failure. reason='parse-error' is an observed policy-output parse failure; "
            "other reason text is not retrospectively adjudicated."
        ),
    }
    return LoadResult(runs=runs, manifest=manifest, skipped=skipped, observability=observability)


def canonical_days(
    runs: dict[tuple[str, int], list[PolicyRecord]],
) -> dict[tuple[str, int, int], CanonicalDay]:
    """Recover the daily parameter triple using every record, including empty picked."""
    answer: dict[tuple[str, int, int], CanonicalDay] = {}
    for (family, run), records in sorted(runs.items()):
        by_day: dict[int, list[PolicyRecord]] = collections.defaultdict(list)
        for record in records:
            by_day[record.sim_day].append(record)
        if set(by_day) != set(range(30)):
            raise ValueError(f"Cannot recover canonical days for {family}/run {run}")
        for day in range(30):
            triples = {(r.hits_param, r.n_crit, r.value_param) for r in by_day[day]}
            if len(triples) != 1:
                raise ValueError(f"Non-unique daily parameter triple at {family}/run {run}/day {day}")
            hp, nc, vp = next(iter(triples))
            answer[(family, run, day)] = CanonicalDay(hp, nc, vp)
    return answer


def _consistent(values: Iterable[Any]) -> Any | None:
    materialized = list(values)
    if not materialized:
        return None
    first = materialized[0]
    return first if all(value == first for value in materialized[1:]) else None


def build_states(
    runs: dict[tuple[str, int], list[PolicyRecord]],
    canonical: dict[tuple[str, int, int], CanonicalDay],
) -> list[KeyState]:
    states: list[KeyState] = []
    for family in FAMILY_ORDER:
        for run in sorted(EXPECTED_RUNS[family]):
            grouped: dict[tuple[int, int], list[PolicyRecord]] = collections.defaultdict(list)
            for record in runs[(family, run)]:
                grouped[(record.agent, record.sim_day)].append(record)
            for agent in range(30):
                for day in range(30):
                    records = grouped.get((agent, day), [])
                    day_parameters = canonical[(family, run, day)]
                    nonempty = [record for record in records if record.nonempty]
                    n_records = len(records)
                    if not records:
                        states.append(KeyState(
                            family, run, agent, day, records, day_parameters,
                            None, None, None, None, None,
                            False, False, False, False,
                        ))
                        continue

                    # Every raw policy record has equal weight within its key. Each key
                    # contributes one record-averaged numerator and one canonical n_crit
                    # denominator. Run recall is a ratio of sums (not an equal-key mean
                    # of recall ratios); return is an equal-key mean of attempt means.
                    full_hits = math.fsum(record.hits_llm for record in records) / n_records
                    full_delta = math.fsum(record.delta_return for record in records) / n_records

                    if nonempty:
                        recall_pair = _consistent((r.hits_llm, r.n_crit) for r in nonempty)
                        resolved_recall = (
                            (float(recall_pair[0]), float(day_parameters.hits_param),
                             float(day_parameters.n_crit))
                            if recall_pair is not None else None
                        )
                        resolved_delta = _consistent(r.delta_return for r in nonempty)
                        resolved_sign = _consistent(r.sign for r in nonempty)
                        six_consistent = len({r.six_field_signature for r in nonempty}) == 1
                    else:
                        # This is the only new zero assignment: an existing key whose
                        # every structurally parseable policy record has picked=[].
                        resolved_recall = (
                            0.0, float(day_parameters.hits_param), float(day_parameters.n_crit)
                        )
                        resolved_delta = -float(day_parameters.value_param)
                        resolved_sign = ((0 > day_parameters.hits_param)
                                         - (0 < day_parameters.hits_param))
                        six_consistent = True

                    states.append(KeyState(
                        family=family, run=run, agent=agent, sim_day=day,
                        records=records, canonical=day_parameters,
                        full_hits_llm=full_hits, full_delta_return=full_delta,
                        resolved_recall=resolved_recall,
                        resolved_delta_return=resolved_delta,
                        resolved_sign=resolved_sign,
                        recall_conflict=bool(nonempty) and resolved_recall is None,
                        return_conflict=bool(nonempty) and resolved_delta is None,
                        sign_conflict=bool(nonempty) and resolved_sign is None,
                        any_six_field_conflict=bool(nonempty) and not six_consistent,
                    ))
    if len(states) != NOMINAL_TOTAL:
        raise AssertionError(f"Expected {NOMINAL_TOTAL} keys, got {len(states)}")
    return states


def _structure_for_states(states: Sequence[KeyState]) -> dict[str, Any]:
    nonempty_keys = sum(state.nonempty_key for state in states)
    nonempty_records = sum(sum(record.nonempty for record in state.records) for state in states)
    existing = sum(state.existing for state in states)
    return {
        "expected_keys": len(states),
        "existing_keys": existing,
        "nonempty_keys": nonempty_keys,
        "empty_only_keys": sum(state.empty_only for state in states),
        "missing_keys": sum(not state.existing for state in states),
        "raw_records": sum(len(state.records) for state in states),
        "nonempty_records": nonempty_records,
        "empty_records": sum(state.n_empty for state in states),
        "empty_records_on_nonempty_keys": sum(
            state.n_empty for state in states if state.nonempty_key
        ),
        "mixed_empty_nonempty_keys": sum(
            state.nonempty_key and state.n_empty > 0 for state in states
        ),
        "nonempty_duplicate_excess": nonempty_records - nonempty_keys,
        "all_record_excess_over_existing_keys": sum(len(state.records) for state in states) - existing,
        "nonempty_duplicate_key_groups": sum(
            sum(record.nonempty for record in state.records) > 1 for state in states
        ),
        "recall_conflicts_nonempty": sum(state.recall_conflict for state in states),
        "return_conflicts_nonempty": sum(state.return_conflict for state in states),
        "sign_conflicts_nonempty": sum(state.sign_conflict for state in states),
        "any_six_field_conflicts_nonempty": sum(state.any_six_field_conflict for state in states),
        "resolved_zero_empty_recall": sum(state.resolved_recall is not None for state in states),
        "resolved_zero_empty_return": sum(state.resolved_delta_return is not None for state in states),
        "resolved_zero_empty_sign": sum(state.resolved_sign is not None for state in states),
        "full_existing_recall": sum(state.full_hits_llm is not None for state in states),
        "full_existing_return": sum(state.full_delta_return is not None for state in states),
    }


def canonical_caliber(name: str) -> str:
    """Resolve an input alias and reject unknown new-caliber names."""
    resolved = LEGACY_CALIBER_ALIASES.get(name, name)
    if resolved not in NEW_CALIBERS:
        raise ValueError(f"Unknown retrospective caliber: {name}")
    return resolved


def _new_run_row(
    caliber: str, state_group: Sequence[KeyState], family: str, run: int,
) -> dict[str, Any]:
    caliber = canonical_caliber(caliber)
    if len(state_group) != NOMINAL_PER_RUN:
        raise ValueError(f"Expected 900 keys at {family}/run {run}")
    if caliber == "ALL_EXISTING_RECORD_MEAN_ZERO_EMPTY":
        recall_values = [
            (state.full_hits_llm, float(state.canonical.hits_param),
             float(state.canonical.n_crit))
            for state in state_group if state.full_hits_llm is not None
        ]
        returns = [state.full_delta_return for state in state_group
                   if state.full_delta_return is not None]
        signs: list[int] = []
        sign_applicable = False
    elif caliber == "ALL_EXPECTED_RECORD_MEAN_ZERO_EMPTY_NO_ROW":
        recall_values = []
        returns = []
        for state in state_group:
            if state.full_hits_llm is not None:
                recall_values.append((state.full_hits_llm, float(state.canonical.hits_param),
                                      float(state.canonical.n_crit)))
                returns.append(state.full_delta_return)
            else:
                # Conservative selected-proxy failure assignment for no-row keys.
                recall_values.append((0.0, float(state.canonical.hits_param),
                                      float(state.canonical.n_crit)))
                returns.append(-float(state.canonical.value_param))
        signs = []
        sign_applicable = False
    elif caliber == "METRIC_RESOLVED_ZERO_EMPTY":
        recall_values = [state.resolved_recall for state in state_group
                         if state.resolved_recall is not None]
        returns = [state.resolved_delta_return for state in state_group
                   if state.resolved_delta_return is not None]
        signs = [state.resolved_sign for state in state_group if state.resolved_sign is not None]
        sign_applicable = True
    else:  # pragma: no cover - internal programmer error
        raise AssertionError(caliber)

    sum_hl = math.fsum(float(item[0]) for item in recall_values)
    sum_hp = math.fsum(float(item[1]) for item in recall_values)
    sum_nc = math.fsum(float(item[2]) for item in recall_values)
    sum_return = math.fsum(float(value) for value in returns)
    structure = _structure_for_states(state_group)
    row: dict[str, Any] = {
        "caliber": caliber,
        "source": "new raw-record computation on hash-verified frozen shards",
        "family": family,
        "run": run,
        **structure,
        "n_recall": len(recall_values),
        "n_return": len(returns),
        "n_sign": len(signs) if sign_applicable else None,
        "sum_n_crit_recall": sum_nc,
        "sum_hits_llm": sum_hl,
        "sum_hits_param": sum_hp,
        "sum_delta_return": sum_return,
        "recall_llm": sum_hl / sum_nc if sum_nc else None,
        "recall_param": sum_hp / sum_nc if sum_nc else None,
        "delta_recall": (sum_hl - sum_hp) / sum_nc if sum_nc else None,
        "delta_return": sum_return / len(returns) if returns else None,
        "recall_conflicts": structure["recall_conflicts_nonempty"],
        "return_conflicts": structure["return_conflicts_nonempty"],
        "sign_conflicts": structure["sign_conflicts_nonempty"],
        "any_six_field_conflicts": structure["any_six_field_conflicts_nonempty"],
        "excluded_conflict_recall": (
            0 if caliber in MEAN_CALIBERS else structure["recall_conflicts_nonempty"]
        ),
        "excluded_conflict_return": (
            0 if caliber in MEAN_CALIBERS else structure["return_conflicts_nonempty"]
        ),
        "excluded_conflict_sign": (
            0 if caliber in MEAN_CALIBERS else structure["sign_conflicts_nonempty"]
        ) if sign_applicable else None,
    }
    if caliber == "ALL_EXISTING_RECORD_MEAN_ZERO_EMPTY":
        if row["n_recall"] != row["existing_keys"] or row["n_return"] != row["existing_keys"]:
            raise AssertionError(f"Incomplete all-existing-key support at {family}/run {run}")
    if caliber == "ALL_EXPECTED_RECORD_MEAN_ZERO_EMPTY_NO_ROW":
        if row["n_recall"] != row["expected_keys"] or row["n_return"] != row["expected_keys"]:
            raise AssertionError(f"Incomplete all-expected-key support at {family}/run {run}")
    return row


def compute_new_run_rows(states: Sequence[KeyState]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[tuple[str, int], list[KeyState]] = collections.defaultdict(list)
    for state in states:
        grouped[(state.family, state.run)].append(state)
    return {
        caliber: [
            _new_run_row(caliber, grouped[(family, run)], family, run)
            for family in FAMILY_ORDER for run in sorted(EXPECTED_RUNS[family])
        ]
        for caliber in NEW_CALIBERS
    }


def _bootstrap_summary(values: Sequence[float | None], indices: np.ndarray) -> dict[str, Any]:
    if any(value is None for value in values):
        raise ValueError("Cannot delete a run with an undefined metric from run-level resampling")
    array = np.asarray(values, dtype=float)
    if not np.all(np.isfinite(array)) or len(array) != indices.shape[1]:
        raise ValueError("Invalid run metric or bootstrap plan")
    means = array[indices].mean(axis=1)
    return {
        "estimate": float(array.mean()),
        "ci95": [float(value) for value in np.percentile(means, [2.5, 97.5])],
        "n_runs": len(array),
    }


def _aggregate_new(rows: Sequence[dict[str, Any]]) -> dict[str, Any]:
    output: dict[str, Any] = {"families": {}}
    for family in FAMILY_ORDER:
        selected = sorted((row for row in rows if row["family"] == family),
                          key=lambda row: row["run"])
        rng = np.random.default_rng(BOOTSTRAP_SEED)
        indices = rng.integers(0, len(selected), size=(BOOTSTRAP_B, len(selected)))
        equal = {
            metric: _bootstrap_summary([row[metric] for row in selected], indices)
            for metric in ("recall_llm", "recall_param", "delta_recall", "delta_return")
        }
        structure_totals = {
            key: sum(row[key] for row in selected)
            for key in (
                "expected_keys", "existing_keys", "nonempty_keys", "empty_only_keys",
                "missing_keys", "raw_records", "nonempty_records", "empty_records",
                "empty_records_on_nonempty_keys", "mixed_empty_nonempty_keys",
                "nonempty_duplicate_excess", "all_record_excess_over_existing_keys",
                "nonempty_duplicate_key_groups", "recall_conflicts_nonempty",
                "return_conflicts_nonempty", "sign_conflicts_nonempty",
                "any_six_field_conflicts_nonempty",
            )
        }
        output["families"][family] = {
            **structure_totals,
            "n_recall": sum(row["n_recall"] for row in selected),
            "n_return": sum(row["n_return"] for row in selected),
            "n_sign": (sum(row["n_sign"] for row in selected)
                       if selected[0]["n_sign"] is not None else None),
            "sum_n_crit_recall": math.fsum(row["sum_n_crit_recall"] for row in selected),
            "equal_run": equal,
            "pooled_agent_day_sensitivity": {
                "recall_llm": (math.fsum(row["sum_hits_llm"] for row in selected)
                               / math.fsum(row["sum_n_crit_recall"] for row in selected)),
                "recall_param": (math.fsum(row["sum_hits_param"] for row in selected)
                                 / math.fsum(row["sum_n_crit_recall"] for row in selected)),
                "delta_recall": (
                    (math.fsum(row["sum_hits_llm"] for row in selected)
                     - math.fsum(row["sum_hits_param"] for row in selected))
                    / math.fsum(row["sum_n_crit_recall"] for row in selected)
                ),
                "delta_return": (math.fsum(row["sum_delta_return"] for row in selected)
                                 / sum(row["n_return"] for row in selected)),
            },
        }
    return output


def _load_frozen() -> tuple[dict[str, Any], list[dict[str, str]]]:
    summary = json.loads(FROZEN_SUMMARY.read_text(encoding="utf-8"))
    with FROZEN_RUN_METRICS.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if summary.get("schema") != "sea.controlled_unique_key_reanalysis/v1":
        raise ValueError("Unexpected frozen summary schema")
    if len(summary.get("scenario_order", [])) != 17 or len(rows) != 17 * 80:
        raise ValueError("Expected all 17 frozen scenarios and 1,360 run rows")
    structure = summary["structure"]
    expected_resolved = {
        "resolved_recall_A": 71573,
        "resolved_value_A": 70676,
        "resolved_sign_A": 71618,
    }
    for field, expected in expected_resolved.items():
        if structure[field] != expected:
            raise ValueError(f"Frozen Rule-A denominator mismatch: {field}={structure[field]}")
    return summary, rows


def _validate_raw_against_frozen(
    structure: dict[str, Any], frozen: dict[str, Any],
) -> None:
    reference = frozen["structure"]
    comparisons = {
        "expected_keys": "expected_keys",
        "nonempty_keys": "valid_unique_keys",
        "empty_only_keys": "empty_only_keys",
        "missing_keys": "no_surviving_row_keys",
        "raw_records": "raw_rows",
        "nonempty_records": "valid_records",
        "empty_records_on_nonempty_keys": "empty_records_on_valid_keys",
        "nonempty_duplicate_excess": "duplicate_excess_records",
        "recall_conflicts_nonempty": "recall_conflicts_A",
        "return_conflicts_nonempty": "value_conflicts_A",
        "sign_conflicts_nonempty": "sign_conflicts_A",
        "any_six_field_conflicts_nonempty": None,
    }
    failures: dict[str, Any] = {}
    for observed_field, frozen_field in comparisons.items():
        if frozen_field is None:
            continue
        if structure[observed_field] != reference[frozen_field]:
            failures[observed_field] = {
                "observed": structure[observed_field], "frozen": reference[frozen_field]
            }
    # Six-field consistency is scenario D; 1,389 unresolved = 1,608 duplicate
    # groups minus 219 same-outcome groups in the immutable integrity audit.
    expected_six_conflicts = structure["nonempty_keys"] - reference["resolved_D"]
    if structure["any_six_field_conflicts_nonempty"] != expected_six_conflicts:
        failures["any_six_field_conflicts_nonempty"] = {
            "observed": structure["any_six_field_conflicts_nonempty"],
            "expected_from_frozen_D": expected_six_conflicts,
        }
    expected_resolved = {
        "resolved_zero_empty_recall": reference["resolved_recall_A"] + reference["empty_only_keys"],
        "resolved_zero_empty_return": reference["resolved_value_A"] + reference["empty_only_keys"],
        "resolved_zero_empty_sign": reference["resolved_sign_A"] + reference["empty_only_keys"],
        "existing_keys": reference["valid_unique_keys"] + reference["empty_only_keys"],
    }
    for field, expected in expected_resolved.items():
        if structure[field] != expected:
            failures[field] = {"observed": structure[field], "expected": expected}
    if failures:
        raise ValueError(f"Raw/frozen structural mismatch: {failures}")


def _validate_resolved_is_frozen_g(
    rows: list[dict[str, Any]], frozen_rows: list[dict[str, str]],
) -> dict[str, Any]:
    reference = {
        (row["family"], int(row["run"])): row
        for row in frozen_rows if row["scenario"] == "G"
    }
    if len(reference) != 80 or len(rows) != 80:
        raise ValueError("Expected 80 new and 80 frozen-G rows")
    comparisons = {
        "n_recall": "n_resolved_recall",
        "n_return": "n_resolved_value",
        "n_sign": "n_resolved_sign",
        "sum_n_crit_recall": "sum_n_crit",
        "sum_hits_llm": "sum_hits_llm",
        "sum_hits_param": "sum_hits_param",
        "sum_delta_return": "sum_delta_value",
        "recall_llm": "recall_llm",
        "recall_param": "recall_param",
        "delta_recall": "delta_recall",
        "delta_return": "delta_value",
    }
    max_error = 0.0
    for row in rows:
        old = reference[(row["family"], row["run"])]
        for new_field, old_field in comparisons.items():
            new_value = row[new_field]
            old_value = old[old_field]
            if new_field.startswith("n_"):
                if int(new_value) != int(old_value):
                    raise AssertionError(f"Scenario-G denominator mismatch: {row['family']}/{row['run']}")
            else:
                error = abs(float(new_value) - float(old_value))
                max_error = max(max_error, error)
                if error > 1e-10:
                    raise AssertionError(
                        f"Scenario-G {new_field} mismatch at {row['family']}/{row['run']}: {error}"
                    )
    return {
        "all_80_runs_match_frozen_scenario_G": True,
        "fields_checked_per_run": list(comparisons),
        "max_absolute_numeric_error": max_error,
        "absolute_tolerance": 1e-10,
    }


def _frozen_secondary_run_rows(frozen_rows: list[dict[str, str]]) -> dict[str, list[dict[str, Any]]]:
    output: dict[str, list[dict[str, Any]]] = {name: [] for name in SECONDARY_CALIBERS}
    scenario_map = {"RULE_A_NONEMPTY": "A", "STRICT_SINGLETON_NONEMPTY": "C"}
    for caliber, scenario in scenario_map.items():
        for old in frozen_rows:
            if old["scenario"] != scenario:
                continue
            def integer(field: str) -> int:
                return int(old[field])
            def number(field: str) -> float:
                return float(old[field])
            existing = integer("valid_unique_keys") + integer("empty_only_keys")
            output[caliber].append({
                "caliber": caliber,
                "source": f"existing frozen_reanalysis_v1 scenario {scenario}",
                "family": old["family"], "run": int(old["run"]),
                "expected_keys": integer("expected_keys"),
                "existing_keys": existing,
                "nonempty_keys": integer("valid_unique_keys"),
                "empty_only_keys": integer("empty_only_keys"),
                "missing_keys": integer("no_surviving_row_keys"),
                "raw_records": integer("raw_rows"),
                "nonempty_records": integer("valid_records"),
                "empty_records": integer("raw_rows") - integer("valid_records"),
                "empty_records_on_nonempty_keys": integer("empty_records_on_valid_keys"),
                "nonempty_duplicate_excess": integer("valid_records") - integer("valid_unique_keys"),
                "n_recall": integer("n_resolved_recall"),
                "n_return": integer("n_resolved_value"),
                "n_sign": integer("n_resolved_sign"),
                "sum_n_crit_recall": number("sum_n_crit"),
                "sum_hits_llm": number("sum_hits_llm"),
                "sum_hits_param": number("sum_hits_param"),
                "sum_delta_return": number("sum_delta_value"),
                "recall_llm": number("recall_llm"),
                "recall_param": number("recall_param"),
                "delta_recall": number("delta_recall"),
                "delta_return": number("delta_value"),
                "recall_conflicts": integer("conflict_recall_A"),
                "return_conflicts": integer("conflict_value_A"),
                "sign_conflicts": integer("conflict_sign_A"),
                "any_six_field_conflicts": "",
                "excluded_conflict_recall": integer("excluded_valid_recall"),
                "excluded_conflict_return": integer("excluded_valid_value"),
                "excluded_conflict_sign": integer("excluded_valid_sign"),
            })
    return output


def _secondary_family_results(frozen: dict[str, Any]) -> dict[str, Any]:
    answer: dict[str, Any] = {}
    for caliber, scenario in (("RULE_A_NONEMPTY", "A"), ("STRICT_SINGLETON_NONEMPTY", "C")):
        families: dict[str, Any] = {}
        for family in FAMILY_ORDER:
            old = frozen["scenarios"][scenario]["families"][family]
            equal = {
                "recall_llm": old["equal_run"]["recall_llm"],
                "recall_param": old["equal_run"]["recall_param"],
                "delta_recall": old["equal_run"]["delta_recall"],
                "delta_return": old["equal_run"]["delta_value"],
            }
            families[family] = {
                "n_recall": old["n_resolved_recall"],
                "n_return": old["n_resolved_value"],
                "n_sign": old["n_resolved_sign"],
                "sum_n_crit_recall": old["pooled_agent_day_sensitivity"]["sum_n_crit"],
                "equal_run": equal,
            }
        answer[caliber] = {
            "source": f"existing frozen scenario {scenario}; values copied, not recomputed",
            "definition": (
                "Nonempty picked only; metric-specific sufficient-statistic consistency; 86 gaps not imputed."
                if scenario == "A" else
                "Exactly one nonempty-picked record per retained key; all three metrics use that common cohort."
            ),
            "families": families,
        }
    return answer


def _scenario_effect_table(frozen: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for scenario in frozen["scenario_order"]:
        scenario_output = frozen["scenarios"][scenario]
        for family in FAMILY_ORDER:
            old = scenario_output["families"][family]
            equal = old["equal_run"]
            rows.append({
                "scenario": scenario,
                "rule": scenario_output["rule"],
                "family": family,
                "n_recall": old["n_resolved_recall"],
                "n_return": old["n_resolved_value"],
                "n_sign": old["n_resolved_sign"],
                "recall_llm": equal["recall_llm"]["estimate"],
                "recall_param": equal["recall_param"]["estimate"],
                "delta_recall": equal["delta_recall"]["estimate"],
                "delta_recall_ci95_low": equal["delta_recall"]["ci95"][0],
                "delta_recall_ci95_high": equal["delta_recall"]["ci95"][1],
                "delta_return": equal["delta_value"]["estimate"],
                "delta_return_ci95_low": equal["delta_value"]["ci95"][0],
                "delta_return_ci95_high": equal["delta_value"]["ci95"][1],
            })
    if len(rows) != 68:
        raise AssertionError("Expected 17 x 4 scenario-effect rows")
    return rows


def _scenario_ranges(frozen: dict[str, Any]) -> dict[str, Any]:
    answer: dict[str, Any] = {}
    order = frozen["scenario_order"]
    for family in FAMILY_ORDER:
        family_answer: dict[str, Any] = {}
        for metric, old_metric in (("delta_recall", "delta_recall"), ("delta_return", "delta_value")):
            values = {
                scenario: frozen["scenarios"][scenario]["families"][family]["equal_run"][old_metric]["estimate"]
                for scenario in order
            }
            signs = {scenario: (value > 0) - (value < 0) for scenario, value in values.items()}
            minimum = min(values.values())
            maximum = max(values.values())
            sequence = [signs[scenario] for scenario in order]
            family_answer[metric] = {
                "estimate_by_scenario": values,
                "minimum": minimum,
                "minimum_scenarios": [key for key, value in values.items() if value == minimum],
                "maximum": maximum,
                "maximum_scenarios": [key for key, value in values.items() if value == maximum],
                "max_minus_min": maximum - minimum,
                "sign_by_scenario": signs,
                "unique_signs": sorted(set(signs.values())),
                "sign_changed_across_scenarios": len(set(signs.values())) > 1,
                "adjacent_sign_changes_in_fixed_scenario_order": sum(
                    left != right for left, right in zip(sequence, sequence[1:])
                ),
                "same_nonzero_sign_all_17": len(set(signs.values())) == 1 and 0 not in signs.values(),
                "sign_scope": "Run-equal point-estimate signs; not interval-exclusion claims.",
            }
        answer[family] = family_answer
    return answer


def _future_logging_schema() -> dict[str, Any]:
    """Prospective schema only; this function never creates historical event values."""
    nullable_integer = {"type": ["integer", "null"], "minimum": 0}
    nullable_number = {"type": ["number", "null"], "minimum": 0}
    nullable_datetime = {"type": ["string", "null"], "format": "date-time"}
    stage_status = {
        "type": "string",
        "enum": ["success", "failure", "not_attempted", "not_applicable", "unknown"],
    }
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://example.invalid/sea.future-policy-delivery-consumption-attempt-v3.schema.json",
        "title": "Prospective SEA policy-attempt delivery and consumption log",
        "description": (
            "Future-only attempt/item schema. Unknown and not_attempted are explicit; no selected "
            "event implies delivery, opening, attendance, or consumption. Historical replay rows "
            "must not be backfilled without independent evidence."
        ),
        "type": "object",
        "additionalProperties": False,
        "required": [
            "schema_version", "run_key", "attempt_id", "policy_record_id", "policy_execution",
            "outcome_protocol", "items", "efficiency",
        ],
        "properties": {
            "schema_version": {"const": "sea.future-policy-delivery-consumption-attempt/v3"},
            "run_key": {
                "type": "object", "additionalProperties": False,
                "required": ["family", "run", "agent", "sim_day"],
                "properties": {
                    "family": {"type": "string", "minLength": 1},
                    "run": {"type": "integer", "minimum": 1},
                    "agent": {"type": "integer", "minimum": 0},
                    "sim_day": {"type": "integer", "minimum": 0},
                },
            },
            "attempt_id": {"type": "string", "minLength": 1},
            "policy_record_id": {"type": "string", "minLength": 1},
            "policy_execution": {
                "type": "object", "additionalProperties": False,
                "required": [
                    "started_at", "ended_at", "execution_status", "parser_status",
                    "transport_status", "empty_selection_reason", "raw_output_artifact_sha256",
                ],
                "properties": {
                    "started_at": nullable_datetime,
                    "ended_at": nullable_datetime,
                    "execution_status": {
                        "type": "string",
                        "enum": ["success", "explicit_abstention", "parse_failure",
                                 "execution_failure", "transport_failure", "unknown"],
                    },
                    "parser_status": {"type": "string", "enum": ["success", "failure", "not_attempted", "unknown"]},
                    "transport_status": stage_status,
                    "empty_selection_reason": {
                        "type": "string",
                        "enum": ["not_applicable", "explicit_abstention", "parse_failure",
                                 "execution_failure", "transport_failure", "unknown"],
                    },
                    "raw_output_artifact_sha256": {
                        "anyOf": [{"type": "string", "pattern": "^[0-9a-f]{64}$"}, {"type": "null"}]
                    },
                },
            },
            "outcome_protocol": {
                "type": "object", "additionalProperties": False,
                "required": [
                    "assignment_id", "primary_rule", "instrument_registry_sha256",
                    "threshold_sensitivity_ids", "attendance_decision_rule",
                    "machine_event_term",
                ],
                "properties": {
                    "assignment_id": {"type": "string", "minLength": 1},
                    "primary_rule": {
                        "const": "ALL_ASSIGNED_FAILURE_COMPOSITE_CONFIRMED_CONSUMPTION_OMISSION_V1"
                    },
                    "instrument_registry_sha256": {
                        "type": "string", "pattern": "^[0-9a-f]{64}$"
                    },
                    "threshold_sensitivity_ids": {
                        "type": "array", "minItems": 1, "uniqueItems": True,
                        "items": {"type": "string", "minLength": 1},
                    },
                    "attendance_decision_rule": {
                        "const": "VALID_READING_AND_CONTENT_LINKED_CONFIRMATION"
                    },
                    "machine_event_term": {
                        "const": "machine_ingestion_and_task_reference_not_human_attention"
                    },
                },
            },
            "items": {
                "type": "array",
                "description": "One entry per candidate item; empty selected lists remain distinguishable by policy_execution.",
                "items": {
                    "type": "object", "additionalProperties": False,
                    "required": ["item_id", "selected", "delivered", "opened", "attended"],
                    "properties": {
                        "item_id": {"type": "string", "minLength": 1},
                        "selected": {
                            "type": "object", "additionalProperties": False,
                            "required": ["status", "event_id", "timestamp", "rank", "selection_source"],
                            "properties": {
                                "status": {"type": "string", "enum": ["selected", "not_selected", "unknown"]},
                                "event_id": {"type": ["string", "null"]},
                                "timestamp": nullable_datetime,
                                "rank": nullable_integer,
                                "selection_source": {"type": ["string", "null"]},
                            },
                        },
                        "delivered": {
                            "type": "object", "additionalProperties": False,
                            "required": ["status", "event_id", "timestamp", "channel", "message_id", "error_code"],
                            "properties": {
                                "status": stage_status, "event_id": {"type": ["string", "null"]},
                                "timestamp": nullable_datetime, "channel": {"type": ["string", "null"]},
                                "message_id": {"type": ["string", "null"]},
                                "error_code": {"type": ["string", "null"]},
                            },
                        },
                        "opened": {
                            "type": "object", "additionalProperties": False,
                            "required": ["status", "event_id", "timestamp", "instrument"],
                            "properties": {
                                "status": stage_status, "event_id": {"type": ["string", "null"]},
                                "timestamp": nullable_datetime, "instrument": {"type": ["string", "null"]},
                            },
                        },
                        "attended": {
                            "type": "object", "additionalProperties": False,
                            "description": (
                                "Operational attendance measurement only; not latent comprehension or learning. "
                                "Opening is not sufficient. Failed or invalid measurement is unknown, not observed non-consumption."
                            ),
                            "required": [
                                "status", "measurement_status", "event_id", "timestamp", "duration_ms",
                                "instrument", "instrument_version", "threshold_id", "validation_status",
                                "assessor_blinding", "evidence_pointer",
                            ],
                            "properties": {
                                "status": stage_status,
                                "measurement_status": {
                                    "type": "string",
                                    "enum": ["complete", "incomplete", "invalid", "not_attempted", "unknown"],
                                },
                                "event_id": {"type": ["string", "null"]},
                                "timestamp": nullable_datetime, "duration_ms": nullable_number,
                                "instrument": {"type": ["string", "null"]},
                                "instrument_version": {"type": ["string", "null"]},
                                "threshold_id": {"type": ["string", "null"]},
                                "validation_status": {
                                    "type": "string",
                                    "enum": ["validated", "not_validated", "expired", "unknown"],
                                },
                                "assessor_blinding": {
                                    "type": "string",
                                    "enum": ["arm_and_model_blind", "not_blind", "not_applicable", "unknown"],
                                },
                                "evidence_pointer": {"type": ["string", "null"]},
                            },
                        },
                        "machine_ingestion_and_task_reference": {
                            "type": "object", "additionalProperties": False,
                            "description": (
                                "Separate machine event: complete content entered a declared task context and a task "
                                "operation referenced the receipt. It is not human attention, comprehension, or proof "
                                "of downstream information use."
                            ),
                            "required": ["status", "content_sha256", "context_receipt_sha256",
                                         "task_reference_sha256", "evidence_pointer"],
                            "properties": {
                                "status": {"type": "string", "enum": ["present", "absent", "unknown"]},
                                "content_sha256": {"type": ["string", "null"], "pattern": "^[0-9a-f]{64}$"},
                                "context_receipt_sha256": {"type": ["string", "null"], "pattern": "^[0-9a-f]{64}$"},
                                "task_reference_sha256": {"type": ["string", "null"], "pattern": "^[0-9a-f]{64}$"},
                                "evidence_pointer": {"type": ["string", "null"]},
                            },
                        },
                    },
                },
            },
            "efficiency": {
                "type": "object", "additionalProperties": False,
                "required": [
                    "measurement_status", "calls", "input_tokens", "output_tokens",
                    "cost", "latency_ms", "retries",
                ],
                "properties": {
                    "measurement_status": {"type": "string", "enum": ["complete", "partial", "unavailable"]},
                    "calls": nullable_integer,
                    "input_tokens": nullable_integer,
                    "output_tokens": nullable_integer,
                    "cost": {
                        "type": "object", "additionalProperties": False,
                        "required": ["amount", "currency"],
                        "properties": {
                            "amount": nullable_number,
                            "currency": {"type": ["string", "null"], "minLength": 3},
                        },
                    },
                    "latency_ms": nullable_number,
                    "retries": nullable_integer,
                },
            },
        },
        "$comment": (
            "Validation must additionally enforce timestamp order and prohibit downstream success "
            "after an upstream failure/not_attempted status. Attended is the operational terminal attendance "
            "measurement, not latent actual consumption. Positive/negative attendance requires complete validated measurement; instrument "
            "failure remains unknown. The registered primary analysis codes unknown terminal outcomes "
            "as failure-composite omission without rewriting raw attendance. Nullable measurements "
            "require an explicit partial/unavailable measurement_status; null is not zero."
        ),
    }


def _ledger_rows(states: Sequence[KeyState]) -> Iterator[dict[str, Any]]:
    for state in states:
        yield {
            "key": [state.family, state.run, state.agent, state.sim_day],
            "status": "MISSING_KEY" if not state.existing else "EMPTY_ONLY" if state.empty_only else "NONEMPTY",
            "n_records": len(state.records),
            "n_nonempty_records": sum(record.nonempty for record in state.records),
            "n_empty_records": state.n_empty,
            "canonical": {
                "hits_param": state.canonical.hits_param,
                "n_crit": state.canonical.n_crit,
                "value_param": state.canonical.value_param,
            },
            "conflicts_on_nonempty_records": {
                "recall": state.recall_conflict,
                "citation_return": state.return_conflict,
                "paired_sign": state.sign_conflict,
                "any_six_field": state.any_six_field_conflict,
            },
            "ALL_EXISTING_RECORD_MEAN_ZERO_EMPTY": None if not state.existing else {
                "hits_llm": state.full_hits_llm,
                "hits_param": state.canonical.hits_param,
                "n_crit": state.canonical.n_crit,
                "delta_citation_return": state.full_delta_return,
                "paired_sign": None,
                "paired_sign_status": "NOT_APPLICABLE_FRACTIONAL_ATTEMPT_MEAN",
            },
            "ALL_EXPECTED_RECORD_MEAN_ZERO_EMPTY_NO_ROW": {
                "hits_llm": 0.0 if not state.existing else state.full_hits_llm,
                "hits_param": state.canonical.hits_param,
                "n_crit": state.canonical.n_crit,
                "delta_citation_return": (-float(state.canonical.value_param)
                                          if not state.existing else state.full_delta_return),
                "paired_sign": None,
                "paired_sign_status": "NOT_APPLICABLE_FRACTIONAL_ATTEMPT_MEAN",
                "no_row_zero_assignment": not state.existing,
            },
            "METRIC_RESOLVED_ZERO_EMPTY": {
                "recall_hits_llm_hits_param_n_crit": state.resolved_recall,
                "delta_citation_return": state.resolved_delta_return,
                "paired_sign": state.resolved_sign,
            },
            "sources": [
                {
                    "file": record.source_file, "line": record.source_line,
                    "picked_count": len(record.picked), "reason_class": record.reason_class,
                    "raw_consume_class": record.raw_consume_class,
                }
                for record in state.records
            ],
            "actual_delivery_open_attendance_consumption_observed": False,
        }


def _csv_text(rows: Sequence[dict[str, Any]], columns: Sequence[str]) -> str:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=columns, extrasaction="ignore", lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow({key: "" if row.get(key) is None else row.get(key, "") for key in columns})
    return buffer.getvalue()


def _fmt(value: float | None, signed: bool = False) -> str:
    if value is None:
        return "NA"
    return format(value, f"{'+' if signed else ''}.6f")


def _estimate_ci(item: dict[str, Any], signed: bool = False) -> str:
    return (f"{_fmt(item['estimate'], signed)} "
            f"[{_fmt(item['ci95'][0], signed)}, {_fmt(item['ci95'][1], signed)}]")


def _new_report_table(result: dict[str, Any]) -> list[str]:
    lines = [
        "| Family | n recall / return / sign | sum n_crit | Selected recall | Parametric recall | Δrecall [95% run CI] | Δcitation return [95% run CI] |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for family in FAMILY_ORDER:
        item = result["families"][family]
        equal = item["equal_run"]
        lines.append(
            f"| {family} | {item['n_recall']} / {item['n_return']} / "
            f"{item['n_sign'] if item['n_sign'] is not None else 'NA'} | "
            f"{item['sum_n_crit_recall']:.0f} | {_estimate_ci(equal['recall_llm'])} | "
            f"{_estimate_ci(equal['recall_param'])} | {_estimate_ci(equal['delta_recall'], True)} | "
            f"{_estimate_ci(equal['delta_return'], True)} |"
        )
    return lines


def render_report(summary: dict[str, Any]) -> str:
    structure = summary["population_accounting"]
    obs = summary["observability"]
    counts = obs["counts"]
    lines = [
        "# Frozen replay selected-proxy consumption-caliber audit",
        "",
        f"**Status: `{STATUS}`.** No model calls, interventions, or new delivery/open/consumption observations.",
        "",
        "`picked` identifies a **selected proxy only**. Neither selected recall nor selected "
        "citation-weighted return is actual consumption, decision utility, welfare, or an end-to-end effect.",
        "",
        "## 1. Observable records and identification boundary",
        "",
        f"- {counts['accepted_shards']} hash-verified shards; {counts['nonblank_lines']} nonblank JSONL rows; "
        f"{counts['valid_parseable_policy_records']} structurally parseable policy records; "
        f"{counts['empty_records']} have `picked=[]`.",
        f"- Current-file transport failures: **{counts.get('file_transport_failures', 0)}**; JSONL decode/parse failures: "
        f"**{counts.get('jsonl_decode_or_parse_failures', 0)}**; invalid policy records: "
        f"**{counts.get('invalid_policy_records', 0)}**. Separately, **{counts.get('policy_reported_parse_error_records', 0)}** "
        f"stored rows say `reason='parse-error'`; **{counts.get('empty_records_with_other_reason', 0)}** empty rows have other reason text.",
        "- Historical API transport failures are not observable from these JSONL fields and are not inferred from dispatch logs. "
        "Current successful file reads do not establish historical delivery or execution success.",
        "- The records contain no delivered/opened/attended or item-level actual-consumption fields. "
        "`raw_consume` is a raw-output diagnostic and `impulse_consumed` concerns injected impulses; neither repairs the missing chain.",
        "- **Historical logs cannot distinguish valid abstention from silent empty-selection execution failure.** "
        "This audit therefore labels zero only as a selected-proxy sensitivity assignment, never as observed actual non-consumption.",
        "",
        "## 2. Existing-key accounting and unresolved duplicates",
        "",
        "An existing key has at least one structurally parseable policy record. There are "
        f"**{structure['existing_keys']} = {structure['nonempty_keys']} nonempty-key + {structure['empty_only_keys']} empty-only** "
        f"existing keys. **{structure['missing_keys']}** no-row keys remain missing in the existing-key and resolved calibers; "
        "only the explicitly named conservative all-expected-key caliber assigns them selected-proxy zero. "
        f"The {structure['empty_records_on_nonempty_keys']} empty records sharing nonempty keys are counted in the all-record-mean "
        "caliber and reported separately in the resolved caliber; they are not extra independent keys.",
        "",
        "| Family | Expected | Nonempty keys | Empty-only | Existing frame | Missing | Empty rows on nonempty keys | Stored parse-error rows |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for family in FAMILY_ORDER:
        item = structure["by_family"][family]
        parse_errors = obs["policy_reported_parse_errors_by_family"][family].get("POLICY_PARSE_ERROR", 0)
        lines.append(
            f"| {family} | {item['expected_keys']} | {item['nonempty_keys']} | {item['empty_only_keys']} | "
            f"{item['existing_keys']} | {item['missing_keys']} | {item['empty_records_on_nonempty_keys']} | {parse_errors} |"
        )
    lines += [
        f"| **Total** | **{structure['expected_keys']}** | **{structure['nonempty_keys']}** | "
        f"**{structure['empty_only_keys']}** | **{structure['existing_keys']}** | **{structure['missing_keys']}** | "
        f"**{structure['empty_records_on_nonempty_keys']}** | **{counts.get('policy_reported_parse_error_records', 0)}** |",
        "",
        f"Nonempty duplicate groups: **{structure['nonempty_duplicate_key_groups']}**; excess nonempty records: "
        f"**{structure['nonempty_duplicate_excess']}**. Metric conflicts are recall **{structure['recall_conflicts_nonempty']}**, "
        f"citation return **{structure['return_conflicts_nonempty']}**, paired sign **{structure['sign_conflicts_nonempty']}**, "
        f"and any six-field conflict **{structure['any_six_field_conflicts_nonempty']}**. No conflict is silently assigned zero.",
        "",
        "Key flow: 72,000 expected keys = 71,970 existing keys + 30 no-row keys; "
        "71,970 existing keys = 71,914 nonempty-selection keys + 56 empty-only keys. "
        "The 73,704 raw records include 157 empty records, of which 101 share nonempty keys. "
        "The three calibers differ only in no-row and conflict disposition, not in the frozen raw inputs.",
        "",
        "## 3. Complete all-existing-key zero-empty sensitivity (`ALL_EXISTING_RECORD_MEAN_ZERO_EMPTY`)",
        "",
        "Every existing key contributes once to recall and return. Within a key, every raw policy record has equal weight, "
        "including each `picked=[]` record as zero selected hits/return. If `h̄_k` is the record-averaged selected hits for key k, "
        "run recall is `sum_k h̄_k / sum_k n_crit,k` (a ratio of sums), **not** `mean_k(h̄_k/n_crit,k)`; keys with more critical "
        "opportunities therefore have greater weight. Citation return is the equal-key mean of within-key attempt-mean contrasts. "
        "This gives complete existing-key support but estimates a recorded-attempt mean; it does not identify the historically "
        "correct attempt. Paired sign is not applicable to fractional means.",
        "",
    ]
    lines += _new_report_table(summary["new_calibers"]["ALL_EXISTING_RECORD_MEAN_ZERO_EMPTY"])
    lines += [
        "",
        "Family estimates are unweighted run means. Intervals are exploratory 10,000-draw whole-run percentile bootstrap intervals "
        "(seed 42); Q/G have only 10 runs. They omit corpus, duplicate-arbitration, missingness, and model-dependence uncertainty.",
        "",
        "## 4. Conservative all-expected-key zero-empty/no-row sensitivity (`ALL_EXPECTED_RECORD_MEAN_ZERO_EMPTY_NO_ROW`)",
        "",
        "This post-hoc descriptive convention extends the recorded-attempt mean to all 72,000 expected keys by assigning "
        "selected-proxy zero to the 30 no-row keys. It answers a different data-quality question from the existing-key caliber: "
        "what if absence of a record is treated as selection failure? It is not a recovered historical all-assigned analysis, "
        "not actual consumption, and not a prospective primary endpoint. Conflict records remain attempt means, as in the "
        "existing-key caliber; the conflict-refusing caliber below answers a separate question.",
        "",
    ]
    lines += _new_report_table(summary["new_calibers"]["ALL_EXPECTED_RECORD_MEAN_ZERO_EMPTY_NO_ROW"])
    lines += [
        "",
        "## 5. Conflict-refusing zero-empty sensitivity (`METRIC_RESOLVED_ZERO_EMPTY` = frozen G)",
        "",
        "Empty-only keys are zero-filled. Nonempty duplicates enter a metric only when that metric's sufficient statistic is consistent; "
        "empty rows sharing a nonempty key do not create a new key or overwrite the nonempty Rule-A value. Exact recall/return/sign "
        f"denominators are **{structure['resolved_zero_empty_recall']} / {structure['resolved_zero_empty_return']} / "
        f"{structure['resolved_zero_empty_sign']}**. The 30 no-row keys and each affected conflict remain excluded, not zero-filled.",
        "",
    ]
    lines += _new_report_table(summary["new_calibers"]["METRIC_RESOLVED_ZERO_EMPTY"])
    validation = summary["validation"]["resolved_zero_empty_vs_frozen_G"]
    lines += [
        "",
        f"Raw recomputation matches frozen scenario G for **80/80 runs** across denominators, sufficient sums, recall, and return "
        f"(maximum absolute numeric error {validation['max_absolute_numeric_error']:.3g}).",
        "",
        "## 6. Secondary existing calibers: nonempty Rule A versus strict singleton",
        "",
        "These are existing frozen outputs, not replacements for the designated retrospective descriptive caliber. Rule A uses different resolved "
        "cohorts by metric: **71,573 recall, 70,676 return, 71,618 sign**. Strict singleton uses exactly one nonempty record per key "
        "and therefore a common **70,306-key** cohort. Their population difference prevents interpreting numerical changes as an isolated duplicate effect.",
        "",
        "| Caliber | Family | n recall / return / sign | Selected recall | Parametric recall | Δrecall [CI] | Δcitation return [CI] |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for caliber in SECONDARY_CALIBERS:
        result = summary["secondary_existing_calibers"][caliber]
        for family in FAMILY_ORDER:
            item = result["families"][family]
            equal = item["equal_run"]
            lines.append(
                f"| {caliber} | {family} | {item['n_recall']} / {item['n_return']} / {item['n_sign']} | "
                f"{_estimate_ci(equal['recall_llm'])} | {_estimate_ci(equal['recall_param'])} | "
                f"{_estimate_ci(equal['delta_recall'], True)} | {_estimate_ci(equal['delta_return'], True)} |"
            )
    lines += [
        "",
        "## 7. All 17 frozen scenarios: effect ranges and point-estimate sign changes",
        "",
        "Ranges below use run-equal point estimates copied from `frozen_reanalysis_v1/summary.json`; no scenario was rerun or hidden. "
        "Sign change means a change in point-estimate sign across scenarios, not whether an interval contains zero.",
        "",
        "| Family | Δrecall min–max | Δrecall sign changes | Δcitation return min–max | Return sign changes |",
        "|---|---:|---:|---:|---:|",
    ]
    for family in FAMILY_ORDER:
        item = summary["frozen_17_scenario_ranges"][family]
        recall = item["delta_recall"]
        ret = item["delta_return"]
        lines.append(
            f"| {family} | {_fmt(recall['minimum'], True)} to {_fmt(recall['maximum'], True)} | "
            f"{recall['adjacent_sign_changes_in_fixed_scenario_order']} | "
            f"{_fmt(ret['minimum'], True)} to {_fmt(ret['maximum'], True)} | "
            f"{ret['adjacent_sign_changes_in_fixed_scenario_order']} |"
        )
    lines += [
        "",
        "For every family and both contrasts, the minimum occurs at `I_favor_param` and `J_lower_value`, and the maximum at "
        "`I_favor_llm` and `J_upper_value`. Recall stays positive in all 17 scenarios for every family. Citation return stays positive "
        "for C/Q and negative for O/G in all 17; there are **zero point-estimate sign changes**. This does not make the intervals or "
        "the causal interpretation uniformly robust.",
        "",
        "All 68 scenario×family estimates, intervals, and exact metric denominators are in `scenario_effects.csv`; min/max scenario IDs "
        "and sign vectors are machine-readable in `summary.json`.",
        "",
        "## 8. Prospective logging schema (not historical backfill)",
        "",
        "`future_logging_schema.json` is a JSON Schema for one policy attempt with explicit attempt identity, parser/execution/transport "
        "status, empty-selection reason, and per-item **selected → delivered → opened → operational attendance** event objects. "
        "Attended is the single terminal consumption event and carries instrument/version, threshold, validation, blinding, and evidence fields. "
        "The registered primary outcome is all-assigned failure-composite omission; unknown raw attendance is not rewritten as observed non-consumption. "
        "The schema also requires explicit `calls`, `input_tokens`, `output_tokens`, `cost{amount,currency}`, `latency_ms`, and `retries`; unknown measurements are null, not zero.",
        "The old replay fails the historical information requirement for this chain, so no synthetic old events or efficiency values are emitted.",
        "",
        "## 9. Reproduction and files",
        "",
        "```bash",
        "PYTHONDONTWRITEBYTECODE=1 python3 sim/sea_pilot/audit_v110_consumption_caliber.py --write",
        "```",
        "",
        "Artifacts: `summary.json`, `REPORT.md`, per-run `run_metrics.csv`, all-scenario `scenario_effects.csv`, compressed unique-key "
        "`key_ledger.jsonl.gz`, prospective `future_logging_schema.json`, and hash-verified `input_manifest.json`. "
        "The ledger gives exact key status, conflict disposition, sources, and both new-caliber values without rationale text.",
        "",
        "Interpretation remains post hoc and exploratory: one frozen 30-day corpus, retrospective citation labels, upstream digest conditioning, "
        "semi-oracle construction, possible nonrandom missingness, and confounded family/backend/prompt/runtime configurations. "
        "No result here measures delivered/opened/attended/actual consumption or human welfare.",
        "",
    ]
    return "\n".join(lines)


def _atomic_write(path: Path, data: bytes) -> None:
    temporary = path.with_name(f".{path.name}.tmp-{os.getpid()}")
    try:
        with temporary.open("xb") as handle:
            handle.write(data)
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def emit(
    summary: dict[str, Any], report: str, run_csv: str, scenario_csv: str,
    states: Sequence[KeyState], future_schema: dict[str, Any], manifest_document: dict[str, Any],
    force: bool,
) -> None:
    targets = {name: OUTDIR / name for name in ARTIFACT_NAMES}
    existing = [str(path) for path in targets.values() if path.exists()]
    if existing and not force:
        raise FileExistsError(f"Refusing to overwrite dedicated artifacts without --force: {existing}")
    OUTDIR.mkdir(parents=True, exist_ok=True)
    _atomic_write(targets["input_manifest.json"], (
        json.dumps(manifest_document, ensure_ascii=False, indent=1, allow_nan=False) + "\n"
    ).encode("utf-8"))
    _atomic_write(targets["future_logging_schema.json"], (
        json.dumps(future_schema, ensure_ascii=False, indent=1, allow_nan=False) + "\n"
    ).encode("utf-8"))
    _atomic_write(targets["run_metrics.csv"], run_csv.encode("utf-8"))
    _atomic_write(targets["scenario_effects.csv"], scenario_csv.encode("utf-8"))
    _atomic_write(targets["REPORT.md"], report.encode("utf-8"))

    ledger_path = targets["key_ledger.jsonl.gz"]
    temporary = ledger_path.with_name(f".{ledger_path.name}.tmp-{os.getpid()}")
    try:
        with temporary.open("xb") as raw:
            with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as compressed:
                for row in _ledger_rows(states):
                    line = json.dumps(row, ensure_ascii=False, sort_keys=True,
                                      separators=(",", ":"), allow_nan=False) + "\n"
                    compressed.write(line.encode("utf-8"))
        os.replace(temporary, ledger_path)
    finally:
        if temporary.exists():
            temporary.unlink()
    _atomic_write(targets["summary.json"], (
        json.dumps(summary, ensure_ascii=False, indent=1, allow_nan=False) + "\n"
    ).encode("utf-8"))


def build_analysis() -> tuple[
    dict[str, Any], dict[str, list[dict[str, Any]]], list[dict[str, Any]],
    list[KeyState], dict[str, Any], dict[str, Any],
]:
    frozen, frozen_run_rows = _load_frozen()
    loaded = load_raw(RESULTS, frozen["input_manifest"])
    canonical = canonical_days(loaded.runs)
    states = build_states(loaded.runs, canonical)
    structure = _structure_for_states(states)
    structure["by_family"] = {
        family: _structure_for_states([state for state in states if state.family == family])
        for family in FAMILY_ORDER
    }
    _validate_raw_against_frozen(structure, frozen)

    new_run_rows = compute_new_run_rows(states)
    new_results = {
        "ALL_EXISTING_RECORD_MEAN_ZERO_EMPTY": {
            "definition": (
                "All 71,970 existing keys; equal-weight mean of all raw policy records within each key; "
                "picked=[] contributes selected-proxy zero; 30 no-row keys missing; no conflict exclusions."
            ),
            "analysis_role": "Designated retrospective descriptive caliber; not a prospective primary outcome or intention-to-treat analysis.",
            "estimand_caution": "Recorded-attempt mean, not recovered historical single-attempt truth or actual consumption.",
            **_aggregate_new(new_run_rows["ALL_EXISTING_RECORD_MEAN_ZERO_EMPTY"]),
        },
        "METRIC_RESOLVED_ZERO_EMPTY": {
            "definition": (
                "Frozen scenario G: empty-only keys zero-filled; nonempty Rule-A sufficient-statistic "
                "conflicts excluded separately by metric; 30 no-row keys missing."
            ),
            "estimand_caution": "Resolved existing-key selected-proxy sensitivity, not actual consumption.",
            **_aggregate_new(new_run_rows["METRIC_RESOLVED_ZERO_EMPTY"]),
        },
        "ALL_EXPECTED_RECORD_MEAN_ZERO_EMPTY_NO_ROW": {
            "definition": (
                "All 72,000 expected keys; existing keys use the recorded-attempt mean; "
                "30 no-row keys are assigned selected-proxy zero as a conservative selection-failure sensitivity."
            ),
            "analysis_role": "Post-hoc conservative descriptive sensitivity; not a prospective primary outcome or actual-consumption analysis.",
            "estimand_caution": "No-row zero is an assumption about selection failure, not recovered historical consumption.",
            **_aggregate_new(new_run_rows["ALL_EXPECTED_RECORD_MEAN_ZERO_EMPTY_NO_ROW"]),
        },
    }
    validation_g = _validate_resolved_is_frozen_g(
        new_run_rows["METRIC_RESOLVED_ZERO_EMPTY"], frozen_run_rows
    )
    secondary_run_rows = _frozen_secondary_run_rows(frozen_run_rows)
    all_run_rows = [
        row for caliber in (*NEW_CALIBERS, *SECONDARY_CALIBERS)
        for row in (new_run_rows | secondary_run_rows)[caliber]
    ]
    scenario_rows = _scenario_effect_table(frozen)
    ranges = _scenario_ranges(frozen)
    future_schema = _future_logging_schema()

    manifest_document = {
        "schema": "sea.v110.selected-proxy-input-manifest/v2",
        "raw_replay_shards": loaded.manifest,
        "raw_replay_manifest_sha256": _sha256_json(loaded.manifest),
        "frozen_outputs": [
            {"path": _relative(path), "size_bytes": path.stat().st_size, "sha256": _sha256_file(path)}
            for path in (FROZEN_SUMMARY, FROZEN_RUN_METRICS)
        ],
        "analysis_script": {
            "path": _relative(Path(__file__).resolve()),
            "sha256": _sha256_file(Path(__file__).resolve()),
        },
        "all_292_raw_shards_match_frozen_reanalysis_manifest": True,
        "skipped_non_main_tags": loaded.skipped,
    }

    # Keep the summary self-contained about provenance without duplicating 292 entries.
    summary: dict[str, Any] = {
        "schema": SCHEMA,
        "script_version": VERSION,
        "status": STATUS,
        "new_model_calls": 0,
        "new_delivery_open_attendance_or_consumption_observations": 0,
        "read_only_inputs": True,
        "post_hoc": True,
        "cross_corpus_confirmatory": False,
        "unique_key": "(family, run, agent, sim_day)",
        "selected_proxy_semantics": {
            "picked": "Policy-selected IDs in the fixed digest; not delivered/opened/attended/actually consumed items.",
            "recall": "Per key, average selected hits over raw attempts; per run, divide the sum of these key numerators by the sum of canonical n_crit. Keys with more critical opportunities weigh more; family estimates are equal run means.",
            "citation_return": "Selected sum of log1p(2026 citations); contrast is value_llm-value_param, not welfare or decision utility.",
            "empty_picked": "Zero selected hits and zero selected citation return only; never evidence of actual non-consumption.",
        },
        "observability": loaded.observability,
        "population_accounting": structure,
        "population_identities": {
            "expected_equals_existing_plus_missing": (
                structure["expected_keys"] == structure["existing_keys"] + structure["missing_keys"]
            ),
            "existing_equals_nonempty_plus_empty_only": (
                structure["existing_keys"] == structure["nonempty_keys"] + structure["empty_only_keys"]
            ),
            "raw_records_equals_existing_plus_all_record_excess": (
                structure["raw_records"] == structure["existing_keys"]
                + structure["all_record_excess_over_existing_keys"]
            ),
            "empty_records_equals_empty_only_plus_empty_on_nonempty": (
                structure["empty_records"] == structure["empty_only_keys"]
                + structure["empty_records_on_nonempty_keys"]
            ),
        },
        "new_calibers": new_results,
        "secondary_existing_calibers": _secondary_family_results(frozen),
        "rule_A_metric_specific_denominators": {
            "recall": frozen["structure"]["resolved_recall_A"],
            "citation_return": frozen["structure"]["resolved_value_A"],
            "paired_sign": frozen["structure"]["resolved_sign_A"],
        },
        "strict_singleton_common_denominator": frozen["structure"]["resolved_C"],
        "bootstrap": {
            "unit": "whole run within family", "resamples": BOOTSTRAP_B,
            "seed": BOOTSTRAP_SEED, "interval": "percentile 95%",
            "new_calibers_recomputed": True, "frozen_A_C_intervals_copied": True,
            "scope": "Exploratory run variation only; no missingness/arbitration/shared-corpus/model uncertainty.",
        },
        "frozen_17_scenario_order": frozen["scenario_order"],
        "frozen_17_scenario_ranges": ranges,
        "validation": {
            "all_292_shards_match_frozen_hash_size_linecount": True,
            "raw_structure_matches_frozen_reanalysis": True,
            "resolved_zero_empty_vs_frozen_G": validation_g,
            "all_17_scenarios_and_1360_frozen_run_rows_loaded": True,
            "all_72000_keys_in_ledger": len(states) == NOMINAL_TOTAL,
        },
        "future_logging_schema": {
            "artifact": "future_logging_schema.json",
            "schema_sha256": _sha256_json(future_schema),
            "prospective_only": True,
            "historical_backfill_performed": False,
            "required_stage_chain": ["selected", "delivered", "opened", "operational_attendance"],
            "primary_missing_outcome_rule": "ALL_ASSIGNED_FAILURE_COMPOSITE_CONFIRMED_CONSUMPTION_OMISSION_V1",
            "attendance_decision_rule": "VALID_READING_AND_CONTENT_LINKED_CONFIRMATION",
            "machine_event_term": "machine_ingestion_and_task_reference_not_human_attention",
            "attendance_measurement_fields": [
                "instrument", "instrument_version", "threshold_id", "validation_status",
                "assessor_blinding", "evidence_pointer",
            ],
            "required_efficiency_fields": [
                "calls", "input_tokens", "output_tokens", "cost.amount", "cost.currency",
                "latency_ms", "retries",
            ],
        },
        "artifacts": {
            "names": list(ARTIFACT_NAMES), "run_metric_rows": len(all_run_rows),
            "scenario_effect_rows": len(scenario_rows), "key_ledger_rows": len(states),
        },
        "environment": {
            "python_version": sys.version,
            "python_version_info": list(sys.version_info[:3]),
            "numpy_version": np.__version__,
            "platform": platform.platform(),
            "analysis_script": _relative(Path(__file__).resolve()),
            "analysis_script_sha256": _sha256_file(Path(__file__).resolve()),
            "frozen_summary_sha256": _sha256_file(FROZEN_SUMMARY),
            "frozen_run_metrics_sha256": _sha256_file(FROZEN_RUN_METRICS),
            "input_manifest_sha256": manifest_document["raw_replay_manifest_sha256"],
        },
        "limitations": [
            "Post-hoc selected-proxy retrospective description on one fixed corpus, not an all-assigned actual-consumption experiment.",
            "Empty picked cannot be retrospectively classified as valid abstention versus silent execution failure.",
            "The all-record mean is a different estimand and does not identify a historically correct duplicate.",
            "The metric-resolved caliber excludes affected conflicts and all 30 no-row keys rather than inventing outcomes.",
            "Run bootstrap does not capture nonrandom missingness, duplicate arbitration, shared corpus/digests/labels, or model dependence.",
            "Citation return is retrospective academic impact, not ex-ante decision value or welfare.",
        ],
    }
    if not all(summary["population_identities"].values()):
        raise AssertionError("Population accounting identity failed")
    return summary, all_run_rows, scenario_rows, states, future_schema, manifest_document


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true",
                        help="Write only sim/pilot/results/v110_consumption_caliber; default stdout only")
    parser.add_argument("--force", action="store_true",
                        help="With --write, permit replacement of the seven dedicated artifacts")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    if args.force and not args.write:
        raise SystemExit("--force is meaningful only together with --write")
    summary, run_rows, scenario_rows, states, future_schema, manifest = build_analysis()
    report = render_report(summary)
    if args.write:
        run_csv = _csv_text(run_rows, RUN_COLUMNS)
        scenario_columns = list(scenario_rows[0])
        scenario_csv = _csv_text(scenario_rows, scenario_columns)
        emit(summary, report, run_csv, scenario_csv, states, future_schema, manifest, args.force)
        print(f"Wrote {len(ARTIFACT_NAMES)} selected-proxy audit artifacts to {_relative(OUTDIR)}")
    else:
        print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
